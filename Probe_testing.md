# Probe Production Run Guide

This guide is for actually running the probe in a production or client network.
It is based on the current code path:

`manager /agents/jobs -> probe agent.task_runner -> agent.engine -> workflow.workflow_engine -> scanner/*`

The probe is a collection agent. It sends outbound traffic only to the manager,
polls for approved jobs, enforces scope again before scanning, collects raw
facts, and ships results back for manager-side detection.

## Verified local smoke test

Last verified: 2026-07-17.

What was tested:

```text
manager API + worker + postgres + redis + local probe container
probe registration -> WebSocket control channel -> scoped job dispatch
scope re-validation -> web scan -> result upload -> asset/service promotion
```

Result:

```text
probe: local-probe
capabilities: 16
use-cases: 12
job: uc_web_app_triage
target: local API container only
status: completed
scan_type: web_scan
facts: 4
hosts: 1
open_ports: 3
promoted asset: 172.18.0.4
promoted service: 8000/tcp
```

Important fix made during testing:

- Manager result ingest now dedupes duplicate service facts in the same probe result.
- This prevents duplicate `(asset_id, port, protocol)` inserts from breaking result submission.
- Probe result retry/spooling can now safely clear after the manager ACKs the result.

Local compose uses `http://api:8000` inside Docker, so the probe correctly logs a
plain-HTTP warning. Production must use `https://` with TLS verification enabled.

---

## 0. Non-negotiable production rules

Do this before any packet leaves the probe host.

1. Get written authorization for the exact CIDRs, hosts, and time window.
2. Put only approved assets in `scope_cidrs`.
3. Put fragile or forbidden assets in `excluded_cidrs`.
4. Never run active scans on OT/ICS/SCADA. Use `uc_ot_passive` only.
5. Start with one known non-critical host, then a small range, then the full approved range.
6. Use HTTPS for `PLATFORM_URL`. Keep `VERIFY_TLS=true`.
7. Keep Postgres and Redis private. Expose only the manager/API through TLS.
8. Keep the probe state volume. If you delete it, the probe re-registers as a new identity.

Recommended rollout order:

```text
single host discovery
single host service-specific scan
single host full assessment
small CIDR discovery, for example /28
approved production CIDR, for example /24
```

---

## 1. Know what the current probe can run

From the repo:

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/probe"

python3 -c "from agent.engine import CAPABILITIES; print(len(CAPABILITIES)); print(', '.join(CAPABILITIES))"
python3 -c "from agent.use_cases import USE_CASES; print(len(USE_CASES)); print('\\n'.join(f'{k}: {v[\"scan_type\"]}/{v[\"profile\"]}' for k,v in sorted(USE_CASES.items())))"
```

Current capabilities:

```text
ai_service_discovery
assessment
db_fingerprint
discovery
host_discovery
mcp_discovery
passive_discovery
port_scan
service_fingerprint
smb_enum
snmp_enum
snmp_scan
tls_scan
udp_scan
vuln_scan
web_scan
```

Current production use-cases:

| Use-case | Profile | What it does | Production use |
|---|---:|---|---|
| `uc_discovery_only` | IT | Host + port triage | First safe run |
| `uc_full_assessment` | IT | Discovery, ports, banners, deep branches | Full approved assessment |
| `uc_external_web_triage` | IT | TLS/web surface | Internet-facing web check |
| `uc_db_exposure` | IT | DB protocol fingerprints | Exposed DB review |
| `uc_windows_estate` | IT | SMB dialect/share signals | Windows estate check |
| `uc_ot_passive` | OT | Listen-only discovery | OT/ICS only |
| `uc_ai_endpoint_sweep` | IT | MCP/AI endpoint discovery | AI service exposure |
| `uc_rescan_delta` | IT | Full assessment for diffing | Repeat assessment |
| `uc_iot_device_survey` | IoT | IoT ports + banners | Embedded/IoT survey |
| `uc_web_app_triage` | IT | Web headers/methods/tech | Web app triage |
| `uc_udp_service_exposure` | IT | DNS/NTP/SNMP/NetBIOS UDP | UDP exposure review |
| `uc_snmp_exposure` | IT | SNMP read-only sysDescr checks | Network device SNMP review |

---

## 2. Production architecture

Use this layout:

```text
Operator browser
    |
    | HTTPS
    v
