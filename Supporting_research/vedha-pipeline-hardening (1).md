# Vedha VA Pipeline — Core-Level Hardening Plan

**Date:** 2026-08-30
**Scope:** closing the `"still not satisfied"` open item from the 2026-08-30 work log
**Status of this document:** design verified against a runnable reference implementation (75,000 randomised states, 34 unit tests, 6/6 mutation kills). Not yet applied to the real repo.

---

## Preface — what is and isn't verified here

I did not have your repository, so nothing in this document has been executed against
`manager/backend` or `frontend`. Claiming otherwise would be worthless to you.

What I did instead: built a zero-dependency executable model of your pipeline with the
same lifecycle, the same transactional-outbox delivery, and the same detection-run state
machine, then attacked it until it stopped breaking. Every mechanism proposed below is
implemented and tested there. The code in this document is the translation of those
verified mechanisms into your stack.

Verification actually performed on the reference model:

| Activity | Result |
|---|---|
| Unit suite | 34 tests, all passing |
| Randomised state-space fuzz | 1,500 trials × 50 steps = **75,000 states, 0 invariant violations** |
| Phases reached during fuzzing | 8/8 (none unreachable) |
| Mutation testing | **6/6 injected bugs killed** |
| Bugs found in my own test suite by mutation testing | 1 (documented in §7.4) |

Two things I could not verify and have marked accordingly:

1. The middle rows of CISA BOD 26-04 Appendix A Table 1. The CISA page blocks
   automated fetching. I sourced the corner rows and marked the interpolated middle
   explicitly in code, with a property test that will catch a transcription error when
   you enter the real table.
2. Your actual fact payload shapes. The corpus in the reference implementation is
   shaped like your log's examples (`smb.data.smbv1_enabled`, `negotiated_dialect`)
   but is not your real data. §3 is the mechanism for replacing my guesses with your
   captured payloads.

---

## Part 0 — Diagnosis: why you're still not satisfied

Your last two passes were both correct and both insufficient, for the same underlying
reason.

The `done` vs `completed` fix repaired one comparison. The raw-facts endpoint gave you a
way to look at evidence by hand. Both are point fixes. Neither changed the property that
produced the bug and will produce the next one:

> **The pipeline cannot distinguish "we checked and found nothing" from "we never
> actually checked."**

Every failure mode in this system converges on the same observable: an empty findings
list. Consider three situations:

1. The host is genuinely not vulnerable.
2. The host **is** vulnerable, but the fact key the rule reads moved between agent
   builds, so the rule silently never fired.
3. Detection never ran at all because the outbox worker is down.

Today all three render as the same thing in the portal. Case 1 is good news. Case 2 is a
false negative in a security product, which is the worst possible failure. Case 3 is an
outage. Your log even names the operational half of this — *"OPERATIONAL GOTCHA: the
outbox worker MUST be running"* — and then documents it rather than making the system
detect it.

That gap is the thing you keep feeling and can't name. It is also exactly what
`"the scripts catch it but the manager doesn't"` means: the probe collected the
evidence, the evidence sits in `scan_results`, and the manager produced no finding — with
no record anywhere of *why*.

The raw-facts endpoint helps you check this **manually, one vuln at a time, if you already
suspect a problem**. That doesn't scale and it doesn't alert. A customer will not read
raw JSON to discover you missed their SMBv1 host.

**The fix is to make non-findings explain themselves.** Everything below follows from
that single change.

Here is the reference implementation's output for those three cases after the change:

```
### Host is genuinely not vulnerable
  phase        : complete             is_complete=True
  findings     : 0    blind_rules=0
  verdict      : evaluated_clean

### Host IS vulnerable, but the fact key moved (schema drift)
  phase        : complete_with_gaps   is_complete=True
  findings     : 0    blind_rules=2
  verdict      : schema_drift
  reason       : required fact path absent: smb.data.smbv1_enabled
  banner       : 2 rule(s) could not be assessed: the scanner submitted facts but
                 the fields those rules read were absent or unusable

### Detection never ran - outbox worker is down
  phase        : stalled              is_complete=False
  findings     : 0    blind_rules=0
  verdict      : detection_never_ran
  banner       : detection queue is not draining: outbox worker has not reported in
```

---

## Part 1 — Fault model

Before writing code, enumerate every way a collected fact fails to become a finding. You
cannot claim a pipeline is correct until each row here is either impossible or visible.

