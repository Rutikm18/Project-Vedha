// pipeline/pipeline.go — the exact Gate 0→6 scanning flow from gates.py.
//
// Gate 0 : passive profile check  (ot → skip all active gates)
// Gate 1 : scope expansion        (CIDR → list of IPs)
// Gate 2 : host discovery         (TCP-probe liveness check)
// Gate 3 : port scan              (TCP connect sweep, profile port list)
// Gate 4 : service banner         (banner grab on all open TCP ports)
// Gate 5 : deep probes (parallel) (TLS / HTTP / DB / UDP)
// Gate 6 : nmap enrichment        (overlay service+version if nmap available)
// Assemble and return result bundle.
package pipeline

import (
	"context"
	"fmt"
	"log"
	"sort"
	"sync"
	"time"

	"probe-go/scanner"
)

// Job describes one scan request from the manager.
type Job struct {
	JobID         string
	ScanType      string // assessment | tls_scan | web_scan | db_fingerprint | udp_scan | ...
	Profile       string // it | ot | iot
	Targets       []string
	ScopeCIDRs    []string
	ExcludeCIDRs  []string
	Rate          float64
	Concurrency   int
	Timeout       float64 // seconds
	DiscTimeout   float64 // seconds — host-discovery timeout
	EngagementID  string
	UseCaseID     string
}

// Fact is a single scanner observation — maps 1:1 to Python's ScanResult.
type Fact map[string]interface{}

// Result is the full bundle returned to the manager after a run.
type Result struct {
	SchemaVersion string                 `json:"result_schema_version"`
	ProbeID       string                 `json:"probe_id"`
	EngagementID  string                 `json:"engagement_uuid"`
	UseCaseID     string                 `json:"use_case_id"`
	ScanType      string                 `json:"scan_type"`
	Profile       string                 `json:"profile"`
	StartedAt     string                 `json:"started_at"`
	FinishedAt    string                 `json:"finished_at"`
	OK            bool                   `json:"ok"`
	Engine        string                 `json:"engine"`
	Facts         []Fact                 `json:"facts"`
	Findings      []scanner.Finding      `json:"findings"`
	Hosts         []map[string]interface{} `json:"hosts"`
	RunStats      map[string]interface{} `json:"run_stats"`
	Errors        []string               `json:"errors"`
	// Flat legacy fields for manager backwards compat
	HostCount    int `json:"host_count"`
	OpenPorts    int `json:"open_ports"`
	FactCount    int `json:"fact_count"`
	FindingCount int `json:"finding_count"`
}

