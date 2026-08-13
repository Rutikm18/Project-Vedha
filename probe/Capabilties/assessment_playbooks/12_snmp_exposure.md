# 12 — SNMP Exposure Check (Core-Level Playbook)

> **Goal:** Find and assess exposed SNMP (Simple Network Management Protocol) services. SNMP is a
> deceptively deep information-disclosure and control surface: with a guessable community string it
> hands over device internals — interfaces, routes, ARP tables, running processes, users,
> sometimes passwords — and, with write access, lets you *reconfigure* the device. It is also a
> potent DDoS amplifier.

---

## 1. Core theory: SNMP is a queryable database over UDP

SNMP exposes a device's management data as a tree — the **MIB (Management Information Base)** —
addressed by **OIDs (Object Identifiers)**, e.g. `1.3.6.1.2.1.1.1.0` = `sysDescr` (device
description string). You **GET** a single OID, **GETNEXT/GETBULK** to walk the tree, and **SET** to
change a writable OID. Transport: **UDP 161** (agent), **UDP 162** (traps).

### 1.1 The version/auth reality (this is the whole vulnerability)
| Version | Auth model | Security reality |
|---------|-----------|------------------|
| **SNMPv1** | "community string" in **cleartext** | A shared password sent in plaintext; trivial to sniff/guess |
| **SNMPv2c** | same cleartext community | Adds GETBULK (faster walks) but *no* security improvement |
| **SNMPv3** | User-based Security Model: auth (MD5/SHA) + priv (DES/AES) | The only secure version; often misconfigured to noAuthNoPriv |

**The core issue:** v1/v2c authenticate with a **community string**, and the defaults are
universally known:
- `public` — default **read** community.
- `private` — default **read-write** community.
- Vendor defaults (`cisco`, `admin`, etc.).

If `public` works, you get **read** access to everything in the device's MIB. If `private` (or a
guessable RW community) works, you get **write** access → reconfigure/brick the device, exfiltrate
configs (e.g., Cisco `RTR` MIB config download), or pivot.

### 1.2 Why the data disclosure is so severe
A read-only SNMP walk typically reveals: hostname, OS/firmware (`sysDescr`), uptime, **full
interface list + IPs** (`ifTable`, `ipAddrTable`), **routing table**, **ARP/neighbor table**
(`ipNetToMedia` → map the whole network!), **TCP/UDP connection tables** (`tcpConnTable` → open
services), installed software, running processes (`hrSWRunTable`), and on some devices **local user
accounts and even password hashes** (host-resources / vendor MIBs). This single protocol can hand
an attacker a network map that would otherwise take extensive scanning.

---

## 2. Approach from a single system (methodology + commands)

**Step 1 — find SNMP (UDP, so use payload-driven scan; see `11`):**
```bash
nmap -sU -p161 -sV --script "snmp-info" -iL live.txt -oX snmp.xml
```

**Step 2 — community-string discovery (in scope, rate-limited):**
```bash
onesixtyone -c community-wordlist.txt -i hosts.txt      # fast community brute
nmap -sU -p161 --script snmp-brute <host>
```
Start with `public`/`private`/vendor defaults before any wordlist.

**Step 3 — enumerate (read):**
```bash
snmpwalk -v2c -c public <host>                 # full walk (or -v1)
snmpwalk -v2c -c public <host> 1.3.6.1.2.1.1   # system group
snmp-check <host> -c public                    # pretty summary: users, processes, net
# Targeted high-value OIDs:
snmpwalk -v2c -c public <host> 1.3.6.1.2.1.4.22   # ARP table (ipNetToMedia) = network map
snmpwalk -v2c -c public <host> 1.3.6.1.2.1.25.4.2 # running processes (hrSWRun)
snmpwalk -v2c -c public <host> 1.3.6.1.2.1.25.6.3 # installed software
```
Nmap NSE equivalents: `snmp-sysdescr`, `snmp-interfaces`, `snmp-netstat`, `snmp-processes`,
`snmp-win32-users`, `snmp-win32-software`, `snmp-ios-config` (Cisco config grab).

**Step 4 — test for write access (carefully, in scope only):**
- Confirm a RW community exists via a **read via the RW string** first; only attempt a benign,
  reversible SET (e.g., `sysContact`) with explicit authorization — a wrong SET can reconfigure or
  brick network gear.

**Step 5 — amplification check:** SNMP GETBULK responses can be far larger than requests → the host
is a reflector. Measure the factor with one request; don't weaponize.

---

## 3. Vulnerability logic

- **Default/guessable community (`public`/`private`)** → info disclosure (read) or device control
  (write). This is the headline finding.
- **Cleartext v1/v2c on the network** → community strings sniffable → credential capture.
- **Network reconnaissance goldmine** → ARP/route/interface tables reveal the entire topology,
  bypassing the need to scan.
- **Config/credential extraction** → Cisco running-config via SNMP, Windows users/software,
  process lists, sometimes hashes.
- **Write access** → reconfigure ACLs/routes, TFTP-exfil configs, DoS.
- **Amplification participant** → DDoS reflector.
- **SNMPv3 misconfig** → noAuthNoPriv or weak auth = v3 with none of the benefit.

---

## 4. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| UDP scan misses SNMP | open|filtered ambiguity (`11`) | Use `-sU -sV` + `snmp-info`; corroborate with `onesixtyone`/`snmpwalk` directly |
| Community not `public` | Custom string | `onesixtyone` with a curated wordlist; try vendor defaults; consider sniffing v1/v2c traffic |
| Brute triggers lockout/alerts | Aggressive guessing | Small default-first list, rate-limited; SNMP rarely locks out but IDS may alert |
| Walk is huge/slow | Big MIB over UDP | Use GETBULK (`-v2c`), target specific OID subtrees, not full walk |
| Write test risk | SET can brick/reconfigure device | Confirm RW via read first; only benign reversible SET with sign-off; often just *report* RW exposure |
| SNMPv3 present | Auth/priv required | Test for noAuthNoPriv; enumerate users (`snmp-v3-enum`); don't brute strong auth |
| Amplification test = DDoS | Repeated GETBULK to spoofed victim | One measurement request; never spoof source |
| Fragile network gear | Old routers/switches/printers | Gentle; treat like IoT/OT; avoid write ops on production |
| False positives (honeypot) | Deceptive SNMP agent | Check data consistency (interface counts, uptime plausibility) |

---

## 5. Considerations & guardrails

- **Read is low-risk; write is dangerous.** A SET on production network gear can drop routes,
  change ACLs, or brick a device. Prefer to *report* RW exposure rather than exercise it.
- **Community strings are credentials** — handle captured ones as secrets.
- **v1/v2c is cleartext** — recommend v3 with authPriv as the fix.
- **Amplification measurement** must be a single, non-spoofed request.

---

## 6. References

- RFC 1157 (SNMPv1), RFC 1901/1905 (SNMPv2c), RFC 3411-3418 (SNMPv3 architecture/USM/VACM),
  RFC 1213 (MIB-II), RFC 2790 / host-resources MIB.
- CISA/US-CERT guidance on SNMP default community strings and amplification (TA14-017A).
- Nmap NSE `snmp-*` scripts; tools: `snmpwalk`/`snmpbulkwalk` (net-snmp), `onesixtyone`,
  `snmp-check`, `snmp-brute`.
- UDP scanning context: `11_udp_service_exposure.md`; Nmap UDP internals `../fresh_implement.md §5.8`.
