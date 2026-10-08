# Network VA — Client/CISO Use Cases (Now vs Pipeline) + Next-Phase Execution Prompt

Date: 2026-10-08 (IST). Sources: `NETWORK_VA_USE_CASES.md`, `probe/PROBE_CAPABILITY_STATUS.md`,
`results_by_actual_scripts.md`, `usecases-networkva.md`, ADR-0001/0002, `docs/research/*`, rig-validation history
(192.168.1.77 / .74) and a 2026 market scan of Tenable, Qualys VMDR, Rapid7 InsightVM, Greenbone OpenVAS, runZero, Nuclei.

> The earlier "Still Needed" list was stale. SSH weak-KEX/Terrapin, NFS world-readable, FTP anonymous, DNS AXFR,
> LDAP anonymous bind, IPMI cipher-0, VNC no-auth, Rsync anon, SMTP VRFY/EXPN and IPv6 link-local ND discovery have
> landed as **rules + unit tests**. What most still lack is **real-target (rig) validation**. Hence three tiers:
> **A** proven on real targets · **B** built + unit-tested, not rig-proven · **C** pipeline.

---

## Part 1 — CISO / customer pitch (value per use case)

✅ proven on real networks · 🟡 built, lab validation in progress.
Audit-control references are indicative; have compliance confirm exact clauses against the client's regulator.

| # | Use case | CISO's question | Value delivered | Supports (audit) | Status |
|---|---|---|---|---|---|
| 1 | Asset Discovery & Inventory | What is actually on my network? | Evidence-based list of live hosts, ports, services, OS, device role, incl. unmanaged IoT/printers/cameras | ISO 27001 A.5.9, PCI DSS 12.5.1, NIST CSF ID.AM | ✅ |
| 2 | Full Attack-Surface Audit (65k ports) | Are services hiding where no one looks? | Non-standard-port services, with a completeness check so "clean" means clean | ISO 27001 A.8.20, PCI DSS 1.2 / 11.3 | ✅ |
| 3 | Internet-Exposure Mapping | What can an outside attacker reach now? | Separates internet-facing from internal-only risk; escalates severity of exposed items | PCI DSS 11.3.2, NIST CSF ID.RA | ✅ |
| 4 | Ransomware Entry-Point Check | Are we open to WannaCry/BlueKeep-style attacks? | SMBv1, SMB signing off, RDP without NLA, exposed RDP, MSRPC | ISO 27001 A.8.8/A.8.9, CERT-In advisories | ✅ |
| 5 | Lateral-Movement Path Detection | If one PC falls, how far can they go? | Attack chains: NTLM relay, legacy Windows, SNMP on core gear | NIST CSF ID.RA, MITRE ATT&CK | ✅ |
| 6 | Backdoor & Rogue-Service Detection | Is anything listening that shouldn't be? | C2/backdoor ports, exposed Docker/K8s APIs, open Redis/Mongo/ES, admin panels | ISO 27001 A.8.16, PCI DSS 11.5 | ✅ |
| 7 | Encryption & Certificate Health | Is data in transit protected? | Old SSL/TLS, weak ciphers, self-signed/expired certs, cleartext protocols | ISO 27001 A.8.24, PCI DSS 4.2, RBI crypto | ✅ |
| 8 | Network Device Weak Config | Are routers/switches on defaults? | Default SNMP communities, UDP amplification reflectors | ISO 27001 A.8.9, PCI DSS 2.2 | ✅ |
| 9 | Exploit-Driven CVE Prioritization | Of 1,000 vulns, which 10 first? | Ranked by CISA KEV, then EPSS, then CVSS; offline/air-gapped | ISO 27001 A.8.8, PCI DSS 6.3.1, SEBI CSCRF | ✅ |
| 10 | Remediation & Audit Reporting | How do I fix and prove it? | Per-OS fix steps, due dates, Excel tracker, scan compare, PDF/Word, AI explanation | ISO 27001 A.8.8, RBI/SEBI VAPT | ✅ |
| 11 | Evidence-Backed "Clean" | Can I trust a green report? | Every rule records whether it ran; a blind rule can't pass as clean | Audit defensibility | ✅ |
| 12 | Zero-Footprint Deployment | Does the tool add risk? | Probe opens no inbound port, one outbound rule, sealed binary | Third-party risk approval | ✅ |
| 13 | Remote-Access & Crypto Hygiene | Are SSH/VNC/IPMI admin paths safe? | Weak SSH crypto + Terrapin, VNC no password, IPMI cipher-0 | ISO 27001 A.8.5 | 🟡 |
| 14 | Data-Leak Exposure | Can anyone read files/directory anonymously? | Anonymous FTP/NFS/Rsync, LDAP anon bind, DNS zone transfer, SMB null session | ISO 27001 A.8.3, DPDP Act | 🟡 |
| 15 | Database & Mail Exposure | Are DBs and mail servers locked down? | Unauth databases, cleartext DB traffic, SMTP enumeration / no STARTTLS | PCI DSS 2.2/4.2, DPDP Act | 🟡 |
| 16 | IPv6, AI/MCP & OT Visibility | What about IPv6, AI servers, plant networks? | IPv6 hosts, exposed AI/MCP servers, passive OT inventory | NIST CSF ID.AM | 🟡 |

