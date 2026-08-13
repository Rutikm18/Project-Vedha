# Learnings

## 2026-08-11

### Coverage ledger
**What:** A per-`DetectionRun` record of `(asset, service_identity, scanner)` tuples that were *provably* re-scanned (`scanner_runs[].status == completed`), derived from probe telemetry.
**Why:** Auto-resolution requires proof that we *looked* at an asset/service and didn't see the finding — not just that the finding wasn't in the result. Degraded/skipped/failed scanners must not count as coverage.

### Coverage-gated auto-resolution with confirmation window
**What:** A finding is auto-closed only when its asset/service appears in the coverage ledger AND the finding is absent for N consecutive qualifying runs (N varies by severity: default 1 for low/medium, 2 for critical/KEV).
**Why:** The existing `first_seen`/`last_seen`/`detection_run_id` infrastructure surfaced "resolution candidates" but deliberately never auto-closed them; partial/degraded scans made absence untrustworthy. The confirmation window absorbs flaky or partial scans before committing to `remediated`.

### DB-version guard on auto-resolution
**What:** Before treating a finding's absence as a remediation signal, compare the run's `vuln_db_version` against the `detected_db_version` stamped on the finding. A mismatch means the vuln DB changed, not that the host was patched.
**Why:** A pinned-DB refresh can drop or rename CVE matches; without this guard, a DB update would appear as a mass-remediation wave on the dashboard.

### Regression detection on auto-resolved findings
**What:** If a finding already marked `remediated` is observed again in a later covered run, it is auto-reopened with a `reopened_count` increment and a `REGRESSION` badge.
**Why:** A vulnerability that came back after being closed is higher-urgency than a fresh one and must be surfaced distinctly rather than merged silently into open findings.

### Tiered verification (passive + active)
**What:** A two-tier FP-reduction approach: (1) passive — offline cross-corroboration of all asset facts using the LangGraph subgraph, confidence can only be maintained or lowered; (2) active — approval-gated, non-destructive validation job sent back to the probe (safe PoC / protocol handshake) for high-sev/KEV suspected findings.
**Why:** Version-matching alone produces false positives from backported fixes; a safe PoC that *fails* on a version match is the strongest possible FP signal (`contradicted` state), and a PoC that *succeeds* is the one legitimate path to upgrading a network-observed finding to `confirmed`.

### LangGraph verification/triage subgraph
**What:** A bounded `StateGraph` (`intake → corroborate → decide_escalation → [active_validation →] interpret → finalize`) with durable checkpoints and a human-in-the-loop interrupt at the approval gate; lives in `app/ai/verification_graph.py`, optional behind a settings flag.
**Why:** The active-validation escalation is a stateful, interruptible workflow (reason → request external job → wait → interpret result) — LangGraph's checkpoint/pause/resume maps 1:1 to this; direct-SDK tool-use loops don't give durable state-machine semantics across the async validation round-trip.

### Risk rank (composite priority)
**What:** A single 0–1000 score combining base CVSS severity, exploit likelihood (EPSS + KEV), verification state, confidence, asset criticality, and exposure (internet-facing, auth-enforced) — used as the default sort order on the findings dashboard.
**Why:** Raw severity alone over-ranks low-confidence inferred findings on hardened internal assets; the composite rank surfaces verified + exploitable + internet-exposed findings at the top while sinking `contradicted` / low-confidence ones.
