# Pending / Completed Work — 2026-08-30

Work log for the last two requests on the Vedha network-VA pipeline.
**Status: code complete + tested locally, UNCOMMITTED. Needs redeploy to take effect.**

Run backend tests via `manager/backend/.venv/bin/python` (structlog/fastapi are not in
base python). Validate frontend via `node_modules/.bin/tsc --noEmit` (non-standard
Next.js per `frontend/AGENTS.md` — a full `next build` can't run in this env).

---

## Prompt 1 — "the pipeline of detection stuck at detection page… check the data flow… test at each phase"

### Root cause (my own bug)
`campaign_progress` decided detection was finished by checking `run.status == "done"`.
But `DetectionRun`'s success constant is `RUN_COMPLETED = "completed"` (see
`app/models/detection_run.py`: statuses are `running` / `completed` / `failed`).
So `detection_done` was **never** true → `overall_status` was stuck at `"detecting"`
forever, even after the backend had actually finished the run.

### Fix
File: `manager/backend/app/routers/engagements.py` (`campaign_progress`)
- Import and use the real constants: `from app.models.detection_run import DetectionRun, RUN_COMPLETED, RUN_FAILED`.
- `detection_done = bool(run and run.status == RUN_COMPLETED)`
- `detection_failed = bool(run and run.status == RUN_FAILED)`
- Added normalized `detection.done` / `detection.failed` to the response.
- `overall_status` state machine: `pending → scanning → aggregating (run is None) →
  detecting (run running) → complete (RUN_COMPLETED) | error (RUN_FAILED)`.
- `is_complete = bool(jobs) and scanning_done and detection_done` — the campaign is
  complete **only** when the whole pipeline finished, not when the scan job finishes.

Frontend: `frontend/app/campaign/[id]/CampaignProgress.tsx`
- "Complete" badge + polling both key off `is_complete` (polls every 4s until the
  whole pipeline is done, not just the scan).
- Empty-findings message keys off `is_complete` ("clean against current rules" vs
  "detection in progress").

### Data flow — verified intact (this was a DISPLAY bug, not a data bug)
```
probe result
  → agents.py / job_result_service.process_job_result
      • persists raw facts to scan_results table
      • enqueues TOPIC_FACTS_READY outbox event   (both atomic, one txn)
  → outbox worker  (python -m app.workers.outbox)
  → engine_bridge.create_findings_from_facts
      • run_full_detection  (CVE + posture)
      • DetectionRun: running → completed   (or → failed on exception; never hangs)
  → Findings  → prioritization (KEV/EPSS) → portal
```
**OPERATIONAL GOTCHA:** the outbox worker `python -m app.workers.outbox` MUST be
running, or detection never fires and the campaign sticks at "aggregating" (run=None).
That is a separate operational issue from the "done vs completed" display bug above.

### Testing at each phase
`manager/backend/tests/test_campaign_progress.py` — parametrized state-machine test
covering every phase transition:
| job_status | run_status | findings | overall_status | is_complete |
|-----------|-----------|----------|----------------|-------------|
| running   | None      | 0 | scanning    | False |
| completed | None      | 0 | aggregating | False |
| completed | running   | 0 | detecting   | False |
| completed | completed | 2 | complete    | True  | ← the fix (was stuck) |
| completed | completed | 0 | complete    | True  | (clean, zero findings) |
| completed | failed    | 0 | error       | False |
Plus `test_completed_run_is_not_stuck_at_detecting` as an explicit regression guard.
Invariant asserted: never `complete` unless `detection.done is True`.

---

## Prompt 2 — "detection should be on the manager side… use data from different lifecycle phases… give me the RAW data in the dashboard: what exactly did the scanner / vedha-agent main_scripts collect?"

Intent: the agent is collection-only (emits raw FACTS); the manager does 100% of
detection. Surface the **raw facts each scanner submitted, verbatim**, so you can
inspect exactly what the probe saw per lifecycle phase — the ground truth that feeds
detection. This is deliberately separate from *findings* (findings = the manager's
conclusions; raw-facts = the evidence the probe sent).

### Backend — new endpoint
File: `manager/backend/app/routers/engagements.py`
`GET /engagements/{engagement_id}/raw-facts`
- Reads the append-only `scan_results` table (`ScanResult.facts`, JSONB) and returns
  the facts **verbatim**, grouped by scanner name.
