Here's each scanner module broken into small, atomic use cases — the kind you'd track individually as tickets or test cases. I've kept every use case to a single testable behaviour, marked which ones your engine already does (✓), does partially (~), or is missing (✗), based on the 5 result files.

## 1. Host Discovery

| ID | Use case | Status |
|---|---|---|
| HD-01 | ICMP echo ping sweep across the subnet | ✓ |
| HD-02 | ARP sweep for same-subnet hosts | ✓ |
| HD-03 | TCP SYN ping to common ports for ICMP-blocking hosts | ~ |
| HD-04 | UDP ping for UDP-only hosts (found .59) | ~ |
| HD-05 | IPv6 neighbour discovery | ✗ (ran, found 0, interface null) |
| HD-06 | Record discovery method + reason per host | ✓ |
| HD-07 | Capture MAC address for each live host | ✗ |
| HD-08 | Resolve vendor from MAC OUI | ✗ |
| HD-09 | Reverse-DNS / NetBIOS name resolution | ~ |
| HD-10 | Detect hosts that reply on UDP but no TCP | ✓ (.59) |
| HD-11 | Flag new hosts vs previous scan | ✗ |
| HD-12 | Flag hosts that disappeared vs previous scan | ✗ |

## 2. Host Liveness / Availability

| ID | Use case | Status |
|---|---|---|
| HL-01 | Confirm host still alive before deep checks | ✓ |
| HL-02 | Record which components were skipped when a host drops | ✓ |
| HL-03 | Retry once before declaring a host offline | ✗ |
| HL-04 | Distinguish "network drop" from "device blocked the scanner" | ✗ |
| HL-05 | Re-queue offline hosts for a second pass at scan end | ✗ |
| HL-06 | Timestamp offline events relative to scan start | ~ |

## 3. Port Scan

| ID | Use case | Status |
|---|---|---|
| PS-01 | TCP connect scan of a defined port list | ✓ |
| PS-02 | TCP SYN scan (half-open) | ✗ (config says SYN, falls back) |
| PS-03 | Full UDP port scan | ~ |
| PS-04 | Classify **open** correctly | ✓ |
| PS-05 | Classify **closed** (RST received) correctly | ✗ (recorded as "error") |
| PS-06 | Classify **filtered** (no reply) correctly | ✓ |
| PS-07 | Retry filtered ports before finalizing | ~ (filtered only) |
| PS-08 | Adaptive rate / congestion control that doesn't over-throttle | ✗ (stuck at 10%) |
| PS-09 | Honest per-host health status | ✗ (`ok` despite 87% error) |
| PS-10 | Checkpoint & save partial results on timeout | ✗ (7,178 s lost) |
| PS-11 | Per-host time budget so one host can't stall the run | ✗ |
| PS-12 | Report actual vs configured port count accurately | ✗ (15 vs 65 mismatch) |
| PS-13 | Tarpit / sinkhole detection (host answers every port) | ~ (field exists) |
| PS-14 | Top-N port profile (e.g. top 1,000) as a preset | ~ |

## 4. Service Banner / Version Detection

| ID | Use case | Status |
|---|---|---|
| SB-01 | Grab TCP service banner | ✓ |
| SB-02 | Identify service name from banner | ~ |
| SB-03 | Extract product name | ✗ (mostly null) |
| SB-04 | Extract version string | ✗ (mostly null) |
| SB-05 | Map service+version to a CPE | ✗ |
| SB-06 | Detect RTSP video services (found 554) | ✓ |
| SB-07 | Detect SOCKS proxy (found 1080 on .24) | ✓ |
| SB-08 | Sanitize non-printable bytes in banners | ✗ (`\x00\x00\x01` on 139) |
| SB-09 | Probe custom/unknown ports (6000, 6666, 8888) | ~ |

## 5. OS Fingerprinting

| ID | Use case | Status |
|---|---|---|
| OS-01 | Guess OS family from TCP/IP stack | ✓ |
| OS-02 | Identify Windows build number | ✓ (19041, 22621, 24H2) |
| OS-03 | Identify Linux/embedded OS | ~ |
| OS-04 | Detect device type from combined evidence | ~ (unreliable) |
| OS-05 | Flag end-of-life / end-of-support OS | ✗ (Win10, Win11 22H2) |
| OS-06 | Report confidence score for the guess | ~ |