| # | Failure | Where | Symptom today | Detected by |
|---|---|---|---|---|
| F1 | Job result saved, outbox event lost | ingest | stuck `aggregating` | single-txn ingest (§2.4) |
| F2 | Outbox worker not running | ops | stuck `aggregating` forever | heartbeat + lag → `stalled` (§2.3) |
| F3 | Worker alive but wedged on a poison event | worker | queue depth grows silently | lease + backoff + dead-letter (§2.3) |
| F4 | Worker dies mid-detection | worker | run stuck at `running` | lease reaper (§2.3) |
| F5 | Redelivery duplicates findings | worker | inflated counts | `dedupe_key` UNIQUE (§2.4) |
| F6 | Redelivery resets finding identity | worker | **triage state silently lost** | identity-stability test (§7.4) |
| F7 | Rule reads a fact path the probe no longer emits | detection | **silent false-clean** | `MISSING_INPUT` trace (§2.1) |
| F8 | Fact present but wrong type | detection | silent false-clean | `UNPARSEABLE` trace (§2.1) |
| F9 | One rule raises, killing the batch | detection | partial silent loss | per-rule isolation (§2.1) |
| F10 | Scanner never ran for that check | scheduling | looks clean | `NO_EVIDENCE` trace (§2.1) |
| F11 | Run completes without covering all evidence | orchestration | premature `complete` | coverage set (§2.2) |
| F12 | `complete` computed from one run in a multi-job campaign | progress | premature `complete` | coverage set (§2.2) |
| F13 | Status constant mismatch | progress | never completes | typed enum + `ALL_RUN_STATES` (§2.2) |
| F14 | Finding created but filtered out downstream | prioritization | invisible finding | trace vs portal reconciliation (§9) |

F7 is the one that should worry you most. It produces a confident wrong answer, it leaves
no trace, and no unit test of the rule will catch it — because **the rule is correct**.
It's the wiring between probe and rule that broke. That is why §3 exists.

---

## Part 2 — The four core mechanisms

### 2.1 Detection trace — make every non-finding explain itself

This is the centrepiece. Every rule evaluation writes one row recording its outcome,
whether or not it produced a finding.

```python
# app/models/detection_trace.py

OUTCOME_MATCH         = "match"          # fired -> finding
OUTCOME_NO_MATCH      = "no_match"       # evaluated, predicate false -> genuinely clean
OUTCOME_NO_EVIDENCE   = "no_evidence"    # scanner never submitted for this engagement
OUTCOME_MISSING_INPUT = "missing_input"  # facts present, declared path absent -> DRIFT
OUTCOME_UNPARSEABLE   = "unparseable"    # path present, value the wrong shape
OUTCOME_ERROR         = "error"          # rule raised

# Scanner ran but the rule still couldn't be assessed. These are DEFECTS and must
# degrade the campaign verdict.
BLIND_OUTCOMES = frozenset({OUTCOME_MISSING_INPUT, OUTCOME_UNPARSEABLE, OUTCOME_ERROR})

# Scanner was never run. A scope fact, reported but not a defect.
UNASSESSED_OUTCOMES = frozenset({OUTCOME_NO_EVIDENCE})


class DetectionTrace(Base):
    __tablename__ = "detection_trace"

    id             = Column(BigInteger, primary_key=True)
    run_id         = Column(UUID(as_uuid=True), ForeignKey("detection_runs.id"),
                            nullable=False, index=True)
    engagement_id  = Column(UUID(as_uuid=True), nullable=False)
    scan_result_id = Column(UUID(as_uuid=True), ForeignKey("scan_results.id"),
                            nullable=True)          # null for NO_EVIDENCE
    scanner        = Column(String(64), nullable=False)
    rule_id        = Column(String(64), nullable=False)
    outcome        = Column(String(24), nullable=False)
    reason         = Column(Text, nullable=True)
    created_at     = Column(DateTime(timezone=True), nullable=False,
                            server_default=func.now())

    __table_args__ = (
        Index("ix_trace_engagement_rule", "engagement_id", "rule_id"),
        Index("ix_trace_blind", "engagement_id", "outcome"),
        CheckConstraint(
            "outcome IN ('match','no_match','no_evidence','missing_input',"
            "'unparseable','error')", name="ck_trace_outcome"),
    )
```

The distinction that makes this work is between *absent* and *null*. A collected value of
`null` is real data. A missing key is a broken contract. Conflating them is how drift
hides:

```python
_MISSING = object()

def get_path(doc, dotted: str):
    """Resolve `a.b.c`. Returns _MISSING (never None) when the key is absent."""
    cur = doc
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return _MISSING
    return cur
```

Each rule then declares the fact paths it consumes. That declaration is a machine-checkable
contract between the probe's emitters and the manager's rules:

```python
@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    scanner: str
    requires: tuple[str, ...]          # the contract
    predicate: Callable[[dict], bool]
    severity: str
    cve_id: str | None = None
    technical_impact: str = "partial"  # 'partial' | 'total'   (SSVC input)
    automatable: bool = False          # (SSVC input)


def evaluate(rule: Rule, facts: dict) -> TraceRow:
    """Evaluate one rule against one fact document. Never raises."""
    for path in rule.requires:
        if get_path(facts, path) is _MISSING:
            return TraceRow(rule, OUTCOME_MISSING_INPUT,
                            f"required fact path absent: {path}")
    try:
        hit = rule.predicate(facts)
    except (TypeError, ValueError) as exc:
        return TraceRow(rule, OUTCOME_UNPARSEABLE, str(exc))
    except Exception as exc:                     # a rule bug must not kill the batch
        return TraceRow(rule, OUTCOME_ERROR, f"{type(exc).__name__}: {exc}")
    return TraceRow(rule, OUTCOME_MATCH if hit else OUTCOME_NO_MATCH)
```

Three properties matter and all three are enforced by tests:

- **`evaluate` never raises.** One malformed rule cannot blind a whole submission (F9).
- **`MISSING_INPUT` is never reported as `NO_MATCH`.** Absence is never rendered as
  cleanliness (F7). This is verified structurally by fuzz invariant I10 below.
