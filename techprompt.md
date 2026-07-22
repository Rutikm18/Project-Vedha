# Implementation Prompt: Distributed Probe / Manager Architecture for VA Scanner

## What you are building

A **distributed vulnerability-assessment system** with two halves:

1. **Probe (agent)** — a lightweight, deployable unit that runs *inside* a client's network, executes the existing collection-only scanner stack, and ships raw results back as `result.json`. It holds no intelligence; it collects and reports.
2. **Manager (cloud)** — a central control plane that registers probes, hands them scope + use-cases + commands, receives `result.json`, runs detection/analysis/reporting, and stores everything per-client.

This is the classic **agent/controller split** used by commercial scanners (the probe is the sensor in the field; the manager is the brain in the cloud). The probe wraps the scanner module you already built; the manager wraps the Phase 1–5 detection pipeline already specified.

**Hard architectural rule, carried from the existing design:** the probe *collects only* — it sends benign read-only probes, never exploits. All correlation, CVE-matching, AI analysis, and risk-scoring happen on the **manager**, never on the probe. The probe never decides "vulnerable"; it only records facts. This keeps the field-deployed component dumb, auditable, and safe.

---

## System Topology

```
┌─────────────────────────────────┐         ┌──────────────────────────────────────────┐
│  CLIENT ENVIRONMENT (untrusted)  │        │  MANAGER / CLOUD (trusted control plane)  │
│                                 │         │                                          │
│  ┌───────────────────────────┐  │         │  ┌────────────────────────────────────┐  │
│  │ PROBE (agent)             │  │ outbound│  │ FRONTEND                           │  │
│  │                           │──┼─────────┼─>│  - per-client dashboards           │  │
│  │ - scanner module (13+2)   │  │ register│  │  - create VA cases                 │  │
│  │ - scope.txt (SOW)         │<─┼─────────┼──│  - showcase results                │  │
│  │ - workflow engine (gates) │  │ pull    │  └────────────────────────────────────┘  │
│  │ - use-case executor       │  │ cmd/api │  ┌────────────────────────────────────┐  │
│  │ - result emitter          │──┼─────────┼─>│ BACKEND                            │  │
│  │                           │  │ push    │  │  - probe registry + auth           │  │
│  │ emits: result.json        │  │ result  │  │  - command/use-case API issuer     │  │
│  └───────────────────────────┘  │         │  │  - result.json receiver            │  │
│                                 │         │  │  - detection (Phase 1)             │  │
│  Deployed via: install.sh       │         │  │  - verifier (Phase 3)              │  │
│  (curl | bash one-liner)        │         │  │  - validation (Phase 4, soon)      │  │
│                                 │         │  │  - attack-path mapping (soon)      │  │
│                                 │         │  │  - reporting (Phase 5)             │  │
└─────────────────────────────────┘         │  └────────────────────────────────────┘  │
                                            │  ┌────────────────────────────────────┐  │
   ALL communication is PROBE-INITIATED     │  │ DB (SQLite to start)               │  │
   outbound (probe → manager). Manager       │  │  - results data                    │  │
   never connects INTO the client network.  │  │  - VA cases                        │  │
   Probe polls/long-polls for commands.     │  │  - case actions + time + metadata  │  │
                                            │  │  - probe activation / last-seen    │  │
                                            │  └────────────────────────────────────┘  │
                                            └──────────────────────────────────────────┘
```

