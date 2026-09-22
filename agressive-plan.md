# Aggressive Scan & Queue — Investigation, Fixes, and Remaining Work

**Status as of 2026-09-22.** Probe suite **2372 passed / 0 failed**. Manager suite
**1272 passed / 4 skipped / 0 failed**. Frontend **221 passed**, `tsc` clean.
Nothing committed — all work is uncommitted on `main`.

**Second pass (2026-09-22, later). Everything that can be done without
hardware is done.** P4, P7 and P2/D1 shipped; P3, P5 and P6 are closed with
reasoning. **P1 is the sole remaining item** and needs a Linux probe host with
`NET_RAW` plus an authorized target network — see §8 for a verified
one-command repro.

Two findings that change how the rest of this document should be read:

1. **The launcher no longer sends a probe envelope**, so `deep` finally runs at
   the 150 pps / 4.0 s it was tuned for. Knock-on: at 150 pps its conntrack
   demand falls from 72,000 entries to **18,000**, under the 65,536 default.
   Three of the four kernel warnings "aggressive" used to raise now clear on an
   untuned host. **Every capacity figure in §4.1 assumed 600 pps — re-derive
   before using.**

2. **D1 (the SYN scanner's serialized send/recv) is real, was measured at ~92%
   reply loss on a wide sweep, and is fixed.** It alone explains *"aggressive
   returns no results."* It also turned out to be verifiable after all — by
   faking the kernel rather than the scanner. See §7 P2.

§6 carries the corrections; several first-pass numbers did not survive a second
reading.

This document is a handoff. It records what was wrong, what was fixed and why,
what is still open and how to approach it, and — importantly — **which of the
original conclusions turned out to be wrong**, so the next person does not
re-derive bad numbers from the first analysis.

---

## 1. The original report

Two symptoms, from the operator:

1. **Aggressive scans return no results, or break mid-operation.** Stealth and
   normal work fine.
2. **The queue does not work.** "When I send a job it should finish first, then
   move to the next job" — instead a second job breaks.

Plus a requirement: **"I want ALL data"** for a 1000-host × 65,535-port scan.

---

## 2. How a scan actually executes

Read this before changing anything in the pipeline.

### 2.1 The three knobs

| Knob | File | Meaning |
|---|---|---|
| `mode` | `probe/workflow/modes.py` | HOW FAR the funnel runs (the stage ceiling) |
| `profile` | `it` / `iot` / `ot` | WHICH ports and deep branches are in play |
| `intensity` | `probe/workflow/intensity.py` | HOW HARD each stage probes |

`intensity` is `light` / `standard` / `deep`. The UI's
`stealth` / `normal` / `aggressive` are **aliases**, mapped in
`manager/backend/app/routers/agents.py` (`_INTENSITY_ALIASES`).

### 2.2 The pipeline

`run_engagement()` — `probe/workflow/workflow_engine.py`. Stages are **hard
barriers**: every host clears stage N before any host enters N+1.

```
Gate 0   passive (OT only) ─────────────── hard stop
Gate 1b  ipv6_discovery      ICMPv6 ND multicast
Gate 2   host_discovery      fan-out: concurrency        (intentionally wide)
Gate 3   port_scan PASS 1    fan-out: host_concurrency
Gate 4b  os_fingerprint      fan-out: host_concurrency   (was: concurrency — fixed)
Gate 4   service_banner      fan-out: host_concurrency   (was: sequential — fixed)
Gate 5   deep branches       fan-out: host_concurrency
Gate 3b  port_scan TAIL      the remaining ~64,500 ports
Gate 5b  re-banner + re-branch hosts the tail opened
Gate 6   credentialed (ssh/win)  still SEQUENTIAL
```

`host_concurrency = max(1, min(8, concurrency))`, env override
`PROBE_HOST_CONCURRENCY`.

### 2.3 Scanner inventory

| Scanner | File | How packets go out |
|---|---|---|
| `host_discovery` | `host_discovery.py` | ICMP + ARP (L2) + TCP connect fallback |
| `ipv6_discovery` | `ipv6_discovery.py` | ICMPv6 ND all-nodes multicast |
| `port_scan` | `port_scanner.py` | `asyncio.open_connection` full handshake; worker pool drains a queue; AIMD window + adaptive RTO |
| `syn_scan` | `syn_scanner.py` | Raw `SOCK_RAW`/`IPPROTO_TCP`, crafted SYN, epoll recv. **Falls back to connect off privileged Linux** |
| `udp_scan` | `udp_scanner.py` | Protocol-specific datagram payloads + generic probe |
| `os_fingerprint` | `os_fingerprint.py` | ICMP echo + SMB2 negotiate + SYN/ACK stack hints |
| `service_banner` | `service_banner.py` | Connect + protocol greeting, TLS rung, ~60 patterns |
| tls / web / smb / smb_enum / db / ldap / snmp / ftp / smtp / ssh / rdp / vnc / nfs / rsync / msrpc / ipmi / printer / iot / mobile / mcp_ai / dns | `*_scanner.py` | Connect + protocol handshake, one per branch, wired via `branches.py` |
| `ssh_collector` / `windows_collector` | — | Authenticated (paramiko / impacket) |

**Packet send mechanics** (`PortScanner.scan_target`):

```
Queue(all ports) → N workers (N = min(concurrency, len(ports)))
  each worker:
    deadline check (BEFORE dequeue)
    limiter.wait()            ← shared per SCANNER INSTANCE, not per host
    async with self.sem       ← Semaphore(concurrency)
    open_connection(timeout = AdaptiveTimeout SRTT+4·RTTVAR)
    classify: open / closed(RST) / filtered(silence)
  → cleanup pass: _reprobe_ambiguous()
  → emit scan_summary (completeness, congestion, tarpit, budget_exhausted, port_states)
```

**Critical property:** `rate` and `concurrency` live on the *scanner instance*,
and one instance serves **every host in the stage**. So `rate` is the aggregate
for the stage, not a per-host allowance. Doubling hosts doubles wall clock.

---

## 3. What "Aggressive" actually resolves to

```
UI "Aggressive"
  → manager/frontend/lib/scan-launch.ts:16
        params.rate=600, concurrency=300, timeout=2.0, disc_timeout=1.0
        params.intensity="aggressive"
  → manager/backend/app/routers/agents.py  _INTENSITY_ALIASES: aggressive → "deep" → code 3
  → probe/workflow/intensity.py            deep preset
  → probe/agent/engine.py:264-268          _clamp() — explicit params WIN over the preset
```

**The collision:** the frontend *unconditionally* sets rate/concurrency/timeout,
so the `deep` preset's own tuning is **always discarded**. The fields it does
not send survive.

| Knob | deep preset | UI override | **Effective** |
|---|---|---|---|
| rate | 150 | **600** | 600 pps |
| concurrency | 80 | **300** | 300 |
| timeout | 4.0 | **2.0** | 2.0 s |
| disc_timeout | 2.0 | **1.0** | 1.0 s |
| `port_profile` | `full` | — | **65,535 ports** |
| `retries` | 2 | — | 2 (→ 3 probes on silence) |
| `max_host_seconds` | 1800 | — | 30 min/host |
| `first_pass_profile` | top1000 | — | two-phase |

You get `deep`'s **breadth** with an envelope 4× more aggressive and
2× shorter-timeout than the preset was tuned for. The preset's 150 pps / 4.0 s
was chosen *because* of the 65k breadth.

> **FIXED — see P4 below.** The launcher now sends `intensity` and nothing
> else. Two corrections to the analysis above: the override also clobbered an
> *explicit* operator `params.rate` (the preset was applied after the spread),
> and the collision ran in **both** directions — `light` never once ran its
> declared 800 pps either.

**This also inverts recall.** Zippier ZMap measured hit rate falling to 68% of
the gigabit baseline at line rate. The codebase records the same effect locally
(`port_scanner.py` comment): 69 ports read `filtered` at rate 300/conc 200, all
69 resolved `closed` when re-probed at rate 40. **Aggressive was a
lower-accuracy mode, not just a faster one.**

> **Still open.** This collision is NOT fixed. See pending task **P4**.

---

## 4. The 1000 × 65,535 physics

Three numbers eliminate most of the option space.

**1. Bandwidth is irrelevant.** 65.5M SYNs × ~60 B = 3.9 GB. At 1 Gbps that is
31 seconds of wire time. The constraint is **packet rate and kernel state**.

**2. Total time depends only on aggregate rate.**

| Aggregate rate | Time for 65.5M probes |
|---|---|
| 600 pps *(today)* | **30.3 hours** |
| 5,000 pps | 3.6 h |
| **20,000 pps** | **55 min** |
| 1.44 Mpps *(ZMap, gigabit)* | 45 s |

**3. `connect()` cannot reach any of those rates — arithmetic, not tuning.**

Every `connect()` burns an ephemeral port held in `TIME_WAIT` for 60 s. Default
range is 28,232 ports:

```
max sustainable connect rate = 28,232 / 60 = 470 conn/sec
65.5M / 470 = 38.7 hours
```

Even with `tcp_tw_reuse` and the full 1024–65535 range: 1,075/sec → **16.9 h**.
Add Docker bridge NAT (one conntrack entry each, 120 s SYN_SENT timeout) and
`nf_conntrack_max` overflows at ~550 pps.

> **Hard conclusion:** 1000 × 65,535 is only possible over **raw SYN**. Without
> `NET_RAW` the job must be *refused at admission*, not attempted.

### 4.1 Kernel limits that masquerade as `filtered`

The errno map (`scanner_base.py` `_ERRNO_MAP`) is genuinely good — `EMFILE` /
`ENOBUFS` / `EADDRNOTAVAIL` map to `local_resource_error`, never `filtered`,
and set `degraded`. But it only catches failures the kernel *reports*. These
cause a **silent packet drop**:

| Kernel limit | Default | Aggressive demand (600 pps) | Visible? |
|---|---|---|---|
| `nf_conntrack_max` (Docker **bridge = NAT**) | 65,536 | 600 × 120 s = **72,000** | ❌ silent → false `filtered` |
| `ip_local_port_range` | 28,232 | 600/s × 60 s = **36,000** | ✅ `EADDRNOTAVAIL` |
| `neigh.default.gc_thresh3` | **1,024** | **1000 hosts on flat L2** | ❌ silent → false `filtered` |
| `pids_limit` (probe/docker-compose.yml) | **256** | thread pool for blocking scanners | partial |

**`gc_thresh3` = 1024 is a direct hit on the 1000-host case.**

`probe/docker-compose.yml` ships `cap_drop: [ALL]` + bridge + `pids_limit: 256`,
so **SYN is unavailable by default** and every probe goes through conntrack.

### 4.2 Research grounding

- **ZMap** (Durumeric et al., USENIX Sec '13) — stateless; no per-connection
  state; send path decoupled from receive path.
- **Zippier ZMap** (Adrian et al., WOOT '14) — sharding via multiplicative-group
  permutation; shards derivable without coordination. Also quantifies the cost
  of speed: hit rate → 68% at 14 Mpps.
- **Censys** (SIGCOMM '25) — production shape: continuous stateless L4 discovery
  at **varying rates per port and per network**, feeding a *separate* L7 tier.
  Rate is a property of the **target network**, not a global operator slider.

### 4.3 Chosen approach for 1000 hosts: windowed sharding

Three options were evaluated.

**Option A — host-serial (the operator's instinct).** One host, all ports,
commit, next. To finish in 2 h needs 9,100 pps *aimed at one host at a time* —
a SYN flood. Accuracy collapses. **Right delivery model, wrong probe ordering.**

**Option B — pure ZMap full permutation.** Best accuracy, but no host completes
until the end, so there is nothing to commit incrementally.

**Option C — windowed sharding (recommended).** Take W hosts, permute all
(host, port) pairs *within* the window, scan at aggregate rate R. When the
window closes, all W hosts are complete → commit → evict → next window.

```
T_total       = (N_hosts × N_ports) / R     ← depends on R only, NOT on W
per-host rate = R / W                        ← politeness knob
window time   = W × N_ports / R              ← commit cadence
memory        = W × bytes_per_host           ← bounded
```

**R and W are orthogonal.** At R = 20,000 pps → **55 minutes regardless of W**:

| W | per-host rate | window duration | commits |
|---|---|---|---|
| 32 | 625 pps | 105 s | 32 |
| **64** | **312 pps** | **3.5 min** | **16** |
| 128 | 156 pps | 7 min | 8 |

Compare like-for-like: at equal politeness (312 pps/host), host-serial takes
**58 hours**. At equal duration, host-serial slams each host at 20,000 pps.

> **Caveat added later:** after the fixes below landed, windowing's rationale
> weakened considerably. See pending task **P3**.

### 4.4 "All data" needs RLE

65.5M probe outcomes as individual rows ≈ **52 GB**. Not viable.

| | rows | raw | gzipped |
|---|---|---|---|
| naive | 65.5M | 52 GB | ~5 GB |
| **RLE** | ~70k | **56 MB** | **~6 MB** |

This is **implemented** — see completed task C-F1.

---

## 5. Completed work

19 tasks. 21 new test files, 264 new tests. 2 migrations.

### Track A — Instrumentation (make the truth visible)

**A1 — Kernel preflight.** `probe/agent/kernel_limits.py` (new), 31 tests.
Reads conntrack / ephemeral range / `gc_thresh3` / `RLIMIT_NOFILE` /
`syn_scan_supported()`; classifies each against a scan envelope. Logged at
startup (`agent.py`, beside `Capabilities:`). Follows `doctor.py`'s pattern:
pure classifiers returning `Check(name, status, detail, remediation)` + separate
IO wiring. **Advisory only** — every check returns `pass` or `warn`, never
`fail`, so `doctor`'s exit code cannot flip because a host is under-tuned.

Reproduces the reported symptom: stealth and normal come back clean; aggressive
warns on **all four** limits.

**A2 — Feasibility calculator.** `probe/agent/feasibility.py` (new), 21 tests.
`estimate(hosts, ports, rate, ceiling)` → floor / retry / reprobe seconds,
`reachable_hosts`, `required_rate`, verdict (`fits` / `tight` / `cannot_finish`).
Wired into `engine.py` at job start.

The model is deliberately a **floor** — port stage only, one probe per port,
ignoring retries, cleanup and every later stage. If even the floor does not fit,
nothing downstream rescues the job.

`port_count_for()` delegates to `workflow_engine._port_candidates` rather than
re-deriving the catalog; a test asserts they agree.

On the reported case: `1022 hosts × 65535 = 66,976,770 probes at 600 pps →
floor 31.0h vs ceiling 2.0h [cannot_finish]`, `~65 of 1022 hosts fit`.

**A3 — Timing in `run_stats`.** `stage_timings()` in `workflow/execution.py:419`;
`feasibility.as_run_stats()`; `run_stats["timing"]` built on **all three** exit
paths (success, deadline, crash). Payload size logged in `transport.submit_result`
(measured where it is already serialized — free, and the true wire size).

Revealed: the port-stage model is accurate to **12%**; for *narrow* sweeps the
datagram branches (snmp 18 s + udp 9 s + ipmi 3 s) dominate, not the port scan.

### Track B — Data loss

**B1 — Partial scope rejection.** *The most likely cause of "no results at all".*

`validate_result_scope` was all-or-nothing: one unparseable target anywhere
returned 422 + `permanent_rejection`, and the probe treats 422 as terminal and
**quarantines the whole payload**. Probability scales with host count, so the
widest and most expensive scans were likeliest to lose everything.

Added `_authorizer()` (one shared predicate), `partition_result_scope()`,
`apply_scope_gate()` in `job_result_service.py` (lines 131 / 187 / 244), plus
`create_scope_rejection_finding()` in `finding_translator.py:257` (medium
severity — an authorization-boundary event, not a quality one).

**Not a weakening:** every rejected identity is still dropped; the same rows
never reach the database. `validate_result_scope` is untouched and all 33
pre-existing scope tests pass unmodified. **Fail-closed preserved:** if nothing
survives, still a permanent 422.

Result: 254 of 255 facts ingest, 1 dropped, finding raised.

**B2 — Probe↔manager scope parity.** My original claim was **backwards**. The
manager already refuses hostnames (`validate_scope_entries` requires
`ip_network()` on every write path). The probe was **fail-open**:

```
from_list(["10.0.0.0/244"])  → silently becomes a HOSTNAME, matches nothing
from_list([...], excludes=["10.0.0.5/33"])
                             → exclusion silently DROPPED → the host the
                               operator carved out gets SCANNED
```

The second fails open in the *dangerous* direction. Added `strict=True` to
`ScopeGuard.from_list`, used by the agent path. Lenient default kept —
`from_file` documents hostname support and `test_probe_core.py` pins it.

Contract enforced by a **shared 11-entry corpus** parametrized on both sides
(`probe/tests/test_scope_parity.py`, `manager/.../test_scope_entry_parity.py`),
following the `_USE_CASE_CODES` precedent.

**B3 — 413 → permanent.** 413 was retryable, so an oversized result looped
forever, filled the spool, and `at_capacity` **permanently stopped the probe
claiming any job** while it still heartbeat and looked healthy.

Now `PERMANENT_REJECTION` → quarantined to `<spool>/rejected/` intact (outside
the `*.json` glob, so capacity is genuinely freed). Error reports **both** raw
and wire size, since the manager enforces 32 MB compressed / 128 MB inflated
separately.

```
BEFORE: spool_count=4  at_capacity=True   ← probe stops claiming jobs, forever
AFTER:  spool_count=0  at_capacity=False  ← keeps working, payloads preserved
```

`test_transport.py` deliberately pinned the old behaviour; that test was updated
with a comment explaining why 413 moved.

**B4 — Spool back-pressure + `paused`.** Found a second bug while scoping:
`at_capacity` was checked in **exactly one place**, the HTTP-only poll loop. The
WebSocket path is the **default** and had no capacity gate at all, so a probe
that could not deliver results kept taking on work producing more of them.

Added `_spool_saturated()`, `_heartbeat_status()`, `PAUSED_STATUS` in
`agent.py:890/901`; gated both WS paths; added `AgentStatus.paused`
(migration **0043**).

Adding the label was sufficient to fix dispatch — `push_job` and the enqueue
eligibility query already filter on `online`. `paused` is deliberately **not**
`offline` (an offline probe gets its jobs reaped; a paused one is healthy and
will resume, and reaping would destroy the very results blocking it).

### Track C — Per-host cost

**C1 — Reprobe deadline.** The cleanup pass ran *after* the workers with **no
clock**. On a silent host every port is a candidate: 65,535 × 4 attempts ÷
40 pps = **6,554 s** — 91% of the 2 h job ceiling, for ONE host, while
`max_host_seconds=1800` sat there doing nothing.

`_reprobe_ambiguous` (`port_scanner.py:755`) now takes `deadline`, drains a
**queue** (matching `scan_target`'s own worker pool — the old
`gather(*(_one(p) for p in ports))` allocated a coroutine per candidate), and
returns stats.

**Semantic distinction that drove the design:**

| | meaning | verdict |
|---|---|---|
| main sweep truncated | never probed | `not_scanned` |
| cleanup truncated | probed, silent, no second look | `filtered` |

Skipped ports keep `filtered`; what is lost is a *confidence upgrade*, not an
observation. Test suite 37.7 s → 1.0 s.

**C2 — Candidate cap.** `reprobe_max_candidates` (default 2048, 0 disables).
`_select_reprobe_candidates` (`port_scanner.py:737`) prioritises `top1000`, since
a false `filtered` matters most on a service port. `capped` and `skipped` are
reported **separately** — different fixes (raise the cap vs raise the budget).

```
20,000 ambiguous ports on a silent host:  48.4s → 6.0s  (capped=17952)
```

A standard assessment sweeps ~1,193 ports, so the cap can never engage there.

**C3 — Cache eviction: CLOSED, NOT BUILT.** Premised on "4.3 GB at 1000 hosts",
which I **measured and disproved**: ~60 KB per realistic 25-open-port host →
~60 MB at 1000 hosts. The 4.3 MB/host figure came from the *pre-fix* era before
`_retain_result` stopped holding every closed port. Eviction would also risk the
final result, which is still built from the whole cache.

**C4 — Cache host index.** `_commit_host` linear-scanned the whole cache **per
host** → O(N²), `await`ed on the event loop, stalling every other host's scan.

```
        BEFORE              AFTER
  50 hosts  0.4 ms/host   0.23 ms/host
1000 hosts  5.0 ms/host   0.24 ms/host
      total    4.98 s        0.24 s
```

Added `_by_host` index in `cache.py:119`; every write routed through one
`_index()` helper (`_load()` bypassing it was the obvious way to get an empty
index — there is a test).

### Queue, durability, admission

**D1/D2 — the reported queue bug.** *This is symptom #2.*

```
poll_fallback:  check state (free) ──► await poll_jobs ─────► job_lock ──► run
main loop:                  job_push arrives ──► stage (state STILL free) ──► claim
```

Both claims succeed. `job_lock` serialises *execution*, but job 2's **300 s
lease started at claim time**, and nothing renews a job that is not running.
Behind a 2 h scan the lease expires, the reaper requeues, and after
`max_attempts` the job lands in `failed` with *"maximum execution attempts
exhausted"* — **having never executed a single probe.**

Fix: **reserve before yielding.** `claiming` flag set ahead of the await, held
across poll AND run, released in one `finally`. `_ws_probe_is_free()`
(`agent.py:1113`) is the single definition used by both claimers.

**D2:** `pending_job` was cleared *only* by a matching `job_claim`. If one never
arrived, the probe went **permanently deaf**. `WS_OFFER_TTL_SECONDS = 30`
(`agent.py:882`) + `_ws_expire_stale_offer()` (`agent.py:1093`).

**T1.4 — Stage-boundary commits.** `_commit_host` ran only at the END of the
deep stage. A job whose ceiling stops earlier — `discovery`, `port_scan`,
`service_fingerprint`, i.e. **most jobs** — committed **nothing, ever**.

Required a modelling change first: `committed_hosts()` feeds RESUME, and a chunk
used to mean "this host finished". Committing partial evidence without saying so
would make a retry **skip hosts it had merely discovered**. Migration **0042**
adds `scan_result_chunks.complete`, defaulting and backfilling `TRUE` so an
older probe is unchanged.

`_commit_stage()` / `_at_ceiling()` in `workflow_engine.py:503/457`, fan-out 8.

```
host_discovery -> [(host, True,  1)]
port_scan      -> [(host, False, 1), (host, True, 5)]
service_banner -> [(host, False, 1), (host, False, 5), (host, True, 7)]
```

A host that never answered is **never** marked complete — liveness is classified
`uncertain` on purpose, so a retry must be free to re-check it.

**T1.5 — Lease patience.** My original framing was wrong in **direction**. The
manager's lease gives 10 heartbeats of headroom; the real defect is that the
**probe abandons work the manager is still holding**:

| path | probe gives up at | lease holds | |
|---|---|---|---|
| WS push / HTTP (hb 30 s) | 90 s | 300 s | 3.3× impatient |
| WS poll-fallback (hb 10 s) | **30 s** | 300 s | **10× impatient** |

A 35 s blip threw away a 2 h scan and burned one of three attempts. The claim
already carried `lease_expires_at`; the probe never read it.
`_lease_deadline` / `_should_abandon_lease` (`agent.py:734/771`). Monotonic
clock, not wall-clock — an NTP step is exactly the event that also causes
heartbeat failures. 409 stays immediate; older managers keep count-based grace.

**H1 — Infeasible-job refusal.** `_refuse_if_infeasible` (`engine.py:256`),
wired at `engine.py:1003`.

```
refused in 0.01s (was: a 2-hour wait for a partial that explained nothing)

error:  job cannot finish: 1022 host(s) x 65535 port(s) = 66,976,770 probes
        at 600 pps needs at least 31.0h, against a 2.0h ceiling
remedy: ~65 host(s) fit at this port breadth, or keep every host and narrow the
        port profile. Finishing as configured needs ~9,302 pps...
        Set allow_infeasible=true to run it anyway and accept a partial.
```

Fires **only** on `cannot_finish`. `tight` still runs. A refused job goes
straight to `failed` — terminal, never requeued, so it does not burn attempts.

### Track F — "All data"

**F1/F3 — RLE port states.** `_retain_result` keeps only OPEN ports; everything
else was a counter. "Was 8443 closed or filtered?" was unanswerable.

Keeping every observation cost 47 MB/host (4.7 GB at 100 hosts, OS-killed). But
what is needed is the **state per port**, not an object per port: a **byte per
port** is 64 KB for the whole TCP space, ~1,000× cheaper, and states cluster so
RLE collapses it.

`_port_state` bytearray + `note_state()` + `state_ranges()`
(`port_scanner.py:282/288`); surfaced as `port_states` in the scan summary.
**65,535 ports reconstruct exactly from under 20 range entries.** Ports requested
but never observed come back as `not_scanned`, never folded into `filtered`.

**F2 — Port-state query.** `manager/backend/app/services/port_coverage.py` (new)
+ `GET /engagements/{id}/port-coverage?host=&port=`
(`engagements.py:1250`). **No migration, no probe change** — the data was already
persisted inside `scan_results.facts`.

```
port 22    -> open        port 20010 -> filtered
port 9000  -> closed      port 40000 -> not_scanned
                          port 70000 -> unknown
probed 20,050 of 65,535 ports (31%)
```

The `scan_summary` is extracted **in SQL** — loading a whole submission to read
one object is what `raw-facts` had to be rewritten to stop doing (~107 KB/host).

### Unplanned — found while working

**RateLimiter.** Slept **while holding its own lock**. Measured (not assumed):
not a collapse, a consistent undershoot growing with rate.

| configured | before | after |
|---|---|---|
| 500/s | 435 (87%) | 500 |
| 5000/s | 3972 (79%) | 4996 |

Matters because **every ETA is computed from the configured rate**, including
A2's estimate. Fix claims a slot under the lock and sleeps outside it
(`scanner_base.py:462`). A source-level test guards the `await` coming back.

**Banner stage was fully sequential** (`workflow_engine.py:759`). 64 hosts:
**3.2 s → 0.42 s**. Bounded by `host_concurrency` — a banner grab opens a socket
per open port, so unbounded would be the widest burst in the pipeline.

**Stage fan-out policy.** `os_fingerprint` fanned out to `concurrency` (up to
500) while making **three** `run_in_executor(None, ...)` calls per host on the
default pool (`min(32, cpu+4)` = 14 threads here) → ~1,500 blocking tasks
against ~14 workers. That saturation is already documented in `_recheck_alive`:
*"one beat got through, then nothing."* Now `host_concurrency`
(`workflow_engine.py:745`). `host_discovery` is the one deliberate exception.

**e2e tests un-redded.** `test_e2e_engagement_to_findings.py` targeted
`127.0.0.1`; the permanent denylist (landed 2026-09-12, tests written
2026-08-15) correctly refuses loopback. Retargeted to the host's own
non-loopback IPv4 — **the fix was to test against an address the probe may
legitimately scan, not to weaken the gate.**

---

## 6. Corrections to the original analysis

**Read this before trusting any number from the first pass.**

| Claim | Reality |
|---|---|
| "Cache grows to 4.3 GB at 1000 hosts" | **~60 MB.** ~60 KB/host measured. C3 closed, not built |
| "Three network blips fail a 2 h scan" | Backwards. The **probe** quits at 30 s against a 300 s lease |
| "Manager too strict about hostname scope" | Backwards. Manager is correct; the **probe** was fail-open |
| "`scan_metrics` bypasses the scope gate" | **Not real.** `summary()` carries `vantage`, no target — nothing to launder |
| "Lock handoff dominates rate-limiter throughput" | Real but small: 79–87% of configured, not a collapse |
| "One filtered host exceeds the 2 h ceiling" | 6,554 s = **91%** of it. *Two* such hosts exceed it |
| "100 hosts × 65,535 @ 2000 pps is `tight`" | It **fits** (3,277 s). 150 hosts is the boundary |
| "`it` profile catalog is ~100 ports" | **125 ports** |

Added by the second pass:

| Claim | Reality |
|---|---|
| "The launcher discards the preset; explicit params survive" | It discarded **both** — the preset was applied after the params spread |
| "The collision only hurts aggressive" | `light` was the worse end: 800 pps / timeout 1.0 / retries 0, past the measured false-`filtered` point |
| "`light` is the fast triage preset" | Its envelope **never ran once.** The UI, its only caller, always overrode all four values |
| "`scan_metrics` orphaning is cosmetic" | It can flip `scan_health_summary` to `degraded` and raise a coverage finding from discarded evidence |
| "Refuse deep below the sysctl floor" | Too broad. `gc_thresh3` is **flat-L2-only**, so refusing a routed sweep would be a false refusal — conntrack is the only unconditional one |
| "Aggressive needs 72,000 conntrack entries" | 72,000 was the *override's* 600 pps. At the preset's 150 pps it is **18,000** — it fits |
| "`SO_RCVBUF` 4 MB ≈ 40,000 packets" | **~5,000.** Linux charges `skb->truesize` (~768 B/segment), not payload bytes |
| "The SYN engine is unverifiable on macOS" | Only the packet BYTES are. The loop structure is testable by faking the *kernel*, which is where D1 lived |
| "D3: colliding source ports read each other's replies" | **Already defended twice** — `ip_src` filter plus a cookie keyed on `dst_ip` |
| "D4: no cooldown after the last send" | **There is one.** The recv deadline is set after the send loop, adaptive to 8 s |

---

## 7. Pending work

### P1 — A4: lab repro **(STILL BLOCKED: needs hardware + an authorized scope)**

**The only remaining action, and it still gates the rest.** It cannot be done
from a dev Mac: it needs a Linux probe host with `NET_RAW` and a target network
the operator is authorized to scan.

Two things make it cheaper than when this was written. The ceilings now come
back **inside the result** (`run_stats["kernel"]`), so nothing has to be
scraped from the probe's stdout; and the envelope under test is finally the one
the preset declares rather than the launcher's override.

Run it with the command in §8 ("P1 lab repro"), which is verified end-to-end
and prints all three answers. Then read:

```
run_stats.kernel.checks        # the ceilings this scan actually ran under
run_stats.kernel.blocking      # non-empty = the run was refused, see T2.4
run_stats.timing.stages        # where the time actually went
run_stats.timing.estimate      # predicted vs actual
```

**What the answers decide:**

- `SYN scan: **no**` → 1000 × 65,535 is a **scoping decision**, not an
  engineering project. Tracks D/E should not be built. H1 already refuses in
  0.01 s with the remedy.
- `SYN scan: **yes**` → Track D is worth building.
- Port stage dominates `stages` → Track D/E.
- Datagram branches dominate → a **different** fix entirely (UDP timeout
  strategy, not the SYN engine).

### P2 — Track D: SYN engine **(D1 FIXED; D2 deferred; D3/D4 were not real)**

Re-read the scanner line by line rather than trusting the first pass. Three of
the five entries below changed.

| | Defect | Status |
|---|---|---|
| D1 | Send and receive serialized per round | **FIXED** — see below |
| D2 | One raw recv socket per host, no BPF filter | **Deferred.** Real, but genuinely unverifiable here |
| D3 | Source-port collisions across a window | **Not a correctness bug.** Already defended twice over |
| D4 | No cooldown after last send | **Already present.** The claim was wrong |
| D5 | Window-level pacer | **Dies with P3** (see below) |

**D1 — fixed, and it is almost certainly the reported symptom.**

Each round sent the whole cohort before reading the socket even once, so every
reply the send phase provoked had to wait in `SO_RCVBUF`.

The original estimate of the ceiling was too generous. `SO_RCVBUF` is 4 MB, but
Linux charges **`skb->truesize`** — roughly 768 B for a 40-byte TCP segment,
not 40 — so the buffer holds on the order of **5,000 packets, not 40,000**. A
65,535-port sweep of a mostly-closed host answers with 65,535 RSTs. About 92%
of them are discarded by the kernel **with no error**, leaving ports that
answered reported as `filtered`.

It is also **rate-independent**: the overflow is set by how many ports are in
the round, not how fast they leave, so neither pacing nor P4's slower envelope
helps. And `deep` is exactly the configuration that routes the port stage here
(65,535 ports > the 1,024 connect/SYN threshold). *"Aggressive returns no
results"* is fully explained by this alone.

Fix: `_drain_ready()` consumes whatever is queued after each send, bounded at
64 packets per call so a fast responder cannot starve the send loop. The reply
handling moved into `_accept_reply()` and is now shared by the interleaved
drain and the existing post-send window.

**It IS verified, contrary to the earlier assessment.** What was blocked was
never the loop — it was the packet bytes. `tests/test_syn_recv_interleave.py`
replaces the *kernel* rather than the scanner: a fake receive queue with a
bounded, silently-dropping capacity, driving the real `_syn_scan_blocking`.
Before the fix it reproduced the defect precisely (**3,850 replies dropped, and
open port 9100 reported `filtered`**); after, zero drops at capacity 1.
`build_syn_packet` / `parse_packet` are untouched, so nothing byte-level
changed.

**D2 — deferred, deliberately.** `SOCK_RAW/IPPROTO_TCP` receives every TCP
packet on the host and filters in Python, so userspace parse load is
H × reply-rate with H hosts in flight. Both fixes (an `SO_ATTACH_FILTER` BPF
program, or `connect()`ing the raw socket so the kernel filters by peer) are
Linux-specific, and their failure mode is the worst possible one: receive
nothing, report everything `filtered`. That needs a Linux box with `NET_RAW`,
not a fake. **This is a throughput problem, not a correctness one** — the three
validation filters in `_accept_reply` already reject foreign packets.

**D3 — not a correctness bug.** `verify_reply_cookie` recomputes the cookie
from `parsed["ip_src"]`, and `syn_cookie` keys on `dst_ip`. A colliding source
port on a concurrently-scanned host therefore fails the cookie check, on top of
the explicit `ip_src != dst_ip` filter. Two independent defences already. The
cost of a collision is wasted parsing — which is D2.

**D4 — already present.** The receive deadline is computed *after* the send
loop (`deadline = now + max(window, 1.0)`), so the last round already gets a
full post-send window, adaptive up to 8 s. The claim that in-flight replies
were lost does not hold.

**Still needed on Linux + `NET_RAW`:** validate D1 against a host with a known
mix of open/closed/filtered ports, comparing against `nmap` from the same
vantage — `accuracy_gate.py`'s provenance rule requires an *independent*
observer for any accuracy claim. Then decide on D2 with measurements.

### P3 — Track E: windowed sharding **(CLOSED — not built)**

Closed on the same basis C3 was: the premise was measured and did not survive.
Left here rather than deleted so nobody re-derives it from §4.3.

Originally the centrepiece. Its four rationales have largely evaporated:

| Rationale | Status |
|---|---|
| Bounded memory | **Non-issue** — measured ~60 KB/host |
| Progressive commits | **Delivered** by T1.4 stage-boundary commits |
| Per-host load spreading | Port stage already spreads across 8 hosts |
| Resume granularity | Partly covered by `skip_hosts` + `complete` |

The remaining delta is raising the window from 8 to 64 with (host, port)
permutation — and ports are **already** shuffled per host (`randomize`).

**A fifth rationale died with D1.** Windowing's real appeal was capping how many
replies are in flight at once — which is exactly the overflow D1 turned out to
be. Interleaving the drain fixes that at the source, for one host or a hundred,
without a scheduling layer. D5 (the window-level pacer) has nothing left to
pace: `SendPacer` already runs AIMD per host off the observed reply ratio.

Revisit only if P1 shows the port stage dominating *after* D1's fix is measured
on real hardware.

### P4 — The frontend/preset collision **(DONE)**

`buildScanLaunchRequest` now sets `params.intensity` and nothing else
(`manager/frontend/lib/scan-launch.ts`). Aggressive resolves to the `deep`
preset's 150 pps / 4.0 s, as §3 asked.

**Two things the original analysis missed.**

**1. The override also clobbered explicit operator values.** The preset was
applied *after* `{...body.params}`, so someone who deliberately passed
`rate: 40` still got 600. The first RED run failed on `600 !== 40`, which is
how this surfaced.

**2. The collision ran in both directions, and the *quiet* end was worse.**
The UI's three names are rate labels; the probe's presets are breadth+envelope
bundles. Dropping the override naively would have made "Stealth" — chosen
explicitly for "monitored, production, or fragile segments" — run at
**800 pps** instead of 50.

Rather than add a fourth preset, `light` was retuned to the envelope its only
caller had always forced (50 / 20 / 4.0 / 2.0). The evidence for that:

- `light`'s declared 800 pps / concurrency 200 / timeout 1.0 / `retries: 0`
  **never ran a single scan.** The launcher overrode all four on every job,
  nothing in `use_cases.py` defaults to `light`, and no test pinned its
  envelope — only its breadth, budget and first-pass profile.
- It was also the least accurate setting in the table, by a margin this repo
  *measured*: `port_scanner.py:474` records rate 300 / concurrency 200
  producing **69 false `filtered`** on a real LAN host, all 69 of which
  resolved `closed` when re-probed at 40 / 10. 800 / 200 sits well past that.

So in both directions the launcher's numbers were the validated ones and the
preset's were unvalidated. `light` now means light **touch**, not light latency.

**Guard against silent drift.** The dial's pps readout is now display-only — it
no longer *causes* the number it reports, which is exactly when a label rots
unnoticed. `tests/scan-intensity.test.ts` reads `intensity.py` and asserts each
UI figure matches its preset's rate. It was mutation-tested (restoring
`600 pps` fails it with `dial shows 600 pps for aggressive but deep probes at
150`).

**Caveat:** `/scan` is behind authentication, so the dial was verified by test
and type-check, **not** rendered in a browser.

| | rate | conc | timeout | disc | breadth |
|---|---|---|---|---|---|
| Stealth → `light` | 50 | 20 | 4.0 | 2.0 | ~15 ports |
| Normal → `standard` | 200 | 100 | 3.0 | 1.5 | profile catalog |
| Aggressive → `deep` | **150** | **80** | **4.0** | **2.0** | 65,535 |

Aggressive is now the *slowest* preset by rate and the widest by breadth, so
the UI copy was rewritten: "Exhaustive, not fast… probed patiently so silence
means a firewall rather than a rushed probe."

### P5 — H2: enqueue-time refusal **(CLOSED — declined, with reasoning)**

Refusing at click-time rather than ~10 s later when a probe claims the job.
**Not worth it:** H1 already refuses, the job goes straight to `failed` (never
requeued, no attempts burned), and H2 would triplicate the intensity→port
tables, host counting, *and* the estimate arithmetic across two processes that
cannot import each other. Revisit only if operators complain about the delay.

### P6 — H3: per-target-network rate **(CLOSED for now — needs P1 data)**

The Censys model: rate as a property of the target network, not a global slider.
Valuable for multi-subnet estates with differing link capacities. Needs real
multi-segment data to justify.

**Closed rather than left open**, because two of the three things that made it
attractive have been answered elsewhere. Per-host politeness is already handled
(`SendPacer`'s AIMD backs off per host off the observed reply ratio, and the
reprobe pass re-checks at 40 pps). The global slider is no longer the accuracy
hazard it was — P4 means a named intensity carries an envelope matched to its
breadth. What remains is genuinely per-network *link capacity*, which cannot be
designed against without multi-segment measurements. **Reopen only with data
from P1 across at least two segments of differing capacity.**

### P7 — Smaller known gaps **(ALL DONE)**

**Gate 6 fan-out.** The last sequential stage. Now a `host_concurrency`
semaphore plus `asyncio.gather`, matching the banner pass —
`workflow_engine.py`, `tests/test_gate6_concurrency.py`, and a policy
assertion in `test_stage_fanout_policy.py`. Measured 8 hosts × 0.12 s:
**1.11 s → 0.30 s.** SSH and Windows stay sequential *within* a host — two
protocols against the same box, and overlapping them doubles load on one
target to save time the fan-out already recovers.

**`ScopeError` reload-aliasing.** `ScopeError` now subclasses `ValueError`.
Before changing it I audited every raise path for a broad `except ValueError`
that might swallow-and-continue — a scope failure turning soft would be a
genuine security regression. There is none: `_guarded` returns an error
`ScanResult` *before* `scan_target`, the CLI wrapper exits 1 on both branches,
and `run_scan`'s handler is the only one in its try. So the widened catch
changes which branch reports a refusal, never whether a target gets scanned —
and `TestTheGateStillRefuses` pins exactly that. The "always reference it
through the module" convention is no longer load-bearing.

**`scan_metrics` accounting.** `partition_result_scope` now drops a host's
metrics row with its facts (`_drop_orphaned_metrics`). Matched **by value**,
one occurrence per dropped `scan_summary` fact, rather than recomputing a list
the probe declared. Worse than cosmetic, as it turned out: the orphaned row
could push `scan_health_summary` to `degraded` and raise a coverage finding
sourced entirely from a host whose evidence was deliberately discarded.

**T2.4 — kernel ceilings are now enforced *and* recorded.** Two halves:

1. **Admission.** `_refuse_if_kernel_unsafe` (`engine.py`), wired beside
   `_refuse_if_infeasible`, overridable with `allow_degraded_kernel=true`.
2. **Evidence.** `run_stats["kernel"]` on all three exit paths. A1 measured
   these and left them in a log line, so the manager — and the report, and the
   operator reading it — never learned the probe was under-tuned.

**Only `conntrack` blocks**, and the line is not severity, it is whether the
failure can *speak*:

| check | silent? | blocks? | why |
|---|---|---|---|
| conntrack | yes | **yes** | Under NAT every probe takes an entry whatever the topology. Unconditional arithmetic |
| neighbour | yes | no | Only holds on a **flat L2** segment. The probe cannot see its targets' topology, so blocking a routed 1000-host sweep would be a **false refusal** |
| ephemeral | no | no | `EADDRNOTAVAIL` → `local_resource_error` → `degraded`. The scan reports its own injury |
| fd | no | no | `EMFILE`, same path |
| raw_socket | no | no | The connect fallback is slow, not wrong; the feasibility floor already refuses what cannot finish |

**`pids_limit: 256`** and the three sysctls are documented in
`probe/docker-compose.yml`, with the per-preset conntrack arithmetic spelled
out (light 6,000 / standard 24,000 / deep 18,000 / an explicit 600 pps →
72,000, which overflows).

---

## 8. Operational notes for whoever picks this up

### Migrations — REQUIRED before the new probe talks to this manager

```bash
cd manager/backend && alembic upgrade head
```

- **0042** `scan_result_chunks.complete` — partial vs finished chunks (T1.4)
- **0043** `agentstatus` gains `paused` — spool back-pressure (B4)

Both default and backfill safely; an older probe is unaffected.

### Running the suites

```bash
cd probe && ./.venv/bin/python -m pytest tests/ -q            # 2313 passed
cd manager/backend && ./.venv/bin/python -m pytest -q         # 1262 passed
```

### The two-tree rule

`probe/scanner/` and `probe/main_scripts/` are **byte-identical mirrors**.
`main_scripts` is canonical. After editing either:

```bash
cp probe/main_scripts/<file>.py probe/scanner/<file>.py
./.venv/bin/python -m pytest tests/test_two_tree_parity.py -q
```

This bit repeatedly during this work — tests import `scanner.*` while edits
landed in `main_scripts/`.

### Lint

There is **no ruff config and no lint step in CI**. Untouched files report
findings under ruff defaults. Compare before/after with `git stash` rather than
chasing the absolute count.

### CI

- `.github/workflows/agent-ci.yml` — `probe/agent/**`, `probe/tests/**`;
  Linux + macOS + Windows
- `.github/workflows/scanner-accuracy.yml` — `probe/main_scripts/**`,
  `probe/scanner/**`, and now `probe/workflow/**` (that path previously
  triggered **no** CI at all)

All 21 new test files are wired into one of the two.

### Useful one-liners

```bash
# What this host can sustain
cd probe && ./.venv/bin/python -c "
import sys; sys.path.insert(0,'.')
from agent.kernel_limits import describe_capability, probe_limits
print(describe_capability(probe_limits()))"

# Feasibility of an envelope
cd probe && ./.venv/bin/python -c "
import sys; sys.path.insert(0,'.')
from agent import feasibility as fz
print(fz.describe(fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=7200)))"
```

**P1 lab repro — one command, all three answers.** Verified end-to-end
(2026-09-22) against the runner's own non-loopback IPv4, which is an address
the probe may legitimately scan; the permanent denylist correctly refuses
loopback, so do not point this at 127.0.0.1.

Edit `TARGETS` / `SCOPE` to the authorized range, then:

```bash
cd probe && ./.venv/bin/python -c "
import sys, json; sys.path.insert(0,'.')
from agent.engine import run_scan

TARGETS = ['192.168.1.10-192.168.1.17']     # the 8 hosts
SCOPE   = ['192.168.1.0/24']                # must cover them

r  = run_scan('port_scan', {'targets': TARGETS, 'scope_cidrs': SCOPE,
                            'intensity': 'deep'})
rs = r.get('run_stats', {})
print('outcome :', r['ok'], r.get('outcome'), r.get('error') or '')
print('kernel  :', json.dumps(rs.get('kernel'), indent=2))
print('timing  :', json.dumps(rs.get('timing'), indent=2))
open('/tmp/p1.json','w').write(json.dumps(r, indent=2, default=str))
print('full result -> /tmp/p1.json')"
```

Reading it:

- `kernel.checks` containing `limits_unread` for ephemeral/conntrack/neighbour
  means **you are not on Linux** — the run tells you nothing about the deployed
  probe's ceilings. Run it on the probe host.
- `kernel.blocking` non-empty means the job was **refused** (T2.4). That is the
  answer, not a failure: fix the sysctl or pass `allow_degraded_kernel=true` to
  measure anyway.
- `timing.stages` dominated by `port_scan` → D1's fix is the thing to measure
  next, against `nmap` from the same vantage.
- dominated by the datagram branches (`udp_scan`, `snmp`, `ipmi`) → a
  **different** fix entirely: UDP timeout strategy, not the SYN engine.
- `timing.estimate.verdict` vs `timing.elapsed_seconds` calibrates the model.
  On the verification run the floor predicted 1.3 s and actual was 1.3 s.

---

## 9. Where to start

**Every task that can be done without hardware is done.** P3, P5 and P6 are
closed with reasoning; P4 and all of P7 shipped; P2 is fixed where it was
verifiable (D1) and correctly scoped where it was not (D2).

**P1 is the only open item, and it needs two things this environment does not
have: a Linux probe host with `NET_RAW`, and a target network you are
authorized to scan.** Everything below is downstream of it.

1. **Run the P1 command in §8** on the probe host. It is verified end-to-end
   and prints the ceilings, the stage timings and predicted-vs-actual in one
   go.
2. **Validate D1 on real packets.** The interleaved drain is proven against a
   fake kernel; the packet path still needs a Linux box with `NET_RAW`, scanned
   against a host with a known mix of open/closed/filtered ports and compared
   with `nmap` from the same vantage. `accuracy_gate.py`'s provenance rule
   requires an independent observer for any accuracy claim.
3. **Then** decide on D2 with measurements. Re-derive §4.1's demand column at
   **150 pps**, not 600 — every figure there assumed the launcher's override.

Two standing gaps worth closing whenever convenient:

- **Frontend tests are not in CI.** `.github/workflows/` covers the probe and
  the scanners only, so `npm test` (221 tests, including the intensity parity
  guard) is a local gate nothing enforces on a PR. It is the only thing
  protecting the dial from drifting again.
- **Manager backend tests are not in CI either** — same story, 1,272 of them.

Commit the current work to a branch first — it is substantial and uncommitted.
