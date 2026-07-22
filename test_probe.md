# Probe Testing Guide

## Environment

- **Python**: 3.13.7 (use `python3`, not `python`)
- **Project root**: `/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner`
- **Probe root**: `probe/`
- **Run all scanner CLIs from `probe/`**: `cd probe` first — scanner modules use package-relative imports and must be invoked as `python3 -m scanner.<module>`.

---

## Step-by-step test plan

### Step 1 — Unit tests (baseline)

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner"
python3 -m pytest probe/tests/ -v --tb=short
```

**Expected result**

```
============================= 268 passed in ~1.6s ==============================
```

| Test file | Count | What it covers |
|---|---|---|
| `test_probe_core.py` | 141 | ScopeGuard, target expansion, port parsing, ScanResult, RateLimiter, gates, router, modes, Asset, cache, agent/engine, use_cases |
| `test_transport.py` | 23 | Register, heartbeat, poll, fetch scope, submit, gzip, http_get, WebSocket |
| `test_task_runner.py` | 17 | Use-case resolution, scope validation, job submission, scan dispatch |
| `test_scope_validator.py` | 20 | Scope validation, exclusions, merge, engagement fetch |
| `test_scope_crypt.py` | 12 | Identity generation, scope encrypt/decrypt roundtrip, tamper detection |
| `test_result_spool.py` | 12 | ResultSpool save/load, retry, flush, corrupt handling |
| `test_hw_bind.py` | 7 | Hardware ID, host-bind check, dev mode |
| `test_integration.py` | 26 | Full lifecycle: identity → encrypt → job → decrypt → validate → submit |
| **Total** | **268** | |

---

### Step 2 — Scanner module imports

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner"
python3 -c "
import sys; sys.path.insert(0, 'probe')
from scanner.port_scanner import PortScanner
from scanner.host_discovery import HostDiscoveryScanner
from scanner.service_banner import ServiceBannerScanner
from scanner.tls_scanner import TLSScanner
from scanner.web_scanner import WebScanner
from scanner.smb_scanner import SMBScanner
from scanner.snmp_scanner import SNMPScanner
from scanner.db_scanner import DBScanner
from scanner.udp_scanner import UDPScanner
from scanner.passive_collector import PassiveCollector
from scanner.ssh_collector import SSHCollector
from scanner.windows_collector import WindowsCollector
from scanner.nmap_wrapper import main
from scanner.mass_scan import _ConnectSweep
from scanner.mcp_ai_scanner import MCPAIScanner
print('All 14 scanner modules imported successfully')
"
```

**Expected result**

```
All 14 scanner modules imported successfully
```

---

### Step 3 — Scanner CLI `--help` smoke test

```bash
cd probe
for mod in port_scanner host_discovery service_banner tls_scanner web_scanner \
           smb_scanner snmp_scanner db_scanner udp_scanner passive_collector \
           ssh_collector windows_collector mass_scan mcp_ai_scanner; do
  python3 -m scanner."$mod" --help 2>&1 | head -3
  echo "---"
done
```

**Expected result** — Every module prints a `usage:` line and exits `0`. No `ModuleNotFoundError` or `SystemError`.

---

### Step 4 — Local fixture scan

Set up a known-good localhost service so results can be verified against ground truth.

```bash
cd probe
rm -rf /tmp/vafix
mkdir -p /tmp/vafix

# HTTP server on 8080 with a known title
printf '<html><head><title>GROUND-TRUTH-PAGE</title></head><body>hi</body></html>' > /tmp/vafix/index.html
( cd /tmp/vafix && python3 -m http.server 8080 --bind 127.0.0.1 >/tmp/vafix/http.log 2>&1 & )

# TLS server on 8443
openssl req -x509 -newkey rsa:2048 -keyout /tmp/vafix/k.pem -out /tmp/vafix/c.pem -days 1 -nodes -subj "/CN=localhost" 2>/dev/null
( openssl s_server -key /tmp/vafix/k.pem -cert /tmp/vafix/c.pem -accept 8443 -www >/tmp/vafix/tls.log 2>&1 & )

# Fake banner service on 3389
cat > /tmp/vafix/banner.py <<'PY'
import socketserver
class H(socketserver.BaseRequestHandler):
    def handle(self):
        try: self.request.sendall(b"GROUND-TRUTH-BANNER-1.0\r\n")
        except OSError: pass
class S(socketserver.ThreadingTCPServer): allow_reuse_address=True
S(("127.0.0.1", 3389), H).serve_forever()
PY
( python3 /tmp/vafix/banner.py >/tmp/vafix/banner.log 2>&1 & )

sleep 2
printf '127.0.0.1\n' > /tmp/test_scope.txt
```

