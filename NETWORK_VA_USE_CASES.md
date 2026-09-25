# Vedha — Network VA Use Cases, Coverage & Capability Proposal

A client-facing summary of what Vedha's network vulnerability assessment **actually detects and has verified**, what is **in the pipeline**, what is **still on the backlog**, and the **testing evidence** behind each claim.

**Legend**
- ✅ **Verified & shipped** — backed by a scanner + detection rule with unit/rig test evidence.
- 🟡 **In pipeline** — designed, partially built, or `coming_soon` in the product.
- ⬜ **Backlog** — planned, not yet started.

> Architecture in one line: the **probe** runs inside the customer network as a *collection-only* sensor (dials **out** over one HTTPS/WSS port, **zero inbound listener** — adds no attack surface); the **manager** does all detection, scoring and correlation. This split is itself a differentiator (see USPs).

---

## 1. Proposed Network VA Use Cases (what we offer the client)

Each use case is dispatched by a stable numeric code; the probe maps it to exactly one scan pipeline.

| Code | Use case | Value to the client | Status | Typical runtime |
|-----:|----------|---------------------|:------:|-----------------|
| `1`  | **Network Discovery** | Live-host + open-port inventory of what is actually on the network — a fast, no-impact "what do I have" baseline. | ✅ | 2–5 min /24 |
| `2`  | **Device Inventory & Classification** | Every device identified and role-classified (workstation / server / network gear / printer / hypervisor / IoT) from OS, ports and banners — evidence-based, never a hostname guess. | ✅ | 5–15 min /24 |
| `10` | **Full Security Assessment** | Complete sweep: hosts → services → OS → TLS/web/SMB/DB/SNMP exposure. The baseline posture picture in one run. | ✅ | 15–60 min /24 |
| `12` | **Network Vulnerability Assessment (Full Campaign)** | The flagship end-to-end campaign, run as one job with live per-stage progress: discovery → inventory → deep service assessment → Windows/SMB → SNMP/UDP → internet-exposure → prioritized CVE candidates. | ✅ | 30–90 min /24 |
| `30` | **Windows & File-Sharing (SMB) Security** | Confirms SMBv1 is off and SMB signing is enforced — closing the EternalBlue / NTLM-relay class of attacks. | ✅ | 5–15 min |
| `50` | **SNMP Weak-Credential Check** | Finds routers/switches/printers answering default community strings ("public"/"private") — a classic config-read + lateral-movement primitive. | ✅ | 2–8 min |
| `51` | **UDP & Amplification Exposure** | Flags open resolvers and DDoS-amplification services (DNS, NTP monlist, memcached, SSDP, chargen) the client could be abused as a reflector for. | ✅ | 2–8 min |
| `60` | **IoT & Embedded Device Discovery** | Surfaces cameras (RTSP), printers, DVRs, MQTT brokers and Telnet-exposed gear — the unmanaged corner of most networks. | ✅ | 3–10 min /24 |
| `80` | **Full-Port Audit (all 65,535)** | Every TCP port on a host, with a completeness self-check so a clean result is genuinely clean — catches services hiding on non-standard ports. | ✅ | 20–90 min /host |
| `81` | **Internet-Exposure Mapping (multi-vantage)** | With two or more probes, separates *truly internet-exposed* services from internal-only ones — answers "what can an outside attacker actually reach?" | ✅ | 5–15 min /24 |
| `82` | **Deep Port Sweep (few hosts)** | Full 65,535-port stealth sweep budgeted for a small, high-value host set (crown-jewel deep dive). | ✅ | 20–90 min/host (≤3 hosts) |
| `11` | **Re-scan & Change Detection** | Re-runs an assessment and highlights *what changed* — new hosts, newly opened ports, config drift. | 🟡 | 15–60 min /24 |
| `20` | **Web & TLS/SSL Security Check** | Grades TLS/SSL config (protocol versions, cipher strength, cert health) on web servers. | 🟡 | 5–15 min |
| `21` | **Web Application Security Check** | Fingerprints web apps — methods, security headers, server tech — a pre-flight before a full web-app pentest. | 🟡 | 5–15 min |
| `40` | **Database Exposure Check** | Checks whether MySQL/Postgres/MSSQL/Redis/Mongo are reachable and accept unauthenticated connections. | 🟡 | 3–10 min |
| `61` | **AI & MCP Endpoint Discovery** | Discovers exposed AI inference endpoints and Model-Context-Protocol servers — a fast-growing, unmonitored surface. | 🟡 | 3–8 min |
| `70` | **OT / ICS Passive Discovery** | Listen-only inventory for industrial networks — zero active packets, so fragile OT gear is never probed. | 🟡 | operator-set |