## 6. TLS / SSL Scan

| ID | Use case | Status |
|---|---|---|
| TLS-01 | Enumerate supported protocol versions | ✓ |
| TLS-02 | Flag TLS 1.0 / 1.1 enabled | ✓ (.19, .65, .252) |
| TLS-03 | Flag SSLv3 / weak ciphers | ~ |
| TLS-04 | Detect missing forward secrecy (grade C) | ✓ |
| TLS-05 | Assign an overall grade (A–F) | ✓ |
| TLS-06 | Parse certificate subject/issuer | ✓ |
| TLS-07 | Detect self-signed certificates | ✓ |
| TLS-08 | Detect expired certificates | ✓ |
| TLS-09 | Flag placeholder/junk certs (CN=cn) | ~ |
| TLS-10 | Flag weak key size (<2048 RSA) | ~ |
| TLS-11 | Check known TLS CVEs (Heartbleed, ROBOT, etc.) | ✗ |

## 7. Web Scan (HTTP/HTTPS)

| ID | Use case | Status |
|---|---|---|
| WEB-01 | Fetch page title & server header | ✓ |
| WEB-02 | Detect tech stack / server product | ~ |
| WEB-03 | Flag missing security headers (CSP, HSTS, X-Frame) | ✓ |
| WEB-04 | Detect dangerous HTTP methods (TRACE on .15) | ✓ |
| WEB-05 | Flag admin panel over plain HTTP (.12, .90) | ✓ |
| WEB-06 | Detect default/vendor landing pages | ~ |
| WEB-07 | Detect outdated web server versions (lighttpd 1.4.54, thttpd 2.29) | ~ (found, not flagged) |
| WEB-08 | Directory traversal / path check | ✗ |
| WEB-09 | Basic injection checks (SQLi, XSS reflection) | ✗ |
| WEB-10 | Detect login form → default-credential opportunity | ✗ |

## 8. SSH Scan

| ID | Use case | Status |
|---|---|---|
| SSH-01 | Grab SSH software banner | ✓ (OpenSSH_9.0) |
| SSH-02 | Enumerate key exchange / cipher / MAC algorithms | ✓ |
| SSH-03 | Flag SHA-1 KEX and MACs | ✓ |
| SSH-04 | Detect Terrapin (CVE-2023-48795) | ✓ |
| SSH-05 | Map banner version to known CVEs (CVE-2024-6387) | ✗ (banner captured, not correlated) |
| SSH-06 | Detect password auth allowed | ~ |
| SSH-07 | Test default/weak SSH credentials | ✗ |

## 9. SMB Scan

| ID | Use case | Status |
|---|---|---|
| SMB-01 | Detect SMB version(s) supported | ✓ |
| SMB-02 | Flag SMBv1 enabled | ✓ |
| SMB-03 | Check whether SMB signing is required | ✓ (.15, .19, .65 not required) |
| SMB-04 | Read OS release string over SMB | ✓ |
| SMB-05 | Enumerate shares (null-session) | ~ |
| SMB-06 | Detect anonymous/guest access | ✗ |
| SMB-07 | Flag NTLM-relay feasibility (signing off + reachable) | ~ (data present, not stated as finding) |
| SMB-08 | Check for EternalBlue-class exposure | ✗ |

## 10. RDP Scan

| ID | Use case | Status |
|---|---|---|
| RDP-01 | Detect RDP service on 3389 | ✓ |
| RDP-02 | Enumerate RDP security layer / TLS versions | ✓ |
| RDP-03 | Flag TLS 1.0/1.1 on RDP (grade F) | ✓ (.19, .65) |
| RDP-04 | Check whether NLA is enforced | ✓ |
| RDP-05 | Detect BlueKeep (CVE-2019-0708) exposure | ✗ |

## 11. SNMP Scan

| ID | Use case | Status |
|---|---|---|
| SNMP-01 | Detect SNMP on 161/udp | ✓ (.252) |
| SNMP-02 | Test default community strings (public/private) | ✓ (public readable) |
| SNMP-03 | Flag SNMP v1/v2c in use | ✓ |
| SNMP-04 | Extract system description via MIB | ✓ |
| SNMP-05 | Flag sensitive data leak (ARP table, interfaces) | ~ (extracted, stored raw) |
| SNMP-06 | Recommend SNMPv3 migration | ✗ |