Ground-truth snapshot (your answer key):

```bash
lsof -nP -iTCP@127.0.0.1 -sTCP:LISTEN | awk 'NR==1 || /127.0.0.1/{print $1, $9}'
curl -s http://127.0.0.1:8080/ | grep -o '<title>.*</title>'
echo | openssl s_client -connect 127.0.0.1:8443 2>/dev/null | grep -i protocol
nc 127.0.0.1 3389 <<< "" | head -c 40; echo
```

**Expected result** — `8080`, `8443`, and `3389` are listening; `3306` may also be open if MySQL is running locally.

---

#### 4a — host_discovery

```bash
python3 -m scanner.host_discovery -t 127.0.0.1 -s /tmp/test_scope.txt
```

**Expected result** — JSONL line with `"alive": true` and at least one `"status": "open"` port (3389).

#### 4b — port_scanner

```bash
python3 -m scanner.port_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
```

**Expected result** — Reports the truly-open ports: `3389`, `8080`, `8443` (and `3306` if MySQL is running). No false positives on closed ports.

#### 4c — service_banner

```bash
python3 -m scanner.service_banner -t 127.0.0.1 -s /tmp/test_scope.txt -p 3389,8080,8443
```

**Expected result**

| Port | Expected banner / evidence |
|---|---|
| 3389 | `GROUND-TRUTH-BANNER-1.0` verbatim |
| 8080 | `HTTP/1.0 200 OK` and `Server: SimpleHTTP...` |
| 8443 | Binary TLS bytes (not a text service) |

#### 4d — tls_scanner

```bash
python3 -m scanner.tls_scanner -t 127.0.0.1 -s /tmp/test_scope.txt -p 8443
```

**Expected result** — `accepted_versions` includes `TLSv1.3` or `TLSv1.2`. Negative control on port 8080 should yield no result.

#### 4e — web_scanner

```bash
python3 -m scanner.web_scanner -t 127.0.0.1 -s /tmp/test_scope.txt -p 8080
```

**Expected result** — `"title": "GROUND-TRUTH-PAGE"` and `Server: SimpleHTTP...`.

#### 4f — db_scanner

```bash
python3 -m scanner.db_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
```

**Expected result** — If MySQL is running on 3306: `"engine": "mysql/mariadb"` and a version string matching `mysql --version`. If MySQL is not running: no output (correct negative).

#### 4g — udp / smb / snmp (localhost negatives)

```bash
python3 -m scanner.udp_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
python3 -m scanner.smb_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
python3 -m scanner.snmp_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
```

**Expected result** — No `"status": "open"` lines. Mostly `filtered` or no output; this is correct on a macOS localhost with no UDP/SMB/SNMP services.

#### 4h — mcp_ai_scanner

```bash
python3 -m scanner.mcp_ai_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
```

**Expected result** — On macOS, port 5000 may be flagged as `ollama`/`mcp` with `auth_enforced=true`. That is a known false positive caused by macOS AirPlay returning 403. For a real true positive, run `ollama serve` and re-scan `127.0.0.1`.

---

### Step 5 — Orchestrator scripts

#### 5a — run_scan.py

```bash
python3 run_scan.py -t 127.0.0.1 -s /tmp/test_scope.txt \
    --scanners host_discovery port_scanner service_banner --split-output /tmp/va_runs
```

**Expected result** — Scope validated, each chosen scanner runs, and `/tmp/va_runs/` contains one `.jsonl` file per scanner with valid results.

#### 5b — pipeline.py (IT profile)

```bash
python3 pipeline.py -t 127.0.0.1 -s /tmp/test_scope.txt --profile it
```

**Expected result** — One clean per-host summary reproducing Step 4 findings: open ports with service names (banner, http, tls, mysql if present).

#### 5c — workflow.cli

```bash
python3 -m workflow.cli -t 127.0.0.1 -s /tmp/test_scope.txt --profile it --mode triage
```

