// scanner/tls.go — Gate 5 branch: TLS handshake probe.
// Collects accepted TLS versions, cipher suite, cert subject/expiry/self-signed flag.
// Does NOT validate the certificate (InsecureSkipVerify) — we are a scanner, not a client.
package scanner

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"net"
	"strings"
	"time"
)

var TLSPorts = map[int]bool{
	443: true, 8443: true, 993: true, 995: true,
	465: true, 636: true, 989: true, 990: true, 5986: true,
}

// ProbeTLS performs TLS handshakes against host:port at multiple protocol
// versions and returns collected facts.
func ProbeTLS(ctx context.Context, host string, port int, timeout time.Duration) Result {
	r := newResult("tls_scan", host)
	r.Port = ptr(port)
	r.Proto = "tcp"

	addr := fmt.Sprintf("%s:%d", host, port)

	type attempt struct {
		version uint16
		name    string
	}
	attempts := []attempt{
		{tls.VersionTLS13, "TLSv1_3"},
		{tls.VersionTLS12, "TLSv1_2"},
		{tls.VersionTLS11, "TLSv1_1"},
		{tls.VersionTLS10, "TLSv1_0"},
	}

	var accepted []string
	var certInfo map[string]interface{}
	negotiatedCiphers := map[string]string{}

	for _, a := range attempts {
		select {
		case <-ctx.Done():
			r.Status = "error"
			r.Error = "context cancelled"
			return r
		default:
		}

		dialer := &net.Dialer{Timeout: timeout}
		cfg := &tls.Config{
			InsecureSkipVerify: true,
			MinVersion:         a.version,
			MaxVersion:         a.version,
			ServerName:         host,
		}
		conn, err := tls.DialWithDialer(dialer, "tcp", addr, cfg)
		if err != nil {
			continue
		}
		state := conn.ConnectionState()
		accepted = append(accepted, a.name)
		negotiatedCiphers[a.name] = tls.CipherSuiteName(state.CipherSuite)

		if certInfo == nil && len(state.PeerCertificates) > 0 {
			certInfo = parseCert(state.PeerCertificates[0])
		}
		conn.Close()
	}

	if len(accepted) == 0 {
		// Not TLS or connection refused
		r.Status = "closed"
		return r
	}

	// Enumerate weak cipher support explicitly (Go only offers a safe default
	// set; probing insecure suites tells us if the server would accept them).
	weak := enumerateWeakCiphers(ctx, addr, host, timeout)

	r.Status = "open"
	r.Data["accepted_versions"] = accepted
	r.Data["negotiated_ciphers"] = negotiatedCiphers
	r.Data["certificate"] = certInfo
	if len(weak) > 0 {
		r.Data["weak_ciphers"] = weak
	}
	r.Evidence = strings.Join(accepted, ",")
	return r
}

// weakCipherSuites are cipher suites Go still exposes as InsecureCipherSuites —
// if the server negotiates one, it supports cryptographically weak crypto.
var weakCipherSuites = func() []uint16 {
	var ids []uint16
	for _, cs := range tls.InsecureCipherSuites() {
		ids = append(ids, cs.ID)
	}
	return ids
}()

// enumerateWeakCiphers checks whether the server will negotiate any of Go's
// known-insecure cipher suites over TLS 1.0–1.2.
func enumerateWeakCiphers(ctx context.Context, addr, host string, timeout time.Duration) []string {
	var found []string
	seen := map[string]bool{}
	for _, id := range weakCipherSuites {
		if ctx.Err() != nil {
			break
		}
		dialer := &net.Dialer{Timeout: timeout}
		cfg := &tls.Config{
			InsecureSkipVerify: true,
			MinVersion:         tls.VersionTLS10,
			MaxVersion:         tls.VersionTLS12,
			CipherSuites:       []uint16{id},
			ServerName:         host,
		}
		conn, err := tls.DialWithDialer(dialer, "tcp", addr, cfg)
		if err != nil {
			continue
		}
		name := tls.CipherSuiteName(conn.ConnectionState().CipherSuite)
		if !seen[name] {
			found = append(found, name)
			seen[name] = true
		}
		conn.Close()
	}
	return found
}

func parseCert(c *x509.Certificate) map[string]interface{} {
	now := time.Now()
	subj := c.Subject.CommonName
	if subj == "" && len(c.Subject.Organization) > 0 {
		subj = c.Subject.Organization[0]
	}

	selfSigned := c.Issuer.CommonName == c.Subject.CommonName &&
		c.Issuer.String() == c.Subject.String()

	var sans []string
	sans = append(sans, c.DNSNames...)
	for _, ip := range c.IPAddresses {
		sans = append(sans, ip.String())
	}

	return map[string]interface{}{
		"subject":      subj,
		"issuer":       c.Issuer.CommonName,
		"sans":         sans,
		"not_before":   c.NotBefore.Format(time.RFC3339),
		"not_after":    c.NotAfter.Format(time.RFC3339),
		"expired":      now.After(c.NotAfter),
		"self_signed":  selfSigned,
		"serial":       c.SerialNumber.String(),
	}
}
