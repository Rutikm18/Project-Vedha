# Aggressive scan redesign — enterprise breadth + capped full-port sweep

**Goal:** Aggressive stops meaning "all 65,535 ports on every host" (which breaks a /24 against the 2 h ceiling). Instead: Aggressive = a bounded, enterprise-realistic port set that finishes a /24 in the ceiling and probes *more forcefully* than Normal; full 65k moves to a separate use-case capped at ≤3 hosts.

**Decisions (confirmed with the operator):**
- Aggressive breadth = **curated enterprise set** (~2,500 ports), not 65k.
- Full 65k = a **new separate use-case**, ≤3 hosts.
- Normal already has UDP/OS-fingerprint/version/vuln capabilities; **Aggressive runs them more forcefully** (degree, not presence).

**Grounding (verified in code, not assumed):**
- `resolve_profile`: quick(15), top100, top1000(1121 = `1–1024 ∪ top100 ∪ Windows-extras`), full(65535). No frequency table.
- `network_va` (uc 12) = assessment mode → runs the full funnel incl. all 19 deep service branches (tls/web/smb/db/rdp/snmp/ssh/ldap/…) at **every** intensity; intensity only changes port breadth + rate/retries.
- OS fingerprint (`os_fingerprint.py`, active ICMP) and default-credential checks (`findings.py`, `CAT_DEFAULT_CRED`, gated by Gate-6 `cred_slots`) already run in the deep stage at every intensity.
- UDP: `udp_scanner.UDP_PROBES` has 12 services {53,69,123,137,161,500,623,1900,4500,5060,5353,11211}; the branch gate `UDP_PORTS` wires only 5 {53,123,161,137,11211}.
- There is **no** version-detection intensity knob today (banner-pattern based).
- Two-tree rule: every `probe/main_scripts/*` edit is mirrored byte-identical to `probe/scanner/*`.
- Admission: `_refuse_if_infeasible` + `MAX_TARGETS`; ceiling `PROBE_MAX_JOB_SECONDS` (2 h).

**Fit math (must hold):** enterprise ~2,500 × 254 hosts = 635,000 probes / 150 pps ≈ 70 min < 2 h ✓. Full 65k × 3 hosts = 196,605 / 150 pps ≈ 22 min ✓.

## Global Constraints
- Two-tree parity: `main_scripts/` canonical, `scanner/` byte-identical for every touched file (`cmp` + `test_two_tree_parity`).
- `.githooks` bumps VERSION (expected). Never `--no-verify`.
- Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Comment rule on touched lines: true, no plan IDs, no before/after history, no line-number citations.
- Do not weaken existing tests; a /24 aggressive must still be admitted after the change.

---

## Task 1 — `enterprise` port profile (~2,500)
**Files:** `probe/main_scripts/port_scanner.py` (+ mirror `probe/scanner/`), `probe/tests/test_port_profiles.py` (new or extend).
- Add `_ENTERPRISE_EXTRA`: curated high-value ports > 1024 that top1000 misses — alt/dev web (3000-3100, 5000-5100, 8000-8100, 8443, 8800-8900, 9000-9100, 9443), app/mgmt (5985/5986 WinRM, 8291, 8888, 9090, 9200/9300 ES, 10000, 50000), DB (1433,1521,3306,5432,5984,6379,7000-7001,8086,9042,11211,27017-27019,28017,1099 RMI), container/orch (2375-2380,4243,6443,10250-10256), VPN/remote (500,1194,1701,1723,4500,3389,5800-5810,5900-5910), messaging (2181,4369,5671,5672,15672,9092,61616), dir/mail (88,389,464,636,3268,3269), IoT/OT-adjacent (102,502,1883,8883,20000,44818,47808,5683), file/print (111,515,631,2049,9100), k8s nodeport sample (30000-30010), 50000-50010.
- `resolve_profile("enterprise")` = `sorted(top1000 ∪ _ENTERPRISE_EXTRA)`. Target 2,000–2,600 ports.
- Tests: size in [2000, 2700]; superset of top1000; contains representative enterprise ports (8443, 5985, 6443, 27017, 3389, 9092); parity.

## Task 2 — Aggressive (`deep`) uses `enterprise`, not full 65k
**Files:** `probe/workflow/intensity.py`, tests `test_intensity_envelope.py`, `test_intensity_budget.py`.
- `deep` preset: `port_profile = "enterprise"`, `first_pass_profile = None`, `max_host_seconds = None` (bounded by breadth now), keep rate 150 / concurrency 80 / timeout 4.0 / retries 2. No more two-phase for `network_va`.
- Tests: `intensity_port_override("deep")` resolves to the enterprise set (~2,500), not 65,535; `intensity_first_pass("deep")` is None; a /24 deep admission fits the 2 h ceiling (extend the admission/feasibility test).

## Task 3 — New use-case: full 65k, ≤3 hosts
**Files:** `probe/agent/engine.py` (scan_type registry, `_FORCE_PORT_PROFILE`, `_DEFAULT_INTENSITY_BY_SCAN_TYPE`, a host cap), `manager/backend/app/routers/agents.py` (uc code + name), `manager/frontend/lib/scan-launch.ts` (JOB_TYPE_MAP), tests both sides.
- New scan_type `deep_port_sweep`, use-case `uc_deep_port_sweep`, numeric code (next free, e.g. 82). Maps to `port_scan_mode`, `_FORCE_PORT_PROFILE["deep_port_sweep"]="full"`, default intensity deep, keeps the (now-safe) two-phase machinery.
- **Host cap:** refuse when resolved live/target host count > `DEEP_PORT_SWEEP_MAX_HOSTS` (default 3, env-overridable) with an actionable message (mirror `_refuse_if_infeasible` shape + `allow_infeasible`). Enforce at admission so a >3-host request is rejected before scanning.
- Tests: 3 hosts × full → admitted; 4 hosts × full → refused with the cap message; `allow_infeasible` override runs it; uc code resolves to the scan_type; frontend maps the use-case.

## Task 4 — UDP breadth scales with intensity (Aggressive "more forcefully")
**Files:** `probe/workflow/gates.py` / the UDP branch wiring, `probe/workflow/intensity.py` (a `udp_profile` field), tests.
- Normal (`standard`): narrow UDP (the current 5). Aggressive (`deep`): wide UDP = all 12 `UDP_PROBES`. Light: none/minimal.
- Wire the udp branch's port set from the intensity's `udp_profile` (fall back to the current 5 when unset, so nothing else changes).
- Tests: deep resolves the wide UDP set; standard the narrow set; branch respects it.

## Task 5 — Verify (no new scanners invented)
- OS fingerprint + default-cred already run in the deep stage at both levels; confirm they still run for Aggressive after the breadth change (existing tests + a focused check). Version-detection intensity dial is a noted follow-up (no knob exists today).

## Task 6 — End-to-end + suites
- Two-tree parity green; full probe suite (baseline 2438) green; manager auth/use-case tests green; frontend intensity/launch tests green.
- Live e2e on the fixed stack: aggressive /24 admits with ~2,500 ports (not 65k) and completes; the new deep-port-sweep admits 3 hosts full-65k and refuses 4.
