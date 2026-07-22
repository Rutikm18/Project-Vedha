// scanner/vulncheck.go — risk correlation layer.
//
// Following 2025 scanner best practice (risk-based prioritization: severity +
// exploited-in-wild + exposure), this turns raw facts into ranked findings.
// It is heuristic and version/config based — NOT an exploit engine. It flags:
//   * deprecated TLS versions and weak ciphers
//   * expired / self-signed certificates
//   * missing HTTP security headers
//   * exposed databases (reachable without auth prompt)
//   * default / guessable SNMP community strings
//   * end-of-life or known-CVE software versions (embedded mini knowledge base)
//   * plaintext protocols (telnet, ftp, http on sensitive ports)
package scanner

import (
	"fmt"
	"regexp"
	"strings"
)

// Severity levels mirror CVSS qualitative bands.
const (
	SevCritical = "critical"
	SevHigh     = "high"
	SevMedium   = "medium"
	SevLow      = "low"
	SevInfo     = "info"
)

// Finding is one ranked, human-reviewable security observation.
type Finding struct {
	Host      string `json:"host"`
	Port      int    `json:"port,omitempty"`
	Proto     string `json:"proto,omitempty"`
	Severity  string `json:"severity"`
	Tag       string `json:"tag"`
	Title     string `json:"title"`
	Detail    string `json:"detail"`
	Evidence  string `json:"evidence,omitempty"`
	KEV       bool   `json:"known_exploited,omitempty"` // exploited-in-wild flag
	Reference string `json:"reference,omitempty"`
}

// severityRank orders findings for reporting (critical first).
func severityRank(s string) int {
	switch s {
	case SevCritical:
		return 0
	case SevHigh:
		return 1
	case SevMedium:
		return 2
	case SevLow:
		return 3
	default:
		return 4
	}
}

// vulnRule matches a product+version and produces a finding.
type vulnRule struct {
	product   *regexp.Regexp
	versionLt string // flag if detected version is below this (simple semver-ish)
	severity  string
	tag       string
	title     string
	kev       bool
	reference string
}

// Embedded mini knowledge base of high-signal, widely-known issues.
// (A real deployment syncs this from NVD/KEV; this covers the common cases so
// the probe produces value offline.)
var vulnRules = buildVulnRules()

func buildVulnRules() []vulnRule {
	raw := []struct {
		product, versionLt, severity, tag, title string
		kev                                      bool
		ref                                      string
	}{
		{`OpenSSH`, "7.4", SevMedium, "SSH-OUTDATED", "Outdated OpenSSH (multiple CVEs before 7.4)", false, "https://www.openssh.com/security.html"},
		{`Apache httpd`, "2.4.50", SevHigh, "CVE-2021-41773", "Apache path traversal / RCE (2.4.49–2.4.50)", true, "https://nvd.nist.gov/vuln/detail/CVE-2021-41773"},
		{`nginx`, "1.20", SevMedium, "NGINX-OUTDATED", "Outdated nginx — upgrade to a supported branch", false, ""},
		{`vsftpd`, "3.0.0", SevHigh, "VSFTPD-OLD", "Old vsftpd (2.3.4 shipped with a known backdoor)", true, "https://nvd.nist.gov/vuln/detail/CVE-2011-2523"},
		{`Exim smtpd`, "4.92", SevCritical, "CVE-2019-10149", "Exim RCE (Return of the WIZard, <4.92)", true, "https://nvd.nist.gov/vuln/detail/CVE-2019-10149"},
		{`ProFTPD`, "1.3.6", SevHigh, "PROFTPD-OLD", "Old ProFTPD — mod_copy CVE-2019-12815", false, "https://nvd.nist.gov/vuln/detail/CVE-2019-12815"},
		{`Microsoft IIS`, "8.0", SevMedium, "IIS-EOL", "End-of-life IIS version", false, ""},
	}
	var out []vulnRule
	for _, r := range raw {
		re, err := regexp.Compile("(?i)" + regexp.QuoteMeta(r.product))
		if err != nil {
			continue
		}
		out = append(out, vulnRule{
			product: re, versionLt: r.versionLt, severity: r.severity,
			tag: r.tag, title: r.title, kev: r.kev, reference: r.ref,
		})
	}
	return out
}

// Weak TLS ciphers/versions we flag by name.
var deprecatedTLS = map[string]string{
	"TLSv1_0": SevMedium,
	"TLSv1_1": SevMedium,
	"SSLv3":   SevHigh,
	"SSLv2":   SevCritical,
}

// Default SNMP community strings that indicate misconfiguration.
var defaultCommunities = map[string]bool{
	"public": true, "private": true, "community": true,
	"admin": true, "manager": true, "cisco": true,
}

