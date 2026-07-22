// scanner/fingerprint.go — nmap-style probe/response service fingerprinting.
//
// This is the "deep scan" upgrade over port-number guessing. Following nmap's
// service-detection model (https://nmap.org/book/vscan-technique.html):
//
//   1. Send a sequence of named PROBES to the open port. The NULL probe just
//      listens (many services greet you); active probes send a protocol-shaped
//      request (HTTP GET, TLS ClientHello marker, etc.).
//   2. Match each response against a table of regex SIGNATURES that extract the
//      product name and version.
//   3. Return the highest-confidence match. If nothing matches but bytes came
//      back, emit the raw fingerprint so an operator can add a signature later.
//
// This yields product+version WITHOUT requiring nmap to be installed; the nmap
// gate (nmap.go) is then an optional cross-check/enrichment, not a dependency.
package scanner

import (
	"context"
	"fmt"
	"net"
	"regexp"
	"sort"
	"strings"
	"time"
)

// probe is one request we send to elicit an identifying response.
type probe struct {
	name  string
	send  []byte // empty = NULL probe (just read the greeting)
	ports map[int]bool
}

// signature matches a probe response and extracts service metadata.
type signature struct {
	service    string
	re         *regexp.Regexp
	product    string // may contain $1/$2 backrefs into the regex groups
	version    string
	confidence int // 1-10, higher wins
}

// Curated probe set — ordered by how commonly they succeed.
var probes = []probe{
	{name: "NULL", send: nil}, // read-first: SSH/FTP/SMTP/MySQL/Redis greet immediately
	{name: "GenericLines", send: []byte("\r\n\r\n")},
	{name: "HTTPGet", send: []byte("GET / HTTP/1.0\r\nHost: localhost\r\nUser-Agent: Mozilla/5.0\r\n\r\n"),
		ports: map[int]bool{80: true, 8080: true, 8000: true, 8443: true, 443: true, 8888: true, 3000: true, 5000: true, 9200: true, 8081: true}},
	{name: "Help", send: []byte("HELP\r\n")},
	{name: "RedisPing", send: []byte("PING\r\n"), ports: map[int]bool{6379: true}},
	{name: "RTSPOptions", send: []byte("OPTIONS / RTSP/1.0\r\nCSeq: 1\r\n\r\n"), ports: map[int]bool{554: true, 7000: true, 8554: true}},
}

// Signature table — regexes compiled once at init. Ordered high→low confidence.
var signatures = buildSignatures()

func buildSignatures() []signature {
	raw := []struct {
		service    string
		pattern    string
		product    string
		version    string
		confidence int
	}{
		// SSH
		{"ssh", `^SSH-([\d.]+)-(OpenSSH[_\w.]*)`, "$2", "$1", 10},
		{"ssh", `^SSH-([\d.]+)-([\w.\-]+)`, "$2", "$1", 8},
		// FTP
		{"ftp", `^220[ -].*?FileZilla Server[^\d]*([\d.]+)`, "FileZilla ftpd", "$1", 10},
		{"ftp", `^220[ -].*?vsFTPd ([\d.]+)`, "vsftpd", "$1", 10},
		{"ftp", `^220[ -].*?ProFTPD ([\d.]+)`, "ProFTPD", "$1", 10},
		{"ftp", `^220[ -].*?Pure-FTPd`, "Pure-FTPd", "", 9},
		{"ftp", `^220[- ]`, "ftp", "", 5},
		// SMTP
		{"smtp", `^220[ -].*?Postfix`, "Postfix smtpd", "", 9},
		{"smtp", `^220[ -].*?Exim ([\d.]+)`, "Exim smtpd", "$1", 10},
		{"smtp", `^220[ -].*?Sendmail[^\d]*([\d.\/]+)`, "Sendmail", "$1", 10},
		{"smtp", `^220[ -].*?Microsoft ESMTP MAIL Service.*?([\d.]+)`, "Microsoft ESMTP", "$1", 10},
		{"smtp", `^220[ -].*?SMTP`, "smtp", "", 5},
		// POP3 / IMAP
		{"pop3", `^\+OK.*?Dovecot`, "Dovecot pop3d", "", 9},
		{"pop3", `^\+OK`, "pop3", "", 5},
		{"imap", `^\* OK.*?Dovecot`, "Dovecot imapd", "", 9},
		{"imap", `^\* OK.*?Courier-IMAP`, "Courier imapd", "", 9},
		{"imap", `^\* OK`, "imap", "", 5},
		// HTTP — Server header
		{"http", `Server: nginx/([\d.]+)`, "nginx", "$1", 10},
		{"http", `Server: nginx`, "nginx", "", 8},
		{"http", `Server: Apache/([\d.]+)`, "Apache httpd", "$1", 10},
		{"http", `Server: Apache`, "Apache httpd", "", 8},
		{"http", `Server: Microsoft-IIS/([\d.]+)`, "Microsoft IIS", "$1", 10},
		{"http", `Server: (?:Werkzeug|gunicorn)/([\d.]+)`, "Python WSGI", "$1", 9},
		{"http", `Server: lighttpd/([\d.]+)`, "lighttpd", "$1", 10},
		{"http", `Server: Caddy`, "Caddy", "", 9},
		{"http", `Server: Jetty\(([\d.]+)`, "Jetty", "$1", 10},
		{"http", `Server: (?:CherryPy|BaseHTTP|SimpleHTTP)[^\r\n]*`, "Python HTTP", "", 8},
		{"http", `Server: AirTunes/([\d.]+)`, "AirTunes (AirPlay)", "$1", 10},
		{"http", `^HTTP/1\.[01] \d{3}`, "http", "", 5},
		// Databases
		{"mysql", `mysql_native_password`, "MySQL", "", 8},
		{"mysql", `([\d]+\.[\d]+\.[\d]+(?:-MariaDB)?[\w.\-]*)`, "MySQL/MariaDB", "$1", 7},
		{"redis", `^\+PONG`, "Redis", "", 9},
		{"redis", `^-NOAUTH|^-ERR`, "Redis", "", 8},
		{"redis", `redis_version:([\d.]+)`, "Redis", "$1", 10},
		{"mongodb", `MongoDB`, "MongoDB", "", 8},
		{"postgresql", `^E.*?FATAL`, "PostgreSQL", "", 7},
		// RTSP / streaming
		{"rtsp", `^RTSP/1\.0`, "rtsp", "", 7},
		// TLS-wrapped hint
		{"tls", `^\x15\x03|^\x16\x03`, "TLS/SSL", "", 6},
		// VNC / RDP / generic
		{"vnc", `^RFB ([\d.]+)`, "VNC (RFB)", "$1", 10},
		{"telnet", `^\xff[\xfb-\xfe]`, "telnet", "", 7},
	}

	out := make([]signature, 0, len(raw))
	for _, r := range raw {
		re, err := regexp.Compile("(?is)" + r.pattern)
		if err != nil {
			continue // skip bad pattern rather than crash
		}
		out = append(out, signature{
			service: r.service, re: re, product: r.product,
			version: r.version, confidence: r.confidence,
		})
	}
	// Highest confidence first so the first match wins.
	sort.SliceStable(out, func(i, j int) bool { return out[i].confidence > out[j].confidence })
	return out
}

