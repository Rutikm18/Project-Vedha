# Network Scanner Hardening Plan
## `probe/main_scripts/` — Offensive-security accuracy pass

---

## Context

The scanner tree under `probe/main_scripts/` is a reference implementation of a
network vulnerability assessment engine. Every observation it makes is
*vantage-relative* and *evidence-backed*. The 30-step plan below drives it from
a prototype that collapsed ambiguous states into confident ones, toward a tool
where ambiguity is a first-class output.

**Working tree:** `probe/main_scripts/`  
**Tests:** `probe/tests/test_main_scripts_hardening.py` (imports `main_scripts.*` directly)  
**The parallel `probe/scanner/` tree** is what production and CI actually run — the
same fixes should eventually be ported there.

---

## Status legend

| Symbol | Meaning |
|--------|---------|
| ✅ DONE | Verified in code — correct behaviour confirmed |
| 🔧 FIXED | Had a bug this session — now fixed + tested |
| ❌ OPEN | Confirmed gap, not yet implemented |
| ⚠️ PARTIAL | Code exists but has a known deficiency |
| 🚫 LIMITATION | Structurally impossible without privileges or live infra |

---

## Step-by-step status

### Step 1 — Audit `scanner_base.py`
**Status: ✅ DONE**

`BaseScanner`, `ScopeGuard`, `RateLimiter`, `ResultWriter`, `expand_targets`, `parse_ports`
all reviewed. Scope enforcement and rate governance are intact. The target-level
sliding window (`run()`) keeps inflight task count bounded. No safety regressions.

---

### Step 2 — Improve `ScanResult` schema
**Status: ✅ DONE**

`ScanResult.data` carries: `reason`, `method`, `confidence`, `rtt_ms`, `attempts`,
`family`, `src_ip`, `vantage`, `errno`. `status` = state only; diagnostic detail
lives in `data`. Evidence is a human string; `error` holds the raw exception string.

---

### Step 3 — Fix TCP port state handling
**Status: ✅ DONE**

`_ERRNO_MAP` in `port_scanner.py` maps every meaningful errno to a distinct state:

```
ECONNREFUSED  → closed  / connection_refused
ECONNRESET    → closed  / connection_reset
ETIMEDOUT     → filtered / no_response
EHOSTUNREACH  → unreachable / host_unreachable
ENETUNREACH   → unreachable / network_unreachable
EHOSTDOWN     → unreachable / host_down
EACCES/EPERM  → error  / permission_denied
EMFILE/ENFILE → error  / local_resource_error
EADDRNOTAVAIL → error  / address_unavailable
(other)       → error  / os_error     ← NEVER filtered
```

---

### Step 4 — Preserve complete TCP scan state internally
**Status: 🔧 FIXED this session**

`ScanMetrics.record()` now tallies EVERY terminal result **before** any
`report_closed` output filtering, so the engine never loses a closed/filtered/
error observation. `report_closed` filters output only. The completeness
invariant `requested == attempted == classified` is asserted in the summary
(`complete: true/false`) and covered by `test_main_scripts_coverage.py`.

---

### Step 5 — Full-port scan profile
**Status: 🔧 FIXED this session** (named profiles added)

`--profile quick|top100|top1000|full|custom` now resolves via `resolve_profile()`:
- `full` = `range(1, 65536)` (tested: first=1, last=65535, unique=65535)
- `top100` = nmap canonical top-100 (incl. 49152-49157 dynamic RPC low block)
- `top1000` = well-known 1-1024 ∪ top-100 ∪ Windows extras (2179/5040/7680/47001/49664+)
- `custom` = explicit `-p` (de-duplicated; errors if `-p` missing)

`--all-ports` and `-p` still work for backward compatibility.

---

### Step 6 — Replace 65,535 task fan-out
**Status: 🔧 FIXED this session**

`scan_target()` now drains an `asyncio.Queue` of ports with a fixed pool of
`min(concurrency, n_ports)` workers — at most `concurrency` per-port coroutines
are live at once (bounded memory + backpressure). Each port is dequeued exactly
once → one terminal result; clean cancellation on interrupt.

