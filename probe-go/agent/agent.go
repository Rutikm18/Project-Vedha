// agent/agent.go — main agent loop: register → WS push → HTTP poll fallback.
//
// On every wakeup (either push or poll tick) the agent:
//   1. Picks up a pending job
//   2. Runs the pipeline (Gate 0–6)
//   3. Submits the result; spools to disk on failure
package agent

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"time"

	"github.com/gorilla/websocket"
	"probe-go/config"
	"probe-go/pipeline"
)

const Version = "1.0.0"

var Capabilities = []string{
	"assessment", "db_fingerprint", "discovery", "host_discovery",
	"mcp_discovery", "passive_discovery", "port_scan", "service_fingerprint",
	"smb_enum", "tls_scan", "udp_scan", "vuln_scan", "web_scan",
}

type Agent struct {
	cfg       *config.Config
	transport *Transport
	spool     *Spool
	probeID   string
}

func New(cfg *config.Config) *Agent {
	return &Agent{
		cfg:       cfg,
		transport: NewTransport(cfg.PlatformURL, cfg.VerifyTLS),
		spool:     NewSpool(cfg.SpoolDir),
		probeID:   cfg.ProbeName,
	}
}

// Run starts the agent — registers, flushes spool, enters push/poll loop.
// Blocks until ctx is cancelled.
func (a *Agent) Run(ctx context.Context) error {
	if a.cfg.PlatformURL == "" {
		return fmt.Errorf("PLATFORM_URL is not set — edit probe.env and set it")
	}

	say("Vedha Probe (Go) v%s", Version)
	say("Platform : %s", a.cfg.PlatformURL)
	say("Probe    : %s", a.cfg.ProbeName)

	// ── Step 1: authenticate and register ────────────────────────────────────
	if err := a.obtainIdentity(ctx); err != nil {
		return err
	}
	say("Registered as '%s' (id=%s)", a.cfg.ProbeName, a.transport.AgentID)

	// ── Step 2: flush any spooled results from previous run ──────────────────
	if n := a.spool.Flush(func(jid string, p map[string]interface{}) error {
		return a.transport.SubmitResult(jid, p)
	}); n > 0 {
		say("Flushed %d spooled result(s)", n)
	}

	// ── Step 3: try WebSocket push mode; fall back to HTTP poll ──────────────
	if a.cfg.WSEnabled {
		say("Connecting via WebSocket (push mode)…")
		err := a.runWSLoop(ctx)
		if err == nil {
			return nil // clean shutdown
		}
		say("WebSocket unavailable (%v) — falling back to HTTP polling", err)
	}

	return a.runPollLoop(ctx)
}

// ── WebSocket push loop ───────────────────────────────────────────────────────

func (a *Agent) runWSLoop(ctx context.Context) error {
	backoff := 1.0
	for {
		err := a.wsSession(ctx)
		if err == errWSFallback {
			return err // caller should switch to poll
		}
		if ctx.Err() != nil {
			return nil // clean shutdown
		}
		jitter := time.Duration(backoff*1000+rand.Float64()*1000) * time.Millisecond
		say("WebSocket closed — reconnecting in %.0fs…", backoff)
		select {
		case <-ctx.Done():
			return nil
		case <-time.After(jitter):
		}
		backoff = math.Min(backoff*2, 60)
	}
}

var errWSFallback = fmt.Errorf("ws-fallback")

