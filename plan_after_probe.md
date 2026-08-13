# Plan — After the Probe: Manager-Side Vulnerability Detection, Verification & Lifecycle

> **Status:** design plan (no code yet).
> **Scope:** enhancement layer on the *existing* manager detection engine. This plan does **not** re-architect the deterministic pipeline that already ships — it adds three capabilities on top of it and surfaces them on the dashboard.
> **Author intent:** turn "the probe shipped raw facts" into "verified, low-false-positive, self-healing findings, ranked by real risk," with a bounded agentic layer that never becomes the source of truth.

---

## 0. TL;DR

The probe ships **raw facts**; the manager already turns those into **Findings** through a deterministic, offline pipeline with an evidence-tiered confidence model. This plan adds three things and one cross-cutting surfacing layer:

1. **Auto-resolution lifecycle (coverage-gated)** — when a later scan *provably re-covers* an asset/service and the finding is gone, auto-close it (with a confirmation window, full audit, and one-click reopen). *Absence is only trusted when coverage is proven.*
2. **Tiered verification** — passive evidence corroboration for every finding; **approval-gated, non-destructive active validation** escalated only for high-severity / KEV suspected findings. This is what makes a finding an **actual** vulnerability, not an inference.
3. **LangGraph verification/triage subgraph** — a bounded, checkpointed, human-in-the-loop orchestrator that gathers evidence, lowers confidence, or requests active validation. It **cannot** invent CVEs, mutate findings, or auto-confirm without a positive control. Fail-closed: if it's unavailable, the deterministic finding stands unchanged.
4. **Risk-rank + lifecycle surfacing** — one sortable priority (severity × CVSS × EPSS × KEV × exploit-validated × verification-state × asset-criticality × exposure) plus a verification badge and a lifecycle timeline on the dashboard.

**Build order (rationale below):** auto-resolution first (pure backend, deterministic, highest value, zero AI risk) → passive verification → active validation → risk-rank unification.

---

## 1. What already exists (the spine we build on)

Documented here only enough to anchor the integration points. See `ARCHITECTURE.md §4–5` and `manager/detection_engine/`.

```
Probe facts  ──POST /agents/{id}/jobs/{job_id}/result──▶  backend
      │
      ▼  (FastAPI BackgroundTask, off the request path)
run_detection_job                                   app/detection/engine_bridge.py:208
      └─ create_findings_from_facts                 engine_bridge.py:108
            ├─ detect_findings_from_facts → detection_engine.run_pipeline
            │     ingest → cpe_normalize → match(pinned vuln DB) → dedup
            │     → suppress_negated → correlate → enrich(CVSS/EPSS/KEV) → verify
            ├─ open a DetectionRun (provenance: facts, vuln_db_version, counts)
            ├─ reaffirm: open duplicate → advance last_seen, point at run
            └─ new finding → insert (first_seen=last_seen=now, detection_run_id)
```

Key facts that shape this plan:

- **The verifier already exists** (`detection_engine/verifier.py`): evidence tiers (authoritative → protocol → multi-signal → single-banner), backport-aware downgrade, AI-assist confidence cap, deception/honeypot scoring. **Rule: it only ever *lowers* confidence, never raises.** Anti-FP is already a design pillar.
- **Finding lifecycle scaffolding already exists** (`models/finding.py`): `first_seen`, `last_seen`, `detection_run_id`; `DetectionRun` makes findings a time series (`findings_new / reaffirmed / current`, stamped `vuln_db_version`). The code comment at `finding.py:52` explicitly states a finding whose `last_seen` lags the latest run is *"a resolution candidate (surfaced, never auto-closed)."* **Auto-closing is deliberately not done yet — this plan is where we do it, safely.**
- **AI is already integrated via the Anthropic SDK directly** (`app/ai/agent.py`), grounded + read-only + human-in-the-loop, model from `settings.llm_model` (Sonnet/Opus/Fable), no temperature, effort-capped. It is **best-effort/optional** (absent SDK or key → clean 503). We mirror this posture for LangGraph.
- **A gated approval pattern already exists** (`models/exploit_approval.py`): `ExploitApprovalRequest` links a finding + target, moves `pending → approved`, and auto-queues a job on approval. **We reuse this exact pattern for active-validation approval.**
- **Probe already reports coverage telemetry**: `scanner_runs[]` carries per-component `completed | cached | skipped | degraded | failed`. This is the raw material for the coverage ledger.
- **Statuses today** (`enums.py FindingStatus`): `open, confirmed, remediated, accepted, fp`. **Severity** (`FindingSeverity`): `critical/high/medium/low/info`. **Asset criticality** and **risk_score (0–1000)** already exist, as does the posture scorecard.