**Critical network-direction decision:** the probe lives in an untrusted client network. The manager must **never** open an inbound connection into that network (it can't anyway — NAT/firewall). So **all traffic is probe-initiated outbound over HTTPS**: the probe registers, then polls (or long-polls / opens a persistent outbound channel) to *pull* commands, and *pushes* results back. The "commands to the probe" arrow in your diagram is logical, not a literal inbound socket — the manager queues a command, the probe fetches it on its next poll.

---

## PART A — THE PROBE (agent in the field)

### A1. Deployment: `install.sh` (curl-to-execute bootstrap)

The probe deploys via a single command the operator runs on a host inside the client network:

```bash
curl -fsSL https://manager.example.com/install.sh | bash -s -- \
    --enroll-token <ONE_TIME_TOKEN> \
    --manager https://manager.example.com \
    --scope-url https://manager.example.com/api/v1/probes/<id>/scope
```

**What `install.sh` does (in order):**
1. **Verify host prerequisites** — Python 3.10+ (the scanner module's floor), enough disk for logs, outbound HTTPS reachability to the manager.
2. **Fetch + verify the probe package** — download the probe tarball, **verify its checksum/signature** against a value baked into the installer (supply-chain integrity: the operator must be able to trust the binary they're piping to bash).
3. **Pull the scope (SOW)** — retrieve `scope.txt` from the manager. This is the **authorization allowlist** — the Statement of Work boundary. Nothing outside it is ever scanned. The scope is signed by the manager so the probe can verify it wasn't tampered with in transit.
4. **Pull initial config** — host-discovery seed ranges, environment profile (it / iot / ot), rate caps.
5. **Establish identity** — exchange the one-time enroll token for a long-lived probe credential (mTLS client cert or a scoped API key). The enroll token is single-use and expires.
6. **Register with the manager** — POST probe metadata (hostname, OS, probe version, network vantage point) → manager records it in the probe registry, marks `last_seen`.
7. **Start the probe service** — install as a systemd unit (or container) that survives reboot and begins the poll loop.

**Install variants from your notes** (the `curl + install + X` lines) map to install flags:
- `curl + install + scope (SOW)` → `--scope-url` (mandatory: no scope, no install)
- `curl + install + host discovery input` → `--seed-ranges 10.0.0.0/24,10.0.1.0/24`
- `curl + install + SOW + ...` → combined: scope + profile + seed ranges in one bootstrap

**Security note on curl-pipe-bash:** this pattern is convenient but is itself a trust decision. Mitigate: serve `install.sh` only over HTTPS, pin the package signature inside the script, make the enroll token single-use and short-lived, and log every enrollment server-side so a leaked token is detectable.

### A2. Probe poll loop (the core runtime)

Once installed, the probe runs a loop. **All connections are outbound.**

```
LOOP:
  1. HEARTBEAT → POST /api/v1/probes/<id>/heartbeat
     - updates last_seen, reports probe health, current job status
     - manager uses this for the "probe activation / connection logs (last seen)" in the DB
  2. PULL COMMAND → GET /api/v1/probes/<id>/commands  (long-poll)
     - returns the next queued job, or 204 if nothing waiting
     - a job = { use_case_id, scope_version, profile, target_ranges, params }
  3. VALIDATE JOB locally
     - re-verify every target is inside the signed scope.txt (defense in depth —
       NEVER trust that the manager's job is in-scope; check again on the probe)
     - reject + report any out-of-scope target without scanning it
  4. EXECUTE use-case via the workflow engine (gates, caching, dynamic routing)
  5. EMIT result.json
  6. PUSH RESULT → POST /api/v1/probes/<id>/results  (body = result.json)
     - on failure, retry with backoff; persist locally so nothing is lost
  7. sleep(poll_interval) → back to top
```

### A3. Use-cases (the unit of work the manager assigns)

A **use-case** is a named, pre-defined scanning scenario the manager offers and the probe knows how to run. This is your "Probe have already defined use cases or scenarios that we can choose from manager." The manager picks one per client/environment; the probe executes it.

Each use-case is a **declarative job spec** the probe interprets against its existing engagement modes (triage / assessment / service-specific / re-scan) and profiles (it / iot / ot):

```json
{
  "use_case_id": "uc_external_web_triage",
  "display_name": "External web-surface triage",
  "engagement_mode": "service-specific",
  "profile": "it",
  "services": ["web", "tls"],
  "target_ranges": ["10.0.0.0/24"],
  "scope_version": "sow_2026_06_28_v3",
  "params": { "rate": 200, "concurrency": 100, "timeout": 3.0 },
  "expected_runtime_hint": "10-20 min"
}
```

**Pre-defined use-case library** (ship a starter set; the manager UI lets an operator pick one):
- `uc_discovery_only` → triage mode, discovery + ports + banner (fast "what's here?")
- `uc_full_assessment` → assessment mode, all branches (standard VA)
- `uc_external_web_triage` → service-specific, web + tls only
- `uc_db_exposure` → service-specific, db only ("are any databases exposed/unauth?")
- `uc_windows_estate` → service-specific, smb + (credentialed windows collector if creds provisioned)
- `uc_ot_passive` → ot profile, passive_collector only (hard-gated, zero active packets)
- `uc_ai_endpoint_sweep` → service-specific, mcp_ai only (exposed inference/MCP discovery)
- `uc_rescan_delta` → re-scan mode against a prior engagement_uuid ("what changed?")

The probe maps `use_case_id` → workflow-engine configuration. It does **not** invent new scan behavior; it selects among the gated, scope-checked scanners already built. This is what keeps an in-the-field component safe: its entire action space is the finite, read-only use-case library.

### A4. `result.json` (the probe's only output artifact)

The probe's sole deliverable. It is **raw collected facts** — the consolidated Asset model from the workflow engine, plus run metadata. **No findings, no CVEs, no scoring** — those are the manager's job.

```json
{
  "result_schema_version": "1.0",
  "probe_id": "probe_clientA_dc1_01",
  "engagement_uuid": "eng_2026_06_28_a1b2c3",
  "use_case_id": "uc_full_assessment",
  "scope_version": "sow_2026_06_28_v3",
  "profile": "it",
  "started_at": "2026-06-28T17:00:00Z",
  "finished_at": "2026-06-28T17:52:00Z",
  "probe_version": "1.4.0",
  "assets": [
    {
      "host": "10.0.0.5",
      "aliases": ["web-prod-01"],
      "last_seen_alive": "2026-06-28T17:01:00Z",
      "open_ports": { "443": { "status": "open", "proto": "tcp" } },
      "services": { "443": { "banner": "Apache/2.4.49 (Ubuntu)", "inferred_type": "web" } },
      "tls_facts": { "443": { "accepted_versions": ["1.2","1.3"], "cert": { } } },
      "web_facts": { "443": { "server": "Apache/2.4.49", "tech_hints": ["..."],
                              "security_headers_missing": ["CSP","HSTS"] } },
      "smb_state": null,
      "db_facts": {},
      "ai_facts": {},
      "credential_inventory": null
    }
  ],
  "raw_scan_results": [ /* every ScanResult JSONL line, for full provenance */ ],
  "run_stats": { "hosts_alive": 18, "packets_sent_estimate": 4200,
                 "cache_reused": 34, "scanners_run": ["host_discovery","port_scan", "..."] },
  "errors": [ /* any scanner errors, out-of-scope rejections, timeouts */ ]
}
```

**Why ship raw results too:** the manager's detection layer needs `evidence_refs` pointing back to exact observations (Phase 1 requirement). Carrying `raw_scan_results` preserves the audit trail end-to-end — every future finding traces to a packet-level fact the probe actually saw.

### A5. Probe security properties (non-negotiable)

- **Outbound-only.** The probe never listens for inbound connections from the manager. No inbound port is opened in the client network.
- **Scope re-validation on the probe.** Every job's targets are re-checked against the signed scope before any packet. A manager bug or a compromised manager cannot make the probe scan out-of-scope — the probe refuses. (This mirrors the existing "scope is structural, not a flag" guarantee.)
- **Read-only / collection-only.** The probe ships only the existing benign scanners. No exploit module is deployable to it. Its action space is the finite use-case library.
- **Credential handling.** If a use-case needs credentialed collection (ssh/windows), creds are delivered just-in-time, held in memory, never written to disk, never included in `result.json`, never logged. (Extends the existing "credentials never logged" rule.)
- **Result integrity.** `result.json` is signed by the probe so the manager can verify it came from the enrolled probe and wasn't altered.
- **Local persistence + retry.** Results are written locally and retried on upload failure so a flaky client network never loses an engagement's data.

---

## PART B — THE MANAGER (cloud control plane)

### B1. Backend responsibilities (maps your "Backend" list)

1. **Connection with probe** — probe registry, enrollment (issue/redeem one-time tokens), authentication (mTLS or scoped API keys), heartbeat tracking → drives "probe activation / last-seen" records.
2. **Create and send APIs/commands to probe** — a command queue per probe. An operator (via frontend) selects a use-case for a client/environment; the backend enqueues it; the probe pulls it on next poll. ("Commands or use-case API to the probe.")
3. **Receive result.json** — an authenticated ingest endpoint that verifies the probe signature, stores the raw artifact, and kicks off the analysis pipeline.
4. **Result analysis (detection + AI)** — run the already-specified pipeline on the received Asset data:
   - **Phase 1 Detection** — CPE normalization → offline OSV/NVD lookup → findings with evidence_refs.
   - **AI normalization assist (Phase 2)** — gated by deterministic lookup; AI proposes CPEs, the DB confirms; the model never emits a CVE.
   - **4.1 Validation using various sources (soon/next)** — corroborate findings against multiple data sources before surfacing.
5. **Attack-possibility mapping (soon)** — chain findings into attack paths across the asset graph (the lateral-movement frontier noted earlier). Mark explicitly as a later phase.
6. **Reporting (Phase 5)** — assemble findings into per-client reports with stability stats and evidence chains; optional AI prose summary over structured facts only.

### B2. Frontend responsibilities (maps your "Frontend" list)

1. **Different per client** — multi-tenant: each client sees only their own probes, scopes, cases, and results. Tenant isolation is enforced at the data layer, not just the UI.
2. **Create VA cases** — an operator defines a VA case (which client, which scope/SOW, which use-case, which target ranges, schedule) → this becomes the command queued to the probe.
3. **Showcase results** — dashboards rendering findings, severity, stability, trends, and the evidence chain for each finding; export to report.

### B3. Data model (DB — start with SQLite, as your diagram says)

SQLite is a fine starting point for a single-manager deployment; design the schema so a later move to Postgres is a swap, not a rewrite. Tables map directly to your "DB" list:

```
clients         (client_id, name, created_at, metadata)
probes          (probe_id, client_id, status, probe_version, last_seen,
                 enrolled_at, vantage_point, public_ip_last_seen)
scopes          (scope_id, client_id, sow_version, allowlist_blob_signed, created_at)
va_cases        (case_id, client_id, use_case_id, scope_id, target_ranges,
                 schedule, created_by, created_at)            -- "va cases"
commands        (command_id, probe_id, case_id, status[queued|pulled|running|done|failed],
                 enqueued_at, pulled_at, completed_at)         -- command queue
results         (result_id, probe_id, case_id, engagement_uuid,
                 raw_json_blob, received_at)                   -- "results data"
findings        (finding_id, result_id, client_id, cve_id, cpe, asset,
                 state, source_confidence, confidence, evidence_refs_blob,
                 created_at)                                   -- after VA/finding data
case_actions    (action_id, case_id, action_type, actor, timestamp, metadata)
                 -- "actions or existing cases with time + metadata (client name)"
probe_logs      (log_id, probe_id, event[enroll|heartbeat|pull|push|error],
                 timestamp, detail)                            -- "connection logs (last seen)"
```

Key design points from your notes:
- **"actions or existing cases with time + metadata (client name)"** → `case_actions` is an append-only audit log: who did what to which case, when. Immutable history.
- **"probe activation or connection logs (last seen added)"** → `probe_logs` + the `last_seen` column on `probes`, updated every heartbeat.
- **"after va or finding data"** → `findings` is populated only after the manager runs detection on a received result; it is never sent by the probe.

### B4. Manager API surface (the probe-facing contract)

All endpoints are HTTPS, probe-authenticated (mTLS client cert or scoped key), and **probe-initiated**:

```
POST /api/v1/enroll                         -- redeem one-time token → probe credential
POST /api/v1/probes/{id}/heartbeat          -- health + status; updates last_seen
GET  /api/v1/probes/{id}/scope              -- fetch current signed scope.txt
GET  /api/v1/probes/{id}/commands           -- long-poll for next queued job (or 204)
POST /api/v1/probes/{id}/results            -- upload signed result.json
POST /api/v1/probes/{id}/job-status         -- progress updates mid-scan (optional)
```

Operator/frontend-facing endpoints (separate auth, human users):
```
POST /api/v1/clients                        -- onboard a client
POST /api/v1/clients/{id}/scopes            -- upload + sign a SOW/scope
POST /api/v1/clients/{id}/cases             -- create a VA case (queues a command)
GET  /api/v1/clients/{id}/results           -- list results
GET  /api/v1/clients/{id}/findings          -- list findings (post-detection)
GET  /api/v1/clients/{id}/report/{eng}      -- generate/download report
```

### B5. The result-ingest pipeline (what happens when result.json lands)

```
POST /results received
  → verify probe signature + identity            (reject if not enrolled / bad sig)
  → verify engagement scope_version matches a known signed scope
  → store raw_json_blob in results table          (immutable, full provenance)
  → enqueue analysis job
       → Phase 1: ingest assets → CPE normalize → OSV/NVD match → findings
       → Phase 2: AI normalization assist on banner misses (DB-gated)
       → Phase 3: verifier — evidence-tiered confidence, backport suppression
       → write findings table (with evidence_refs back into raw_json_blob)
  → update va_case status = analyzed
  → frontend dashboards now render the new findings
  → (later) Phase 5 N-run aggregation if this is one of several runs
```

---

## PART C — END-TO-END SEQUENCE (one engagement, start to finish)

```
1.  Operator onboards Client A in the frontend.
2.  Operator uploads Client A's SOW → manager signs it → scopes table.
3.  Operator creates a VA case: client=A, use_case=uc_full_assessment,
    ranges=10.0.0.0/24, profile=it → backend enqueues a command.
4.  Field engineer runs the install one-liner on a host inside Client A's network:
        curl -fsSL https://manager/install.sh | bash -s -- --enroll-token <T> ...
5.  install.sh: verifies package sig → pulls signed scope → redeems token for a
    probe credential → registers → starts the probe service.   (probe_logs: enroll)
6.  Probe poll loop:
        heartbeat (last_seen updated) → GET /commands → receives the queued job.
7.  Probe re-validates every target against the signed scope (defense in depth).
8.  Probe runs the workflow engine for uc_full_assessment:
        gate 0 profile=it (not ot) → discovery → port_scan (live only) →
        service_banner → dynamic routing → tls/web/smb/db/snmp/mcp_ai branches →
        (credentialed collectors if creds provisioned).
9.  Probe consolidates everything into the Asset model → emits signed result.json.
10. Probe POST /results (retry-on-fail, persisted locally).      (probe_logs: push)
11. Manager verifies sig → stores raw → runs Phase 1 detection → Phase 3 verifier →
    writes findings.
12. Frontend dashboard for Client A now shows findings with severity, confidence,
    and evidence chains tracing back to the probe's raw observations.
13. Operator generates the report. case_actions logs every step with time + client.
14. Next week: operator creates a uc_rescan_delta case → probe re-runs, manager diffs
    against the prior engagement → "what changed" report.
```

---

## PART D — BUILD ORDER (what to implement, in sequence)

You noted "Scripts done (testing pending)" for the scanner backend — so the collection layer exists. Build outward from it:

**Milestone 1 — Probe result contract + emitter.**
Define `result.json` (A4) and make the existing workflow engine emit it. Test locally: run a scan, produce a valid signed result.json. No manager yet — write to disk.

**Milestone 2 — Minimal manager: ingest + store.**
Backend endpoint `POST /results` + SQLite schema (B3) for `results`. Manually POST a result.json, confirm it stores with provenance intact. Wire Phase 1 detection so a stored result produces findings.

**Milestone 3 — Probe enrollment + command pull.**
`install.sh` (A1) + enroll/heartbeat/commands endpoints (B4) + the poll loop (A2). Now a probe can register, pull a use-case, run it, and push results without manual steps.

**Milestone 4 — Use-case library + scope signing.**
Implement the pre-defined use-cases (A3) and signed-scope fetch + on-probe re-validation (A5). This is the safety core — do not ship field deployment without it.


**Milestone 5 — Frontend.**
Multi-tenant client view, VA-case creation (which queues commands), results/findings dashboards (B2). SQLite-backed.

**Milestone 6 — Hardening + later phases.**
mTLS, signature verification end-to-end, retry/persistence, then the "soon" items: validation-from-multiple-sources (4.1), attack-path mapping (5), Phase 5 N-run aggregation.

---

## Cross-cutting rules (hold in every milestone)

- **Probe is dumb, manager is smart.** Collection on the probe; all detection/AI/scoring on the manager. Never leak analysis logic into the field component.
- **All probe traffic is outbound, probe-initiated.** The manager never connects into the client network.
- **Scope is re-validated on the probe**, against a signed allowlist, before any packet — a compromised or buggy manager still cannot widen scope.
- **Read-only, finite action space.** The probe can only run the existing benign scanners via the use-case library. No exploit code is deployable to it.
- **Provenance is end-to-end.** Raw observations travel in result.json; every manager-side finding traces back to a packet-level fact the probe recorded.
- **Multi-tenant isolation at the data layer.** One client can never see another's probes, scopes, cases, or results.
- **Secrets never touch disk or logs or result.json.** Credentials for credentialed collection are just-in-time and in-memory only.

---

## Note on framing (keep this a legitimate VA product)

This architecture is a standard agent/controller vulnerability-assessment design: a sensor in the client network, a brain in the cloud, talking over an authenticated outbound channel, operating strictly within a signed Statement-of-Work scope, doing read-only collection. That is exactly how commercial VA platforms are structured, and the safety properties above (outbound-only, scope-re-validated, collection-only, finite action space, full provenance) are what keep it on the right side of the line — a vulnerability-assessment tool, not an autonomous attack framework. Keep every one of those properties as a hard requirement, not a configurable option.
```