# Vedha Probe — Network Scanning Capability Matrix

Marked against the **current** probe code (`probe/scanner/*`, `probe/agent/*`) as
of 2026-08-12. This tracks which network-VA capabilities the probe supports
today, so gaps are visible and plannable.

**Legend:** ✅ supported · 🟡 partial (detection/port-level, or with a caveat) · ❌ not present

**Caveats:** `†` needs root / `CAP_NET_RAW` (Linux) · `‡` only if the `nmap` binary is present

**Note:** the probe is **collection-only** by design — it finds exposures and
misconfigurations, not CVEs. CVE correlation / risk scoring is explicitly a
separate, out-of-scope layer (see
`docs/superpowers/specs/2026-08-10-native-host-discovery-engine-design.md` §2).

---

## Discovery

| Capability | Status | Backed by |
|---|:--:|---|
| Host discovery scan | ✅ | `host_discovery` (TCP-connect + ARP-cache fusion) |
| IPv4 discovery | ✅ | `host_discovery` |
| IPv6 discovery | 🟡 | resolves/scans IPv6 targets; no active NDP sweep |
| ARP discovery | 🟡 | ARP-cache harvest (passive read); active `-PR` via nmap‡ |
| ICMP ping scan | ✅ | `os_fingerprint` (ICMP echo/timestamp; unpriv datagram or raw†) |
| TCP ping scan | ✅ | `host_discovery`; nmap `-PS/-PA`‡ |
| UDP ping scan | 🟡 | `udp_scanner` service probes (not a generic UDP ping) |
| DNS discovery scan | 🟡 | mDNS/DNS-SD in `iot_scanner`; no full DNS enumeration |
| Reverse DNS scan | 🟡 | mDNS PTR only; no `in-addr.arpa` sweep |

## Port scanning