**Design consequence:** we are extending, not replacing. Every new stage is additive, best-effort, and fails closed to today's behavior.

---

## 2. Locked design decisions

| # | Decision | Choice | Why |
|---|----------|--------|-----|
| D1 | What "verifiable / actual vulnerability" means | **Tiered**: passive evidence corroboration for all; approval-gated non-destructive active validation escalated for high-sev/KEV suspected | Balances "actual" with low-FP and client-network safety |
| D2 | Auto-resolution policy | **Coverage-gated + confirmation window** | Absence ≠ remediation unless the re-scan provably covered the asset/service; window absorbs flaky/partial scans |
| D3 | Agentic framework & placement | **LangGraph**, confined to a **verification/triage subgraph** (evidence-gather / lower-confidence / request-review only) | Durable checkpoints + conditional routing + HITL interrupts map 1:1 to a gated security flow; kept out of the deterministic core |
| D4 | Plan scope | **Enhancement layer** on the existing engine | The deterministic engine + pinned vuln DB already work and are auditable |

---

## 3. Target architecture (enhanced data flow)

New stages marked **[NEW]**. Everything runs inside the existing background `run_detection_job` (off the probe-result request path) or in follow-up gated jobs.

```
Probe facts ──▶ run_detection_job
  │
  ├─ create_findings_from_facts            (deterministic engine + DetectionRun + reaffirm)   [exists]
  │
  ├─ build_run_coverage                    what (asset, service, scanner) was PROVEN scanned  [NEW]
  │        source: scanner_runs[].status == completed  (degraded/skipped/failed ≠ covered)
  │
  ├─ evaluate_resolutions                  coverage-gated auto-resolve + confirmation window  [NEW]
  │        open, not-reaffirmed, covered  → pending_remediation (miss_count++)
  │        miss_count ≥ N (per severity)  → remediated (auto, audited, reopenable)
  │        reappears in a covered run     → reopen + REGRESSION flag
  │
  ├─ verification_orchestrator             LangGraph subgraph, per suspected/high finding      [NEW]
  │        ├─ intake        load finding + ALL asset facts + KEV/EPSS/CVSS + exposure (read-only)
  │        ├─ corroborate   passive verdict {maintain | lower | request_active | contradicted}
  │        ├─ escalate?     high-sev/KEV + suspected + RoE allows → active_validation
  │        ├─ active_validation   create GATED validation job  → checkpoint + PAUSE
  │        ├─ interpret_active     read proof → confirm | contradict | inconclusive
  │        └─ finalize      write verification_state + evidence bundle + pending recommendation
  │
  ├─ compute_risk_rank                     unified priority for ordering                       [NEW]
  │
  └─ persist + emit                        findings + lifecycle transitions + audit
           ▼
      Dashboard: severity chip + verification badge + confidence + lifecycle timeline
                 + coverage/resolution evidence + risk-ranked ordering                        [NEW/extend]
```

---

## 4. Capability 1 — Auto-resolution lifecycle (coverage-gated)

**Goal:** when a vulnerability is fixed and the next qualifying scan doesn't see it, auto-mark it resolved on the dashboard — **without ever falsely telling a customer they're safe.**

### 4.1 The core safety principle

> **Absence of a finding is only meaningful if we can prove we looked.**

A finding disappearing from a run has *four* possible causes, and only one is "fixed":

