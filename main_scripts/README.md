# main_scripts — the actual scanner scripts (for manual runs)

A **snapshot copy** of `probe/scanner/*.py` so you can run each real scanner by
hand, read the raw findings, and check accuracy. Same code the probe runs — just
a self-contained package you drive directly.

> ⚠️ This is a COPY. If you edit the real scanners in `probe/scanner/`, re-sync:
> `cp scanner/*.py main_scripts/` (run from `probe/`). Changes here do NOT affect
> the deployed probe.

## Setup — you only provide the target IP

```bash
cd probe                                   # run from the probe/ dir
T=192.168.1.10 ; echo "$T" > /tmp/s.txt    # ← your target IP (the only input)
```
`-s /tmp/s.txt` is the authorization allowlist (just your target). Output is
JSONL printed to the terminal.

## The actual-function scanners (target IP only)

```bash
python3 -m main_scripts.host_discovery  -t $T -s /tmp/s.txt     # alive? + MAC/mobile
python3 -m main_scripts.os_fingerprint  -t $T -s /tmp/s.txt     # ICMP + TTL -> OS
python3 -m main_scripts.port_scanner    -t $T -s /tmp/s.txt     # open TCP ports
python3 -m main_scripts.service_banner  -t $T -s /tmp/s.txt -p 21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443
python3 -m main_scripts.tls_scanner     -t $T -s /tmp/s.txt     # TLS config/cert/cipher
python3 -m main_scripts.tls_fingerprint -t $T -s /tmp/s.txt     # JARM fingerprint
python3 -m main_scripts.web_scanner     -t $T -s /tmp/s.txt --timeout 6   # HTTP headers/methods
python3 -m main_scripts.udp_scanner     -t $T -s /tmp/s.txt     # UDP + amplification
python3 -m main_scripts.smb_scanner     -t $T -s /tmp/s.txt     # SMB dialect/signing (:445)
python3 -m main_scripts.snmp_scanner    -t $T -s /tmp/s.txt     # SNMP communities (:161)
python3 -m main_scripts.db_scanner      -t $T -s /tmp/s.txt     # DB fingerprint
python3 -m main_scripts.mcp_ai_scanner  -t $T -s /tmp/s.txt     # AI/MCP endpoints
python3 -m main_scripts.iot_scanner     -t $T -s /tmp/s.txt     # SSDP/RTSP/MQTT/CoAP
python3 -m main_scripts.mobile_scanner  -t $T -s /tmp/s.txt     # mobile exposure
```

Save a run instead of printing: add `-o /tmp/out.jsonl`, then view nicely:
```bash
python3 -c "import json,sys;[print(r.get('port'),r.get('status'),r.get('evidence')) for l in open(sys.argv[1]) for r in [json.loads(l)]]" /tmp/out.jsonl
```

## Need more than an IP (also copied here, but extra args)

```bash
# SYN scan — Linux+root (macOS: add --force-fallback = connect scan)
sudo python3 -m main_scripts.syn_scanner -t $T -s /tmp/s.txt -p 1-1000
# masscan wrapper (root) / pure-Python fallback (no root)
python3 -m main_scripts.mass_scan  -t $T -s /tmp/s.txt -p 1-1000 --fallback
# nmap wrapper (needs nmap; os/syn profiles need root)
python3 -m main_scripts.nmap_wrapper -t $T -s /tmp/s.txt --profile version
# credentialed
python3 -m main_scripts.ssh_collector    -t $T -s /tmp/s.txt --user U --key ~/.ssh/id_rsa
WIN_SCAN_PASSWORD=*** python3 -m main_scripts.windows_collector -t $T -s /tmp/s.txt --user U
# passive OT (listens) / delta (diffs two prior JSONL files)
python3 -m main_scripts.passive_collector -t $T -s /tmp/s.txt --listen-seconds 60
python3 -m main_scripts.delta_scanner /tmp/baseline.jsonl /tmp/current.jsonl
```

## Orchestrators (also copied)
```bash
python3 -m main_scripts.scan_funnel -t $T -s /tmp/s.txt    # per-host funnel (chains the scanners)
```

## Wrappers (which shell out to external tools)
- `mass_scan` → **masscan** (root) or pure-Python `--fallback`
- `nmap_wrapper` → **nmap**
- `host_discovery` → reads local **ARP cache** (`arp -an`) — not a scan tool
- everything else = pure Python, no external binaries