Tests (`test_main_scripts_coverage.py`):
- `test_all_65535_ports_scheduled_exactly_once` — full profile, every port once
- `test_concurrency_is_bounded_by_the_pool` — semaphore neutralised, peak in-flight ≤ pool size
- `test_every_port_scanned_exactly_once` — no drops, no duplicates

---

### Step 7 — RTT / duration measurements
**Status: ✅ DONE**

`time.monotonic()` used in `_attempt()`. `rtt_ms` stored in `data` for all
non-cancelled outcomes (open, filtered, closed, unreachable, error).

---

### Step 8 — Conservative timeout retry
**Status: ✅ DONE**

`_scan_port()` retries **only** `filtered/no_response` up to `self.retries` times
(default 1). Definitive `closed`, `unreachable`, and `error` states are never
retried. `attempts` count stored in `data`.

---

### Step 9 — Scan metrics
**Status: 🔧 FIXED this session**

`ScanMetrics` emits a terminal `ScanResult(status="scan_summary", ...)` per target:
```json
{
  "ports_requested": 65535, "ports_attempted": 65535, "ports_not_scanned": 0,
  "classified": 65535, "open": 5, "closed": 65200, "filtered": 320,
  "unreachable": 0, "error": 10, "retries": 320, "local_resource_errors": 0,
  "duration_s": 12.4, "complete": true, "health": "ok"
}
```
`health` flips to `"degraded"` on any local-resource error (fd/buffer exhaustion),
and `complete: false` surfaces a partial scan (`attempted != requested`).

---

### Step 10 — IPv4 / IPv6 handling
**Status: ✅ DONE**

`_family_of()` resolves `ipv4`/`ipv6` from the actual connected peer address.
`data["family"]` is set on every result. The two families are never conflated.
`--ipv4`/`--ipv6` CLI flags are **not yet exposed** (but the engine records
correctly).

---

### Step 11 — Source / vantage information
**Status: ✅ DONE**

`data["vantage"]` = hostname of scanner (or `--vantage` override).  
`data["src_ip"]` = local socket address that completed the connection.  
Multiple vantage observations are kept independent — no collapse.

---

### Step 12 — Fix SMB scanner parsing
**Status: 🔧 FIXED this session**

**Root cause (two-part):**
1. Request advertised SMB 3.1.1 (`0x0311`). MS-SMB2 requires a preauth-integrity
   negotiate context with 3.1.1; without it Windows returns `STATUS_INVALID_PARAMETER`
   (an error response, not a negotiate).
2. Parser read `SecurityMode` / `DialectRevision` from offsets 70/72 of that error
   body — which produces `signing=false`, `dialect=0x0000`.

**Fix applied:**
- Request now advertises only `[0x0202, 0x0210, 0x0300, 0x0302]`.
- `parse_smb2_security_mode()` validates `Status == 0`, `Command == 0`, and
  `body_structure_size == 65` before trusting those offsets.
- An error response returns `signing_parsed: False, reason: not_a_successful_negotiate`.

---

### Step 13 — Separate SMB configured vs negotiated state
**Status: 🔧 FIXED this session**

Fields renamed:
```
signing_supported  = SecurityMode bit 0 (SMB2_NEGOTIATE_SIGNING_ENABLED)
signing_required   = SecurityMode bit 1 (SMB2_NEGOTIATE_SIGNING_REQUIRED)
signing_enabled    = deprecated alias for signing_supported (kept for compatibility)
negotiated_dialect = e.g. "0x0302"
security_mode_raw  = raw hex for forensic evidence
```

Ground truth verified against `Get-SmbServerConfiguration`:
```
EnableSecuritySignature  : True   → signing_supported: true  ✓
RequireSecuritySignature : True   → signing_required:  true  ✓
```

---

### Step 14 — Fix UDP state model
**Status: 🔧 FIXED this session**

**Before:** `status="filtered"` for no-reply (evidence text contradicted it).  
**After:** `status="open|filtered"`, `data.reason="no_response"`.

