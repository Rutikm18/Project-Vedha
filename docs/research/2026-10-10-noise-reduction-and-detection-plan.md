# Reducing noise and closing detection gaps — research and plan (agent vs manager)

**Date:** 2026-10-10 · **Status:** research and plan only, no code changed.
**Input:** the first Vedha scan of the weak lab ([gap analysis](../reports/2026-10-10-newenv1-scan-gap-analysis.md)): 7 of 25 scenarios detected, 15 missed, 22 findings for about 13 issues, 39 of 83 report columns empty.
**Constraint kept:** the agent collects facts only; the manager detects, scores, explains and reports.

---

## 1. Root causes, traced to code

| Symptom in the report | Root cause | Where |
|---|---|---|
| 39 narrative/metadata columns empty | The report reads Technical details, Impact, Business impact, Exploitation, Reproduction, Root cause and Preconditions **only** from analyst/AI overrides or from values recorded in the finding's evidence. The deterministic content KB (`finding_content.py`) is never used as a source, and no producer records these values | `services/report_document.py` (around lines 1349–1375) |
| 19 of 22 findings "generic"; IPMI filed as `weak_tls`, the management-plane correlation as `exposed_rdp` | Category comes from **keyword matching on free text** (first match wins). "cipher suite" in the IPMI text matches the TLS keywords; "RDP" in the correlation's remediation matches `exposed_rdp`. The KB has only 9 categories | `services/remediation_kb.py` `_CATEGORY_KEYWORDS`, `classify_finding` |
| Structured recommendations `[]`, one-line remediation | Recommendations come from remediation plan rows, which are not created automatically for detection findings. The recipes keyed by category exist but are not attached | `report_document._remediation`, `remediation_kb.RECIPES` |
| Medium findings (285) outrank Criticals (≤274) | The 0–1000 rank weights evidence/verification 15% and treats verification state as a strong multiplier. Port-derived signals are stored as `confirmed`, so they collect the full evidence weight, while open Criticals sit at the default 0.65. Severity is only 40% (`impact_n`) when CVSS is absent | `services/risk_rank.py` `compute_risk_rank`; `engine_bridge.py` status mapping |
| Port-derived signals marked "confirmed" | `port_scan` is in `VALIDATED_SCANNERS`, so anything derived from an open port inherits the *confirmed* state, although the finding text says "confirm the owning process" | `detection_engine/posture_rules.py` `VALIDATED_SCANNERS` |
| SNMP findings "suspected" although rig-verified | `snmp_scan` is not in `VALIDATED_SCANNERS`; the list was not updated after validation | same |
| Duplicates (VNC ×2, NFS ×4, Redis ×2, FTP ×2, SNMP ×4) | Cross-producer dedup only covers the exposed-service class by port (`exposed:<port>`). A specific rule (VNC no-auth) and the generic exposed-port signal on the same port have different condition keys; NFS is reported on both 111 and 2049 | `discovery/finding_translator.py` `_EXPOSED_CATEGORIES`, `_find_open_duplicate` |
| Stock sshd on :22 flagged High | The rule fires on any entry in the scanner's `failures` list, so one weak MAC on a default OpenSSH config is graded the same as weak key exchange plus CBC ciphers | `posture_rules._ssh_weak_algos` |
| "UDP amplification" on a DNS server with recursion off | Fallback branch: `responded is True and service in _AMPLIFIERS` fires on any answer. The recursion and monlist branches are precise; this one is not | `posture_rules._udp_amplifier` |
| MQTT 1883 never checked on an IT scan | The IT profile's deep branches have no `iot` / `mobile` branch | `probe/workflow/gates.py` `PROFILE_DEEP_BRANCHES` |
| TLS 8444/8445, ADB 5555 missed | **Not provable from code.** Banner-based TLS routing exists (`workflow/router.py`) and the certificate fetch worked against 1024-bit and SHA-1 certificates in a local test. The report cannot tell "not checked" from "checked and clean", which is a design gap of its own (see A1) | — |

## 2. What the research says to do

| Problem | Logic to adopt | Source |
|---|---|---|
| Duplicate findings | Two-layer model: *signals* (what a check observed) roll up into *issues* (one per asset + condition). DefectDojo matches on a scanner unique ID or a hash of configured fields (e.g. title, CWE, severity, endpoint), configurable per parser | DefectDojo deduplication docs |
| Scoring misconfigurations (no CVE, so no CVSS) | CVSS is designed for software vulnerabilities; NIST's **Common Configuration Scoring System (CCSS, NIST IR 7502)** scores configuration issues with CVSS-like base metrics. Store a per-rule base vector and record "CVSS not applicable: configuration issue, CCSS vector …" rather than leaving it blank | NIST IR 7502 |
| Amplification noise | Decide from the *measured* response/request ratio, not from "it answered". CISA TA14-017A lists bandwidth amplification factors: DNS 28–54 (open resolvers), NTP 556.9 (monlist), SNMPv2 6.3 (GetBulk), SSDP 30.8, NetBIOS 3.8, mDNS 2–10, Portmap 7–28, chargen 358.8, QOTD 140.3, TFTP 60, memcached 10,000–51,000, WS-Discovery 10–500 | CISA TA14-017A |
| Services on unexpected ports | Identify the protocol from the conversation, not the port number. nmap's version detection detects SSL and then probes the service *inside* the encryption ("SSL scan-through") | nmap book, ch. 7 |
| SSH grading | Grade algorithms by level (fail / warn / info) and by policy. Removing SHA-1 MACs from OpenSSH defaults is described as a local-policy choice, so a SHA-1 MAC alone is a *warn*, not a High | ssh-audit; OpenBSD Handbook |
| Known CVE references for posture rules | Curate per-rule CVE lists from authoritative plugins, e.g. IPMI cipher zero → CVE-2013-4782, -4783, -4784 (Tenable plugin 68931) | Tenable plugin 68931 |

---

## 3. AGENT (probe) plan — collection only

| ID | Change | Why | Acceptance test (lab) |
|---|---|---|---|
| **A1** | **Coverage manifest per host**: for every host, emit which ports were scanned (profile + range), which deep branches ran, which were skipped and why (`not_routed`, `port_closed`, `timeout`, `scanner_error`, `profile_excludes`) | Without it the manager cannot say "not checked" vs "clean", and misses like TLS 8444 or ADB 5555 cannot be diagnosed | Every lab port appears in the manifest with a branch decision |
| **A2** | **Route by observed service, not only by profile**: if the banner/handshake identifies MQTT, RTSP, SSDP/UPnP, CWMP or ADB on any profile, run the matching IoT/mobile collector (or add an `iot` branch to the IT profile when those services are seen) | IT scans can never check MQTT/ADB today | T18 MQTT and T21 ADB produce facts on an IT-profile scan |
| **A3** | **TLS everywhere it is observed**: keep banner-based routing, and make the certificate fetch use the same permissive context (security level 0) as the version probes. Add a probe-container test (Debian OpenSSL at security level 2) with 1024-bit and SHA-1 certificates | One code path lacks the explicit setting; the local test passed on a different OpenSSL build, so it must be proven in the shipped image | T14 and T15 produce `tls_scan` facts with key size and signature algorithm |
| **A4** | **Unidentified-service fact**: for every open port whose service could not be identified, emit a structured fact (port, protocol, banner bytes hash, TLS yes/no, response class