Manager/API + dashboard
    |
    | outbound HTTPS from probe to manager
    v
Probe inside client network
    |
    | scoped scan traffic only
    v
Approved target CIDRs
```

Manager responsibilities:

- Authentication, tenants, engagements, scope, job queue, result ingest.
- Detection and findings from raw probe facts.
- Stores CVE/vulnerability data. The probe does not need the vuln DB.

Probe responsibilities:

- Register or resume identity.
- Heartbeat and poll/push job handling.
- Re-fetch engagement scope before scanning.
- Refuse out-of-scope and excluded targets.
- Collect raw facts only.
- Spool results locally if manager is temporarily unreachable.

Control/data behavior:

- The probe keeps a continuous outbound control channel to the manager.
- WebSocket push is tried first; HTTP polling is the fallback.
- The probe continuously sends heartbeat/state.
- Scans are on-demand: no target scan runs until the manager queues a job.
- Results are sent after each job. If the manager is down or rejects the ACK,
  results are spooled locally and retried until accepted.

Production security requirement:

```text
PLATFORM_URL=https://manager.example.com
VERIFY_TLS=true
PROBE_CA_BUNDLE=/path/to/private-ca.pem   # only when using private PKI
```

Optional mTLS:

```text
PROBE_CLIENT_CERT=/etc/vedha/probe.crt
PROBE_CLIENT_KEY=/etc/vedha/probe.key
```

---

## 3. Bring up the manager in production mode

On the manager host:

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner"
cp .env.docker.example .env
$EDITOR .env
```

Set these before production:

```env
APP_ENV=production
JWT_SECRET=<long-random-secret-at-least-32-chars>
SEED_ADMIN_EMAIL=<real-admin-email>
SEED_ADMIN_PASSWORD=<strong-temporary-password-change-after-first-login>
CORS_ORIGINS=https://<dashboard-domain>
API_PORT=18080
FRONTEND_PORT=3000
```

Start the platform:

```bash
docker compose up -d --build
docker compose --profile ui up -d --build frontend
docker compose ps
curl -fsS http://127.0.0.1:18080/health
```

For production internet/client access, put a reverse proxy or load balancer in
front of the API and dashboard:

```text
https://manager.example.com   -> api container port 8000, host port 18080
https://dashboard.example.com -> frontend container port 3000
```

Do not expose Postgres or Redis to the internet.

Optional graph stack:

```bash
NEO4J_ENABLED=true docker compose --profile graph up -d --build
```

---

## 3A. Two-machine lab: one Mac and one Windows system

Use this when you have only your Mac and one Windows machine. Keep the scope to
your own systems and local LAN IPs only.

Recommended roles:

```text
Mac      = manager/API + dashboard + operator CLI
Windows  = test target, and optionally the probe host for production-like testing
```

### 3A.1 Get the network addresses

On the Mac:

```bash
MAC_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
echo "$MAC_IP"
```

On Windows PowerShell:

```powershell
Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object {$_.IPAddress -notlike '169.254*' -and $_.InterfaceAlias -notlike '*Loopback*'} |
  Select-Object InterfaceAlias,IPAddress
```

Pick the Windows LAN IP, for example `192.168.1.50`.

### 3A.2 Start the manager on the Mac

For a local lab:

```bash
docker compose up -d --build api worker
curl -fsS http://127.0.0.1:18080/health
```

Make sure macOS firewall allows inbound connections to port `18080` from the
Windows machine. Then test from Windows:

```powershell
Test-NetConnection <MAC_IP> -Port 18080
Invoke-RestMethod "http://<MAC_IP>:18080/health"
```

If this fails, fix networking before touching the probe.

### 3A.3 Create a PAT on the Mac