- **`NO_EVIDENCE` is judged at engagement scope, not per batch.** Each outbox event
  carries one `ScanResult`, so per-batch scoping would flag every other scanner on every
  event. This was a real bug I hit in the reference implementation and fixed.

#### The verdict function

Roll the trace up into a single answer per rule:

```python
VERDICT_FINDING_EXISTS  = "finding_exists"
VERDICT_EVALUATED_CLEAN = "evaluated_clean"
VERDICT_SCHEMA_DRIFT    = "schema_drift"
VERDICT_NO_EVIDENCE     = "no_evidence_collected"
VERDICT_RULE_ERROR      = "rule_error"
VERDICT_NOT_RUN         = "detection_never_ran"
```

`explain(engagement_id, rule_id)` returns one of these plus the reason strings. This is
the direct, machine-readable answer to *"the scripts catch it but the manager doesn't"*.

A test asserts every verdict is reachable from some real scenario. A verdict nobody can
reach is dead code pretending to be diagnostics.

### 2.2 Reconciled progress — derive from evidence, not from one nullable row

The original bug was structural, not typographical. `campaign_progress` inferred the whole
pipeline state from a single nullable `run`, so `run is None` had to mean three different
things at once: facts not published, event published but unconsumed, or detection crashed
before creating the row. Unrepresentable states produce exactly this class of bug.

Replace inference with reconciliation against the evidence ledger:

```python
def compute_progress(db, engagement_id, *, now=None,
                     worker_stale_after=90, queue_stall_after=120):
    now = now or utcnow()

    jobs_total, jobs_done = _job_counts(db, engagement_id)
    sr_ids                = _scan_result_ids(db, engagement_id)
    queue_pending, queue_dead, oldest = _queue_state(db, engagement_id)
    lag                   = (now - oldest).total_seconds() if oldest else 0.0
    runs                  = _runs(db, engagement_id)

    # A run holds a lease. An unexpired lease is a MORE specific liveness signal
    # than the global worker heartbeat: it means a worker is actively holding
    # this exact work. An expired lease is a dead worker's orphan.
    runs_running_live = sum(
        1 for r in runs
        if r.status == RUN_RUNNING and r.lease_expires_at and r.lease_expires_at > now)
    runs_failed = sum(1 for r in runs if r.status == RUN_FAILED)

    # Completion is proven by coverage, not asserted by a status column.
    covered = set()
    for r in runs:
        if r.status == RUN_COMPLETED:
            covered |= set(r.covered_scan_result_ids)
    covered &= sr_ids

    blind      = _distinct_rules_with(db, engagement_id, BLIND_OUTCOMES)
    unassessed = _distinct_rules_with(db, engagement_id, UNASSESSED_OUTCOMES)
    worker_alive = _heartbeat_age(db) <= worker_stale_after

    scanning_done    = jobs_total > 0 and jobs_done == jobs_total
    evidence_covered = bool(sr_ids) and covered == sr_ids

    # Precedence order is load-bearing. It is the outcome of the reference
    # implementation's fuzz run, not a guess.
    if jobs_total == 0:
        phase = PHASE_PENDING
    elif queue_dead:
        phase = PHASE_ERROR
    elif runs_running_live:
        phase = PHASE_DETECTING
    elif runs_failed and not queue_pending and not evidence_covered:
        phase = PHASE_ERROR
    elif queue_pending and (lag > queue_stall_after or not worker_alive):
        phase = PHASE_STALLED
    elif not scanning_done:
        phase = PHASE_SCANNING
    elif queue_pending:
        phase = PHASE_QUEUED
    elif evidence_covered:
        phase = PHASE_COMPLETE_WITH_GAPS if blind else PHASE_COMPLETE
    else:
        phase = PHASE_QUEUED

    is_complete = phase in (PHASE_COMPLETE, PHASE_COMPLETE_WITH_GAPS)
```

Three deliberate changes from your current version:

**`complete_with_gaps` is a new terminal phase.** A campaign that finished but couldn't
assess some rules is not the same as a clean one. This is what makes F7 visible in
aggregate rather than only under manual inspection.

**`stalled` is a new phase.** Distinguishes "working" from "wedged". A queue that isn't
draining is an operational fact the system should state, not one the operator should have
to infer from a spinner that never stops.

**Completion is proven by coverage.** `covered == sr_ids` means every submission was
consumed by a run that reached `completed`. This is what makes multi-job campaigns correct
(F12) — your current single-`run` check is wrong the moment a campaign has two agents.

On the constant that started this: don't fix the literal, make the wrong literal
impossible.

```python
RUN_RUNNING, RUN_COMPLETED, RUN_FAILED = "running", "completed", "failed"
ALL_RUN_STATES = frozenset({RUN_RUNNING, RUN_COMPLETED, RUN_FAILED})
TERMINAL_RUN_STATES = frozenset({RUN_COMPLETED, RUN_FAILED})
```

with a DB-level `CheckConstraint` and a regression test asserting
`"done" not in ALL_RUN_STATES`. Better still, use a `str, Enum` so a typo is a
`NameError` at import rather than a `False` at runtime.

### 2.3 Outbox worker — liveness, leases, bounded retry

