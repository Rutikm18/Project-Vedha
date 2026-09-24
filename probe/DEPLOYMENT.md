# Vedha — Split Deployment (Manager in cloud, Probe on-prem)

Vedha runs as **two independent deployments**:

| Component | Where it runs | Compose file | Reaches |
|-----------|---------------|--------------|---------|
| **Manager** | Your cloud (VM / AWS) | `manager/docker-compose.yml` (behind Caddy TLS) | Nothing outbound to the probe |
| **Probe** | Inside the customer network | `probe/docker-compose.yml` | Dials **out** to the Manager; scans the local LAN |

```
   Customer network (on-prem)                         Your cloud
 ┌───────────────────────────┐                   ┌──────────────────────────┐
 │  vedha-agent (container)  │                   │  Caddy :80/:443 (TLS)    │
 │   scans 10.0.0.0/24 …     │ ==HTTPS/WSS 443==▶ │    └─▶ api :8000          │
 │   NO inbound listener     │   (dial-out only) │    worker, postgres,      │
 └───────────────────────────┘                   │    redis, neo4j, frontend │
                                                  └──────────────────────────┘
```

The probe **never accepts an inbound connection** — it opens a single outbound
HTTPS connection to the Manager and receives jobs over that channel (WebSocket
push, HTTP long-poll fallback). Results are pushed back over the same connection.
This is the key property: **connecting a probe adds zero inbound attack surface
to the customer network.**

---

## 1. Manager (cloud)

```bash
# on the cloud host
cp .env.example .env          # set JWT_SECRET, DB creds, MANAGER_PUBLIC_URL, domain
cd manager && docker compose up -d      # postgres, redis, neo4j, migrate, api, worker, frontend
# TLS + public domain are provisioned by Caddy (see deploy/aws/install.sh)
```

Public entrypoint: `https://manager.your-domain.com` (Caddy on 443 → `api:8000`).
That URL is what every probe uses as `PLATFORM_URL`.

## 2. Probe (customer network) — one command, zero secrets

The probe is a thin executor: give it the **Manager address** and nothing else.
Auth (token), per-job **scope**, and **use-cases** are all governed by the Manager.