**One-line pitch:** "Vedha shows what an attacker can reach and exploit first, proves when your network is actually clean, and adds zero attack surface in doing it."

## Part 2 — What to add to be best-in-class

| Pri | Add | CISO value | Benchmark |
|---|---|---|---|
| P0 | Rig-validate items 13–16 (Docker lab of weak targets) | Every pitched item backed by proof | Standard |
| P0 | Banner → product/version/CPE (close ~32-pattern gap) | More accurate CVE matching | All leaders |
| P0 | Re-scan & change tracking (uc 11) | "What changed, did fixes work?" board trend | Rapid7, runZero |
| P1 | Credentialed scanning (SSH/WinRM/SMB) | Confirmed missing patches vs suspected | Nessus, Qualys |
| P1 | CIS / compliance benchmarks | One-click audit evidence, compliance % | Greenbone, Qualys |
| P1 | Single risk score per asset/org (0–1000) | One board number with trend | Tenable VPR, Qualys TruRisk |
| P1 | AD exposure: Kerberoast, AS-REP, LDAP signing, NTLMv1 | Path to Domain Admin | Tenable Identity |
| P1 | Jira/ServiceNow + SLA tracking | Fixes assigned, tracked, escalated | Rapid7, Tenable |
| P1 | Quick-win rules: SMTP open relay, FTP anon write, SNMPv3 noAuth, NTP monlist, TFTP, UPnP, RTSP/MQTT no-auth | More real findings | Nessus, Nuclei |
| P2 | MAC/OUI vendor, device names, rogue-device alerts | Shadow IT flagged day one | runZero |
| P2 | Scheduled/continuous scanning + SLA dashboards | Yearly VA → always-on assurance | All |
| P2 | Certificate inventory & expiry calendar | Prevents outages/audit findings | Qualys CertView |
| P2 | Scan-accuracy modes (fast/thorough/paranoid) | Depth vs false-positive trade-off | Tenable |
| P2 | Safe default-credential verification (opt-in, RoE-gated) | Candidate → confirmed | Nessus |
| P3 | Network-device config audit (Cisco/Fortinet/Juniper) | ACL/firewall hygiene proof | Nessus, Nipper |
| P3 | External attack surface from cloud vantage | Attacker's view, no probe | Tenable One |
| P3 | Container/K8s/cloud posture | Hybrid estate view | Qualys, Wiz |
| P3 | Active IPv6 (/64, DHCPv6, RA) | IPv6-only hosts | Nessus |
| P3 | Template-based web checks (RoE-gated) | Pre-pentest web depth | Nuclei |

**Positioning:** the big three win on plugin volume (Tenable claims 116K+ CVEs) and publish no independent accuracy
benchmark. Our wedge is trust: zero-inbound probe, coverage-proven clean, confirmed-vs-suspected discipline,
offline CVE matching, attack-path chains, sovereign/BFSI AI gateway. That is why P0 is validation, not new features.

---

## Part 3 — Execution prompt (paste into a fresh session)