Your log says the worker "MUST be running." Any invariant maintained only by human
discipline is an invariant that will be violated. Make the system observe it.

Three additions:

**Heartbeat.** The worker writes `worker_heartbeat(worker, last_beat_at)` every tick.
`campaign_progress` reads it. No heartbeat within `worker_stale_after` plus a non-empty
queue means `stalled`, with a specific banner instead of a spinner.

**Leases.** Claim events with an expiry, not a boolean flag:

```python
def claim(self, now, batch):
    with self.db.begin():                       # SELECT ... FOR UPDATE SKIP LOCKED
        rows = self.db.execute(
            select(Outbox)
            .where(Outbox.state == OUTBOX_PENDING, Outbox.available_at <= now)
            .order_by(Outbox.id).limit(batch)
            .with_for_update(skip_locked=True)  # safe for N workers
        ).scalars().all()
        for r in rows:
            r.state, r.locked_by = OUTBOX_INFLIGHT, self.name
            r.lease_expires_at = now + timedelta(seconds=self.lease_seconds)
            r.attempts += 1
    return rows
```

`SKIP LOCKED` is what lets you run more than one worker without double-processing. Since
you are already on Postgres for JSONB, use it.

**Bounded retry with dead-letter.** Exponential backoff, then a terminal `dead` state that
surfaces as `PHASE_ERROR`. An event that fails forever must stop being invisible.

```python
except Exception as exc:
    if row.attempts >= self.max_attempts:
        row.state, row.last_error = OUTBOX_DEAD, f"{type(exc).__name__}: {exc}"
    else:
        row.state = OUTBOX_PENDING
        row.available_at = now + timedelta(seconds=min(2 ** row.attempts, 300))
```

**Reaper.** `DetectionRun` also carries a lease. A run whose lease expired belongs to a
worker that died:

```python
def reap_stale_runs(db, now):
    return db.execute(
        update(DetectionRun)
        .where(DetectionRun.status == RUN_RUNNING,
               DetectionRun.lease_expires_at.isnot(None),
               DetectionRun.lease_expires_at < now)
        .values(status=RUN_FAILED, error="lease expired; worker presumed dead",
                finished_at=now)
    ).rowcount
```

Without this, a worker killed mid-detection leaves the campaign at `detecting` forever.
Mutation testing confirmed the reaper is load-bearing: removing it is caught immediately.

### 2.4 Idempotent findings — at-least-once delivery done properly

A transactional outbox gives at-least-once delivery. Redelivery is normal, not
exceptional, so `create_findings_from_facts` must be idempotent by construction.

```python
def dedupe_key(engagement_id, asset, rule_id, evidence) -> str:
    return hashlib.sha256(
        "|".join([str(engagement_id), asset, rule_id, fingerprint(evidence)]).encode()
    ).hexdigest()
```

with `UNIQUE(dedupe_key)` and an insert that **ignores** rather than replaces:

```python
stmt = insert(Finding).values(...).on_conflict_do_nothing(index_elements=["dedupe_key"])
```

`on_conflict_do_nothing`, not `on_conflict_do_update`. This distinction is not
cosmetic, and it is the one my own test suite initially missed — see §7.4.

Ingest must remain a single transaction:

```python
def process_job_result(db, *, engagement_id, job_id, agent_id, scanner, facts):
    with db.begin():                                    # ONE transaction
        sr = ScanResult(engagement_id=engagement_id, job_id=job_id, agent_id=agent_id,
                        scanner=scanner, facts=facts, fingerprint=fingerprint(facts))
        db.add(sr)
        db.flush()
        db.add(Outbox(topic=TOPIC_FACTS_READY, engagement_id=engagement_id,
                      payload={"scan_result_id": str(sr.id)}, state=OUTBOX_PENDING,
                      available_at=utcnow()))
```

Split this and you get either lost detections or phantom events, both silent (F1).

---

## Part 3 — The fact contract: catch drift in CI, not in production

§2.1 makes drift *visible after a scan*. This makes it *impossible to ship*.

Every rule declares `requires`. Capture a corpus of real probe submissions. Assert in CI
that every declared path is actually emitted by something:

```python
# manager/backend/tests/test_fact_contract.py
CORPUS = Path("tests/fixtures/probe_corpus")   # captured verbatim from real agents

def test_every_rule_input_is_emitted_by_some_scanner():
    emitted = set()
    for f in CORPUS.glob("*.json"):
        emitted |= collect_emitted_paths(json.loads(f.read_text()))

    required = {p for r in ALL_RULES for p in r.requires}
    unsatisfied = sorted(required - emitted)

    assert not unsatisfied, (
        "These rules read fact paths no scanner emits. They can never fire:\n  "
        + "\n  ".join(unsatisfied))
```

This is the highest-leverage test in the whole plan, because it catches the failure that
no other test can. A rule reading a path nothing emits is a **rule that is individually
correct and globally useless**. Unit-testing the rule passes. Testing the scanner passes.
Only comparing them catches it.

The reverse direction is also worth reporting, at warning level rather than as a failure:
`emitted - required` is evidence the probe collects that no rule consumes. That's your
backlog of detections you could be writing from data you already have.