```bash
BASE="http://127.0.0.1:18080"

ACCESS_TOKEN=$(curl -fsS -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vedha.io","password":"ChangeMe123!"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

PAT_RESPONSE=$(curl -sS -X POST "$BASE/auth/personal-access-tokens" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  --data-raw '{"name":"mac-windows-lab","expires_in_days":7,"scopes":["probe:read","probe:write","probe:register","engagement:read","engagement:write"]}')

printf '%s\n' "$PAT_RESPONSE"
PROBE_PAT=$(printf '%s' "$PAT_RESPONSE" | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

echo "$PROBE_PAT"
```

Store the PAT somewhere temporary. Revoke it after the lab.
Do not split a quoted JSON string across terminal lines. If the API returns an
error body instead of `token`, fix that response before running the Python
extract command.

### 3A.4 Simple test: run the probe on Mac and scan Windows

This verifies the manager, CLI, job dispatch, scope enforcement, result upload,
and Windows target visibility.

On Windows, start a safe test web service:

```powershell
mkdir C:\probe-lab
cd C:\probe-lab
"probe lab ok" | Out-File index.html
py -m http.server 8080 --bind 0.0.0.0
```

Allow the Windows Firewall prompt for Python on the private network only. From
the Mac:

```bash
curl -I "http://<WINDOWS_IP>:8080/"
```

Authenticate and start the local probe on the Mac:

```bash
cd probe
export PROBE_PAT="$PROBE_PAT"
./probe auth login --manager "http://127.0.0.1:18080"
./probe daemon run --name mac-lab-probe --segment "<WINDOWS_IP>/32"
```

Open a second terminal on the Mac and run:

```bash
cd probe
./probe doctor

EID=$(./probe engagements create \
  --name "Mac Windows local lab" \
  --scope "<WINDOWS_IP>/32" \
  --scan-profile it \
  --json | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

./probe doctor --engagement-id "$EID"

./probe scan run \
  --engagement-id "$EID" \
  --use-case uc_web_app_triage \
  --target "<WINDOWS_IP>" \
  --param ports=8080 \
  --wait \
  --json
```

Expected:

- `probe doctor` shows manager health, authenticated PAT, 12 use-cases, and at
  least one online probe.
- The scan job ends as `completed`.
- The manager shows the Windows IP as an asset and `8080/tcp` as a web service.

### 3A.5 Production-like test: run the probe container on Windows

Use this when you want to test the real outbound-client deployment pattern:
Windows probe connects outbound to the Mac manager, then scans the Windows LAN
IP. Install Docker Desktop on Windows and run Linux containers.

On the Mac, create a download folder and serve the installer + image:

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner"

mkdir -p /tmp/probe-dist
cp probe/install.sh /tmp/probe-dist/install.sh

# Most Windows Docker Desktop installs are linux/amd64.
docker buildx build --platform linux/amd64 -t vedha-probe:local-amd64 --load ./probe
docker save vedha-probe:local-amd64 -o /tmp/probe-dist/vedha-probe-local-amd64.tar

python3 -m http.server 8000 --directory /tmp/probe-dist
```

Keep that HTTP server running. From Windows PowerShell, verify download access:

```powershell
Invoke-WebRequest "http://<MAC_IP>:8000/install.sh" -OutFile install.sh
Get-Content .\install.sh -TotalCount 20
```

The installer is a shell script. Run it from WSL Ubuntu or Git Bash on Windows.
In WSL/Git Bash:

```bash
curl -fsSL "http://<MAC_IP>:8000/install.sh" | \
  PLATFORM_URL="http://<MAC_IP>:18080" \
  VERIFY_TLS=false \
  OPERATOR_TOKEN="<PROBE_PAT>" \
  PROBE_IMAGE="vedha-probe:local-amd64" \
  PROBE_IMAGE_TAR_URL="http://<MAC_IP>:8000/vedha-probe-local-amd64.tar" \
  PROBE_NAME="windows-lab-probe-01" \
  PROBE_LOCATION="windows-lab" \
  PROBE_NETWORK_SEGMENTS="<MAC_IP>/32" \
  LICENSE_ENFORCED=false \
  sh