---

## 2. Coverage Areas (what we look at)

| Area | Protocols / surfaces covered | Underlying capability |
|------|------------------------------|-----------------------|
| **Host & port discovery** | ICMP/ARP liveness, TCP connect + stateless SYN, protocol-specific UDP | port_scanner, syn_scanner, udp_scanner |
| **Service identification** | SSH, SMTP, FTP, Telnet, VNC, HTTP(S) banners; soft-match service table | service_banner + TLS rung |
| **TLS / crypto** | Versions, ciphers, cert (self-signed/expired), JARM fingerprint | tls_scanner / tls_fingerprint |
| **Windows estate** | SMB1/2 negotiate, signing, null session, MSRPC endpoint mapper | smb_scan / msrpc_scan |
| **Remote access** | RDP (NLA/TLS), VNC (auth type), WinRM, X11, ARD | service + posture rules |
| **Directory & mail** | LDAP anonymous bind, DNS AXFR, SMTP STARTTLS / VRFY-EXPN | dedicated probes |
| **File services** | FTP anon, NFS world-readable exports, Rsync anon modules | dedicated probes |
| **Infra / OOB** | SNMP (v1 community + MIB walk + amplification, v3 presence), IPMI/BMC | snmp_scan / ipmi |
| **Databases** | MySQL/Postgres/MSSQL/Oracle/Redis/Mongo/Elastic reachability + unauth read + cleartext transport | db_fingerprint |
| **IoT / printers** | RTSP, MQTT, 9100 PJL, 631 IPP printer identity | service_fingerprint / printer_scan |
| **OS fingerprint** | TTL + TCP window/MSS + ICMP multi-probe → OS family, EOL check | os_stage |
| **IPv6** | RFC 4861 link-local Neighbor Discovery (no /64 enumeration) | ipv6_discovery |
| **Exposure & backdoors** | ~90-port intel catalog: backdoor/C2, container APIs, datastores, admin UIs, cleartext | port_intel |
| **Known-CVE correlation** | Observed product+version → CVE candidates, KEV/EPSS/CVSS prioritized | manager CVE track |

---

## 3. Vulnerabilities & Misconfigurations We Detect (verified)

**36 posture checks** (29 hand-written rules + 7 exposed-service categories), **5 multi-signal attack-path correlations**, and a **CVE intelligence track**. Every rule carries a severity, CWE and MITRE ATT&CK technique.