1. The vuln was actually remediated. ✅ (what we want to auto-close)
2. The asset/service wasn't scanned this run (host down, out of target set, scanner skipped/timed out). ❌ must NOT close
3. The scanner *ran but degraded* (partial output). ❌ must NOT close
4. The **vuln DB changed** — the CVE no longer matches the same version (DB regression / re-scoping), not a fix. ❌ must NOT close

The whole design is about distinguishing (1) from (2)/(3)/(4).

### 4.2 The coverage ledger `[NEW]`

For each `DetectionRun`, record the set of **proven-covered** `(asset, service_identity, scanner)` tuples:

- Derived from the probe's `scanner_runs[]` where `status == completed` (explicitly **not** `degraded/skipped/failed`; `cached` is configurable — default *not* covered, since cache means we didn't re-observe).
- `service_identity` = `(asset, product)` primarily, with port as secondary — so a service that moved ports still matches (avoids false "resolved" when a service relocates).
- Stored on `DetectionRun.stats` JSONB initially (`stats.coverage`), promotable to a dedicated `run_coverage` table if query volume warrants.

### 4.3 Resolution evaluation `[NEW]`

New step after `create_findings_from_facts`, same DB session/run:

```
for each finding F where F.status in (open, confirmed) and F.detection_run_id != this_run:   # not reaffirmed
    if F.(asset, service) NOT in this_run.coverage:
        annotate F "not re-observed — out of coverage"     # leave open, do NOT touch counter
        continue
    if this_run.vuln_db_version != F.detected_db_version:
        annotate F "absent under DB {v}; not a confirmed fix"   # DB-change guard, leave open
        continue
    # genuine, coverage-proven disappearance:
    F.status = pending_remediation
    F.resolution_miss_count += 1
    if F.resolution_miss_count >= threshold(F.severity):
        F.status        = remediated
        F.resolved_at   = now
        F.resolution_method = "auto"
        F.resolution_run_id = this_run.id
        F.evidence["resolution"] = coverage proof + reason
```

