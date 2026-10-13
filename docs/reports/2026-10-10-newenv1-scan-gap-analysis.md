# newenv1 scan report — what was detected, what was missed, what to improve

**Source:** `vedha-newenv1-report.csv` (generated 2026-10-10 05:52 UTC, status *DRAFT / NOT APPROVED*).
**Target:** one host, 192.168.1.70 (the Ubuntu weak lab, 25 Critical/High scenarios built by `vedha-weak-lab.sh`).
**Method:** parsed all 22 findings × 83 columns, then compared them with the 25 lab scenarios and with `probe/workflow/gates.py`, `port_intel.py` and the posture rules. This is a first Vedha scan of the lab, so it is the first real accuracy measurement.

**Not recorded in the CSV (so some conclusions are inferences):** which scan use case and port range ran, and which rules were evaluated clean or blind. Items that depend on this are marked *inferred*.

---

## 1. Headline numbers

| Measure | Result |
|---|---|
| Findings | 22 (4 critical, 8 high, 9 medium, 1 low) |
| Distinct issues behind them | about 13 (the rest are duplicates or overlaps) |
| Lab scenarios detected as intended | **7 of 25** |
| Partly detected (other signal only) | 3 |
| Missed | **15** (11 because no rule/scanner exists yet; **4 where a rule exists and did not fire**) |
| Columns empty on every finding | **39 of 83** |
| Evidence integrity | 22 of 22 hashed and verified (custody works) |

## 2. Detection scorecard (25 lab scenarios)

| Result | Scenarios |
|---|---|
| ✅ Detected | T01 weak SSH :2222 · T03 VNC no auth · T05 IPMI cipher-0 (plus the "exposed management plane" correlation) · T10 NFS world-readable · T11 Rsync anonymous · T12 Redis no auth · T22 Ollama API no auth |
| 🟡 Partly | **T08** DNS: only `version.bind` (Low) and "UDP amplification" were reported; the **zone transfer was not**. **G06** FTP: anonymous *login* found, write not tested (the lab side also failed). **G01** SNMP: v2c findings only, the v3 noAuth user is not checked |
| ❌ Missed, rule/scanner not built (expected) | G09 SIP · G11 NetBIOS · G14 Smart Install 4786 · G15 SLP 427 · G16 XDMCP 177 · G17 Radmin 4899 · G18 AFP 548 · G19 EPMD 4369 · G20 BGP 179 · G22 Ubiquiti 10001 · G25 NAT-PMP 5351 |
| ❌ Missed, **a rule exists and did not fire** | **T14** 1024-bit TLS key :8444 · **T15** SHA-1 certificate :8445 · **T18** MQTT anonymous :1883 · **T21** ADB no auth :5555 |

### Why the four "rule exists" misses happened

| Scenario | Cause found in the code |
|---|---|
| T14, T15 TLS | The TLS scanner only runs on a fixed list of standard TLS ports (443, 8443, 9443, 993, 995 …). 8444 and 8445 are not on it, so the TLS rules never received facts. The scanner should run on any port the banner step identifies as TLS |
| T18 MQTT | The IT profile's deep branches are db, dns, ftp, ipmi, ldap, mcp_ai, msrpc, nfs, printer, rdp, rsync, smb, smb_enum, smtp, snmp, ssh, tls, vnc, web. **There is no `iot` or `mobile` branch**, so MQTT, RTSP, CWMP, UPnP and ADB checks can never run on an IT-profile scan |
| T21 ADB 5555 | Not explained by the code: 5555 is in the default IT port list *and* in the backdoor/C2 catalogue, so at minimum an exposed-port finding should exist. Investigate the detection run's ingest/trace stats |

### The scan went wider than the default profile (inferred)
Ports 2222, 873 and 11434 are not in the default 95-port IT set, but findings exist for them. So the scan covered more than the default, and the unidentified listeners (4786, 427, 4899, 548, 4369, 179) were probably found open. **They produced no finding at all**, not even an "unidentified service on a non-standard port" inventory item. That silent result is the single biggest coverage risk.

## 3. Precision problems (noise and probable false positives)

