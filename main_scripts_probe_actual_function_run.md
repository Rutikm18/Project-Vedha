# main_scripts — Actual-Function Run & Verification Runbook

Run every real scanner in `probe/main_scripts/` **one at a time**, see the raw
findings, and verify each against the target machine (attacker-side cross-check
with `nmap`/`openssl`, and target-side ground truth).

Validated 2026-08-17 on `192.168.1.0/24` against `192.168.1.254` (a GPON router:
`22/ssh dropbear`, `80/http thttpd`, `443/https TLS1.3`). Substitute your own
`CIDR` + `TARGET` below.

---

## 0. One-time setup (run first, every session)

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe"
PY=.venv/bin/python3                       # the project venv Python
CIDR="192.168.1.0/24"                       # authorization scope (allowlist)
T="192.168.1.254"                           # the target you are verifying
echo "$CIDR" > /tmp/s.txt                    # -s scope file = allowlist; target must be inside it
```

- `-t` = target(s); `-s /tmp/s.txt` = authorization allowlist (target must be within it).
- Alternative to the scope file: append `--allow-targets` (scope = exactly `-t`), handy for your own lab.
- Every scanner prints **JSONL to stdout**. Add `-o /tmp/out.jsonl` to any command to save it.
- See any scanner's exact flags: `$PY -m main_scripts.<name> --help`.

### Pretty-printer (optional) — pipe any scanner through this to read findings
```bash
JR='import sys,json
for l in sys.stdin:
 l=l.strip()
 if not l: continue
 try: j=json.loads(l)
 except: continue
 d=j.get("data") or {}
 print(j.get("scanner"), j.get("target"), j.get("port",""), j.get("status",""),
       {k:v for k,v in {**d, **{x:j.get(x) for x in ("service","product","version","evidence")}}.items()
        if v not in (None,"",[],{})})'
# usage:  $PY -m main_scripts.port_scanner -t $T -s /tmp/s.txt | $PY -c "$JR"
```

### Ground-truth tools (attacker-side) used to verify below
```bash
nmap -Pn -sV -F "$T"                          # open ports + service/version (top 100)
nmap -Pn -sV -p- --min-rate 1000 "$T"         # full 65535-port version scan (slower)
echo | openssl s_client -connect "$T:443"     # real TLS cert/version/cipher
curl -sI "http://$T/" ; curl -skI "https://$T/"   # HTTP headers
```

### Ground-truth (target-side) — run these **on the target machine**
```bash
# Linux target
ss -tlnp ; ss -ulnp          # listening TCP / UDP ports (authoritative)
uname -a                     # OS/kernel
# macOS target
lsof -nP -iTCP -sTCP:LISTEN ; lsof -nP -iUDP
# Windows target
netstat -ano | findstr LISTENING ; systeminfo
```

---

## A. Core recon — run in THIS order (each feeds the next)

### 1. host_discovery — is it alive? MAC / vendor / device class
```bash
$PY -m main_scripts.host_discovery -t $CIDR -s /tmp/s.txt          # sweep the whole subnet
$PY -m main_scripts.host_discovery -t $T   -s /tmp/s.txt           # just the target
# privileged extras (macOS/Linux, needs sudo): add --syn ; disable ICMP with --no-icmp
```
- **Should find:** `state=confirmed_alive` (+ `confidence`, `mac`, `vendor`, `device_hint`) for live hosts; `unreachable_from_vantage` for dead ones.
- **Verify (attacker):** `nmap -sn $CIDR` → compare the live-host list.
- **Verify (target):** the host is powered on and on the LAN; `arp -an | grep <ip>` shows its MAC.

### 2. port_scanner — open TCP ports (unprivileged connect scan)
```bash
$PY -m main_scripts.port_scanner -t $T -s /tmp/s.txt -p 1-1024
$PY -m main_scripts.port_scanner -t $T -s /tmp/s.txt               # default top-ports set
```
- **Should find:** each open port as `{port, status:"open", confidence}`.
- **Verify (attacker):** `nmap -Pn -p 1-1024 $T`.
- **Verify (target):** `ss -tlnp` (Linux) / `lsof -nP -iTCP -sTCP:LISTEN` (mac) — the LISTEN ports must match.

### 3. os_fingerprint — OS family guess
```bash
$PY -m main_scripts.os_fingerprint -t $T -s /tmp/s.txt
```
- **Should find:** `os_guess` (e.g. `Linux/Unix/macOS`) + `confidence`.
- **Verify (attacker):** `sudo nmap -O $T` (needs root for OS detection).
- **Verify (target):** `uname -a` / `systeminfo`.

### 4. service_banner — service + version string per port  (**-p REQUIRED**)
```bash
$PY -m main_scripts.service_banner -t $T -s /tmp/s.txt -p 22,80,443,445,3389,8080
```
- **Should find:** `service / product / version / banner` (e.g. `ssh / dropbear / 2017.75`; `Server: thttpd`).
- **Verify (attacker):** `nmap -Pn -sV -p 22,80,443 $T`.
- **Verify (target):** `ssh -V`, web server version, etc.

### 5. service_enum — deep service / role / OS enrichment
```bash
$PY -m main_scripts.service_enum -t $T -s /tmp/s.txt -p 22,80,443
$PY -m main_scripts.service_enum -t $T -s /tmp/s.txt --topology     # also prints subnets + gateway
```
- **Should find:** `services` map (per-port service, tls_version, cert_present), `roles` (web/db/...), `hostnames.reverse_dns`, `os_guess`.
- **Known weakness:** `os_guess` can be `None` on some hosts (unprivileged heuristic). Cross-check with step 3.
- **Verify (attacker):** `nmap -Pn -sV $T` + `dig -x $T` (reverse DNS).

---

## B. TLS & Web

### 6. tls_scanner — TLS versions, ciphers, cert, posture grade  (auto-targets 443/8443/…)
```bash
$PY -m main_scripts.tls_scanner -t $T -s /tmp/s.txt
```
- **Should find:** `evidence: "grade A; accepts: TLSv1_3, TLSv1_2"`; `data.{accepted_versions, cipher_by_version, cipher_analysis, posture, certificate}`.
- **Verify (attacker):** `echo | openssl s_client -connect $T:443` → compare protocol/cipher/subject/issuer.

### 7. tls_fingerprint — JARM active TLS-stack fingerprint
```bash
$PY -m main_scripts.tls_fingerprint -t $T -s /tmp/s.txt
```
- **Should find:** a `jarm` hash for the TLS service.
- **Verify:** stable across runs for the same server; differs across different TLS stacks.

### 8. web_scanner — HTTP headers / title / methods
```bash
$PY -m main_scripts.web_scanner -t $T -s /tmp/s.txt --timeout 6
```
- **Should find:** `title` (e.g. `GPON Home Gateway`), server header, status, allowed methods — for 80 and 443.
- **Verify (attacker):** `curl -sI http://$T/` and `curl -skI https://$T/`.