**Expected result** — Exits 0 and emits a JSON result file with discovery + port + banner facts.

---

### Step 6 — Scope safety test

```bash
python3 -m scanner.port_scanner -t 8.8.8.8 -s /tmp/test_scope.txt -v
```

**Expected result** — A scope-refusal message (e.g., `dropping out-of-scope target`) and no scan results. Confirm zero traffic in a second terminal:

```bash
sudo tcpdump -i any -n 'host 8.8.8.8' -c 3
```

You should see no packets.

---

### Step 7 — OT passive-safety test

```bash
# terminal 1 — packet watcher (replace with your LAN IP)
sudo tcpdump -i any -n 'udp and src host 192.168.x.x' -c 5

# terminal 2 — passive listen
python3 pipeline.py -t 192.168.x.0/24 -s /tmp/test_scope.txt --profile ot --listen-seconds 20 -v
```

**Expected result** — The probe reports hosts it hears via mDNS/SSDP, while tcpdump captures zero outbound probe packets. OT mode is receive-only.

---

### Step 8 — Cross-engine agreement

```bash
python3 -m scanner.port_scanner -t 127.0.0.1 -s /tmp/test_scope.txt
python3 -m scanner.nmap_wrapper -t 127.0.0.1 -s /tmp/test_scope.txt --profile fast
python3 -m scanner.mass_scan -t 127.0.0.1 -s /tmp/test_scope.txt -p 1-10000 --fallback
```

**Expected result** — All three engines agree on the same open ports (`3389`, `8080`, `8443`, and `3306` if present). `nmap_wrapper` requires the `nmap` binary; `mass_scan --fallback` uses the pure-Python sweep and does not need root.

---

### Step 9 — Full agent–manager round-trip (optional, requires Docker stack)

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner"
docker compose up -d --build
docker compose --profile probe up
```

**Expected result** — Probe logs show, in order:

1. `Registered as '<name>'` and `Capabilities: discovery, ..., passive_discovery`.
2. Heartbeat every ~30 seconds.
3. On job dispatch: poll/job pickup → scan → result submitted.

Then dispatch a scan from the Scanner UI and verify the job completes and facts flow into `scan_results` and findings into `findings`.

---

### Step 10 — Teardown

```bash
pkill -f "http.server 8080"
pkill -f "/tmp/vafix/banner.py"
pkill -f "openssl s_server"
rm -rf /tmp/vafix /tmp/test_scope.txt /tmp/va_runs
```

**Expected result** — All fixtures stopped and scratch files removed.

---

## Summary of expected results

| Layer | Test count | Expected pass | Expected fail | Notes |
|---|---|---|---|---|
| Unit tests | 268 | 268 | 0 | `pytest probe/tests/` |
| Scanner imports | 14 | 14 | 0 | Pure Python + optional deps |
| Scanner `--help` | 14 | 14 | 0 | CLI smoke test |
| Individual scans | 8+ | all | 0 | Against localhost fixtures |
| Orchestrators | 3 | 3 | 0 | `run_scan.py`, `pipeline.py`, `workflow.cli` |
| Scope safety | 1 | 1 | 0 | Out-of-scope target refused |
| OT passive | 1 | 1 | 0 | No outbound probe packets |
| Cross-engine | 3 | 3 | 0 | port_scanner == nmap == mass_scan |
| Agent–manager | 1 | 1 | 0 | Requires Docker stack |

**Overall expected result: all tests pass, no crashes, no false positives on closed ports, and all open fixture ports are detected.**

---

## Quick one-command smoke test

Use the bundled script for a fast pass/fail matrix:

```bash
cd probe
./Testscipt.sh
```

This sets up the fixtures, runs every scanner, checks results against ground truth, and prints a PASS/FAIL summary table.

For a simpler (no ground-truth checking) smoke test:

```bash
cd probe
./test_all.sh
```

Both scripts should finish with zero failures for a healthy probe.

---

## Common pitfalls

- **Run scanner CLIs from `probe/`** — they rely on `from .scanner_base import ...`.
- **Always use `python3`** — `python` is not on PATH.
- **Scope file is mandatory** — every scanner requires `-s`.
- **macOS port 5000 AirPlay false positive** — not a real MCP/AI service; filter it out.
- **MySQL on 3306** — if present, DB scanner will find it; if absent, no output is correct.
