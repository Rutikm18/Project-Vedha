# Network VA Coverage Framework — what "complete" means, and where Vedha stands

**Date:** 2026-10-09 · **Status:** research only, no code changed · **Why this exists:** web has the OWASP Top 10 and the CWE Top 25 ("SANS 25"). Network VA has no single equivalent, so "did we cover every required area?" had no answer. This doc builds one by taking the union of independent baselines and diffing it against Vedha's real code.

**How to read the labels**
- ✅ **Verified 9 Oct 2026** — fetched from the primary source during this research.
- 📚 **From knowledge** — a standard I know well but did not re-fetch today. Re-check before quoting a clause number to a client.
- ⚠️ **Secondary only** — found only on a third-party page.
- Vedha status is from reading `port_intel.py`, `posture_rules.py`, `gates.py`, `udp_scanner.py` and the docs, not from a live run.

**Honest limit.** Nobody can prove "nothing is left", because no external list is complete. The method here is to use **independent baselines** (policy lists, exploitation data, a 150-report internet-exposure programme, a commercial scanner's plugin taxonomy) so a blind spot has to be missed by all of them at once. Section 7 lists what is deliberately out of scope.

---

## 1. There is no "Top 10 for networks" — there are six questions

| Question | Answered by |
|---|---|
| What mistakes are most common? | NSA/CISA Top 10 Misconfigurations |
| What is being exploited right now? | CISA KEV, CISA "Top Routinely Exploited", Shadowserver |
| What must be fixed, how fast? | CISA BODs (26-04, 26-02, 23-02), CERT-In, PCI DSS |
| What should a program include? | CIS Controls v8.1, NIST CSF/800-53/800-40/800-115 |
| What should the scanner check? | Nessus/NNM plugin families, Shadowserver report types |
| How do we rank findings? | KEV + EPSS + CVSS + SSVC |

## 2. Source catalogue

### 2.1 Weakness and misconfiguration lists
| Source | Use | Status |
|---|---|---|
| **NSA/CISA Top Ten Cybersecurity Misconfigurations** (AA23-278A, Oct 2023) | The closest thing to a "network Top 10": 1 default configs/credentials · 2 user/admin privilege separation · 3 insufficient internal monitoring · 4 no segmentation · 5 poor patch management · 6 access-control bypass · 7 weak MFA · 8 weak ACLs on shares/services · 9 poor credential hygiene · 10 unrestricted code execution. Sub-items inside #1: default credentials, **insecure AD Certificate Services**, **LLMNR/NetBIOS**, **SMB signing**. | ✅ items 1–5, 10 and sub-items confirmed; 6–9 order from knowledge |
| **CWE Top 25, 2025** | Code-level weakness classes. For network VA it is a **tag** on a CVE, not a test list. Network-relevant: CWE-306 (rank 21), CWE-284 (19), CWE-200 (20), CWE-78 (9), CWE-22 (6). | ✅ |
| **CWE Top 10 KEV Weaknesses, 2025** | The weaknesses behind *exploited* CVEs: CWE-78, 416, 787, **306**, 502, 22, 94, **288**, 122, 79. | ✅ |
| **NSA Network Infrastructure Security Guide** (Jun 2022) | Router/switch/firewall hardening checklist | ✅ cited by AA23-278A |
| **CISA Cybersecurity Performance Goals (CPGs)** | Baseline practices incl. vulnerability scanning and asset documentation | ✅ page; goal text not read |
| **OWASP IoT Top 10** | IoT device weaknesses | 📚 |

### 2.2 Exploitation and exposure data
| Source | Use | Status |
|---|---|---|
| **CISA KEV catalog** | Live list of exploited CVEs; entries dated 8 Oct 2026 present | ✅ |
| **CISA/NSA "Top Routinely Exploited Vulnerabilities"** | Latest I could confirm is the **2023 list (AA24-317A)**: 15 headline CVEs (Citrix NetScaler ×2, Cisco IOS XE ×2, Fortinet FortiOS, MOVEit, Confluence, Log4Shell, Barracuda ESG, Zoho ManageEngine, PaperCut, Netlogon/Zerologon, TeamCity, Outlook, ownCloud) plus 8 more (F5 BIG-IP, BlueKeep, FortiOS path traversal, etc.). **Edge devices dominate.** I did not find a 2024 or 2025 edition. | ✅ |
| **Shadowserver network reports** | **150 report types**, daily Internet-wide scans, each rated CRITICAL/HIGH/MEDIUM/LOW/INFO. The best available checklist of "services that should not be exposed". Section 4 diffs it against Vedha. | ✅ |

### 2.3 Directives that set what "must be fixed" (new in 2026)
| Directive | Date | What matters for a VA | Status |
|---|---|---|---|
| **BOD 26-04** *Prioritizing Security Updates Based on Risk* | 10 Jun 2026 | **Replaces BOD 22-01 and 19-02.** Remediation urgency comes from four variables: **Asset Exposure** (publicly exposed?), **KEV status**, **Exploit Automation** ("Automatable"), **Technical Impact** (partial vs total control). Based on SSVC. CISA publishes the last three per CVE through the **Vulnrichment** programme. Agencies must tag assets with org, environment, exposure (public/internal) and type, and include **private IPs** (RFC 1918/4193) in inventories. | ✅ |
| **BOD 26-02** *End-of-Support Edge Devices* | 5 Feb 2026 | Edge devices = load balancers, firewalls, routers, switches, wireless APs, security appliances, IoT edge. Inventory EOS devices, decommission on a 12/18/24-month schedule; CISA publishes an **EOS Edge Device List** (product, version, EOS date). | ✅ |
| **BOD 23-02** *Internet-Exposed Management Interfaces* | 13 Jun 2023 | Remove an exposed management interface from the internet (or protect it with zero-trust controls) within **14 days** of discovery. | ✅ |

### 2.4 Control frameworks, methods and prioritisation data
| Source | Use | Status |
|---|---|---|
| **CIS Controls v8.1** (18 controls) | **Control 7** Continuous Vulnerability Management; **Control 12** Network Infrastructure Management | ✅ |
| **NIST SP 800-115** | Technical guide to security testing; still the 2008 final | ✅ |
| NIST SP 800-40 Rev 4 (patching), SP 800-53 RA-5, CSF 2.0 ID.RA, SP 800-207 (zero trust) | Patching unit of work, scanning control, risk assessment | ✅ 800-40/800-207 cited by BODs; the rest 📚 |
| **SSVC** (CISA/CERT-CC) | Decision-tree prioritisation behind BOD 26-04 | ✅ |
| CVSS v4.0, **EPSS**, KEV | Severity, exploit likelihood, exploited-in-wild | 📚 |
| **NVD / CVE / CPE** | Vulnerability identity and affected-product data. **Policy changed 15 Apr 2026**, see §5.1. | ✅ |
| MITRE ATT&CK / CAPEC, ISO 27001:2022 A.8.8, PTES, OSSTMM | Attacker-behaviour mapping, control reference, methodology | 📚 (OSSTMM also cited by CERT-In ✅) |
| **Vendor PSIRTs** (Microsoft MSRC, Cisco, Fortinet, Palo Alto, Juniper, F5, Ivanti, Citrix, VMware) | Authoritative fixed-in versions | 📚 |
| **CIS Benchmarks, DISA STIGs, SCAP/OVAL** | Host and device configuration baselines | ✅ STIGs cited by AA23-278A; rest 📚 |

### 2.5 Regulators and compliance
| Regime | Requirement relevant to a VA | Status |
|---|---|---|
| **PCI DSS 11.3** | Internal scans at least quarterly and after significant change, **authenticated**; external scans quarterly **by an Approved Scanning Vendor (ASV)**. Vedha has no credentialed scanning and is not an ASV. | ✅ 11.3.2 ASV (PCI SSC); ⚠️ "authenticated" from a secondary page |
| **CERT-In Comprehensive Cyber Security Audit Policy Guidelines** | Audit **at least once a year**; scope must cover the full estate incl. test/UAT/dev/prod and an asset inventory; reports must classify findings using **both CVSS and EPSS**; audit types include ICS; references OSSTMM and OWASP WSTG | ✅ |
| **SEBI CSCRF** | VAPT frequency "half-yearly for market infrastructure institutions and qualified stockbrokers, at least annually for most" | ⚠️ secondary only |
| RBI IT governance / cyber directions, DPDP Act, ISO 27001 | Frequency and evidence rules | 📚 not verified |

### 2.6 Scanner taxonomies (completeness baselines)
**Nessus plugin families** ✅ (what a mature scanner thinks "all areas" are): Backdoors · CGI abuses (+XSS) · Cisco · Databases · Default Unix Accounts · Denial of Service (only when safe checks are off) · Firewalls · Gain a shell remotely · General · Misc. · Mobile Devices · Netware · Peer-to-Peer · Policy Compliance · Port scanners · SCADA · Service detection · Settings · Web Servers · Windows · Windows: Microsoft Bulletins · Windows: User management · Local Security Checks (28 OS/vendor families incl. F5, Junos, Palo Alto, Huawei, VMware ESX) · Protocol checks (DNS, FTP, RPC, SMTP, SNMP).
**Nessus Network Monitor families** ✅ add: Data Leakage, Cloud Services, Internet Messengers, IRC, IoT, OS Detection, Policy (shadow IT), SSH, Samba.
**Web App Scanning families** ✅: Authentication & Session, Code Execution, Component Vulnerability, CSRF, XSS, File Inclusion, HTTP Security Header, Injection, SSL/TLS.
Greenbone/OpenVAS NVT families 📚 not fetched.

---

## 3. Coverage matrix — the checklist for every assessment

Legend: ✅ covered and rig-verified (per owner, 9 Oct) · 🟢 rule exists, not rig-verified · 🟡 partial · ❌ not covered · ⛔ out of scope by decision.

| # | Area | Authority | Vedha today |
|---|---|---|---|
| 1 | Asset discovery and inventory (incl. private IPs, tagging by exposure) | CIS 1, BOD 26-04, BOD 23-01 | ✅ discovery; 🟡 exposure tagging needs 2+ probes |
| 2 | Open ports and service exposure, TCP and UDP | PCI 11.3, CIS 7 | 🟡 **95 default TCP ports, 5 default UDP ports**; see §4 |
| 3 | Known-CVE matching, ranked by exploitation | NVD/KEV, CIS 7, CERT-In | 🟡 banner-based = "suspected"; see §5.1 |
| 4 | **Edge and network-device CVEs** (VPN, firewall, router, load balancer) | KEV, annual CISA list, BOD 26-02 | ❌ not built (STATUS testing-round-1 item 14) |
| 5 | **End-of-support edge devices** | BOD 26-02 | ❌ OS end-of-life rule exists (`POSTURE-OS-END-OF-LIFE`), no device/firmware lifecycle data |
| 6 | **Internet-exposed management interfaces** | BOD 23-02 | 🟡 admin-UI exposure rule exists at Low severity; check exposure escalation applies |
| 7 | Default and weak credentials | CISA #1, #9 | 🟡 SNMP default community ✅; credential candidate only |
| 8 | TLS, ciphers, certificates | PCI 4.2, CWE-326/327 | ✅ deprecated versions, weak cipher, self-signed, expired; 🟢 weak key, weak signature; ❌ Heartbleed/ROBOT-class checks |
| 9 | Windows: SMB, RDP, MSRPC, NTLM relay | CISA #1, #6, #8 | ✅ verified set |
| 10 | Active Directory: Kerberos, LDAP signing, ADCS, LLMNR/NetBIOS | CISA #1, #9 | 🟡 LDAP anonymous bind 🟢; ❌ Kerberos (port 88 not scanned), ADCS, LLMNR scanning |
| 11 | Remote and management access: SSH, VNC, IPMI, WinRM, Telnet | CISA #8 | ✅ Telnet; 🟢 SSH, VNC, IPMI |
| 12 | File and data services: FTP, NFS, Rsync, DBs | CISA #8 | ✅ FTP anon; 🟢 NFS, Rsync, DB |
| 13 | Infrastructure services: DNS, NTP, SNMP, DHCP | CIS 12 | ✅ SNMP/UDP amplification; 🟢 DNS zone transfer; 🟡 NTP; ❌ DHCP |
| 14 | Mail | CIS 12 | ✅ STARTTLS, VRFY/EXPN; 🟡 open relay |
| 15 | VPN / IKE / SIP / VoIP | KEV, Shadowserver | 🟡 IKE and SIP probes exist, **no rule** (§4.3) |
| 16 | Hypervisor and virtualization management (ESXi, vCenter) | KEV, Shadowserver | ❌ no fingerprinting; SLP (427) not scanned |
| 17 | Container and orchestration exposure | KEV, Shadowserver | 🟢 Docker/K8s/etcd/kubelet exposure; config depth ❌ |
| 18 | Data stores and message queues | Shadowserver | 🟢 Redis/Mongo/ES/Memcached etc.; ❌ ActiveMQ, AMQP, RocketMQ, MSMQ, Hadoop RPC, Erlang EPMD |
| 19 | IoT, printers, cameras | OWASP IoT | ✅ discovery; 🟢 MQTT, RTSP, CWMP, ADB |
| 20 | Segmentation and firewall-rule validation | CISA #4, CIS 12 | 🟡 inferred in attack-path engine; exposure matrix |
| 21 | Backdoors and rogue listeners | Nessus "Backdoors" | 🟢 ~20 known backdoor/C2 ports; banner-confirmed shells |
| 22 | IPv6 | CIS 1, BOD 26-04 | 🟡 link-local ND only |
| 23 | Credentialed host patch and config | PCI 11.3.1, CIS 4, Nessus Local Security Checks | ❌ first cut only (host posture) |
| 24 | Configuration baselines (CIS Benchmarks/STIG) | CIS 4 | ❌ |
| 25 | Prioritisation by SSVC (Automatable, Technical Impact) | BOD 26-04 | ❌ ranking is KEV > EPSS > CVSS |
| 26 | CVSS **and** EPSS in every report | CERT-In | 🟡 EPSS joined to CVE track; confirm both appear on every finding in reports |
| 27 | Change tracking and re-scan | CIS 7, PCI 11.3 | ✅ (catalog flag pending) |
| 28 | Reporting mapped to ATT&CK, CWE, compliance | all | ✅ |
| 29 | Wireless | NIST 800-115 | ⛔ not covered; say so |
| 30 | OT / ICS | IEC 62443, CERT-In | ⛔ not planned (but CERT-In lists ICS as an audit type) |
| 31 | Web application testing | OWASP Top 10 | ⛔ separate Web Sec track, P3 |
| 32 | Cloud posture | CSPM | ⛔ separate track |

## 4. Concrete diffs found in code

### 4.1 Default scan profile
- `IT_PORTS` is **95 TCP ports** (`probe/workflow/gates.py`). **UDP default is 5 ports** (53, 123, 137, 161, 11211).
- `udp_scanner.py` has probes for 12 ports (53, 69, 123, 137, 161, 500, 623, 1900, 4500, 5060, 5353, 11211). The default UDP set omits 69, 500, 623, 1900, 4500, 5060, 5353, so those probes exist but are not in the default UDP port set. **Verify whether another path covers them before treating this as a defect.**
- Not in the default IT TCP set, so the matching scanner is never reached on a standard scan: **rsync 873** (rsync scanner exists), **IPP 631** (printer scanner), **Kerberos 88**.

### 4.2 Shadowserver exposures with no port, probe or rule in Vedha
These are exposures an internet-wide programme rates as worth reporting; none appears in `port_intel.py`, `gates.py` or `udp_scanner.py`.

| Service | Port | Shadowserver rating |
|---|---|---|
| **Cisco Smart Install** | 4786/tcp | CRITICAL |
| **SLP** (ESXi ransomware path) | 427 | HIGH |
| XDMCP | 177/udp | HIGH |
| Radmin | 4899 | HIGH |
| AFP | 548 | HIGH |
| Erlang port mapper (EPMD) | 4369 | HIGH |
| MikroTik service (Winbox) | 8291 | MEDIUM |
| BGP | 179 | HIGH |
| Ubiquiti discovery | 10001/udp | HIGH |
| MSMQ | 1801 | MEDIUM |
| ActiveMQ / AMQP | 61616 / 5672 | MEDIUM / MEDIUM |
| RocketMQ | 9876 | appears only as a *honeypot scan-events* report (HIGH), not an exposed-service report |
| NAT-PMP | 5351/udp | HIGH |
| WS-Discovery, STUN, CoAP | 3702, 3478, 5683 (udp) | MEDIUM |
| QOTD, chargen | 17, 19 | MEDIUM |
| DB2 discovery | 523/udp | HIGH |
| Open HTTP proxy | 3128 | MEDIUM |
| GTP, NTRIP | 2123/2152, 2101 | LOW / INFO |

Service names and ratings are from the Shadowserver report list ✅. Port numbers for Radmin, XDMCP, WS-Discovery, STUN, CoAP and the DVR report are stated on that page; the rest are standard registrations 📚 and should be confirmed before they go into a port table.

Already covered (in `port_intel.py`): Docker, Kubernetes, kubelet, etcd, Redis, MongoDB, Elasticsearch, Memcached, CouchDB, Telnet, FTP, TFTP, VNC, WinRM, X11, ARD, SOCKS, portmapper, NFS, Hadoop UI, many admin UIs, ADB, CWMP.

### 4.3 Collected but no rule
`udp_scanner.py` probes **IKE (500/4500), SIP (5060), mDNS (5353), NetBIOS (137)**, and SIP 5060/tcp is in the default scan, but I found no posture rule for IKE aggressive mode, SIP exposure, mDNS exposure or NetBIOS exposure. This is the cheapest gap to close: the collection half is done.

### 4.4 Not present anywhere in the code
Cisco Smart Install, SLP, **Heartbleed** and ROBOT-class TLS checks, Kerberos, VMware ESXi/vCenter fingerprinting (Shadowserver has a "VMware vCenter CVE-2026-59310 exploitation victim" special report), BGP, ISAKMP aggressive mode. LLMNR appears only in the Sigma/capability mapping, not as a scanner.

## 5. Landscape changes in 2026 that affect Vedha's design

### 5.1 The NVD stopped enriching most CVEs (15 Apr 2026) ✅
NIST now enriches only CVEs in the KEV catalog, software used by the federal government, and critical software (EO 14028): roughly **15–20% of new CVEs** (per the Cloud Security Alliance summary of NIST's notice). About 29,000 backlogged CVEs published before 1 Mar 2026 moved to "Not Scheduled". NIST no longer adds its own CVSS score when the CVE's numbering authority already supplied one.
**Impact:** the "NVD companion" Vedha treats as optional can no longer be assumed to carry CPE, CVSS or CWE for a given CVE. Matching must lean on OSV, CNA-supplied data and CISA's Vulnrichment ADP data, and say "not enriched" rather than "no match".

### 5.2 BOD 26-04 changes the prioritisation vocabulary ✅
KEV > EPSS > CVSS is the pre-2026 model. The new federal model is exposure + KEV + Automatable + Technical Impact. Vedha already has exposure (multi-vantage) and KEV; it lacks Automatable and Technical Impact, which CISA publishes per CVE. Adding them lets Vedha say "fix within N days" in the same terms a customer's regulator may use.

### 5.3 BOD 26-02 and BOD 23-02 are scanner-checkable ✅
EOS edge devices (needs vendor lifecycle data or CISA's EOS list) and internet-exposed management interfaces (needs exposure tagging plus escalation) are both things a network VA can report on directly.

## 6. Recommended backlog (proposed, not yet decided)

| ID | Item | Why | Size | Suggested priority |
|---|---|---|---|---|
| N1 | Rules for already-collected facts: IKE, SIP, mDNS, NetBIOS | Collection is done; rule only | S | P1 |
| N2 | Fix default scan profile gaps: rsync 873, IPP 631, Kerberos 88; confirm UDP default set | Scanners exist but are never reached | S | P1 |
| N3 | Edge/network-device CVE fingerprinting + EOS lifecycle (BOD 26-02) | Edge devices dominate KEV and the annual exploited lists | L | P1 |
| N4 | Hypervisor management: SLP 427 + ESXi/vCenter fingerprint | Ransomware path; KEV and Shadowserver both track it | M | P1 |
| N5 | Prioritisation: add Automatable and Technical Impact from Vulnrichment; make matching NVD-independent (OSV/CNA/ADP) | BOD 26-04 and NVD triage | M | P1 |
| N6 | Exposure catalogue expansion (the §4.2 list), handshake-only, no auth attempts | Closes the Shadowserver diff | M | P2 |
| N7 | TLS: Heartbleed, ROBOT and similar protocol checks | Classic, still checked by every scanner | M | P2 |
| N8 | CVSS **and** EPSS shown on every finding in reports | CERT-In requirement | S | P1 if India clients |
| N9 | AD depth: Kerberos exposure, ADCS, LLMNR/NetBIOS hardening | CISA #1 sub-items | L | P2 |
| N10 | Credentialed scanning | PCI 11.3.1, CIS 4, Nessus Local Security Checks | L | already P1 |

## 7. Deliberately out of scope (say this to clients)
Web application testing (separate Web Sec track), cloud posture, wireless, OT/ICS (not planned), physical security, social engineering, denial-of-service testing (Nessus gates this behind "safe checks off"), exploit validation, endpoint malware, MFA configuration, and code-level CWE auditing. A client who reads "network VA" next to a Top-10 claim will otherwise assume these are included.

## 8. Keeping this current
| Source | Cadence | Where to look |
|---|---|---|
| CISA KEV | daily | cisa.gov/known-exploited-vulnerabilities-catalog |
| CISA BODs | on release | cisa.gov/news-events/directives |
| CWE Top 25 and KEV weaknesses | annual (the 2025 list appeared Dec 2025) | cwe.mitre.org/top25 |
| CISA/NSA top routinely exploited | annual | cisa.gov advisories |
| Shadowserver report list | quarterly diff | shadowserver.org/what-we-do/network-reporting |
| Tenable plugin families | quarterly diff | tenable.com/plugins/families/about |
| NVD policy | on announcement | nist.gov/itl/nvd |
| Regulators (CERT-In, SEBI, RBI, PCI) | on revision | owner: compliance |

## 9. Not verified in this pass
Greenbone/OpenVAS families, OWASP IoT Top 10, ISO 27001:2022, RBI directions, SEBI CSCRF primary text, CVSS/EPSS version details, NSA/CISA misconfiguration items 6–9 order, and any CISA "Top Routinely Exploited" list newer than 2023.
