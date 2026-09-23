# Scalable Aggressive Scanning — Verified Triage and Roadmap

> **For agentic workers:** this is a ROADMAP, not an executable plan. Each phase
> gets its own executable plan (superpowers:writing-plans) when it starts.
> Phase 0 is being executed on branch `fix/review-followups`.

**Input:** the research note "Scalable aggressive scanning for large authorized
subnets" (2026-09-23). That note reviewed commit `ad6d3ec` (2026-09-09). This
roadmap re-checks every claim against branch head `7f76678` and later, because
several subsystems changed in between.

**Goal:** an Aggressive request on a /24 or larger scope finishes. Coverage
must be reported truthfully and pacing must be enforceable. Partial evidence
must never close a finding.

## 1. The reported failure

Job `250e6892`: "254 host(s) x 65535 port(s) = 16,645,890 probes at 150 pps
needs at least 30.8h, against a 2.0h ceiling".

| Question | Answer (verified) |
|---|---|
| Why 150 pps, not the UI's 600? | Not deployment drift. Commit `13f1170`, which postdates `ad6d3ec`, made the launcher send `params.intensity` only (`manager/frontend/lib/scan-launch.ts`). The probe resolves `aggressive` → `deep` → preset rate 150 (`probe/workflow/intensity.py`). |
| Where is the error string? | `probe/agent/engine.py`, `_refuse_if_infeasible`, added after `ad6d3ec`. |
| Is the arithmetic right? | Yes. It is the admission floor for a monolithic full-range sweep. |
| Why does it refuse? | Admission priced all 65,535 ports on all 254 addresses. On `main` it ignores the two-phase design, in which everything downstream runs on the first pass. |
| Fixed on this branch? | Yes, for admission. Phased jobs are sized by the first pass (1,145 ports, ~32 min floor at 150 pps on a /24). The full-range tail is budgeted against the job's own deadline. Unreached ports are reported `not_scanned`, never `filtered`. |

## 2. Claim-by-claim status at branch head

Legend: **FIXED-BRANCH** = fixed on `fix/review-followups`; **OPEN** = still
true; **OUTDATED** = already addressed before this branch; **FALSE** = does
not hold as stated.

| # | Claim | Status | Evidence / where fixed |
|---|---|---|---|
| 1 | UI Aggressive couples pace and coverage (`aggressive → deep` = full range) | OPEN | Phase 2 (contract v2) |
| 2 | Rate/provenance drift explains 150 pps | FALSE | See §1. `engine_manifest` / `_runtime_manifest()` already rides every result |
| 3 | One outer `wait_for` owns the whole job | OPEN (mitigated) | The job-budgeted tail stops sending before the backstop (`_tail_deadline`) |
| 4 | Results are terminal-only; `attempt_id` unique blocks chunks | OUTDATED | Per-host result chunks + chunk buffer (migration 0041, `result_chunk_service.py`) |
| 5 | Site `max_rate_pps` never reaches the probe | OPEN | Stored/returned only (`probe_enrollment.py`). Phase 1 |
| 6 | `SendPacer` may climb to 4x the requested rate | FIXED-BRANCH (Wave D) | Ceiling = requested rate |
| 7 | Shared `SendPacer` unsynchronized across per-host threads | FIXED-BRANCH (Wave D) | Slot reserved under a lock |
| 8 | SYN AIMD treats every silent port as congestion; one filtered host throttles all | FIXED-BRANCH (Wave D) | AIMD is per host; the shared pacer is a fixed aggregate cap |
| 9 | Raw SYN emits no coverage record | FIXED-BRANCH (Wave D) | Per-host `scan_summary` from `ScanMetrics` on the raw path |
| 10 | Failed `sendto` becomes `filtered` | FIXED-BRANCH (Wave D) | Recorded as `error` / `local_resource_error` → health degraded |
| 11 | Coverage-gated auto-resolution is host-level; partial runs close findings | **OPEN → FIXED-BRANCH (Wave E)** | Auto-resolution is ARMED on `main`. A Stealth/Normal run after an Aggressive one could auto-close findings on unprobed ports. Wave E requires re-evaluation of the same rule/port or re-identification of the same product |
| 12 | Two-phase hosts: the manager keeps only the LAST `scan_summary` | FIXED-BRANCH (Wave D, R1b) | `ranges_from_facts` merges summaries |
| 13 | Partial work becomes a `completed` job | OPEN | The engine emits `outcome: partial` and `degraded`, but the manager maps job status to completed/failed only (`job_result_service.py`). Phase 1 |
| 14 | Cancellation does not stop raw packets | OPEN (deadline case mitigated) | Operator cancel / lease loss still leave the executor thread sending until its host budget ends. Phase 1 |
| 15 | Result authorization checks engagement scope, not assigned targets | OPEN | Phase 1 |
| 16 | `ipv6_discovery` label bypasses scope and reaches detection | FALSE as stated / LOW | Detection ingest never mints an Asset from run-scoped facts (`manager/detection_engine/ingest.py`), and no rule reads them. The target string is only stored in the raw result. Phase 1 hygiene: strip or validate it before persistence |
| 17 | Detection failure is acknowledged as done | OPEN (confirmed) | `create_findings_from_facts` catches `Exception`, marks the run failed and returns, so the outbox marks the event done. Phase 1 |
| 18 | Job/attempt lock order inconsistent; cancel not CAS | UNVERIFIED here | The earlier SELECT…FOR UPDATE question is still a user decision. Needs a deadlock analysis |
| 19 | Outbox claim not renewable/fenced | KNOWN (ADR-0002 D4) | Phase 1 |
| 20 | Connect fallback: memory/FD amplification at width | PARTLY OUTDATED | 47 → 4.3 MB/host, two-phase ports, bounded fan-out (earlier work). Re-measure at /24 x full |
| 21 | Launch not idempotent; count-then-insert cap | OPEN | Phase 3 |
| 22 | "Campaign" progress reads engagement-wide history | OPEN | Phase 3 |

