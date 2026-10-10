# Network VA — scenario catalogue (verified, to-test, gaps)

**Date:** 2026-10-10 · **Purpose:** one list to build test scenarios from. Every row is a check Vedha either already performs or should. **Docs only; no code changed.**

**Sources:** `docs/STATUS.md` (P1-4 to P1-7), the owner's list of rig-verified checks (9 Oct), [`NETWORK_VA_USE_CASES.md`](../../NETWORK_VA_USE_CASES.md), the [8 Oct use-case doc](../planning/2026-10-08-network-va-usecases-and-scanner-prompt.md), the archived [probe QA doc](../archive/probe-va-use-cases-qa.md), and the [coverage framework](../research/2026-10-09-network-va-coverage-framework.md). Rule IDs are from `manager/detection_engine/posture_rules.py`; where a rule ID is not certain the row says "category" instead of inventing one.

## How the tiers work

| Tier | Meaning | What the scenario must prove |
|---|---|---|
| **V** | Rig-verified, client-ready (owner, 9 Oct) | Regression: it still works, and a clean control stays clean |
| **R** | Called "confirmed" in older docs but **not** on the 9 Oct client-ready list | Re-confirm, then promote to V or demote |
| **T** | Built and unit-tested, **never rig-validated** | First real validation; this is where false positives hide |
| **G** | **Gap**: not built, or built but never reaches a finding | Build first, then write the same three scenarios |

## Three controls every scenario needs
1. **Positive**: a target that has the weakness; expect the finding with the stated rule, severity and evidence.
2. **Clean control**: the same service, configured safely; expect **no finding** and a rule trace of "clean" (not "no-evidence").
3. **Blind control**: the service filtered or unreachable; expect "no-evidence", never "clean". This is the repo's *coverage-proven clean* guarantee.

Record provenance for each run (target, date, pcap or ground-truth JSON, report path). The accuracy merge gate allows no accuracy claim without it. **The 9 Oct verified list has no recorded rig run yet** (see `STATUS.md` P1-6).

**Suggested lab targets** (from the 8 Oct plan): a Windows 11 box with toggleable SMB/RDP/Defender settings (the .74 / .77 rigs); a Samba container (SMBv1, null session, signing); a Debian container with old OpenSSH, vsftpd, bind9, NFS, rsyncd, OpenLDAP, Postfix, x11vnc, `ipmi_sim`, snmpd; Redis/Mongo with no auth; nginx with TLS 1.0 and a self-signed/expired cert. Use an isolated VMnet, **not** the owner's Wi-Fi adapter.

---

## Tier V — rig-verified, client-ready (18)