| Category | Check | Severity | CWE | MITRE |
|----------|-------|:--------:|-----|-------|
| Windows/SMB | SMBv1 enabled (EternalBlue/WannaCry transport) | Critical | CWE-477 | T1210 |
| Windows/SMB | SMB signing not required (NTLM relay) | High | CWE-306 | T1557.001 |
| Windows/SMB | SMB null session (anon enumeration) | Medium | CWE-306 | T1087.002 |
| Windows/SMB | MSRPC endpoint mapper exposed | Medium | CWE-200 | T1135 |
| Remote access | RDP without NLA (pre-auth surface) | High | CWE-287 | T1210 |
| Remote access | RDP refuses TLS (legacy RC4, MITM) | High | CWE-326 | T1040 |
| Remote access | RDP reachable from vantage (info) | Low | CWE-284 | T1021.001 |
| Remote access | VNC with no authentication | Critical | CWE-306 | T1021.005 |
| Remote access | VNC weak/legacy DES auth | Medium | CWE-327 | T1021.005 |
| Crypto/TLS | Deprecated SSL/TLS version (SSLv3/TLS1.0/1.1) | High | CWE-326 | T1040 |
| Crypto/TLS | Weak TLS cipher (NULL/EXPORT/RC4/DES/anon) | Medium | CWE-327 | T1040 |
| Crypto/TLS | Self-signed certificate | Medium | CWE-295 | T1557 |
| Crypto/TLS | Expired certificate | Medium | CWE-298 | T1557 |
| Crypto/SSH | SSH Terrapin (CVE-2023-48795) | Medium | CWE-354 | T1557 |
| Crypto/SSH | SSH weak KEX/cipher/MAC (CBC, SHA-1, 1024-bit DH) | High | CWE-327 | T1040 |
| Cleartext | SMTP without STARTTLS | Low | CWE-319 | T1040 |
| Cleartext | Database cleartext transport (no TLS) | Medium | CWE-319 | T1040 |
| Info disclosure | DNS AXFR zone transfer allowed | High | CWE-200 | T1590.002 |
| Info disclosure | LDAP anonymous bind | Low | CWE-306 | T1087.002 |
| Info disclosure | SMTP VRFY/EXPN user enumeration | Medium | CWE-200 | T1087.003 |
| File services | FTP anonymous login | High | CWE-287 | T1078.001 |
| File services | NFS world-readable export | High | CWE-732 | T1039 |
| File services | Rsync anonymous module | High | CWE-306 | T1039 |
| OOB / BMC | IPMI cipher-zero auth bypass (BMC takeover) | Critical | CWE-287 | T1078 |
| SNMP/UDP | SNMP default community | High | CWE-1392 | T1078 |
| SNMP/UDP | UDP amplification service (DDoS reflector) | Medium | CWE-406 | T1498.002 |
| Database | Unauthenticated database read (Redis/Mongo) | Critical | CWE-306 | T1213 |
| Host posture | OS past end-of-support (EOL catalog) | High | CWE-1104 | T1190 |
| Host posture | Default-credential candidate (vendor allowlist) | High | CWE-1392 | T1078.001 |
| Exposed ports | Backdoor / C2 listener (Meterpreter, NetBus, Mirai…) | High | CWE-506 | T1571 |
| Exposed ports | Container/orchestration API exposed (Docker/K8s/etcd) | High | CWE-306 | T1610 |
| Exposed ports | Unauth-prone datastore (Redis/Mongo/Elastic/Memcached) | Medium | CWE-306 | T1210 |
| Exposed ports | Traditional database reachable | Medium | CWE-284 | T1210 |
| Exposed ports | Cleartext/legacy protocol (Telnet/rlogin/TFTP…) | High–Low | CWE-319 | T1040 |
| Exposed ports | Remote-access/mgmt service (VNC/WinRM/X11) | Medium | CWE-284 | T1021 |
| Exposed ports | Admin/dev/CI web UI (Grafana/Webmin/Proxmox…) | Low | CWE-284 | T1190 |
| **Correlation** | NTLM-relay path (SMB signing off, worse on a DC) | Med→Crit | — | T1557.001, T1210 |
| **Correlation** | Legacy Windows surface (SMBv1 + exposed RDP) | High→Crit | — | T1210, T1021.001 |
| **Correlation** | Cleartext cluster (≥2 cleartext services on one host) | Medium | — | T1040 |
| **Correlation** | Exposed datastore + unauth access (data breach) | Critical | — | T1210, T1078, T1005 |
| **Correlation** | Default SNMP on network infra (lateral movement) | Med→High | — | T1602.001, T1078 |

### 3a. CVE / Exploitability Intelligence (verified)