## 12. UDP Scan

| ID | Use case | Status |
|---|---|---|
| UDP-01 | Probe common UDP services (DNS, NetBIOS, SNMP) | ✓ |
| UDP-02 | Detect DNS open recursion (.1) | ✓ |
| UDP-03 | Resolve `open|filtered` ambiguity with service probes | ✗ (~95% ambiguous) |
| UDP-04 | Detect NetBIOS name service (137) | ✓ |
| UDP-05 | Detect amplification-prone services (NTP, SSDP, memcached) | ~ |

## 13. Printer Scan

| ID | Use case | Status |
|---|---|---|
| PR-01 | Detect print services (9100 raw, 631 IPP, 515 LPD) | ✓ (.252) |
| PR-02 | Identify printer model | ✓ (Brother MFC-T4500DW) |
| PR-03 | Flag raw print port open to whole LAN | ~ |
| PR-04 | Test default printer admin credentials | ✗ |
| PR-05 | Detect stored-job / address-book data exposure | ✗ |

## 14. MSRPC Scan

| ID | Use case | Status |
|---|---|---|
| RPC-01 | Enumerate RPC endpoints on 135 + dynamic range | ✓ |
| RPC-02 | Map dynamic ports (49664–49675) to services | ~ |
| RPC-03 | Detect exposed high-risk interfaces (Task Scheduler, PrintNightmare) | ✗ |
| RPC-04 | Redact/limit raw endpoint storage | ✗ (stored raw) |

## 15. Camera / IoT / NVR Scan (needs building)

| ID | Use case | Status |
|---|---|---|
| CAM-01 | Identify camera/NVR by cert, banner, RTSP UA | ~ (evidence present, classifier ignores it) |
| CAM-02 | Detect RTSP stream requires no authentication | ✗ |
| CAM-03 | Test default camera credentials (admin/admin, etc.) | ✗ |
| CAM-04 | Detect Hikvision/Dahua firmware CVEs | ✗ |
| CAM-05 | Detect exposed SDK/service ports (8000, 6000, 6666) | ~ (found, not explained) |
| CAM-06 | Group identical camera models into one finding | ✗ |

## 16. Network Device Config Audit (needs building)

| ID | Use case | Status |
|---|---|---|
| CFG-01 | Authenticated config pull from switch/router/AP | ✗ |
| CFG-02 | Audit against CIS/STIG benchmark (Cisco, Netgear, etc.) | ✗ |
| CFG-03 | Flag plain-HTTP management (.12, .21) | ~ |
| CFG-04 | Detect default admin credentials on network gear | ✗ |
| CFG-05 | Check firmware version against vendor EOL list | ✗ |

## 17. AI / Correlation Scan

| ID | Use case | Status |
|---|---|---|
| AI-01 | `mcp_ai_scan` produces any output | ✗ (runs, 0 facts, every time) |
| AI-02 | Correlate raw facts into findings with severity | ✗ (`finding_count = 0`) |
| AI-03 | CVE/CVSS/EPSS/KEV enrichment per finding | ✗ |
| AI-04 | Generate remediation text per finding | ~ (only for scan errors) |
| AI-05 | Cross-run reconciliation into one current truth | ✗ |


pipeline- 

Here are the new scanner modules in the same atomic format, continuing the numbering from the previous list (which ended at Module 17). Everything here is net-new, so status is ✗ unless a related check already exists partially (~). As you asked, I've kept **detection** (what the scanner does) and **mapping** (CWE / WSTG / ATT&CK / compliance) as two separate things: each module below is detection-only, and the single mapping table is at the very end.

## 18. LAN Poisoning / Spoofing Scan

| ID | Use case (detection) | Status |
|---|---|---|
| POI-01 | Detect LLMNR responder enabled on the segment | ✗ |
| POI-02 | Detect NBT-NS (NetBIOS name service) enabled | ✗ |
| POI-03 | Detect mDNS responder exposure | ✗ |
| POI-04 | Detect IPv6 accepts rogue Router Advertisements (mitm6) | ✗ |
| POI-05 | Detect ARP spoofing / MITM susceptibility | ✗ |
| POI-06 | Detect rogue DHCP server / DHCP starvation exposure | ✗ |
| POI-07 | Detect WPAD auto-discovery exposure | ✗ |