| ID | Check | Rule / category | Positive | Clean control | Pass |
|---|---|---|---|---|---|
| V01 | SMBv1 enabled | `POSTURE-SMB-V1-ENABLED` | Samba/Windows with SMB1 on | SMB1 off | Critical finding with dialect evidence |
| V02 | SMB signing not required | `POSTURE-SMB-SIGNING-OFF` | `server signing = disabled` | signing required | High finding |
| V03 | SMB null session | `POSTURE-SMB-NULL-SESSION` | anonymous enumeration allowed | `RestrictAnonymous` set | Medium finding; users/shares in evidence |
| V04 | RDP without NLA | `POSTURE-RDP-NO-NLA` | NLA off | NLA required | High finding |
| V05 | RDP legacy / no-TLS layer | `POSTURE-RDP-NO-TLS` | standard RDP security only | TLS/CredSSP | High finding |
| V06 | RDP exposed / reachable | `POSTURE-RDP-EXPOSED` | 3389 reachable | firewalled (blind control) | Low inventory finding; none when filtered |
| V07 | MSRPC endpoint mapper enumerable | `POSTURE-MSRPC-EPMAP-EXPOSED` | 135 open, anonymous map | 135 filtered | Medium finding with endpoint list |
| V08 | Telnet cleartext | exposed-service, cleartext category | telnetd on 23 | closed | Finding at stated severity |
| V09 | FTP cleartext + anonymous login | `POSTURE-FTP-ANONYMOUS-LOGIN` + exposed FTP | vsftpd anon on | anon off | High finding; login result in evidence |
| V10 | SMTP no STARTTLS | `POSTURE-SMTP-NO-STARTTLS` | Postfix without TLS | STARTTLS offered | Low finding |
| V11 | SMTP VRFY/EXPN enumeration | `POSTURE-SMTP-USER-ENUMERATION` | VRFY enabled | disabled | Medium finding |
| V12 | Web / HTTP admin interface exposed | exposed-service, admin-UI category | Grafana/Webmin/Proxmox UI | not exposed | Finding names the product |
| V13 | SNMP default community | `POSTURE-SNMP-DEFAULT-COMMUNITY` | `public`/`private` | custom community | High finding |
| V14 | UDP amplification service | `POSTURE-UDP-AMPLIFIER` | open resolver / NTP / memcached | none enabled | Medium finding; measured factor if present |
| V15 | Correlation: NTLM-relay path | NTLM-relay correlation | signing off **and** SMBv1 (as the owner worded it) | either one fixed | Compound finding; confirm it does not require SMBv1 if you quote it that way |
| V16 | Correlation: legacy-Windows surface | legacy-Windows correlation | SMBv1 + exposed RDP | either fixed | High→Critical, severity amplified by role |
| V17 | **Caveat:** version-to-CVE mapping | CVE track | clean parse, e.g. OpenSSH 8.2p1 | unparsable banner | "Suspected" unless authoritative; no CVE on a blank version |
| V18 | **Caveat:** service/banner identification | `service_banner` | known banners | no banner | Blank product/version is allowed; no invented values |

### Verified use cases (live targets, per the one-pager)
| ID | Use case | Code | Scenario |
|---|---|---|---|
| U01 | Network Discovery | `1` | /24 with known live hosts: recall and precision vs ground truth |
| U02 | Device Identification | `2` | mixed devices: role correct, confidence shown |
| U03 | Full Security Assessment | `10` | end-to-end on the lab; findings match V/R/T rows |
| U04 | Network VA, full campaign | `12` | live per-stage progress; a stage error does not stop the run |
| U05 | Windows / SMB | `30` | V01–V03 |
| U06 | SNMP weak credentials | `50` | V13 |
| U07 | UDP & amplification | `51` | V14 |
| U08 | IoT & embedded | `60` | camera/MQTT/printer emulators |
| U09 | Full-port audit (65k) | `80` | service on a non-standard port; completeness self-check passes |
| U10 | Internet-exposure mapping | `81` | two probes, different reach |
| U11 | Deep Port Sweep / single-host Deep scan | `82` | finishes within budget; cancelled run keeps finished hosts |
| U12 | Re-scan & Change Detection | `11` | **done per owner; catalog flag still `coming_soon`.** New host, new port, closed port, version change |

---

## Tier R — "confirmed" in older docs, not on the client-ready list: re-confirm (18)