| Aspect | How it works | Why it's trustworthy |
|--------|--------------|----------------------|
| Version → CVE | Observed product+version → CPE 2.3 candidate → **offline OSV snapshot** version-range match (dpkg/epoch-aware) | Fully **offline & deterministic** — no data leaves the network; every run records `db_snapshot_hash` |
| Confirmed vs suspected | "Confirmed" requires the range match **and** an authoritative (credentialed) source; banner-inferred stays "suspected, backport-possible" | We never claim a vuln we can't substantiate |
| Prioritization | CISA **KEV** + FIRST **EPSS** + CVSS joined per finding; precedence KEV > EPSS≥0.5 > EPSS≥0.1 > CVSS | Client sees *actually-exploited* risk first, not just high CVSS |
| Exploitability overlay | Posture findings linked to live CVEs (SMBv1→EternalBlue, RDP-no-NLA→BlueKeep, SMB-signing→PetitPotam, container→Docker-API, MSRPC→PrintNightmare) | Turns a config finding into a named, prioritized attack |

---

## 4. USPs — What Differentiates Us (shipped)

| USP | What it means | Why the client should care |
|-----|---------------|----------------------------|
| **Zero-inbound probe** | Sensor dials out on one port, never listens | Deploying Vedha adds *no* attack surface — one egress firewall rule to approve |
| **Confirmed-vs-suspected discipline** | A finding is only "confirmed" with authoritative evidence | No false-alarm fatigue; findings are defensible |
| **Coverage-proven "clean"** | Every rule records match / clean / no-evidence / drift; a blind rule can't masquerade as clean; auto-close needs N consecutive coverage-proven clean runs | A green report is genuinely green — the #1 trust problem in VA tools |
| **Offline / air-gap CVE matching** | OSV snapshot + KEV/EPSS pinned locally, deterministic | Works in sovereign/air-gapped networks; no telemetry leakage |
| **Attack-path correlation** | Multi-signal composites, severity amplified by device role (DC / network gear) | Shows the *chain*, not just isolated findings |
| **Tiered verification** | Passive tiers (confirmed/corroborated/inferred/contradicted) + AI rationale that can only **downgrade** + safe RoE-gated active validation (OT structurally passive) | High-confidence prioritization without unsafe probing |
| **Partial-safe deep scans** | Two-phase: fast high-signal pass committed per host, then budgeted tail; a cancelled/timed-out job keeps finished hosts | Big scans never lose hours of work to one interruption |
| **Grounded, injection-hardened AI advisor** | Customer-facing assistant answers only from *their* recorded evidence, fenced against prompt injection from scanned banners | Explains findings + remediation in plain language, safely |
| **Sealed-probe IP protection** | Nuitka native binary + Ed25519 signed, host-locked license | Ship the sensor to a client without exposing source |

---

## 5. In Pipeline (building now / next)

| Item | What it adds | Status |
|------|--------------|:------:|
| Web & TLS/SSL triage (`uc 20`) | Cert/cipher/protocol grading as a standalone use case | 🟡 coming_soon |
| Web application triage (`uc 21`) | Method/header/tech fingerprint pre-pentest | 🟡 coming_soon |
| Database exposure check (`uc 40`) | DB reachability + unauth as a standalone use case | 🟡 coming_soon |
| AI & MCP endpoint discovery (`uc 61`) | Exposed inference / MCP server surface | 🟡 coming_soon |
| OT / ICS passive discovery (`uc 70`) | Listen-only industrial inventory | 🟡 coming_soon |
| Re-scan & change detection (`uc 11`) | Delta reporting between runs | 🟡 coming_soon |
| EDR/SIEM detection-coverage grader | Matches attack actions vs SIEM/EDR alerts → ATT&CK coverage % + Sigma-rule gap recommendations | 🟡 built, integrating |
| NVD companion snapshot | Optional NVD/CPE data beside OSV | 🟡 optional |
| Regional compliance packs + sector/BFSI AI gateway | Jurisdiction-aware guidance (IN/EU/UK/US/ME/APAC), cloud/hybrid/sovereign deployment profiles | 🟡 branch, unmerged |

---

## 6. Backlog — Use Cases We Still Need To Build

