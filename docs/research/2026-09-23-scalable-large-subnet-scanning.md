# Scalable aggressive scanning for large authorized subnets

**Date:** 2026-09-23

**Repository state reviewed:** `ad6d3ec`

**Status:** research and architecture recommendation; no implementation in this document

**Scope:** authorized IPv4 network vulnerability assessment, especially `/24` and larger scopes

## Executive decision

Vedha should not solve the reported failure by raising the two-hour timeout or by
turning a `/24` into one long-running process. The durable solution is a
**campaign orchestrator** with five independent controls:

1. **Coverage** — quick, standard, or all 65,535 TCP ports.
2. **Pace** — stealth, balanced, or aggressive packets per second.
3. **Confidence** — survey versus verified retry policy.
4. **Depth** — discovery, service identification, or vulnerability checks.
5. **Assurance** — responsive assets versus every authorized address.

The current implementation violates this separation. The UI presents
`aggressive` as a faster timing choice, but the Manager converts it to `deep`,
and `deep` changes the port set to all 65,535 ports while slowing the default rate
and adding retries. The result is a discontinuous jump from about 298 thousand
minimum probes in Normal mode to 16.6 million in Aggressive mode.

The recommended execution architecture is:

```text
immutable authorized scope
  -> lightweight multi-probe discovery
  -> durable discovery manifest
  -> deterministic L4 port-sweep shards
  -> open (IP, port) records
  -> stateful service/vulnerability checks only on relevant opens
  -> coverage-aware campaign finalization
```

This follows the division used by ZMap/ZGrab, Censys, Nmap, and NIST guidance:
discover broadly and cheaply, then spend stateful work on the reduced set
([ZMAP-2013], [ZGRAB], [CENSYS], [NMAP-DISCOVERY], [NIST-800-115]).

For the current reported configuration, **three live hosts** is a conservative
arithmetic seed at the observed 150 pps when budgeting for two retry rounds and
reserving 30% of the two-hour deadline. It is not yet a safety guarantee: the
current runtime cannot attest a hard aggregate rate, raw-SYN capability,
cancellation, or complete coverage. Those controls must be fixed first. The
planner should then size shards from lower-tail sustained throughput (for example
p10/p05 effective pps), equivalently p95/p99 duration, and method-specific
history.

## 1. Confirmed diagnosis in Vedha

### 1.1 Why Stealth and Normal finish but Aggressive is rejected

The following values were resolved directly through the repository's Python
profiles without transmitting packets:

| UI selection | Effective coverage in this workflow | Advertised/default rate | Extra retry rounds | `/24` one-pass probes | Theoretical floor | Retry-bound probe time |
|---|---:|---:|---:|---:|---:|---:|
| Stealth / light | 15 ports | 50 pps from UI | 0 | 3,810 | 76 seconds | 76 seconds |
| Normal / standard | 1,175 ports | 200 pps | 1 | 298,450 | 24.9 minutes | 49.7 minutes |
| Aggressive / deep, observed | 65,535 ports | 150 pps | 2 | 16,645,890 | 30.8 hours | 92.5 hours |
| Aggressive / deep, UI rate | 65,535 ports | 600 pps | 2 | 16,645,890 | 7.7 hours | 23.1 hours |

The observed error is therefore mathematically correct as a best-case lower
bound:

```text
254 usable IPv4 hosts x 65,535 ports = 16,645,890 target pairs
16,645,890 / 150 pps = 110,972.6 seconds = 30.8 hours
```

