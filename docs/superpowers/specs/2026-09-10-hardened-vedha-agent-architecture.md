# Hardened cross-OS vedha-agent — architecture, failure register & small-task plan

**Date:** 2026-09-10
**Branch:** `cross-os-vedha-agent-install`
**Status:** Architecture + plan for review — NO implementation until approved

## Framing

The earlier installer spec/plan
(`2026-09-09-universal-cross-os-agent-installer.*`) solves *installation*.
The second-pass senior review establishes that installation is ~15% of the
problem; the other 85% is **identity, authorization, safety, observability, and
a two-year operational lifetime**. This document is the full-proof architecture
that treats the agent as what it is: **a root-privileged, self-restarting,
network-scanning, dial-out process shipped to thousands of hosts across three
OSes.** Every decision below is chosen to survive an EDR fleet, an OT segment, a
week-long Manager outage, a compliance audit, and a hostile clock.

Two rules govern the whole design:
1. **Unsafe defaults are bugs.** Where a default could brick a device, lose
   data, or trip an EDR, the safe behavior is the default and the dangerous one
   is explicitly, separately authorized.
2. **Every failure is legible.** No silent data loss, no generic "connection
   failed", no unfalsifiable "it didn't take effect". Each failure has a distinct
   state, an operator-facing message, and a remediation string.

---

## Part A — Architecture

### A0. Component map

```
 ┌──────────────────────────── vedha-agent (host) ────────────────────────────┐
 │ bootstrap (sh/ps1)  ── ensure Python + Layer-1 deps, hand off ──▶           │
 │ brain (agent.setup) ── doctor | self-scan | connect | config | diagnostics  │
 │   ├─ config loader        (single precedence chain, one validated object)   │
 │   ├─ interface+scope model (typed segments, denylist, container detect)     │
 │   ├─ scan engine           (EXISTING agent.workflow — reused, rate-gated)   │
 │   ├─ durable result queue  (fsync'd, bounded, encrypted, idempotent)        │
 │   ├─ uplink                (mTLS, job-signature verify, kill-switch honor)  │
 │   ├─ supervisor            (monotonic backoff, restart limits, exit-states) │
 │   └─ observability         (structured logs, heartbeat metrics, bundle)     │
 └─────────────────────────────────────────────────────────────────────────────┘
        │ dial-out 443 (REST+WSS)                     ▲ signed jobs, short-lived certs
        ▼                                             │
 ┌──────────── Manager (crown jewel — separate hardening track) ───────────────┐
 │ enrollment CA  ≠  job-signing key · kill switch · fleet views · audit store  │
 └──────────────────────────────────────────────────────────────────────────────┘
```

The **brain↔daemon boundary** and the **agent↔manager boundary** are the two
load-bearing interfaces. Both become *versioned, contract-tested artifacts*
(Task 0b), not implicit couplings.

### A1. Identity & authorization model (§2, §11 of the review)

- **Separate keys:** the enrollment CA (issues agent identity) is distinct from
  the job-signing key (authorizes scan jobs). Compromise of one does not grant
  the other.
- **Independent ceiling enforcement:** every job the Manager pushes is
  **signed**; the agent verifies the signature against a **pinned** job-signing
  public key and then **re-checks the job's targets against its own local typed
  scope** before a packet leaves. The agent never trusts the Manager to stay in
  scope — it enforces its own ceiling.
- **mTLS, short-lived certs.** The agent authenticates to the Manager and vice
  versa at the TLS layer; certs are short-lived (clock-sensitive → A6).
- **Manager-independent kill switch.** A locally-honored stop (file/signal/OS
  service stop) halts scanning even if the Manager is unreachable — and a
  Manager-pushed revoke that the agent obeys on next contact.
- **Rogue-actor threats:** rogue agent enrolling (mitigated by approval-gated
  enrollment + CA), rogue Manager issuing jobs (mitigated by pinned job-signing
  key), local tampering with scope/config (mitigated by signed config + audit).

### A2. Scope model — typed segments (replaces the flat CIDR string) (§4)

The single `PROBE_NETWORK_SEGMENTS` string is replaced by a **typed segment
list**, established and human-confirmed **at enrollment**:

```jsonc
scope = [
  { "cidr": "10.20.0.0/24", "type": "IT",   "profile": "it",  "authorized_by": "...", "site": "hq" },
  { "cidr": "10.20.5.0/24", "type": "IoT",  "profile": "iot", "rate_ceiling_pps": 50, "site": "hq" },
  { "cidr": "10.99.0.0/24", "type": "OT",   "profile": null, "active": false, "site": "plant" },
  { "cidr": "10.20.9.0/24", "type": "NEVER" }
]
```

