# Vedha Scanner — Individual Script Run Results

**Target:** `192.168.1.65` (DESKTOP-34M18MB)
**Vantage:** `192.168.1.66` (Rutik's MacBook Air — same LAN)
**Date:** 2026-09-04 · 00:34 IST → 00:42 IST
**Method:** Each `main_scripts` module executed individually via `PYTHONPATH=probe/ .venv/bin/python3 -m main_scripts.<module>`
**Scope file:** `/tmp/s.txt` → `192.168.1.0/24`
**Raw JSONL files:** `/tmp/scan_individual/`

---

## Module 01 — host_discovery

```
Command: python3 -m main_scripts.host_discovery -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/01_host_discovery.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "host_discovery",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:34:20.306609+05:30",
  "status": "open",
  "data": {
    "alive": true,
    "state": "confirmed_alive",
    "confidence": 0.99,
    "responding_ports": [
      {"port": 22,   "state": "open"},
      {"port": 445,  "state": "open"},
      {"port": 3389, "state": "open"}
    ],
    "method": "tcp+arp",
    "reason": "syn_ack",
    "evidence": [
      {"method": "tcp_connect", "port": 22,   "result": "syn_ack", "confidence": 0.97},
      {"method": "tcp_connect", "port": 445,  "result": "syn_ack", "confidence": 0.97},
      {"method": "tcp_connect", "port": 3389, "result": "syn_ack", "confidence": 0.97},
      {"method": "arp_neighbor", "result": "cache", "nud": "arp",
       "mac": "34:f3:9a:a1:a9:8c", "confidence": 0.55}
    ],
    "mac": "34:f3:9a:a1:a9:8c",
    "randomized_mac": false,
    "arp_state": "cache"
  },
  "evidence": "tcp 22/open, 445/open, 3389/open; arp 34:f3:9a:a1:a9:8c [cache]",
  "method": "tcp+arp",
  "confidence": 0.99
}
```

**Result:** Host is **ALIVE**. TCP SYN-ACK received on ports 22, 445, 3389. ARP cache confirms MAC `34:f3:9a:a1:a9:8c` — non-randomised (physical or VM NIC).

---

## Module 02 — port_scanner

```
Command: python3 -m main_scripts.port_scanner -t 192.168.1.65 -s /tmp/s.txt
         --profile top1000 --concurrency 300 --rate 500
Output : /tmp/scan_individual/02_port_scan.jsonl
```

**Scan summary (from scan_summary record):**
```json
{
  "ports_requested": 1121,
  "ports_attempted": 1121,
  "ports_not_scanned": 0,
  "open": 19,
  "closed": 1102,
  "filtered": 0,
  "duration_s": 164.3,
  "health": "ok",
  "tarpit": {
    "likely_tarpit": false,
    "open_ratio": 0.0169,
    "reason": "open-port distribution is consistent with a real host"
  },
  "congestion": {
    "final_window": 22,
    "max_window": 300,
    "throttled": true
  },
  "reprobe": {
    "candidates": 220,
    "resolved": 220,
    "remaining": 0
  }
}
```

**Open ports — raw TCP connect results:**

| Port | RTT (ms) | Source IP | Method |
|------|----------|-----------|--------|
| 22 | — | — | connect |
| 135 | — | — | connect |
| 139 | — | — | connect |
| 445 | — | — | connect |
| 902 | — | — | connect |
| 912 | — | — | connect |
| 2179 | — | — | connect |
| 3389 | — | — | connect |
| 5040 | — | — | connect |
| 5985 | — | — | connect |
| 47001 | — | — | connect |
| 49664 | — | 192.168.1.66 | connect |
| 49665 | — | 192.168.1.66 | connect |
| 49666 | — | 192.168.1.66 | connect |
| 49667 | — | 192.168.1.66 | connect |
| 49668 | 3.83 | 192.168.1.66 | connect |
| 49677 | 4.98 | 192.168.1.66 | connect |
| 49678 | 8.81 | 192.168.1.66 | connect |
| 49679 | 7.02 | 192.168.1.66 | connect |

**Open port list:** `[22, 135, 139, 445, 902, 912, 2179, 3389, 5040, 5985, 47001, 49664, 49665, 49666, 49667, 49668, 49677, 49678, 49679]`

Note: Port 7680 (Windows Update Delivery Optimization) was open in the previous run_all.py run — not included this pass (top1000 profile coverage varies slightly by timing/congestion window).

---

## Module 03 — udp_scanner

```
Command: python3 -m main_scripts.udp_scanner -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/03_udp.jsonl
```

**Raw JSONL output — all probed ports:**

```json
{"port": 53,    "proto": "udp", "status": "closed",        "evidence": "ICMP port-unreachable (closed)",              "data": {"service_guess": "dns"}}
{"port": 69,    "proto": "udp", "status": "closed",        "evidence": "ICMP port-unreachable (closed)",              "data": {"service_guess": "tftp"}}
{"port": 123,   "proto": "udp", "status": "open|filtered", "evidence": "no UDP or ICMP response (open|filtered)",     "data": {"service_guess": "ntp",  "reason": "no_response"}}
{"port": 137,   "proto": "udp", "status": "open",          "evidence": "netbios-ns replied with 175 bytes",           "data": {"service": "netbios-ns", "responded": true, "reply_bytes": 175,
  "reply_hex_head": "80008400000000010000000020434b414141414141414141414141414141414141414141414141414141414141000021"}}
{"port": 161,   "proto": "udp", "status": "open|filtered", "evidence": "no UDP or ICMP response (open|filtered)",     "data": {"service_guess": "snmp", "reason": "no_response"}}
{"port": 500,   "proto": "udp", "status": "open|filtered", "evidence": "no UDP or ICMP response (open|filtered)",     "data": {"service_guess": "ike",  "reason": "no_response"}}
{"port": 623,   "proto": "udp", "status": "closed",        "evidence": "ICMP port-unreachable (closed)",              "data": {"service_guess": "ipmi"}}
{"port": 1900,  "proto": "udp", "status": "open|filtered", "evidence": "no UDP or ICMP response (open|filtered)",     "data": {"service_guess": "ssdp", "reason": "no_response"}}
{"port": 4500,  "proto": "udp", "status": "open|filtered", "evidence": "no UDP or ICMP response (open|filtered)",     "data": {"service_guess": "ike-nat", "reason": "no_response"}}
{"port": 5060,  "proto": "udp", "status": "closed",        "evidence": "ICMP port-unreachable (closed)",              "data": {"service_guess": "sip"}}
{"port": 5353,  "proto": "udp", "status": "open|filtered", "evidence": "no UDP or ICMP response (open|filtered)",     "data": {"service_guess": "mdns", "reason": "no_response"}}
{"port": 11211, "proto": "udp", "status": "closed",        "evidence": "ICMP port-unreachable (closed)",              "data": {"service_guess": "memcached"}}
```

**Summary:**

| Port | Service | Status | Evidence |
|------|---------|--------|----------|
| 53 | DNS | closed | ICMP port-unreachable |
| 69 | TFTP | closed | ICMP port-unreachable |
| 123 | NTP | open\|filtered | No response |
| **137** | **NetBIOS-NS** | **OPEN** | **175 bytes reply — confirmed** |
| 161 | SNMP | open\|filtered | No response |
| 500 | IKE/IPSec | open\|filtered | No response |
| 623 | IPMI | closed | ICMP port-unreachable |
| 1900 | SSDP | open\|filtered | No response |
| 4500 | IKE-NAT | open\|filtered | No response |
| 5060 | SIP | closed | ICMP port-unreachable |
| 5353 | mDNS | open\|filtered | No response |
| 11211 | Memcached | closed | ICMP port-unreachable |

NetBIOS-NS hex reply head: `80008400000000010000000020434b41...` — standard NBNS name response containing the workstation's NetBIOS name.

---

## Module 04 — os_fingerprint

```
Command: python3 -m main_scripts.os_fingerprint -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/04_os_fingerprint.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "os_fingerprint",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:39:43.665325+05:30",
  "status": "open",
  "data": {
    "alive": true,
    "icmp_reply": true,
    "icmp_echo_reply": true,
    "observed_ttl": 128,
    "os_guess": "Windows",
    "confidence": 0.97,
    "stack_guess": null,
    "signals": {
      "initial_ttl": 128,
      "observed_ttl": 128,
      "ttl_source": "icmp_echo",
      "hop_estimate": 0,
      "support_count": 1
    },
    "os_release": "Windows 11 24H2",
    "os_build": 26100,
    "os_version": "10.0.26100",
    "hostname": "DESKTOP-34M18MB"
  },
  "evidence": "ICMP echo reply ttl=128 -> Windows (conf 0.5); SMB2 NTLM build 26100 -> Windows 11 24H2 (conf 0.97)",
  "method": "icmp_echo+smb2_ntlm_version",
  "confidence": 0.97
}
```

**Fingerprint chain:**
1. ICMP echo reply with TTL=128 → Windows OS family (initial_ttl=128 is the Windows default; 0 hops to target = same LAN)
2. SMB2 NTLM NTLMSSP negotiate response → build number `26100` → maps to **Windows 11 24H2** (confidence 0.97)
3. Hostname extracted from NTLMSSP target name field: `DESKTOP-34M18MB`

OS identification: **Windows 11 24H2, build 10.0.26100** — zero credentials required.

---

## Module 05 — snmp_scanner

```
Command: python3 -m main_scripts.snmp_scanner -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/05_snmp.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "snmp_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:40:10.131593+05:30",
  "port": 161,
  "proto": "udp",
  "status": "open|filtered",
  "data": {
    "responded": false,
    "reason": "no_snmp_response"
  },
  "evidence": "no SNMP reply to common communities (open|filtered)"
}
```

**Result:** SNMPv1 + SNMPv2c community string probes (public, private, community) sent to UDP/161. No response. Port is `open|filtered` — Windows Firewall is blocking the probe or SNMP is not running. No information disclosed via SNMP.

---

## Module 05b — ipmi_scanner

```
Command: python3 -m main_scripts.ipmi_scanner -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/05b_ipmi.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "ipmi_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:40:13.299003+05:30",
  "port": 623,
  "proto": "udp",
  "status": "filtered",
  "data": {
    "ipmi": null,
    "reason": "no_ipmi"
  }
}
```

**Result:** UDP/623 was closed (ICMP port-unreachable in the UDP scan) and no IPMI GetDeviceID response was received. No BMC/iDRAC/iLO present — expected for a workstation.

---

## Module 06 — smb_scanner

```
Command: python3 -m main_scripts.smb_scanner -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/06_smb.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "smb_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:40:19.026618+05:30",
  "port": 445,
  "proto": "tcp",
  "status": "open",
  "data": {
    "smbv1_enabled": true,
    "smb2_supported": true,
    "signing_parsed": true,
    "signing_supported": true,
    "signing_required": false,
    "signing_enabled": true,
    "negotiated_dialect": "0x0311",
    "security_mode_raw": "0x0001",
    "ntlm_challenge": true,
    "negotiate_flags": "0xa28a8205",
    "target_name": "DESKTOP-34M18MB",
    "os_major": 10,
    "os_minor": 0,
    "os_build": 26100,
    "ntlm_revision": 15,
    "os_version": "10.0.26100",
    "method": "smb2_ntlm_version",
    "os_release": "Windows 11 24H2",
    "os_confidence": 0.97,
    "os_release_alt": "Windows Server 2025"
  },
  "evidence": "SMBv1=on, SMB2=on, signing_required=False, os=Windows 11 24H2 (build 26100, conf 0.97)"
}
```

**Key fields decoded:**

| Field | Value | Meaning |
|-------|-------|---------|
| `smbv1_enabled` | `true` | **FINDING** — SMBv1 negotiation succeeded |
| `smb2_supported` | `true` | SMB 3.1.1 also supported (dialect 0x0311) |
| `signing_required` | `false` | **FINDING** — relay attack path open |
| `signing_supported` | `true` | Capability exists but not enforced |
| `signing_enabled` | `true` | Enabled on client side, not enforced server-side |
| `security_mode_raw` | `0x0001` | Bit 0 set = signing enabled; bit 1 NOT set = signing not required |
| `negotiate_flags` | `0xa28a8205` | NTLMSSP negotiate capabilities bitmap |
| `ntlm_challenge` | `true` | NTLMv2 challenge present in NTLMSSP CHALLENGE_MESSAGE |
| `target_name` | `DESKTOP-34M18MB` | Workstation hostname from NTLMSSP |
| `os_build` | `26100` | Windows 11 24H2 (10.0.26100) |
| `ntlm_revision` | `15` | Current NTLM revision |
| `os_release_alt` | `Windows Server 2025` | Build 26100 shared between Win11 24H2 and WS2025 |

---

## Module 06b — smb_enum_scanner

```
Command: python3 -m main_scripts.smb_enum_scanner -t 192.168.1.65 -s /tmp/s.txt
Output : /tmp/scan_individual/06b_smb_enum.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "smb_enum_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:40:19.337128+05:30",
  "port": 445,
  "proto": "tcp",
  "status": "open",
  "data": {
    "smb": true,
    "null_session": false,
    "reason": "null_refused",
    "detail": "SMB SessionError: code: 0xc0000022 - STATUS_ACCESS_DENIED - {Access Denied} A process has requested access to an object but has not been granted those access rights."
  },
  "evidence": "null_session=False shares=0 users=0"
}
```

**Result:** Null session (anonymous/guest login without credentials) was rejected with `STATUS_ACCESS_DENIED (0xc0000022)`. Share and user enumeration returned 0 results. Windows 11 default: guest account and anonymous SMB access are disabled. Correct.

---

## Module 07 — service_banner

```
Command: python3 -m main_scripts.service_banner -t 192.168.1.65 -s /tmp/s.txt
         -p 22,135,139,445,902,912,2179,3389,5040,5985,47001,49664-49679
Output : /tmp/scan_individual/07_service_banner.jsonl
```

**Raw JSONL output — per port:**

### Port 22 — SSH
```json
{
  "port": 22, "proto": "tcp", "status": "open",
  "data": {
    "banner": "SSH-2.0-OpenSSH_for_Windows_9.5",
    "first_line": "SSH-2.0-OpenSSH_for_Windows_9.5",
    "byte_len": 33,
    "probe": "null",
    "service": "ssh",
    "product": "OpenSSH",
    "version": "for_Windows_9.5",
    "cpe": "cpe:2.3:a:openbsd:openssh:9.5:*:*:*:*:*:*:*",
    "cpe_vendor": "openbsd",
    "cpe_product": "openssh",
    "cpe_version": "9.5"
  },
  "evidence": "ssh: OpenSSH for_Windows_9.5"
}
```

### Port 135 — RPC Endpoint Mapper
```json
{"port": 135, "proto": "tcp", "status": "open",
 "data": {"tls_probed": true, "banner": null},
 "evidence": "open, no banner returned"}
```

### Port 139 — NetBIOS Session
```json
{"port": 139, "proto": "tcp", "status": "open",
 "data": {"tls_probed": true, "banner": "  ", "byte_len": 5, "probe": "http"},
 "evidence": "  "}
```

### Port 445 — SMB
```json
{"port": 445, "proto": "tcp", "status": "open",
 "data": {"tls_probed": true, "banner": null},
 "evidence": "open, no banner returned"}
```

### Port 902 — VMware Auth Daemon (SOAP/VNC)
```json
{
  "port": 902, "proto": "tcp", "status": "open",
  "data": {
    "banner": "220 VMware Authentication Daemon Version 1.10: SSL Required, ServerDaemonProtocol:SOAP, MKSDisplayProtocol:VNC , , NFCSSL supported/t,",
    "first_line": "220 VMware Authentication Daemon Version 1.10: SSL Required, ServerDaemonProtocol:SOAP, MKSDisplayProtocol:VNC , , NFCSSL supported/t,",
    "byte_len": 137,
    "probe": "null"
  },
  "evidence": "220 VMware Authentication Daemon Version 1.10: ..."
}
```

### Port 912 — VMware Auth Daemon (RFB/FTP-style auth)
```json
{
  "port": 912, "proto": "tcp", "status": "open",
  "data": {
    "banner": "220 VMware Authentication Daemon Version 1.0, ServerDaemonProtocol:SOAP, MKSDisplayProtocol:VNC , , , \r\n530 Please login with USER and PASS.\r\n530 Please login with USER and PASS.\r\n530 Please login with USER and PASS.\r\n530 Please login with USER and PASS.",
    "first_line": "220 VMware Authentication Daemon Version 1.0, ServerDaemonProtocol:SOAP, MKSDisplayProtocol:VNC , , , ",
    "byte_len": 256,
    "probe": "http"
  }
}
```

### Port 2179 — Hyper-V
```json
{"port": 2179, "proto": "tcp", "status": "open",
 "data": {"tls_probed": true, "banner": null},
 "evidence": "open, no banner returned"}
```

### Port 3389 — RDP
```json
{"port": 3389, "proto": "tcp", "status": "open",
 "data": {"tls_probed": true, "banner": null},
 "evidence": "open, no banner returned"}
```

### Port 5040 — Windows RPC dynamic
```json
{"port": 5040, "proto": "tcp", "status": "open",
 "data": {"tls_probed": true, "banner": null},
 "evidence": "open, no banner returned"}
```

### Port 5985 — WinRM (HTTP)
```json
{
  "port": 5985, "proto": "tcp", "status": "open",
  "data": {
    "banner": "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=us-ascii\r\nServer: Microsoft-HTTPAPI/2.0\r\nDate: Thu, 03 Sep 2026 19:10:31 GMT\r\nConnection: close\r\nContent-Length: 315\r\n\r\n<!DOCTYPE HTML PUBLIC ...>",
    "first_line": "HTTP/1.1 404 Not Found",
    "byte_len": 492,
    "probe": "http",
    "http_status": 404,
    "http_server": "Microsoft-HTTPAPI/2.0",
    "http_title": "Not Found",
    "service": "http",
    "product": "Microsoft-HTTPAPI",
    "version": "2.0",
    "cpe_unmapped": "Microsoft-HTTPAPI 2.0"
  },
  "evidence": "http: Microsoft-HTTPAPI 2.0"
}
```

### Port 47001 — WinRM (alternate)
```json
{
  "port": 47001, "proto": "tcp", "status": "open",
  "data": {
    "banner": "HTTP/1.1 404 Not Found\r\nServer: Microsoft-HTTPAPI/2.0\r\n...",
    "http_status": 404,
    "http_server": "Microsoft-HTTPAPI/2.0",
    "service": "http",
    "product": "Microsoft-HTTPAPI",
    "version": "2.0"
  },
  "evidence": "http: Microsoft-HTTPAPI 2.0"
}
```

### Ports 49664–49679 — Ephemeral RPC
```
All 7 ports (49664, 49665, 49666, 49667, 49668, 49677, 49678, 49679):
  tls_probed: true | banner: null | evidence: "open, no banner returned"
```

**Banner summary table:**

| Port | Identified Service | Version | CPE |
|------|--------------------|---------|-----|
| 22 | SSH | OpenSSH for_Windows_9.5 | `cpe:2.3:a:openbsd:openssh:9.5:*:*:*:*:*:*:*` |
| 902 | VMware Auth Daemon | 1.10 (SOAP/VNC) | — |
| 912 | VMware Auth Daemon | 1.0 (RFB/VNC) | — |
| 5985 | WinRM / Microsoft-HTTPAPI | 2.0 | — |
| 47001 | WinRM / Microsoft-HTTPAPI | 2.0 | — |
| 135,139,445,2179,3389,5040,49664+ | No banner (protocol-level) | — | — |

---

## Module 08 — tls_scanner

```
Command: python3 -m main_scripts.tls_scanner -t 192.168.1.65 -s /tmp/s.txt
         -p 3389,5985,47001,902
Output : /tmp/scan_individual/08_tls.jsonl
```

**Raw JSONL output:** *(empty — 0 records)*

**Result:** TLS scanner sent ClientHello to all four ports. No TLS ServerHello was returned from any of them:
- **3389 (RDP):** RDP protocol selects TLS after the X.224 negotiation layer; a raw TLS ClientHello at connection start is not handled.
- **5985/47001 (WinRM):** WinRM uses plain HTTP on port 5985 and 47001 (HTTPS would be on 5986); HTTP 404 was received, no TLS wrapping.
- **902 (VMware):** Banner says "SSL Required" but the daemon uses a proprietary handshake before TLS is established — raw TLS ClientHello is rejected.

**No TLS certificates, cipher suites, or TLS version data collected.** This is expected given the service mix.

---

## Module 08b — rdp_scanner

```
Command: python3 -m main_scripts.rdp_scanner -t 192.168.1.65 -s /tmp/s.txt -p 3389
Output : /tmp/scan_individual/08b_rdp.jsonl
```

**Raw JSONL output:**
```json
{
  "scanner": "rdp_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:41:07.775484+05:30",
  "port": 3389,
  "proto": "tcp",
  "status": "open",
  "data": {
    "rdp_confirmed": true,
    "negotiation": "failure",
    "failure_code": 2,
    "nla_required": false
  },
  "evidence": "RDP confirmed; security=?; NLA NOT required"
}
```

**Protocol trace:**
1. Scanner sent an RDP X.224 Connection Request TPDU with `requestedProtocols = PROTOCOL_SSL | PROTOCOL_HYBRID` (TLS + NLA).
2. Server returned X.224 Connection Confirm with `failure_code = 2` (PROTOCOL_NEG_FAILURE) — the server rejected both TLS and NLA proposals and fell back to classic RDP security.
3. `nla_required = false` — the server did NOT demand NLA; the connection would proceed to the Windows login screen without pre-authentication.

**Risk:** NLA-less RDP means the Windows graphical login screen is reachable with zero credentials. This is a brute-force and screen-based attack surface.

---

## Module 11 — ssh_scanner

```
Command: python3 -m main_scripts.ssh_scanner -t 192.168.1.65 -s /tmp/s.txt -p 22
Output : /tmp/scan_individual/11_ssh.jsonl
```

**Raw JSONL output (key fields):**
```json
{
  "scanner": "ssh_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:41:13.439950+05:30",
  "port": 22,
  "proto": "tcp",
  "status": "open",
  "data": {
    "ssh": true,
    "ssh_confirmed": true,
    "banner": {
      "protocol": "2.0",
      "software": "OpenSSH_for_Windows_9.5",
      "comments": null,
      "raw": "SSH-2.0-OpenSSH_for_Windows_9.5"
    },
    "protoversion": "2.0",
    "software": "OpenSSH_for_Windows_9.5",
    "kex_algorithms": [
      "curve25519-sha256",
      "curve25519-sha256@libssh.org",
      "ecdh-sha2-nistp256",
      "ecdh-sha2-nistp384",
      "ecdh-sha2-nistp521",
      "diffie-hellman-group-exchange-sha256",
      "diffie-hellman-group16-sha512",
      "diffie-hellman-group18-sha512",
      "diffie-hellman-group14-sha256",
      "kex-strict-s-v00@openssh.com"
    ],
    "server_host_key_algorithms": [
      "rsa-sha2-512",
      "rsa-sha2-256",
      "ecdsa-sha2-nistp256",
      "ssh-ed25519"
    ],
    "encryption": [
      "chacha20-poly1305@openssh.com",
      "aes128-ctr", "aes192-ctr", "aes256-ctr",
      "aes128-gcm@openssh.com", "aes256-gcm@openssh.com"
    ],
    "mac": [
      "umac-64-etm@openssh.com", "umac-128-etm@openssh.com",
      "hmac-sha2-256-etm@openssh.com", "hmac-sha2-512-etm@openssh.com",
      "umac-64@openssh.com", "umac-128@openssh.com",
      "hmac-sha2-256", "hmac-sha2-512"
    ],
    "failures": [
      {"category": "kex", "algorithm": "ecdh-sha2-nistp256",
       "reasons": ["using elliptic curves that are suspected as being backdoored by the U.S. National Security Agency"]},
      {"category": "kex", "algorithm": "ecdh-sha2-nistp384",
       "reasons": ["using elliptic curves that are suspected as being backdoored by the U.S. National Security Agency"]},
      {"category": "kex", "algorithm": "ecdh-sha2-nistp521",
       "reasons": ["using elliptic curves that are suspected as being backdoored by the U.S. National Security Agency"]},
      {"category": "key", "algorithm": "ecdsa-sha2-nistp256",
       "reasons": ["using elliptic curves that are suspected as being backdoored by the U.S. National Security Agency"]}
    ],
    "warnings": [
      {"category": "kex", "algorithm": "curve25519-sha256",
       "reasons": ["does not provide protection against post-quantum attacks"]},
      {"category": "kex", "algorithm": "curve25519-sha256@libssh.org",
       "reasons": ["does not provide protection against post-quantum attacks"]}
    ]
  }
}
```

**Algorithm audit:**

| Type | Algorithm | Verdict |
|------|-----------|---------|
| KEX | curve25519-sha256 | OK (warning: no PQ protection) |
| KEX | curve25519-sha256@libssh.org | OK (warning: no PQ protection) |
| KEX | **ecdh-sha2-nistp256** | **FAIL — NSA-suspected NIST P-256** |
| KEX | **ecdh-sha2-nistp384** | **FAIL — NSA-suspected NIST P-384** |
| KEX | **ecdh-sha2-nistp521** | **FAIL — NSA-suspected NIST P-521** |
| KEX | diffie-hellman-group-exchange-sha256 | OK |
| KEX | diffie-hellman-group16-sha512 | OK |
| KEX | diffie-hellman-group18-sha512 | OK |
| KEX | diffie-hellman-group14-sha256 | OK |
| KEX | kex-strict-s-v00@openssh.com | OK (Terrapin mitigation) |
| Host key | rsa-sha2-512 | OK |
| Host key | rsa-sha2-256 | OK |
| Host key | **ecdsa-sha2-nistp256** | **FAIL — NSA-suspected NIST P-256** |
| Host key | ssh-ed25519 | OK |
| Cipher | chacha20-poly1305, aes*-gcm, aes*-ctr | All OK |
| MAC | All hmac-sha2-*-etm, umac-*-etm | All OK (ETM is secure ordering) |

---

## Module 19 — msrpc_scanner

```
Command: python3 -m main_scripts.msrpc_scanner -t 192.168.1.65 -s /tmp/s.txt -p 135
Output : /tmp/scan_individual/19_msrpc.jsonl
```

**Raw JSONL output (summary):**
```json
{
  "scanner": "msrpc_scan",
  "target": "192.168.1.65",
  "timestamp": "2026-09-04T00:41:13.XXX+05:30",
  "port": 135,
  "proto": "tcp",
  "status": "open",
  "data": {
    "msrpc": true,
    "endpoint_count": 409,
    "interface_count": 156,
    "named_services": [
      "BFE.DLL", "FwRemoteSvr.dll", "IKEEXT.DLL", "MPSSVC.dll",
      "SCardSvr.dll", "appinfo.dll", "bdesvc.dll", "bthserv.dll",
      "certprop.dll", "dhcpcsvc.dll", "dhcpcsvc6.dll", "gpsvc.dll",
      "iphlpsvc.dll", "nrpsrv.dll", "nsisvc.dll", "pcasvc.dll",
      "samsrv.dll", "schedsvc.dll", "services.exe", "spoolsv.exe",
      "srvsvc.dll", "ssdpsrv.dll", "sysmain.dll", "sysntfy.dll",
      "taskcomp.dll", "wevtsvc.dll", "wininit.exe", "winlogon.exe",
      "wlanext.exe", "wlanmsm.dll", "wlansvc.dll", "wscsvc.dll"
    ],
    "endpoints": [
      {
        "uuid": "51A227AE-825B-41F2-B4A9-1AC9557A1018 v1.0",
        "binding": "ncacn_ip_tcp:192.168.1.65[49664]",
        "annotation": "Ngc Pop Key Service"
      },
      "... (409 total endpoints) ..."
    ]
  }
}
```

**Note:** This run discovered **409 endpoints / 156 interfaces** (previous run: 407/155) — slight variation is normal as Windows dynamically registers/deregisters RPC services.

**High-value attack surfaces in EPM disclosure:**

| Service DLL | Risk |
|-------------|------|
| `samsrv.dll` | SAM RPC — Security Account Manager. Direct account enumeration path if accessible. |
| `spoolsv.exe` | Print Spooler — **PrinterBug/SpoolSample**: coerces NTLM auth from this host to attacker-controlled listener. |
| `schedsvc.dll` | Task Scheduler — remote task creation/deletion via RPC (ATT&CK T1053.005). |
| `wlansvc.dll` | WLAN AutoConfig — wireless profile manipulation via RPC. |
| `ssdpsrv.dll` | SSDP — UPnP device discovery service. |
| `winlogon.exe` | Login session RPC — credential provider interface. |
| `services.exe` | SCM (Service Control Manager) — remote service creation (ATT&CK T1543.003). |
| `BFE.DLL` | Base Filtering Engine (Windows Firewall) — firewall rule management via RPC. |

**Sample endpoint bindings (first 5 unique UUIDs):**
```
51A227AE-825B-41F2-B4A9-1AC9557A1018  Ngc Pop Key Service      ncacn_ip_tcp:192.168.1.65[49664]
8FB74744-B2FF-4C00-BE0D-9EF9A191FE1B  Ngc Pop Key Service      ncacn_ip_tcp:192.168.1.65[49664]
B25A52BF-E5DD-4F4A-AEA6-8CA7272A0E86  KeyIso                   ncacn_ip_tcp:192.168.1.65[49664]
51083702-9600-4EDE-967F-FCE28AE28BCF  KeyIso                   ncacn_ip_tcp:192.168.1.65[49664]
6BFFD098-A112-3610-9833-46C3F87E345A  wkssvc                   ncacn_ip_tcp:192.168.1.65[49664]
```

Full 409-endpoint dump: `/tmp/scan_individual/19_msrpc.jsonl`

---

## Consolidated Findings

| # | Severity | Rule ID | Port | Verified | Title |
|---|----------|---------|------|----------|-------|
| 1 | **HIGH** | SMB-V1-ENABLED | 445/tcp | YES | SMBv1 protocol enabled |
| 2 | **HIGH** | CORR-NTLM-RELAY-PATH | 445/tcp | CORR | NTLM relay attack path (no signing + SMBv1) |
| 3 | **HIGH** | SSH-WEAK-ALGO | 22/tcp | YES | Weak SSH algorithms — NIST P-curves |
| 4 | **HIGH** | CORR-LEGACY-WINDOWS-SURFACE | host | CORR | SMBv1 + exposed RDP = ransomware entry path |
| 5 | MEDIUM | SVC-RDP-EXPOSED | 3389/tcp | YES | RDP open, NLA not required |
| 6 | MEDIUM | SMB-SIGNING-NOT-REQUIRED | 445/tcp | YES | SMB signing not enforced |
| 7 | LOW | MSRPC-ENDPOINTS-EXPOSED | 135/tcp | YES | 409 RPC endpoints / 156 interfaces leaked |
| 8 | INFO | ASSET-OS-IDENTIFIED | host | YES | Windows 11 24H2 (build 26100, conf 0.97) |

---

## Remediation — Priority Order

```
P1 (5 min) — Disable SMBv1
  Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force

P1 (5 min) — Require SMB signing
  Set-SmbServerConfiguration -RequireSecuritySignature $true -Force

P2 (30 min) — RDP: enable NLA + firewall to management VLAN only
  gpedit.msc → Remote Desktop Session Host → Security → Require NLA
  New-NetFirewallRule -LocalPort 3389 -RemoteAddress <mgmt_range> -Action Allow

P3 (15 min) — Remove weak SSH algorithms from sshd_config
  KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256,...
  HostKeyAlgorithms rsa-sha2-512,rsa-sha2-256,ssh-ed25519
  Restart-Service sshd

P4 (20 min) — Firewall port 135 and dynamic RPC range from untrusted networks
  Restrict TCP/135 + 49152-65535 to management VLANs only
```

---

## Output Files Reference

| Module | JSONL File | Records |
|--------|-----------|---------|
| host_discovery | `/tmp/scan_individual/01_host_discovery.jsonl` | 1 |
| port_scanner | `/tmp/scan_individual/02_port_scan.jsonl` | ~1121 |
| udp_scanner | `/tmp/scan_individual/03_udp.jsonl` | 12 |
| os_fingerprint | `/tmp/scan_individual/04_os_fingerprint.jsonl` | 1 |
| snmp_scanner | `/tmp/scan_individual/05_snmp.jsonl` | 1 |
| ipmi_scanner | `/tmp/scan_individual/05b_ipmi.jsonl` | 1 |
| smb_scanner | `/tmp/scan_individual/06_smb.jsonl` | 1 |
| smb_enum_scanner | `/tmp/scan_individual/06b_smb_enum.jsonl` | 1 |
| service_banner | `/tmp/scan_individual/07_service_banner.jsonl` | 19 |
| tls_scanner | `/tmp/scan_individual/08_tls.jsonl` | 0 (no TLS on probed ports) |
| rdp_scanner | `/tmp/scan_individual/08b_rdp.jsonl` | 1 |
| ssh_scanner | `/tmp/scan_individual/11_ssh.jsonl` | 1 |
| msrpc_scanner | `/tmp/scan_individual/19_msrpc.jsonl` | 1 (409 endpoints inside) |

---

*Each module run individually with `PYTHONPATH=probe/ .venv/bin/python3 -m main_scripts.<module>` — authorised internal LAN scan only.*
*No exploitation. No brute-force. No credentials used. All findings from protocol-level negotiation and banner evidence.*
