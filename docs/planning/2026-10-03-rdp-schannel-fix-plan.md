# RDP / SCHANNEL inner-TLS measurement — Build Plan (status gap #3)

**Status:** Build plan. Implementation proceeds phase by phase in `probe/`
(two-tree: `scanner/` + byte-identical `main_scripts/`), each phase tested and
committed. **Date:** 2026-10-03 · **Branch:** `claude/serene-bardeen-1uqxzq`

## Research summary (done)

**Gap (confirmed in code).** `probe/scanner/tls_scanner.py` grades TLS
versions/ciphers/cert, but the deep-scan router never routes it to **3389** (RDP
tunnels TLS inside its own protocol), so the SCHANNEL protocol/cipher set behind
RDP is never measured. `rdp_scanner.py` already does the X.224 negotiation and
reports `selected_protocol` / `nla` / `tls` / `standard_rdp_security` /
`nla_required`, but stops before the crypto.

**Key enablers found.**
- When RDP selects `PROTOCOL_SSL` (0x01) or `PROTOCOL_HYBRID(_EX)` (0x02/0x08),
  the server then expects a standard TLS ClientHello **on the same socket**. So
  measuring SCHANNEL = negotiate RDP→SSL, then run the ordinary TLS version/cipher/
  cert enumeration over that socket.
- `tls_scanner._try_version` / `_get_cert_der` / `_scan_tls_sync` already do all the
  TLS work — but they each open their own `socket.create_connection`. Making the
  connection step **injectable** lets `rdp_scanner` reuse 100% of the TLS logic
  (versions, cipher classification, cert parse, JA4X, posture grade) over an
  RDP-negotiated socket, with zero duplication.
- `findings.py::_rule_tls` keys on `scanner == "tls_scan"`. If `rdp_scanner` emits
  the SCHANNEL facts as a **`tls_scan`-typed** ScanResult on port 3389, the existing
  TLS findings rules (`POSTURE-TLS-DEPRECATED-VERSION`, `-WEAK-CIPHER`,
  `-SELF-SIGNED`, cert/sig/key rules, JA4X) grade it automatically — **gap #3 closes
  with no new findings rule.**

**Two-tree + gates.** `scanner/` and `main_scripts/` copies of `tls_scanner.py`,
`rdp_scanner.py`, `findings.py` are byte-identical (enforced by
`tests/test_two_tree_parity.py`); every edit is mirrored. The `rdp` branch is
already in the `it` profile (`gates.PROFILE_DEEP_BRANCHES`), so no routing change is
needed — the RDP branch itself produces the SCHANNEL fact.

## Phases (small, prioritized, one commit each)

### Phase 1 — make the TLS handshake connection injectable  *(pure refactor)*
- Add an optional `connect` hook to `tls_scanner._try_version`, `_get_cert_der`,
  `_scan_tls_sync` (default: today's `socket.create_connection`). No behaviour
  change for existing callers.
- Mirror to `main_scripts/`. Tests: existing TLS tests stay green; add a test that a
  custom `connect` hook is used.
- **Exit:** targeted TLS + parity suites green.

### Phase 2 — RDP inner-TLS (SCHANNEL) enumeration
- `rdp_scanner._rdp_tls_connect(host, port, timeout)`: fresh connection → X.224 CR
  offering SSL|HYBRID|HYBRID_EX → read CC → if a TLS-capable protocol was selected,
  return the live socket (ready for ClientHello); else close and raise.
- `RDPScanner`: when the posture shows `tls=True`, run
  `_scan_tls_sync(target, port, timeout, connect=_rdp_tls_connect)` and emit an
  ADDITIONAL `ScanResult(scanner="tls_scan", port=3389, data={**tls_info,
  "transport": "rdp"})` alongside the existing rdp_scan result. Collection-only:
  extra read-only handshakes, no credentials.
- Mirror to `main_scripts/`. Unit tests with a monkeypatched connect + fake TLS.
- **Exit:** targeted suites green.

### Phase 3 — findings wiring + grade verification
- Confirm `_rule_tls` grades the RDP-transport TLS fact (add a test feeding a
  deprecated-TLS SCHANNEL fact → asserts `POSTURE-TLS-DEPRECATED-VERSION` fires).
- Keep the `transport: "rdp"` marker in evidence so a report distinguishes SCHANNEL
  from a normal 443 TLS finding.
- **Exit:** targeted suites green.

### Phase 4 — two-tree parity + wiring gate + full probe suite
- Run `test_two_tree_parity`, `test_tier1_wiring_gate`, and the full probe suite;
  fix any wiring/parity gaps. Update `docs/STATUS.md` gap #3.
- **Exit:** full probe suite green; commit + push.

## Scope / invariants
- Collection-only: read-only handshakes, no credentials, no exploitation; ScopeGuard
  + rate limits via BaseScanner (unchanged).
- Each `_scan_tls_sync` over RDP does ≤4 version probes + 1 cert fetch = ≤5 fresh
  RDP negotiations per host — acceptable for a deep branch on a few hosts.
- Deliberately **out of scope for now** (documented follow-on): legacy *standard-RDP*
  encryption-level detection (RC4 40/56/128, FIPS-3DES) — that lives in the MCS
  Connect / Server Security Data block, a deeper handshake than X.224; the SSL/HYBRID
  SCHANNEL grading is the high-value 80% and the reported gap.
- Every edit mirrored byte-identically into `main_scripts/`; baseline targeted
  suite = 124 passed.