## 19. Switching / Layer-2 Scan

| ID | Use case (detection) | Status |
|---|---|---|
| L2-01 | Detect CDP/LLDP info leakage from switch ports | ✗ |
| L2-02 | Detect DTP enabled (VLAN hopping via trunk negotiation) | ✗ |
| L2-03 | Detect 802.1Q double-tagging exposure | ✗ |
| L2-04 | Detect STP without BPDU guard (topology manipulation) | ✗ |
| L2-05 | Detect missing port security / MAC flooding exposure | ✗ |

## 20. Segmentation & Firewall Validation

| ID | Use case (detection) | Status |
|---|---|---|
| SEG-01 | Prove VLAN/subnet isolation actually holds (cross-segment reachability test) | ✗ |
| SEG-02 | Detect overly permissive firewall rules (any-any) | ✗ |
| SEG-03 | Test egress filtering (arbitrary outbound ports allowed) | ✗ |
| SEG-04 | Firewalk / infer ACLs in front of a host | ✗ |
| SEG-05 | Detect exposed management plane across segments | ~ (flat /24 observed) |

## 21. VPN / Remote-Access Scan

| ID | Use case (detection) | Status |
|---|---|---|
| VPN-01 | Detect IKE/IPsec service and enumerate transforms | ✗ |
| VPN-02 | Detect IKE aggressive mode / weak DH group | ✗ |
| VPN-03 | Detect SSL-VPN appliance & fingerprint version | ✗ |
| VPN-04 | Correlate SSL-VPN version to CVE/KEV (Fortinet, Palo Alto, Citrix, Ivanti) | ✗ |
| VPN-05 | Detect VPN portal weak TLS / default cert | ✗ |

## 22. Active Directory / Identity Scan

| ID | Use case (detection) | Status |
|---|---|---|
| AD-01 | Detect anonymous / null-session LDAP enumeration | ✗ |
| AD-02 | Kerberoasting exposure (SPN accounts) | ✗ |
| AD-03 | AS-REP roasting exposure (pre-auth disabled) | ✗ |
| AD-04 | MS-RPC coercion exposure (PetitPotam, PrinterBug) | ✗ |
| AD-05 | ADCS misconfiguration (ESC1–ESC8) | ✗ |
| AD-06 | Weak / spray-able domain password policy | ✗ |
| AD-07 | SMB signing enforced domain-wide | ~ (per-host only) |
| AD-08 | Detect legacy NTLMv1 / LM allowed | ✗ |

## 23. Network Services Scan (routing / infra services)

| ID | Use case (detection) | Status |
|---|---|---|
| NS-01 | DNS zone transfer (AXFR) exposure | ✗ |
| NS-02 | DNS open resolver / cache-poisoning exposure | ~ (open recursion on .1 found) |
| NS-03 | NTP mode-6/7 amplification & info leak | ✗ |
| NS-04 | SSDP / UPnP amplification & info leak | ~ (UPnP string seen on .21) |
| NS-05 | SNMP write-community exposure | ✗ (read-only tested) |
| NS-06 | BGP/OSPF unauthenticated neighbor exposure | ✗ |
| NS-07 | Detect amplification-prone services (memcached, chargen, LDAP) | ✗ |

## 24. Firmware & Config-Baseline Scan

| ID | Use case (detection) | Status |
|---|---|---|
| FW-01 | Firmware version → vendor EOL/EOS correlation | ✗ |
| FW-02 | Known backdoor / hard-coded account detection per device family | ✗ |
| FW-03 | Config drift vs golden baseline | ✗ |
| FW-04 | Certificate lifecycle (expiry window, weak key, self-signed in prod) | ~ (detected, not lifecycle-tracked) |
| FW-05 | Unsigned / outdated firmware advisory flagging | ✗ |

## 25. Wireless Scan (if in scope)

| ID | Use case (detection) | Status |
|---|---|---|
| WIFI-01 | Rogue AP / evil-twin detection | ✗ |
| WIFI-02 | WPA2/WPA3 config & PMKID exposure | ✗ |
| WIFI-03 | WPS enabled detection | ✗ |
| WIFI-04 | Open / weak-encryption SSID detection | ✗ |

