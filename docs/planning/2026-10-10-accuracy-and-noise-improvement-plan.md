# Accuracy and noise-reduction plan — agent side and manager side

**Date:** 2026-10-10 · **Status:** research + plan, no code changed.
**Driver:** the first lab scan ([gap analysis](../reports/2026-10-10-newenv1-scan-gap-analysis.md)) detected 7 of 25 scenarios, duplicated findings (22 rows ≈ 13 issues), ranked Medium above Critical, marked port-guesses "confirmed", and left 39 of 83 report columns empty.

**Constant constraint:** the **probe collects facts only; the manager does all detection, scoring and correlation**. Every manager change lands in `manager/`; every agent change lands in `probe/scanner` and its byte-identical `probe/main_scripts` mirror, is wired into `probe/workflow`, and keeps the two-tree parity and wiring gates green. New check = scanner fact + manager rule + fact-contract corpus entry + `ingest._validate` acceptance, or it is silently dropped.

**See also:** [noise reduction and detection plan](../research/2026-10-10-noise-reduction-and-detection-plan.md), a companion root-cause table and agent plan (coverage manifest, observed-service routing). That file is cut off after its row A4 and has no manager section; this document is the complete agent + manager plan.

Everything below cites the file and line I read on 2026-10-10. Where a cause is not proven from code alone it says *(verify)*.

---

## Part A — grounding: what the code actually does today

| Observation | Root cause in code | Verified? |
|---|---|---|
| TLS on 8444/8445 not graded (T14, T15) | `tls_scan` only runs on `scanner.service_enum.TLS_PORTS` (443, 8443, 9443, 993, 995, 2376, 8883 …). `_get_cert_der` **can** fetch a 1024-bit and a SHA-1 cert (tested against live `openssl s_server`, on macOS Python with OpenSSL 3.0.16, both at defaults and with the client context set to `@SECLEVEL=2`, because with verification off OpenSSL does not abort on key-size or signature-strength checks), so the scanner is capable; it is simply never pointed at 8444/8445. **Not yet proven:** the shipped Debian probe image, and servers that only speak TLS 1.0/1.1 (`_get_cert_der` sets no `@SECLEVEL=0`, unlike the version probes at `tls_scanner.py:192-205`). Add a container test for both `workflow/router.py` is meant to route a TLS port found by the banner, but 8444/8445 were not in the scan's port list in the first place | ✅ tested |
| MQTT (T18), ADB (T21), RTSP, CWMP, UPnP missed | IT profile deep branches (`workflow/gates.py:83`) have no `iot`/`mobile` branch: `{tls, web, smb, db, mcp_ai, snmp, ssh, smb_enum, ldap, dns, nfs, ftp, rsync, vnc, ipmi, smtp, msrpc, rdp, printer}`. These checks live only in the `iot` profile | ✅ |
| ADB 5555 produced nothing although 5555 is in the default IT ports and in `_BACKDOOR` | Not explained by reading code — needs the detection run's ingest trace | *(verify)* |
| "confirmed" on port-only guesses | `posture_rules.py:131` `_STATE_FACTOR={confirmed:1.0, suspected:0.8, potential:0.6}`; validated scanners (`VALIDATED_SCANNERS`, line 43) include `port_scan`, so an exposed-port signal from `port_scan` is treated as a confirmed-tier source | ✅ |
| Risk 285 (Medium) > 254/274 (Critical) | `risk_rank.compute_risk_rank` weights impact 0.40, exploit 0.25, **context 0.20**, evidence 0.15. `context_n` mixes exposure and the auth-gap; several Medium exposed-service findings have `auth_enforced=False` and internal exposure, which lifts them above Criticals that carry no CVSS. Severity only contributes 0.2 of the impact term when CVSS is absent (line 45-50) | ✅ |
| SSH :22 (stock Ubuntu) flagged High | `_ssh_weak_algos` (`posture_rules.py:498`) fires on any non-empty `failures` list from the scanner's vendored weakness table; it does not weight by how weak. OpenSSH 9.6 still offers `hmac-sha1`, which the table counts | ✅ (rule logic); the exact algorithm *(verify from evidence)* |
| DNS :53 "UDP amplification" though recursion is off | `_udp_amplifier` (`posture_rules.py:377`) fires if `responded and service in _AMPLIFIERS and status==open`, independent of open recursion / measured factor; only the NTP and DNS-recursion branches are precise | ✅ |
| Duplicates (NFS ×4, SNMP ×4, VNC ×2) | `finding_translator.py`: cross-producer condition key exists but only for `_EXPOSED_CATEGORIES = {cleartext_protocol, exposure, amplification}` (line 229) and only when a producer stamps `dedup_key`. A dedicated-scanner finding (NFS) and a port-intel cleartext finding on the same port are different categories and different titles, so they never merge | ✅ |
| Empty narrative columns | The report (`report_document.py:1349`) reads technical_details / impact / business_impact / reproduction / root_cause / preconditions **only from `finding.evidence` or `content_overrides`**. The deterministic knowledge base `services/finding_content.py` (categories: weak_tls, outdated_ssh, anon_ftp, exposed_rdp, smb_signing, open_mgmt_port, default_credentials, missing_patch, generic) is **never called by the export**, so its prose never reaches the CSV | ✅ |
| 19 of 22 "generic" category | `remediation_kb.classify_finding` keyword table (`remediation_kb.py:60`) has no needles for VNC, Redis/NoSQL, NFS, rsync, SNMP, IPMI, MQTT, AI/MCP, cleartext-non-telnet, SIP, amplification | ✅ |
| Role = "network infrastructure" with 7 roles | `intel/tagging.py`: `_roles` yields a role per matched port (5060→voip, etc.) with no dominant-role resolution; `_host_type` maps `device_role`/`asset_type` straight through | ✅ |

