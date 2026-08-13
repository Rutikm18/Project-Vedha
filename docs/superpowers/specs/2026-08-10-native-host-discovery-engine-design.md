# Native Multi-Probe Host-Discovery Engine — Design Spec

**Date:** 2026-08-10
**Area:** `probe/` — network discovery module (core-level, backend + frontend surfacing)
**Status:** Approved for implementation (brick-by-brick, checkpoint after each)

---

## 1. Problem

Today `probe/scanner/host_discovery.py` (`HostDiscoveryScanner`) determines liveness
with a **single stimulus type**: an unprivileged TCP `connect()` to 8 fixed ports
(`80,443,445,22,3389,53,135,139`). Any response — SYN/ACK **or** RST — counts as
alive; silence on all 8 = `filtered`. Its own docstring concedes: *"For ICMP/ARP-based
discovery use nmap_wrapper.py."*

This structurally under-reports live hosts. The research-backed "verified best method"
(playbook `01_network_discovery.md` §11; Bano et al., *Scanning the Internet for
Liveness*, SIGCOMM CCR 2018) is **multi-protocol liveness fusion**: *no single probe
type sees all live hosts.* The current engine misses:

- Hosts that drop all TCP but answer **ICMP echo / timestamp**.
- On-LAN hosts reachable via **ARP / NDP** — the playbook's "ground truth, unfilterable"
  method (L3 firewalls cannot filter ARP; a host that ignores every ping must still ARP
  to function on the LAN). ARP also yields a free **MAC→vendor (OUI)** fingerprint.
- Hosts reachable only via a **UDP** service (DNS/SNMP/NTP) or that reveal themselves via
  an **ICMP port-unreachable**.
- The free fingerprint signal in *how* a host replies: **TTL→OS family**, MAC→vendor.

**Goal:** build this capability *natively inside the probe* — no dependency on `nmap` or
`masscan` — while preserving the probe's hard guarantees (scope-gating, rate governance,
OT passive-only) and never regressing the unprivileged path.

## 2. Non-goals

- Not reworking port scanning, service ID, or the deep scanners (separate bricks/modules).
- Not changing the sealed container's default privileges. Raw probing is **opt-in** via a
  documented capability grant; absent it, the engine behaves exactly as today.
- Not building CVE correlation / risk scoring (explicitly a separate, out-of-scope layer).
- Not reworking the frontend's TypeScript scan engine (`manager/frontend/lib/engine/*`);
  the frontend brick only **surfaces** the new discovery evidence.

## 3. Constraints discovered in the codebase (load-bearing)

1. **Integration seam:** `HostDiscoveryScanner` (class name + async `scan_target(target)
   -> list[ScanResult]` contract + `ScanResult` schema) is consumed by `pipeline.py`,
   the `run_scan.py` registry, and the workflow `STAGE_HOST_DISCOVERY` stage
   (`workflow/modes.py`). Preserve all three and the drop-in is wiring-free.
2. **Privilege reality:** the sealed container runs as `USER 10001:10001`
   (`probe/Dockerfile`, `Dockerfile.sealed`) with **no `NET_RAW`** capability
   (`docker-compose.yml` adds none). Raw ICMP/ARP/SYN therefore require an explicit
   `setcap cap_net_raw+ep <binary>` or `--cap-add=NET_RAW` / compose `cap_add`.
3. **Downstream depends on `status` semantics:** `agent/engine.py` (~line 262) treats a
   host-discovery `status="filtered"` specially (negative/ambiguous → re-probe later).
   The new engine MUST keep emitting `status="open"` (alive) / `status="filtered"`
   (silent). All new richness is *additive* inside `data`.
4. **Safety invariants:** `ScopeGuard` gates every target; `RateLimiter` paces every
   network op; the **`ot` profile is passive-only** and must never invoke active raw
   discovery; the `iot` profile must stay gentle (small probe set, low rate).
5. **Zero third-party imports** in the scanner core today (pure stdlib). The native engine
   must stay pure-stdlib (`socket`, `struct`, `asyncio`, `fcntl`/`ctypes` only as needed).

## 4. Design

### 4.1 Capability tiers (auto-detected at runtime, silent graceful downgrade)

| Tier | Precondition | Probe set |
|---|---|---|
| **A** | root or `CAP_NET_RAW`, target on-LAN | ARP/NDP + ICMP echo/ts + TCP SYN/ACK + UDP; +MAC/vendor, +TTL→OS |
| **B** | root or `CAP_NET_RAW`, routed target | ICMP echo/ts + TCP SYN + TCP ACK + UDP |
| **C** | Linux unprivileged ICMP allowed (`ping_group_range`) | `SOCK_DGRAM`+`IPPROTO_ICMP` echo + TCP connect + UDP-reply |
| **D** | no privilege | **today's TCP-connect method, unchanged (zero regression)** |

Tier selection is per-target-aware (on-LAN vs routed) but the raw-socket capability is
process-global. Downgrade is logged at INFO, never a hard failure.

### 4.2 Probe set

