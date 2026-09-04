# Vedha — Vulnerability Assessment Runbook (verified)

Step-by-step to run the probe and produce **real VA findings** — local lab, real targets,
and production. Every command here was run and verified end-to-end.

> **Two-deployable model:** the **probe** collects *raw facts* (never CVEs); the **manager**
> runs detection (facts → CVE findings) against its pinned vuln DB. See `ARCHITECTURE.md`.

---

## 0. What actually produces findings (read this first)

The detection engine matches against **`osv_debian_snapshot.json` (OSV, Debian:12)** + KEV/EPSS.
This governs *everything*:

- **Findings come from Debian-package/service versions** of covered products:
  `openssh, openssl, curl, nginx, apache2, mariadb, mongodb, postgresql-15, redis, samba,
  vsftpd, proftpd, bind9, dnsmasq, lighttpd, caddy, docker.io, iis, mssql, boa`.
- **Unauthenticated** detection works from banners the probe can read:
  - **SSH banner** → `openssh` (e.g. `SSH-2.0-OpenSSH_8.4p1`)
  - **HTTP `Server` header** → `nginx` / `apache2`
  - **DB handshake** → `mariadb` / `postgresql` / `redis`
- **Authenticated dpkg inventory** (300+ findings) is the richest path — **but the manager
  currently rejects credentials in job params** (`HTTP 422: "Vedha does not persist target
  credentials…"`). It is disabled until an ephemeral credential broker is added.
- **A macOS host or a Windows host will usually yield 0 CVE findings** — their services aren't
  Debian packages. That is a *correct* result, not a bug.

**Rule of thumb:** to see findings, scan a host running a **covered service with a readable
version** (openssh / nginx / apache / a DB). The lab target below does exactly that.

---

## 1. Prerequisites

- Docker Desktop / Engine running, `python3`, `curl`.
- From the repo root:
  ```bash
  cd "<repo>"        # this project
  make doctor        # checks Docker, ports 18080/3000, .env, insecure defaults
  ```
- Default admin: `admin@vedha.io` / `ChangeMe123!` (change `SEED_ADMIN_PASSWORD` in `.env`).

---

## 2. One-command live VA (recommended) — `scripts/probe-lab.sh`

Brings the manager up, stands up a **vulnerable Debian target**, runs the **real probe**
against it, waits for detection, and prints the VA report. **Verified: 39 findings.**

```bash
ADMIN_PASSWORD=ChangeMe123! scripts/probe-lab.sh
```
Expected:
```
✓ manager up · ✓ authenticated
• lab target up: 172.18.0.9 (openssh + nginx)
• compose probe online (covers 172.18.0.0/16): local-probe
  → job … scan: completed · detecting…
── VA REPORT ──
  probe funnel : host_alive=1 services=5 (host_discovery/port_scan/service_banner/web_scan ✓)
  findings     : 39  (C3 H9 M8 L2 I17)
     [CRITICAL] cvss 7.7  CVE-2021-23017  nginx
     [CRITICAL] cvss 7.5  CVE-2023-44487  nginx  (HTTP/2 Rapid Reset)
     [    HIGH] cvss 7.4  CVE-2020-15778  openssh
```
Then open **Dashboard → http://localhost:3000 → Findings** and click **Explain** (Ask Vedha).

Scan a **real LAN host** instead of the lab target:
```bash
# run this in YOUR terminal (native probe needs real LAN access; see §6 macOS note)
scripts/probe-lab.sh --target 192.168.1.78 --cidr 192.168.1.0/24
```
Cleanup: `docker rm -f vedha-lab-target`.

---

## 3. Run the probe manually — local lab, step by step

If you want the individual steps instead of the wrapper:

```bash
cd "<repo>"

# 1. manager up
make up
curl -s -o /dev/null -w "api %{http_code}\n" http://localhost:18080/health   # 200

# 2. vulnerable Debian target on the manager's Docker network
docker run -d --name vuln-target --network vedha_default --hostname deb-vuln debian:11 bash -c \
 "apt-get update -qq && apt-get install -y openssh-server nginx >/dev/null 2>&1; \
  mkdir -p /run/sshd; nginx; /usr/sbin/sshd -D"
sleep 25
IP=$(docker inspect vuln-target --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'); echo "$IP"

# 3. probe on the same network (segment must cover the target)
PROBE_NETWORK_SEGMENTS=172.18.0.0/16 docker compose --profile probe up -d probe

# 4. login → engagement → unauthenticated assessment → poll
BASE=http://localhost:18080
TOKEN=$(curl -s -X POST $BASE/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"admin@vedha.io","password":"ChangeMe123!"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
EID=$(curl -s -X POST $BASE/engagements -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"Live probe VA","scope_cidrs":["172.18.0.0/16"]}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
JID=$(curl -s -X POST $BASE/agents/jobs -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"engagement_id\":\"$EID\",\"use_case_id\":\"uc_full_assessment\",\"params\":{\"targets\":[\"$IP\"],\"scope_cidrs\":[\"172.18.0.0/16\"]}}" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["job_id"])')
until [ "$(curl -s $BASE/agents/jobs/$JID -H "Authorization: Bearer $TOKEN" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("status"))')" = completed ]; do sleep 4; done

# 5. WAIT for async detection, then read findings  (see §7 gotchas)
sleep 8
curl -s "$BASE/findings/summary?engagement_id=$EID" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
curl -s "$BASE/findings?engagement_id=$EID&page_size=100&sort=risk" -H "Authorization: Bearer $TOKEN" \
  | python3 -c 'import sys,json;[print((x.get("cve_ids") or [""])[0], x.get("cvss_score"), x.get("title")) for x in json.load(sys.stdin)["items"][:15]]'
```

---

## 4. Turn a probe scan export into a VA (offline / re-detect) — `scripts/detect-va.sh`

Runs a facts file through the *same* detection pipeline a live probe result takes. **Verified.**

```bash
scripts/detect-va.sh                              # DEMO: vulnerable Debian host → real findings
scripts/detect-va.sh --facts <probe-scan.jsonl>   # your own probe export
```

---

## 5. Operator scripts (all verified this session)

| Script / command | Does |
|---|---|
| `scripts/probe-lab.sh` | One-command **live probe** VA (lab or `--target <ip>`). |
| `scripts/detect-va.sh` | Import a facts file → real detection → VA report. |
| `scripts/run_engagement.sh <mgr> <cidr>` | Operator flow: confirm probe → engagement → discovery+assessment → findings, with per-stage error + pipeline-breakpoint diagnosis. |
| `scripts/assess.sh <scope>` | Self-provisioning assessment + funnel/accuracy/failure debug. |
| `probe/test_capabilities.sh [target]` | Standalone probe **capability self-test** (no manager needed). |
| `make probe-pat` | Mint a scoped probe PAT (`vpat_…`) — no dashboard PAT UI exists. |
| `make doctor` | Preflight: Docker, ports, `.env`, insecure defaults. |

---

## 6. Production deployment (real client network)

Split topology: **manager in your cloud behind TLS**, **probe on a Linux host inside the
client network** (dial-out only). The container probe reaches the LAN natively on Linux (the
macOS Docker NAT limitation does *not* apply there).