**Reusable building blocks that already exist and are not wired in:** `finding_content.py` (narratives), `remediation_kb.py` RECIPES (per-OS fix steps with verification), `verification.py` (four-tier confidence), `risk_rank.py` (0–1000), `dns_scanner.derive_zones` (zone discovery). Much of the fix is wiring and tuning, not greenfield.

---

## Part B — AGENT plan (probe: collection accuracy, fewer silent misses)

The probe cannot reduce manager-side noise, but it causes misses when it fails to collect a fact or mislabels one. Land each in `scanner/` + `main_scripts/` mirror, wire in `workflow/`, add a `tests/rig/` expected-facts case.

### A1 — TLS on any port, driven by the banner (fixes T14/T15 class) · P0 · S
- **Now:** deep `tls` branch runs only on the static `TLS_PORTS`; `service_banner` already attempts a TLS handshake on unknown ports and records `tls: True`, and `router.looks_like_tls` exists.
- **Logic:** in `workflow`, after the banner stage, for every open port where `service_banner` recorded `tls: True` or `service: "tls"`, add that port to the `tls` branch's target set for this host even if it is not in `TLS_PORTS`. This is Nmap's "if SSL is detected, connect through it" behaviour (nmap `-sV` SSL scan-through).
- **Fact:** `tls_scan` already emits version/cipher/cert/key-size/sig-alg; no new fact shape.
- **Reference:** Nmap service/version detection, SSL scan-through (nmap.org/book/vscan.html).

### A2 — Make IoT/mobile checks reachable on an IT scan (fixes T18/T21/RTSP/CWMP) · P0 · M
- **Now:** `PROFILE_DEEP_BRANCHES["it"]` has no `iot`/`mobile` branch, so MQTT/RTSP/CWMP/ADB/UPnP never run on an IT engagement.
- **Logic (pick one, prefer the second):** (a) add a lightweight `iot` branch to the IT profile; or (b) **port-triggered branches** — when the discovery/banner stage sees 1883/8883 (MQTT), 554/8554 (RTSP), 7547 (CWMP), 5555 (ADB) or 1900 (SSDP) open, auto-enable the matching scanner for that host regardless of profile. (b) avoids scanning IoT ports on every host while never missing one that is actually open.
- **Also:** `adb` (5555) and MQTT must reach `ingest._validate` — add the fact-contract corpus entries, or they are dropped silently.