// Run executes the full pipeline for a job and returns the assembled result.
func Run(ctx context.Context, job Job, probeID string) Result {
	start := time.Now()
	var errs []string
	var facts []Fact

	timeout := time.Duration(clamp(job.Timeout, 0.5, 30, 3)) * time.Second
	discTimeout := time.Duration(clamp(job.DiscTimeout, 0.5, 15, 1.5)) * time.Second
	concurrency := clampInt(job.Concurrency, 1, 500, 100)

	// Circuit breaker: after 5 consecutive scanner failures against one host we
	// stop probing it so a dead/filtered host doesn't drain the scan budget.
	breaker := scanner.NewCircuitBreaker(5)

	log.Printf("[pipeline] job=%s type=%s profile=%s targets=%v",
		job.JobID, job.ScanType, job.Profile, job.Targets)

	// ── Gate 0: passive profile (OT) ─────────────────────────────────────────
	if job.Profile == "ot" {
		// OT is passive-only — no active probes.
		log.Printf("[pipeline] gate0: OT profile → passive only (no active probes)")
		return assemble(job, probeID, start, facts, errs, concurrency)
	}

	// Build scope guard
	scopeEntries := job.ScopeCIDRs
	if len(scopeEntries) == 0 {
		scopeEntries = job.Targets
	}
	sg, err := scanner.NewScopeGuard(scopeEntries, job.ExcludeCIDRs)
	if err != nil {
		errs = append(errs, fmt.Sprintf("scope error: %v", err))
		return assembleError(job, probeID, start, err.Error())
	}

	// ── Gate 1: expand scope to IP list ──────────────────────────────────────
	var allHosts []string
	for _, t := range job.Targets {
		if sg.InScope(t) {
			allHosts = append(allHosts, t)
		}
	}
	// Also expand any CIDRs that were passed as scope
	for _, h := range sg.ExpandCIDRs() {
		allHosts = dedup(append(allHosts, h))
	}
	if len(allHosts) == 0 {
		errs = append(errs, "no in-scope targets after scope expansion")
		return assembleError(job, probeID, start, "no targets in scope")
	}
	log.Printf("[pipeline] gate1: %d hosts to probe", len(allHosts))

	// ── Gate 2: host discovery ────────────────────────────────────────────────
	log.Printf("[pipeline] gate2: host discovery…")
	hostResults := scanner.DiscoverHosts(ctx, allHosts, concurrency, discTimeout)
	var aliveHosts []string
	for _, hr := range hostResults {
		if hr.Alive {
			aliveHosts = append(aliveHosts, hr.Host)
			facts = append(facts, toFact(scanner.Result{
				Scanner: "host_discovery", Target: hr.Host, Status: "open",
				Data: map[string]interface{}{"host_state": "up", "rtt_ms": hr.RTT.Milliseconds()},
			}))
		}
	}
	log.Printf("[pipeline] gate2: %d/%d hosts alive", len(aliveHosts), len(allHosts))

	if len(aliveHosts) == 0 {
		return assemble(job, probeID, start, facts, errs, concurrency)
	}

	// ── Gate 3: port scan ─────────────────────────────────────────────────────
	log.Printf("[pipeline] gate3: port scan…")
	profilePorts := scanner.ProfilePorts[job.Profile]
	if len(profilePorts) == 0 {
		profilePorts = scanner.ProfilePorts["it"]
	}

	// host → open ports
	hostPorts := make(map[string][]int)
	for _, host := range aliveHosts {
		portResults := scanner.ScanPorts(ctx, host, profilePorts, concurrency, timeout)
		for _, pr := range portResults {
			hostPorts[host] = append(hostPorts[host], pr.Port)
			facts = append(facts, toFact(scanner.Result{
				Scanner: "port_scan", Target: host,
				Port: ptr(pr.Port), Proto: "tcp", Status: "open",
				Data: map[string]interface{}{"service": pr.Service},
			}))
		}
		log.Printf("[pipeline] gate3:   %s → %d open ports", host, len(hostPorts[host]))
	}

	// ── Gate 4: deep service fingerprint (probe/match engine) ─────────────────
	// Replaces naive banner-grab with nmap-style probe/response fingerprinting
	// to recover product + version. Panic-safe per port so one malformed
	// response can't take down the run.
	log.Printf("[pipeline] gate4: deep service fingerprint…")
	for _, host := range aliveHosts {
		if !breaker.Allow(host) {
			log.Printf("[pipeline] gate4: circuit open for %s — skipping", host)
			continue
		}
		for _, port := range hostPorts[host] {
			host, port := host, port
			r := scanner.SafeRun("fingerprint", host, func() scanner.Result {
				return scanner.Fingerprint(ctx, host, port, timeout)
			})
			if r.Status == "error" {
				breaker.RecordFailure(host)
			} else {
				breaker.RecordSuccess(host)
			}
			facts = append(facts, toFact(r))
		}
	}

	// ── Gate 5: deep probes (parallel branches) ───────────────────────────────
	log.Printf("[pipeline] gate5: deep probes (TLS / HTTP / DB / UDP)…")

	serviceFilter := serviceFilterFor(job.ScanType)

	var mu sync.Mutex
	var wg sync.WaitGroup
	addFacts := func(rs []scanner.Result) {
		mu.Lock()
		for _, r := range rs {
			facts = append(facts, toFact(r))
		}
		mu.Unlock()
	}

	for _, host := range aliveHosts {
		ports := hostPorts[host]
		portSet := toSet(ports)

		// TLS branch
		if serviceFilter == nil || serviceFilter["tls"] {
			tlsPorts := intersect(portSet, scanner.TLSPorts)
			// Also try any port that served HTTPS in the banner
			for _, port := range ports {
				if scanner.TLSPorts[port] || looksLikeTLS(port, portSet) {
					tlsPorts[port] = true
				}
			}
			for port := range tlsPorts {
				port := port
				host := host
				wg.Add(1)
				go func() {
					defer wg.Done()
					r := scanner.SafeRun("tls_scan", host, func() scanner.Result {
						return scanner.ProbeTLS(ctx, host, port, timeout)
					})
					addFacts([]scanner.Result{r})
				}()
			}
		}

		// HTTP branch
		if serviceFilter == nil || serviceFilter["web"] {
			webPorts := intersect(portSet, scanner.WebPorts)
			for port := range webPorts {
				port := port
				host := host
				wg.Add(1)
				go func() {
					defer wg.Done()
					// Try plain HTTP first; ProbeHTTP auto-retries as HTTPS
					r := scanner.SafeRun("web_scan", host, func() scanner.Result {
						return scanner.ProbeHTTP(ctx, host, port, false, timeout)
					})
					addFacts([]scanner.Result{r})
				}()
			}
		}

		// DB branch
		if serviceFilter == nil || serviceFilter["db"] {
			dbPorts := intersect(portSet, scanner.DBPorts)
			for port := range dbPorts {
				port := port
				host := host
				wg.Add(1)
				go func() {
					defer wg.Done()
					r := scanner.SafeRun("db_scan", host, func() scanner.Result {
						return scanner.ProbeDB(ctx, host, port, timeout)
					})
					addFacts([]scanner.Result{r})
				}()
			}
		}

		// UDP (always runs — no port gate because UDP is separate from TCP)
		if serviceFilter == nil || serviceFilter["udp"] {
			host := host
			wg.Add(1)
			go func() {
				defer wg.Done()
				udpResults := scanner.SafeRunMulti("udp_scan", host, func() []scanner.Result {
					return scanner.ProbeUDP(ctx, host, timeout)
				})
				addFacts(udpResults)
			}()
		}
	}
	wg.Wait()
	log.Printf("[pipeline] gate5: deep probes done — %d facts so far", len(facts))

	// Record any hosts the breaker tripped for run-stats visibility.
	if tripped := breaker.Tripped(); len(tripped) > 0 {
		errs = append(errs, fmt.Sprintf("circuit-broke on %d host(s): %v", len(tripped), tripped))
	}

	// ── Gate 6: nmap enrichment ───────────────────────────────────────────────
	if scanner.NmapAvailable() && (serviceFilter == nil || serviceFilter["nmap"]) {
		log.Printf("[pipeline] gate6: nmap service/version enrichment…")
		for _, host := range aliveHosts {
			if len(hostPorts[host]) == 0 {
				continue
			}
			nmapTimeout := timeout * 10
			if nmapTimeout < 60*time.Second {
				nmapTimeout = 60 * time.Second
			}
			nmapResults, err := scanner.RunNmapVersion(ctx, host, hostPorts[host], nmapTimeout)
			if err != nil {
				log.Printf("[pipeline] gate6: nmap error on %s: %v", host, err)
				continue
			}
			for _, nr := range nmapResults {
				p := nr.Port
				facts = append(facts, Fact{
					"scanner": "nmap_version", "target": nr.Host,
					"port": p, "proto": nr.Proto, "status": nr.State,
					"data": map[string]interface{}{
						"service": nr.Service, "product": nr.Product, "version": nr.Version,
					},
				})
			}
		}
	}

	// ── Gate 7: risk correlation (facts → ranked findings) ───────────────────
	log.Printf("[pipeline] gate7: risk correlation…")
	findings := scanner.SafeCorrelate(factsAsMaps(facts))
	log.Printf("[pipeline] gate7: %d finding(s)", len(findings))

	result := assemble(job, probeID, start, facts, errs, concurrency)
	result.Findings = findings
	result.FindingCount = len(findings)
	return result
}