| ID | Check | Positive | Clean / blind control | Pass |
|---|---|---|---|---|
| R01 | TCP state taxonomy (open / closed / filtered) | open, RST-closed, dropped ports | filtered host | three states reported distinctly; RST is "closed", never "error" |
| R02 | UDP discovery with reply decode | DNS/NTP/SNMP reply | silent port | "open\|filtered" never read as open |
| R03 | Banner capture is honest | SSH/FTP/SMTP banner | service with no banner | "no banner", nothing fabricated |
| R04 | Printer detection via real PJL | JetDirect 9100 | port open, not a printer | PJL handshake required |
| R05 | OS fingerprint (TTL + SMB2) | Linux, Windows, network gear | wrong-TTL host | family correct with confidence |
| R06 | Host liveness (ARP/ICMP) | live hosts | down hosts | retry-once before "offline" |
| R07 | SYN / mass scan feeds deep routing | open ports populate deep scanners | Linux with raw sockets vs connect fallback | same open set either way |
| R08 | TLS deprecated version | TLS 1.0 / SSLv3 | TLS 1.2+ only | High finding |
| R09 | TLS weak cipher | NULL/EXPORT/RC4/DES | modern ciphers | Medium finding |
| R10 | TLS self-signed certificate | self-signed | CA-signed | Medium finding |
| R11 | TLS expired certificate | expired | valid | Medium finding |
| R12 | Backdoor/C2 listener | Meterpreter handler on 4444 | empty port | finding; banner-confirmed shell raises confidence |
| R13 | Container API exposed | Docker 2375, kubelet, etcd | closed | High finding |
| R14 | Unauthenticated-prone datastore | Redis/Mongo/ES/Memcached | auth enabled | Medium finding |
| R15 | Database port directly exposed | MySQL/Postgres/MSSQL | firewalled | Medium finding |
| R16 | Remote-access service exposed | VNC / WinRM / X11 | closed | Medium finding |
| R17 | Internet-facing severity escalation | same service seen from two vantages | internal only | severity rises only when externally reachable |
| R18 | Port precision/recall on a real host | host with firewalled extra ports | — | 100% precision and recall, extra firewalled ports not reported |

---

## Tier T — built, never rig-validated (first real test)

### Remote access, files, directory (lab: Debian container set)
| ID | Check | Rule | Positive | Clean | Pass |
|---|---|---|---|---|---|
| T01 | SSH weak KEX/cipher/MAC | `POSTURE-SSH-WEAK-ALGORITHMS` | old OpenSSH / Dropbear | modern sshd | High finding listing algorithms |
| T02 | SSH Terrapin | `POSTURE-SSH-TERRAPIN` | vulnerable build | patched | Medium finding |
| T03 | VNC no auth | `POSTURE-VNC-NO-AUTH` | x11vnc `-nopw` | password set | Critical finding |
| T04 | VNC weak (DES) auth | `POSTURE-VNC-WEAK-AUTH` | legacy VNC auth | strong | Medium finding |
| T05 | IPMI cipher-zero | `POSTURE-IPMI-CIPHER-ZERO` | `ipmi_sim` cipher 0 | disabled | Critical finding |
| T06 | LDAP anonymous bind | `POSTURE-LDAP-ANONYMOUS-BIND` | OpenLDAP anon on | off | Low finding |
| T07 | LDAP anonymous search | `POSTURE-LDAP-ANONYMOUS-SEARCH` | directory returned | denied | Medium finding with content proof |
| T08 | DNS zone transfer | `POSTURE-DNS-ZONE-TRANSFER` | bind9 AXFR allowed | denied | High finding |
| T09 | DNS version disclosure | `POSTURE-DNS-VERSION-DISCLOSURE` | `version.bind` answers | hidden | Low finding |
| T10 | NFS world-readable export | `POSTURE-NFS-WORLD-READABLE-EXPORT` | `*(ro)` export | restricted | High finding |
| T11 | Rsync anonymous module | `POSTURE-RSYNC-ANONYMOUS-MODULE` | anon module | auth required | High finding |
| T12 | DB unauthenticated read | `POSTURE-DB-UNAUTHENTICATED-ACCESS` | Redis/Mongo no auth | auth on | Critical finding |
| T13 | DB cleartext transport | `POSTURE-DB-CLEARTEXT-TRANSPORT` | no TLS | TLS on | Medium finding |

