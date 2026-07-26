// agent/agent.go — main agent loop: register → WS push → HTTP poll fallback.
//
// On every wakeup (either push or poll tick) the agent:
//  1. Picks up a pending job
//  2. Runs the pipeline (Gate 0–6)
//  3. Submits the result; spools to disk on failure
package agent

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	"probe-go/config"
	"probe-go/pipeline"
)

const Version = "1.0.0"

var Capabilities = []string{
	"assessment", "db_fingerprint", "discovery", "host_discovery",
	"port_scan", "service_fingerprint", "tls_scan", "udp_scan",
	"web_scan", "web_tls_scan",
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
	if err := a.transport.RefreshRegistration(Capabilities, a.cfg.NetworkSegments); err != nil {
		return fmt.Errorf("refresh probe capabilities: %w", err)
	}
	say("Registered as '%s' (id=%s)", a.cfg.ProbeName, a.transport.AgentID)

	// ── Step 2: flush any spooled results from previous run ──────────────────
	if n := a.flushSpool(); n > 0 {
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

const (
	wsProtocolVersion    = 2
	wsAtomicClaimFeature = "atomic_job_claim_v1"
)

type wsJSONWriter struct {
	conn    *websocket.Conn
	mu      sync.Mutex
	timeout time.Duration
}

type wsHelloMessage struct {
	Type            string   `json:"type"`
	ProtocolVersion int      `json:"protocol_version"`
	Features        []string `json:"features"`
}

type wsJobState struct {
	sync.RWMutex
	currentJobID string
	pendingJobID string
}

func (w *wsJSONWriter) Write(payload interface{}) error {
	data, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("marshal WebSocket message: %w", err)
	}

	w.mu.Lock()
	defer w.mu.Unlock()
	if err := w.conn.SetWriteDeadline(time.Now().Add(w.timeout)); err != nil {
		return err
	}
	return w.conn.WriteMessage(websocket.TextMessage, data)
}

func (a *Agent) wsSession(ctx context.Context) error {
	conn, err := a.transport.ConnectWS()
	if err != nil {
		return errWSFallback // WS not available
	}

	sessionCtx, cancel := context.WithCancel(ctx)
	var heartbeatDone <-chan struct{}
	defer func() {
		cancel()
		_ = conn.Close()
		if heartbeatDone != nil {
			select {
			case <-heartbeatDone:
			case <-time.After(2 * time.Second):
				log.Printf("[agent] WebSocket heartbeat did not stop before shutdown deadline")
			}
		}
	}()
	go func() {
		<-sessionCtx.Done()
		_ = conn.Close()
	}()

	writer := &wsJSONWriter{conn: conn, timeout: 10 * time.Second}

	// Auth handshake
	if err := writer.Write(map[string]interface{}{
		"type":             "hello",
		"agent_id":         a.transport.AgentID,
		"token":            a.transport.AgentToken,
		"protocol_version": wsProtocolVersion,
		"features":         []string{wsAtomicClaimFeature},
	}); err != nil {
		return errWSFallback
	}

	if err := conn.SetReadDeadline(time.Now().Add(10 * time.Second)); err != nil {
		return errWSFallback
	}
	_, raw, err := conn.ReadMessage()
	if err != nil {
		return errWSFallback
	}
	var hello wsHelloMessage
	if err := json.Unmarshal(raw, &hello); err != nil {
		return errWSFallback
	}
	if hello.Type != "hello_ok" ||
		hello.ProtocolVersion < wsProtocolVersion ||
		!containsString(hello.Features, wsAtomicClaimFeature) {
		log.Printf("[agent] manager lacks required WebSocket feature %q; using HTTP polling",
			wsAtomicClaimFeature)
		return errWSFallback
	}
	if err := conn.SetReadDeadline(time.Time{}); err != nil {
		return err
	}
	if n := a.flushSpool(); n > 0 {
		say("Flushed %d spooled result(s) after WebSocket reconnect", n)
	}
	say("WebSocket push mode active")

	// Heartbeat sender
	hbDone := make(chan struct{})
	heartbeatDone = hbDone
	heartbeatInterval := a.cfg.HeartbeatInterval
	if heartbeatInterval <= 0 {
		heartbeatInterval = 30 * time.Second
	}
	jobState := &wsJobState{}
	go func() {
		defer close(hbDone)
		ticker := time.NewTicker(heartbeatInterval)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				jobState.RLock()
				currentJobID := jobState.currentJobID
				pendingJobID := jobState.pendingJobID
				jobState.RUnlock()
				status := "online"
				if currentJobID != "" || pendingJobID != "" {
					status = "busy"
				}
				if writer.Write(map[string]interface{}{
					"type": "heartbeat", "status": status, "current_job_id": currentJobID,
				}) != nil {
					cancel()
					return
				}
			case <-sessionCtx.Done():
				return
			}
		}
	}()

	pendingResults := make(map[string]struct{})
	var pendingJob map[string]interface{}
	for {
		_, raw, err := conn.ReadMessage()
		if err != nil {
			return err
		}
		var m map[string]interface{}
		if err := json.Unmarshal(raw, &m); err != nil {
			log.Printf("[agent] ignoring malformed WebSocket message: %v", err)
			continue
		}

		switch m["type"] {
		case "job_push":
			jmap, ok := m["job"].(map[string]interface{})
			if !ok {
				log.Printf("[agent] ignoring malformed job_push payload")
				continue
			}
			jobID, _ := jmap["job_id"].(string)
			if _, err := a.spool.path(jobID); err != nil {
				log.Printf("[agent] rejecting job_push: %v", err)
				if writeErr := writer.Write(map[string]interface{}{
					"type": "job_ack", "job_id": jobID, "accepted": false,
				}); writeErr != nil {
					return writeErr
				}
				continue
			}

			jobState.Lock()
			canAccept := jobState.currentJobID == "" && jobState.pendingJobID == ""
			if canAccept {
				jobState.pendingJobID = jobID
				pendingJob = jmap
			}
			jobState.Unlock()
			if err := writer.Write(map[string]interface{}{
				"type": "job_ack", "job_id": jobID, "accepted": canAccept,
			}); err != nil {
				return err
			}
			if !canAccept {
				log.Printf("[agent] declined job offer %s while another job is pending or running",
					jobID)
			}

		case "job_claim":
			jobID, _ := m["job_id"].(string)
			jobState.Lock()
			matchesPending := pendingJob != nil &&
				jobState.pendingJobID == jobID &&
				str(pendingJob, "job_id") == jobID
			var claimedJob map[string]interface{}
			if matchesPending {
				claimedJob = pendingJob
				pendingJob = nil
				jobState.pendingJobID = ""
			}
			jobState.Unlock()

			if !matchesPending {
				log.Printf("[agent] ignoring job_claim for unstaged job %q", jobID)
				continue
			}
			claimed, _ := m["claimed"].(bool)
			if !claimed {
				log.Printf("[agent] manager rejected job claim %s: %v", jobID, m["reason"])
				if err := writer.Write(map[string]interface{}{
					"type": "heartbeat", "status": "online", "current_job_id": nil,
				}); err != nil {
					return err
				}
				continue
			}

			jobState.Lock()
			jobState.currentJobID = jobID
			jobState.Unlock()
			if err := writer.Write(map[string]interface{}{
				"type": "heartbeat", "status": "busy", "current_job_id": jobID,
			}); err != nil {
				return err
			}

			result := a.runJob(sessionCtx, claimedJob)
			payload := resultPayload(result)
			if err := a.spool.Save(jobID, payload); err != nil {
				// Disk durability failed. A synchronous HTTP acknowledgment is
				// the only safe fallback before releasing the in-memory result.
				if submitErr := a.transport.SubmitResult(jobID, payload); submitErr != nil {
					return fmt.Errorf("preserve result %s: spool: %v; HTTP fallback: %w",
						jobID, err, submitErr)
				}
				if cleanupErr := a.spool.Delete(jobID); cleanupErr != nil {
					log.Printf("[agent] HTTP fallback accepted %s; spool cleanup: %v",
						jobID, cleanupErr)
				}
				say("  Spool unavailable for %s; manager accepted HTTP fallback", jobID)
			} else if err := writer.Write(map[string]interface{}{
				"type":    "result",
				"job_id":  jobID,
				"success": payload["success"],
				"result":  payload["result"],
				"error":   payload["error"],
			}); err != nil {
				return err
			} else {
				pendingResults[jobID] = struct{}{}
			}

			jobState.Lock()
			jobState.currentJobID = ""
			jobState.Unlock()
			if err := writer.Write(map[string]interface{}{
				"type": "heartbeat", "status": "online", "current_job_id": nil,
			}); err != nil {
				return err
			}

		case "displaced", "error":
			say("WS: %v", m["message"])
			return fmt.Errorf("ws displaced")

		case "result_ack":
			jobID, _ := m["job_id"].(string)
			if _, pending := pendingResults[jobID]; pending {
				if err := a.spool.Delete(jobID); err != nil {
					log.Printf("[agent] result %s acknowledged but spool cleanup failed: %v",
						jobID, err)
				} else {
					delete(pendingResults, jobID)
				}
			}
		}

		if sessionCtx.Err() != nil {
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
			if err := a.heartbeatWithRetry(ctx, "online", "", 2); err != nil {
				log.Printf("[agent] online heartbeat failed: %v", err)
			} else {
				lastHB = time.Now()
			}
		}

		jobs, err := a.transport.PollJobs(a.cfg.JobLimit)
		if err != nil {
			say("Manager unreachable: %v — retrying…", err)
		} else {
			for _, job := range jobs {
				jobID, _ := job["job_id"].(string)
				if err := a.heartbeatWithRetry(ctx, "busy", jobID, 3); err != nil {
					message := fmt.Sprintf(
						"lease heartbeat failed; refusing to execute claimed job: %v", err,
					)
					log.Printf("[agent] job %s: %s", jobID, message)
					a.submitWithSpool(jobID, a.rejectJob(job, message))
					if onlineErr := a.heartbeatWithRetry(ctx, "online", "", 2); onlineErr != nil {
						log.Printf("[agent] rejection heartbeat failed: %v", onlineErr)
					}
					continue
				}
				result := a.runPolledJob(ctx, jobID, job)
				a.submitWithSpool(jobID, result)
				if err := a.heartbeatWithRetry(ctx, "online", "", 2); err != nil {
					log.Printf("[agent] post-job heartbeat failed: %v", err)
				}
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

func (a *Agent) runPolledJob(
	ctx context.Context,
	jobID string,
	raw map[string]interface{},
) map[string]interface{} {
	jobCtx, cancel := context.WithCancel(ctx)
	heartbeatDone := make(chan struct{})
	leaseFailure := make(chan error, 1)
	interval := a.cfg.HeartbeatInterval
	if interval <= 0 {
		interval = 30 * time.Second
	}
	go func() {
		defer close(heartbeatDone)
		ticker := time.NewTicker(interval)
		defer ticker.Stop()
		consecutiveFailures := 0
		for {
			select {
			case <-ticker.C:
				if err := a.heartbeatWithRetry(jobCtx, "busy", jobID, 2); err != nil {
					if jobCtx.Err() != nil {
						return
					}
					consecutiveFailures++
					log.Printf("[agent] lease heartbeat failed for job %s: %v", jobID, err)
					if consecutiveFailures >= 3 {
						leaseFailure <- fmt.Errorf(
							"lease heartbeat failed %d consecutive times: %w",
							consecutiveFailures, err,
						)
						cancel()
						return
					}
				} else {
					consecutiveFailures = 0
				}
			case <-jobCtx.Done():
				return
			}
		}
	}()

	result := a.runJob(jobCtx, raw)
	cancel()
	select {
	case <-heartbeatDone:
	case <-time.After(2 * time.Second):
		log.Printf("[agent] lease heartbeat worker did not stop before deadline")
	}
	select {
	case err := <-leaseFailure:
		message := fmt.Sprintf("scan cancelled because manager lease could not be renewed: %v", err)
		result["ok"] = false
		result["error"] = message
		switch existing := result["errors"].(type) {
		case []interface{}:
			result["errors"] = append(existing, message)
		case []string:
			result["errors"] = append(existing, message)
		default:
			result["errors"] = []string{message}
		}
	default:
	}
	return result
}

func (a *Agent) heartbeatWithRetry(
	ctx context.Context,
	status string,
	jobID string,
	attempts int,
) error {
	if attempts < 1 {
		attempts = 1
	}
	var lastErr error
	for attempt := 0; attempt < attempts; attempt++ {
		requestCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
		lastErr = a.transport.Heartbeat(requestCtx, status, jobID)
		cancel()
		if lastErr == nil {
			return nil
		}
		log.Printf(
			"[agent] heartbeat status=%s job=%s attempt=%d/%d failed: %v",
			status, jobID, attempt+1, attempts, lastErr,
		)
		if attempt+1 == attempts {
			break
		}
		delay := time.Duration(1<<attempt) * 250 * time.Millisecond
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(delay):
		}
	}
	return lastErr
}

// ── job execution ─────────────────────────────────────────────────────────────

func (a *Agent) runJob(ctx context.Context, raw map[string]interface{}) map[string]interface{} {
	job, err := mapToJob(raw)
	if err != nil {
		log.Printf("[agent] rejected job %s before execution: %v", job.JobID, err)
		return resultToMap(pipeline.Reject(job, a.probeID, err.Error()))
	}
	log.Printf("[agent] running job %s type=%s profile=%s", job.JobID, job.ScanType, job.Profile)

	result := pipeline.Run(ctx, job, a.probeID)
	say("  ✓ job %s done — %d hosts, %d ports, %d facts",
		job.JobID, result.HostCount, result.OpenPorts, result.FactCount)

	return resultToMap(result)
}

func (a *Agent) rejectJob(raw map[string]interface{}, message string) map[string]interface{} {
	job, _ := mapToJob(raw)
	if job.JobID == "" {
		job.JobID = str(raw, "job_id")
	}
	return resultToMap(pipeline.Reject(job, a.probeID, message))
}

func resultToMap(result pipeline.Result) map[string]interface{} {
	b, err := json.Marshal(result)
	if err != nil {
		return map[string]interface{}{
			"ok": false, "error": fmt.Sprintf("encode pipeline result: %v", err),
		}
	}
	var m map[string]interface{}
	if err := json.Unmarshal(b, &m); err != nil {
		return map[string]interface{}{
			"ok": false, "error": fmt.Sprintf("decode pipeline result: %v", err),
		}
	}
	return m
}

func (a *Agent) submitWithSpool(jobID string, payload map[string]interface{}) {
	envelope := resultPayload(payload)
	if err := a.spool.Save(jobID, envelope); err != nil {
		say("  Could not preserve result before submit: %v", err)
		if submitErr := a.transport.SubmitResult(jobID, envelope); submitErr != nil {
			say("  Submit also failed (%v); result could not be persisted", submitErr)
		} else if cleanupErr := a.spool.Delete(jobID); cleanupErr != nil {
			say("  Manager accepted result; spool cleanup failed: %v", cleanupErr)
		}
		return
	}

	if err := a.transport.SubmitResult(jobID, envelope); err != nil {
		say("  Submit failed (%v); preserved result remains spooled for retry", err)
		return
	}
	if err := a.spool.Delete(jobID); err != nil {
		say("  Manager accepted result but spool cleanup failed: %v", err)
	}
}

func (a *Agent) flushSpool() int {
	return a.spool.Flush(func(jobID string, payload map[string]interface{}) error {
		return a.transport.SubmitResult(jobID, normalizeResultPayload(payload))
	})
}

func resultPayload(result map[string]interface{}) map[string]interface{} {
	success, _ := result["ok"].(bool)
	payload := map[string]interface{}{
		"success": success,
		"result":  result,
		"error":   nil,
	}
	if errText, ok := result["error"].(string); ok && errText != "" {
		payload["error"] = errText
	}
	return payload
}

func normalizeResultPayload(payload map[string]interface{}) map[string]interface{} {
	if _, hasSuccess := payload["success"]; hasSuccess {
		if _, hasResult := payload["result"]; hasResult {
			return payload
		}
	}
	return resultPayload(payload)
}

// ── identity / registration ───────────────────────────────────────────────────

func (a *Agent) obtainIdentity(ctx context.Context) error {
	// Explicit configuration always wins over persisted state. Refuse partial
	// credentials rather than combining values from different trust sources.
	configuredID := strings.TrimSpace(a.cfg.AgentID)
	configuredToken := strings.TrimSpace(a.cfg.AgentToken)
	if configuredID != "" || configuredToken != "" {
		if configuredID == "" || configuredToken == "" {
			return fmt.Errorf("AGENT_ID and AGENT_TOKEN must be set together")
		}
		a.transport.AgentID = configuredID
		a.transport.AgentToken = configuredToken
		return nil
	}

	if a.cfg.StateFile != "" {
		state, err := loadIdentityState(
			a.cfg.StateFile,
			a.cfg.PlatformURL,
			a.cfg.ProbeName,
		)
		if err == nil {
			a.transport.AgentID = state.AgentID
			a.transport.AgentToken = state.Token
			return nil
		}
		if !os.IsNotExist(err) {
			log.Printf("[agent] ignoring unusable identity state %q: %v",
				a.cfg.StateFile, err)
		}
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
		if a.cfg.StateFile != "" {
			if err := saveIdentityState(
				a.cfg.StateFile,
				a.transport.AgentID,
				a.transport.AgentToken,
				a.cfg.PlatformURL,
				a.cfg.ProbeName,
			); err != nil {
				return fmt.Errorf("persist registered agent identity: %w", err)
			}
		}
		return nil
	}
}

// ── helpers ───────────────────────────────────────────────────────────────────

type useCasePlan struct {
	scanType string
	profile  string
}

var useCasePlans = map[string]useCasePlan{
	"uc_discovery_only":       {scanType: "discovery", profile: "it"},
	"uc_full_assessment":      {scanType: "assessment", profile: "it"},
	"uc_external_web_triage":  {scanType: "web_tls_scan", profile: "it"},
	"uc_db_exposure":          {scanType: "db_fingerprint", profile: "it"},
	"uc_windows_estate":       {scanType: "smb_enum", profile: "it"},
	"uc_ot_passive":           {scanType: "passive_discovery", profile: "ot"},
	"uc_ai_endpoint_sweep":    {scanType: "mcp_discovery", profile: "it"},
	"uc_rescan_delta":         {scanType: "assessment", profile: "it"},
	"uc_iot_device_survey":    {scanType: "discovery", profile: "iot"},
	"uc_web_app_triage":       {scanType: "web_scan", profile: "it"},
	"uc_udp_service_exposure": {scanType: "udp_scan", profile: "it"},
	"uc_snmp_exposure":        {scanType: "snmp_scan", profile: "it"},
}

func mapToJob(m map[string]interface{}) (pipeline.Job, error) {
	params := map[string]interface{}{}
	if rawParams, exists := m["params"]; exists {
		var ok bool
		params, ok = rawParams.(map[string]interface{})
		if !ok {
			return pipeline.Job{JobID: str(m, "job_id")}, fmt.Errorf("job params must be an object")
		}
	}

	jobType := strings.ToLower(strings.TrimSpace(firstStr(str(m, "job_type"), "discovery")))
	useCaseID := strings.TrimSpace(firstStr(str(params, "use_case_id"), str(m, "use_case_id")))
	j := pipeline.Job{
		JobID:        strings.TrimSpace(str(m, "job_id")),
		EngagementID: strings.TrimSpace(firstStr(str(m, "engagement_id"), str(params, "engagement_id"))),
		UseCaseID:    useCaseID,
		Concurrency:  int(floatOr(params["concurrency"], 100)),
		Timeout:      floatOr(params["timeout"], 3),
		DiscTimeout:  floatOr(params["disc_timeout"], 1.5),
	}
	j.Rate, _ = params["rate"].(float64)

	if useCaseID != "" {
		plan, ok := useCasePlans[useCaseID]
		if !ok {
			return j, fmt.Errorf("unknown use_case_id %q", useCaseID)
		}
		j.ScanType = plan.scanType
		j.Profile = plan.profile
	} else {
		j.ScanType = strings.ToLower(strings.TrimSpace(firstStr(
			str(params, "scan_type"),
			str(m, "scan_type"),
			defaultScanType(jobType),
		)))
		j.Profile = strings.ToLower(strings.TrimSpace(firstStr(str(params, "profile"), "it")))
	}

	if encrypted := strings.TrimSpace(firstStr(
		str(m, "encrypted_scope"), str(params, "encrypted_scope"),
	)); encrypted != "" {
		return j, fmt.Errorf(
			"encrypted scope is unsupported by the Go probe; refusing to execute",
		)
	}

	authoritativeScope, err := stringList(params["_scope_cidrs"], "_scope_cidrs")
	if err != nil {
		return j, err
	}
	embeddedScope, err := stringList(params["scope_cidrs"], "scope_cidrs")
	if err != nil {
		return j, err
	}
	if j.EngagementID != "" && len(authoritativeScope) == 0 {
		return j, fmt.Errorf(
			"manager-issued job lacks authoritative _scope_cidrs; refusing target-only payload",
		)
	}
	j.ScopeCIDRs = authoritativeScope
	if len(j.ScopeCIDRs) == 0 {
		j.ScopeCIDRs = embeddedScope
	}

	j.Targets, err = firstTargetList(params, m)
	if err != nil {
		return j, err
	}
	if len(j.Targets) == 0 {
		j.Targets = append([]string(nil), j.ScopeCIDRs...)
	}
	if len(j.Targets) == 0 {
		return j, fmt.Errorf("job has no requested targets")
	}

	authoritativeExcludes, err := stringList(params["_excluded_cidrs"], "_excluded_cidrs")
	if err != nil {
		return j, err
	}
	jobExcludes, err := stringList(params["excluded_cidrs"], "excluded_cidrs")
	if err != nil {
		return j, err
	}
	j.ExcludeCIDRs = dedupStrings(append(authoritativeExcludes, jobExcludes...))

	if err := pipeline.ValidatePlan(j.ScanType, j.Profile); err != nil {
		return j, err
	}
	return j, nil
}

func defaultScanType(jobType string) string {
	switch jobType {
	case "discovery":
		return "discovery"
	case "lateral":
		return "smb_enum"
	case "cloud_scan":
		return "vuln_scan"
	default:
		return jobType
	}
}

func firstTargetList(params, topLevel map[string]interface{}) ([]string, error) {
	for _, source := range []map[string]interface{}{params, topLevel} {
		for _, key := range []string{"targets", "target"} {
			if value, exists := source[key]; exists {
				targets, err := stringList(value, key)
				if err != nil {
					return nil, err
				}
				if len(targets) > 0 {
					return targets, nil
				}
			}
		}
	}
	return nil, nil
}

func stringList(value interface{}, field string) ([]string, error) {
	if value == nil {
		return nil, nil
	}
	var raw []string
	switch typed := value.(type) {
	case string:
		raw = []string{typed}
	case []string:
		raw = typed
	case []interface{}:
		raw = make([]string, 0, len(typed))
		for _, item := range typed {
			text, ok := item.(string)
			if !ok {
				return nil, fmt.Errorf("%s must contain only strings", field)
			}
			raw = append(raw, text)
		}
	default:
		return nil, fmt.Errorf("%s must be a string or list of strings", field)
	}

	cleaned := make([]string, 0, len(raw))
	for _, item := range raw {
		if item = strings.TrimSpace(item); item != "" {
			cleaned = append(cleaned, item)
		}
	}
	return dedupStrings(cleaned), nil
}

func dedupStrings(values []string) []string {
	seen := make(map[string]bool, len(values))
	out := make([]string, 0, len(values))
	for _, value := range values {
		if !seen[value] {
			seen[value] = true
			out = append(out, value)
		}
	}
	return out
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

func containsString(values []string, want string) bool {
	for _, value := range values {
		if value == want {
			return true
		}
	}
	return false
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