| # | Problem | Evidence in the CSV |
|---|---|---|
| 1 | **Duplicates**: 22 findings, about 13 issues | VNC ×2 (#7, #14) · NFS ×4 (#4, #21 plus cleartext #16, #17) · Redis ×2 (#6, #9) · FTP ×2 (#8, #12) · SNMP ×4 on port 161 (#2, #11, #18, #20) |
| 2 | "Confirmed" on unverified signals | #2 #6 #8 #14 #16 #17 #22 are `confirmed`, yet five of them say "Signal derived from the open port … confirm the owning process/scope" |
| 3 | **Risk score does not follow severity** | All seven "confirmed" medium findings score 285, above every critical (274, 254, 254, 245). A Medium cleartext-NFS note outranks Critical VNC no-auth |
| 4 | Stock sshd on port 22 flagged High (#13) | The lab built only :2222; :22 is Ubuntu's default. Likely triggered by default SHA-1 MACs (my independent check found no SHA-1 key exchange and no CBC ciphers). *Inferred*, because Technical details is empty |
| 5 | "UDP amplification service exposed" on DNS :53 (#22) | The lab DNS has `recursion no`. The rule fires whenever the service *answers*, but DNS only amplifies with open recursion or large answers |
| 6 | Cleartext findings on NFS and rpcbind (#16, #17) | Noise next to the real NFS export finding |
| 7 | **Role misclassification** (#11) | "This host is NETWORK infrastructure" for an Ubuntu server. Asset tags give it `host_type:network` plus 7 roles (database, dns, file_share, monitoring, remote_access, voip, web). Partly a lab artefact (emulated BGP, SIP), but it repeats round-1 gap #8 |
| 8 | SNMP findings still "SUSPECTED" | #18, #20: "snmp_scan is not in the validated trust tier yet", although SNMP default community is on the owner's rig-verified list. The trust tier was not updated after validation |
| 9 | Wrong categories | IPMI cipher-0 is categorised `weak_tls`; the management-plane correlation is `exposed_rdp`; 19 of 22 are `generic`. Themes say `patch_vulnerability_mgmt` for access-control problems |

## 4. Description, remediation, fix plan: quality check

| Item | State |
|---|---|
| **Description** | Filled, but it is the rule's internal *false-positive note* ("Fires only when the scanner confirmed …"), not a description a customer can read. For 2 findings it is correct prose (#3, #11) |
| Technical details, Technical impact, Business impact, Exploitation context, Reproduction, Root cause, Preconditions | **Empty on all 22** |
| **Remediation** | One sentence per finding. The impact explanation is sometimes mixed into it. No commands, no steps, no verification step, no effort, no rollback |
| Structured recommendation records, Compatibility recommendations | `[]` / empty on all 22. The contextual-remediation engine's output is not in this export |
| CVSS, CVSS vector, CVEs | Empty on all 22 (no "not applicable" reason either). CERT-In needs CVSS **and** EPSS |
| Compliance mappings | Empty. Only "derived context" control pointers (generic PCI DSS 2.2.1 / 6.3.1 and ISO A.8.8/A.8.9 for 19 findings). Regional profile = `default_generic_profile`, sector `generic` |
| Owner, asset owner, planned closure, action reference | Empty on all 22 |
| Retest | All empty (nothing retested yet; expected) |
| Risk acceptance | #9 (Critical Redis) is `accepted` with no owner, no expiry, no compensating controls (the report flags it itself) |
| Evidence | 1 item per finding, hashes verified. Two correlation findings (#3, #11) have no evidence source |
| Readiness gaps column | Reports 12–16 gaps on every finding, so the product already knows the report is not client-ready |

### What is good
Evidence hashing and custody (22 of 22 verified), MITRE mapping on every finding, CWE on 20 of 22, SLA dates that scale with severity (critical 1 day, high 3, medium 7, low 29), re-scan continuity (first seen 21:03, last seen 04:46, one finding set), specific rules with clear scanner provenance ("observed by vnc_scan"), and clear evidence-based wording on the best rules (VNC, IPMI, FTP).

## 5. Areas of improvement (priority order)

| Pri | Area | What to do | Size |
|---|---|---|---|
| P0 | Report content | Generate Technical details, Impact, Business impact, Exploitation context, Reproduction, Root cause and Preconditions from rule metadata. Move the false-positive note out of Description | M |
| P0 | Remediation / fix plan | Export the contextual-remediation output: steps, per-OS commands, verification command, effort, rollback, owner. Fill the structured recommendation records | M |
| P0 | De-duplication | Merge findings on the same (asset, condition) across producers; fold cleartext-NFS/rpcbind into the NFS finding; show "13 issues, 22 signals" | M |
| P0 | Status and risk score | Port-derived signals must be *suspected*, not *confirmed*. Make the risk score monotonic with severity so a Medium never outranks a Critical | S |
| P1 | TLS on any port | Route any banner-identified TLS port to `tls_scanner` | M |
| P1 | IoT/mobile checks in the IT profile | Add an `iot` branch (or auto-add it when 1883/554/1900/5555/7547 are open); explain why ADB 5555 produced nothing | M |
| P1 | Unidentified open ports | Never silent: add the Shadowserver catalogue (Smart Install CRITICAL, SLP, XDMCP, Radmin, AFP, EPMD, BGP …) and a generic "unidentified service on non-standard port" inventory finding | M |
| P1 | DNS zone transfer | The zone name cannot be guessed. Derive candidates (reverse DNS, SOA/NS lookups, search domain, an operator-supplied zone list) | S |
| P1 | Rules for probed facts | SIP, NetBIOS, mDNS, IKE (collected, no rule). Also FTP anonymous-write and SNMPv3 noAuth checks | S–M |
| P1 | Precision fixes | SSH: grade by strength, not by presence of SHA-1 MACs. DNS amplification: require open recursion or a measured factor. Promote validated scanners (SNMP) out of "suspected" | S |
| P1 | Role classification | Do not call a general server "network infrastructure" from a few ports; show the role confidence | M |
| P2 | CVSS / EPSS / CVE | Fill CVSS and EPSS for posture findings (or a "not applicable" reason); attach known CVEs (e.g. IPMI cipher-0 → CVE-2013-4782 / -4783 / -4784, as cited by Tenable plugin 68931; CVE-2013-4786 is a different IPMI issue, RAKP hash disclosure) | M |
| P2 | Compliance and regional | More specific control mapping than 19 "generic"; fix wrong categories and themes; set the sector profile (e.g. India BFSI) | M |
| P2 | Ownership and acceptance | Auto-propose owner from asset tags; refuse risk acceptance without owner, expiry and compensating controls | S |
| P2 | Coverage sheet | Add to the export: scan use case, ports scanned, rules evaluated, and per-rule outcome (match, clean, no-evidence). Without it "not detected" cannot be told apart from "not checked" | M |

## 6. How to confirm the inferences
1. Open the detection run `384ff89d-0412-480b-a2ef-4c779f2fef21` and check `DetectionRun.stats["ingest"]` for dropped facts (ADB 5555, MQTT 1883, TLS 8444/8445).
2. Read the SSH evidence for port 22 (which algorithm triggered it).
3. Run `dig @192.168.1.70 +recurse example.com` to confirm DNS recursion is off (supports false positive #5).
4. Re-run the scan after fixing G06 on the lab, then re-compare against this document.
