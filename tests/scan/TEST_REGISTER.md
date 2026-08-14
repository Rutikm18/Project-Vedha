# Scan Harness — Manual Testing Register

Granular test register for the per-scanner intensity harness in
`probe/tests/scan/`. Work top to bottom, run each command, then fill in the
**Status** and **Remark** columns yourself.

- **Status:** `OK` = passed / `FAIL` = failed / `-` = not run yet
- **Remark:** what you saw (counts, banners, errors, anything odd)
- Run everything from `probe/tests/scan/` unless a row says otherwise.

**Targets used below** (edit to match your LAN):

| Alias | IP | Role |
|---|---|---|
| WIN | 192.168.1.68 | Windows box (135/445/3389) |
| RTR | 192.168.1.254 | Router / gateway (22/80/443) |
| PHONE | 192.168.1.84 | iPhone (62078) |
| NET | 192.168.1.64/27 | small CIDR covering the live hosts |
| CIDR | 192.168.1.0/24 | full subnet |

Scanners (11): `host_discovery port_scan service_banner tls_scan web_scan udp_scan smb_scan snmp_scan db_scan mcp_ai_scan mass_scan`
Profiles (5): `T1` paranoid · `T2` sneaky · `T3` normal · `T4` aggressive · `T5` insane (+ `all`)

---

## 0. Foundation / harness wiring

| ID | Scenario | Command | Expected | Status | Remark |
|---|---|---|---|---|---|
| F1 | Smoke test | `./smoke.sh` | 2 passed, 0 failed | | |
| F2 | Help text | `./run.sh --help` | usage prints, exit 0 | | |
| F3 | Too few args | `./run.sh 1.2.3.4` | usage prints, exit 1 | | |
| F4 | Bad profile | `./run.sh RTR T9 port_scan` | "unknown intensity", exit 2 | | |
| F5 | Bad scanner | `./run.sh RTR T3 bogus_scan` | "unknown scanner", exit 2 | | |
| F6 | Keep artifacts | `KEEP_ARTIFACTS=1 ./run.sh RTR T3 port_scan` | prints artifacts dir; jsonl kept | | |
| F7 | expected.env TARGET | `./run.sh - T3 host_discovery` | uses TARGET from expected.env | | |
| F8 | live w/o discovery | `rm -rf .live && ./run.sh live T3 port_scan` | "run host_discovery first", exit 3 | | |

## 1. Per-scanner smoke @ T3 (runs clean + basic finding)

| ID | Scanner | Command | Expected | Status | Remark |
|---|---|---|---|---|---|
| S1 | host_discovery | `./run.sh NET T3 host_discovery` | live-host list printed, ran clean | | |
| S2 | port_scan | `./run.sh WIN T3 port_scan` | 445 open (135/3389 too), ran clean | | |
| S3 | service_banner | `./run.sh RTR T3 service_banner` | SSH/HTTP banner reported | | |
| S4 | tls_scan | `./run.sh RTR T3 tls_scan` | TLS on 443 reported | | |
| S5 | web_scan | `./run.sh RTR T3 web_scan` | HTTP fingerprint on 80/443 | | |
| S6 | udp_scan | `./run.sh RTR T3 udp_scan` | ran clean (DNS/NTP/etc if present) | | |
| S7 | smb_scan | `./run.sh WIN T3 smb_scan` | SMB dialect on 445 | | |
| S8 | snmp_scan | `./run.sh RTR T3 snmp_scan` | ran clean (SNMP if community open) | | |
| S9 | db_scan | `./run.sh WIN T3 db_scan` | ran clean (DB if present) | | |
| S10 | mcp_ai_scan | `./run.sh RTR T3 mcp_ai_scan` | ran clean (AI endpoint if present) | | |
| S11 | mass_scan | `./run.sh WIN T3 mass_scan` | fast sweep, 445 among open | | |

## 2. Intensity matrix — each scanner × each profile

Run `./run.sh <target> all <scanner>` (sweeps T1→T5) or one profile at a time.
Mark each cell `OK`/`FAIL`. Findings should be **identical** across profiles;
only wall-clock time changes.