docker logs -f vedha-probe
```

From the Mac:

```bash
cd probe
./probe --manager "http://127.0.0.1:18080" --pat "$PROBE_PAT" doctor
./probe agents list
```

Then create the same `/32` engagement and run `uc_web_app_triage` against
`<MAC_IP>` port `8080` when the Windows probe is scanning the Mac target.

### 3A.6 Negative tests to prove safety gates

Run these after the happy path:

```bash
# Out-of-scope target should fail or produce no scan work.
./probe scan run \
  --engagement-id "$EID" \
  --use-case uc_discovery_only \
  --target "1.1.1.1" \
  --wait \
  --json

# OT profile should block active use-cases.
OT_EID=$(./probe engagements create \
  --name "OT safety gate lab" \
  --scope "<WINDOWS_IP>/32" \
  --scan-profile ot \
  --json | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

./probe scan run \
  --engagement-id "$OT_EID" \
  --use-case uc_web_app_triage \
  --target "<WINDOWS_IP>" \
  --json
```

Expected:

- Out-of-scope targets are rejected by the probe scope guard.
- Active scans on `scan_profile=ot` are blocked by the manager.

---

## 4. Build or publish the probe image

For internal production testing:

```bash
cd probe
docker build -t registry.example.com/vedha-probe:2.0.0 .
docker push registry.example.com/vedha-probe:2.0.0
```

For customer distribution, use the sealed image flow:

```bash
cd probe
python3 tools/issue_license.py keygen

docker build -f Dockerfile.sealed \
  -t registry.example.com/vedha-probe:2.0.0-sealed \
  --build-arg PROBE_LICENSE_PUBKEY=<vendor-public-key-hex> \
  .

docker push registry.example.com/vedha-probe:2.0.0-sealed
```

Keep the vendor private key off the manager and off client machines.

If licensing is enforced, get the target host ID before final install:

```bash
docker volume create vedha-probe-state
docker run --rm \
  -v vedha-probe-state:/var/lib/vedha-probe \
  registry.example.com/vedha-probe:2.0.0-sealed hostid
```

Issue a license from the vendor machine:

```bash
cd probe
python3 tools/issue_license.py issue \
  --hostid <host-id-from-client> \
  --customer "<customer-name>" \
  --days 365
```

---

## 5. Prepare the production probe host

Pick a small Linux host inside the client network.

Requirements:

- Docker Engine.
- Outbound HTTPS to the manager.
- Routing to approved target CIDRs.
- Correct system time/NTP.
- Enough CPU/RAM for concurrent TCP connections.
- No inbound firewall rule required for the probe.

For normal IT scans, Docker bridge networking is enough if the host can route to
the target networks. For OT passive discovery, prefer native install or Docker
with Linux host networking so multicast/broadcast announcements are visible:

```bash
--network host
```

---

## 6. Run the production probe

On the probe host:

For the normal Python image built from `probe/Dockerfile`, do not append a
command after the image name. The image already has the correct `CMD`.

Recommended production defaults:

```env
PLATFORM_URL=https://manager.example.com
VERIFY_TLS=true
OPERATOR_TOKEN=vpat_xxx
HEARTBEAT_INTERVAL=30
POLL_INTERVAL=10
JOB_LIMIT=1
RESULT_SPOOL_DIR=/var/lib/vedha-probe/spool
RESULT_COMPRESS_OVER=1048576
```

Create and store the PAT with the CLI when running a native probe:

```bash
cd probe
./probe auth login --manager https://manager.example.com --pat "vpat_xxx"
./probe daemon run \
  --name prod-dmz-probe-01 \
  --location client-dmz \
  --segment 10.10.20.0/24
```

For containerized probes, pass the same PAT as `OPERATOR_TOKEN`. The token must
have `probe:register`; scan dispatch also needs the manager-side operator PAT to
have the normal route role and scopes.

```bash
docker volume create vedha-probe-state

docker run -d --name vedha-probe \
  --restart unless-stopped \
  -e PLATFORM_URL="https://manager.example.com" \
  -e VERIFY_TLS=true \
  -e OPERATOR_TOKEN="vpat_xxx" \
  -e PROBE_NAME="prod-dmz-probe-01" \
  -e PROBE_LOCATION="client-dmz" \
  -e PROBE_NETWORK_SEGMENTS="10.10.20.0/24" \
  -e HEARTBEAT_INTERVAL=30 \
  -e POLL_INTERVAL=10 \
  -e JOB_LIMIT=1 \
  -v vedha-probe-state:/var/lib/vedha-probe \
  registry.example.com/vedha-probe:2.0.0
```

If using a private CA:

```bash
docker run -d --name vedha-probe \
  --restart unless-stopped \
  -e PLATFORM_URL="https://manager.example.com" \
  -e VERIFY_TLS=true \
  -e PROBE_CA_BUNDLE=/etc/vedha/ca.pem \
  -e OPERATOR_TOKEN="vpat_xxx" \
  -e PROBE_NAME="prod-dmz-probe-01" \
  -e PROBE_NETWORK_SEGMENTS="10.10.20.0/24" \
  -e HEARTBEAT_INTERVAL=30 \
  -e POLL_INTERVAL=10 \
  -e JOB_LIMIT=1 \
  -v /etc/vedha/ca.pem:/etc/vedha/ca.pem:ro \
  -v vedha-probe-state:/var/lib/vedha-probe \
  registry.example.com/vedha-probe:2.0.0
```

If using mTLS:

```bash
docker run -d --name vedha-probe \
  --restart unless-stopped \
  -e PLATFORM_URL="https://manager.example.com" \
  -e VERIFY_TLS=true \
  -e PROBE_CA_BUNDLE=/etc/vedha/ca.pem \
  -e PROBE_CLIENT_CERT=/etc/vedha/probe.crt \
  -e PROBE_CLIENT_KEY=/etc/vedha/probe.key \
  -e OPERATOR_TOKEN="vpat_xxx" \
  -e PROBE_NAME="prod-dmz-probe-01" \
  -e PROBE_NETWORK_SEGMENTS="10.10.20.0/24" \
  -v /etc/vedha/ca.pem:/etc/vedha/ca.pem:ro \
  -v /etc/vedha/probe.crt:/etc/vedha/probe.crt:ro \
  -v /etc/vedha/probe.key:/etc/vedha/probe.key:ro \
  -v vedha-probe-state:/var/lib/vedha-probe \
  registry.example.com/vedha-probe:2.0.0
```

If using the sealed image with license enforcement, append `run` because
`Dockerfile.sealed` uses the probe binary as `ENTRYPOINT`:

```bash
docker run -d --name vedha-probe \
  --restart unless-stopped \
  -e PLATFORM_URL="https://manager.example.com" \
  -e VERIFY_TLS=true \
  -e OPERATOR_TOKEN="vpat_xxx" \
  -e PROBE_NAME="prod-dmz-probe-01" \
  -e PROBE_LICENSE="<license-token>" \
  -e PROBE_NETWORK_SEGMENTS="10.10.20.0/24" \
  -e HEARTBEAT_INTERVAL=30 \
  -e POLL_INTERVAL=10 \
  -e JOB_LIMIT=1 \
  -v vedha-probe-state:/var/lib/vedha-probe \
  registry.example.com/vedha-probe:2.0.0-sealed run
```

For lab/dev only, licensing can be disabled:

```bash
-e LICENSE_ENFORCED=false
```

Do not use that for customer distribution.

---

## 7. Verify the probe is online

On the probe host:

```bash
docker logs -f vedha-probe
```

Expected healthy sequence:

```text
Vedha Probe
Registered as 'prod-dmz-probe-01'
Capabilities: ai_service_discovery, assessment, ...
Use-case library: uc_ai_endpoint_sweep, ...
Attempting WebSocket push mode...
Waiting for scan jobs
```

From the manager API:

```bash
BASE="https://manager.example.com"

TOKEN=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"<email>","password":"<password>"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

# Production-preferred: mint a revocable PAT once, then use that as TOKEN.
TOKEN=$(curl -s -X POST "$BASE/auth/personal-access-tokens" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "prod-probe-cli",
    "expires_in_days": 90,
    "scopes": [
      "probe:read",
      "probe:write",
      "probe:register",
      "engagement:read",
      "engagement:write"
    ]
  }' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

curl -s "$BASE/agents" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool

curl -s "$BASE/agents/use-cases" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

Check:

- Probe status is online.
- Capabilities include `assessment`, `web_scan`, `tls_scan`, `mcp_discovery`, `snmp_scan`.
- `network_segments` matches the network the probe can actually reach.

---

## 8. Create the production engagement

Start with one safe host, not the whole range.

```bash
EID=$(curl -s -X POST "$BASE/engagements" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Client production first probe run",
    "scope_cidrs": ["10.10.20.42/32"],
    "excluded_cidrs": [],
    "rules_of_engagement": {
      "scan_profile": "it",
      "change_window": "approved production window",
      "notes": "First run: one non-critical host only"
    }
  }' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

echo "$EID"
```

For OT/ICS, create the engagement as passive-only:

```json
"rules_of_engagement": {
  "scan_profile": "ot"
}
```

The manager blocks active scan types on `scan_profile=ot`. The probe also uses
the OT profile to avoid active probing.

---

## 9. First production run: discovery only

Use low intensity for the first run.

This is on-demand. The probe is online before this step, but it does not scan
until this job is queued by the manager.

```bash
JOB_ID=$(curl -s -X POST "$BASE/agents/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"engagement_id\": \"$EID\",
    \"job_type\": \"discovery\",
    \"use_case_id\": \"uc_discovery_only\",
    \"params\": {
      \"targets\": [\"10.10.20.42\"],
      \"rate\": 25,
      \"concurrency\": 10,
      \"timeout\": 2,
      \"disc_timeout\": 1.5
    }
  }" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["job_id"])')

echo "$JOB_ID"
```

Poll status:

```bash
watch -n 5 "curl -s '$BASE/agents/jobs/$JOB_ID' -H 'Authorization: Bearer $TOKEN' | python3 -m json.tool"
```

Probe log should show:

```text
Job <id> done - discovery
```

If this produces unexpected traffic volume, stop here and tune before expanding.

---

## 10. Confirm facts landed in the manager

Check job status:

```bash
curl -s "$BASE/agents/jobs/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

Check promoted assets:

```bash
curl -s "$BASE/engagements/$EID/assets" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

Check engagement scope as the probe sees it:

```bash
curl -s "$BASE/engagements/$EID/scope" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool
```

Expected:

- Job moves `pending -> running -> completed`.
- Assets/services appear for in-scope targets only.
- No excluded CIDR appears in assets or services.
- Probe logs show `Job <id> done` or the WebSocket equivalent.
- If result upload fails temporarily, the probe keeps the result in
  `RESULT_SPOOL_DIR` and retries.

---

## 11. Expand safely

After the single-host discovery is clean, use this order.

### 11.1 Service-specific scan on the same host

Web/TLS example:

```bash
curl -s -X POST "$BASE/agents/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"engagement_id\": \"$EID\",
    \"job_type\": \"discovery\",
    \"use_case_id\": \"uc_web_app_triage\",
    \"params\": {
      \"targets\": [\"10.10.20.42\"],
      \"rate\": 25,
      \"concurrency\": 10,
      \"timeout\": 3
    }
  }"
```

SNMP example for network devices:

```bash
curl -s -X POST "$BASE/agents/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"engagement_id\": \"$EID\",
    \"job_type\": \"discovery\",
    \"use_case_id\": \"uc_snmp_exposure\",
    \"params\": {
      \"targets\": [\"10.10.20.42\"],
      \"rate\": 10,
      \"concurrency\": 5,
      \"timeout\": 3
    }
  }"
```

### 11.2 Full assessment on the same host

```bash
curl -s -X POST "$BASE/agents/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"engagement_id\": \"$EID\",
    \"job_type\": \"discovery\",
    \"use_case_id\": \"uc_full_assessment\",
    \"params\": {
      \"targets\": [\"10.10.20.42\"],
      \"rate\": 50,
      \"concurrency\": 25,
      \"timeout\": 3,
      \"disc_timeout\": 1.5
    }
  }"
```

### 11.3 Small range

Patch the engagement scope to a small approved range:

```bash
curl -s -X PATCH "$BASE/engagements/$EID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scope_cidrs": ["10.10.20.32/28"],
    "excluded_cidrs": ["10.10.20.33/32"]
  }' \
  | python3 -m json.tool
```

Run discovery:

```bash
curl -s -X POST "$BASE/agents/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"engagement_id\": \"$EID\",
    \"job_type\": \"discovery\",
    \"use_case_id\": \"uc_discovery_only\",
    \"params\": {
      \"targets\": [\"10.10.20.32/28\"],
      \"rate\": 50,
      \"concurrency\": 25,
      \"timeout\": 2
    }
  }"
```

### 11.4 Approved production CIDR

Only after the small range is clean:

```bash
curl -s -X PATCH "$BASE/engagements/$EID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scope_cidrs": ["10.10.20.0/24"],
    "excluded_cidrs": ["10.10.20.1/32", "10.10.20.10/32"]
  }' \
  | python3 -m json.tool
```

Then run either `uc_discovery_only` or `uc_full_assessment` depending on the
approved test plan.

---

## 12. OT/ICS passive production run

For OT, do not use discovery, full assessment, web, SMB, DB, UDP, SNMP, or MCP
active use-cases.

Create or patch the engagement:

```bash
curl -s -X PATCH "$BASE/engagements/$EID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scope_cidrs": ["10.50.0.0/24"],
    "excluded_cidrs": [],
    "rules_of_engagement": {
      "scan_profile": "ot"
    }
  }'
```

Run passive discovery:

```bash
curl -s -X POST "$BASE/agents/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"engagement_id\": \"$EID\",
    \"job_type\": \"discovery\",
    \"use_case_id\": \"uc_ot_passive\",
    \"params\": {
      \"targets\": [\"10.50.0.0/24\"],
      \"passive_listen_seconds\": 300
    }
  }"
```

For OT passive collection:

- Put the probe on a SPAN/mirror port or TAP.
- Prefer native run or Docker `--network host`.
- Increase `passive_listen_seconds` if the segment is quiet.
- Treat "no hosts observed" as "no announcements heard", not as "network empty".

---

## 13. Production tuning presets

Use low settings first. The probe clamps unsafe values, but operators should
still choose production-safe values.

| Environment | rate | concurrency | timeout | Notes |
|---|---:|---:|---:|---|
| First prod host | 25 | 10 | 2-3s | Safest active start |
| Normal LAN /24 | 50-200 | 25-100 | 2-5s | Watch IDS and network load |
| High-latency WAN | 25-75 | 10-50 | 5-10s | Avoid false negatives |
| Fragile/legacy IT | 10-25 | 5-10 | 3-5s | Avoid deep scans first |
| OT/ICS | n/a | n/a | n/a | Passive only |

Avoid this on the first production run:

- Whole enterprise ranges.
- Internet-wide targets.
- High concurrency.
- Active scans against PLCs, RTUs, safety systems, medical devices, or fragile appliances.
- Running during business peak unless explicitly approved.

---

## 14. What to monitor during a live run

Probe host:

```bash
docker logs -f vedha-probe
docker stats vedha-probe
docker inspect vedha-probe --format '{{.State.Status}}'
```

Manager host:

```bash
docker compose logs -f api worker
docker compose ps
```

API:

```bash
curl -s "$BASE/agents" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
curl -s "$BASE/agents/jobs/$JOB_ID" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Network/security team:

- Firewall/IDS alert volume.
- Unexpected blocked destinations.
- Target CPU/network spikes.
- Any service instability on target segments.

Stop immediately if production systems show instability.

---

## 15. Stop, rollback, or decommission

Pause scanning:

```bash
docker stop vedha-probe
```

Start again:

```bash
docker start vedha-probe
```

Remove the running container but keep identity/state:

```bash
docker rm -f vedha-probe
docker volume inspect vedha-probe-state
```

Full decommission, including local identity and spooled results:

```bash
docker rm -f vedha-probe
docker volume rm vedha-probe-state
```

Do not remove the volume during normal restarts. Keeping it prevents duplicate
agent registrations and keeps result spooling durable.

---

## 16. Troubleshooting

### Probe says manager unreachable

Check:

```bash
docker exec vedha-probe sh -c 'getent hosts manager.example.com || true'
docker logs vedha-probe --tail 100
```

Common causes:

- Probe host cannot resolve manager DNS.
- Firewall blocks outbound 443.
- `PLATFORM_URL` is wrong.
- Manager TLS certificate is not trusted.
- Private CA not mounted with `PROBE_CA_BUNDLE`.

### Probe says manager rejected sign-in

Check:

- `OPERATOR_TOKEN` starts with `vpat_` and was copied completely.
- The PAT is not expired or revoked.
- PAT scopes include `probe:register`.
- PAT role allows agent registration: admin or manager.
- The token belongs to the correct tenant.

### Probe online but job stays pending

Check:

```bash
curl -s "$BASE/agents" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
curl -s "$BASE/agents/jobs/$JOB_ID" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
docker logs vedha-probe --tail 200
```

Common causes:

- Probe cannot poll the manager.
- Job targets are outside engagement scope.
- OT engagement was given an active use-case.
- Probe is busy with another job. `JOB_LIMIT` defaults to `1`.

### Job completes but no assets appear

Common causes:

- Target is down or unreachable from the probe host.
- Firewall drops probe traffic.
- Scope or exclusions removed the target.
- Timeout too low for the network path.
- Passive OT segment has no visible announcements.

### Duplicate probe rows appear

The probe state volume was probably deleted or not mounted. Re-run with:

```bash
-v vedha-probe-state:/var/lib/vedha-probe
```

### OT passive sees nothing

Check:

- Probe is connected to the right switch port.
- SPAN/mirror/TAP is configured.
- Docker host networking is used, or run natively.
- `passive_listen_seconds` is long enough.

---

## 17. Local production-like smoke test

Use this only before real production.

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner"
cp .env.docker.example .env
docker compose --profile probe --profile ui up -d --build
docker compose logs -f probe
```

This starts an in-stack local probe with:

```text
PLATFORM_URL=http://api:8000
LICENSE_ENFORCED=false
```

That is good for smoke testing the manager/probe flow, not for customer
production deployment.

---

## 18. Standalone scanner validation

Use standalone validation when you want to prove scanner accuracy before a live
manager-dispatched run.

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/probe"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -q
```

Create a tiny scope and run the workflow directly:

```bash
printf '127.0.0.1/32\n' > scope.txt
python3 -m workflow.cli \
  -t 127.0.0.1 \
  -s scope.txt \
  --profile it \
  --mode assessment \
  -o /tmp/probe-assessment.json
```

Service-specific examples:

```bash
python3 -m workflow.cli -t 127.0.0.1 -s scope.txt --profile it --mode service-specific --services web tls
python3 -m workflow.cli -t 127.0.0.1 -s scope.txt --profile it --mode service-specific --services snmp
python3 -m workflow.cli -t 127.0.0.1 -s scope.txt --profile it --mode service-specific --services mcp_ai
```

Scope safety check:

```bash
python3 -m scanner.port_scanner -t 203.0.113.10 -s scope.txt -v
```

Expected: out-of-scope refusal before any scan packet.

---

## 19. Production success criteria

A production probe run is successful only if all are true:

- Probe is online and heartbeating.
- Capability list is current and includes the intended use-case.
- Engagement scope and exclusions match written authorization.
- First job completes on one safe host.
- Facts land in the manager.
- Assets/services are promoted.
- No out-of-scope assets appear.
- Target owners report no instability.
- Full-range scan is run only after the controlled rollout succeeds.