Correct model now in `udp_scanner.py`:
```
valid UDP response   → open
ICMP port-unreach   → closed   (via _UDP_CLOSED sentinel)
no response         → open|filtered  ← FIXED
ICMP admin prohibit → filtered (if platform surfaces it)
```

---

### Step 15 — Capture ICMP errors for UDP
**Status: ✅ DONE (unprivileged path)**

`async_udp_probe` in `scanner_base.py` uses the event-loop's UDP protocol and
surfaces `_UDP_CLOSED` when an ICMP port-unreachable is returned by the OS.
`ICMP administratively prohibited` is documented as a limitation — raw ICMP
socket correlation requires privileges on most platforms.

---

### Step 16 — Protocol-specific UDP probes
**Status: ✅ DONE**

`UDP_PROBES` in `udp_scanner.py`:
```
53    DNS (valid query)
123   NTP (monlist / version request)
137   NetBIOS Name Service
161   SNMP (v1 get-request, community "public")
500   IKE (SA_INIT)
1900  SSDP (M-SEARCH)
4500  IKE NAT-T
5353  mDNS (PTR query)
5060  SIP (OPTIONS)
69    TFTP (RRQ)
11211 Memcached (stats)
```

Each has a payload builder; service is confirmed from protocol response, not
assumed from port number.

---

### Step 17 — Improve SNMP scanner semantics
**Status: 🔧 FIXED this session**

`snmp_scanner.py` no-response branch now returns `status="open|filtered"` with
`data.reason="no_snmp_response"` (was `filtered`). A silent agent that rejects our
communities/versions no longer masquerades as a firewall — consistent with the
Step 14 UDP semantics.

---

### Step 18 — Improve `service_banner` scanner
**Status: ⚠️ PARTIAL**

Generic banner scanner exists. A port-to-deep-scanner routing table is described
in `scan_funnel.py` but the mapping is not exhaustive. Ports 445/3389/135 that
return no banner on raw connect are not treated as failures (correct), but are not
automatically handed off to their protocol scanner from within `service_banner.py`
itself.

---

### Step 19 — RDP protocol scanner
**Status: ❌ OPEN**

TCP/3389 is confirmed open but no RDP handshake scanner exists in `main_scripts/`.
Needed: safe RDP X.224 Connection Request → negotiation response → read
`NEG_RSP` for security layer flags (TLS/CredSSP/NLA). No auth, read-only.

---

### Step 20 — RPC endpoint identification
**Status: ❌ OPEN**

TCP/135 is confirmed open but no MSRPC endpoint mapper scanner exists.
Needed: safe DCE/RPC bind to the EPM interface (UUID `e1af8308-...`), enumerate
endpoint entries. Read-only, no exploitation.

---

### Step 21 — Improve OS fingerprint confidence
**Status: 🔧 FIXED this session**

**Before:** TTL-alone produced `confidence: 1.0`.  
**After:** confidence capped by corroborating signal count:

| Independent signals | Max confidence |
|---------------------|---------------|
| 1 (e.g. TTL only)   | 0.50          |
| 2 (TTL + window)    | 0.80          |
| 3+                  | 0.95          |

`signals["support_count"]` exposed so callers know what backed the guess.

Example — Windows 11 target:
```
TTL 128 only       → Windows, confidence 0.50  (before: 1.0)
TTL 128 + win 8192 → Windows, confidence 0.80
```

---

### Step 22 — TLS scanner legacy protocol handling
**Status: ⚠️ PARTIAL**

`tls_scanner.py` tests legacy versions. OpenSSL deprecation warnings for TLSv1/1.1
are not suppressed blindly, but the distinction between "target refused" and
"local OpenSSL doesn't support it" is not always surfaced cleanly in the output.

---

### Step 23 — Scanner pipeline (open ports feed deep scanners)
**Status: ⚠️ PARTIAL**

`scan_funnel.py` implements the pipeline concept — host discovery → port scan →
route to service scanners. The routing table exists but is not exhaustive
(missing RDP, RPC routers). Standalone execution of each scanner is preserved.

---

### Step 24 — Normalized evidence model
**Status: ✅ DONE**