| Scanner | Target | T1 | T2 | T3 | T4 | T5 | Remark (timing / drops) |
|---|---|---|---|---|---|---|---|
| host_discovery | WIN | | | | | | |
| port_scan | WIN | | | | | | |
| service_banner | RTR | | | | | | |
| tls_scan | RTR | | | | | | |
| web_scan | RTR | | | | | | |
| udp_scan | RTR | | | | | | |
| smb_scan | WIN | | | | | | |
| snmp_scan | RTR | | | | | | |
| db_scan | WIN | | | | | | |
| mcp_ai_scan | RTR | | | | | | |
| mass_scan | WIN | | | | | | |

## 3. Discovery-driven pipeline (live mode)

| ID | Scenario | Command | Expected | Status | Remark |
|---|---|---|---|---|---|
| P1 | Discover + save | `./run.sh NET T3 host_discovery` | "saved N live host(s)" | | |
| P2 | Saved list | `cat .live/hosts.txt` | one IP per live host | | |
| P3 | Saved detail | `cat .live/hosts.jsonl` | mac/vendor/device_hint/ports present | | |
| P4 | Live single scanner | `./run.sh live T3 service_banner` | only live hosts, one by one | | |
| P5 | Live chain | `./run.sh live T3 port_scan service_banner` | both scanners per host | | |
| P6 | Phones = ran clean | (from P4) | randomized-MAC hosts: ran clean only, no false FAIL | | |
| P7 | Re-discover overwrites | `./run.sh WIN T3 host_discovery && cat .live/hosts.txt` | list now = just WIN | | |

## 4. Correctness scenarios (the interesting behaviors)

| ID | Scenario | Command | Expected | Status | Remark |
|---|---|---|---|---|---|
| C1 | ARP recovers silent host | `./run.sh NET T3 host_discovery` | a host with `arp` method, no tcp | | |
| C2 | Mobile detection | (from C1) | randomized-MAC → "mobile/privacy device" | | |
| C3 | iPhone via lockdownd | (from C1) | a host with 62078 → "apple-mobile" | | |
| C4 | MAC → vendor | (from C1) | router/known device shows vendor | | |
| C5 | Windows fingerprint | `./run.sh WIN T3 port_scan` | 135 + 445 + 3389 open | | |
| C6 | Router services | `./run.sh RTR T3 port_scan service_banner` | 22/80/443 open + SSH/HTTP banners | | |
| C7 | Intensity stability | `./run.sh RTR all service_banner` | same banners T1..T5, time differs | | |
| C8 | Per-host assertion | `./run.sh WIN T3 port_scan` | asserts EXPECT_PORTS_192_168_1_68 only | | |

## 5. Edge / negative scenarios

| ID | Scenario | Command | Expected | Status | Remark |
|---|---|---|---|---|---|
| E1 | Dead host | `./run.sh 192.168.1.250 T3 host_discovery` | not alive / host reachable FAIL | | |
| E2 | Unused IP not alive | pick a known-empty IP | `filtered`, alive:false | | |
| E3 | Scope enforcement | manual (see §7) — scan an out-of-scope IP | scanner refuses, scope error | | |
| E4 | T1 on single host | `./run.sh WIN T1 port_scan` | slow but same result as T3 | | |
| E5 | T5 no false-negatives | `./run.sh RTR T5 service_banner` | still finds SSH/HTTP banners | | |
| E6 | Hostname target | `./run.sh <a-hostname> T3 host_discovery` | resolves + scans (or clean error) | | |

## 6. Manual deep-dive (raw module + inspect output)

Run from `probe/` (one level up). Make a scope file first:
`echo "192.168.1.0/24" > /tmp/scope.txt`