### A3 — Collect the facts that have no rule yet, where the scanner is cheap · P1 · M
SIP, NetBIOS and mDNS are already probed by `udp_scanner`; IKE too. The agent side is done; these are manager rules (B6). Agent work remaining:
- **SNMPv3 noAuth** (`snmp_scanner`): add a USM security-level probe that records whether a noAuthNoPriv user answered (today only v3 *presence* is recorded).
- **FTP anonymous write** (`ftp_scanner`): a bounded `STOR`/`DELE` of a probe file in an allowed dir, RoE-gated, recording `anon_write: true|false`.
- **NTP monlist measured factor** (`udp_scanner`): record the measured response/request byte ratio as `amplification_factor`, so the manager can threshold it (see B5).

### A4 — Unidentified-open-port fact · P1 · S
- **Now:** a port open but not identified by any rung produces no inventory fact the manager can turn into a finding, so Smart Install 4786, SLP 427, Radmin 4899, AFP 548, EPMD 4369, BGP 179 were silent in the lab.
- **Logic:** `service_banner`/`port_scanner` already know the open set and which ports got no identification. Emit a `service_banner` fact with `identified: false` for each, carrying port + any raw bytes. The manager then raises a low-severity "unidentified service on a non-standard port" (B7). Pure collection, no new scanner.

### A5 — Harden the SSH fact so the manager can grade, not just count · P1 · S
- **Now:** `ssh_scanner` emits `failures: [...]`; the manager rule fires on any non-empty list.
- **Logic:** emit the algorithms in structured buckets — `kex`, `ciphers`, `macs`, `host_key` — each tagged `fail` / `warn` using ssh-audit's classification (CBC ciphers, `hmac-sha1`, 1024-bit DH = at least warn; `arcfour`, `3des`, SSHv1, `diffie-hellman-group1-sha1` = fail). The manager then grades High only on a `fail`, Low/info on `warn`-only. This stops stock OpenSSH 9.6 (warn-only `hmac-sha1`) from being High.
- **Reference:** jtesta/ssh-audit level model (`info`/`warn`/`fail`) and its platform hardening guides.

### A6 — Agent accuracy hygiene (already-known gaps, keep on the list) · P1/P2
rsync 873, IPP 631 and Kerberos 88 are not in the default IT TCP set; the default UDP set is 5 ports though probes exist for 12. Fold into `gates.py`. OS-fingerprint connect-path window harvest (p0f-class) and the accuracy-corpus CI gate are still open from earlier memory.

---

## Part C — MANAGER plan (detection, scoring, de-duplication, report content)

### M1 — De-duplicate across producers by (asset, condition) · P0 · M
- **Now:** cross-producer merge only covers `{cleartext_protocol, exposure, amplification}` and needs a stamped `dedup_key`. NFS (dedicated scanner, `access_control`) and NFS-cleartext (port-intel) don't merge; SNMP default-community, SNMP-amplifier and the two SNMP exposure rows don't merge.
- **Logic:**
  1. Give every rule a **canonical condition key** = `(asset, protocol-or-service, port, weakness-class)`, independent of producer and title. Store it in `evidence[dedup_key]` from the rule definition, not ad-hoc.
  2. Broaden `_find_open_duplicate` to match on that key for **all** categories, keeping the "two genuinely different issues on one port stay separate" guard (e.g. weak-TLS vs web-method on 443 differ in weakness-class).
  3. Add a **roll-up** layer for the report: group the condition-keyed findings per asset into one row with sub-findings, so the client sees "13 issues" with the signals nested, not 22 flat rows. This is DefectDojo's model: a configurable hash over a chosen field set (`HASHCODE_FIELDS_PER_SCANNER`, with `service` always included) decides identity.
- **Reference:** DefectDojo deduplication (hash_code over a field set; `HASH_CODE_FIELDS_ALWAYS=["service"]`).
- **Files:** `discovery/finding_translator.py` (`_condition_of`, `_EXPOSED_CATEGORIES`, `_find_open_duplicate`), `detection_engine/posture_rules.py` (emit the key per rule), `services/report_document.py` (roll-up).