// factsAsMaps converts []Fact to []map for the correlation layer.
func factsAsMaps(facts []Fact) []map[string]interface{} {
	out := make([]map[string]interface{}, len(facts))
	for i, f := range facts {
		out[i] = map[string]interface{}(f)
	}
	return out
}

// ── helpers ──────────────────────────────────────────────────────────────────

func serviceFilterFor(scanType string) map[string]bool {
	filters := map[string]map[string]bool{
		"tls_scan":       {"tls": true},
		"web_scan":       {"web": true},
		"db_fingerprint": {"db": true},
		"smb_enum":       {"smb": true},
		"udp_scan":       {"udp": true},
		"mcp_discovery":  {"mcp_ai": true},
	}
	if f, ok := filters[scanType]; ok {
		return f
	}
	return nil // nil = run all branches
}

func looksLikeTLS(port int, all map[int]bool) bool {
	// If we have 443 open alongside 80, try TLS on non-standard ports too
	return all[443] && port > 8000
}

func toSet(ports []int) map[int]bool {
	s := make(map[int]bool, len(ports))
	for _, p := range ports {
		s[p] = true
	}
	return s
}

func intersect(a, b map[int]bool) map[int]bool {
	out := make(map[int]bool)
	for p := range a {
		if b[p] {
			out[p] = true
		}
	}
	return out
}