```bash
# on YOUR machine — mint a scoped PAT
make probe-pat ARGS="--url https://vedha.<domain> --email you@vendor.com --days 365"   # → vpat_…

# (optional) host-bound license
PROBE_IMAGE=<registry>/vedha-probe:1.0 sh install.sh hostid                              # on the client host
python3 probe/tools/issue_license.py issue --hostid <HOSTID> --customer "<Client>" --days 365

# on the CLIENT host — install (dial-out only, no inbound ports). install.sh preflights the
# URL + token and ships hardened: --read-only, --cap-drop ALL, no-new-privileges, --pids-limit,
# PROBE_MAX_TARGETS / PROBE_MAX_JOB_SECONDS caps, persistent identity volume.
curl -fsSL https://vedha.<domain>/install.sh -o install.sh && less install.sh
PROBE_IMAGE=<registry>/vedha-probe:1.0 \
PLATFORM_URL=https://vedha.<domain> \
OPERATOR_TOKEN=vpat_<…> \
PROBE_LICENSE=<token> PROBE_LICENSE_PUBKEY=<64-hex-public-key> \
LICENSE_ENFORCED=true VERIFY_TLS=true \
PROBE_NAME="<client>-probe-01" PROBE_NETWORK_SEGMENTS=<AUTHORIZED_CIDR> \
sh install.sh

docker logs -f vedha-probe        # License OK → Registered as … → WebSocket push mode
```
Drive the scan with `scripts/run_engagement.sh https://vedha.<domain> <AUTHORIZED_CIDR>` or the
dashboard **Scanner** page. Hardening checklist: `prod_test.md §9`.

---

## 7. Troubleshooting (the exact failure modes, with fixes)

| Symptom | Cause → Fix |
|---|---|
| Job stuck **`pending`** forever | No online probe whose **`network_segments` covers the target**. → set `PROBE_NETWORK_SEGMENTS` to a CIDR containing the target; confirm `GET /agents` shows an online probe covering it. |
| **`422` "credentials not accepted"** | Authenticated scanning is disabled. → run **unauthenticated**; expose covered services on the target for banner-based findings. |
| Job **`completed` but 0 findings** | Detection runs **asynchronously** after the probe submits. → poll `GET /findings/summary?engagement_id=…` until `total>0` (a few seconds). |
| `0 findings` even after detection | Target exposes **no covered service** (macOS/Windows host, or services not running). → scan a host running openssh/nginx/apache/a DB. |
| Findings query returns **0 unexpectedly** | Either a **stale JWT** (login tokens expire fast — re-login) or **`page_size>100`** (backend caps at 100 → 422). → fresh token, `page_size≤100`, use `/findings/summary` for totals. |
| Scan finds a **dead host** (COLLECTION stage) | Target down / out of scope / unreachable from the probe's vantage. → verify reachability from the probe host first (`nc -z <ip> <port>`). |
| macOS: containerised probe can't reach the LAN | Docker Desktop NAT-isolates the Mac's LAN. → for real LAN targets use the **native probe** run **in a real terminal** (`python3 -m agent.agent`), scoped to the LAN CIDR. Container→container on the Docker network works fine (that's the lab). |
| Native probe: `Operation not permitted: '/tmp'` | The probe was launched from a **sandboxed shell**. → run it from a normal terminal, or set `TMPDIR`/`STATE_FILE`/`RESULT_SPOOL_DIR` to a writable dir. |

**Pipeline breakpoint quick map:** `host_count=0` → COLLECTION (target/reachability); facts
collected but `assets=0` → INGEST (`docker compose logs api worker`); `assets>0, findings=0` →
DETECTION (no covered service / version-poor). `scripts/assess.sh` and `run_engagement.sh` print
this automatically.

---

## 8. Reference

**Use-case catalog** (`GET /agents/use-cases`): `uc_discovery_only`, `uc_full_assessment`,
`uc_external_web_triage`, `uc_db_exposure`, `uc_windows_estate`, `uc_snmp_exposure`,
`uc_udp_service_exposure`, `uc_web_app_triage`, `uc_ai_endpoint_sweep`, `uc_iot_device_survey`,
`uc_ot_passive` (passive-only), `uc_rescan_delta`.

**Key endpoints:** `POST /auth/login` · `POST /auth/personal-access-tokens` ·
`GET /agents` · `POST /agents/jobs` · `GET /agents/jobs/{id}` ·
`POST /engagements` · `POST /engagements/{id}/scans/import-facts` ·
`GET /findings?engagement_id=&page_size≤100&sort=risk` · `GET /findings/summary?engagement_id=`.

**Scope safety:** dual-enforced — the manager refuses to dispatch out-of-scope and the probe
refuses to scan outside `scope_cidrs`. `ot` profile is passive-only on both ends.