// plaintextRisky flags services that transmit credentials in the clear.
var plaintextRisky = map[string]string{
	"telnet": "Telnet transmits credentials in plaintext — use SSH",
	"ftp":    "FTP transmits credentials in plaintext — use SFTP/FTPS",
}

// SafeCorrelate is Correlate with panic recovery — a malformed fact can never
// crash the probe at the reporting stage.
func SafeCorrelate(facts []map[string]interface{}) (out []Finding) {
	defer func() {
		if r := recover(); r != nil {
			out = []Finding{{
				Severity: SevInfo, Tag: "CORRELATE-ERROR",
				Title:  "Risk correlation partially failed",
				Detail: fmt.Sprintf("panic recovered: %v", r),
			}}
		}
	}()
	return Correlate(facts)
}

// Correlate walks the collected facts and produces ranked findings.
func Correlate(facts []map[string]interface{}) []Finding {
	var findings []Finding

	for _, f := range facts {
		host, _ := f["target"].(string)
		if host == "" {
			continue
		}
		port := intFromFact(f["port"])
		proto, _ := f["proto"].(string)
		scanner, _ := f["scanner"].(string)
		data, _ := f["data"].(map[string]interface{})
		if data == nil {
			data = map[string]interface{}{}
		}

		switch scanner {
		case "fingerprint", "nmap_version", "service_banner":
			findings = append(findings, checkService(host, port, proto, data)...)
		case "tls_scan":
			findings = append(findings, checkTLS(host, port, proto, data)...)
		case "web_scan":
			findings = append(findings, checkWeb(host, port, proto, data)...)
		case "db_scan":
			findings = append(findings, checkDB(host, port, proto, data)...)
		case "udp_scan":
			findings = append(findings, checkUDP(host, port, data)...)
		}
	}

	return dedupAndRank(findings)
}

func checkService(host string, port int, proto string, data map[string]interface{}) []Finding {
	var out []Finding
	service, _ := data["service"].(string)
	product, _ := data["product"].(string)
	version, _ := data["version"].(string)

	// Plaintext protocol exposure
	if msg, ok := plaintextRisky[service]; ok {
		out = append(out, Finding{
			Host: host, Port: port, Proto: proto, Severity: SevMedium,
			Tag: "PLAINTEXT-PROTO", Title: "Plaintext protocol exposed",
			Detail: msg, Evidence: service,
		})
	}

	// Version-based known-vuln correlation
	banner := product + " " + version
	for _, rule := range vulnRules {
		if rule.product.MatchString(banner) || (product != "" && rule.product.MatchString(product)) {
			if version == "" || versionLessThan(version, rule.versionLt) {
				sev := rule.severity
				out = append(out, Finding{
					Host: host, Port: port, Proto: proto, Severity: sev,
					Tag: rule.tag, Title: rule.title,
					Detail:    fmt.Sprintf("detected %s %s", product, version),
					Evidence:  strings.TrimSpace(banner),
					KEV:       rule.kev,
					Reference: rule.reference,
				})
			}
		}
	}
	return out
}

func checkTLS(host string, port int, proto string, data map[string]interface{}) []Finding {
	var out []Finding

	for _, vs := range toStrings(data["accepted_versions"]) {
		if sev, bad := deprecatedTLS[vs]; bad {
			out = append(out, Finding{
				Host: host, Port: port, Proto: proto, Severity: sev,
				Tag: "WEAK-TLS", Title: "Deprecated TLS/SSL version accepted",
				Detail:   fmt.Sprintf("server negotiates %s", vs),
				Evidence: vs,
			})
		}
	}
	// Weak ciphers enumerated by the TLS scanner
	if names := toStrings(data["weak_ciphers"]); len(names) > 0 {
		out = append(out, Finding{
			Host: host, Port: port, Proto: proto, Severity: SevMedium,
			Tag: "WEAK-CIPHER", Title: "Weak TLS cipher suites offered",
			Detail:   fmt.Sprintf("%d weak cipher(s)", len(names)),
			Evidence: strings.Join(names, ", "),
		})
	}

	if cert, ok := data["certificate"].(map[string]interface{}); ok {
		if expired, _ := cert["expired"].(bool); expired {
			out = append(out, Finding{
				Host: host, Port: port, Proto: proto, Severity: SevHigh,
				Tag: "TLS-CERT-EXPIRED", Title: "TLS certificate expired",
				Detail: "the presented certificate is past its notAfter date",
			})
		}
		if ss, _ := cert["self_signed"].(bool); ss {
			out = append(out, Finding{
				Host: host, Port: port, Proto: proto, Severity: SevLow,
				Tag: "TLS-CERT-SELFSIGNED", Title: "Self-signed TLS certificate",
				Detail: "certificate is not chained to a trusted CA",
			})
		}
	}
	return out
}