| Probe | Proof-of-life | Privilege | Fingerprint yield |
|---|---|---|---|
| **ARP** (IPv4, on-LAN) | `is-at` reply | CAP_NET_RAW (AF_PACKET) | MAC → OUI vendor |
| **ICMPv6 NDP** (IPv6, on-LAN) | neighbor advertisement | CAP_NET_RAW | MAC → vendor |
| **ICMP echo (8)** | echo reply | raw, or Tier-C DGRAM-ICMP | TTL → OS family |
| **ICMP timestamp (13)** | timestamp reply | raw | catches ACLs that forget type 13 |
| **TCP SYN** → 443,80 | SYN/ACK **or RST** | CAP_NET_RAW | TTL, window → OS hint |
| **TCP ACK** → 80 | RST (slips stateless filters) | CAP_NET_RAW | — |
| **UDP** → 53,161,123 | protocol reply **or** ICMP port-unreach | reply=unpriv; port-unreach=raw | — |
| **TCP connect** (existing) | connect OK or RST | none | — |

**Fusion rule (per playbook §11.2):** fire the selected probes concurrently; **any**
positive reply OR host-sourced negative (RST, ICMP-unreachable *from the target*) ⇒
alive. Record the full per-probe outcome vector as evidence, and the *strongest* proof as
the headline `method`/`reason`.

### 4.3 Module structure — `probe/scanner/discovery/` (new package)

Each unit has one purpose, a narrow interface, and is testable in isolation:

- `capabilities.py` — `detect() -> Capabilities`: root/`CAP_NET_RAW`, unpriv-ICMP
  availability, per-target on-LAN vs routed (via local interface/route table + subnet
  match). Pure logic over injectable inputs (no side effects at import).
- `raw_socket.py` — low-level core: build/parse Ethernet/ARP/IPv4/IPv6/ICMP/ICMPv6/TCP/UDP
  headers, checksum helpers, raw send + async recv with BPF-style match. **The heart of the
  "core-level tech."** Pure byte functions + thin socket wrappers.
- `probes/` — one file per probe (`arp.py`, `ndp.py`, `icmp.py`, `tcp_raw.py`,
  `udp_probe.py`, `connect.py`), each exposing a uniform
  `async def probe(ctx, target) -> ProbeOutcome`.
- `fusion.py` — `ProbeOutcome` dataclass + `fuse(outcomes) -> LivenessVerdict`
  (verdict, method, reason, liveness_vector, fingerprints). Pure, table-driven.
- `engine.py` — the new `HostDiscoveryScanner(BaseScanner)`: picks the tier from
  `capabilities`, selects the probe set (honoring profile gentleness), runs `fusion`,
  emits `ScanResult`.

`probe/scanner/host_discovery.py` becomes a **thin re-export shim**
(`from .discovery.engine import HostDiscoveryScanner, PROBE_PORTS`), so every existing
import, the `run_scan.py` registry, `pipeline.py`, the workflow stage, and
`tests/test_probe_core.py` keep working unchanged.

### 4.4 Schema (additive, backward compatible)

```jsonc
{
  "scanner": "host_discovery",
  "target": "10.0.0.5",
  "status": "open",                 // "open" = alive, "filtered" = silent (UNCHANGED)
  "data": {
    "alive": true,                  // kept
    "responding_ports": [ ... ],    // kept for compat
    "method": "arp",                // NEW: strongest proof-of-life
    "reason": "arp-reply",          // NEW: syn-ack | rst | icmp-echo-reply | icmp-port-unreach | ...
    "liveness_vector": {            // NEW: every probe's outcome (the fingerprint)
      "arp": "reply", "icmp_echo": "reply", "tcp_syn_443": "rst",
      "tcp_connect_80": "no-response", "udp_53": "no-response"
    },
    "mac": "00:0c:29:ab:cd:ef",     // NEW: when ARP/NDP available
    "vendor": "VMware, Inc.",       // NEW: OUI lookup (small local prefix table)
    "ttl": 64, "os_hint": "linux",  // NEW: TTL→OS family (64=nix,128=win,255=netgear)
    "capability_tier": "A"          // NEW: which tier actually ran
  },
  "evidence": "arp is-at 00:0c:29:ab:cd:ef; icmp echo reply (ttl 64)"
}
```

### 4.5 Safety wiring

- ScopeGuard `assert_in_scope` before any probe (inherited from `BaseScanner._guarded`).
- Every raw send goes through `self.limiter.wait()` and `self.sem` — raw probes count the
  same as connects, so `--rate`/`--concurrency` still cap total network pressure.
- **OT gate unchanged:** `ot` profile runs `passive_collector` only; the engine refuses to
  run active raw probes under an OT profile (assert + hard error, mirroring the existing
  structural gate). `iot` profile → Tier-limited gentle set (ICMP echo + connect + a tiny
  UDP set; **no** TCP SYN/ACK storms), low rate.

### 4.6 Frontend (`manager/frontend`, Next.js)