**Building the corpus.** You already have the exact tool for this — the `raw-facts`
endpoint from prompt 2. Point it at a real engagement, save each `facts` blob verbatim
into `tests/fixtures/probe_corpus/`, redact hostnames and banners. That reframes the
raw-facts work from a debugging convenience into the input to a permanent regression gate,
which I think is its real value.

---

## Part 4 — API surface

### `GET /engagements/{id}/campaign-progress` (extended)

```jsonc
{
  "phase": "complete_with_gaps",
  "is_complete": true,
  "jobs":      { "total": 2, "done": 2 },
  "evidence":  { "submissions": 7, "covered": 7 },
  "queue":     { "pending": 0, "dead": 0, "lag_seconds": 0.0, "worker_alive": true },
  "detection": { "running": 0, "running_live": 0, "failed": 0, "done": true },
  "coverage":  { "rules_total": 24, "rules_assessed": 22,
                 "rules_blind": 2, "rules_unassessed": 0 },
  "findings": 5,
  "reasons": [
    "2 rule(s) could not be assessed: the scanner submitted facts but the fields those rules read were absent or unusable"
  ]
}
```

Keep `is_complete` — your frontend already keys off it, and the contract still holds.

### `GET /engagements/{id}/coverage` (new)

Per-rule verdicts plus the assessed/blind split. This is the campaign-level answer to
"what did we actually check?"

### `GET /engagements/{id}/detection-explain?rule_id=SMB-001` (new)

```jsonc
{
  "rule_id": "SMB-001",
  "title": "SMBv1 enabled",
  "scanner": "smb_scan",
  "requires": ["smb.data.smbv1_enabled"],
  "findings": 0,
  "outcomes": { "missing_input": 3 },
  "reasons": ["required fact path absent: smb.data.smbv1_enabled"],
  "verdict": "schema_drift"
}
```

**Authorization.** Same gate as `raw-facts`: `require_role(["admin","manager","tester"])`,
tenant-scoped via `get_or_404`. Reasons quote fact paths and error text, which can leak
banner and hostname detail. Treat these as operator endpoints and keep them out of the
client role, consistent with your existing `_REDACT` policy.

---

## Part 5 — Frontend

Two changes in `CampaignProgress.tsx`, plus one new component.

**Stop polling forever.** Back off, and stop on terminal phases:

```tsx
const TERMINAL = new Set(["complete", "complete_with_gaps", "error"]);

useEffect(() => {
  if (!progress) return;
  if (TERMINAL.has(progress.phase)) return;           // never poll a settled campaign

  // 4s while things are moving; back off to 30s once stalled, so a dead worker
  // doesn't generate a request every 4 seconds indefinitely.
  const delay = progress.phase === "stalled" ? 30_000 : 4_000;
  const t = setTimeout(refetch, delay);
  return () => clearTimeout(t);
}, [progress, refetch]);
```

**Fix the empty state.** The current message — *"clean against current rules"* — is the
single most dangerous string in the product, because it asserts a security conclusion the
backend has not established. Make it state what actually happened:

```tsx
function FindingsEmptyState({ progress }: { progress: Progress }) {
  if (progress.phase === "stalled")
    return <Notice tone="warning" title="Detection hasn't started">
      {progress.reasons[0]}
      <Button onClick={retryDetection}>Retry detection</Button>
    </Notice>;

  if (progress.phase === "error")
    return <Notice tone="error" title="Detection failed">{progress.reasons[0]}</Notice>;

  if (progress.coverage.rules_blind > 0)
    return <Notice tone="warning" title="No findings, but the scan was incomplete">
      {progress.coverage.rules_blind} of {progress.coverage.rules_total} checks
      couldn't run against the data the scanner returned. Treat this as unknown,
      not clean.
      <Link href={`/campaign/${id}/coverage`}>See which checks were skipped</Link>
    </Notice>;

  if (!progress.is_complete)
    return <Notice tone="info" title="Detection in progress" />;

  return <Notice tone="success" title="No findings">
    All {progress.coverage.rules_assessed} checks ran against this data and none matched.
  </Notice>;
}
```

The wording matters as much as the logic. "No findings, but the scan was incomplete —
treat this as unknown, not clean" tells an operator what happened and what to do. "Clean
against current rules" tells them something that may be false.

**New: `<CoveragePanel />`.** Sits next to `<RawFacts />`. Lists blind rules with the
missing path and a link into `raw-facts` filtered to the relevant scanner, so the
question "did the probe even send this?" is one click, not a manual hunt.

That gives you the full diagnostic chain in the UI:
**finding missing → which rule → why → the raw evidence.**

---

## Part 6 — Prioritization: the ground moved under you

Worth flagging because it postdates your work log and changes the design of this layer.

**CISA BOD 26-04** was issued 2026-06-10 and supersedes and revokes both BOD 19-02 and BOD 22-01. It ends flat one-size-fits-all patch deadlines and drops the requirement to use CVSS as the prioritization mechanism. Remediation urgency is now set by four binary variables evaluated per vulnerability, per asset: whether the asset is publicly exposed, whether the CVE is on the KEV catalog, and whether an adversary can automate all the steps necessary to exploit it — plus technical impact. Appendix A Table 1 maps all 16 combinations to five tiers, running 3, 14 or 60 calendar days, with the lowest-risk cases deferred to the next scheduled major upgrade or rebuild.