Every `ScanResult` carries:
```json
{
  "target": "...",
  "proto": "tcp",
  "port": 445,
  "status": "open",
  "data": { "reason": "connect_success", "method": "connect", ... },
  "evidence": "tcp connect completed (3-way handshake)",
  "error": null
}
```

---

### Step 25/26 — TCP and UDP accuracy harnesses
**Status: ❌ OPEN**

No reusable harness compares scanner output against an independent reference (e.g.
nmap) and classifies TP/FN/FP. Mock-based unit tests exist but a controlled
validation harness (with known-open, known-closed, known-filtered ports) is not
yet written.

---

### Step 27 — Regression tests
**Status: ✅ PARTIAL (new file covers Phase-1 areas)**

`tests/test_main_scripts_hardening.py` — 10 tests:
- UDP: silence → `open|filtered`, ICMP → `closed`
- OS: single TTL capped ≤ 0.5, two signals > one, no-signal → unknown
- SMB: error-body not trusted, success body decoded, 3.1.1 excluded from request

**Still needed:** Step 6 (bounded worker), Step 9 (metrics completeness), Step 4
(no silent drops), Steps 19/20 (RDP/RPC), SNMP no-reply fix.

---

### Step 28 — Compare against nmap
**Status: 🚫 LIMITATION (live-infra dependency)**

Requires an authorized target and nmap on the same host. When results differ:
inspect packet evidence → determine ground truth → document. Not automatable in
unit tests.

---

### Step 29 — Module separation
**Status: ✅ DONE**

Clean boundaries are maintained:
```
host_discovery   → liveness
port_scanner     → TCP reachability
udp_scanner      → UDP state
service_banner   → protocol fingerprint
smb_scanner      → SMB config
os_fingerprint   → OS family inference
scan_funnel      → orchestration
```
No vulnerability conclusions in collection modules.

---

### Step 30 — Final verification report

#### Files changed (this session)
| File | Change |
|------|--------|
| `main_scripts/udp_scanner.py` | Step 14: silence → `open\|filtered` |
| `main_scripts/os_fingerprint.py` | Step 21: confidence cap by corroboration |
| `main_scripts/smb_scanner.py` | Steps 12/13: parser guard + drop 3.1.1 from request |
| `main_scripts/port_scanner.py` | Steps 4/5/6/9: profiles, bounded worker pool, `ScanMetrics` completeness/health |
| `main_scripts/snmp_scanner.py` | Step 17: no-response → `open\|filtered` |
| `main_scripts/device_classifier.py` | **NEW** — device-role inference (workstation/server/network_device/printer/hypervisor/iot) |
| `main_scripts/vantage_matrix.py` | **NEW** — multi-vantage reconciliation + external-exposure verdict |
| `tests/test_main_scripts_hardening.py` | 10 tests (UDP/OS/SMB) |
| `tests/test_main_scripts_coverage.py` | 12 tests (profiles / worker pool / metrics) |
| `tests/test_main_scripts_device.py` | 10 tests (device classification) |
| `tests/test_main_scripts_vantage.py` | 7 tests (multi-vantage reconciliation) |

**Test totals:** 39 new tests pass · 84/84 in the relevant regression subset · no regressions.

---

## Use-case coverage matrix