---

## C. Service-specific — only find something if the target runs that service

### 9. udp_scanner — UDP services + amplification exposure
```bash
$PY -m main_scripts.udp_scanner -t $T -s /tmp/s.txt
```
- Needs open UDP (53/123/161/1900/…). Verify: `nmap -Pn -sU --top-ports 50 $T` (root) / `ss -ulnp` on target.

### 10. smb_scanner — SMB dialect / signing  (needs **445**)
```bash
$PY -m main_scripts.smb_scanner -t $T -s /tmp/s.txt
```
- Verify: `nmap -p445 --script smb-protocols,smb-security-mode $T`; on a Windows target `Get-SmbServerConfiguration`.

### 11. snmp_scanner — SNMP communities/exposure  (needs **161/udp**)
```bash
$PY -m main_scripts.snmp_scanner -t $T -s /tmp/s.txt
```
- Verify: `snmpwalk -v2c -c public $T system` (if community known).

### 12. db_scanner — database fingerprint  (needs DB ports 3306/5432/1433/6379/27017/…)
```bash
$PY -m main_scripts.db_scanner -t $T -s /tmp/s.txt
```
- Verify: `nmap -sV -p 3306,5432,1433,6379,27017 $T`.

### 13. rdp_scanner — RDP exposure  (needs **3389**)
```bash
$PY -m main_scripts.rdp_scanner -t $T -s /tmp/s.txt
```
- Verify: `nmap -p3389 --script rdp-ntlm-info $T`.

### 14. iot_scanner — SSDP / RTSP / MQTT / CoAP discovery
```bash
$PY -m main_scripts.iot_scanner -t $T -s /tmp/s.txt
```
- Verify: `nmap -sU -p1900 --script upnp-info $T`; cameras answer RTSP on 554.

### 15. mobile_scanner — mobile-device exposure signals
```bash
$PY -m main_scripts.mobile_scanner -t $T -s /tmp/s.txt
```
- Verify: point at a phone; iPhone lockdownd = 62078, randomized MAC = privacy device.

### 16. mcp_ai_scanner — exposed AI / MCP endpoints
```bash
$PY -m main_scripts.mcp_ai_scanner -t $T -s /tmp/s.txt
```
- Verify: target must run an MCP/AI server (e.g. Ollama :11434, MCP HTTP).