CISA's Vulnrichment Program supplies KEV status, automatability and technical impact; asset exposure is determined by the agency, from its own asset or scanner data.

This matters to you specifically for a reason that's easy to miss: **three of the four
variables come from public feeds, and the fourth is exactly what your probe already
collects.** Your port-scan reachability data *is* the asset-exposure signal. You are one
join away from a prioritization model that matches the current federal directive, which is
a real differentiator for a VA product.

The other two inputs sit naturally on the `Rule`, since `technical_impact` and
`automatable` are properties of the vulnerability:

```python
def bod_2604_tier(*, exposed: bool, kev: bool, automatable: bool,
                  total_impact: bool) -> str:
    if kev and total_impact:
        return TIER_3D_TRIAGE   # SOURCED: KEV + total control, regardless of the rest
    if exposed and automatable and total_impact:
        return TIER_3D          # SOURCED: exposed + automatable + total, non-KEV
    # ---- INFERRED middle rows: monotone interpolation, NOT directive text ----------
    if kev or (exposed and (automatable or total_impact)):
        return TIER_14D
    if exposed or automatable or total_impact:
        return TIER_60D
    # --------------------------------------------------------------------------------
    return TIER_NEXT_UPGRADE    # SOURCED: not exposed, not KEV, not automatable
```

**Transcribe the real 16 rows from the directive before making any compliance claim.**
I could source the corners but not the middle, and I've marked that in the code rather
than letting an inference pass as directive text. Keep it as a data table, not branching
logic, so verifying it is a reading task rather than a code review.

The test I'd keep regardless of the exact table is the property one, because it holds
however the rows are transcribed and will catch a data-entry error:

```python
def test_tier_table_is_monotone_in_every_risk_variable():
    """Turning a risk variable OFF must never produce a STRICTER deadline."""
    for bits in range(16):
        base = {n: bool(bits >> i & 1) for i, n in enumerate(NAMES)}
        base_rank = RANK[bod_2604_tier(**base)]
        for n in NAMES:
            if base[n]:
                assert RANK[bod_2604_tier(**{**base, n: False})] >= base_rank
```

**Also update your EPSS ingest.** EPSS v5 began publishing on 2026-06-15, and the bulk daily file now lives at a single stable URL, `https://epss.empiricalsecurity.com/epss_scores-current.csv.gz`, which redirects — so use `curl -L`. For bulk loading, pulling that file once daily is the intended path; the API at `api.first.org/data/v1/epss` is for single-CVE or small-batch lookups, and the "v1" there refers to the API version, not the EPSS model version. If you're polling the API per CVE to populate a local table, you're using it against its documented intent and will be rate-limited.

Use EPSS as a **tiebreak within** a BOD tier, not as the tier itself. The directive's model
is categorical; EPSS is a probability. Ordering a 3-day queue by EPSS is useful. Letting
EPSS override the tier is not.

---

## Part 7 — Test strategy that catches this class of bug

Your current tests are good and would not have caught the real problem. `test_raw_facts`
and `test_campaign_progress` test units in isolation. The bug lives *between* units.

### 7.1 The ladder

| Level | What it proves | Runtime |
|---|---|---|
| L0 | Rule logic: given facts, does the predicate fire | ms |
| L1 | **Contract**: every `requires` path is emitted by some scanner (§3) | ms |
| L2 | Golden corpus: real captured payloads → expected findings | s |
| L3 | **In-process E2E**: ingest → real outbox worker → findings | s |
| L4 | **Fault injection**: worker down, crash mid-run, poison event, redelivery | s |
| L5 | **Invariants under randomised interleaving** | ~20s / 75k states |

L1, L3, L4 and L5 are the ones you don't have. L3 matters most day to day: your current
tests never execute the outbox worker, so nothing exercises the path that actually broke.

```python
def test_ingest_to_finding_through_the_real_worker(db):
    seed_job(db, status=JOB_COMPLETED)
    process_job_result(db, engagement_id=ENG, job_id="j1", agent_id="a1",
                       scanner="smb_scan", facts=SMB_VULN)

    OutboxWorker(db).drain()                        # the REAL worker loop

    assert {f.rule_id for f in findings(db, ENG)} == {"SMB-001", "SMB-002"}
    assert compute_progress(db, ENG).phase == PHASE_COMPLETE
```

### 7.2 The invariants

These are the properties that must hold in **every** reachable state. In the reference
implementation they're checked after every single operation during randomised fuzzing.

| | Invariant | Catches |
|---|---|---|
| I1 | `is_complete` ⟹ every submission covered by a completed run | F11, F12 |
| I2 | `is_complete` ⟹ queue empty | premature completion |
| I3 | `complete` ∧ 0 findings ⟹ 0 blind rules | **false-clean** |
| I4 | `is_complete` ⟹ no live detection lease | F4 |
| I5 | **Soundness**: no finding unsupported by raw facts | false positives |
| I6 | **Completeness**: once complete, every supported finding exists | missed detections |
| I7 | No duplicate `dedupe_key` rows | F5 |
| I8 | Any problem phase carries a human-readable reason | silent failure |
| I9 | **Liveness**: a settled campaign reaches a terminal phase | **the original bug** |
| I10 | `no_match` only if the declared inputs were readable | **F7 structurally** |
| I11 | A finding's id and first-seen never change | F6 |