### M2 — Status must reflect evidence strength, not scanner membership · P0 · S
- **Now:** `port_scan` is in `VALIDATED_SCANNERS`, so an exposed-port *guess* inherits confirmed-tier confidence; the CSV marks seven port-derived findings `confirmed`.
- **Logic:** separate **"the scanner is validated"** from **"this finding is a direct protocol observation vs a port inference."** A rule that keys only off an open port or a port+banner heuristic is `suspected` regardless of which scanner saw the port; `confirmed` requires a protocol-level observation (VNC security-type byte, IPMI RMCP+ status, SMB signing flag, a real banner match). Encode an `evidence_basis` field (`protocol_observed` | `port_inference` | `banner_inference`) on each rule and map it to the state in `posture_rules.compute_risk`/the translator.
- **Reference:** matcher.py's existing `source_confidence == authoritative` gate — apply the same discipline to posture.

### M3 — Risk score monotonic with severity · P0 · S
- **Now:** `risk_rank.compute_risk_rank` can rank a Medium (285) above a Critical (254) because context (exposure + auth gap) contributes 0.20 and severity only 0.2 of a 0.40 impact term when CVSS is absent.
- **Logic:** make severity a **hard band**, then rank within the band by exploitability and context — i.e. a Critical's floor is always above a High's ceiling. Either (a) compute the 0–1000 score then clamp into per-severity sub-ranges (crit 750–1000, high 500–749, med 250–499, low 1–249), or (b) sort by `(severity_rank, raw_score)` for display. (a) keeps one comparable number. Posture findings with no CVSS must still get an impact value from severity, not near-zero.
- **Reference:** FIRST CVSS v4 + SSVC separate *severity* from *decision/priority*; keep severity authoritative for ordering.
- **File:** `services/risk_rank.py`, `detection/prioritization.py`.

### M4 — Precision fix: DNS amplification · P0 · S
- **Now:** `_udp_amplifier` fires for any answering service in `_AMPLIFIERS` on an open UDP port; the lab DNS has recursion off yet was flagged.
- **Logic:** for DNS, require `open_recursion is True` **or** a measured amplification factor above a threshold; never fire on "the resolver answered a normal query." For NTP, keep `monlist_enabled`. Use the CISA TA14-017A bandwidth-amplification factors as the per-protocol thresholds (DNS 28–54, NTP 556, SNMPv2 6.3, SSDP 30.8, CharGEN 358, Memcached 10,000+, LDAP 46–55). Below the factor, it is exposure, not an amplifier.
- **Reference:** CISA TA14-017A (verified table).