```text
ROLE: Senior network-security engineer + systems architect on Vedha (probe = collection-only sensor,
manager = detection/scoring/correlation). Work in the Vedha repo root.

READ FIRST (do not re-derive): CLAUDE.md; graphify-out/GRAPH_REPORT.md; NETWORK_VA_USE_CASES.md; this doc;
results_by_actual_scripts.md; usecases-networkva.md; probe/PROBE_CAPABILITY_STATUS.md; docs/adr/0001, 0002;
docs/architecture/*; docs/research/2026-09-23-scalable-large-subnet-scanning.md; docs/research/pipeline-hardening.md;
memory notes on scanner v2/v3, accuracy pass (AIMD + MERGE GATE), AIMD ratchet regression, aggressive-scan failure,
ingest-gate silent drop, run-scoped fact 422, rig-validated scanners, shared-checkout concurrency.

HARD CONSTRAINTS:
- Branch first (feat/scanner-accuracy-v4); never work on main. Shared checkout + symlinked .venv: never upgrade
  the venv; stage explicit paths; isolate live stacks with -p.
- probe/scanner ≡ probe/main_scripts (main_scripts canonical, drift-guarded) AND install.sh runs probe/workflow/.
  Land every scanner change in all shipping trees.
- Agent emits FACTS ONLY; detection lives in the manager. New check = scanner fact + manager rule + fact-contract
  corpus entry + ingest._validate acceptance (else silent drop: check DetectionRun.stats["ingest"]).
- Accuracy MERGE GATE: no accuracy claim without provenance (rig/pcap/real target).
- IST-aware timestamps via project_time helpers. CI runs tests by NAME allowlist: register new tests.
- Read-only, RoE-gated, lockout-safe active checks; OT stays passive; no credential brute force.
- TDD: failing test first for every defect and new rule.

PHASE 1 — Core scanner accuracy + capability
1. Build a reproducible lab under probe/tests/rig/ (docker-compose) of deliberately weak targets with expected-facts
   JSON ground truth: old OpenSSH/Dropbear, bind9 (AXFR+recursion), vsftpd anon rw, NFS world export, rsyncd anon,
   openldap anon bind, samba null session + SMBv1, postfix open relay + VRFY, x11vnc no-auth, ipmi_sim cipher-0,
   redis/mongo no-auth, nginx TLS1.0 + self-signed/expired, snmpd public. `make rig-validate` diffs facts vs
   ground truth and prints precision/recall per scanner. Record the baseline.
2. For each Tier B scanner (ssh, smb enum, ldap, dns, nfs, ftp, rsync, vnc, snmp, ipmi, smtp, db, web): fix every
   mismatch, add regression tests, promote to Tier A only at 100% rig recall and zero false positives on a clean control.
3. Close missing rules end-to-end: FTP anon WRITE, SMTP open relay, SNMPv3 noAuth, NTP mode-6/monlist, TFTP read,
   SSDP/UPnP IGD, RTSP/MQTT no-auth, LDAP signing off, Kerberoast/AS-REP exposure (network-observable only).
4. Banner → product/version/CPE: measure null-rate, close the pattern gap (target product ≥90%, version ≥75% where
   the banner carries one), emit CPE 2.3, prove CVE hit-rate improves (before/after table).
5. Asset intelligence: MAC + OUI vendor, NetBIOS/rDNS names, closed-vs-error port state fix, honest per-host health,
   retry-once-before-offline, drop-vs-blocked distinction.
6. Guard known perf wins with benchmark assertions: AIMD delivery-rate (no 0.62 ports/s collapse), 4.3 MB/host,
   per-host chunk commit.

PHASE 2 — Architecture & design review, then fix
1. Map the real data path end to end (launcher → queue → probe WS → workflow scanners → upload → ingest._validate →
   detection → verification → findings → remediation/reporting → portal) from code and graphify, noting wrong docs.
2. Rank (impact × effort): silent-drop points, duplicated logic across scanner trees (propose one tree + build step),
   N+1/blocking calls, unbounded memory/queues, upload idempotency, migration safety, observability gaps, config
   sprawl (intensity presets vs pps caps), test-suite speed.
3. Write docs/architecture/2026-10-architecture-review-v2.md (findings with file:line evidence) and an ADR per
   structural change.
4. Implement the safe, testable top items; leave the rest as tracked cards. Do NOT start the ADR-0002 D1/D2
   auto-close fix without coverage-proven gating.

DEFINITION OF DONE: `make rig-validate` green with per-scanner precision/recall committed under docs/testing/;
full pytest passes; new tests in the CI allowlist; drift guard passes; before/after metrics; NETWORK_VA_USE_CASES.md
updated (B→A only with rig evidence); `graphify update .`; docs/STATUS.md updated; commit per logical change;
do NOT push or merge without asking. REPORT what moved tier, what regressed, what was skipped and why.
```