| ID | Scanner | Manual command (from `probe/`) | Inspect | Status | Remark |
|---|---|---|---|---|---|
| M1 | host_discovery | `python3 -m scanner.host_discovery -t 192.168.1.64/27 -s /tmp/scope.txt -o /tmp/hd.jsonl -v` | `cat /tmp/hd.jsonl` — alive/mac/method | | |
| M2 | port_scan | `python3 -m scanner.port_scanner -t 192.168.1.68 -s /tmp/scope.txt -o /tmp/ps.jsonl -v` | open ports | | |
| M3 | service_banner | `python3 -m scanner.service_banner -t 192.168.1.254 -s /tmp/scope.txt -p 22,80,443 -o /tmp/sb.jsonl -v` | evidence banners | | |
| M4 | tls_scan | `python3 -m scanner.tls_scanner -t 192.168.1.254 -s /tmp/scope.txt -o /tmp/tls.jsonl -v` | cert/proto/cipher | | |
| M5 | web_scan | `python3 -m scanner.web_scanner -t 192.168.1.254 -s /tmp/scope.txt -o /tmp/web.jsonl -v` | server header/title | | |
| M6 | udp_scan | `python3 -m scanner.udp_scanner -t 192.168.1.254 -s /tmp/scope.txt -o /tmp/udp.jsonl -v` | udp replies | | |
| M7 | smb_scan | `python3 -m scanner.smb_scanner -t 192.168.1.68 -s /tmp/scope.txt -o /tmp/smb.jsonl -v` | dialect/signing | | |
| M8 | snmp_scan | `python3 -m scanner.snmp_scanner -t 192.168.1.254 -s /tmp/scope.txt -o /tmp/snmp.jsonl -v` | community/sysDescr | | |
| M9 | db_scan | `python3 -m scanner.db_scanner -t 192.168.1.68 -s /tmp/scope.txt -o /tmp/db.jsonl -v` | db banner | | |
| M10 | mcp_ai_scan | `python3 -m scanner.mcp_ai_scanner -t 192.168.1.254 -s /tmp/scope.txt -o /tmp/ai.jsonl -v` | ai endpoint | | |
| M11 | mass_scan | `python3 -m scanner.mass_scan -t 192.168.1.68 -s /tmp/scope.txt -p 1-1000 --fallback -o /tmp/mass.jsonl -v` | open ports | | |

**Inspect any output file:**
```bash
python3 -c "import json,sys;[print(r.get('port'),r.get('status'),r.get('evidence')) for l in open(sys.argv[1]) for r in [json.loads(l)]]" /tmp/hd.jsonl
```

## 7. Scope enforcement check (safety)

The scanner refuses anything not in the scope allowlist. To prove it:
```bash
cd ..                                  # probe/
echo "192.168.1.68" > /tmp/one.txt     # scope allows ONLY .68
python3 -m scanner.port_scanner -t 192.168.1.254 -s /tmp/one.txt -o /tmp/x.jsonl
# expect: 0 rows / scope refusal — .254 is not in scope
```

| ID | Scenario | Expected | Status | Remark |
|---|---|---|---|---|
| G1 | Out-of-scope target refused | no results for .254; scope-gated | | |
| G2 | In-scope target allowed | `-s` with .254 in it → scans normally | | |

---

### First-run observations (2026-08-11, T3)

Captured while validating the harness — treat as leads, verify yourself:

- **Router `.254` = "GPON Home Gateway"** — 22/80/443 open; TLS on 443; web admin
  reachable. All 11 scanners ran clean (21/22 checks).
- **Windows `.68`** — 135/445/3389 open; SMB dialect reported; no web/TLS.
- **`web_scan` is timeout-sensitive** ⚠️ — 0 rows on `.254` at **T3 (`timeout=3`)**,
  but full fingerprint at **`--timeout 4`** (HTTPS handshake + fetch needs >3s on
  this router). Test `web_scan` at **T2** or use a longer timeout for slow web
  servers. Not a scanner bug.
- **`mcp_ai_scan` is slow** — 54s (`.254`) to 162s (`.68`) at T3; it probes many
  AI ports. Expect long wall-clock; not a hang.
- **Global-EXPECT false FAILs** — running *all* scanners against *one* host makes
  `tls_scan`/`web_scan` "FAIL" on a host that lacks those services (global
  `EXPECT_TLS`/`EXPECT_WEB` applied everywhere). The register avoids this by
  pointing each scanner at the right host (§1). Only a concern in kitchen-sink runs.

### Summary

| Section | Total | OK | FAIL |
|---|---|---|---|
| 0 Foundation | 8 | | |
| 1 Per-scanner smoke | 11 | | |
| 2 Intensity matrix | 55 | | |
| 3 Pipeline | 7 | | |
| 4 Correctness | 8 | | |
| 5 Edge/negative | 6 | | |
| 6 Manual deep-dive | 11 | | |
| 7 Scope | 2 | | |
| **Total** | **108** | | |