---

## Separate mapping table (detection ID → standards)

This is the part you asked to keep separate. Each scanner use case maps to the weakness class and framework control it satisfies. This is what makes findings audit-ready.

| Use case ID(s) | CWE | OWASP WSTG | MITRE ATT&CK | Compliance driver |
|---|---|---|---|---|
| POI-01, POI-02, POI-03 | CWE-290 | — | T1557.001 (LLMNR/NBT-NS poisoning) | CIS 7, internal PT |
| POI-04 | CWE-290 | — | T1557.003 (IPv6 RA) | BOD 23-01 (IPv6 coverage) |
| POI-06 | CWE-306 | CONF-01 | T1557 | — |
| L2-01 | CWE-200 | CONF-01 | T1200 | CIS 4 |
| L2-02, L2-03 | CWE-284 | CONF-01 | T1599 (network boundary bridging) | PCI seg. |
| SEG-01, SEG-05 | CWE-923 | CONF-01 | T1046 | **PCI 11.4.5 (seg. testing)** |
| SEG-02, SEG-03 | CWE-284 | CONF-01 | T1090 | ISO A.8.20, CIS 4 |
| VPN-02 | CWE-326 | CRYP | T1600 | RBI/SEBI crypto |
| VPN-03, VPN-04 | CWE-1035 (known-vuln) | CONF-05 | T1133 (external remote services) | **CISA KEV / BOD 26-04** |
| AD-01 | CWE-200 | ATHN | T1087 (account discovery) | CIS 5/6 |
| AD-02, AD-03 | CWE-522 | ATHN | T1558.003 / T1558.004 | internal PT |
| AD-04 | CWE-306 | — | T1187 (forced auth) | — |
| AD-05 | CWE-269 | — | T1649 (steal/forge cert) | — |
| AD-06 | CWE-521 | ATHN | T1110 (password spray) | PCI 8, ISO A.8.5 |
| AD-07, AD-08 | CWE-287 | ATHN | T1557.001 (NTLM relay) | CIS 4 |
| NS-01 | CWE-200 | CONF-01 | T1590 | CERT-In / OSSTMM |
| NS-02, NS-03, NS-04, NS-07 | CWE-406 (amplification) | — | T1498.002 | ISO A.8.20 |
| NS-05 | CWE-284 | — | T1602 (config repository) | — |
| FW-01, FW-05 | CWE-1104 (unmaintained components) | — | — | **PCI 6/11, ISO A.8.8** |
| FW-02 | CWE-798 (hard-coded creds) | ATHN | T1078.001 (default accounts) | SANS/CWE Top 25 #22 |
| FW-03 | CWE-1188 (insecure default config) | CONF-01 | — | CIS 4, STIG |
| WIFI-01 | CWE-290 | — | T1557 | internal PT |
| WIFI-02, WIFI-03 | CWE-326 | CRYP | T1600 | — |

Also relevant to the modules from the earlier list (so the mapping is complete):

| Earlier use case | CWE | WSTG | ATT&CK |
|---|---|---|---|
| PS-01…PS-06 (port scan) | CWE-200 | CONF-01 | T1046 |
| SB-05 (CPE), AI-03 (CVE match) | CWE-1035 | INFO-02 | T1595.002 |
| WEB-04 (dangerous methods) | CWE-650 | CONF-06 | — |
| WEB-03 (missing headers) | CWE-693 | CONF-07/12/14 | — |
| TLS-02…TLS-04 (weak TLS) | CWE-326/327 | CRYP | T1040 |
| SSH-04 (Terrapin) | CWE-300 | CRYP | T1557 |
| SMB-03 (signing) | CWE-287 | — | T1557.001 |
| SNMP-02 (default community) | CWE-798 | ATHN | T1078.001 |
| CAM-03, PR-04, CFG-04 (default creds) | CWE-798 | ATHN | T1078.001 |
| OS-05 (EOL) | CWE-1104 | — | — |

**Running total across all 25 modules:** roughly 40 working/partial and about 95 use cases still to build, now with a CWE, WSTG, and ATT&CK tag on each so every finding is traceable to a standard.