func (a *Agent) wsSession(ctx context.Context) error {
	conn, err := a.transport.ConnectWS()
	if err != nil {
		return errWSFallback // WS not available
	}
	defer conn.Close()

	// Auth handshake
	hello, _ := json.Marshal(map[string]string{
		"type":     "hello",
		"agent_id": a.transport.AgentID,
		"token":    a.transport.AgentToken,
	})
	conn.WriteMessage(websocket.TextMessage, hello)

	conn.SetReadDeadline(time.Now().Add(10 * time.Second))
	_, raw, err := conn.ReadMessage()
	if err != nil {
		return errWSFallback
	}
	var msg map[string]interface{}
	json.Unmarshal(raw, &msg)
	if msg["type"] != "hello_ok" {
		return errWSFallback
	}
	conn.SetReadDeadline(time.Time{})
	say("WebSocket push mode active")

	// Heartbeat sender
	hbDone := make(chan struct{})
	go func() {
		defer close(hbDone)
		for {
			select {
			case <-time.After(a.cfg.HeartbeatInterval):
				hb, _ := json.Marshal(map[string]string{"type": "heartbeat", "status": "online"})
				if conn.WriteMessage(websocket.TextMessage, hb) != nil {
					return
				}
			case <-ctx.Done():
				return
			}
		}
	}()
	defer func() { <-hbDone }()

	for {
		_, raw, err := conn.ReadMessage()
		if err != nil {
			return err
		}
		var m map[string]interface{}
		json.Unmarshal(raw, &m)

		switch m["type"] {
		case "job_push":
			job := m["job"]
			jraw, _ := json.Marshal(job)
			var jmap map[string]interface{}
			json.Unmarshal(jraw, &jmap)

			jobID, _ := jmap["job_id"].(string)
			ack, _ := json.Marshal(map[string]interface{}{"type": "job_ack", "job_id": jobID, "accepted": true})
			conn.WriteMessage(websocket.TextMessage, ack)

			busy, _ := json.Marshal(map[string]interface{}{"type": "heartbeat", "status": "busy", "current_job_id": jobID})
			conn.WriteMessage(websocket.TextMessage, busy)

			result := a.runJob(ctx, jmap)

			res, _ := json.Marshal(map[string]interface{}{
				"type":    "result",
				"job_id":  jobID,
				"success": result["ok"],
				"result":  result,
			})
			conn.WriteMessage(websocket.TextMessage, res)

			online, _ := json.Marshal(map[string]string{"type": "heartbeat", "status": "online"})
			conn.WriteMessage(websocket.TextMessage, online)

		case "displaced", "error":
			say("WS: %v", m["message"])
			return fmt.Errorf("ws displaced")

		case "result_ack":
			// manager acknowledged our result
		}

		if ctx.Err() != nil {
			return nil
		}
	}
}

// ── HTTP poll loop ────────────────────────────────────────────────────────────

func (a *Agent) runPollLoop(ctx context.Context) error {
	say("HTTP polling every %v…", a.cfg.PollInterval)
	lastHB := time.Time{}

	for {
		select {
		case <-ctx.Done():
			return nil
		default:
		}

		if time.Since(lastHB) >= a.cfg.HeartbeatInterval {
			a.transport.Heartbeat("online", "")
			lastHB = time.Now()
		}

		jobs, err := a.transport.PollJobs(a.cfg.JobLimit)
		if err != nil {
			say("Manager unreachable: %v — retrying…", err)
		} else {
			for _, job := range jobs {
				jobID, _ := job["job_id"].(string)
				a.transport.Heartbeat("busy", jobID)
				result := a.runJob(ctx, job)
				a.submitWithSpool(jobID, result)
				a.transport.Heartbeat("online", "")
			}
		}

		// Jitter: [interval, 1.5×interval)
		wait := a.cfg.PollInterval + time.Duration(rand.Float64()*float64(a.cfg.PollInterval/2))
		select {
		case <-ctx.Done():
			return nil
		case <-time.After(wait):
		}
	}
}

// ── job execution ─────────────────────────────────────────────────────────────

func (a *Agent) runJob(ctx context.Context, raw map[string]interface{}) map[string]interface{} {
	job := mapToJob(raw)
	log.Printf("[agent] running job %s type=%s profile=%s", job.JobID, job.ScanType, job.Profile)

	result := pipeline.Run(ctx, job, a.probeID)
	say("  ✓ job %s done — %d hosts, %d ports, %d facts",
		job.JobID, result.HostCount, result.OpenPorts, result.FactCount)

	b, _ := json.Marshal(result)
	var m map[string]interface{}
	json.Unmarshal(b, &m)
	return m
}

