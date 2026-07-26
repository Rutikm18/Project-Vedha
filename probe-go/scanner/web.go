// scanner/web.go — Gate 5 branch: HTTP(S) fingerprint.
// Fetches / and collects status, title, server, security headers, and redirect target.
package scanner

import (
	"context"
	"crypto/tls"
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"
	"time"
)

var WebPorts = map[int]bool{
	80: true, 443: true, 8080: true, 8443: true, 8000: true,
	8888: true, 9000: true, 9200: true, 8081: true, 5000: true, 3000: true,
}

var securityHeaders = []string{
	"content-security-policy",
	"strict-transport-security",
	"x-frame-options",
	"x-content-type-options",
	"referrer-policy",
	"permissions-policy",
}

var titleRe = regexp.MustCompile(`(?i)<title[^>]*>([^<]{1,200})`)

// ProbeHTTP fingerprints host:port over HTTP or HTTPS.
func ProbeHTTP(ctx context.Context, host string, port int, useTLS bool, timeout time.Duration) Result {
	r := newResult("web_scan", host)
	r.Port = ptr(port)
	r.Proto = "tcp"

	scheme := "http"
	if useTLS {
		scheme = "https"
	}
	url := fmt.Sprintf("%s://%s:%d/", scheme, host, port)

	client := &http.Client{
		Timeout: timeout,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			// Redirect targets are not part of the authorized request. Record the
			// Location header from the original response without following it.
			return http.ErrUseLastResponse
		},
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}

	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		r.Status = "error"
		r.Error = err.Error()
		return r
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (scanner)")

	resp, err := client.Do(req)
	if err != nil {
		// Try HTTPS if HTTP failed (port might be TLS only)
		if !useTLS {
			return ProbeHTTP(ctx, host, port, true, timeout)
		}
		r.Status = "error"
		r.Error = err.Error()
		return r
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(io.LimitReader(resp.Body, 65536))

	r.Status = "open"
	r.Data["url"] = url
	r.Data["status"] = resp.StatusCode
	r.Data["final_url"] = resp.Request.URL.String()
	r.Data["server"] = resp.Header.Get("Server")
	r.Data["x_powered_by"] = resp.Header.Get("X-Powered-By")
	r.Data["content_type"] = resp.Header.Get("Content-Type")

	// Extract <title>
	if m := titleRe.FindSubmatch(body); m != nil {
		r.Data["title"] = strings.TrimSpace(string(m[1]))
	}

	// Redirect
	if loc := resp.Header.Get("Location"); loc != "" {
		r.Data["redirect_location"] = loc
	}

	// Security headers
	var present, missing []string
	for _, h := range securityHeaders {
		if resp.Header.Get(h) != "" {
			present = append(present, h)
		} else {
			missing = append(missing, h)
		}
	}
	r.Data["security_headers_present"] = present
	r.Data["security_headers_missing"] = missing

	// Tech hints from headers/body
	r.Data["tech_hints"] = detectTech(resp, string(body))

	// All headers as flat map
	hdrs := make(map[string]string)
	for k, v := range resp.Header {
		if len(v) > 0 {
			hdrs[strings.ToLower(k)] = v[0]
		}
	}
	r.Data["all_headers"] = hdrs

	title, _ := r.Data["title"].(string)
	server, _ := r.Data["server"].(string)
	r.Evidence = fmt.Sprintf("HTTP %d server=%s title=%s", resp.StatusCode, server, title)
	return r
}

func detectTech(resp *http.Response, body string) []string {
	var hints []string
	server := strings.ToLower(resp.Header.Get("Server"))
	xpb := strings.ToLower(resp.Header.Get("X-Powered-By"))
	bl := strings.ToLower(body)

	checks := map[string]string{
		"nginx":     server,
		"apache":    server,
		"iis":       server,
		"caddy":     server,
		"gunicorn":  server,
		"php":       xpb,
		"asp.net":   xpb,
		"django":    bl,
		"react":     bl,
		"angular":   bl,
		"wordpress": bl,
		"joomla":    bl,
		"drupal":    bl,
		"grafana":   bl,
		"jenkins":   bl,
	}
	seen := map[string]bool{}
	for tech, src := range checks {
		if !seen[tech] && strings.Contains(src, tech) {
			hints = append(hints, tech)
			seen[tech] = true
		}
	}
	return hints
}