Surface the new evidence in the discovery/host results view (`app/scan`, `app/findings`,
`lib/scan-*`): per-host chips for `method`/`reason`, MAC + vendor, OS hint, capability
tier, and an expandable **liveness vector** (which probes answered). Adapter/normalizer in
`lib/` maps the new `data.*` keys; a JSONL fact with only the legacy keys must still render
(graceful for Tier-D probes). Exact component wiring is finalized in the frontend brick
after reading the current discovery view.

## 5. Testing deliverables (explicitly requested)

Layered, matching existing conventions (`selftest_live.py` PASS/FAIL style, pytest,
`test_all.sh` shell harness):

1. **Golden-vector unit tests** — `tests/test_discovery_packets.py`: assert exact bytes of
   built ARP/ICMP/ICMPv6/TCP-SYN/UDP packets and correct parsing of canned reply buffers
   (checksums included). Fully deterministic, **no network**, runs in CI everywhere.
2. **Capability + fusion unit tests** — `tests/test_discovery_fusion.py`: table-driven —
   given a set of `ProbeOutcome`s, assert the fused verdict/method/reason/vector; and
   `capabilities.detect()` over mocked euid / socket-availability / route inputs.
3. **Tier reporter script** — `probe/discovery_probe_check.py`: prints the detected
   capability tier, which probes are available, and *why* (root? CAP_NET_RAW? unpriv-ICMP?
   on-LAN?). Operator/debug aid; exits 0.
4. **Live accuracy harness** — `probe/discovery_selftest.py` (sibling to
   `selftest_live.py`): stands up local fixtures (a listening TCP port, a UDP responder,
   loopback), runs the engine, and asserts liveness is detected via the expected method for
   the current tier; asserts scope/exclude refusals still hold; CI-friendly PASS/FAIL, exit
   non-zero on any failure. Capability-gated tiers (A/B) are **skipped, not failed**, when
   unprivileged — same opt-in pattern as the SSH/WinRM tests.
5. **Shell smoke harness** — `probe/test_discovery.sh`: one command that runs the unit
   tests + tier reporter + live selftest and prints a pass/fail summary; wired so it can be
   called from the existing `test_all.sh`.

## 6. Build sequence (bricks — checkpoint after each)

1. **Brick 1 — skeleton + capabilities + shim.** New package, `capabilities.py`,
   `fusion.py` scaffolding, `engine.py` that (for now) runs only the connect probe →
   **Tier D output byte-identical to today**. Shim re-export. Golden-vector harness
   scaffolding + capability/fusion tests. *Zero behavior change; proves the seam.*
2. **Brick 2 — raw core + ICMP.** `raw_socket.py` + `icmp.py` (echo+timestamp, raw and
   Tier-C DGRAM). Fuse {connect, icmp}. Golden-vector tests for ICMP build/parse. First
   real accuracy gain (ICMP-only hosts).
3. **Brick 3 — TCP SYN/ACK raw probes** into fusion. TTL/window→OS hint. Tests.
4. **Brick 4 — ARP (on-LAN ground truth)** + MAC parse + OUI vendor table + wire
   MAC/TTL fingerprints into the schema. Tests.
5. **Brick 5 — UDP fusion + IPv6 NDP.** ICMP port-unreach detection; NDP for on-LAN v6.
   Tests.
6. **Brick 6 — frontend surfacing** of the new evidence + `test_discovery.sh` integration +
   deploy note (`setcap` / `cap_add`) documented in `PROBE_RUNBOOK.md` / `CURRENT_STATE.md`.

Each brick: TDD (tests first where practical), keep the module green, update
`CURRENT_STATE.md`.

## 7. Risks & mitigations

- **Raw sockets differ across OS (Linux AF_PACKET vs macOS BPF).** Mitigation: dev/CI is
  macOS but the shipped probe is Linux; `raw_socket.py` targets Linux for AF_PACKET/ARP and
  degrades to Tier C/D on macOS dev boxes. Golden-vector tests are OS-independent (pure
  bytes); live raw tests are capability/OS-gated skips.
- **Regression risk on the critical discovery path.** Mitigation: Brick 1 keeps Tier D
  byte-identical and lands behind the existing test suite before any raw code exists.
- **Rate/safety on wide ranges.** Mitigation: raw sends counted by the shared limiter/sem;
  `iot` gentle set; `ot` hard-gated to passive.
- **Non-determinism of live LAN discovery** (already documented in `CURRENT_STATE.md`).
  Mitigation: live harness asserts *method reached the engine*, not exact host counts.

## 8. Definition of done

- All 6 bricks merged; `CURRENT_STATE.md` updated to describe the tiered native engine.
- Existing probe test suite green; new discovery unit tests + live selftest green (Tier D/C
  in CI, A/B verified locally with `CAP_NET_RAW`).
- `HostDiscoveryScanner` public contract unchanged; no downstream wiring edits required.
- Frontend renders the new evidence and still renders legacy-only records.
- Deploy note documents the one-line capability grant to unlock raw tiers.