func (a *Agent) submitWithSpool(jobID string, payload map[string]interface{}) {
	err := a.transport.SubmitResult(jobID, payload)
	if err != nil {
		say("  Submit failed (%v) — spooling result for retry", err)
		a.spool.Save(jobID, payload)
	}
}

// ── identity / registration ───────────────────────────────────────────────────

func (a *Agent) obtainIdentity(ctx context.Context) error {
	// Use pre-configured token if present
	if a.cfg.AgentID != "" && a.cfg.AgentToken != "" {
		a.transport.AgentID = a.cfg.AgentID
		a.transport.AgentToken = a.cfg.AgentToken
		return nil
	}

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}

		if a.cfg.OperatorEmail == "" || a.cfg.OperatorPassword == "" {
			return fmt.Errorf("OPERATOR_EMAIL and OPERATOR_PASSWORD must be set in probe.env")
		}

		token, err := a.transport.Login(a.cfg.OperatorEmail, a.cfg.OperatorPassword)
		if err != nil {
			say("Login failed (%v) — retrying in 10s…", err)
			select {
			case <-ctx.Done():
				return ctx.Err()
			case <-time.After(10 * time.Second):
			}
			continue
		}

		err = a.transport.Register(token, a.cfg.ProbeName, a.cfg.ProbeLocation,
			Capabilities, a.cfg.NetworkSegments)
		if err != nil {
			say("Registration failed (%v) — retrying in 10s…", err)
			select {
			case <-ctx.Done():
				return ctx.Err()
			case <-time.After(10 * time.Second):
			}
			continue
		}
		return nil
	}
}

// ── helpers ───────────────────────────────────────────────────────────────────

func mapToJob(m map[string]interface{}) pipeline.Job {
	j := pipeline.Job{
		JobID:    str(m, "job_id"),
		ScanType: firstStr(str(m, "job_type"), str(m, "scan_type"), "assessment"),
	}
	if p, ok := m["params"].(map[string]interface{}); ok {
		j.Profile = firstStr(str(p, "profile"), "it")
		j.EngagementID = str(p, "engagement_id")
		j.UseCaseID = str(p, "use_case_id")
		j.Rate, _ = p["rate"].(float64)
		j.Concurrency = int(floatOr(p["concurrency"], 100))
		j.Timeout = floatOr(p["timeout"], 3)
		j.DiscTimeout = floatOr(p["disc_timeout"], 1.5)

		if sc, ok := p["scope_cidrs"].([]interface{}); ok {
			for _, v := range sc {
				if s, ok := v.(string); ok {
					j.ScopeCIDRs = append(j.ScopeCIDRs, s)
				}
			}
		}
		if ex, ok := p["excluded_cidrs"].([]interface{}); ok {
			for _, v := range ex {
				if s, ok := v.(string); ok {
					j.ExcludeCIDRs = append(j.ExcludeCIDRs, s)
				}
			}
		}
		// targets can be in params or top-level
		for _, key := range []string{"targets", "target", "scope_cidrs"} {
			switch v := p[key].(type) {
			case string:
				j.Targets = append(j.Targets, v)
			case []interface{}:
				for _, vv := range v {
					if s, ok := vv.(string); ok {
						j.Targets = append(j.Targets, s)
					}
				}
			}
		}
	}
	if len(j.Targets) == 0 {
		j.Targets = j.ScopeCIDRs
	}
	return j
}

func str(m map[string]interface{}, k string) string {
	v, _ := m[k].(string)
	return v
}

func firstStr(vals ...string) string {
	for _, v := range vals {
		if v != "" {
			return v
		}
	}
	return ""
}

func floatOr(v interface{}, def float64) float64 {
	if f, ok := v.(float64); ok && f > 0 {
		return f
	}
	return def
}

func say(format string, args ...interface{}) {
	fmt.Printf(format+"\n", args...)
}

// Hostname returns the machine's hostname for use as the default probe name.
func Hostname() string {
	h, _ := os.Hostname()
	return h
}