- **Interface enumeration:** the agent enumerates **all** NICs with prefixes and
  classifies each (physical / virtual / tunnel / container / loopback) and
  reports the full inventory to the Manager. Scope is **confirmed by a human
  once**, not derived automatically.
- **Permanent denylist (never scanned, not configurable up):** loopback,
  link-local incl. `169.254.169.254`, multicast, broadcast, and **the Manager's
  own address**.
- **Container / WSL2 refusal:** if the primary interface is a container/WSL2 NAT
  namespace (e.g. `172.17.0.0/16` docker bridge), the agent **refuses LAN scan**
  with a specific message — it does not scan the virtual bridge.
- **Site/tenant key:** every result is keyed by `(site, address, …)`, resolved
  at enrollment — so overlapping RFC1918 across branches/VPCs stays
  distinguishable in the Manager's DB.
- **IPv6:** explicitly out of scope for v1; `doctor` states this on v6-only
  hosts instead of emitting a confusing "no scope" error.
- `doctor` **suggests** a derived `/24`; `connect` **never** auto-adopts it.

### A3. OT safety model — the single highest risk (§1)

**Decision: do NOT ship the `ot` profile in v1.** Ship **IT** and **IoT
(rate-limited)**. OT is a separately-designed, separately-reviewed capability
(own track, own approval). When built, it must have:

| Control | Requirement |
|---|---|
| Passive-first default | `ot` defaults to passive (SPAN/TAP, ARP-cache read, mDNS/LLDP listen); active probing needs a separate explicit authorization |
| Hard rate ceiling | Per-host/per-segment packet-rate caps enforced **in the engine**, not raisable from the CLI; single-digit pps is normal |
| Protocol-aware safety | No version probes / fuzzing / OS-fingerprint on industrial ports; connect-scan only, one connection at a time, immediate clean close |
| Blast-radius fence | Device-class denylist + maintenance-window gate |
| Two-person authorization | OT scan requires a second approver + a signed, retained record |
| Abort on anomaly | If a target stops responding mid-scan, halt the **whole segment** immediately and alert; never retry |

The CLI must not expose `--profile ot` in v1 (the flag itself is the hazard).

### A4. Durable result queue (§3)

Between the scan engine and the uplink sits an explicit durable queue:

- **Append-only, `fsync`'d**, under an OS `StateDirectory`.
- **Bounded by size AND age**, with a **declared overflow policy** (drop-oldest
  for scan data) — a decision, not an accident.
- **At-least-once + idempotency keys** (per job) so a crash between "sent" and
  "acked" replays safely and the Manager dedups.
- **Encrypted at rest** with a **host-sealed key** (queue holds topology +
  banners).
- **Backpressure:** above a high-water mark, the scheduler **stops starting new
  scans** rather than filling the disk — prevents the "security agent filled
  `/var` fleet-wide" incident.

### A5. Config model & precedence (§7)

- **One documented precedence chain:** CLI flag > process env > `probe.env` >
  Manager-pushed config > built-in default. One loader, one validated config
  object; the service unit is **rendered from** that object (no third hardcoded
  copy).
- **`vedha-setup config show --effective`** prints every resolved value **with
  its source** — kills the "I changed it and it didn't take effect" class.

### A6. Clock & authentication robustness (§5)

- `doctor` reports **clock offset vs the Manager** and flags skew beyond a
  threshold (two-line check, kills an entire support category).
- Enrollment refuses with a **specific** error when skew exceeds token TTL
  ("system clock is 4h12m behind the Manager; fix NTP before enrolling").
- Bounded validity **leeway** on token checks is **server-side policy**, not a
  client flag.
- Supervisor backoff uses **`time.monotonic()`**, never wall-clock (an NTP step
  mid-backoff must not cause a retry storm or a multi-hour stall).

### A7. Exit-state protocol (§8)

Replace the four overloaded exit codes with a **wide channel**: a structured
state (a state file + a structured stderr line the supervisor parses), with the
**exit code only distinguishing broad classes**:

| Class | Code | Examples | Supervisor policy |
|---|---|---|---|
| success | 0 | clean shutdown | stop |
| retryable | 10 | manager-503, DNS-fail, no-interface-up, TLS-transient | monotonic backoff, capped retries |
| fatal-config | 20 | empty scope, bad manager URL, clock-skew>TTL | stop, print remediation |
| fatal-identity | 30 | cert-expired, revoked, orphaned identity | re-enroll flow (bounded) |
| awaiting-approval | 40 | pairing not yet approved | poll, no error |

