# Deep scan: every one of the 65,535 TCP ports, with no cap

Date: 2026-10-09 · Status: **design for review — nothing implemented** · Trigger: a deep port
sweep of one host (`192.168.1.70`) from the Windows agent took 6.5 minutes for its first 1,145
ports, and its 64,390-port tail could not finish inside the job's budget.

## 1. Goal and the rule that makes it safe

**Goal.** A deep scan covers all 65,535 TCP ports of every in-scope host. Nothing is dropped to
fit a clock.

**Rule.** "No cap" applies to *coverage*, not to *load on the customer's network*. Rate limits,
the fragile-asset guard, blackout windows and the operator's cancel button all stay. Time
becomes the variable: the scan takes as long as the covered ports need, it shows its
progress and ETA, and it survives restarts.

Every port ends in exactly one state: `open`, `closed`, `filtered` (with evidence), or
`not_scanned` with a stated reason. A clock running out is never reported as `filtered`.

## 2. What caps coverage today

| # | Cap | Where | Effect |
|---|---|---|---|
| 1 | Whole-job ceiling, 2 h (env max 24 h; a job can only lower it) | `probe/agent/engine.py:78` `MAX_JOB_SECONDS` | Everything must fit 2 h |
| 2 | Port-tail deadline = ceiling − max(300 s, 15 %) | `engine.py:273` `_tail_deadline` | Unreached tail ports become `not_scanned` |
| 3 | `deep` intensity is the ~2,400-port "enterprise" set, not 65,535 | `probe/workflow/intensity.py` `"deep"` | Network VA at deep never sees the full range |
| 4 | `deep_port_sweep` limited to 3 hosts | `engine.py` `DEEP_PORT_SWEEP_MAX_HOSTS` | Wider scope refused |
| 5 | Admission refuses a job whose estimate does not fit | `engine.py:300` `_refuse_if_infeasible` | Needs `allow_infeasible` |
| 6 | Cleanup re-probe limited to 2,048 ports per host | `probe/scanner/port_scanner.py:457` | The rest stay mis-reported `filtered` |

And two defects that make the caps bite far earlier than they should:

- **Windows reports a closed port only after ~2.2 s** (measured on the customer's agent: it
  re-sends the SYN before failing `connect()`). The scanner's adaptive timeout learns the LAN's
  millisecond RTT from open ports and drops toward its 0.3 s floor, so nearly every closed port
  times out and is recorded `filtered` (`55/55` and `1110/1110` "resolved" by the cleanup pass in
  the logs). The scan is slow *and* wrong until the cleanup pass rescues it, and cap 6 stops the
  rescue on a 65,535-port host.
- **SYN scanning is Linux-only** (`probe/scanner/syn_scanner.py` `syn_scan_supported`): Windows
  forbids TCP over raw sockets, so the Windows agent always uses `connect()`.

## 3. Design

### 3.1 Make a full sweep physically fast (agent)

**Windows: no SYN retransmission on scan sockets.** Before `connect()`, set
`SIO_TCP_INITIAL_RTO` with `MaxSynRetransmissions = TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS`
(Windows 8+). On Windows 10 builds before RS3 that constant is misread as "255 retries", so use
`MaxSynRetransmissions = 1` there (the workaround OpenJDK ships). A refused port then fails at
network speed, the adaptive timeout stays honest, and the cleanup pass has almost nothing to do.
Scope: scan sockets only, never the agent's manager connection.

**Windows: raise connect concurrency** from 80 toward a measured safe value (target 512), now
that a closed port no longer holds a slot for 2.2 s. Measure on the customer's machine first.

**Linux: SYN is the full-port engine.** Stateless, one packet per port. A deep scan prefers a
Linux agent when one is online and eligible (manager dispatch, §3.3).

**Rate is the operator's choice, not a constant.** `deep` runs at 150 pps today. A deep scan
gets its own rate (decision D1); the existing AIMD controller still backs off when delivery
drops, so a fragile segment slows the scan instead of being flooded.

**Estimated wall-clock per host for 65,535 ports** (one attempt per port; silent ports add
retries; to be confirmed by measurement):

| Engine | Target refuses closed ports | Target drops closed ports |
|---|---|---|
| Windows `connect()` today (2.2 s per closed port, 80 slots) | ~30 min, and mostly mis-reported | timeout-bound, hours |
| Windows `connect()` fixed, 512 slots, 1,000 pps | ~66 s | ~2–5 min |
| Linux SYN, 1,000 pps | ~66 s | ~66 s + retries |
| Linux SYN, 3,000 pps | ~22 s | ~22 s + retries |

A /24 (254 hosts) at 1,000 pps is about 4.6 h of probing whichever engine runs it. That is why
the time ceiling has to go (§3.2), not just the per-port cost.

### 3.2 Remove the time ceiling as a coverage limit: sharded jobs (manager + agent)

A long scan must not be one job holding one lease for hours. The manager splits a full-port
scan into **shards**, each a normal leased `scan_job`:

- **Shard 0 per host**: host discovery + the high-signal first pass (today's 1,145 ports) + the
  full assessment (banners, OS, deep branches). The customer gets findings early.
- **Shards 1…N per host**: the remaining ports in fixed ranges (default 8,192 ports, 8 shards per
  host). Each shard re-assesses only the ports it opened (the logic already exists after the
  tail: "tail opened new port(s) — assessing them").

Why shards:

- **Resume.** A crash, reboot, agent upgrade or lost lease costs one shard, not the scan. Today
  resume is per host (`skip_hosts`), so a 65,535-port host restarts from zero.
- **No ceiling.** Each shard fits the existing 2 h job budget easily, so caps 1, 2 and 5 stop
  limiting coverage without being raised.
- **Parallel.** Several eligible agents can take shards of the same scan at once.
- **Progress.** "37 / 2,032 shards, ETA 3 h 10 m" falls out of shard counts.

Data model (one migration): `scan_jobs.parent_job_id`, `shard_index`, `shard_count`,
`port_ranges` (JSON). The parent job's status is derived from its shards. The claim, lease,
fence and result paths are unchanged: a shard is a job.

### 3.3 Dispatch

- A full-port shard prefers a Linux agent with SYN capability, then a fixed Windows agent.
- The agent reports `scan_engine` (`syn` or `connect`) and `connect_syn_retry_off` in its
  capabilities, so the manager knows what it is dispatching to.
- Lift cap 4 for sharded scans: the host count only affects how many shards exist.

### 3.4 Honest results

- Cap 6: when the cleanup pass cannot re-check a port, report it `not_scanned`
  (reason `reprobe_budget`), never `filtered`. Better: scale the budget with the port count, and
  with the Windows fix it is rarely reached.
- Per host, record coverage: ports `classified / 65,535`, engine, rate, retries, shards done.
  The report states coverage beside the findings.
- Fix the runtime estimate (it counted only the first pass at nominal rate) and replace the
  Linux-only `NET_RAW` advice with platform-correct advice.
- Log the banner-grab `WinError 10054` resets at debug level; they are the target closing a
  connection, not an agent error.

## 4. Phases

| Phase | Contents | Removes | Size |
|---|---|---|---|
| **1. Correct and fast** | Windows SYN-retry off; concurrency measured and raised; cleanup honesty (cap 6); estimate and warning text; 10054 noise; capability flags | The 2.2 s-per-port defect and false `filtered` | Agent only, small |
| **2. Full coverage, no ceiling** | Sharded jobs (migration, manager splitter, parent status, progress/ETA API), resume per shard, cap 4 lifted, deep option = 65,535 | Caps 1, 2, 4, 5 as coverage limits | Manager + agent + UI, medium |
| **3. Throughput** | Linux-preferred dispatch, deep rate decision applied, Linux scanner VM image (OVA) | Wall-clock at /24 scale | Medium |

Phase 1 alone makes a few-host 65,535-port sweep from the Windows agent fit comfortably inside
today's 2 h budget. Phase 2 is what makes "no cap" true for any scope.

## 5. How we know it works

- Phase 1, on the customer's Windows agent against `192.168.1.70`: the cleanup line goes from
  `1110/1110` to near zero, the 1,145-port pass takes seconds, and a full 65,535-port sweep
  completes with every port classified and none `not_scanned`.
- A closed-port `connect()` from PowerShell drops from 2.2 s to milliseconds when made with the
  same socket option (a one-line check we ship in `doctor`).
- Phase 2: kill the agent mid-scan; on restart only the in-flight shard is redone; the parent
  reaches 65,535 / 65,535 per host.
- Unit tests on Linux for the socket-option code path (mocked), the shard splitter, parent-status
  derivation and the `not_scanned` accounting; the Windows path is proven by the measurement
  above (the Windows CI runner is blocked by Actions billing).

## 6. Decisions for you

- **D1 — deep scan rate.** 150 pps today. Proposal: 1,000 pps default for deep, operator-editable
  per engagement, AIMD still backing off. Banks may want a lower default.
- **D2 — what "deep" means.** Make Network VA at deep cover all 65,535 ports (sharded), or keep
  that only in the Deep Port Sweep use-case and lift its 3-host cap. Proposal: both reach 65,535;
  Network VA deep shows the ETA before it starts.
- **D3 — longest scan an operator may start.** With shards there is no technical limit. Proposal:
  show the ETA and require confirmation above 8 h, rather than a hard stop.

## 7. Not chosen, and why

- **Npcap or WinDivert SYN on Windows.** Near-Linux speed, but a kernel driver on customer
  endpoints (security review and EDR friction at banks) and, for Npcap, a paid OEM
  redistribution licence. Revisit if Windows-only customers need SYN speed after Phase 1.
- **Just raising `PROBE_MAX_JOB_SECONDS` to 24 h.** Removes cap 1 without resume: one crash late
  in a 20-hour single job loses it all, and the 2.2 s Windows defect makes most of that time
  wasted.