Completing one pass in two hours would require at least 2,312 effective pps,
before discovery, response collection, retries, service work, or result upload.
The probe currently clamps a job request to at most 2,000 pps
([engine.py](../../probe/agent/engine.py#L250-L268)), so the unsharded job is not
feasible even at the code's theoretical input maximum.

### 1.2 The primary product/contract bug

- The UI defines intensity as an Nmap-like timing control and describes
  Aggressive as 600 pps
  ([scan/page.tsx](../../manager/frontend/app/scan/page.tsx#L148-L157)).
- The frontend request mapper sends that 600 pps setting
  ([scan-launch.ts](../../manager/frontend/lib/scan-launch.ts#L29-L51)).
- The Manager aliases `aggressive` to `deep`
  ([agents.py](../../manager/backend/app/routers/agents.py#L301-L329)).
- The probe's `deep` preset selects the full TCP port range, 150 pps, and two
  extra attempts on silence
  ([intensity.py](../../probe/workflow/intensity.py#L31-L58)).

The module describes intensity as an “orthogonal” knob but then bundles port
breadth with rate, concurrency, timeout, and retry policy. Coverage and pace are
therefore not independent in practice. This is the direct reason only the
Aggressive selection creates an impossible amount of work.

### 1.3 The observed 150 pps reveals deployment or payload drift

In this checkout an explicit `params.rate=600` should win over the `deep` default.
The reported guard used 150 pps instead. In addition, the exact text
`job cannot finish: ...` is not present anywhere in this checkout or its currently
reachable Git history.

At least one of these conditions must be true:

1. The deployed probe image is not built from `ad6d3ec`.
2. A newer or downstream preflight guard resolves the preset before applying the
   explicit rate.
3. The UI-to-Manager or Manager-to-probe path is dropping the explicit tuning.
4. Different Manager and probe releases implement different scan contracts.

Before changing algorithms, capture and persist the job's serialized parameters,
Manager build SHA, probe build SHA, image digest, policy version, and resolved
execution plan. The 2024 ZMap retrospective specifically recommends recording
version, configuration, environment, progress, and machine-readable completion
metadata because these are essential for interpreting and reproducing scans
([ZMAP-2024]).

### 1.4 The job is monolithic even though the workflow batches in memory

The workflow discovers hosts before port scanning and then scans only its
`live_hosts` list
([workflow_engine.py](../../probe/workflow/workflow_engine.py#L497-L518)). That is
good funnel behavior, but `_gather_per_host` only batches coroutines inside one
process. It does not create durable, independently retryable work
([workflow_engine.py](../../probe/workflow/workflow_engine.py#L106-L123)).

One outer `asyncio.wait_for` still owns the entire campaign and imposes one
deadline ([engine.py](../../probe/agent/engine.py#L826-L867)). A crash or timeout
therefore loses scheduling progress for the whole job.

The reported preflight also used all 254 addresses rather than a discovered-live
count. That is conservative but is occurring at the wrong phase. Discovery must
produce a durable manifest first; the planner can then create full-port work for
responsive hosts while preserving a separate, explicit assurance lane for silent
addresses.

### 1.5 Current result delivery is terminal-only

The task runner calls the Manager only after the engine returns
([task_runner.py](../../probe/agent/task_runner.py#L438-L494)). The Manager then
marks the whole attempt terminal and stores one append-only result row
([job_result_service.py](../../manager/backend/app/services/job_result_service.py#L238-L328)).
`ScanResult.attempt_id` is unique, so the current schema cannot accept multiple
chunks for one attempt
([scan_result.py](../../manager/backend/app/models/scan_result.py#L20-L46)).

This is reliable for small jobs but wrong for multi-hour campaigns. It creates a
large loss/retry window and can also collide with the Manager's 32 MiB compressed
and 128 MiB decompressed request limits
([main.py](../../manager/backend/app/main.py#L123-L173)).

### 1.6 Scanner method and rate enforcement can differ from the plan

The hardened probe runs as UID 10001 and drops all Linux capabilities
([Dockerfile](../../probe/Dockerfile#L17-L25),
[install.sh](../../probe/install.sh#L574-L586)). The deployment documentation
states that raw SYN scanning requires an explicitly different network/capability
profile and otherwise falls back to connect scanning
([probe/docker-compose.yml](../../probe/docker-compose.yml#L50-L72)).

Consequently the planner must price the method the probe can actually execute,
not merely the requested `syn` method. A raw SYN sweep and tens of thousands of
kernel `connect()` calls are not equivalent capacity classes.

There are also two rate-governance defects to correct:

- Site policy stores `max_rate_pps`, but probe startup applies only target and
  runtime limits
  ([probe_site.py](../../manager/backend/app/models/probe_site.py#L21-L27),
  [agent.py](../../probe/agent/agent.py#L520-L530)).
- `SendPacer` defaults its adaptive maximum to four times the requested rate and
  is shared by concurrently executing per-host threads without synchronization
  ([scanner_base.py](../../probe/scanner/scanner_base.py#L583-L625),
  [workflow_engine.py](../../probe/workflow/workflow_engine.py#L106-L123)). A
  configured site rate therefore is not currently a defensible hard aggregate
  ceiling.

Finally, the SYN pacer treats every unanswered port as a congestion-loss signal
([syn_scanner.py](../../probe/scanner/syn_scanner.py#L512-L521)). Nmap's official
documentation explains that silence can mean filtering, packet loss, or target
rate limiting; those cases cannot be distinguished from silence alone
([NMAP-TIMING]). A filtered host can therefore cause Vedha to repeatedly halve
its pace even when the source network is healthy, making the 30.8-hour estimate
optimistic.

## 2. Evidence from primary research and authoritative documentation

### 2.1 Use stateless breadth and stateful depth

The original ZMap paper separates fast, single-packet L4 probing from follow-up
actions such as protocol handshakes. Its high throughput comes from independent
send/receive paths, minimal per-target state, response cookies, and a
pseudorandom target permutation ([ZMAP-2013]). ZGrab2 is explicitly designed as
the stateful application-layer companion: ZMap finds responsive L4 targets and
ZGrab performs follow-up handshakes ([ZGRAB]).

Censys operationalized the same funnel: single-packet discovery first, then
pluggable application scanners that emit structured data. Its paper states that
responsive hosts from ZMap seed the application scanners ([CENSYS]). NIST SP
800-115 similarly describes using network-discovery output as input to network
port and service identification ([NIST-800-115]).

**Vedha implication:** a full campaign should not execute discovery, every TCP
port, every banner, and every vulnerability branch inside one indivisible task.
Each phase should consume the durable output of the preceding phase.

### 2.2 Discovery is a filter, not proof that a silent address is absent

Nmap ordinarily performs host discovery before port scanning because scanning
every port of every address is slow and usually unnecessary
([NMAP-DISCOVERY]). It also warns that bypassing discovery and treating every
address as online can slow a scan by an order of magnitude because silent hosts
require retransmission and timeout handling ([NMAP-PN]).

However, Bano et al. show that liveness depends on probe type, filtering,
cross-layer responses, and temporal churn. Their methodology uses ICMP, multiple
TCP protocols, UDP, negative responses, and cross-layer responses rather than a
single ping ([LIVENESS]). The 2024 ZMap retrospective adds that L4 responsiveness
does not perfectly imply L7 service presence and that some systems react
differently to two-phase scanners ([ZMAP-2024]).

**Vedha implication:** support two declared coverage modes:

- `responsive-assets-full`: full-port scanning of assets proven live by a
  documented multi-probe discovery policy. Fast, but not equivalent to every
  address.
- `address-space-full`: every authorized address and every selected port,
  including silent addresses. Expensive, separately sharded, and normally run as
  lower-priority assurance work.

The UI and report must never label the first mode as complete coverage of all 254
addresses.

### 2.3 Full-port scanning should be an explicit coverage decision

Nmap defaults to the 1,000 most common ports; its published empirical table says
that set observed roughly 93% of open TCP ports in the data used to build its
frequency list. It also states that port-scan time is roughly proportional to
the number of ports ([NMAP-PORTS], [NMAP-PORT-SELECTION]). These figures are not
a universal guarantee—an enterprise can use custom high ports—but they explain
why a standard assessment provides strong initial value at a small fraction of
the cost.

**Vedha implication:** the standard set should remain top ports plus organization
and profile-specific high-signal ports. Full 1–65,535 should be selected because
the engagement requires exhaustive coverage, not because the operator chose a
faster timing dial.

### 2.4 A requested rate is a safety ceiling, not a completion guarantee

Nmap exposes a global maximum packet rate and warns that excessive minimum rates
can reduce accuracy or even lengthen scans by causing retransmissions. Limiting
retries shortens runtime at the cost of missed information ([NMAP-TIMING]). RFC
2914 explains why senders must respond to congestion rather than injecting
unbounded best-effort traffic ([RFC-2914]).

ZMap's original gigabit result assumed a well-provisioned source and randomly
dispersed Internet-wide targets; the authors explicitly warn that other source
networks may perform worse ([ZMAP-2013]). ZMap's current guidance says to scan at
the slowest speed necessary and to slow further for smaller target spaces, where
traffic is concentrated rather than dispersed ([ZMAP-README]).

**Vedha implication:** never copy Internet-wide ZMap packet rates onto one `/24`.
Use a hard site-wide budget plus per-destination and per-subnet budgets. Effective
rate is observed throughput after all constraints, not the number displayed by
the UI.

### 2.5 Randomize the `(IP, port)` space and shard deterministically

ZMap traverses a pseudorandom permutation rather than sequential addresses to
spread traffic and avoid concentrated destination load ([ZMAP-2013]). Modern
ZMap treats an `(IP, port)` pair as the target unit and supports deterministic
shards with a shared seed ([ZMAP-MANPAGE]). Masscan likewise permutes the combined
address/port index space, supports non-overlapping shards, and can resume from a
saved index ([MASSCAN-DESIGN], [MASSCAN-MANPAGE]).

The 2024 ZMap paper is especially relevant: its original interleaved sharding had
repeated boundary and off-by-one correctness problems, so the project replaced
it with simple disjoint ranges over the permutation—“pizza” slices that are
easier to reason about while retaining pseudorandom traversal ([ZMAP-2024]).

**Vedha implication:** make shard membership deterministic and independently
verifiable. For a `/24`, simple sorted host slices are adequate. For very large
`(IP, port)` spaces, use disjoint half-open index ranges over a seeded permutation.
Store the range, seed, scope digest, and planned target-pair count with each
shard. Never use a scheduler that merely asks workers to “take the next host”
without a durable membership ledger.

### 2.6 At-least-once work requires idempotent result ingestion

Google's MapReduce design partitions input into bounded tasks, tracks each task's
state, and reschedules work from failed workers. Its master records completion
state and intermediate-output locations rather than relying on one giant worker
([MAPREDUCE]). Google Cloud Tasks explicitly documents at-least-once delivery and
requires idempotent handlers because rare duplicate execution is possible
([CLOUD-TASKS]). AWS's idempotency guidance recommends a caller-provided request
identifier and atomic persistence of that identifier with the mutation
([AWS-IDEMPOTENCY]).

The 2024 ZMap retrospective recommends continuous per-record output where
possible and separate streams for data, progress, metadata, and logs
([ZMAP-2024]).

**Vedha implication:** checkpoint every completed asset locally and upload
idempotent result chunks. A lost acknowledgement may cause the same chunk to be
sent again; Manager acceptance must produce the same logical state rather than
duplicate facts or findings.

### 2.7 Authorization and exclusions are execution invariants

Nmap provides explicit host/network exclusions for mission-critical or
out-of-administration targets ([NMAP-TARGETS]). ZMap has an exclusion structure
for reserved and opt-out ranges and recommends scans no larger or more frequent
than needed ([ZMAP-2013], [ZMAP-MANPAGE]). RFC 1262 says active measurement must
minimize operational impact and should not impose undue burden without explicit
permission ([RFC-1262]).

**Vedha implication:** every campaign and child shard must carry an immutable
authorized-scope snapshot and exclusion digest. Both the probe before transmit
and the Manager during result ingestion must validate it. Splitting a campaign
must never weaken the existing scope gate.

## 3. Proposed target architecture

### 3.1 Separate the public scan contract

Replace one overloaded `intensity` field with explicit axes:

```text
coverage:   quick | standard | full
pace:       stealth | balanced | aggressive
confidence: survey | verified
depth:      discovery | services | vulnerabilities | full_campaign
assurance:  responsive_assets | every_authorized_address
```

Example semantics:

| Axis | Controls | Must not control |
|---|---|---|
| Coverage | selected TCP/UDP ports | packet rate, retry count |
| Pace | aggregate and destination rates, concurrency | port list |
| Confidence | repeats, confirmation rules, diverse vantage policy | port list |
| Depth | last allowed pipeline stage | timing preset |
| Assurance | whether silent addresses receive later exhaustive work | finding severity |

Introduce a versioned scan contract instead of silently changing existing API
semantics. The first-party UI should send contract v2 with explicit axes:

```text
contract_version=2
pace=aggressive
coverage=standard
confidence=survey
depth=full_campaign
```

Legacy contract-v1 clients can temporarily retain the documented old mapping
(`aggressive -> deep`) behind a deprecation warning. Do not globally remap that
value and surprise existing API users. Negotiate `scan_contract_v2` with the
probe, migrate the UI first, observe usage, and then retire v1 deliberately.

### 3.2 Add a capacity-planning contract before enqueue

Manager should expose a pure planning operation that returns, before the user
launches work:

```json
{
  "scope_addresses": 254,
  "coverage_ports": 65535,
  "assurance": "responsive_assets",
  "requested_pps": 600,
  "effective_hard_cap_pps": 600,
  "scanner_method": "syn_raw",
  "confidence_attempts": 3,
  "estimated_shards": 17,
  "estimated_p50_seconds": 41200,
  "estimated_p95_seconds": 69000,
  "deadline_seconds_per_shard": 7200,
  "warnings": []
}
```

The exact figures above are illustrative. The important properties are:

- The plan is persisted, versioned, and returned with a `plan_digest`.
- The probe resolves capabilities again and either accepts the plan or rejects it
  with a stable, actionable error code.
- A change from raw SYN to connect fallback causes re-planning, not silent
  execution under an invalid ETA.
- UI displays both total campaign ETA and per-shard deadline.
- “Aggressive” is allowed to produce many safe child jobs; it is not rejected
  merely because one monolithic job cannot fit.

### 3.3 Use a two-stage dynamic plan

Do not calculate full assessment work from all 254 addresses before discovery.
Create the plan in stages:

1. Validate and persist an immutable audit snapshot of authorized scope and
   exclusions, plus the current live policy/revocation epoch.
2. Run bounded discovery shards.
3. Persist a discovery manifest with evidence and capability tier.
4. Plan full-port shards for responsive assets.
5. If `assurance=every_authorized_address`, also plan lower-priority silent-address
   shards.
6. Feed discovered open services to stateful L7 checks.
7. Finalize only after every required manifest item has a terminal coverage state.

This avoids the current all-254 pessimism without pretending discovery is perfect.

### 3.4 Campaign, phase, shard, and attempt model

Add the following logical records. They may be new tables or extensions of the
existing job/attempt model, but their semantics should remain distinct.

#### `scan_campaign`

- `campaign_id`, tenant, engagement, creator
- immutable scope/exclusion snapshot digests plus current policy/revocation epoch
- coverage, pace, confidence, depth, assurance
- plan version and planner build
- aggregate work units and completion counters
- state: `planning | running | finalizing | cancelling | complete |
  complete_with_gaps | failed | cancelled`
- coverage verdict and finalization timestamp

#### `scan_phase`

- `discovery | l4_sweep | l7_identification | vulnerability_checks`
- dependency set
- planned, completed, partial, failed, and excluded counts
- phase-specific rate allocation

#### `scan_shard`

- immutable target membership or half-open permutation interval
- port selection/range
- seed and scope digest
- planned target-pair count
- predicted p50/p95 runtime and deadline
- assigned site/probe and rate lease
- state and retry budget

#### `scan_attempt`

- existing attempt UUID and fencing token
- probe/build/method/capability metadata
- started, heartbeat, checkpoint, and terminal timestamps
- contiguous acknowledged delivery watermark plus explicit sequence gaps

The campaign is the user's unit. A shard is the scheduler's retry unit. An
attempt is a fenced execution of that shard.

### 3.5 Shard sizing

Use target pairs rather than host count as the fundamental work unit:

```text
pair_budget = floor(
    shard_deadline_seconds
  * conservative_effective_pps
  * deadline_utilization
  / expected_attempts_per_pair
)

hosts_per_shard = floor(pair_budget / ports_per_host)
```

Where:

- `conservative_effective_pps` is the lower of the hard policy allocation and a
  lower-tail observed throughput percentile, such as p10 or p05, for
  `(probe, method, site)`. Equivalently, size from p95/p99 observed duration;
  p95 throughput is the optimistic tail and is the wrong direction for a
  deadline guarantee.
- `deadline_utilization` should initially be 0.70, reserving 30% for discovery
  handoff, cooldown, timeouts, serialization, upload, and variance.
- `expected_attempts_per_pair` must be explicit. For a strict worst-case bound
  with two retry rounds, use 3. For estimates, learn the p95 silent/retry ratio
  and show both expected and worst-case numbers.

At the observed values:

```text
floor(7200 * 150 * 0.70 / (65535 * 3)) = 3 hosts per shard
```

At a measured, safely enforced 600 pps, the same conservative calculation gives
15 hosts per shard. These numbers must be reduced when the method is connect
fallback or when lower-tail throughput/p95 duration says the nominal rate is not
sustained.

Use host-complete shards first. They naturally produce meaningful asset records
and simple retries. Introduce port-range subshards only if a single host cannot
fit its deadline; in that case, merge every range into an asset coverage manifest
before declaring the asset complete or running absence-based resolution.

### 3.6 Deterministic shard correctness

The planner must prove these invariants before dispatch:

```text
union(required shard target pairs) = required campaign target pairs
intersection(any two required shards) = empty
every target pair is inside immutable scope
no target pair is inside immutable exclusions
sum(shard planned pairs) = campaign planned pairs
```

Store a canonical membership hash for small host shards. For very large spaces,
store the permutation version, seed, and half-open start/end indices. Include a
dry-run iterator in tests that enumerates small synthetic spaces and proves no
gaps, overlap, off-by-one termination, or seed drift.

### 3.7 Rate-governance hierarchy

Use a nested governance hierarchy:

```text
Manager site budget
  -> per-probe leased allocation
      -> local global token bucket
          -> per-subnet and per-destination buckets
```

Rules:

1. `site.max_rate_pps` is a hard aggregate ceiling across all active shards and
   probes at that site.
2. A lease carries an allocation and expiry; unused capacity can be reassigned.
3. The local pacer may adapt downward but must never increase above the leased
   hard cap.
4. Multiple host threads must share a synchronized global pacer or consume from
   one sender loop.
5. Randomize across the whole shard's `(IP, port)` pairs instead of completing
   65,535 sends to one host before moving to the next.
6. Track source-side send errors, kernel/NIC capture drops, queue depth, RTT, and
   abrupt changes from a baseline. Do not equate every filtered port with
   congestion.
7. Record requested, allocated, initial, p05/p10, p50, p95, and final effective
   pps, plus p50/p95 shard duration.

For multiple probes, assign disjoint shards and keep one site-wide budget.
Launching the same target list independently on several probes is duplication,
not distribution, and multiplies target pressure.

### 3.8 Scanner engine boundary

Define a narrow internal `L4SweepEngine` adapter whose output is an immutable
stream of open `(IP, port, protocol, evidence)` records plus a typed
`CoverageReceipt`.

Candidate implementations:

- Vedha's native SYN scanner for dependency-free deployments.
- ZMap 4.x for an externally installed, mature multi-port stateless engine with
  deterministic sharding.
- The existing Masscan wrapper for separately governed validation or an approved
  high-scale deployment.

Do not couple campaign semantics to one executable. Run a conformance suite over
each engine:

- known open, closed, filtered, and rate-limited fixtures
- target-pair coverage and exclusion proofs
- duplicate response handling
- pause/resume behavior
- method/capability downgrade
- measured false-negative and false-positive rates
- output schema and scope validation

The high-scale engine should perform L4 breadth only. Vedha's stateful service,
TLS, SMB, OS, and vulnerability logic should consume confirmed opens. This is the
small-tool pipeline recommended by the ZMap authors after a decade of operating
the project ([ZMAP-2024]).

## 4. Checkpointing and incremental results

### 4.1 Answer to “send after every asset?”

**Checkpoint after every completed asset: yes. Trigger a full Manager detection
and prioritization pass after every asset: no.**

Use two independent thresholds:

- Local durability: fsync/atomic checkpoint at every host or completed port-range
  unit.
- Network upload: cut envelopes only at completed-work-unit boundaries and flush
  when a small host-count, byte, or time threshold is reached. Set host-count to
  one when the remote-durability RPO requires immediate per-asset acknowledgement.

For the first incremental-receipt implementation, a host-complete logical work
unit is simplest. The transport may batch several small host receipts into a
1–5 MiB envelope to reduce HTTP/transaction overhead without changing logical
idempotency or materially increasing the crash-loss window.

### 4.2 Chunk protocol

Add a separate non-terminal endpoint and append-only table. Do not reuse the
current terminal result API.

Use two identities. A delivery identity authorizes and deduplicates transport
within one attempt; a logical identity deduplicates completed work across
replacement attempts:

```text
delivery: (attempt_id, fence, sequence_number)
logical:  (campaign_id, shard_id, work_unit_id, schema_version)
```

`work_unit_id` is deterministic from the immutable plan and identifies one host
or port-range unit independent of the attempt that executed it. If attempt A
uploads hosts 1 and 2 and attempt B resumes the shard, those units remain complete
instead of becoming duplicate evidence. The attempt and fence are provenance and
authorization, not semantic identity. Sequence continuity proves delivery only;
campaign coverage is proved by equality between planned and accepted work-unit
sets.

Each chunk carries:

- content checksum and schema version
- scope and plan digests
- probe/build/scanner method
- one or more host/port-range completion records
- facts discovered so far
- planned, attempted, answered, retried, and unresolved counts
- start/end timestamps and effective rate telemetry
- whether the chunk is data, progress, or final metadata

Manager behavior:

1. Authenticate the tenant/probe and look up the delivery identity. If it was
   committed with the same checksum, return the original acknowledgement even if
   the attempt is now stale; this is the lost-ACK case.
2. For a new delivery, validate the current fence, cancellation/policy epoch,
   scope, exclusions, plan digest, and exact shard target-pair membership.
3. Insert the delivery and logical work-unit receipts atomically.
4. If a logical identity and checksum already exist, return the original
   acknowledgement without duplicating facts.
5. If either identity exists with a different checksum, reject as a permanent
   protocol conflict.
6. Acknowledge only after durable commit.
7. Probe retains the local spool until acknowledgement.
8. Track both a contiguous sequence watermark and explicit gaps; a highest
   sequence alone is insufficient for out-of-order delivery.
9. Finalization supplies an aggregate checksum and coverage manifest; Manager
   verifies exact planned-versus-accepted unit equality, not only sequence
   continuity.

Retries use exponential backoff with jitter and respect cancellation. The same
delivery identity and sequence number must be reused after an uncertain outcome.
A replacement attempt requests only residual work units not already accepted.

### 4.3 Detection and prioritization

Raw facts may be detected incrementally so useful findings appear early, but
absence-based decisions require final coverage.

The existing ADR notes that every submission currently re-prioritizes the entire
engagement, creating work proportional to submissions times findings
([ADR-0001](../adr/0001-manager-detection-pipeline.md#r3--every-submission-re-prioritises-the-entire-engagement)).
Per-host uploads would magnify that problem.

Therefore:

- enqueue durable `facts.ready` events per accepted chunk;
- make detection idempotent per
  `(input_receipt_id, detector_bundle_digest)`;
- coalesce or debounce engagement prioritization;
- update touched findings incrementally;
- pin or deliberately reconcile the detector ruleset and vulnerability-database
  snapshot used by the campaign;
- run final absence/auto-resolution only after the campaign coverage manifest is
  complete and the required detector bundle has processed every accepted input.

## 5. Coverage and partial-result semantics

A vulnerability platform must distinguish “not found” from “not assessed.” Store
coverage as first-class evidence.

Recommended per-asset/per-phase states:

| State | Meaning |
|---|---|
| `not_planned` | Outside the declared campaign plan |
| `excluded` | Explicitly omitted by policy |
| `planned` | Required but not started |
| `in_progress` | At least one unit started; required work remains |
| `complete` | Every required unit has accepted evidence |
| `partial` | Some evidence accepted; required units missing |
| `failed` | Retry policy exhausted |
| `unresponsive` | Discovery produced no proof of life; not equivalent to clean |

Campaign verdicts should be:

- `complete`: all required coverage and detection complete.
- `complete_with_gaps`: terminal, but some assets/phases are partial, failed, or
  unresponsive under an assurance mode that required more.
- `failed`: campaign could not produce a valid result set.
- `cancelled`: explicitly stopped; accepted partial facts remain visible.

Never close a finding merely because it is absent from a partial campaign. This
aligns with Vedha's existing coverage-gated resolution plan
([coverage-gated plan](../superpowers/plans/2026-08-11-coverage-gated-auto-resolution.md)).

## 6. Second-pass failure-mode review

### 6.1 Important execution-path distinction

Vedha currently has two different orchestration concepts:

- Manager-dispatched `network_va`, which maps to the ordinary `assessment`
  workflow. The code explicitly says the richer sequential campaign is
  standalone-only
  ([engine.py](../../probe/agent/engine.py#L111-L124)). The reported 0-second
  rejection belongs to this managed path or to a deployed preflight in front of
  it.
- `scanner.va_campaign`, which is a standalone/local campaign and progress
  implementation. It is not the code path that raised the reported error, but it
  contains correctness failures that make it unsafe to adopt unchanged as the
  production campaign coordinator.

The product currently calls `uc_network_va` a “complete” campaign while these
paths have different stages, progress, CVE behavior, and failure semantics. A
versioned Manager-owned campaign contract must become canonical; scanner modules
remain execution adapters beneath it.

### 6.2 Ranked FMEA

`P0` means a safety, authorization, false-clean, or terminal-state correctness
blocker. `P1` means likely loss of work, outage, or inability to scale reliably.
`P2` means observability or maintainability debt that materially slows incident
response.

| Rank | Failure mode and trigger | Customer/operational effect | Code evidence | Required control |
|---|---|---|---|---|
| P0 | **Release/plan drift:** the checkout's UI sends 600 pps, while the rejection prices 150 pps and its exact error string is absent. | A patch can target the wrong code or configuration; ETA and policy cannot be reproduced. | [scan-launch.ts](../../manager/frontend/lib/scan-launch.ts#L29-L51), [engine.py](../../probe/agent/engine.py#L240-L268) | Persist request, resolved plan, Manager/probe SHAs, image digest, planner version, and capability digest; reject incompatible versions before transmit. |
| P0 | **Partial becomes completed:** timeout/degraded work with any evidence sets `ok=true`; TaskRunner maps that to wire `success=true`; Manager sets the job `completed`. | A deadline-truncated exhaustive scan can appear green and later drive a clean conclusion. | [engine.py](../../probe/agent/engine.py#L882-L930), [task_runner.py](../../probe/agent/task_runner.py#L466-L494), [job_result_service.py](../../manager/backend/app/services/job_result_service.py#L289-L326) | Use a typed outcome (`succeeded`, `partial`, `failed`, `cancelled`) independent of “has useful facts”; require a coverage receipt for success. |
| P0 | **Cancellation does not stop raw packets:** async cancellation cancels the future, but the blocking executor loop has no stop token. | Traffic may continue after an operator cancels, the lease is revoked, or the two-hour deadline expires; a replacement attempt can overlap it. | [engine.py](../../probe/agent/engine.py#L550-L568), [syn_scanner.py](../../probe/scanner/syn_scanner.py#L379-L382), [syn_scanner.py](../../probe/scanner/syn_scanner.py#L425-L524) | Cooperative cancellation at small send windows or a killable helper process; do not acknowledge cancellation until egress stops. |
| P0 | **Advertised rate is not a hard rate:** the site cap is not applied; `SendPacer` may rise to 4x and is not thread-safe; the standalone path gives each host a full-rate scanner. | Policy/ROE breach, target disruption, self-induced loss, and invalid duration math. | [agent.py](../../probe/agent/agent.py#L517-L530), [scanner_base.py](../../probe/scanner/scanner_base.py#L583-L625), [va_campaign.py](../../probe/scanner/va_campaign.py#L420-L444) | One synchronized hard site/probe grant with subnet/destination buckets; adaptation may decrease but never exceed the grant. |
| P0 | **Raw SYN cannot prove coverage:** a round sends all pending ports before receiving; raw output normally contains opens only and no `scan_summary`. | Receive-buffer overflow or send failure can manufacture false negatives while the trace still says completed. | [syn_scanner.py](../../probe/scanner/syn_scanner.py#L398-L459), [syn_scanner.py](../../probe/scanner/syn_scanner.py#L459-L592), [execution.py](../../probe/workflow/execution.py#L289-L415) | Concurrent sender/receiver with bounded windows and an engine-neutral `CoverageReceipt` containing planned, sent, classified, unresolved, retry, send-error, and drop counts. |
| P0 | **Coverage-gated resolution is too coarse:** any fact from a completed scanner can mark an entire asset covered. | A standard-port or TLS-only result can advance the miss count for an unrelated finding previously found on another port/scanner; per-asset chunks make this worse. | [resolution.py](../../manager/backend/app/detection/resolution.py#L36-L64), [resolution.py](../../manager/backend/app/detection/resolution.py#L100-L145) | Positive detection may run incrementally; absence-based resolution runs only after final coverage for `(asset, vantage, protocol, port set, scanner/rule, confidence, detector bundle)`. |
| P0 | **Result authorization checks the engagement, not the assigned work:** current ingest validates CIDRs but not requested host/port membership or a plan digest. | A buggy or compromised probe can submit an in-scope but unassigned target/port and corrupt deduplication and coverage. | [job_result_service.py](../../manager/backend/app/services/job_result_service.py#L267-L287) | Validate every fact and coverage unit against exact immutable shard membership and exclusions. |
| P0 | **Caller-controlled scope exemption:** facts named `ipv6_discovery` are omitted from scope identity checks but still persisted and sent to detection. | An arbitrary out-of-scope IP can bypass result scope validation by using that scanner label. | [job_result_service.py](../../manager/backend/app/services/job_result_service.py#L61-L113), [test_run_scoped_fact_scope.py](../../manager/backend/tests/test_run_scoped_fact_scope.py#L94-L100) | Put run metadata in a separate typed field/table; never exempt an arbitrary fact target by scanner name, or strip the record before persistence. |
| P0 | **Job/attempt lifecycle lock order is inconsistent:** heartbeat locks attempt then job; result locks job then attempt; cancel does not lock/CAS the row. | Deadlock, stale cancellation overwriting completion, or two terminal outcomes under result/heartbeat/reaper/cancel races. | [job_attempt_service.py](../../manager/backend/app/services/job_attempt_service.py#L86-L129), [job_result_service.py](../../manager/backend/app/services/job_result_service.py#L186-L233), [agents.py](../../manager/backend/app/routers/agents.py#L1249-L1291) | One lock order (`campaign/job -> attempt`), fenced compare-and-swap transitions, and the same parent lock for cancel and finalization. |
| P0 | **Detection failure can be acknowledged as done:** the detector catches a broad exception, marks its run failed, and returns normally; the outbox then marks the event done. | Transient detector failure loses retry and can strand the campaign with durable facts but no findings. | [engine_bridge.py](../../manager/backend/app/detection/engine_bridge.py#L657-L674), [outbox.py](../../manager/backend/app/workers/outbox.py#L389-L398) | Propagate typed retryable failures; mark an event done only after a unique durable detector receipt exists. |
| P0 | **Outbox claim expiry is not renewable or fenced:** 16 events may wait behind same-engagement serialization, but a fixed five-minute timestamp permits reclaim and `_mark_done` has no claim token. | Old and new workers can process/complete the same input concurrently. | [outbox.py](../../manager/backend/app/workers/outbox.py#L41-L69), [outbox.py](../../manager/backend/app/workers/outbox.py#L213-L283), [outbox.py](../../manager/backend/app/workers/outbox.py#L358-L364) | Renewable claim token/worker lease and CAS completion, or claim at most one event per engagement. |
| P1 | **Silent connect fallback changes the capacity class:** the hardened container lacks raw-socket capability; retry/cleanup behavior also changes. | A shard priced as stateless SYN can become a much slower socket-heavy job and miss its deadline. | [Dockerfile](../../probe/Dockerfile#L17-L25), [syn_scanner.py](../../probe/scanner/syn_scanner.py#L347-L375), [port_scanner.py](../../probe/scanner/port_scanner.py#L619-L645) | Capability-attest before planning; a method change requests re-plan rather than silently continuing. Keep the default hardened; isolate any approved `NET_RAW` helper. |
| P1 | **Connect fallback amplifies tasks and memory:** up to 80 hosts each build a 65,535-entry queue/result map and up to 80 workers; cleanup creates one coroutine per ambiguous port. | Multi-GB memory growth, FD pressure, event-loop overload, and OOM/retry loops. | [workflow_engine.py](../../probe/workflow/workflow_engine.py#L106-L123), [port_scanner.py](../../probe/scanner/port_scanner.py#L619-L773) | One globally bounded `(host, port)` stream, small host-complete shards, bounded cleanup workers, and explicit FD/memory admission budgets. |
| P1 | **Shared scanner state crosses hosts:** a shared pacer is unsynchronized; the “per-host” delivery window is instance state; one host can flip the whole scanner to fallback. | Cross-host throttling, burstiness, race-dependent method changes, and irreproducible coverage. | [workflow_engine.py](../../probe/workflow/workflow_engine.py#L500-L518), [port_scanner.py](../../probe/scanner/port_scanner.py#L395-L398), [syn_scanner.py](../../probe/scanner/syn_scanner.py#L339-L369) | Keep timeout/congestion/method state host-local; share only a locked aggregate budget and receiver. |
| P1 | **Discovery is treated as an exhaustive gate:** full-port work runs only for hosts declared live. | A host filtering discovery probes but open on an unusual port is omitted from “every address” coverage. | [workflow_engine.py](../../probe/workflow/workflow_engine.py#L463-L518) | Declare `responsive_assets` versus `every_authorized_address`; discovery prioritizes but does not silently narrow the latter. Give discovery manifests vantage, policy, timestamp, and TTL. |
| P1 | **Work and results are terminal-only:** a batch must finish before cache/store; one terminal payload is sent; the reaper retries the entire logical job. | Crash, timeout, or stale fence discards hours of completed-host work and repeats target traffic. | [workflow_engine.py](../../probe/workflow/workflow_engine.py#L106-L123), [task_runner.py](../../probe/agent/task_runner.py#L438-L494), [reaper.py](../../manager/backend/app/workers/reaper.py#L33-L53) | Durable logical work-unit receipts, residual-work retries, and bounded host checkpoints. |
| P1 | **Current result API cannot accept incremental receipts:** `attempt_id` is unique and ingest terminalizes the job; large gzip bodies are fully buffered and inflated before the output-size check. | Later asset uploads conflict, large results hit 413, and a compressed bomb can exhaust memory before validation. | [scan_result.py](../../manager/backend/app/models/scan_result.py#L20-L46), [main.py](../../manager/backend/app/main.py#L123-L192) | Separate bounded chunk/receipt table and endpoint; streaming decompression with a running cap; short ingest transaction. |
| P1 | **Naive per-asset detection creates a worker storm:** each accepted input can run detection and whole-engagement prioritization. | `O(chunks x findings)` database work and long outbox leases; useful scanning outruns analysis. | [ADR-0001](../adr/0001-manager-detection-pipeline.md#r3--every-submission-re-prioritises-the-entire-engagement), [outbox.py](../../manager/backend/app/workers/outbox.py#L174-L188) | Positive-only, idempotent detector receipts per bundle; bounded coalescing; touched-finding scoring; one final negative-resolution pass. |
| P1 | **Empty/zero-open work has no durable processing receipt:** a `ScanResult` and outbox event exist only when facts are non-empty. | A legitimately clean/empty shard can remain “aggregating” forever, or be indistinguishable from not processed. | [job_result_service.py](../../manager/backend/app/services/job_result_service.py#L298-L345), [engagements.py](../../manager/backend/app/routers/engagements.py#L724-L741) | Persist a zero-fact coverage receipt and a no-work detector receipt. |
| P1 | **“Campaign” is engagement-history-wide:** progress reads every historical job, result, run, outbox event, and open finding for an engagement. | Unrelated old work contaminates a new launch; one historical dead event can keep future views in error; queries grow without bound. | [engagements.py](../../manager/backend/app/routers/engagements.py#L773-L883) | First-class `campaign_id`, campaign-scoped projections/indexes, materialized counters as caches, and pagination. |
| P1 | **Launch/queue operations are not idempotent or transactionally capped:** enqueue is count-then-insert; probes load all tenant-pending rows and Python-filter them. | Double-click/retry duplicates scans, concurrent launch exceeds the cap, and thousands of shards create unfair/unbounded polling. | [agents.py](../../manager/backend/app/routers/agents.py#L1206-L1215), [agents.py](../../manager/backend/app/routers/agents.py#L1380-L1391), [agents.py](../../manager/backend/app/routers/agents.py#L1486-L1493) | Unique tenant/idempotency key with request hash, transactional capacity reservation, bounded SQL-routable candidate query, campaign active cap, and weighted fairness. |
| P1 | **Standalone campaign declares failure as success and orders depth before full breadth.** | A failed stage can end at 100%/completed, and an unusual port found by the later full sweep never receives deep assessment. | [va_campaign.py](../../probe/scanner/va_campaign.py#L222-L320), [va_campaign.py](../../probe/scanner/va_campaign.py#L587-L616), [test_va_campaign.py](../../probe/tests/test_va_campaign.py#L119-L134) | Do not promote this orchestrator unchanged; required-stage errors produce partial/failed and full breadth precedes depth or triggers delta assessment. |
| P2 | **Progress and ETA are work-blind:** standalone ETA gives each stage equal weight and callback failure is debug-only. | A full-port stage appears frozen for hours and progress loss is invisible. | [va_campaign.py](../../probe/scanner/va_campaign.py#L236-L273) | Progress by accepted work units/target pairs and measured lower-tail throughput; alert on stalled progress sinks/spool. |

### 6.3 Fail-closed response policy

| Event | Required behavior |
|---|---|
| Plan/build/capability digest mismatch | Reject before packets leave the probe; return `replan_required`. |
| Raw SYN unavailable or method changes mid-shard | Stop at the current bounded unit, checkpoint it, and re-plan the residual work for the new capacity class. |
| Rate grant or authorization epoch expires | Stop transmitting; do not “finish the host” outside authority. |
| Operator cancel or stale fence | Revoke new work immediately, stop egress, retain already accepted positive evidence, and finalize as cancelled/partial with no absence-based resolution. |
| Send error, FD/buffer exhaustion, capture drop, or unresolved target pairs | Mark the unit degraded/partial; never translate a local failure to target `filtered`. Throttle once, then fail the bounded unit if health does not recover. |
| Manager unavailable | Checkpoint locally and retry the same delivery identity. Continue only while the rate grant is valid and spool is below its high-water mark; otherwise pause. |
| Chunk acknowledgement uncertain | Resend the identical delivery identity and checksum; never mint a new logical unit. |
| Out-of-order or missing sequence | Accept valid independent units, track gaps, and block finalization until exact manifest reconciliation succeeds. |
| Detector transient failure | Keep facts durable, renew/retry the detector claim, and keep campaign state `detecting`/`stalled`; never mark the input done without a detector receipt. |
| Coverage gap after retry budget | Finish as `complete_with_gaps`, preserve positives, display exact missing units, and prohibit clean/auto-resolution conclusions for those domains. |
| Spool/disk high-water | Stop claiming shards, flush/compact the append journal, and alert; never evict unacknowledged evidence. |

### 6.4 Recommended deep-module boundary

Keep this inside the existing Manager and probe deployments initially; it does
not require another microservice.

```text
ScanPlanner.plan(request_v2, scope_snapshot, live_policy,
                 probe_capabilities, capacity_history)
    -> ExecutionPlan | PlanRejection

CampaignCoordinator.reconcile(campaign_id)
    -> transactional scheduling/cancel/finalization commands

ResultLedger.accept(work_receipt)
    -> durable acknowledgement

L4SweepEngine.execute(shard, hard_budget, stop_token, receipt_sink)
    -> CoverageReceipt
```

- `ScanPlanner` hides legacy translation, validation, total/per-shard feasibility,
  method selection, deterministic membership, and the plan digest.
- `CampaignCoordinator` hides staged fan-out, sealed planning generations,
  retries, fairness, policy revocation, cancellation, and finalization.
- `ResultLedger` hides fencing, transport and logical idempotency, exact shard
  membership validation, facts, coverage, and transactional outbox creation.
- `L4SweepEngine` is the only justified scanner adapter seam. Native SYN,
  connect, and an approved Masscan/ZMap engine must all return the same typed
  coverage receipt.

Do not expose planner internals or scanner-specific flags throughout the UI,
routers, scheduler, and detector. The public contract should remain the explicit
five axes plus authorization and time-window policy.

The alternative—letting each probe own an autonomous multi-hour campaign—was
rejected because a probe cannot enforce a site-wide multi-probe budget, provide
transactional tenant idempotency/fairness, or safely fail over campaign state.
The probe should own local pacing, cancellation, and checkpoints; the Manager
owns durable campaign truth.

### 6.5 Shard feasibility is not campaign feasibility

Sharding prevents one job from exceeding two hours; it does not reduce total
work. An exhaustive IPv4 `/16` contains 4,294,770,690 TCP target pairs:

| Hard aggregate rate | One pass | Three-attempt worst-case |
|---:|---:|---:|
| 150 pps | 331 days | 994 days |
| 600 pps | 82.9 days | 248.5 days |
| 2,000 pps | 24.9 days | 74.6 days |

The planner therefore needs campaign-level admission controls in addition to
per-shard deadlines:

- maximum target pairs/packets and projected p95 duration;
- required completion deadline and authorized maintenance windows;
- daily and site-wide traffic budget;
- maximum active/queued shards and campaign TTL;
- predicted storage and detector workload;
- a stale-discovery/plan policy.

Some full-subnet requests must be rejected as operationally infeasible even
though they can be divided into valid shards. The recommended `/16` default is
discovery plus standard coverage across responsive assets, followed by explicit
full-port work on selected high-value assets. “Every address, every port” must be
an exceptional assurance policy with a separately approved budget.

### 6.6 Finalization, cancellation, and authorization invariants

Aggregate campaign counters are useful projections, not completion proof. The
finalizer must take a campaign row/advisory lock and derive truth from canonical
records:

1. The current planning generation is sealed; planner retry produced the same
   membership digests and did not append duplicate shards.
2. Every required shard is terminal and every planned logical work unit has
   exactly one accepted receipt or an explicit terminal gap state.
3. Every accepted fact input has a successful detector receipt for the campaign's
   pinned detector/rule bundle and vulnerability-database snapshot.
4. No required retry, dead-letter, sequence gap, or open cancellation remains.
5. A compare-and-swap transition moves `running -> finalizing -> complete` or
   `complete_with_gaps`; concurrent finalizers cannot both win.

Cancellation takes the same parent lock and monotonically moves
`running -> cancelling -> cancelled`, increments a cancellation epoch, revokes
attempt fences/rate grants, and blocks new deliveries. A final chunk racing cancel
is therefore serialized rather than dependent on timing.

Authorization has two layers:

```text
immutable scope/exclusion snapshot and digest (audit/reproducibility)
+ live policy/revocation epoch and emergency deny list (current authority)
```

The probe checks both before dispatch and periodically during a long shard. A
policy epoch change pauses or cancels affected units; an immutable historical
snapshot must never be interpreted as permission to ignore a later revocation.

### 6.7 Smallest safe implementation slice

Avoid changing every subsystem at once. The first production slice should be:

1. Contract v2 and artifact/plan provenance.
2. Typed outcome plus trustworthy `CoverageReceipt`; disable negative resolution
   for partial or unfinalized campaign evidence.
3. Hard aggregate pacing and cancellation that proves egress stopped.
4. One `scan_campaign` parent; add `campaign_id`, stage, shard ordinal,
   generation, plan digest, and typed outcome to bounded child jobs.
5. Discovery first, then a bounded wave of small host-complete L4 child shards.
6. Campaign-scoped progress and transactionally safe finalization/cancel.

Existing terminal results can serve these small child shards initially if their
measured result-loss window and payload remain inside the agreed RPO/SLO. Add the
separate `ResultLedger` work-receipt endpoint when the required RPO is one host,
payload limits are approached, or larger campaigns are enabled. For that path,
checkpoint each completed asset locally, but upload a bounded batch on host,
size, or time thresholds—do not synchronously run the full Manager pipeline once
per asset.

Defer multi-probe distributed rate leases and a new external breadth engine until
the single-probe campaign invariants pass. Benchmark the existing Masscan wrapper
behind the same `L4SweepEngine` conformance suite before adding another adapter.

## 7. Operational rollout plan

### Phase 0 — establish provenance and stop misleading launches

1. Capture the deployed Manager/probe build SHAs and image digests.
2. Persist and display the resolved job plan and effective rate.
3. Add a stable `capacity_plan_infeasible` code with work math and alternatives.
4. Move the first-party UI to contract v2 with explicit coverage and pace;
   preserve and warn on legacy-v1 translation until its planned retirement.
5. Correct typed outcome propagation so partial work cannot become a completed
   job/campaign, and disable negative auto-resolution without dimensional final
   coverage.
6. Make deadline, lease loss, and operator cancellation stop raw packet egress.
7. Enforce `max_rate_pps` on the probe as a hard cap.
8. Prevent the adaptive pacer from increasing above its lease and make aggregate
   pacing thread-safe.
9. Distinguish raw SYN from connect fallback at planning time.
10. Fix result-scope metadata separation and standardize Manager job/attempt lock
    order before adding concurrency.

### Phase 1 — campaign planner and discovery manifest

1. Add the minimal campaign parent and shard metadata plus a pure deterministic
   planner; introduce a separate phase table only when its independent lifecycle
   is needed.
2. Execute discovery as its own bounded phase.
3. Persist responsive, silent, excluded, and errored targets with evidence.
4. Generate L4 shards from the manifest and selected assurance policy.
5. Apply campaign-wide packet/time/window/storage admission before enqueue.
6. Show total campaign ETA, shard count, and expected traffic before launch.

### Phase 2 — durable shard scheduling

1. Reuse the existing attempt and fence model for each child shard after
   standardizing lock order and cancellation CAS.
2. Lease rate allocation with the shard.
3. Retry only failed/expired shards, never the entire campaign.
4. Support cancellation at campaign and shard granularity.
5. Add fairness so one `/16` campaign cannot starve small jobs.
6. Seal dynamic planning generations and make planner retry idempotent.

### Phase 3 — incremental result chunks

1. Add separate delivery and logical work-unit identities, chunk/receipt schema,
   endpoint, append-journal spool format, and acknowledgements.
2. Checkpoint after host completion.
3. Add duplicate, conflicting, missing, and out-of-order chunk tests.
4. Add final coverage manifest validation.
5. Add renewable/fenced detector receipts and coalesce detection/prioritization
   work.

### Phase 4 — calibrated capacity and multi-probe scheduling

1. Measure lower-tail p05/p10 effective pps and p50/p95 duration by site, probe,
   and scan method.
2. Size future shards from conservative history.
3. Allocate disjoint shards to several probes only when their network vantage is
   valid for those targets.
4. Enforce one aggregate site budget.
5. Add optional diverse-vantage verification as a confidence policy, not as
   duplicate uncoordinated scans. The ZMap retrospective reports that diverse
   vantages can recover transient visibility missed by repeated probes from one
   source ([ZMAP-2024]).

### Phase 5 — canary and migration

1. Feature-flag campaign sharding and chunk ingestion separately.
2. Shadow-plan existing jobs and compare predicted versus actual runtime.
3. Canary one authorized site and one `/24`.
4. Compare standard and exhaustive coverage against known fixtures.
5. Preserve read compatibility with existing single-result jobs.
6. Roll back by disabling new campaign creation; retain accepted chunks and facts.

## 8. Verification strategy

### Unit/property tests

- Exact reproduction of `254 x 65,535` work math.
- Coverage and pace are independent in every API translation.
- Explicit tuning survives UI -> Manager -> probe serialization.
- Contract-v1 and v2 translations are separately pinned and capability-negotiated.
- Deterministic shard union, disjointness, termination, and stable digest.
- Scope subtraction and exclusions under IPv4 CIDRs/ranges.
- Formula boundaries at one pair below/equal/above the deadline budget.
- Hard aggregate rate never exceeded under many concurrent host workers.
- Filtered silence does not automatically prove source congestion.
- A zero-open raw-SYN unit still produces a complete or explicitly degraded
  coverage receipt.
- Campaign admission rejects a globally infeasible plan even when every shard
  individually fits its deadline.

### Integration tests

- Probe dies after N completed hosts; replacement attempt resumes without lost or
  duplicate logical results.
- Manager commits a chunk but its acknowledgement is dropped; retry is idempotent.
- Duplicate, stale-fence, different-checksum, out-of-order, cross-attempt, and
  logical-work-unit receipt cases.
- Result exceeds one chunk threshold but remains below endpoint limits.
- Raw SYN capability removed between planning and execution triggers re-plan.
- Connect fallback produces a different capacity class.
- Campaign cancellation preserves accepted partial evidence.
- Detection sees early positive findings but does not auto-resolve on partial
  coverage.
- An in-scope but outside-shard host/port is rejected, and a caller-controlled
  scanner label cannot bypass scope.
- A zero-fact/zero-open shard obtains both a durable coverage receipt and a
  no-work detector receipt.
- Detector transient failure retries and no outbox event becomes done without a
  detector receipt.

### Network laboratory tests

- Known open, closed, and silently filtered ports.
- A host that blocks ICMP but answers TCP, and the reverse.
- RST/ICMP rate limiting and controlled loss.
- Fragile/low-capacity target with per-destination cap.
- Proxy ARP and middlebox-induced false liveness.
- Multiple probes with deliberately overlapping candidate inputs; scheduler still
  assigns disjoint target pairs.
- Cancel or expire a raw scan while transmitting and prove no packet leaves after
  cancellation acknowledgement.
- Burst replies during a wide raw scan while measuring socket/NIC drops and
  validating concurrent receive behavior.

### Load and chaos tests

- Sparse and dense synthetic `/24` campaigns.
- Synthetic `/16` planning without materializing one giant in-memory task list.
- Manager/probe restart, database failover, queue backlog, upload timeout, and
  spool pressure.
- 413 response, corrupt chunk, and disk-full behavior.
- Detection backlog under thousands of chunks with coalesced prioritization.
- Compressed bomb, oversized uncompressed body, excessive nesting/cardinality,
  and spool high-water behavior.
- Real-Postgres races: heartbeat versus result, reaper versus result, cancel versus
  last result, finalizer versus cancel, and concurrent idempotent launch.
- Mixed-version Manager/worker/probe matrix and rollback while campaigns remain in
  flight.

## 9. Observability and service-level objectives

Required metrics:

- planned, attempted, answered, retried, and unresolved target pairs
- unique hosts planned/live/complete/partial/failed
- requested, leased, initial, current, p05/p10/p50/p95, and final effective pps
- raw SYN versus connect fallback counts
- local send errors, capture drops, response duplication, timeout distribution
- active/queued shards and queue wait time
- estimated versus actual shard duration
- chunk bytes, acknowledgement latency, duplicate count, spool files/bytes
- outbox/detection/prioritization lag
- scope/exclusion rejection count
- campaign coverage percentage by phase

Suggested initial SLOs:

- 100% of transmitted target pairs pass both the immutable scope/exclusion
  snapshot and the current policy/revocation gate.
- 100% of accepted chunks are idempotently reproducible by identity/checksum.
- A probe crash loses no acknowledged evidence and at most the current host's
  uncheckpointed work.
- No shard is planned above 70% of its runtime budget at the conservative rate.
- A campaign is never presented as clean while required coverage is partial.
- No packet is emitted after cancellation has been acknowledged or the hard rate
  grant/policy epoch has expired.

## 10. Immediate operating guidance before implementation

1. Use Normal/standard for the broad `/24` campaign. It is not “less real”; it is
   the high-value first pass and aligns with common-port evidence from Nmap.
2. Use full-port coverage only for explicitly selected high-value or unusual
   live assets.
3. Until automatic sharding exists, **three live hosts per full/deep job** is only
   a conditional starting bound at the observed 150 pps: first confirm the actual
   raw-SYN method, hard aggregate rate, retry contract, cancellation, and remaining
   stage budget. If the hardened deployment uses connect fallback, use smaller
   batches or do not run exhaustive coverage until it is benchmarked.
4. Do not raise the job ceiling to 31–92 hours. That increases the failure,
   cancellation, and result-loss window without fixing checkpointing.
5. Do not raise pps merely to satisfy the equation. First verify authorization,
   target fragility, source capacity, raw SYN capability, measured loss, and the
   site-wide aggregate budget.
6. Capture job `250e6892`'s serialized parameters and deployed build/image identity
   before redeploying; it is the evidence needed to explain why the guard saw 150
   rather than the UI's 600 pps.

## 11. Definition of done

The large-subnet solution is complete when:

- Contract-v2 Aggressive changes pace only; full coverage is a separate explicit
  choice, while legacy-v1 behavior is explicitly versioned and deprecated.
- A `/24` exhaustive request returns a safe campaign plan instead of one
  impossible monolithic job.
- A globally infeasible `/16` plan is rejected or narrowed even though it is
  technically shardable.
- Every shard has deterministic, disjoint, in-scope membership and a deadline
  with reserve.
- Manager and probe agree on the effective rate, retry policy, scanner method,
  build version, and plan digest.
- Site-wide and per-destination hard rate limits hold under concurrency.
- Cancellation, lease loss, deadline expiry, and policy revocation stop packet
  egress before acknowledgement.
- Every completed host is checkpointed and can be uploaded idempotently.
- Probe/Manager restarts resume only residual logical work without duplicate
  facts across attempts.
- Partial, silent, excluded, and failed coverage are visible and never rendered
  as clean.
- Coverage is dimensional enough to prove the relevant asset, vantage, protocol,
  port set, scanner/rule, and confidence policy.
- Detection can surface positive findings early but only performs negative
  conclusions after coverage finalization under one pinned detector/database
  bundle.
- A zero-fact result and a failed detector both reach explicit durable states.
- A synthetic `/16` can be planned and executed as bounded work without one giant
  in-memory job or final-only payload.

## Sources

All external sources below are primary research papers, official project
documentation/source, standards, or first-party platform documentation.

- **[ZMAP-2013]** Zakir Durumeric, Eric Wustrow, and J. Alex Halderman,
  “ZMap: Fast Internet-Wide Scanning and its Security Applications,” USENIX
  Security 2013. https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_durumeric.pdf
- **[ZMAP-2024]** Zakir Durumeric, David Adrian, Phillip Stephens, Eric Wustrow,
  and J. Alex Halderman, “Ten Years of ZMap,” ACM IMC 2024.
  https://web.stanford.edu/class/cs244/papers/ten-years-zmap.pdf
- **[ZMAP-README]** ZMap official repository and current architecture/ethics
  guidance. https://github.com/zmap/zmap/blob/main/README.md
- **[ZMAP-MANPAGE]** ZMap official man page: target-pair rate, seed, probes,
  shard count/index, allow/block lists, and metadata.
  https://github.com/zmap/zmap/blob/main/src/zmap.1
- **[ZGRAB]** ZGrab2 official repository: ZMap L4 discovery followed by stateful
  L7 handshakes. https://github.com/zmap/zgrab2
- **[CENSYS]** Zakir Durumeric et al., “A Search Engine Backed by Internet-Wide
  Scanning,” ACM CCS 2015. https://zakird.com/papers/censys.pdf
- **[LIVENESS]** Shehar Bano et al., “Scanning the Internet for Liveness,” ACM
  SIGCOMM CCR 2018. https://discovery.ucl.ac.uk/id/eprint/10048442/
- **[MASSCAN-DESIGN]** Masscan official repository design: asynchronous
  send/receive, permutation, sharding, rate, and resume.
  https://github.com/robertdavidgraham/masscan/blob/master/README.md
- **[MASSCAN-MANPAGE]** Masscan official man page: non-overlapping shard and
  resume-index semantics.
  https://github.com/robertdavidgraham/masscan/blob/master/doc/masscan.8.markdown
- **[NMAP-DISCOVERY]** Nmap official host-discovery documentation.
  https://nmap.org/book/man-host-discovery.html
- **[NMAP-PN]** Nmap official discussion of scanning every address versus host
  discovery. https://nmap.org/book/host-discovery-controls.html
- **[NMAP-TIMING]** Nmap official timing, rate, retry, and timeout documentation.
  https://nmap.org/book/man-performance.html
- **[NMAP-PORTS]** Nmap official port specification and default common-port set.
  https://nmap.org/book/man-port-specification.html
- **[NMAP-PORT-SELECTION]** Nmap's empirical port-selection effectiveness data.
  https://nmap.org/book/performance-port-selection.html
- **[NMAP-TARGETS]** Nmap official target and exclusion documentation.
  https://nmap.org/book/man-target-specification.html
- **[NIST-800-115]** NIST SP 800-115, “Technical Guide to Information Security
  Testing and Assessment.” https://doi.org/10.6028/NIST.SP.800-115
- **[RFC-1262]** IAB, “Guidelines for Internet Measurement Activities.”
  https://www.rfc-editor.org/rfc/rfc1262
- **[RFC-2914]** IETF BCP 41, “Congestion Control Principles.”
  https://www.rfc-editor.org/info/rfc2914/
- **[MAPREDUCE]** Jeffrey Dean and Sanjay Ghemawat, “MapReduce: Simplified Data
  Processing on Large Clusters,” OSDI 2004.
  https://research.google.com/archive/mapreduce-osdi04.pdf
- **[AWS-IDEMPOTENCY]** Amazon Builders' Library, “Making retries safe with
  idempotent APIs.”
  https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- **[CLOUD-TASKS]** Google Cloud Tasks first-party delivery semantics.
  https://docs.cloud.google.com/tasks/docs/dual-overview

[ZMAP-2013]: https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_durumeric.pdf
[ZMAP-2024]: https://web.stanford.edu/class/cs244/papers/ten-years-zmap.pdf
[ZMAP-README]: https://github.com/zmap/zmap/blob/main/README.md
[ZMAP-MANPAGE]: https://github.com/zmap/zmap/blob/main/src/zmap.1
[ZGRAB]: https://github.com/zmap/zgrab2
[CENSYS]: https://zakird.com/papers/censys.pdf
[LIVENESS]: https://discovery.ucl.ac.uk/id/eprint/10048442/
[MASSCAN-DESIGN]: https://github.com/robertdavidgraham/masscan/blob/master/README.md
[MASSCAN-MANPAGE]: https://github.com/robertdavidgraham/masscan/blob/master/doc/masscan.8.markdown
[NMAP-DISCOVERY]: https://nmap.org/book/man-host-discovery.html
[NMAP-PN]: https://nmap.org/book/host-discovery-controls.html
[NMAP-TIMING]: https://nmap.org/book/man-performance.html
[NMAP-PORTS]: https://nmap.org/book/man-port-specification.html
[NMAP-PORT-SELECTION]: https://nmap.org/book/performance-port-selection.html
[NMAP-TARGETS]: https://nmap.org/book/man-target-specification.html
[NIST-800-115]: https://doi.org/10.6028/NIST.SP.800-115
[RFC-1262]: https://www.rfc-editor.org/rfc/rfc1262
[RFC-2914]: https://www.rfc-editor.org/info/rfc2914/
[MAPREDUCE]: https://research.google.com/archive/mapreduce-osdi04.pdf
[AWS-IDEMPOTENCY]: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
[CLOUD-TASKS]: https://docs.cloud.google.com/tasks/docs/dual-overview