- **Confirmation window** `threshold(severity)`: default **1** qualifying covered run for low/medium; configurable to **2** for critical/KEV (don't celebrate a critical fix on a single clean scan). Per-engagement override.
- **Reaffirm resets everything:** if the finding is seen again in a covered run before it reaches `remediated`, reset `resolution_miss_count = 0`, status back to `open`, note "flapped."
- **Regression detection:** if a finding already `remediated` is observed again in a later covered run → auto-**reopen**, increment `reopened_count`, and raise a **REGRESSION** flag (a vuln that came back is more urgent than a fresh one — surfaced distinctly).

### 4.4 Data model changes

Add to `findings` (Alembic migration):

| Column | Type | Purpose |
|--------|------|---------|
| `resolution_miss_count` | int, default 0 | consecutive covered runs the finding was absent |
| `resolved_at` | timestamptz null | when auto/'manually' resolved |
| `resolution_method` | text null | `auto` \| `manual` |
| `resolution_run_id` | uuid null (FK detection_runs) | the run that closed it |
| `reopened_count` | int, default 0 | regression counter |
| `detected_db_version` | text null | `vuln_db_version` that first produced it (for the D4 DB-change guard) |

Add status value **`pending_remediation`** to `FindingStatus` (a soft state between `open` and `remediated`; excluded from the "current risk" count only once `remediated`). Auto-resolution never touches `accepted` or `fp`.

### 4.5 Edge cases (auto-resolution)

| Edge case | Handling |
|-----------|----------|
| Host entirely offline | Not in coverage → stays open, "asset not reached this run" |
| Scanner degraded/timed out on that service | `status != completed` → not covered → stays open |
| Service moved ports | Coverage keyed on `(asset, product)` → still matches, no false resolve |
| Vuln DB refreshed between runs | `detected_db_version` mismatch → "absent under new DB, not a fix" |
| Cached scanner result | Default: not counted as coverage (didn't re-observe); configurable |
| Low-confidence/AI-assisted suspected finding | Cheaper to be wrong → window can be 1; still coverage-gated |
| Critical/KEV finding | Window default 2 covered runs before auto-close |
| Manual `accepted`/`fp` | Never auto-touched; human state wins |
| Finding flaps (gone, back, gone) | Counter resets on every reappearance; flap count surfaced |
| Regression (resolved → seen again) | Auto-reopen + REGRESSION badge + reopened_count |
| Partial engagement (only some targets scanned) | Only findings whose asset/service were covered are eligible |

### 4.6 Dashboard surfacing

- Lifecycle timeline per finding: `first_seen → last_seen → pending_remediation → remediated` (or `reopened`).
- Resolution card: "Auto-resolved on run #42 (2026-08-11): asset 10.0.0.5:443 re-scanned clean, service confirmed reachable, same vuln-DB basis." One-click **Reopen**.
- Distinct badges: `Auto-resolved`, `Pending remediation`, `Regression`.

---

## 5. Capability 2 — Tiered verification (passive + active)

**Goal:** raise a finding from *inferred* to *actual*, with the lowest possible false-positive rate, without hammering the client network.

### 5.1 Tier P — Passive verification (default, offline, every finding)

Extends today's `verify()`. Adds an **agentic corroboration pass** (the LangGraph `corroborate` node, §6) that reasons over the *whole asset picture*, not just the single fact:

- Do independent scanners corroborate product/version? (multi-signal → higher tier)
- Is the port actually `open` vs `filtered`? (filtered → less certain, already modeled)
- Is there **authoritative package data** that patches this CVE? (→ suppress/contradict — already partly in `suppress_negated`)
- Compensating controls: `auth_enforced`, not `internet_facing`, WAF present? (→ lower exploitability confidence)
- Backport signal present? (→ downgrade — already modeled; the agent makes it explicit and explains it)

**Output:** `verification_state ∈ {confirmed, corroborated, inferred, contradicted}`, `verification_confidence`, `verification_evidence` (the audit bundle), `verification_method = passive`.
**Invariant:** passive verification can only **maintain or lower** confidence — never raise, never fabricate. (Same rule as `verifier.py`.)

### 5.2 Tier A — Active validation (escalated, opt-in, approval-gated)

**Trigger (all must hold):**
- Finding is **high/critical severity** OR **KEV-listed** OR **EPSS ≥ threshold**, AND
- `verification_state ∈ {inferred, corroborated}` (not already authoritative-confirmed, not contradicted), AND
- Engagement RoE has `active_validation_allowed = true` (new flag), AND
- Profile is not `ot` (OT stays structurally passive on both ends, per existing invariant).

**Mechanism:** the manager enqueues a **targeted, minimal validation `ScanJob`** back to the probe, scoped to exactly one `asset + port + check`:

- New `ScanJobType.validate` (or `params.mode="validate"` on `vuln_scan`).
- Probe runs a **safe, non-destructive validator** only:
  - protocol/TLS handshake + precise version read,
  - service banner re-grab,
  - **safe PoC** — e.g. a pinned Nuclei template *for that CVE* with an allowlist that excludes any `destructive`/`dos`/`intrusive`/write-capable template,
  - service-specific read-only checks.
- **Never** exploitation, writes, brute force, or DoS. ScopeGuard + RoE enforced on both ends (defense in depth, per existing invariant).

**Approval gate:** reuse `ExploitApprovalRequest` (it already links a finding + target and auto-queues on approval). Add a lighter `validation` reason/category. Support a **pre-authorized RoE window** so routine safe validation can auto-approve inside agreed bounds, while anything outside requires a human click.

**Outcome:**
- **Confirmed** (handshake/PoC proves it) → this is the **one** place a network-observed finding may be **promoted to `confirmed`**, with `exploit_validated`-style proof attached. `verification_method = active`.
- **Contradicted** (safe PoC fails though version matched) → strong **backport/false-positive** signal → downgrade to `contradicted` / likely-FP. *This is a powerful FP killer.*
- **Inconclusive** (timeout, unreachable, deception) → **do not** downgrade to resolved; keep suspected, note "validation inconclusive," optionally retry with backoff.

### 5.3 Edge cases (verification)

| Edge case | Handling |
|-----------|----------|
| Active check can't reach target | Inconclusive, not resolved; keep state, annotate |
| Backported fix (version matches, PoC fails) | → `contradicted`; big FP reduction |
| Honeypot/tarpit (deception score high) | Don't trust active result; mark deceptive |
| RoE forbids active checks | Passive-only; badge says "active validation not permitted" |
| OT profile | Structurally passive; never escalate |
| Rate/blast-radius | Validation jobs are per-finding, bounded, rate-limited, idempotent |
| LLM/agent unavailable | Passive tier still runs deterministically; escalation simply doesn't fire |
| Active result stale (asset changed since) | Re-tie result to the run that requested it; expire old approvals |

---

## 6. Capability 3 — LangGraph verification/triage subgraph

**Goal:** orchestrate the multi-step verification reasoning (and the async active-validation round-trip) as a bounded, auditable, human-in-the-loop state machine — **without letting an LLM become the source of truth.**

### 6.1 Why LangGraph (vs LangChain vs no-framework)

| Requirement | LangGraph | LangChain | Direct SDK (today) |
|-------------|-----------|-----------|--------------------|
| Durable **pause/resume** across the async active-validation round-trip | ✅ checkpointer + interrupts | ⚠️ manual | ⚠️ manual |
| **Conditional routing** (escalate or not) | ✅ native edges | ✅ | manual |
| **Human-in-the-loop** approval interrupt | ✅ first-class | ⚠️ | manual |
| **Deterministic replay / audit** of state | ✅ checkpoints | ⚠️ | manual |
| Keep LLM boxed (typed tools, no fabrication) | ✅ | ✅ | ✅ (already) |

The active-validation escalation is a **stateful, interruptible workflow** (reason → maybe request an external job → wait → interpret). That is precisely LangGraph's sweet spot; LangChain's chain abstractions don't give durable state-machine + interrupt semantics as cleanly. The existing direct-SDK agent stays fine for one-shot report/advice; we don't rip it out.

### 6.2 Graph shape

`manager/backend/app/ai/verification_graph.py` — a `StateGraph` invoked per suspected/high finding (or batched per asset) inside `run_detection_job`, best-effort:

```
intake ──▶ corroborate ──▶ decide_escalation ──┬──(no)──▶ finalize
                                               └──(yes)─▶ active_validation
                                                              │  (checkpoint + PAUSE
                                                              │   until job result / approval)
                                                              ▼
                                                        interpret_active ──▶ finalize
```

- **intake** — read-only tools load the finding, *all* asset facts, KEV/EPSS/CVSS, exposure context.
- **corroborate** — LLM emits a **typed** verdict (Pydantic): `action ∈ {maintain, lower, request_active, contradicted}` + reason + confidence delta. **Cannot** raise confidence or invent data.
- **decide_escalation** — deterministic conditional edge implementing §5.2 triggers.
- **active_validation** — a **single gated write tool** that creates a *pending* validation job/approval (never executes). Graph **checkpoints and pauses**; resumes when the result/approval arrives.
- **interpret_active** — read the proof, emit `confirm | contradict | inconclusive`.
- **finalize** — persist `verification_state`, confidence, evidence bundle; emit a **pending `AgentRecommendation`** (reusing the recommend-only pattern) — never a direct destructive mutation.

### 6.3 Non-negotiable invariants (the guardrails)

1. **Fail-closed / best-effort.** LangGraph or the LLM unavailable/erroring → the deterministic finding stands *exactly* as the pipeline produced it. Mirrors `ai_normalizer.py` / `agent.py`. No hard dependency.
2. **Read-only + one gated write.** The graph's only write is *create a pending validation job / pending recommendation*. It cannot mutate findings, launch exploits, or change scope.
3. **Typed + grounded.** Every LLM output is a constrained Pydantic schema; only tool-returned data may be cited (reuse `hallucination.py`). No invented CVEs, scores, or hosts.
4. **Can only lower or request — never fabricate-confirm.** The *only* path to `confirmed` for a network-observed finding is an **active positive control** (§5.2), not the model's say-so.
5. **Deterministic core is source of truth.** The pinned vuln DB + deterministic pipeline decide *what a finding is*; the graph decides *how sure we are* and *whether to actively check*.
6. **Fully audited.** Every graph run persists its checkpoints/state (reuse `llm_outputs`), so a reviewer can replay the reasoning.
7. **Model policy consistent with today.** `settings.llm_model` (latest Claude — Opus/Sonnet/Fable), no `temperature`, effort-capped, handle `stop_reason == "refusal"`.

### 6.4 Dependencies & placement

- Add `langgraph`, `langchain-core`, `langchain-anthropic` to **`requirements-extras.txt`** (optional, like `anthropic` today).
- Lives in `app/ai/` (needs async Postgres tools), wired as an optional stage in `engine_bridge.run_detection_job` *after* `create_findings_from_facts`.
- Off by default behind a settings flag (`verification_agent_enabled`), like AI-assist.

---

## 7. Cross-cutting — severity, criticality & risk rank

Most of the raw material exists (`FindingSeverity`, `risk_score` 0–1000, `AssetCriticality`, EPSS/KEV, posture scorecard). The enhancement is a **single, explainable Risk Rank** used for default ordering:

```
risk_rank = f( base_severity(CVSS),
               exploit_likelihood(EPSS, KEV),
               verified?(verification_state, exploit_validated),
               confidence,                       # de-rank low-confidence / contradicted
               asset_criticality,
               exposure(internet_facing, auth_enforced) )
```

- Findings that are **verified + exploitable + on a critical, internet-facing asset** float to the top; `contradicted` / low-confidence sink.
- Dashboard row = **severity chip + verification badge (`Confirmed-Active / Corroborated / Inferred / Contradicted`) + confidence + lifecycle state + risk rank.**
- Keep it explainable: every rank exposes its component contributions (consistent with the verifier's `checks{}` audit philosophy).

---

## 8. API / endpoint changes (sketch)

| Endpoint | Change |
|----------|--------|
| `POST /agents/{id}/jobs/{job_id}/result` | unchanged; still triggers `run_detection_job` |
| `GET /engagements/{id}/findings` | add `verification_state`, `confidence`, lifecycle fields, `risk_rank`; sortable by risk rank; filter by lifecycle/verification |
| `POST /findings/{id}/reopen` | manual reopen of an auto-resolved finding |
| `POST /findings/{id}/validate` | request active validation (creates gated approval) |
| `GET /engagements/{id}/detection-runs/{run}/coverage` | inspect coverage ledger (transparency for auto-resolution) |
| `POST /engagements/{id}/redetect` | re-run detection against a newer vuln-DB (already implied by `TRIGGER_MANUAL`) |
| RoE / engagement settings | add `active_validation_allowed`, confirmation-window overrides, `verification_agent_enabled` |

---

## 9. Consolidated edge-case & failure-mode register

| Domain | Failure/edge | Behavior |
|--------|--------------|----------|
| Coverage | Partial scan, host down, scanner degraded/skipped | Not covered → never auto-resolve |
| Coverage | Vuln DB changed between runs | DB-change guard → not a "fix" |
| Coverage | Service relocated ports | Keyed on `(asset, product)` → no false resolve |
| Resolution | Flapping finding | Counter resets each reappearance |
| Resolution | Regression (resolved → returns) | Auto-reopen + REGRESSION flag |
| Verification | Backport (version match, safe PoC fails) | `contradicted` / likely-FP |
| Verification | Honeypot/deception | Distrust results, mark deceptive |
| Verification | Active check inconclusive | Keep state; never resolve on inconclusive |
| Verification | RoE forbids / OT profile | Passive-only, no escalation |
| Agent | LLM/LangGraph down | Deterministic finding unchanged (fail-closed) |
| Agent | Model refusal on pentest content | Handled explicitly (like `agent.py`) |
| Agent | Attempted fabrication | Blocked by typed/grounded schema + `hallucination.py` |
| Concurrency | Two runs for one engagement | Detection already background + DB-transactional; resolution eval scoped per run |
| Idempotency | Re-delivered probe result | `dedup`/reaffirm already idempotent; validation jobs idempotent |
| Perf | Agent per finding is expensive | Only run for suspected/high; batch per asset; cache per (finding, evidence-hash) |

---

## 10. Testing & validation strategy

- **Golden fixtures (must-pass):** backport case (→ contradicted), honeypot case (→ distrust), **partial-scan case (must NOT auto-resolve)**, **DB-version-change case (must NOT auto-resolve)**, flap case, regression/reopen case, active-confirm case.
- **Precision/recall harness:** extend the existing `pipeline.ab_evaluate` (§ `pipeline.py:109`) to cover verification verdicts — every verification-gained certainty must be additive, never a silent precision regression.
- **LangGraph subgraph:** deterministic replay tests with a mocked LLM emitting constrained outputs; explicit **fail-closed test** (LLM down → finding byte-identical to deterministic output); grounding test (fabricated CVE rejected).
- **Auto-resolution:** coverage-gate tests, confirmation-window tests (N=1 and N=2), reopen/regression tests, DB-change-guard test.
- **Calibration:** track confidence vs. active-validation outcomes (Brier score) to tune thresholds over time.
- Keep the existing accuracy/precision-recall and dpkg cross-validation harnesses green (`ARCHITECTURE.md §8`).

---

## 11. Phased rollout (recommended build order)

The user listed verification → auto-resolve → LangGraph; **build order is deliberately different** — deliver the highest-value, lowest-risk, no-AI-dependency piece first.

| Phase | Deliverable | Depends on | Risk | Value |
|-------|-------------|------------|------|-------|
| **P0** | Coverage ledger (record only, no behavior change) | probe `scanner_runs` | none | enabler |
| **P1** | **Auto-resolution** (coverage-gated, confirm window, reopen, dashboard lifecycle) | P0 | low (deterministic) | **highest** |
| **P2** | **Passive verification** (LangGraph subgraph, passive nodes only) + verification badges | agent infra | low (fail-closed) | high |
| **P3** | **Active validation** (probe `validate` scan_type + gated approval + confirm/contradict) | P2, probe change, RoE | medium (touches client net) | high |
| **P4** | **Risk-rank unification** + calibration feedback loop | P1–P3 | low | medium |

Rationale: P1 is pure backend, deterministic, and immediately visible to customers (self-healing dashboard) with zero AI risk. P2 is additive and fail-closed. P3 is the most sensitive (packets on the client network, RoE) so it lands last, behind approvals.

---

## 12. Areas of improvement / future enhancements

- **Analyst feedback loop:** capture TP/FP labels → active-learning calibration of confidence thresholds and evidence weights.
- **Exposure/attack-path integration:** feed `ad/ graph/ exploit/` reachability into risk rank (a vuln behind five hops ranks below an internet-facing one).
- **EPSS/KEV time series:** a finding whose exploit-likelihood is *rising* should re-alert even if unchanged.
- **Multi-probe corroboration:** the same asset seen by two probes → higher evidence tier.
- **Vuln-DB-diff re-detection:** on snapshot refresh, auto-diff what newly matches / no longer matches, distinct from remediation.
- **SLA timers:** severity → remediation SLA countdown (the repo history hints a SLA cell was prototyped) — pairs naturally with lifecycle state.
- **Confidence calibration dashboard:** Brier/reliability plots from active-validation outcomes.
- **Suppression memory:** remember analyst-accepted FPs so identical inferences are pre-suppressed next run.

---

## 13. Open questions to revisit before/while building

1. **Confirmation window defaults** — is N=1 (low/med) / N=2 (critical/KEV) the right starting point, or should it be time-based (e.g., "absent for 7 days") instead of run-count-based?
2. **Cached scanner results** — count as coverage or not? (Default: not.)
3. **Active-validation auto-approve window** — how wide is the pre-authorized RoE band before a human must click?
4. **Agent batching granularity** — per finding vs per asset (cost vs. context richness).
5. **Where the subgraph lives** — `app/ai/` (chosen, needs async DB) vs a new `detection_engine/verification/` package (keeps engine cohesive but can't touch Postgres directly).
6. **Do we migrate the existing report/advisor agent to LangGraph too**, or keep the direct-SDK one and only add LangGraph for verification? (Plan assumes the latter.)

---

*End of plan. Nothing here is implemented yet; this document is the design contract for the work described in §11.*