### TLS, web, IoT, AI
| ID | Check | Rule | Pass |
|---|---|---|---|
| T14 | Weak certificate key (<2048 RSA) | `POSTURE-TLS-WEAK-KEY` | High finding; 2048+ stays clean |
| T15 | Certificate signed with MD5/SHA-1 | `POSTURE-TLS-WEAK-SIGNATURE` | High finding |
| T16 | Dangerous HTTP methods | `POSTURE-WEB-DANGEROUS-METHODS` | Medium; GET/POST only is clean |
| T17 | HTTPS without HSTS | `POSTURE-WEB-NO-HSTS` | Low finding |
| T18 | MQTT broker accepts anonymous clients | `POSTURE-MQTT-UNAUTHENTICATED` | High; auth-required broker is clean |
| T19 | RTSP endpoint exposed | `POSTURE-RTSP-EXPOSED` | Medium; see G05 for unauthenticated stream |
| T20 | CWMP / TR-069 exposed | `POSTURE-CWMP-EXPOSED` | Medium finding |
| T21 | Android ADB unauthenticated | `POSTURE-ADB-UNAUTHENTICATED` | Critical finding |
| T22 | AI / MCP endpoint without auth | `POSTURE-AI-ENDPOINT-UNAUTHENTICATED` | High; authenticated endpoint is clean |
| T23 | SNMP measured GETBULK amplification | `POSTURE-SNMP-AMPLIFIER` | Medium with measured factor |
| T24 | OS past end-of-support | `POSTURE-OS-END-OF-LIFE` | High; supported OS is clean |
| T25 | Default-credential candidate | `POSTURE-DEFAULT-CRED-CANDIDATE` | High *candidate*; never "confirmed" |

### Host posture / indicators of attack (needs the Windows/Linux inventory the probe collects)
| ID | Check | Pass |
|---|---|---|
| T26 | Endpoint protection disabled (Defender off) | High, confirmed tier |
| T27 | Service binary in a user-writable directory | High, confirmed |
| T28 | Unquoted Windows service path | Medium, confirmed |
| T29 | Excessive local administrators | Low, confirmed |
| T30 | Known miner/malware process (curated list) | Critical, confirmed; benign process names stay clean |
| T31 | Backdoor listener bound on the host | High, confirmed |
| T32 | TLS fingerprint (JARM/JA4S/JA4X) matches known tooling | High, suspected IOC tier |

### Correlations and intelligence
| ID | Check | Pass |
|---|---|---|
| T33 | AD exposure (anon LDAP + SMB; worse on a DC) | Medium→Critical |
| T34 | Exposed management plane (IPMI cipher-0 / WinRM+RDP) | High→Critical |
| T35 | Cleartext cluster (≥2 cleartext services on one host) | Medium |
| T36 | Exposed datastore + unauthenticated access | Critical |
| T37 | Default SNMP on network infrastructure | Medium→High |
| T38 | Anonymous data exposure (≥2 anonymous channels) | finding fires only at ≥2 |
| T39 | User enumeration + weak auth | finding fires only with both |
| T40 | KEV/EPSS exploitability overlay (e.g. SMBv1→EternalBlue, RDP-no-NLA→BlueKeep) | named CVE attached; severity unchanged, risk boosted |
| T41 | Attack paths: relay edges, credential reuse, capability map, crown-jewel auto-selection | route to a crown jewel appears; empty result is explained, never "safe" |