The structured detail (`reason`, `remediation`) rides the state file so
"cert expired" is never confused with "manager down".

### A8. EDR coexistence & distribution (§2, §10)

- **Code signing on all three OSes:** Authenticode (EV cert) on Windows;
  notarized + hardened-runtime on macOS; signed package + published GPG key on
  Linux. Unsigned binaries are the single biggest EDR trigger.
- **Vendor submission** (Microsoft MSRC FP portal + major EDR allowlist
  programs) — started **before GA**.
- **SOC deployment guide:** exact process names, paths, hashes, network
  destinations, expected behaviors, and per-EDR exclusion rules; plus a candid
  "here's what looks suspicious and why" section.
- **Predictable network behavior:** one destination, one port, TLS; no domain
  fronting, no DGA, no dynamic C2 discovery.
- **Restart limits, not infinite self-heal:** `StartLimitBurst`/equivalent so a
  deliberate stop is respected — the difference between "tolerated tool" and
  "malware resisting remediation".

### A9. Observability (§6)

- **Structured JSON logs**, stable schema, correlation ID per job, severity
  field; **never** log credentials / full results / target lists at info; local
  rotation with a size cap + optional forwarding.
- **Heartbeat metrics (low cardinality — no IPs/hostnames as labels):** agent
  version+OS+artifact hash, time-since-last-successful-contact, queue depth +
  oldest-unsent age, job-outcome counts by terminal state, restart count + last
  exit class, RSS/CPU high-water, privilege/capability state.
- **`vedha-setup collect-diagnostics`** → a **redacted** archive (versions,
  secret-stripped config, recent logs, interface inventory, clock offset,
  connectivity results, service state).
- **Manager fleet views:** by version, not-seen-in-N-hours, growing queues,
  repeated restarts.

### A10. Data handling, privacy, residency (§9)

- **Classification:** scan output is **confidential customer data**, not
  telemetry — protected in transit, at rest on agent, at rest on Manager.
- **Minimization:** normalized service+version identifiers, not full banner
  capture (a banner is a liability).
- **Residency:** the Manager URL is per-deployment; the agent **never** sends to
  a default/hardcoded endpoint.
- **Retention & deletion:** "delete this host's data" works end-to-end (agent
  queue + Manager).
- **Redaction** in logs and the diagnostics bundle (the most likely disclosure
  vector).

### A11. Compliance & legal (§10) — roadmap with real deadlines

| Item | Action | Gate |
|---|---|---|
| SBOM | Generate CycloneDX/SPDX in CI, publish per release | EU CRA + US EO 14028 procurement |
| VDP + CVE/CNA | `security.txt`, disclosure address, SLA, CNA relationship | before GA |
| FIPS 140-3 | FIPS-validated crypto + FIPS mode (constrains TLS lib + build) | fed/defence/finance roadmap |
| Npcap OEM license | Verify paid OEM license **before** building the Windows capture path | commercial redistribution |
| Export control | Legal opinion (Wassenaar-derived; India SCOMET) — distributing binaries from a public URL | before public distribution |
| SOC2 / ISO 27001 audit evidence | System produces immutable "who authorized which scan, when, against what" at scan time | enterprise procurement |

### A12. Threat model & process (§11)

- **STRIDE document** (Task 0a): spoofing (rogue agent/manager), tampering
  (local scope/config), repudiation (unsigned scan authorization), info
  disclosure (queue on disk, diagnostics bundle), DoS (agent→manager, or
  scanner→fragile device), EoP (root agent with a network-facing parser). Each
  entry maps to a control; uncontrolled entries are the roadmap.
- **Manager hardening** (separate track): signed job authorization verified
  against a pinned key; manager-independent kill switch; strict input validation
  on everything the agent accepts (remote attack surface running as root);
  enrollment CA separated from job-signing key.
- **Game days:** manager-down-48h-then-restored (stampede? results survive?),
  fleet cert expiry, bad version to 100% (rollback without SSH?), out-of-scope
  scan (kill-switch latency), disk-full queue, mass clock-skew.

---

## Part B — Points-of-failure register

Severity: **S1** = bans/bricks/lawsuit-class · **S2** = fleet-wide outage/data
loss · **S3** = per-host/support burden.