| Capability | Status | Backed by |
|---|:--:|---|
| TCP port scan | ✅ | `port_scanner` |
| UDP port scan | ✅ | `udp_scanner` |
| Full-port scan (65,535) | ✅ | `mass_scan -p 1-65535` |
| Common-port scan | ✅ | `port_scanner` top-ports |
| Custom-port scan | ✅ | `-p` on every scanner |
| TCP SYN scan | ✅† | `syn_scanner` (Linux + raw socket; SYN-cookie stateless) |
| TCP connect scan | ✅ | `port_scanner` |
| TCP ACK scan | ❌ | — |
| TCP FIN scan | ❌ | — |
| TCP NULL scan | ❌ | — |
| TCP Xmas scan | ❌ | — |
| Firewall-filtering scan | 🟡 | SYN/UDP report open/closed/**filtered** (no dedicated ACK map) |

## Service detection / fingerprinting

| Capability | Status | Backed by |
|---|:--:|---|
| Service detection scan | ✅ | `service_banner` |
| Service-version detection | ✅ | `service_banner`; nmap `-sV`‡ |
| Operating-system fingerprinting | ✅ | `os_fingerprint` (ICMP+TTL); nmap `-O`‡ |
| Network-device fingerprinting | 🟡 | MAC→OUI vendor + banners + SNMP sysDescr |
| Banner-grabbing scan | ✅ | `service_banner` |
| Protocol detection on non-standard ports | 🟡 | `db_scanner`/`iot_scanner` by response, not universal |

## TLS / SSL

| Capability | Status | Backed by |
|---|:--:|---|
| TLS/SSL configuration scan | ✅ | `tls_scanner` |
| Digital-certificate scan | ✅ | `tls_scanner` |
| Cipher-suite scan | ✅ | `tls_scanner` + `tls_fingerprint` (JARM) |

## Vulnerability / credentialed

| Capability | Status | Backed by |
|---|:--:|---|
| Unauthenticated vulnerability scan | 🟡 | exposures/misconfig only (no CVE DB — out of scope) |
| Authenticated vulnerability scan | 🟡 | `ssh_collector`/`windows_collector` config gather (no CVE) |
| Windows credentialed scan | ✅ | `windows_collector` |
| Linux/Unix SSH credentialed scan | ✅ | `ssh_collector` |
| Network-device credentialed scan | 🟡 | via SSH/SNMP; no dedicated module |

## Per-protocol / per-service scans

| Capability | Status | Backed by |
|---|:--:|---|
| SNMP scan | ✅ | `snmp_scanner` (community checks) |
| SMB scan | ✅ | `smb_scanner` (dialect + signing) |
| RDP scan | 🟡 | port 3389 detection only (no NLA/enum) |
| SSH scan | ✅ | `service_banner` + `ssh_collector` |
| FTP/SFTP scan | 🟡 | FTP banner on 21; SFTP via SSH; no protocol checks |
| HTTP/HTTPS service scan | ✅ | `web_scanner` |
| DNS service scan | 🟡 | UDP recursion check + mDNS; no zone transfer |
| DHCP service scan | ❌ | — |
| LDAP/LDAPS scan | 🟡 | 389/636 port + LDAPS TLS; no LDAP query |
| Kerberos service scan | ❌ | — |
| SMTP/IMAP/POP3 scan | 🟡 | banner grab + STARTTLS/implicit-TLS ports; no protocol checks |
| NTP service scan | ✅ | `udp_scanner` (mode-3 + monlist) |
| RPC service scan | 🟡 | port 135 detection only |
| Telnet service scan | ✅ | `service_banner` / `iot_scanner` |
| Database-service scan | ✅ | `db_scanner` |
| VPN-gateway scan | 🟡 | IKE 500/4500 (UDP) detection |
| Firewall/router/switch scan | 🟡 | SNMP + banner + OS fingerprint |
| Hypervisor-management scan | ❌ | no ESXi/vCenter-specific |
| Remote-management interface scan | 🟡 | RDP/SSH/WinRM/IPMI(623) as ports |

## Configuration / posture / policy

| Capability | Status | Backed by |
|---|:--:|---|
| Default-credential check | 🟡 | SNMP communities ✅; MQTT/DB unauth; no broad brute |
| Weak-protocol scan | ✅ | weak TLS, SMBv1, Telnet/cleartext |
| Network misconfiguration scan | 🟡 | exposed svc, missing headers, open recursion, unauth |
| Missing-patch scan | ❌ | no CVE/patch DB |
| Firmware vulnerability scan | ❌ | — |
| End-of-life software/device scan | ❌ | version seen, no EOL DB |
| Internal network vulnerability scan | 🟡 | exposure-based |
| External network vulnerability scan | 🟡 | exposure-based |
| Network-segmentation validation scan | ❌ | — |
| Rogue-device scan | 🟡 | discovery/inventory; baseline diff at manager |
| Unauthorized-service scan | 🟡 | inventory; policy diff at manager |

## Specialized / OT / wireless / IoT

| Capability | Status | Backed by |
|---|:--:|---|
| Wireless network scan | ❌ | no Wi-Fi scanning |
| IoT-device scan | ✅ | `iot_scanner` (SSDP/UPnP, RTSP, MQTT, CoAP) |
| Printer and VoIP-device scan | 🟡 | printer 9100 in IoT set; VoIP SIP 5060; partial |
| Passive OT/ICS discovery scan | ✅ | `passive_collector` (`ot` profile, passive-only) |
| Low-impact OT/ICS vulnerability scan | 🟡 | OT profile is passive-only; no active OT checks |

## Lifecycle / scheduling

| Capability | Status | Backed by |
|---|:--:|---|
| Scheduled recurring scan | 🟡 | manager/agent scheduling infra |
| Scan after significant network changes | 🟡 | `delta_scanner` / `uc_rescan_delta` (manual trigger) |
| Targeted vulnerability retest | 🟡 | service-specific / re-scan mode |

## Compliance

| Capability | Status | Backed by |
|---|:--:|---|
| Compliance configuration scan | ❌ | — |
| CIS Benchmark scan | ❌ | — |
| SCAP/OVAL configuration scan | ❌ | — |

---

## Tally (~78 items)

| | Count |
|---|:--:|
| ✅ Full | ~26 |
| 🟡 Partial | ~33 |
| ❌ None | ~19 |

## Biggest gaps (❌ — nothing today)

- **Stateless flag scans:** TCP ACK / FIN / NULL / Xmas (`syn_scanner` is SYN-only; the raw-socket core exists, so these are extendable).
- **Missing per-service modules:** DHCP, Kerberos, hypervisor-management.
- **Vuln/patch intelligence:** missing-patch, firmware, end-of-life (all need a version→CVE/EOL DB the probe deliberately doesn't ship).
- **Posture/topology:** network-segmentation validation.
- **Wireless:** no Wi-Fi scanning.
- **Compliance:** CIS Benchmark, SCAP/OVAL, compliance config — needs a config-audit engine that doesn't exist yet.

## Scanner module → capability quick map

| Module | Provides |
|---|---|
| `host_discovery` | liveness, IPv4/6, ARP-cache, TCP ping, mobile/MAC |
| `os_fingerprint` | ICMP ping, TTL→OS |
| `syn_scanner` | TCP SYN (Linux/raw) |
| `port_scanner` | TCP connect, common/custom ports |
| `mass_scan` | full-range / fast sweep (masscan + fallback) |
| `service_banner` | banners, version strings |
| `tls_scanner` / `tls_fingerprint` | TLS config, cert, ciphers, JARM |
| `web_scanner` | HTTP/HTTPS fingerprint, headers, methods |
| `udp_scanner` | UDP services + amplification (NTP/DNS/memcached/SSDP/mDNS) |
| `smb_scanner` | SMB dialect + signing |
| `snmp_scanner` | SNMP communities + sysDescr |
| `db_scanner` | DB protocol fingerprint (MySQL/PG/MSSQL/Redis/Mongo/Oracle) |
| `mcp_ai_scanner` | AI/MCP endpoint discovery |
| `iot_scanner` | SSDP/UPnP, RTSP, MQTT, CoAP |
| `mobile_scanner` | mobile device exposure (ADB, etc.) |
| `nmap_wrapper` | ‡ discovery, `-sV`, `-O`, SMB scripts |
| `ssh_collector` / `windows_collector` | credentialed Linux / Windows |
| `passive_collector` | passive OT/ICS discovery |
| `delta_scanner` | re-scan / change delta |
