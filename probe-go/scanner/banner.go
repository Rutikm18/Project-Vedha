// scanner/banner.go — Gate 3: service banner grab.
// Connects, sends an HTTP probe on web-like ports, reads raw bytes on others.
// Output feeds the router (gate 5 branch selection) and the final report.
package scanner

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"net"
	"strings"
	"time"
)

var httpLikePorts = map[int]bool{
	80: true, 443: true, 8080: true, 8443: true,
	8000: true, 8888: true, 9000: true, 9200: true,
	8081: true, 5000: true, 3000: true,
}

// GrabBanner connects to host:port, tries to elicit a banner, and returns
// the first meaningful bytes the server sends.
func GrabBanner(ctx context.Context, host string, port int, timeout time.Duration) Result {
	r := newResult("service_banner", host)
	r.Port = ptr(port)
	r.Proto = "tcp"

	addr := fmt.Sprintf("%s:%d", host, port)
	dialer := &net.Dialer{}
	dctx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()

	conn, err := dialer.DialContext(dctx, "tcp", addr)
	if err != nil {
		r.Status = "closed"
		r.Error = err.Error()
		return r
	}
	defer conn.Close()
	conn.SetDeadline(time.Now().Add(timeout))

	r.Status = "open"

	var raw []byte
	if httpLikePorts[port] {
		// Send a minimal HTTP/1.0 GET — many services echo something back.
		fmt.Fprintf(conn, "GET / HTTP/1.0\r\nHost: %s\r\n\r\n", host)
		raw, _ = io.ReadAll(io.LimitReader(conn, 2048))
	} else {
		// Just read — SSH, FTP, MySQL, etc. send a greeting immediately.
		raw, _ = io.ReadAll(io.LimitReader(conn, 512))
	}

	banner := strings.TrimRight(string(raw), "\r\n\x00")
	if len(banner) > 120 {
		banner = banner[:120]
	}

	firstLine := banner
	if idx := strings.IndexAny(banner, "\r\n"); idx >= 0 {
		firstLine = banner[:idx]
	}

	r.Data["banner"] = banner
	r.Data["first_line"] = firstLine
	r.Data["service"] = guessService(port, firstLine)
	r.Evidence = firstLine
	return r
}

func guessService(port int, firstLine string) string {
	fl := strings.ToLower(firstLine)
	switch {
	case strings.HasPrefix(fl, "ssh-"):
		return "ssh"
	case strings.HasPrefix(fl, "220 ") && strings.Contains(fl, "ftp"):
		return "ftp"
	case strings.HasPrefix(fl, "220 ") && strings.Contains(fl, "smtp"):
		return "smtp"
	case strings.HasPrefix(fl, "+ok"):
		return "pop3"
	case strings.HasPrefix(fl, "* ok"):
		return "imap"
	case strings.HasPrefix(fl, "http/"):
		return "http"
	case len(firstLine) > 4 && strings.Contains(fl, "mysql"):
		return "mysql"
	case strings.HasPrefix(fl, "err"):
		return "redis"
	case strings.HasPrefix(fl, "+pong"):
		return "redis"
	}
	known := map[int]string{
		21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "domain",
		80: "http", 110: "pop3", 135: "msrpc", 139: "netbios-ssn",
		143: "imap", 389: "ldap", 443: "https", 445: "microsoft-ds",
		465: "smtps", 587: "submission", 636: "ldaps", 993: "imaps",
		995: "pop3s", 1433: "ms-sql-s", 1521: "oracle", 3306: "mysql",
		3389: "ms-wbt-server", 5432: "postgresql", 5900: "vnc",
		5985: "wsman", 5986: "wsmans", 6379: "redis", 8080: "http-proxy",
		8443: "https-alt", 9200: "wap-wsp", 11211: "memcache",
		27017: "mongod",
	}
	if s, ok := known[port]; ok {
		return s
	}
	return "unknown"
}

// ParseHTTPResponse extracts status code and Server header from raw HTTP bytes.
func ParseHTTPResponse(raw string) (status int, server string) {
	sc := bufio.NewScanner(strings.NewReader(raw))
	first := true
	for sc.Scan() {
		line := sc.Text()
		if first {
			first = false
			// "HTTP/1.1 200 OK"
			parts := strings.SplitN(line, " ", 3)
			if len(parts) >= 2 {
				fmt.Sscanf(parts[1], "%d", &status)
			}
			continue
		}
		if line == "" {
			break
		}
		k, v, ok := strings.Cut(line, ":")
		if ok && strings.EqualFold(strings.TrimSpace(k), "server") {
			server = strings.TrimSpace(v)
		}
	}
	return
}