| # | Capability | Why we need it | Priority |
|---|------------|----------------|:--------:|
| 1 | **Credentialed / authenticated scanning** | Turn "default-cred candidate" into *confirmed*; deeper patch/config visibility | High |
| 2 | **CIS / SCAP compliance benchmarking** | No compliance-benchmark scanning today; clients ask for CIS baselines | High |
| 3 | **Confirmed default-credential testing** | Currently candidate-only (safe); needs opt-in safe login attempts | Medium |
| 4 | **Deeper web-app testing** | Beyond triage — injection/authz checks (RoE-gated) | Medium |
| 5 | **Container / Kubernetes config audit** | Beyond "exposed" flag — RBAC/anonymous-API depth | Medium |
| 6 | **Cloud / hybrid asset coverage** | Extend beyond on-prem network to cloud posture | Medium |
| 7 | **CI-automated rigs for printer, IPv6, SYN, OS-fingerprint** | Raw-socket / ICMP paths are logic-tested but not CI-run (platform-gated) | Medium |
| 8 | **Active NDP / DHCPv6 IPv6 sweep** | Today IPv6 is link-local ND only (no /64 enum by design) | Low |

---

## 7. Testing & Verification Status

Scale: probe ≈ 2,190 test functions across ~165 files; manager backend ≈ 1,410 across ~144 files; detection engine posture/pipeline suites; plus a manual field rig (`probe/tests/scan/`, 11 scanners × 5 intensities).

| Capability | Test / rig evidence | Automated CI | Known gap |
|------------|---------------------|:------------:|-----------|
| port_scanner | `test_port_scan_budget`, `test_port_state_ranges`, `test_two_phase_port_coverage` + rig | ✅ | Reachability-from-vantage only (by design) |
| udp_scanner | `test_async_udp` (real loopback), `test_udp_amplifiers` + rig | ✅ | No-reply is open\|filtered (inherent) |
| service_banner | `test_service_banner_ident` (18), `test_banner_pass_concurrency` + rig | ✅ | Records banner; mapping to vuln is the detection layer |
| TLS / crypto | integration + legacy-version + posture + fingerprint tests | ✅ | Fingerprint only, not trust decision |
| snmp_scan | unit tests + `uc_snmp_exposure` rig | ✅ | Community list, not brute-force |
| syn_scanner | `test_syn_coverage_and_pacing` (24), `test_syn_budget_wiring` | 🟡 logic only | Raw-socket path Linux-only, not CI-run; falls back to connect |
| tail budget (deep scans) | `test_tail_budget` (25) | ✅ | — |
| os_fingerprint | `test_os_fingerprint` (62), `test_os_stage_wiring` (19) | 🟡 logic only | ICMP socket I/O not portably CI-run |
| ipv6_discovery | `test_ipv6_discovery` (8) + `test_ipv6_wiring` (14) | ✅ unit | No dedicated field rig |
| printer_scan | `test_printer_scanner` (7, mocked socket) | 🟡 unit only | No rig; real 9100 path via ad-hoc ground-truth |
| posture rules | `test_posture_rules`, `test_service_posture_rules`, `test_db_posture_rules`, `test_posture_confidence` | ✅ | — |
| exposed-service detection | `test_exposed_services`, `test_exposure_analytics` | ✅ | — |
| CVE track (matcher/enrich) | matcher/correlate/enrichment unit suites (offline snapshot) | ✅ | Data currency = snapshot age |
| verification tiers & non-finding trace | `test_verification_core`, `test_active_validation_*`, `test_detection_coverage`, `test_posture_trace` | ✅ | — |

**Verification model (the trust story):** findings map to a four-word confidence vocabulary — **confirmed** (credentialed/authoritative), **corroborated** (strong network evidence), **inferred** (single weak signal), **contradicted** (only ever set downward). Uncertain + high-stakes findings (KEV or critical/high) are flagged `needs_review`, and may be escalated to **safe active validation** only when Rules-of-Engagement allow and the profile isn't OT. An optional AI rationale tier can *only downgrade*, never raise confidence. Non-findings explain themselves via six mutually-exclusive rule outcomes, so "clean" always means *coverage-proven clean*, never "the scanner silently didn't run."

---

*Grounded in the Vedha repository as of 2026-09-25 — probe scanners, `manager/detection_engine` posture rules, `manager/backend/app/detection` correlation + CVE track, and the probe/manager test suites. Items marked 🟡/⬜ are roadmap, not current guarantees.*