| # | Failure mode | Sev | Consequence | Control (arch ref) | Detection |
|---|---|---|---|---|---|
| 1 | `ot` active scan bricks a PLC/pump/fire-panel | S1 | Safety event; one customer lost, market reputation | Don't ship OT v1; passive-first + engine rate cap + abort-on-anomaly (A3) | Abort-on-anomaly; maintenance-window gate |
| 2 | EDR quarantines the agent fleet-wide; self-heal reads as malware | S1 | Rollout blocked / removed during IR | Code signing + vendor allowlist + restart limits + SOC guide (A8) | Fleet "not-seen" spike; restart-count metric |
| 3 | Manager down → scan results lost from memory | S2 | Compliance shows "clean" — worse than loud failure | Durable fsync'd queue + at-least-once + idempotency (A4) | Queue depth / oldest-unsent-age metric |
| 4 | Queue fills `/var` during a long outage | S2 | Disk-full on production hosts fleet-wide | Bounded queue + backpressure stops scans (A4) | Queue high-water metric; disk-space `doctor` check |
| 5 | Overlapping RFC1918 → results collide across sites | S2 | Findings DB unusable at multi-site scale | Site/tenant key at enrollment (A2) | Manager dedup/anomaly on key collisions |
| 6 | Container/WSL2 → scans the virtual bridge, not the LAN | S2 | Silently wrong results (worst kind) | Namespace detection + refusal (A2) | `doctor` reports namespace + refusal |
| 7 | Clock skew → TLS "cert not yet valid" surfaced as generic failure | S3 | Days of misdiagnosed support per occurrence | `doctor` skew check + specific enroll error + server leeway (A6) | `doctor` clock-offset check |
| 8 | Config drift (probe.env vs env vs service unit) | S3 | "Changed scope, no effect" — unfalsifiable | One precedence chain + `config show --effective` (A5) | `config show --effective` reveals source |
| 9 | Overloaded exit codes → wrong retry policy | S3 | No-network host retry-storms like a transient outage | Exit-state protocol (A7) | Structured state file; restart/exit-class metric |
| 10 | `curl\|sh` tampered / unsigned artifact | S1 | Supply-chain compromise of a root agent | Signed artifacts + checksums + package managers (A8) | Signature verification at install |
| 11 | Rogue Manager issues jobs to the fleet | S1 | Arbitrary root-adjacent scanning + network map | Pinned job-signing key + independent scope ceiling (A1) | Signature verification per job |
| 12 | Diagnostics bundle leaks topology/creds | S2 | Confidential-data disclosure (emailed around) | Redaction + minimization (A9/A10) | Redaction tests on bundle output |
| 13 | Infinite self-heal fights a deliberate stop | S2 | Reads as malware; SOC escalation | `StartLimitBurst` + honor kill switch (A7/A8) | Restart-count metric threshold |
| 14 | VPN split-tunnel → scans through the concentrator | S3 | Traffic the network team won't appreciate | Interface classification + human-confirmed scope (A2) | Interface inventory in `doctor` |
| 15 | Network-facing parser bug in a root process | S1 | Remote EoP to root on thousands of hosts | Strict input validation on manager input; least-privilege (A1/A12) | Fuzzing in CI; threat-model control |

---

## Part C — Small-task plan (phased, sequencing fixed per the review)

The review's structural fix is honored: **two design tasks go first**, and the
**scope model lands in Phase 1** (not retrofitted after a `/24` assumption
propagates). OT is a **separate future track**, not in v1.

### Phase 0 — Design & contracts (no product code)
- **0a Threat model (STRIDE)** — one doc: fix identity, authorization, scope, and
  data-classification models before code. Output: control-per-entry table.
- **0b Brain↔daemon interface contract** — versioned artifact both sides import:
  config schema, enrollment protocol, **exit-state protocol** (A7), job-signature
  format. Contract tests on both sides. (Removes the "archaeology" coupling the
  earlier plan flagged.)
- **0c Agent↔Manager contract** — signed-job format, mTLS profile, kill-switch
  semantics, result idempotency key, site/tenant key. (Manager team dependency.)

### Phase 1 — Interface & typed-scope model (pure, testable)
- 1a Enumerate all interfaces (prefix + classify physical/virtual/tunnel/container/loopback) — cross-OS, stdlib-first.
- 1b Permanent denylist (loopback, link-local/169.254.169.254, multicast, broadcast, manager addr).
- 1c Typed-segment scope object + validation (IT/IoT/OT/NEVER, per-segment profile+authz+site).
- 1d Container/WSL2 detection → refusal path.
- 1e IPv6 out-of-scope handling (explicit, documented).
- 1f Unit tests for every classifier + denylist + refusal (golden cases).

