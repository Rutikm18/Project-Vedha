# ADR-0001: The manager's detection pipeline after facts arrive

**Status:** Proposed
**Date:** 2026-09-02
**Deciders:** Vedha platform owner
**Scope:** what happens between a probe submitting facts and a finding appearing in the UI

## Context

The probe is collection-only. Everything that turns evidence into a vulnerability
happens manager-side, along this path:

```
probe ──HTTP──▶ scan_results row (durable facts)
                      │
                      └─▶ outbox_events (topic=facts.ready, scan_result_id)   ← the handoff
                                │
              outbox worker ────┤  _claim_batch: 16 rows, FOR UPDATE SKIP LOCKED
                                │  asyncio.gather → handlers run CONCURRENTLY
                                ▼
                    _handle_facts_ready
                      ├─ re-read facts from scan_results (never from the event)
                      ├─ create_findings_from_facts
                      │    ├─ open a DetectionRun (leased)
                      │    ├─ detect_all_from_facts_traced  → CVE + posture tracks
                      │    └─ per finding: _find_open_duplicate → reaffirm | insert
                      └─ prioritize_engagement_findings(engagement)
                                ▼
                       findings ──▶ campaign-progress ──▶ UI
```

Several things about this are genuinely good and should be preserved. The event
carries only an id, so facts are re-read from the durable row rather than
duplicated into the queue. The queue is a table, so nothing is lost on restart.
`FOR UPDATE SKIP LOCKED` means multiple workers never claim the same event. Runs
carry a lease, so a crashed worker's run is reaped precisely instead of guessed at
by age. Retries back off exponentially and dead-letter rather than looping.

This ADR is about four places where the design does not hold up, found by reading
the path end to end.

## Findings

### R1 — Concurrent detection for one engagement can duplicate findings

**Severity: high (correctness, customer-visible).**

`run_worker` claims up to `BATCH_SIZE = 16` events and runs them through
`asyncio.gather`, each handler with its own session. Nothing prevents two
`facts.ready` events for the *same engagement* from landing in one batch — two
probes on one engagement, or a re-submission, is the normal case.

Dedup inside detection is a read-then-write:

```python
dup = await _find_open_duplicate(db, engagement_id, asset_id, title)   # plain SELECT
if dup is None:
    db.add(Finding(...))
```

There is **no unique constraint on findings** and no lock. Two concurrent handlers
both SELECT, neither sees the other's uncommitted INSERT, both insert. The result
is two rows for one issue — which then double-counts in open-finding totals, the
posture score, SLA tracking and the customer's report.

This is invisible in single-probe testing, which is why it has survived.

### R2 — A retry can open a second DetectionRun for one submission

**Severity: medium (correctness of campaign state).**

`_process` calls the handler, and only then `_mark_done` — in a **separate
transaction**. A crash in that window leaves the event `PROCESSING`; the reclaimer
requeues it; the handler runs again and opens a second `DetectionRun` for the same
`scan_result_id`.

Findings mostly absorb this (the second run reaffirms rather than duplicates), but
`campaign_progress` derives `evidence_covered` by mapping scan submissions to
completed runs, so run counts and coverage arithmetic are computed on a set that
now contains a phantom. The handler is not idempotent with respect to
`scan_result_id`, and it needs to be, because at-least-once delivery is the whole
point of an outbox.

### R3 — Every submission re-prioritises the entire engagement

**Severity: medium (scalability).**

`prioritize_engagement_findings(db, engagement_id)` recomputes `risk_score` for
every still-relevant finding in the engagement, and it runs on **every**
`facts.ready` event. A 10-probe campaign therefore does ten full passes over a
finding set that grows with the engagement — O(submissions × findings) where
O(submissions × touched) would do. It also runs inside the handler's transaction,
so it lengthens the window described in R2.

### R4 — The detection engine is reached by path manipulation, not as a dependency

**Severity: low (deployability).**

`engine_bridge._ensure_importable()` does `sys.path.insert(0, DETECTION_ENGINE_PATH)`
and then `import pipeline`. The detection engine is a sibling directory discovered
at runtime, not an installed package. It degrades gracefully when absent — which is
good — but it means the worker's most important dependency is not expressed
anywhere a deployment can verify, and `import pipeline` is a name collision waiting
to happen in a shared environment.

## Decision

Fix R1 and R2 now; schedule R3; record R4.

R1 and R2 are correctness issues that produce wrong numbers in front of a
customer, and both have small, local fixes. R3 is a cost that is invisible until
an engagement is large. R4 is a deployment smell, not a defect.

## Options considered for R1

### Option A — Partial unique index + `ON CONFLICT DO NOTHING`

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Correctness | Enforced by the database; cannot be bypassed |
| Concurrency cost | None — no serialisation |
| Risk | Existing duplicate rows must be reconciled before the index can be created |

**Pros:** the guarantee lives in the schema, so any future write path inherits it.
**Cons:** the dedup key `(engagement_id, asset_id, title)` is only unique *among
open statuses*, which needs a partial index; and `title` is a formatted string, so
the constraint is on a value the application composes.

### Option B — Per-engagement advisory lock around detection

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Correctness | Serialises the whole read-modify-write, so the race cannot occur |
| Concurrency cost | Detection for one engagement becomes serial (across engagements stays parallel) |
| Risk | A lock held across a long transaction; must be released on every path |

**Pros:** protects the entire dedup/regression/resolution sequence, not just the
INSERT — and that sequence has several read-then-write steps, not one.
**Cons:** gives up intra-engagement parallelism.

### Option C — Serialise at claim time (one in-flight event per engagement)

**Pros:** no lock, no schema change.
**Cons:** complicates `_claim_batch`'s single clean query, and starves an
engagement behind one slow event.

## Trade-off analysis

Option A only protects the single INSERT it constrains. The handler also does
regression reopening, resolution evaluation and reaffirmation — all read-then-write
against the same rows — so a unique index would convert *one* symptom into a
constraint violation while leaving the others racing.

Option B is chosen: it protects the whole critical section, matches how the code is
already structured (one handler = one logical unit of work per engagement), and
costs only intra-engagement parallelism, which is not where the throughput is —
concurrency across *engagements* is preserved, and that is the axis that scales.

Option A remains worth adding later as defence in depth once existing duplicates
are reconciled; the two are complementary, not alternatives.

## Consequences

**Easier:** finding counts, posture scores and SLA arithmetic become trustworthy
under multi-probe campaigns. Campaign coverage stops counting phantom runs.

**Harder:** detection for a single engagement is now serial, so one very slow
submission delays the next for that engagement. This is the intended trade.

**To revisit:** if a single engagement's detection ever becomes the bottleneck,
the lock granularity can move from engagement to `(engagement, asset)` — the same
mechanism, a narrower key.

## Action items

1. [x] **R1** — take a transaction-scoped advisory lock keyed on the engagement for
   the duration of `create_findings_from_facts`.
2. [x] **R2** — make `_handle_facts_ready` idempotent: skip a submission that
   already has a completed run.
3. [ ] **R3** — scope prioritisation to the findings a run touched, or debounce it
   per engagement, and move it outside the detection transaction.
4. [ ] **R4** — make `detection_engine` an installed package rather than a
   `sys.path` insert, so deployments can verify it.
5. [ ] Add a partial unique index on the open-finding dedup key once existing
   duplicates are reconciled (defence in depth behind the lock).