### 17. ja4s / ja4x — JA4 TLS-server / certificate fingerprints
```bash
$PY -m main_scripts.ja4s -t $T -s /tmp/s.txt          # server-hello fingerprint
$PY -m main_scripts.ja4x -t $T -s /tmp/s.txt          # X.509 cert fingerprint
```

### 18. unauth_access — unauthenticated-access checks
```bash
$PY -m main_scripts.unauth_access -t $T -s /tmp/s.txt
```

---

## D. Privileged / heavier scanners

### 19. syn_scanner — raw SYN scan  (**root**; macOS falls back to connect)
```bash
sudo $PY -m main_scripts.syn_scanner -t $T -s /tmp/s.txt -p 1-1000
sudo $PY -m main_scripts.syn_scanner -t $T -s /tmp/s.txt -p 1-1000 --force-fallback   # macOS (no raw sockets)
```
- Verify vs `sudo nmap -sS -p 1-1000 $T`.

### 20. mass_scan — masscan wrapper (root) or pure-Python fallback
```bash
$PY -m main_scripts.mass_scan -t $T -s /tmp/s.txt -p 1-1000 --fallback
```

### 21. nmap_wrapper — drives real nmap (needs `nmap`; os/syn profiles need root)
```bash
$PY -m main_scripts.nmap_wrapper -t $T -s /tmp/s.txt --profile version
```

---

## E. Credentialed collectors (need creds on the target)

### 22. ssh_collector — authenticated Linux facts (needs SSH key/user)
```bash
$PY -m main_scripts.ssh_collector -t $T -s /tmp/s.txt --user U --key ~/.ssh/id_rsa
```

### 23. windows_collector — authenticated Windows facts (needs creds)
```bash
WIN_SCAN_PASSWORD='***' $PY -m main_scripts.windows_collector -t $T -s /tmp/s.txt --user U
```

---

## F. Passive & diff

### 24. passive_collector — listen only (OT-safe), no active probes
```bash
$PY -m main_scripts.passive_collector -t $T -s /tmp/s.txt --listen-seconds 60
```

### 25. delta_scanner — diff two prior JSONL runs (change detection)
```bash
$PY -m main_scripts.host_discovery -t $CIDR -s /tmp/s.txt -o /tmp/baseline.jsonl
# ... later ...
$PY -m main_scripts.host_discovery -t $CIDR -s /tmp/s.txt -o /tmp/current.jsonl
$PY -m main_scripts.delta_scanner /tmp/baseline.jsonl /tmp/current.jsonl
```

---

## G. Orchestrators (chain everything)

### 26. scan_funnel — per-host funnel (discovery → ports → services → …)
```bash
$PY -m main_scripts.scan_funnel -t $T -s /tmp/s.txt
```

### 27. run_all — run the full scanner set (see `--help` for selection flags)
```bash
$PY -m main_scripts.run_all -t $T -s /tmp/s.txt
$PY -m main_scripts.run_all --help
```

---

## H. Verification cross-check matrix

| Scanner | Compare against (attacker) | Ground truth on target |
|---|---|---|
| host_discovery | `nmap -sn $CIDR` | host powered on; `arp -an` |
| port_scanner / syn_scanner / mass_scan | `nmap -Pn -p… $T` | `ss -tlnp` / `lsof -iTCP -sTCP:LISTEN` |
| os_fingerprint | `sudo nmap -O $T` | `uname -a` / `systeminfo` |
| service_banner / service_enum | `nmap -Pn -sV $T` | service version on host |
| tls_scanner / tls_fingerprint / ja4s / ja4x | `openssl s_client -connect $T:443` | cert on host |
| web_scanner | `curl -skI https://$T/` | web server config |
| udp_scanner | `sudo nmap -sU $T` | `ss -ulnp` |
| smb_scanner | `nmap -p445 --script smb-* $T` | `Get-SmbServerConfiguration` |
| snmp_scanner | `snmpwalk -v2c -c public $T` | snmpd.conf |
| db_scanner | `nmap -sV -p 3306,5432,1433,6379 $T` | DB listener |

---

## Notes / gotchas

- **Run from `probe/`** so `main_scripts` is importable (`python -m main_scripts.X`).
- **Use the venv Python** (`.venv/bin/python3`) — the scanners need its dependencies.
- **TLS output** lives in `data.accepted_versions / cipher_analysis / posture / certificate` (not a flat `tls_version`).
- **Unprivileged limits:** without `sudo`, ICMP/SYN/OS-TTL paths are skipped; `os_guess` may be blank in `service_enum` — cross-check with `os_fingerprint`.
- **A scanner returning nothing** on a host that lacks that service is correct, not a bug — validate service-specific scanners against a host that actually runs the service.
- **Save + re-read:** add `-o /tmp/out.jsonl`, then `$PY -c "$JR" < /tmp/out.jsonl`.