I9 is the one that would have caught your original bug automatically. The `done`/`completed`
mismatch never crashed and never logged. It just never finished. Liveness — *"given enough
time and no errors, does this thing actually terminate?"* — is the property it violated,
and it's the property nobody writes tests for.

I10 is the structural guard against false-clean. `no_match` is a positive claim that a
rule was evaluated; it's only legitimate if the inputs it declares were present. Checking
that independently is what makes F7 impossible to reintroduce quietly.

### 7.3 The independent oracle

For I5 and I6 the fuzzer recomputes expected findings from raw facts using code that
**shares nothing with the engine** — a hand-rolled restatement of what each rule means. My
first version called the engine's own `evaluate()`, which would have inherited any bug in
it. That's a common and fatal mistake in this kind of test: an oracle that reuses the
implementation can only ever confirm the implementation is consistent with itself.

One honest limitation, worth knowing: **the oracle cannot detect schema drift.** If the
probe stops emitting `smb.data.smbv1_enabled`, the oracle reads the same drifted facts and
also finds nothing, so engine and oracle agree — both blind. This is precisely why the
contract gate (§3) and I10 exist as separate mechanisms. No amount of differential testing
against the collected data will tell you the collected data changed shape.

### 7.4 Mutation testing: verify the verification

A suite that has never failed may simply be incapable of failing. So inject each real bug
back in and confirm the suite catches it:

```
[KILLED  ] original_defect__done_vs_completed              caught by: unit + fuzz
[KILLED  ] absence_read_as_cleanliness                     caught by: unit + fuzz
[KILLED  ] no_reaper__dead_worker_hangs_detection_forever  caught by: unit only
[KILLED  ] coverage_not_recorded                           caught by: unit + fuzz
[KILLED  ] completion_ignores_queue_depth                  caught by: unit only
[KILLED  ] no_idempotency__duplicate_findings              caught by: unit + fuzz
```

**This found a real hole in my own suite.** The idempotency mutant — swapping
`INSERT OR IGNORE` for `INSERT OR REPLACE` — initially **survived**. My tests only counted
findings, and `OR REPLACE` still satisfies the UNIQUE constraint, so counts stayed correct.
But it destroys and recreates the row: a new primary key and a new `created_at` on every
redelivery. Any triage state, ticket link, remediation status or first-seen date attached
to that finding is silently wiped every time the worker retries.

A customer triages a finding, the worker redelivers, the triage is gone. Nothing errors.

The fix was a test asserting identity stability (I11), not a change to the code. That is
what mutation testing is for, and I'd run it in CI on the detection and outbox modules
specifically. Those are the two places where a bug is silent.

---

## Part 8 — Deploy order

Do this in four independently shippable stages. Never ship 1–4 together; you will not know
which one moved the needle.

**Stage 1 — Observability only. No behaviour change.**
Add `detection_trace`, heartbeat, leases, coverage counters. Write the trace, expose the
new fields, change no decision logic. Deploy. Now watch: `rules_blind` on your existing
engagements will tell you immediately whether F7 is your live problem, before you've
changed a single detection.

*I'd expect this alone to answer "what's still missing."*

**Stage 2 — Correctness.**
Reconciled `compute_progress`, coverage-proven completion, reaper, dead-letter,
`on_conflict_do_nothing`. Behaviour changes; the invariant tests must be in place first.

**Stage 3 — Frontend.**
Stall banner, backoff, honest empty state, coverage panel.

**Stage 4 — Prioritization.**
BOD 26-04 tiers with the real transcribed table, EPSS v5 bulk ingest.

**Migrations.** Additive throughout. `detection_trace` and `worker_heartbeat` are new
tables. `detection_runs.covered_scan_result_ids` and `lease_expires_at` are nullable
columns — backfill `covered_scan_result_ids` for historical completed runs from
`scan_results` by `engagement_id` and time window, or accept that old campaigns show as
uncovered and exclude them by `created_at`. `findings.dedupe_key` needs backfill before
the UNIQUE index; expect to resolve pre-existing duplicates, and count them, because that
number tells you how long F5 has been running.

**Rollback.** Stage 1 is pure addition and can be left in place. Stage 2 is the one to
guard: keep the old `campaign_progress` behind a feature flag for one release so you can
compare the two verdicts on live campaigns before cutting over.

---

## Part 9 — Runbook: "the scripts catch it but the manager doesn't"

The exact sequence, once Stage 1 is deployed. Stop at the first step that answers.

**1. Is the pipeline even running?**
```
GET /engagements/{id}/campaign-progress
```
`phase: stalled` → the outbox worker is down or wedged. `queue.dead > 0` → poison event;
read `last_error`. Not `complete`/`complete_with_gaps` → stop here, this is an outage, not
a detection gap.

**2. Ask the rule directly.**
```
GET /engagements/{id}/detection-explain?rule_id=SMB-001
```

