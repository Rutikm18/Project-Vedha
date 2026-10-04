# Detection Engine Enhancements — gap analysis + plan

Scope: the **manager** detection engine (`manager/detection_engine/`) and the
backend detection bridge (`manager/backend/app/detection/`). The probe ships raw
facts; all detection runs here. This document is the detection-engineering review
of what we collect vs. what we actually assess, and the plan to close the gaps.

## Method

Inventoried every field each probe scanner emits (`probe/scanner/*.py`) and
cross-walked it against what the manager reads: the CVE track
(`cpe_normalizer._DISPATCH` → `matcher` → `enrichment`), the posture track
(`posture_rules.RULES` + `port_intel` exposed-services + `posture_confidence`),
and the composite layer (`backend/app/detection/attack_paths.py`).

The governing principle (already stated in `posture_rules.py`): **absent key ≠
collected-null**. A fact the manager never reads is a *guaranteed* silent
false-negative regardless of how accurate the scanner is — the host reports clean
and nothing logs an error. `test_fact_contract.test_report_unconsumed_evidence`
already prints this backlog; this plan works through it.

## Gaps found

### A. Collected-but-unconsumed facts (silent false-negatives)

| Source fact | Assessed today | Missed detection |
|---|---|---|
| `windows_inventory.inventory.defender_status` | no | **IOA** — AV / real-time protection disabled or stale (T1562.001) |
| `windows_inventory.inventory.services` (PathName) | no | unquoted service path (T1574.009), service binary in user-writable/temp dir (T1543.003) |
| `windows_inventory.inventory.local_admins` | no | excessive / unexpected local administrators |
| `windows_inventory.inventory.hotfixes` | MS17-010 only | ZeroLogon, SMBGhost, PrintNightmare, ProxyShell missing-patch state |
| `ssh_inventory.inventory.processes` / `listening_*` | no | **IOA** — miner/reverse-shell process names, rogue listeners |
| `tls_scan.certificate.public_key_bits` / `sig_algorithm` | no | weak RSA key (<2048), SHA-1/MD5-signed cert |
| `tls_fingerprint` / `ja4s` / `ja4x` | no (runs only in probe, never in prod path) | **IOC** — C2 / tooling TLS fingerprint attribution |
| `web_scan.dangerous_methods` / `security_headers_missing` | no | PUT/DELETE/TRACE enabled, missing HSTS/CSP |
| `iot_scan` MQTT `unauthenticated_access`, CoAP, RTSP, CWMP | no | unauth broker, exposed embedded management |
| `mobile_scan` ADB `unauthenticated_shell` | no | remote shell with no auth (critical) |
| `mcp_ai_scan.unauthenticated_access` | no | exposed Ollama/vLLM/MCP inference endpoint |
| `dns_scan.version_bind` / `dnssec` | zone-transfer only | BIND version disclosure, DNSSEC absent |
| `ldap_scan.anonymous_search_allowed` | anon-bind only | anonymous directory **content** disclosure (higher sev) |
| `snmp_scan.sysdescr` / `amplification_factor` | community only | system/software disclosure, amplification exposure |
| `smb_enum_scan` shares / users | null-session only | sensitive/admin share exposure, user enumeration escalation |

### B. Missing TTP / IOA correlation

- No attacker-behaviour (IOA) detection at all — AV tampering, rogue service
  binaries, unexpected listeners are invisible even with credentialed data.
- Composite attack paths number 5; missing AD-exposure, management-plane,
  data-exfil (unauth datastore + cleartext cluster), and AV-off + remote-access.
- No ATT&CK technique roll-up across findings for the exposure picture.

### C. Thin intel enrichment

- `exploitability._KEV_LINKS` links only 5 rules to KEV/EPSS; many high-signal
  weaknesses (VNC no-auth, IPMI cipher-0, unauth DB, FTP anon, RDP-no-TLS, AXFR,
  default creds) carry no exploitation evidence.
- `ja4x.SUSPICIOUS_JA4X` / `ja4s.SUSPICIOUS_JA4S` are empty stubs and never
  consulted on the manager.

## Plan / task status

- [x] **P1 — service-layer posture rules** for the unconsumed network facts in §A
      (TLS weak key/sig, web methods/headers, DNS version/DNSSEC, LDAP anon
      search, SMB sensitive shares, SNMP sysinfo/amplification, IoT MQTT/CoAP/
      RTSP/CWMP, mobile ADB, MCP/AI unauth). SUSPECTED tier. Corpus + unit tests.
- [x] **P2 — credentialed host posture / IOA** (`host_posture.py`): Defender off,
      missing critical KBs, suspicious service binaries, excessive admins, Linux
      rogue listeners/processes. CONFIRMED tier (authoritative). Traced sub-layer.
- [x] **P3 — TLS fingerprint IOC** (`fingerprint_intel.py`): JA4X/JA4S/JARM
      curated-registry matching on the manager path. SUSPECTED, tagged IOC.
- [x] **P4 — expand `_KEV_LINKS`** exploitability coverage for the high-signal
      posture rules.
- [x] **P5 — attack-path composites + ATT&CK roll-up** in the backend.

Every phase keeps the `detection_engine` suite (431 baseline) and the backend
detection tests green, and extends `tests/fixtures/probe_corpus/` so the
fact-contract gate covers each new rule input.

## Outcome (all phases shipped)

- detection_engine suite: **488 passed** (was 431); backend detection tests:
  **129 passed, 1 skipped**. The two backend collection errors
  (`test_ai_openai_tools`, `test_llm_report_fallback`) are a pre-existing
  `openai` optional-dependency gap, unrelated to detection.
- **18 new detections** across network facts (P1 ×12), credentialed host / IOA
  (P2 ×6) and TLS-fingerprint IOC (P3), plus **2 new attack-path composites**
  (P5) and an **ATT&CK tactic/technique roll-up** for reporting.
- `mcp_ai_scan` left `test_branch_rule_coverage.KNOWN_UNASSESSED` — a backlog
  item turned into a resolution. Remaining exemption: `printer_scan`.
- Honesty preserved: P4 added only genuinely-documented KEV preconditions and
  deliberately left VNC/FTP/IPMI/DB/ADB/MQTT unlinked (direct weaknesses, not
  CVE preconditions).

### Still open (future work, not silent — tracked here)

- `printer_scan` facts (PJL / IPP) remain unassessed — a rule for
  unauthenticated PJL control / exposed printer admin is the next branch to
  close.
- JA4S / JA4X IOC registries ship empty seeds; populate from a signed
  `tls_fingerprint_intel.json` feed as threat intel is curated.
- Per-CVE missing-KB mapping (ZeroLogon/SMBGhost/ProxyShell patch state) was
  deliberately NOT implemented in P2 — it needs the KB-supersedence chain to
  avoid false "unpatched" accusations; the MS17-010 composite remains the one
  case proven from data on hand.

## Design rules honoured (unchanged from the engine's existing discipline)

- Absent required input → `MISSING_INPUT` drift, never a silent clean.
- No evidence, no finding (Finding/PostureFinding invariant reused).
- A detector NEVER guesses: an uncatalogued / unparseable input stays silent
  (asymmetry favours silence — a false accusation destroys trust in every finding).
- Confidence (true-positive likelihood) stays separate from impact (risk score).
- Validated/credentialed sources → CONFIRMED; everything else → SUSPECTED.
