# Vedha Network VA — Prompt Output Documentation

---

## Prompt 1: Network VA Use Cases — Confirmed Accurate vs Still Needed

**Q:** List down the network use cases that confirm we are doing accurately, and network VA related use cases still we need to add (all for on-prem, not cloud related).

---

### Confirmed & Accurate (On-Prem Network VA)

**Scanner-level (rig-validated ground truth against 192.168.1.77):**

1. TCP port discovery — open / filtered / firewall-blocked distinction
2. UDP port discovery — generic probe + real reply payload decode
3. Service banner capture — raw banner, no fabrication; reports "no banner" honestly
4. Printer service detection — real PJL handshake, not port assumption
5. OS fingerprinting — TTL + SMB2 signals
6. Host liveness discovery — host_discovery (ARP/ICMP)
7. SYN scan / mass scan — wide sweep, open ports correctly populate deep-scan routing

**Posture/config rules (detection engine, confirmed working):**

8. SMBv1 enabled (wormable)
9. SMB signing off (NTLM relay exposure)
10. RDP without NLA
11. RDP exposed/reachable
12. TLS deprecated version (SSL2/3, TLS1.0/1.1)
13. TLS weak cipher suite
14. TLS self-signed cert
15. TLS expired cert
16. MSRPC epmap anonymously enumerable
17. UDP amplification service exposed
18. SNMP default community string

**Exposed-service / suspicious-port detection (from open ports + banners):**

19. Backdoor/C2 ports (4444, 31337, 12345, 6667, 5555, 2323, etc.)
20. Container API exposed (Docker 2375, K8s 6443, kubelet 10250, etcd 2379)
21. Unauthenticated datastore exposed (Redis 6379, MongoDB 27017, ES 9200, Memcached 11211)
22. Database port directly exposed (MySQL 3306, Postgres 5432, MSSQL 1433, Oracle 1521)
23. Cleartext protocol in use (Telnet 23, FTP 21, r-services 512-514)
24. Remote access service exposed (VNC 5900, WinRM 5985, X11 6000)
25. Admin UI exposed (8080, 8888, 3000, 15672, 9100, etc.)
26. Internet-facing severity escalation (BOD-26-04 model)

---

### Still Needed (On-Prem Network VA, Not Yet Accurate)

**Experimental scanners — wired but unvalidated (need rig testing):**

1. SSH scanner — banner grab works, but version parsing / algo negotiation not validated
2. SMB enumeration — shares/users enumeration not validated
3. LDAP scanner — anonymous bind / null base DN not validated
4. DNS scanner — recursion open / zone transfer not validated
5. NFS scanner — exports enumerable not validated
6. FTP scanner — anonymous login / writeable directory not validated
7. Rsync scanner — unauthenticated module list not validated
8. VNC scanner — no-auth / weak-auth not validated
9. SNMP scanner — community string enumeration accuracy not validated
10. IPMI scanner — default credentials / cipher-0 not validated
11. SMTP scanner — open relay / auth bypass not validated
12. DB scanners (db_scan) — actual query/auth checks not validated
13. Web scanner (web_scan) — HTTP headers / misconfig not validated

**Detection rules still missing:**

14. SSH weak key exchange / deprecated algorithms (needs validated ssh_scan)
15. NFS world-readable export
16. FTP anonymous write
17. DNS open resolver / zone transfer allowed
18. LDAP anonymous bind leaking directory data
19. IPMI cipher-0 / default credentials
20. Kerberoastable SPN exposure (needs domain context)
21. IPv6 host discovery — scanners currently IPv4-only; IPv6-only hosts invisible

**Structural gaps:**

22. Banner → product/version parsing (~32 pattern gap in service_banner)
23. IPv6 scope: connect scanners are dual-stack but nothing discovers IPv6 addresses

---

## Prompt 2: Commands to Run All Scanners Manually

**Q:** Give me commands to run accurate scripts and other scripts as well — mention accurate and need-improvement scripts — give me all that we added.

---

### Setup (run once per terminal)

```bash
cd /Users/rutikmangale/Documents/DRIVE\ T\ -Var/Security-projects/Vedha/probe/main_scripts
export TARGET=192.168.1.77       # change to your test host
export SCOPE=192.168.1.0/24      # must include target
```

---

### VERIFIED (Accurate) Scanners

#### 1. Host Discovery
```bash
python3 host_discovery.py -t $TARGET -s $SCOPE
```

#### 2. TCP Port Scan (connect scan)
```bash
python3 port_scanner.py -t $TARGET -s $SCOPE -p 1-1024
python3 port_scanner.py -t $TARGET -s $SCOPE -A           # all 65535 ports
```

#### 3. SYN Scan (needs sudo)
```bash
sudo python3 syn_scanner.py -t $TARGET -s $SCOPE -p 1-1024
```

#### 4. Mass Scan (needs sudo)
```bash
sudo python3 mass_scan.py -t $TARGET -s $SCOPE
```