- Filters: `job_id` (one submission), `scanner` (one scanner's facts),
  `limit` (≤25 submissions), `max_facts` (≤20 000 per submission, sets `truncated`
  so a huge scan can't blow up the payload).
- Response shape:
  ```json
  {
    "engagement_id": "…",
    "scanners": ["port_scan","rdp_scan","smb_scan"],
    "by_scanner": {"port_scan":2,"rdp_scan":1,"smb_scan":1},
    "scan_results": [{
      "id","job_id","agent_id","scan_type","fact_count",
      "validation_state","created_at",
      "by_scanner": {…}, "facts": [ …raw ScanResult dicts… ], "truncated": false
    }]
  }
  ```
- **Security:** OPERATOR-GATED — `require_role(["admin","manager","tester"])`,
  tenant-scoped via `get_or_404`. Facts carry banners/hostnames, so this is NOT
  exposed to client / read-only roles. (Existing list endpoints redact
  `_REDACT = {"facts","ssh_creds","win_creds"}`; this endpoint is the deliberate,
  auth-gated exception for operators.)

### Frontend
- Proxy: `frontend/app/api/engagements/[id]/raw-facts/route.ts` — BFF proxy,
  forwards `job_id` / `scanner` / `limit` / `max_facts`.
- Component: `frontend/app/campaign/[id]/RawFacts.tsx`
  - Collapsed and **un-fetched by default** (facts can be large); lazy-loads on first
    open.
  - Scanner-filter chips built from the `by_scanner` breakdown (all · N, smb_scan · N…).
  - One card per submission (ScanResult) with per-submission scanner breakdown +
    expandable verbatim pretty-JSON facts; shows a truncation warning when hit.
- Wired as `<RawFacts engagementId={id} />` at the bottom of `CampaignProgress.tsx`
  (VA Campaigns view → below Findings & Remediation → "Raw scanner data").

### Why this is also the right diagnostic tool
It reads `scan_results` directly, so it works **regardless of detection status** —
even if the outbox worker is down and no findings exist yet, you can see exactly what
the probe sent. If a vuln's evidence (e.g. `smbv1_enabled: true`) shows up in
raw-facts but NOT in findings, the gap is in the manager detection/outbox path, not
the probe. That is the "scripts catch it but the manager doesn't" gap, made visible.

### Testing
`manager/backend/tests/test_raw_facts.py` (3):
- `test_raw_facts_grouped_by_scanner` — grouping + verbatim facts preserved
  (e.g. `smb.data.smbv1_enabled is True`, `negotiated_dialect == "0x0311"`).
- `test_raw_facts_filter_by_scanner` — `scanner=` filters `facts` but `by_scanner`
  still reflects ALL scanners (the full breakdown).
- `test_raw_facts_bounds_and_no_results` — `limit`/`max_facts` clamped; empty engagement.

---

## Verification (this pass)
- Backend: `test_raw_facts.py` (3) + `test_campaign_progress.py` (9) +
  `test_fleet_jobs.py` (3) = **15 passed**.
- Frontend: `tsc --noEmit` = **0 errors**.

## Files touched
Backend
- `manager/backend/app/routers/engagements.py`  (campaign_progress fix + raw-facts endpoint)
- `manager/backend/tests/test_raw_facts.py`  (new)
- `manager/backend/tests/test_campaign_progress.py`  (per-phase state machine)

Frontend
- `frontend/app/api/engagements/[id]/raw-facts/route.ts`  (new proxy)
- `frontend/app/campaign/[id]/RawFacts.tsx`  (new component)
- `frontend/app/campaign/[id]/CampaignProgress.tsx`  (wire RawFacts + is_complete)

## Deploy / operational notes (must do for this to take effect)
1. Redeploy the **manager backend** (campaign-progress fix + raw-facts endpoint +
   posture detection from earlier work).
2. Redeploy the **probe** (workflow RDP branch from earlier work).
3. Ensure the **outbox worker** is running: `python -m app.workers.outbox`.
   Without it, detection never fires and the campaign sticks at "aggregating".

## Remaining / open
- Everything above is UNCOMMITTED (no commit requested yet).
- "still not satisfied" — addressed below (Prompt 3) with the supporting research.

---

# Prompt 3 — "result still not accurate as expected… refer Supporting_research… proper system-level design… CHECK if already implemented (past cases weren't)… follow SDLC"

Supporting research read: `Supporting_research/vedha-pipeline-hardening (1).md`,
`vedha-platform-architecture-strategy.md`, `evidence_store.py`, `test_evidence_store.py`.

## Step 1 — AUDIT (what's actually in the code vs. claimed vs. research)

| Research mechanism | Real code state (verified, not claimed) |
|---|---|
| Outbox worker: lease / backoff / dead-letter / SKIP LOCKED / stale-requeue | ✅ ALREADY built (`app/workers/outbox.py`, 348 lines) |
| `DetectionRun` enum + `RUN_COMPLETED` in progress | ✅ present (prior fix) |
| **Detection trace** (every non-finding explains itself) | ❌ was MISSING — the centerpiece |
| Rule `requires` contract + MISSING-vs-absent distinction | ❌ was MISSING — `detect(f)`→evidence-or-None conflated drift/clean/no-evidence |
| Per-rule isolation (a raising rule can't blind the batch) | ❌ was MISSING (no try/except around `rule.detect`) |
| Coverage-proven completion, `complete_with_gaps`/`stalled`, worker heartbeat | ❌ MISSING (heartbeat/coverage-proof still open — see below) |
| Fact-contract CI gate | ❌ was MISSING |
| Idempotent findings via UNIQUE `dedupe_key` + `on_conflict_do_nothing` | ⚠️ partial (dedup by title/reaffirm) — still open |
| Assertion layer / identity resolution / retroactive detection (strategy doc) | ❌ MISSING (larger, deferred) |

**Root defect confirmed:** `_smbv1(f)` did `_d(f).get("smbv1_enabled") is True` → returned
`None` both when the key was ABSENT (probe drift → silent false-negative) and when it
was genuinely `False` (clean). The manager could not tell "checked and clean" from
"never actually checked". That is exactly *"the scripts catch it but the manager doesn't."*

## Step 2 — DESIGN (Stage 1 = observability-only, behaviour-preserving)

Followed the research's own staging (*"Never ship 1–4 together; Stage 1 = observability,
I'd expect this alone to answer what's still missing"*). Chose a **migration-free** Stage 1:
persist the trace roll-up into the EXISTING `DetectionRun.stats` JSONB (no new table),
so it's fully unit-testable here and safe to deploy.

## Step 3 — IMPLEMENT (all landed + tested)

**Detection engine** (`manager/detection_engine/posture_rules.py`):
- `get_path`/`_MISSING` — an absent key ≠ a collected `null`/`false`.
- `requires` contract added to every `PostureRule` (the fact.data paths it reads).
- Trace outcomes: `match / no_match / no_evidence / missing_input / unparseable / error`;
  `BLIND_OUTCOMES` = the silent-false-clean class.
- `evaluate_rule(rule, f)` — NEVER raises; checks `requires` BEFORE the predicate so an
  absent declared path is `missing_input` (drift), never `no_match`.
- `detect_posture_traced` / `detect_all_traced` — findings BYTE-IDENTICAL to before, plus
  the trace + asset-scoped `no_evidence`. `detect_posture`/`detect_all` now delegate →
  **zero behaviour change** for existing callers (19 existing posture tests still green).
- `verdict_for_rule` (finding/error/schema_drift/clean/no_evidence) + `summarize_traces`
  (`rules_blind`, `blind_rule_ids`, …).

**Pipeline** (`pipeline.py`): `run_full_detection` returns `posture_traces`,
`posture_coverage`, `posture_verdicts` (+ `counts.posture_blind_rules`).

**Bridge** (`app/detection/engine_bridge.py`): new `detect_all_from_facts_traced` →
`(cve, posture, meta)`; `create_findings_from_facts` persists
`run.stats["posture_coverage"]` + `run.stats["posture_verdicts"]` (migration-free).
`detect_all_from_facts` kept as a 2-tuple wrapper.

**API** (`app/routers/engagements.py`):
- `campaign-progress` extended: new `coverage` block, `reasons[]`, and a new
  `overall_status = "complete_with_gaps"` when a completed run has blind rules
  (`is_complete` stays true — it's terminal, just not clean). `aggregating` now carries a
  reason naming the outbox worker.
- NEW `GET /engagements/{id}/detection-explain[?rule_id=]` — per-rule verdict + reasons,
  gaps sorted first. Operator-gated (admin/manager/tester), tenant-scoped.

**Frontend**:
- `CampaignProgress.tsx`: coverage strip (`N/M checks assessed`, `k blind (unknown, not
  clean)`), reasons banner, `complete_with_gaps` label + amber status dot, and a new
  `FindingsEmpty` component that **replaces the dangerous "clean against current rules"**
  string with honest states (error / not-run / *"No findings, but the scan was incomplete
  — treat as unknown, not clean"* / genuinely clean).
- New proxy `app/api/engagements/[id]/detection-explain/route.ts`.

**Fact contract (the research's highest-leverage test)** — `test_fact_contract.py` +
`tests/fixtures/probe_corpus/` (seed shapes): asserts every rule's `requires` path is
emitted by some scanner. Replace seeds with REAL captures via `GET …/raw-facts` (README
in the corpus dir). Also surfaces the "emitted-but-unconsumed" detection backlog.

## Step 4 — VERIFY
- detection_engine: **246 passed** (was 232; +11 `test_posture_trace`, +3 `test_fact_contract`; 0 regressions).
- backend: **24 passed** across `test_detection_coverage` (6 new), campaign, engine_bridge,
  raw-facts, fleet.
- frontend `tsc --noEmit`: **0 errors**.

## Files touched (Prompt 3)
- `manager/detection_engine/posture_rules.py`, `pipeline.py`
- `manager/detection_engine/tests/test_posture_trace.py` (new), `test_fact_contract.py` (new),
  `tests/fixtures/probe_corpus/*` (new)
- `manager/backend/app/detection/engine_bridge.py`
- `manager/backend/app/routers/engagements.py`
- `manager/backend/tests/test_detection_coverage.py` (new); updated
  `test_engine_bridge_posture.py`, `test_engine_bridge_resolution.py` (patch traced fn)
- `manager/frontend/app/campaign/[id]/CampaignProgress.tsx`
- `manager/frontend/app/api/engagements/[id]/detection-explain/route.ts` (new)

## Deploy note
Migration-free (uses existing `DetectionRun.stats` JSONB). Redeploy manager backend +
frontend; coverage/verdicts populate on the NEXT detection run per engagement.

## Remaining after Prompt 3 — see Stage 2 below (now done, migration-free)

---

# Stage 2 — reconciled completion + worker liveness (correctness, migration-FREE)

Delivered the research's Stage-2 correctness core WITHOUT migrations (so it deploys with
zero migration step to miss — the coverage signal is derived from the EXISTING
`DetectionRun.scan_result_id` + `scan_results`, not a new column).

### A. Coverage-PROVEN completion (F11/F12 — multi-agent premature-complete)
`campaign_progress` now fetches ALL DetectionRuns (not just the latest) and proves
completion: every `scan_results` row for the engagement must have a COMPLETED run
(`sr_ids <= covered`). A campaign with 2 agents no longer flips to "complete" the moment
the LAST job's run finishes while an earlier submission is still undetected. Falls back to
the single-run signal when submissions aren't linkable (old data). New response block
`evidence{submissions,covered,fully_covered}`.

### B. `stalled` phase (F2 — dead/wedged worker made visible)
New status `stalled`: queried undrained `facts.ready` outbox events whose `available_at`
is older than `_QUEUE_STALL_SEC` (120s) → the queue isn't draining → the worker is down or
wedged, with a specific reason instead of a permanent "aggregating" spinner. A dead-lettered
facts event → `error`. New response block `queue{pending,overdue,dead}`.

### C. DetectionRun reaper (F4 — worker dies mid-detection)
`app/workers/outbox.py`: `_reap_stale_runs` (+ `_reap_runs_stmt`) marks runs stuck RUNNING
past `DETECTION_RUN_STALE_SEC` (2× the event lease = 10 min) as FAILED — so a crashed
detection worker's campaign moves to `error` instead of hanging at "detecting" forever.
Wired into the worker's periodic sweep next to `_reclaim_stale`.

### Refactor
Pure `_reconcile_status(...)` helper (engagements.py) derives ONE phase from reconciled
signals (jobs/queue/runs/coverage/gaps) — independently unit-tested across all precedence
branches. `campaign_progress` query order is now: get_or_404 → jobs → [agents] → runs(all)
→ scan_result_ids → queue_rows → findings.

### Frontend
`CampaignProgress.tsx`: `Stalled` label, `evidence` "N/M submissions detected" line (amber
when incomplete), polling backs off to 30s while stalled (don't hammer a dead worker).
`FindingsEmpty` already covers stalled/error.

### Verify
- backend: **54 passed** (new `test_stage2_reconcile.py` = 18: pure state-machine table,
  multi-agent coverage, stalled, dead-letter, reaper; + updated campaign/coverage mocks for
  the new query order; + `test_outbox_reclaim` still green).
- detection_engine: **246**; frontend `tsc`: **0**.

### Files (Stage 2)
- `manager/backend/app/routers/engagements.py` (`_reconcile_status`, reconciled campaign_progress)
- `manager/backend/app/workers/outbox.py` (`_reap_stale_runs` + loop wiring)
- `manager/backend/tests/test_stage2_reconcile.py` (new); updated `test_campaign_progress.py`,
  `test_detection_coverage.py` (new query order)
- `manager/frontend/app/campaign/[id]/CampaignProgress.tsx`

# Prompt 4 — "different approach like a security expert, stronger detection logic; refer AttackLens, use only what's actually required, verify"

AttackLens is a sibling project (host-EDR telemetry: processes/ports/persistence/lateral
movement) — NOT in this tree; used the pasted doc as reference only. Its domain differs
from Vedha's unauthenticated network-VA, so I did NOT port it wholesale.

## Verify-first (the instruction: only adopt what's actually required)
Audited the existing detection confidence/correlation:
- **CVE track ALREADY has AttackLens-grade confidence** — `verifier.py`: evidence tiers
  (authoritative/protocol/multi-signal/single-banner → 95/85/70/50), transparent logged
  downgrades (backport, AI-cap, filtered, auth, deception) in `checks{}`, only-ever-lower
  anti-FP, pure/deterministic. Also `correlate.py` (dedup + authoritative-suppression +
  one composite MS17-010 rule) and `_persist_attack_paths` (composite attack-PATH findings).
- **POSTURE track had NONE of it** — flat `confidence = _STATE_CONF[state]` (90/65/45), no
  evidence calibration, no corroboration, no audit trail. The posture findings (SMBv1,
  RDP-NLA, TLS, MSRPC, SNMP) are exactly the config/exposure vulns that matter here.

## What I adopted (only the genuinely-missing pieces, domain-adapted)
New `manager/detection_engine/posture_confidence.py`:
- **Separates confidence from impact** (verifier.py's principle): confidence = "likely a
  true positive"; impact stays `compute_risk`'s risk_score. This module never touches
  severity/risk/state.
- **Auditable** `precision_factors{}` on every posture finding (base tier, each factor,
  final) — mirrors verifier's `checks{}`.
- **Cross-signal attack-chain corroboration matrix** (AttackLens `cross_matrix` idea,
  network-VA-adapted) — the new "strong logic": when ≥2 independent posture signals compose
  a real attack path on ONE host, every member's confidence is FLOORED higher (independent
  agreement = strong TP evidence). Chains: `ntlm_relay_surface` (SMBv1+signing-off→92),
  `rdp_preauth_surface` (RDP-no-NLA+exposed→88), `weak_tls_cluster` (≥2 TLS weaknesses→85),
  `exposed_windows_infra` (RPC+SMB+SNMP→82). A LONE member gets NO floor (never inflates).
- **Downgrades** (only-ever-lower): unconfirmed reachability (filtered port −20), deception
  hook (−25/−10).
Wired via `calibrate_host_findings` (second pass in `detect_posture_traced`, after the
host's rules are known, so corroboration can see partners). Best-effort/lazy-imported so
calibration can never sink detection. `PostureFinding` gained `precision_factors`.

Deliberately did NOT adopt from AttackLens (not required / wrong domain / against strategy):
clustering (scan-batch, not streaming), AI-in-runtime-decision (violates "AI never decides
the verdict"), terrain validators (impact-page concept), a second remediation KB (posture
rules already carry deterministic remediation).

## Surfaced
`campaign_progress` findings now include `confidence` + `corroborated_by[]` (read from the
posture finding's evidence). Frontend: `conf N` + a `⛓ corroborated` chip on the finding row.

## Verify
detection_engine **257** (+11 `test_posture_confidence.py`: pure assessor, chain matrix,
end-to-end floor/lone/filtered/serialization; 0 regressions), backend **54**, frontend `tsc` **0**.

## Files (Prompt 4)
- `manager/detection_engine/posture_confidence.py` (new), `posture_rules.py` (field + calibrate pass)
- `manager/detection_engine/tests/test_posture_confidence.py` (new)
- `manager/backend/app/routers/engagements.py` (surface confidence/corroboration)
- `manager/frontend/app/campaign/[id]/CampaignProgress.tsx` (conf + corroborated chip)

# Stage 2b — migration-backed liveness refinements (DONE)

Finishes the pieces Stage 2 approximated migration-free.

### Migration 0034 (`0034_run_lease_worker_heartbeat.py`, revises 0033 — additive, no backfill)
- `detection_runs.lease_expires_at` (nullable) + index `ix_detection_runs_lease`.
- new `worker_heartbeats` table (worker_name PK, last_beat_at, meta) + index.

### Per-run lease → precise reaping (F4, sharper)
- `engine_bridge.create_findings_from_facts` stamps `lease_expires_at = now +
  DETECTION_RUN_LEASE_SEC` (10 min, == the worker's reaper threshold) on the run.
- `outbox._reap_runs_stmt(now, age_cutoff)` reaps `RUNNING` where `lease_expires_at < now`
  (precise) OR `lease_expires_at IS NULL AND started_at < age_cutoff` (fallback for
  historical runs) → no legitimate run is ever reaped early.

### Worker heartbeat → precise stalled (F2, sharper) + operational visibility
- `WorkerHeartbeat` model + `outbox._write_heartbeat("outbox")` upserts (pg
  `on_conflict_do_update`) every ~30s sweep tick.
- `campaign_progress` reads the freshest heartbeat (best-effort, LAST query, wrapped in
  try/except so a pre-migration missing table degrades to the queue-lag signal instead of
  erroring the page). `_reconcile_status` now: `stalled` when `queue_pending AND
  (queue_overdue OR worker_alive is False)` — a dead worker is caught BEFORE events age
  out. `worker_alive` (True/False/None) exposed in the response `queue{}` block.

### dedupe_key (F5/F6) — RESOLVED as not-needed (not deferred)
Verified against the actual code: Vedha's finding lifecycle is find-then-**update**
(`_find_open_duplicate` → reaffirm the SAME row; `_find_remediated_match` → regression-
reopen the SAME row). It NEVER does INSERT-OR-REPLACE, so the F6 triage-wipe cannot occur.
And the outbox claims events with `FOR UPDATE SKIP LOCKED`, so the same event is never
processed by two workers concurrently → the F5 duplicate-insert race doesn't arise either.
Adding a UNIQUE `dedupe_key` would be defense-in-depth against a race the architecture
already prevents, at the cost of either batch-transaction poisoning (naive) or per-finding
savepoints (untestable here). Correct call: don't add it; document the reasoning.

### Verify
backend **60 passed** (Stage 2b: +6 in `test_stage2_reconcile.py` — worker_alive pure
cases, `_write_heartbeat`, fresh/stale-heartbeat integration, lease-aware reap stmt);
`app.main` + `app.workers.outbox` import clean; migration compiles, revision chain clean
(0034→0033, single head).

### Files (Stage 2b)
- `alembic/versions/0034_run_lease_worker_heartbeat.py` (new)
- `app/models/worker_heartbeat.py` (new), `app/models/__init__.py`, `app/models/detection_run.py`
- `app/detection/engine_bridge.py` (lease stamp + const), `app/workers/outbox.py`
  (lease reaper + heartbeat), `app/routers/engagements.py` (worker_alive)
- `tests/test_stage2_reconcile.py`

### Deploy note
Run `alembic upgrade head` (applies 0034) before/with the manager redeploy. Pre-migration,
the page degrades gracefully (worker_alive=None → queue-lag stalled signal).

---

## Roadmap (future initiatives, not in-flight tasks)
- **Stage 4 (prioritization):** BOD 26-04 tier table + EPSS v5 bulk ingest.
- **Strategy doc (bigger):** assertion layer (L2), identity resolution (`evidence_store.py`
  ref), retroactive detection, coverage attestation / VEX.
- Everything UNCOMMITTED.