### M5 — SNMP amplifier + validated-tier correction · P1 · S
- Promote `snmp_scan` into `VALIDATED_SCANNERS` now that SNMP default-community is rig-verified (per the owner's 9 Oct list), so it stops printing "SUSPECTED pending validation." Gate the amplifier finding on the measured GETBULK factor (A3), matching TA14-017A's SNMPv2 BAF ~6.3.

### M6 — Rules for the facts the agent already collects · P1 · S–M
SIP exposure, NetBIOS exposure, mDNS exposure, IKE aggressive mode: the facts exist (`udp_scanner`), the rules do not. Add them to `posture_rules.py` with condition keys (M1), severities from the catalogue, and fact-contract corpus entries. Also SNMPv3-noAuth and FTP-anonymous-write rules once A3 ships.

### M7 — Fill the report narrative from the knowledge base · P0 · M
- **Now:** `report_document` reads narrative fields only from evidence/overrides; `finding_content.py` is never called, so Technical details / Impact / Business impact / Exploitation context / Reproduction / Root cause / Preconditions are empty on all 22.
- **Logic:** in the report builder, when a field is absent from evidence and overrides, fall back to `finding_content.build_finding_content(finding, asset)` (the deterministic KB, already asset-criticality aware and honest about unvalidated exploitation). Keep the precedence overrides > evidence > KB. Then the "Description" column can stop being the rule's internal FP note — move that note to a separate `detection_rationale` field.
- **Expand the KB categories** (`finding_content._CONTENT` + `remediation_kb._CATEGORY_KEYWORDS`) to cover VNC-no-auth, unauth datastore, NFS export, rsync, SNMP, IPMI, MQTT, AI/MCP, cleartext (non-telnet), SIP — so fewer findings fall to `generic`.
- **Files:** `services/report_document.py`, `services/finding_content.py`, `services/remediation_kb.py`.

### M8 — Export the structured fix plan · P0 · M
- **Now:** "Structured recommendation records" and "Compatibility recommendations" are `[]` on every finding; `remediation_kb.RECIPES` has per-OS steps with verification and effort that never reach the CSV.
- **Logic:** attach the classified recipe (steps, per-OS commands, verification command, effort, remediation-risk, rollback) to each finding at report time, keyed by the same category taxonomy as M7. One finding → one fix plan with ordered steps.

### M9 — CVSS / EPSS / CVE for posture findings · P1 · M
- **Now:** empty with no "not applicable" reason (the gap column flags it).
- **Logic:** for posture findings, either attach a representative CVSS vector per rule (IPMI cipher-0 → CVSS 10.0 `AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`, CVEs 2013-4782/4783/4784 per Tenable plugin 68931) **or** set `cvss_not_applicable_reason` so the readiness gap clears honestly. Show CVSS **and** EPSS on every finding (CERT-In requirement). Do not invent an EPSS for a config finding with no CVE; state "no CVE, EPSS not applicable."

### M10 — Role classification with a dominant role + confidence · P1 · M
- **Now:** `intel/tagging._roles` emits one role per matched port; an Ubuntu box with emulated SIP/BGP/printer became "network infrastructure" with 7 roles.
- **Logic:** keep the per-port role signals but compute a **dominant `device_role`** from the strongest evidence (OS fingerprint and SMB/RDP for a server, management-protocol density for network gear), with a confidence, and only let a high-confidence role drive `host_type` and the attack-path severity amplifier. Show the role confidence in the report. Many lab roles were emulator artefacts, so re-measure on a clean host.

### M11 — Coverage sheet in the export · P2 · M
Add scan use case, ports scanned, rules evaluated, and per-rule outcome (match / clean / no-evidence) to the export — the `verification.py` outcomes already exist internally. Without it, "not detected" cannot be told from "not checked," which is the core trust claim.

### M12 — Risk-acceptance and ownership hygiene · P2 · S
Refuse `accepted` disposition without owner + expiry + compensating control (the CSV shows an accepted Critical Redis with none). Auto-propose an owner from asset tags.

---

## Part D — sequence and ownership

| Wave | Items | Effect |
|---|---|---|
| 1 (noise now, mostly manager) | M1 dedup · M2 status · M3 risk order · M4 DNS amp · M5 SNMP tier · M7 narrative · M8 fix plan | Report drops from 22 noisy rows to ~13 explained issues, correct severity order, real descriptions and fix steps |
| 2 (coverage, agent + manager) | A1 TLS-any-port · A2 IoT branch · A4 unidentified-port fact · B7/M6 missing rules · A5 SSH buckets | Detects the 4 "rule existed" misses and stops silent unknown ports |
| 3 (depth) | A3 new probes · M9 CVSS/EPSS · M10 role · M11 coverage sheet · M12 acceptance | Closes compliance-grade reporting gaps |

**Validation for every item:** re-run the Ubuntu weak lab, compare against the [scenario catalogue](../testing/2026-10-10-network-va-scenario-catalogue.md), and record precision/recall. No accuracy claim without that rig evidence (the standing MERGE GATE rule).

## Sources
CISA TA14-017A (UDP amplification BAF table, verified) · Nmap service/version detection and SSL scan-through · DefectDojo deduplication (hash_code / field sets) · jtesta/ssh-audit info/warn/fail model · Tenable plugin 68931 (IPMI cipher-0, CVE-2013-4782/4783/4784) · NIST IR 7502 CCSS (configuration-issue scoring, for the severity model) · FIRST CVSS v4 + SSVC (severity vs priority). Code read on 2026-10-10 in `manager/` and `probe/` as cited inline.