**Simplest — fully automatic (single-owner fleets):** if the Manager runs with
`PROBE_AUTO_ENROLL=true` (the AWS testing deploy sets this by default via
`gen-env`), a probe **auto-connects with nothing but the Manager IP** — no token,
no PAT, no approval:
```bash
./install.sh 13.127.147.205
```
The probe generates its own keypair (that's its id), the Manager **auto-approves**
it and issues an agent token, and it starts polling. Every auto-enrollment is
written to the Manager audit log. (Turn it off — `PROBE_AUTO_ENROLL=false` — for
untrusted networks; then use one of the flows below.)

**Zero-touch pairing (approval-gated — no token to copy):**
```bash
./install.sh <manager-ip> --enroll     # e.g. ./install.sh 13.127.147.205 --enroll
```
The probe generates its own keypair and prints a short **pairing code**:
```
══════════════════════════════════════════════════════════
  PROBE PAIRING REQUIRED — approve to start scanning
══════════════════════════════════════════════════════════
   1) Open this URL : http://13.127.147.205:18080/fleet/enroll
   2) Enter code    : A7BQ-9KFP
══════════════════════════════════════════════════════════
```
Open the dashboard, enter/approve the code, and the probe **activates itself and
starts scanning** — the Manager issues the token only after you approve, and no
secret is ever copy-pasted. (This is the OAuth device-flow / Tailscale model.)

**Alternatives:**
```bash
./install.sh <manager-ip>              # use a PAT already saved in probe.env
./install.sh <manager-ip> <enroll-token>   # pre-authorized, site-bound token (auto-approve)
```

`install.sh` normalizes a bare IP to `http://<ip>:18080` (pass a full `https://…`
URL for a TLS Manager), **auto-detects this host's /24** as the local scan-ceiling,
creates the state dir, and launches the agent. Run detached with
`nohup ./install.sh <ip> --enroll &`. Docker alternative: comment the host
`STATE_FILE`/`RESULT_SPOOL_DIR` in probe.env, then `docker compose up -d`.

**Verify the probe came online** (any install path):
```bash
docker compose logs -f probe        # containerized install
#   ↳ look for:  "Registered as '<name>'."
#                "WebSocket connected. Push mode active — waiting for jobs."
```
The startup banner also prints the resolved scan ceilings and, importantly,
**`SYN scan: yes|no`** — `no` means the probe will connect-scan wide sweeps (see
§4). In the dashboard, **Settings → Probe Fleet** shows the probe online within
~30s. If it exits immediately, the two usual causes are an empty
`PROBE_NETWORK_SEGMENTS` (fail-closed — it refuses every job) or an unreachable
`PLATFORM_URL`.

### Local all-in-one (one host, for testing only)

To try the whole platform plus a probe on a single machine, use the repo-root
compose targets instead of the split deployment above:

```bash
cp .env.docker.example .env          # set JWT_SECRET + SEED_ADMIN_PASSWORD
make run                             # api + worker + a self-registering probe (no dashboard)
#   or: make dev                     # + the Next.js dashboard on :3000
docker compose -p vedha logs -f probe    # watch it register
```
(`make full` and `make up` are **probe-free** — they run only the platform.)

The in-stack probe registers with the seed operator credentials automatically —
no PAT or enrollment needed. This path shares the customer network's routing, so
it is for validation, never a production deployment.

---

## 3. Firewall / ports the organization must open

### Probe side (customer egress) — the only rule you need from the org

| Direction | Port | Proto | Destination | Why |
|-----------|------|-------|-------------|-----|
| **Outbound** | **443** | TCP | `manager.your-domain.com` | REST **and** WebSocket (WSS) — the entire control + result channel, multiplexed on one port |
| Outbound | 53 | UDP/TCP | DNS resolver | Resolve the Manager domain |
| **Inbound** | — | — | — | **NONE.** The probe never listens. |
| Outbound (LAN) | scan ports | TCP/UDP | `PROBE_NETWORK_SEGMENTS` | The probe scanning the customer's own assets — internal traffic, not to the Manager |

> One outbound 443 rule to a single hostname is all IT/security needs to approve.
> If egress is via a proxy, set `HTTPS_PROXY` in `probe.env` (the REST path honors
> it); if the proxy can't carry WebSockets, set `PROBE_WS_ENABLED=false` and the
> probe long-polls over HTTPS through the proxy instead.

### Manager side (cloud security group / firewall)

| Direction | Port | Proto | Source | Why |
|-----------|------|-------|--------|-----|
| Inbound | **443** | TCP | probe public egress IP(s) **+** operator browsers | HTTPS REST + WSS (probe control **and** the dashboard) |
| Inbound | 80 | TCP | `0.0.0.0/0` | Caddy HTTP→HTTPS redirect + Let's Encrypt ACME challenge |
| Inbound | 22 | TCP | admin IPs only | SSH administration (optional) |
| **Internal only** | 5432 / 6379 / 7687 / 8000 / 3000 | TCP | compose network | postgres / redis / neo4j / api / frontend — **never expose publicly**; Caddy is the only front door |

Lock inbound 443 down to the customer's known egress IP range plus your operators
where possible. Everything else (database, cache, graph, the raw API) stays on the
internal Docker network and is unreachable from the internet.

---

## 4. Running scans — the numeric use-case protocol

You never configure use-cases on the probe. The **Manager** dispatches a job by a
compact **number**; the probe maps that number to exactly one scan pipeline and
runs only that. Two knobs:

- **`uc`** — use-case code (what to scan)
- **`intensity`** — `1` light · `2` standard · `3` deep (how hard: port breadth +
  rate/timeout/retries). A code or a name is accepted; omit to use the use-case default.

| `uc` | Use-case | | `uc` | Use-case |
|------|----------|-|------|----------|
| `1`  | Host discovery | | `50` | SNMP exposure |
| `2`  | Device inventory | | `51` | UDP service exposure |
| `10` | Full assessment | | `60` | IoT / embedded survey |
| `11` | Re-scan (delta) | | `61` | AI / MCP endpoints |
| `20` | Web + TLS triage | | `70` | OT / ICS passive |
| `21` | Web-app triage | | `80` | Full-port audit |
| `30` | Windows / SMB estate | | `81` | Multi-vantage exposure |
| `40` | Database exposure | | | |

Discover them live: `GET /agents/use-cases` (each entry carries its `code`) and
`GET /agents/intensities`.

**Dispatch a scan** (Manager governs scope from the engagement — you send targets):

```bash
# a deep full-port audit (uc=80, intensity=3) of a target in the engagement
curl -sS -X POST "$MANAGER/agents/jobs" \
  -H "Authorization: Bearer $PAT" -H 'Content-Type: application/json' \
  -d '{
        "engagement_id": "…",
        "uc": 80,
        "intensity": 3,
        "params": { "targets": ["192.168.1.0/24"] }
      }'
```

The Manager validates the code, injects the engagement's authoritative scope, and
pushes `{ "uc": 80, "intensity": 3, "scope_cidrs": […], "targets": […] }` to the
probe over the existing WebSocket. The probe resolves `80 → full_port_audit`,
`3 → deep`, runs it inside the scope, and streams facts back. (String `use_case_id`
still works for backward compatibility; the number is the compact interface.)

> **Deep / aggressive full-port scans need raw SYN.** `intensity: 3` (deep, the
> dashboard's "Aggressive") and the full-port audit sweep all 65,535 TCP ports.
> The probe uses a stateless raw-SYN scanner for that, which requires
> `network_mode: host` **and** `cap_add: [NET_RAW, NET_ADMIN]` (the commented
> block in `probe/docker-compose.yml`). The default hardened container drops all
> capabilities, so it falls back to a `connect()` scan — which cannot finish
> 65,535 ports per host inside the job's time budget. When that happens the
> unreached ports are reported **`not_scanned`** (never `filtered`, so coverage
> stays honest) and the scan is admitted and completed on its high-signal first
> pass. Grant the raw-socket profile on any probe expected to run deep or
> full-port scans; the startup banner's `SYN scan: yes` confirms it is active.
>
> A deep scan is also two-phase and partial-safe: each host's first-pass
> assessment is committed to the Manager as the scan runs, so a job that is
> cancelled or hits its runtime ceiling during the port tail keeps the hosts it
> already finished.

## 5. TLS notes

- **Public CA (default):** Caddy auto-provisions a Let's Encrypt cert for your
  domain. Probes trust it out of the box (`VERIFY_TLS=true`).
- **Private/internal CA:** mount the CA PEM into the probe and set
  `PROBE_CA_BUNDLE=/etc/vedha/ca.pem` (see the commented volume in
  `probe/docker-compose.yml`). Never set `VERIFY_TLS=false` in production.
- **mTLS (optional hardening):** issue the probe a client cert
  (`PROBE_CLIENT_CERT` / `PROBE_CLIENT_KEY`) so the Manager authenticates the
  probe at the TLS layer in addition to its token.