### Round-1 fixes to verify live (fixed in code on `claude/serene-bardeen-1uqxzq`)
| ID | Fix | Pass |
|---|---|---|
| T42 | Chain of custody stamped on every finding (round-1 #1) | `sha256`, `captured_at`, `captured_by`, `source_host` present; tampering is detected |
| T43 | Duplicate findings collapsed (#2) | FTP/Telnet give one finding per condition, not 3–6; two real issues on one port stay separate |
| T44 | RDP SCHANNEL inner-TLS measured (#3) | RDP host with TLS 1.0 gets a TLS finding |
| T45 | Version→CVE false positives (#4) | OpenSSH 9.5 and vsftpd 3.0.3 no longer produce open-ended-range CVEs; authoritative (dpkg) findings unchanged |
| T46 | KEV escalation is OS-gated (#5) | BlueKeep escalates on Windows 7, not Windows 11 |
| T47 | EPSS alone cannot make Critical (#6) | DoS at low confidence caps at High |

### Platform behaviour
| ID | Check | Pass |
|---|---|---|
| T48 | Coverage-proven clean + auto-close | needs N consecutive coverage-proven clean runs; a blind rule never auto-closes |
| T49 | Multi-vantage exposure | internet-reachable vs internal-only separated |
| T50 | IPv6 link-local discovery and dual-stack scan | v6-only host appears; scope enforced |
| T51 | Verification tiers and `needs_review` | KEV or critical/high uncertain findings flagged; AI can only downgrade; OT never actively validated |
| T52 | Partial-safe deep scans | cancel mid-run keeps finished hosts |
| T53 | Scale: no 0.62 ports/s collapse; ~4.3 MB/host; per-host chunks | benchmark assertions hold |
| T54 | **Safety**: scope enforcement, blackout windows, fragile-asset guard | nothing outside scope is touched; blocked job explains why |
| T55 | Database Exposure use case (`40`) | needs a DB target; promote out of `coming_soon` |
| T56 | Web & TLS use case (`20`), TLS half | web half needs a 80/443 target (Web Sec, P3) |
| T57 | Web App use case (`21`) | fingerprint only (Web Sec, P3) |
| T58 | AI & MCP use case (`61`) | probe-side collection needed (AI Sec, P1) |

---

## Tier G — gaps: build first, then test

### G-A. P1-4 quick wins (decided, `STATUS.md`)
| ID | Gap | What to build | Positive scenario |
|---|---|---|---|
| G01 | SNMPv3 noAuth | noAuth/noPriv security-level check + rule | snmpd with a noAuth user |
| G02 | UPnP / SSDP IGD | manager rule on collected `rootDesc.xml` | miniupnpd with IGD |
| G03 | TFTP unauthenticated read | RRQ for a common file + rule | tftpd serving a file |
| G04 | NTP monlist measured amplification | measured-factor fact + rig validation | ntpd with monlist |
| G05 | RTSP unauthenticated stream | stream-open check beyond OPTIONS | RTSP server without auth |
| G06 | FTP anonymous **write** | write-permission check + rule | vsftpd `anon_upload_enable` |
| G07 | SMTP open relay | manager rule on the scanner's result | Postfix relaying to external |

### G-B. Collected but no rule (cheapest)
| ID | Gap | Positive scenario |
|---|---|---|
| G08 | IKE aggressive mode / vulnerable ISAKMP | strongSwan with aggressive mode |
| G09 | SIP exposure (5060) | Asterisk/Kamailio |
| G10 | mDNS exposure (5353) | avahi |
| G11 | NetBIOS exposure (137) | Samba `nmbd` |

### G-C. Default scan reach
| ID | Gap | Positive scenario |
|---|---|---|
| G12 | rsync 873, IPP 631, Kerberos 88 missing from the default IT TCP set | standard scan finds rsync/CUPS/KDC |
| G13 | Default UDP set is 5 ports; probes exist for 12 (69, 500, 623, 1900, 4500, 5060, 5353 omitted); verify first whether another path covers them | standard UDP scan reaches TFTP/IKE/IPMI/SSDP/SIP/mDNS |

### G-D. Exposures Shadowserver rates that Vedha lacks (port + handshake + rule)
| ID | Service | Port (📚 confirm) | Rating |
|---|---|---|---|
| G14 | Cisco Smart Install | 4786/tcp | CRITICAL |
| G15 | SLP | 427 | HIGH |
| G16 | XDMCP | 177/udp | HIGH |
| G17 | Radmin | 4899 | HIGH |
| G18 | AFP | 548 | HIGH |
| G19 | Erlang EPMD | 4369 | HIGH |
| G20 | BGP | 179 | HIGH |
| G21 | MikroTik Winbox | 8291 | MEDIUM |
| G22 | Ubiquiti discovery | 10001/udp | HIGH |
| G23 | MSMQ | 1801 | MEDIUM |
| G24 | ActiveMQ / AMQP | 61616 / 5672 | MEDIUM |
| G25 | NAT-PMP | 5351/udp | HIGH |
| G26 | WS-Discovery, STUN, CoAP, QOTD, chargen, DB2 discovery | 3702, 3478, 5683, 17, 19, 523 | MEDIUM–HIGH |
| G27 | Open HTTP proxy / open SOCKS (unauthenticated) | 3128, 1080 | MEDIUM |

Scenario for each: positive = the service listening; clean = closed or authenticated; **safety rule = handshake only, no auth attempts**.

### G-E. Vulnerability depth
| ID | Gap | Scenario |
|---|---|---|
| G28 | Heartbleed, ROBOT-class TLS checks | vulnerable OpenSSL lab |
| G29 | ESXi / vCenter fingerprint + SLP | ESXi version banner → CVE |
| G30 | Edge-device CVE fingerprinting (Fortinet, Citrix, Cisco, Palo Alto, Ivanti, F5, Juniper, Sophos) | device banners / TLS cert / login-page tells |
| G31 | End-of-support edge devices (BOD 26-02) | device on a lifecycle list → finding |
| G32 | Internet-exposed management interface escalation (BOD 23-02) | admin UI reachable from outside → severity rises |

### G-F. Prioritisation and reporting
| ID | Gap | Scenario |
|---|---|---|
| G33 | SSVC fields: Automatable and Technical Impact (BOD 26-04) | KEV CVE ranks above same-CVSS non-KEV |
| G34 | NVD-independent matching and a "not enriched" state (NVD triage, 15 Apr 2026) | CVE with no CPE/CVSS is labelled, not silently dropped |
| G35 | CVSS **and** EPSS on every finding in reports (CERT-In) | every report row shows both |

### G-G. Active Directory and credentialed
| ID | Gap | Scenario |
|---|---|---|
| G36 | Kerberos exposure, AS-REP / Kerberoast (network-observable only) | lab AD |
| G37 | ADCS misconfiguration | AD CS with weak templates |
| G38 | LLMNR / NetBIOS name-resolution exposure | enabled vs disabled |
| G39 | LDAP signing / channel binding off | DC with signing off |
| G40 | Credentialed scanning (SSH/WinRM/SMB), patch level | confirmed vs suspected patch state; needed for PCI 11.3.1 |
| G41 | CIS / SCAP benchmarks | compliance percentage on a hardened vs default host |
| G42 | Confirmed default-credential testing (opt-in, RoE-gated, lockout-safe) | candidate → confirmed |

### G-H. Other
| ID | Gap | Scenario |
|---|---|---|
| G43 | DHCP exposure | rogue DHCP |
| G44 | Active IPv6 sweep (/64, DHCPv6, RA) | v6-only subnet |
| G45 | Placeholder leakage ("not recorded") in reports (round-1 #7) | report shows real OS/service values |
| G46 | Role misclassification (round-1 #8) | VMware workstation not called hypervisor |
| G47 | Full-port / UDP profile misses (round-1 #9) | rsync, VNC found on re-scan |
| G48 | SNMP write community not distinguished (round-1 #12) | wording or controlled SET decision |
| G49 | Report quality: coverage tautology, duplicate ATT&CK refs, repro steps, window vs scan date (round-1 #13) | report review checklist |
| G50 | Container / Kubernetes config audit | RBAC / anonymous API |

**Out of scope, no scenario:** OT/ICS passive (not planned), wireless, cloud posture, web-application testing beyond fingerprint.

---

## Counts
V 18 + 12 use cases · R 18 · T 58 · G 50 · out of scope 4 areas.