| verdict | meaning | action |
|---|---|---|
| `finding_exists` | it fired | the gap is downstream: prioritization filter, severity threshold, tenant scoping, portal query (F14) |
| `evaluated_clean` | rule ran, host not vulnerable | if you disagree, the **rule** is wrong — go to step 4 |
| `schema_drift` | **the contract broke** | go to step 3 |
| `no_evidence_collected` | scanner never ran | scheduling/scope problem, not detection |
| `rule_error` | rule raised | read `reasons`, fix the rule |
| `detection_never_ran` | no trace at all | back to step 1 |

**3. If `schema_drift` — confirm against raw evidence.**
The reason names the exact missing path. Pull the raw facts for that scanner:
```
GET /engagements/{id}/raw-facts?scanner=smb_scan
```
Find where the value actually lives now. Then decide: was it the probe that changed, or
the rule? Fix whichever is wrong, add the payload to the corpus, and the CI gate from §3
prevents recurrence.

**4. If `evaluated_clean` but you believe the host is vulnerable.**
Detection did its job with the data it had. Either the predicate is wrong, or the probe
reported the wrong value. `raw-facts` settles it in one look. If the probe is right and
the predicate is wrong, that's an L0 test and a one-line fix.

**5. If `finding_exists` but nothing in the portal.**
The finding exists and something downstream is eating it. Compare
`detection_trace` match count against the portal query for the same engagement. The
difference is your filter bug. This is F14 and it's the only failure mode the trace
doesn't localise for you, because it happens after detection.

The point of this ladder is that **each step eliminates a whole layer**. Today you have no
way to eliminate any layer, which is why every investigation is a manual crawl through
raw JSON.

---

## Part 10 — Acceptance criteria

Done means all of these, not most:

- [ ] `"done"` is not a valid `DetectionRun` status at the DB, model, or type level
- [ ] `campaign_progress` derives completion from coverage, and is correct for a campaign with ≥2 jobs and ≥2 agents
- [ ] Killing the outbox worker moves a live campaign to `stalled` within 2 minutes, with a specific banner
- [ ] `SIGKILL` on the worker mid-detection: the run reaps to `failed`, the event retries, findings do not duplicate, campaign reaches `complete`
- [ ] Replaying an outbox event 10× yields identical findings, with **identical ids and `created_at`**
- [ ] Renaming a fact key in the probe fixture makes CI fail with the exact missing path
- [ ] A campaign with any blind rule reports `complete_with_gaps`, never `complete`
- [ ] The portal never shows "clean" text when `rules_blind > 0`
- [ ] `detection-explain` returns a correct verdict for all six causes, each covered by a test
- [ ] Fuzz suite runs in CI, ≥50,000 states, zero violations
- [ ] Mutation suite runs in CI on detection + outbox modules, zero survivors
- [ ] BOD 26-04 Table 1 transcribed from the directive, monotonicity test passing
- [ ] EPSS ingest reads the bulk daily file, not per-CVE API calls

---

## Appendix A — Reference implementation

Attached alongside this document. Runs with stdlib Python 3.12, no install step,
no network.

```
vedha_ref/
  pipeline.py            ~620 lines   the model: ingest, outbox worker, detection
                                      engine, trace, progress, explain, prioritization
  test_pipeline.py       34 tests     unit + E2E + fault injection
  fuzz_invariants.py     11 invariants + independent oracle
  mutation_test.py       6 injected bugs, all killed
```

```bash
cd vedha_ref
python3 -m unittest discover -v      # 34 tests
python3 fuzz_invariants.py 1500 50   # 75,000 states
python3 mutation_test.py             # 6/6 killed
```

`pipeline.MAPPING` maps every function to its counterpart in your repo:

| reference | your repo |
|---|---|
| `submit_job_result` | `app/services/job_result_service.process_job_result` |
| `OutboxWorker.tick` | `app/workers/outbox.py` |
| `run_detection` | `app/services/engine_bridge.create_findings_from_facts` |
| `evaluate` / `TraceRow` | `app/detection/engine.run_full_detection` |
| `compute_progress` | `app/routers/engagements.campaign_progress` |
| `explain` | **new** `GET /engagements/{id}/detection-explain` |
| `coverage_report` | **new** `GET /engagements/{id}/coverage` |
| `check_fact_contract` | **new** `tests/test_fact_contract.py` |
| `reap_stale_runs` | **new** reaper in `app/workers/outbox.py` |
| `prioritize` | `app/services/prioritization.py` |

---

## Appendix B — The one-paragraph version

The `done`/`completed` bug and the raw-facts endpoint were both correct fixes to symptoms.
The underlying defect is that your pipeline cannot tell "checked and clean" from "never
checked", because every failure mode collapses into the same observable — an empty findings
list. Fix that by making every rule evaluation write an outcome, not just its matches;
by deriving campaign completion from proven evidence coverage rather than one nullable
status column; by giving the outbox worker a heartbeat, leases, bounded retry and a reaper
so a dead worker announces itself instead of producing a permanent spinner; and by
declaring each rule's fact-path contract so CI fails when the probe stops emitting what a
rule reads. Then test it for liveness and false-clean, not just for correct outputs, and
mutation-test the suite to prove it can fail. Ship the observability first, with no
behaviour change: `rules_blind` on your existing engagements will tell you within a day
whether silent detection blindness is what you've been feeling.