// Fingerprint deep-identifies the service on host:port by sending probes and
// matching responses. Wrapped in retry + panic safety by the caller (SafeRun).
func Fingerprint(ctx context.Context, host string, port int, timeout time.Duration) Result {
	r := newResult("fingerprint", host)
	r.Port = ptr(port)
	r.Proto = "tcp"

	var bestSig *signature
	var bestResp string
	var rawFingerprint string

	for _, p := range probes {
		if ctx.Err() != nil {
			break
		}
		// Skip probes that declare specific ports if this isn't one of them —
		// but always run the port-agnostic ones (ports == nil).
		if p.ports != nil && !p.ports[port] {
			continue
		}

		resp, err := sendProbe(ctx, host, port, p.send, timeout)
		if err != nil {
			if IsRefused(err) {
				r.Status = "closed"
				return r
			}
			continue // try the next probe
		}
		if len(resp) == 0 {
			continue
		}
		rawFingerprint = resp

		if sig := matchSignature(resp); sig != nil {
			if bestSig == nil || sig.confidence > bestSig.confidence {
				bestSig = sig
				bestResp = resp
			}
			if sig.confidence >= 9 {
				break // strong match — stop probing
			}
		}
	}

	r.Status = "open"
	if bestSig != nil {
		product := expandBackrefs(bestSig.product, bestSig.re, bestResp)
		version := expandBackrefs(bestSig.version, bestSig.re, bestResp)
		r.Data["service"] = bestSig.service
		r.Data["product"] = product
		r.Data["version"] = version
		r.Data["confidence"] = bestSig.confidence
		r.Evidence = strings.TrimSpace(fmt.Sprintf("%s %s %s", bestSig.service, product, version))
	} else {
		// No signature matched — fall back to port-based guess and record the
		// raw bytes so a human can add a signature later (nmap does the same).
		r.Data["service"] = guessService(port, firstLine(rawFingerprint))
		r.Data["confidence"] = 2
		if rawFingerprint != "" {
			r.Data["raw_fingerprint"] = sanitize(firstLine(rawFingerprint))
		}
		r.Evidence = sanitize(firstLine(rawFingerprint))
	}
	return r
}

// sendProbe opens a connection, optionally writes the probe payload, and reads
// the response (bounded). Retries transient failures via the shared dialer.
func sendProbe(ctx context.Context, host string, port int, payload []byte, timeout time.Duration) (string, error) {
	addr := net.JoinHostPort(host, fmt.Sprintf("%d", port))
	conn, err := DialContext(ctx, "tcp", addr, timeout)
	if err != nil {
		return "", err
	}
	defer conn.Close()
	conn.SetDeadline(time.Now().Add(timeout))

	if len(payload) > 0 {
		if _, err := conn.Write(payload); err != nil {
			return "", err
		}
	}

	buf := make([]byte, 4096)
	n, _ := conn.Read(buf) // read error is fine — we may still have bytes
	return string(buf[:n]), nil
}

func matchSignature(resp string) *signature {
	for i := range signatures {
		if signatures[i].re.MatchString(resp) {
			return &signatures[i]
		}
	}
	return nil
}

// expandBackrefs replaces $1/$2 in a template with the corresponding regex
// capture groups from the response.
func expandBackrefs(template string, re *regexp.Regexp, resp string) string {
	if template == "" || !strings.Contains(template, "$") {
		return template
	}
	m := re.FindStringSubmatch(resp)
	out := template
	for i := len(m) - 1; i >= 1; i-- {
		out = strings.ReplaceAll(out, fmt.Sprintf("$%d", i), strings.TrimSpace(m[i]))
	}
	return strings.TrimSpace(out)
}

func firstLine(s string) string {
	if i := strings.IndexAny(s, "\r\n"); i >= 0 {
		return s[:i]
	}
	if len(s) > 160 {
		return s[:160]
	}
	return s
}

// sanitize strips non-printable bytes so a binary greeting doesn't corrupt logs.
func sanitize(s string) string {
	var b strings.Builder
	for _, r := range s {
		if r >= 32 && r < 127 {
			b.WriteRune(r)
		} else {
			b.WriteByte('.')
		}
	}
	out := b.String()
	if len(out) > 120 {
		out = out[:120]
	}
	return out
}