func checkWeb(host string, port int, proto string, data map[string]interface{}) []Finding {
	var out []Finding

	if names := toStrings(data["security_headers_missing"]); len(names) >= 3 {
		out = append(out, Finding{
			Host: host, Port: port, Proto: proto, Severity: SevLow,
			Tag: "MISSING-HEADERS", Title: "Missing HTTP security headers",
			Detail:   fmt.Sprintf("%d headers absent", len(names)),
			Evidence: strings.Join(names, ", "),
		})
	}
	// Exposed admin/management interfaces by title
	if title, _ := data["title"].(string); title != "" {
		lt := strings.ToLower(title)
		for _, adminHint := range []string{"grafana", "jenkins", "kibana", "phpmyadmin", "adminer", "login", "dashboard"} {
			if strings.Contains(lt, adminHint) {
				out = append(out, Finding{
					Host: host, Port: port, Proto: proto, Severity: SevInfo,
					Tag: "EXPOSED-UI", Title: "Management/login interface exposed",
					Detail: fmt.Sprintf("page title suggests %q", adminHint), Evidence: title,
				})
				break
			}
		}
	}
	return out
}

func checkDB(host string, port int, proto string, data map[string]interface{}) []Finding {
	engine, _ := data["engine"].(string)
	version, _ := data["server_version"].(string)
	if engine == "" {
		return nil
	}
	return []Finding{{
		Host: host, Port: port, Proto: proto, Severity: SevHigh,
		Tag: "DB-EXPOSED", Title: "Database reachable from scanner",
		Detail:   fmt.Sprintf("%s responded to a protocol handshake", engine),
		Evidence: strings.TrimSpace(engine + " " + version),
	}}
}

func checkUDP(host string, port int, data map[string]interface{}) []Finding {
	var out []Finding
	if comm, _ := data["community"].(string); comm != "" {
		sev := SevMedium
		if defaultCommunities[strings.ToLower(comm)] {
			sev = SevHigh
		}
		out = append(out, Finding{
			Host: host, Port: port, Proto: "udp", Severity: sev,
			Tag: "SNMP-COMMUNITY", Title: "SNMP responds to a community string",
			Detail:   fmt.Sprintf("community %q accepted", comm),
			Evidence: comm,
		})
	}
	return out
}

// ── helpers ──────────────────────────────────────────────────────────────────

func dedupAndRank(findings []Finding) []Finding {
	seen := map[string]bool{}
	var out []Finding
	for _, f := range findings {
		key := fmt.Sprintf("%s|%d|%s|%s", f.Host, f.Port, f.Tag, f.Detail)
		if seen[key] {
			continue
		}
		seen[key] = true
		out = append(out, f)
	}
	// Stable sort: severity, then KEV-first within a band.
	for i := 0; i < len(out); i++ {
		for j := i + 1; j < len(out); j++ {
			ri, rj := severityRank(out[i].Severity), severityRank(out[j].Severity)
			if rj < ri || (rj == ri && out[j].KEV && !out[i].KEV) {
				out[i], out[j] = out[j], out[i]
			}
		}
	}
	return out
}

// toStrings normalises a slice field that may be []string (in-memory fact) or
// []interface{} (after a JSON round-trip through the manager) into []string.
func toStrings(v interface{}) []string {
	switch s := v.(type) {
	case []string:
		return s
	case []interface{}:
		out := make([]string, 0, len(s))
		for _, e := range s {
			if str, ok := e.(string); ok {
				out = append(out, str)
			}
		}
		return out
	}
	return nil
}

func intFromFact(v interface{}) int {
	switch n := v.(type) {
	case int:
		return n
	case float64:
		return int(n)
	}
	return 0
}

// versionLessThan does a best-effort numeric-dotted comparison (a<b).
// Non-numeric segments compare lexically; missing segments count as 0.
func versionLessThan(a, b string) bool {
	if b == "" {
		return false
	}
	as := splitVersion(a)
	bs := splitVersion(b)
	n := len(as)
	if len(bs) > n {
		n = len(bs)
	}
	for i := 0; i < n; i++ {
		var ai, bi int
		if i < len(as) {
			ai = as[i]
		}
		if i < len(bs) {
			bi = bs[i]
		}
		if ai != bi {
			return ai < bi
		}
	}
	return false
}

var verNumRe = regexp.MustCompile(`\d+`)

func splitVersion(v string) []int {
	parts := verNumRe.FindAllString(v, -1)
	out := make([]int, 0, len(parts))
	for _, p := range parts {
		n := 0
		fmt.Sscanf(p, "%d", &n)
		out = append(out, n)
	}
	return out
}