func toFact(r scanner.Result) Fact {
	f := Fact{
		"scanner":   r.Scanner,
		"target":    r.Target,
		"timestamp": r.Timestamp,
		"status":    r.Status,
	}
	if r.Port != nil {
		f["port"] = *r.Port
	}
	if r.Proto != "" {
		f["proto"] = r.Proto
	}
	if len(r.Data) > 0 {
		f["data"] = r.Data
	}
	if r.Evidence != "" {
		f["evidence"] = r.Evidence
	}
	if r.Error != "" {
		f["error"] = r.Error
	}
	return f
}

func assemble(job Job, probeID string, start time.Time, facts []Fact, errs []string, concurrency int) Result {
	now := time.Now()
	hosts := buildHostsMap(facts)
	openPorts := countOpenPorts(facts)

	return Result{
		SchemaVersion: "1.1",
		ProbeID:       probeID,
		EngagementID:  job.EngagementID,
		UseCaseID:     job.UseCaseID,
		ScanType:      job.ScanType,
		Profile:       job.Profile,
		StartedAt:     start.UTC().Format(time.RFC3339),
		FinishedAt:    now.UTC().Format(time.RFC3339),
		OK:            len(errs) == 0,
		Engine:        "vedha-probe-go",
		Facts:         facts,
		Hosts:         hosts,
		Errors:        errs,
		RunStats: map[string]interface{}{
			"host_count":   len(hosts),
			"open_ports":   openPorts,
			"fact_count":   len(facts),
			"duration_sec": now.Sub(start).Seconds(),
		},
		HostCount:    len(hosts),
		OpenPorts:    openPorts,
		FactCount:    len(facts),
		FindingCount: 0,
	}
}

func assembleError(job Job, probeID string, start time.Time, errMsg string) Result {
	r := assemble(job, probeID, start, nil, []string{errMsg}, 0)
	r.OK = false
	return r
}

func buildHostsMap(facts []Fact) []map[string]interface{} {
	// host → "proto/port" → merged port entry (deduped; richest service wins).
	type portKey struct {
		host, proto string
		port        int
	}
	merged := make(map[portKey]map[string]interface{})
	hostOrder := []string{}
	seenHost := map[string]bool{}

	for _, f := range facts {
		host, _ := f["target"].(string)
		if host == "" || f["status"] != "open" {
			continue
		}
		if !seenHost[host] {
			seenHost[host] = true
			hostOrder = append(hostOrder, host)
		}
		port, ok := f["port"].(int)
		if !ok {
			continue
		}
		proto, _ := f["proto"].(string)
		if proto == "" {
			proto = "tcp"
		}
		svc := ""
		if d, ok := f["data"].(map[string]interface{}); ok {
			if s, _ := d["service"].(string); s != "" {
				svc = s
			}
		}
		k := portKey{host, proto, port}
		if existing, ok := merged[k]; ok {
			// Prefer a more specific service label than a bare guess/empty.
			if cur, _ := existing["service"].(string); svc != "" && (cur == "" || cur == "unknown") {
				existing["service"] = svc
			}
		} else {
			merged[k] = map[string]interface{}{"port": port, "protocol": proto, "service": svc}
		}
	}

	// Group merged ports back under their host, preserving first-seen order.
	hostPorts := make(map[string][]map[string]interface{})
	for k, entry := range merged {
		hostPorts[k.host] = append(hostPorts[k.host], entry)
	}

	out := make([]map[string]interface{}, 0, len(hostOrder))
	for _, h := range hostOrder {
		ports := hostPorts[h]
		sort.Slice(ports, func(i, j int) bool {
			return ports[i]["port"].(int) < ports[j]["port"].(int)
		})
		out = append(out, map[string]interface{}{"ip": h, "ports": ports})
	}
	return out
}

// countOpenPorts counts DISTINCT open host:proto:port tuples (not raw facts,
// which double-count a port probed by several scanners).
func countOpenPorts(facts []Fact) int {
	seen := map[string]bool{}
	for _, f := range facts {
		if f["status"] != "open" || f["port"] == nil {
			continue
		}
		host, _ := f["target"].(string)
		proto, _ := f["proto"].(string)
		key := fmt.Sprintf("%s|%s|%v", host, proto, f["port"])
		seen[key] = true
	}
	return len(seen)
}

func dedup(s []string) []string {
	seen := make(map[string]bool, len(s))
	var out []string
	for _, v := range s {
		if !seen[v] {
			seen[v] = true
			out = append(out, v)
		}
	}
	return out
}

func clamp(v, lo, hi, def float64) float64 {
	if v == 0 {
		return def
	}
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func clampInt(v, lo, hi, def int) int {
	if v == 0 {
		return def
	}
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func ptr(i int) *int { return &i }