#### 5. OS Fingerprint
```bash
python3 os_fingerprint.py -t $TARGET -s $SCOPE
```

#### 6. SMB Posture
```bash
python3 smb_scanner.py -t $TARGET -s $SCOPE --port 445
```

#### 7. RDP Posture
```bash
python3 rdp_scanner.py -t $TARGET -s $SCOPE -p 3389
```

#### 8. TLS Posture
```bash
python3 tls_scanner.py -t $TARGET -s $SCOPE -p 443,8443
```

#### 9. MSRPC Endpoint Map
```bash
python3 msrpc_scanner.py -t $TARGET -s $SCOPE -p 135
```

#### 10. UDP Services
```bash
python3 udp_scanner.py -t $TARGET -s $SCOPE -p 53,67,123,161,500,1900
```

#### 11. Service Banners (run after port scan so you know open ports)
```bash
python3 service_banner.py -t $TARGET -s $SCOPE -p 22,80,443,8080,3306
```

#### 12. Printer Scanner
```bash
python3 printer_scanner.py -t $TARGET -s $SCOPE -p 9100,631
```

---

### EXPERIMENTAL (Run but results need validation)

> Output may be inaccurate — treat as leads, not confirmed findings.

#### 13. SSH Posture
```bash
python3 ssh_scanner.py -t $TARGET -s $SCOPE -p 22
```

#### 14. SMB Enumeration (null-session shares/users)
```bash
python3 smb_enum_scanner.py -t $TARGET -s $SCOPE -p 445
```

#### 15. Web Assessment
```bash
python3 web_scanner.py -t $TARGET -s $SCOPE -p 80,443,8080,8443
```

#### 16. Database Services
```bash
python3 db_scanner.py -t $TARGET -s $SCOPE -p 3306,5432,1433,1521
```

#### 17. LDAP
```bash
python3 ldap_scanner.py -t $TARGET -s $SCOPE -p 389,636
```

#### 18. DNS
```bash
python3 dns_scanner.py -t $TARGET -s $SCOPE -p 53
```

#### 19. NFS Exports
```bash
python3 nfs_scanner.py -t $TARGET -s $SCOPE -p 2049
```

#### 20. FTP
```bash
python3 ftp_scanner.py -t $TARGET -s $SCOPE -p 21
```

#### 21. Rsync
```bash
python3 rsync_scanner.py -t $TARGET -s $SCOPE -p 873
```

#### 22. VNC
```bash
python3 vnc_scanner.py -t $TARGET -s $SCOPE -p 5900,5901
```

#### 23. SNMP
```bash
python3 snmp_scanner.py -t $TARGET -s $SCOPE --port 161
```

#### 24. IPMI/BMC
```bash
python3 ipmi_scanner.py -t $TARGET -s $SCOPE -p 623
```

#### 25. SMTP
```bash
python3 smtp_scanner.py -t $TARGET -s $SCOPE -p 25,587
```

---

### Tips

- Add `-o results.jsonl` to any command to save output to a file
- Add `-v` for verbose output
- `syn_scanner` and `mass_scan` need `sudo` (raw sockets)
- For full port coverage: `-p 1-65535` (slow) or use `mass_scan` for speed
- After running, pipe through `python3 -m json.tool` if output is single-line JSON

---

## Prompt 3: Is main_scripts What the Probe/Agent Runs for Manager Jobs?

**Q:** Is it main_scripts that probe or vedha-agent is running when manager provides a job?

**A: No — the agent runs `workflow/`, not `main_scripts/`.**

### Actual Execution Path (manager job)

```
Manager → probe/agent/engine.py
             ↓
          _SCAN_MAP["network_va"] → workflow/modes.assessment
             ↓
          workflow/workflow_engine.py  (run_engagement)
             ↓
          workflow/gates.py → router.py → execution.py
             ↓
          imports scanner/* (same scanner code as main_scripts)
             ↓
          emits raw JSONL facts → back to manager
             ↓
          manager/detection_engine/ does ALL detection
```

### Key Differences

| | `main_scripts/` (standalone) | `workflow/` (agent, runs for manager jobs) |
|---|---|---|
| Triggered by | You manually, CLI | Manager job dispatch |
| Orchestration | `va_campaign.py`, `scan_funnel.py`, `run_all.py` | `workflow_engine.py` + `gates.py` + `modes.py` |
| Scanner code | `main_scripts/*.py` | `scanner/*` (same underlying code, synced copy) |
| Detection/findings | `main_scripts/findings.py` runs **locally** | **None** — agent is collection-only, manager does 100% of detection |
| Output | Findings printed to terminal | Raw JSONL facts sent to manager |

### Why This Matters

- Running `python3 smb_scanner.py` manually tests the **scanner + findings logic together**
- When the manager runs a job, only the **scanner runs on the probe** — the manager's `detection_engine/` (posture_rules + CVE matcher) handles all detection
- If the manager's detection side is wrong/missing a rule, the manager job will miss that vuln even if the scanner correctly collected the fact