| Priority | Use case | Module | Status |
|----------|----------|--------|--------|
| P0 | Host discovery | `host_discovery.py` | ✅ vantage-aware reachability states |
| P0 | TCP port discovery | `port_scanner.py` | ✅ evidence-based states + reasons |
| P0 | UDP discovery | `udp_scanner.py` | ✅ open / closed / open\|filtered |
| P0 | Full 65,535 TCP scan | `port_scanner.py --profile full` | ✅ bounded worker pool + completeness |
| P0 | Service detection | `service_banner.py` | ✅ `match_service` (behaviour, not port#) |
| P0 | Version detection | `service_banner.py` | ✅ OpenSSH/IIS/nginx/MySQL version groups |
| P0 | Protocol detection | `service_banner.py` + `web_scanner.py` | ✅ HTTP probe on non-standard ports |
| P0 | OS fingerprint | `os_fingerprint.py` | ✅ multi-signal, calibrated confidence |
| **P0** | **Device classification** | **`device_classifier.py`** | **🔧 NEW this session** |
| **P0+++** | **Reachability validation** | **`vantage_matrix.py`** | **🔧 NEW — external-exposure verdict** |
| **P0+++** | **Multi-vantage scanning** | **`vantage_matrix.py`** | **🔧 NEW — per-port matrix, no collapsing** |

Note: multi-vantage *execution* (actually scanning from several network positions)
is an orchestration/deploy concern; `vantage_matrix.reconcile_vantages()` provides
the pure-logic reconciliation those runs feed into.

#### Bugs fixed
| Bug | Root cause | Fix |
|-----|-----------|-----|
| UDP silence → `filtered` | No distinction between silence and ICMP-refused | Return `open\|filtered` + `reason:no_response` |
| SMB `signing=false`, dialect `0x0000` | Request offered 3.1.1 without preauth context → Windows returned error body; parser read offsets blindly | Drop 3.1.1 from request; validate `Status/Command/StructureSize` before parsing |
| SMB `signing_enabled` ambiguous name | Name didn't distinguish supported vs required | `signing_supported` / `signing_required` (alias kept) |
| OS `confidence: 1.0` from TTL alone | Score ratio with single-signal total = 1.0 | Cap by `support_count`: 1 signal → ≤ 0.5 |

#### Test results
```
test_main_scripts_hardening.py   10/10 pass
scanner/ regression suite        72/72 pass  (untouched)
```

---

## Open work (priority order)

**P0 cluster (profiles, bounded workers, completeness/health telemetry, SNMP) —
DONE this session.** Remaining, mostly P1/P2 requiring raw sockets / root / live infra:

| Priority | Step | Task | Why not yet |
|----------|------|------|-------------|
| P1 | #4 (raw SYN) | Stateless SYN breadth engine feeding the connect validator | `syn_scanner.py` exists (raw, Linux/root); needs live/priv to verify |
| P1 | #5 (ICMP) | Parse `icmp_type`/`icmp_code` (3/0, 3/1, 3/3, 3/9-13) | Raw ICMP socket → root |
| P1 | 19 (RDP) | X.224 Connection Request → NEG_RSP (TLS/CredSSP/NLA), read-only | Needs live 3389 to validate |
| P1 | 20 (RPC) | MSRPC endpoint-mapper bind on 135 → correlate 49664+ dynamic ports | Needs live 135 |
| P1 | #8 (adaptive) | Per-host SRTT/RTTVAR adaptive timeout (slow ≠ filtered) | Design ready; RTT already captured |
| P1 | 10/11 | `--ipv4/--ipv6/--family`, `--interface/--source-ip` flags | Engine records family/vantage; flags pending |
| P2 | 12/13 UDP | UDP profiles (top100/top1000/full) + DHCP(67/68) probe | Extend `UDP_PROBES` |
| P2 | 15 (service) | Generic probe-ladder service ID on every OPEN port | Route via `scan_funnel` |
| P2 | 19 OS | Multi-signal OS fp (window/MSS/WSCALE/SACK/DF/IP-ID/TCP-opt order) | Needs raw TCP option capture |
| P2 | 25/26/20 | Ground-truth TP/TN/FP/FN accuracy harness vs nmap | Live infra |

---

## Permanent constraints (never violate)

- `ScopeGuard` must be enforced on every outbound probe — never bypassed.
- Rate limiter (`RateLimiter`) must gate every socket operation.
- `report_closed=False` may filter *output*, but the engine must tally all states internally.
- Local `LISTEN` ≠ remote `OPEN`. Never infer one from the other.
- UDP silence = `open|filtered`. Never `filtered` alone.
- `OSError` → `classify_os_error()`. Never collapse to `filtered`.
- TTL alone → confidence ≤ 0.5. Never 1.0.
- SMB parse: validate successful NEGOTIATE before reading `SecurityMode`/`DialectRevision`.
- No brute-force, no authentication attempts, no exploitation, no destructive checks.
- One logical change at a time; verify after every change.