### Phase 2 — Config loader + `doctor` (real checks)
- 2a Single precedence chain + one validated config object + loader.
- 2b `config show --effective` (value + source).
- 2c `doctor` real checks: Python, artifact integrity, privilege/capability,
  interface inventory, DNS-of-manager, TCP+TLS+cert-chain to manager, **clock
  offset**, queue disk space, service state, EDR-likely-present. Each → pass/fail/warn + remediation string. (Fix the `or True` false-positive; actually contact the Manager.)

### Phase 3 — Exit-state protocol + supervisor
- 3a State-file + structured-stderr emitter (classes in A7).
- 3b Supervisor: **monotonic** backoff, per-class policy, `StartLimitBurst`,
  honor kill switch. Unit-tested with an injected spawn.

### Phase 4 — Durable result queue
- 4a Append-only fsync'd store under StateDirectory; size+age bounds; drop-oldest overflow.
- 4b Idempotency key per job; at-least-once send; encrypt-at-rest (host-sealed key).
- 4c Backpressure high-water → scheduler stops new scans; disk-space guard.
- 4d Tests: crash-replay dedup, overflow policy, backpressure trigger.

### Phase 5 — self-scan (own IP, manager-less) — uses the real scope model
- 5a Own-IP via interface model (not the naive UDP trick alone); scope = own host only.
- 5b Invoke existing local engine; write results through the durable queue's local-archive path.
- 5c Tests: scope-to-own-IP, refusal when no IP / container namespace.

### Phase 6 — connect (verified contract) + uplink security
- 6a Implement against the **0b/0c contracts**: enrollment (pairing/PAT/token) with clock-skew guard; mTLS; **verify signed jobs against pinned key**; re-check targets vs local scope before scanning; honor kill switch.
- 6b Supervisor integration (Phase 3) with the exit-state protocol.
- 6c Contract tests for the enrollment env/protocol mapping (the earlier plan's flagged coupling — now specified, not guessed).

### Phase 7 — Dependency bootstrap + shims
- 7a Layer-1 (Python + venv module) per OS in `install.sh` (apt/dnf/pacman/brew) / `install.ps1` (winget).
- 7b Layer-2 wheel-first / compile-fallback pip (from the earlier plan).
- 7c Signature-verify the fetched bootstrap (checksum/GPG) — supply-chain (A8).

### Phase 8 — Observability
- 8a Structured JSON logging (schema, correlation id, secret/target redaction, rotation).
- 8b Heartbeat metrics (the low-cardinality set in A9).
- 8c `collect-diagnostics` redacted bundle + redaction tests.

### Phase 9 — Service install (with limits)
- 9a systemd / launchd / Scheduled Task rendered **from the config object**;
  `StartLimitBurst`/KeepAlive-with-limits; StateDirectory wired for the queue.
- 9b Uninstall that actually works (round-trip test).

### Phase 10 — Distribution, signing, SBOM, CI
- 10a Code signing pipeline: Authenticode(EV) / notarize+harden / signed pkg+GPG.
- 10b SBOM (CycloneDX/SPDX) in CI, published per artifact.
- 10c 3-OS CI matrix: unit tests + `doctor` smoke + signature verify + SBOM presence.
- 10d SOC deployment guide, network-requirements doc, data-handling statement, per-exit-state runbook, uninstall guide.

### Deferred / separate tracks (explicitly NOT v1)
- **OT capability** (A3) — own design, own review, two-person authz.
- **FIPS 140-3 mode**, **Npcap OEM** (only if Windows packet-capture path is built), **export-control legal opinion**, **Manager hardening + game days** (Manager team).

---

## Part D — v1 scope line

**Ships in v1:** IT + IoT(rate-limited) scanning; typed-scope model with
interface enumeration + denylist + container refusal; durable encrypted queue
with backpressure; single-precedence config + `config show --effective`;
exit-state protocol + limited supervisor; real `doctor`; structured
logs + heartbeat metrics + diagnostics bundle; mTLS + signed-job verification;
signed artifacts + SBOM; per-OS service with restart limits; SOC/uninstall/
network/data-handling docs.

**Explicitly deferred:** OT active scanning, FIPS mode, IPv6 scanning, Manager
hardening & game days (dependency track), full compliance certifications.

## Part E — Why this sequencing

- **0a/0b/0c before code:** every expensive change in both review passes traces
  to a model decided implicitly. Decide identity/authz/scope/data-class first.
- **Scope model in Phase 1:** the `/24` assumption must never propagate; typed
  segments + interface enumeration are the foundation self-scan and connect
  build on.
- **Queue (Phase 4) before connect (Phase 6):** results must have somewhere
  durable to go before the uplink can lose them.
- **Signing/SBOM (Phase 10) gated before GA**, not after the first EDR complaint.