## 3. Phase 0 — make Aggressive safe to run today (this branch)

| Wave | What | State |
|---|---|---|
| Task 15 | Admission sized by first pass for phased jobs | done, reviewed |
| A | Job-budgeted tail (one shared scanner, per-call host budget, estimate scope) | done; review found #9 → Wave D |
| B | Manager lease guard on push + poll claim (one job per probe) | done, reviewed |
| D | Raw SYN: coverage summary, honest attempts, hard-cap thread-safe aggregate pacer, host-local AIMD, summary merge | in progress |
| E | Dimensional auto-resolution (claim #11) | queued after D |
| C | CI/test hygiene (timeouts, triggers, wiring, reconnect-test determinism, small comment fixes) | queued |

**Exit criteria:**
- An Aggressive /24 is admitted and completes inside 2 h.
- Every host carries a merged coverage map (first pass + tail, `not_scanned` explicit).
- The raw-SYN aggregate never exceeds the requested rate.
- No finding accrues a clean miss unless its own check was re-evaluated.

## 4. Phase 1 — outcome, authority, and stop semantics (small tasks)

1. **Typed job outcome.** Add `ScanJobStatus.partial` (or a `coverage_verdict` column, whichever the UI can adopt with fewer changes). Map the result's `outcome` onto it. Test: a budget-exhausted tail yields `partial` with explicit missing counts. It never yields plain `completed`.
2. **Hard site cap.** Apply `site.max_rate_pps` at probe startup, and clamp every job with `effective_rate = min(job rate, site cap)`. Test: a job requesting above the cap runs at the cap. The `SendPacer` ceiling equals the effective rate.
3. **Cooperative stop for raw SYN.** Give `_syn_scan_blocking` a stop token (a threading.Event), checked at the same send-window boundary as the host budget. Wire it to job cancellation and lease loss. Test: after `stop.set()`, no further `sendto` calls.
4. **Assigned-target validation.** At ingest, reject facts whose target is outside the job's resolved target list, not merely outside the engagement scope. Test: an in-scope but unassigned IP returns 422 with the path.
5. **Run-scoped facts carry no host.** Validate or strip `target` on `ipv6_discovery` facts before persistence. Test: an out-of-scope literal is not stored.
6. **Detection failure is retried.** Commit the failed `DetectionRun` in its own transaction, then raise, so the outbox backs off and retries. Test: a transient exception is retried and a poison event dead-letters at `max_attempts`.

## 5. Phase 2 — scan contract v2: separate coverage from pace

1. Add a request field `coverage: quick|standard|full`, independent of `intensity` (pace).
2. The probe resolves the port set from `coverage` and the envelope from `intensity`, and pins both in `run_stats.applied_tuning`.
3. The UI gets two controls. Aggressive = pace only. Full range = an explicit coverage choice with its own time estimate.
4. Legacy `intensity=aggressive` with no `coverage` keeps today's meaning and logs a deprecation (never silently remapped).
5. Tests: every translation pinned. Explicit tuning survives UI → manager → probe serialization.

## 6. Phase 3 — campaign sharding (the note's §3)

1. A `scan_campaign` parent row plus `campaign_id`, `shard_ordinal` and `plan_digest` on child jobs.
2. Discovery runs as its own job and persists a manifest of responsive, silent and excluded hosts.
3. A pure planner: `hosts_per_shard = floor(deadline x conservative_pps x 0.70 / (ports x attempts))`. It proves union, disjointness and scope inclusion in tests.
4. The coordinator enqueues shards in waves, retries only failed shards, and finalizes with a lock + CAS.
5. Campaign-scoped progress and an idempotent launch (a unique key with a request hash).

## 7. Phase 4 — calibrated capacity

Record the effective pps (p10/p50/p95) per probe, scan method and site from
`run_stats`, and size shards from p10. Multi-probe distribution gets disjoint
shards under one site budget.

## 8. Operating guidance until Phase 2

- Broad /24: **Normal**. With this branch deployed, Aggressive also runs. Its
  first pass is a high-signal set of about the same size as Normal's (1,145 vs
  1,175 ports on the `it` profile), and its tail covers as much of the full
  range as the budget allows, reported as `not_scanned` beyond that.
- Exhaustive full-range assurance on specific hosts: Aggressive on a small
  target list. At 150 pps and 3 attempts, about 3 hosts fit in a 2 h job in
  the worst case.
- Do not raise the 2 h ceiling or the pps to make the arithmetic fit.
