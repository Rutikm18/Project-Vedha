# Production Deployment & First Real Assessment — End to End

Deploy the manager, deploy the probe **inside the network you're authorized to assess**, run a
**real scan against real targets**, and get **real findings** from the real detection pipeline.
Every stage has a **⏱ performance checkpoint**.

> This is a **production** runbook — no test containers, no demo targets, no seeded data.

---

## 0. "Real findings" — what actually produces them (read first)

```
Probe (real scan of authorized targets)
   → raw facts → Manager backend → detection engine (facts → CVEs, CVSS/KEV/EPSS)
   → findings persisted in Postgres → dashboard Findings (Priority Queue)
```

- **Findings are real.** The dashboard's `/api/findings` is a thin proxy to the FastAPI backend
  (single source of truth); the seeder creates **only the admin account — never any findings.**
  So the database starts empty of findings, and everything you see comes from an actual scan.
- **Two things that are NOT real yet — know this before you rely on them:**
  - **AI Brain page** is still hardcoded mock (pending the OpenRouter wiring). Don't present its
    output as assessment results.
  - **Attack-path graph** ships a demo module (`manager/backend/app/graph/demo.py`). Keep
    `NEO4J_ENABLED` off / ignore the graph demo for a real engagement.
- **Highest-fidelity findings need authenticated inventory** (SSH/WinRM creds) — unauthenticated
  scanning gives thin, version-poor data. See Stage 6.

---

## 1. Production topology

```
  Operator ──► Dashboard/API  (manager, on a server, behind TLS)
                     ▲  outbound-only
                     │
        Probe (deployed INSIDE the client/target network) ──► scans authorized targets
```

The manager runs on a server you control (cloud VM or on-prem). The probe is deployed **remotely,
inside the network under assessment** — it dials **out only** to the manager. They are **not** on
the same host in production.

---

## 2. Manager — deploy (production)

On the **manager server**:

```bash
cd <repo>
cp .env.docker.example .env
```

Edit `.env` for production — **do not ship the defaults**:

| Var | Set to |
|---|---|
| `JWT_SECRET` | a long random secret (`openssl rand -hex 32`) |
| `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD` | your real admin + a strong password |
| `POSTGRES_PASSWORD` | a strong DB password |
| `ANTHROPIC_API_KEY` | your key (for AI reporting; optional) |
| `API_PORT` / `FRONTEND_PORT` | as needed (default `18080` / `3000`) |

Bring up the manager (**`up`, not `full`** — the probe is deployed separately in the target
network, not as a local container):

```bash
time make up          # postgres + redis + migrate + api + dashboard
make ps               # all services Up / healthy
```

**Put it behind TLS.** The probe warns/should not send an agent token or scan results over plain
`http` to a non-local manager. Terminate TLS with a reverse proxy (Caddy/nginx/traefik) in front
of `FRONTEND_PORT` and `API_PORT`, so the manager is reachable as `https://vedha.<your-domain>`.

**⏱ Record:** `time make up` (cold/warm). Verify:
```bash
curl -s -o /dev/null -w "API → HTTP %{http_code} · %{time_total}s\n" https://vedha.<domain>/docs
```
✅ Pass: `make ps` healthy; dashboard loads at `https://vedha.<domain>`; API `/docs` returns `200`.

---

## 3. Manager — first login + a probe token

Log in to the dashboard, change the admin password. Then mint a **scoped PAT** for the probe
(production-preferred over an operator password). Via API:

```bash
BASE=https://vedha.<domain>
curl -s -o /tmp/login.json -w "login → HTTP %{http_code} · %{time_total}s\n" \
  -X POST $BASE/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"<admin-email>","password":"<admin-password>"}'
TOKEN=$(python3 -c 'import json;print(json.load(open("/tmp/login.json"))["access_token"])')
```
Create the PAT in the dashboard (Settings) or via the API, and keep it for Stage 4.

---

## 4. Probe — deploy inside the target network (production)

On a host **inside the network to be assessed** (per `PROBE_RUNBOOK.md §B`):

```bash
# 1) Host ID (no install needed)
docker run --rm registry.<your-registry>/vedha-probe:1.0 hostid      # → send this to the vendor/you

# 2) Issue a license bound to that host (on your trusted machine)
python3 probe/tools/issue_license.py issue --hostid <id> --customer "<Client>" --days 365

# 3) Install — dials OUT only, no inbound ports
curl -fsSL https://vedha.<domain>/install.sh -o install.sh && less install.sh   # inspect first
PROBE_IMAGE=registry.<your-registry>/vedha-probe:1.0 \
PLATFORM_URL=https://vedha.<domain> \
OPERATOR_TOKEN=<the PAT from Stage 3> \
PROBE_LICENSE=<token from step 2> \
sh install.sh

docker logs -f vedha-probe        # watch: license OK → Registered as … → polling
```

**Verify online:** dashboard **Scanner** page shows the probe **ONLINE**, or:
```bash
curl -s $BASE/agents -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**⏱ Registration latency:** install → first `online` heartbeat (probe log timestamps).
✅ Pass: probe `online`, recent heartbeat, dialing out over `https`.

---

## 5. Engagement — the authorized scope (Rules of Engagement)

Create the engagement with the client's **actual authorized CIDRs**. This is the legal boundary —
the probe refuses everything outside it.

```bash
curl -s -o /tmp/eng.json -X POST $BASE/engagements \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"<Client> — <Quarter>","scope_cidrs":["<AUTHORIZED_CIDR_1>","<AUTHORIZED_CIDR_2>"]}'
EID=$(python3 -c 'import json;print(json.load(open("/tmp/eng.json"))["id"])')
```
Or use the dashboard **Engagements → New**. Double-check the scope matches your written
authorization before scanning.

---

## 6. Run the real assessment ⏱

Drive from the dashboard **Scanner** page (pick the engagement, use-case, and targets ⊆ scope),
**or** via API. Start with discovery, then a full assessment.

```bash
# Discovery first — confirm what's live and reachable
date +%s > /tmp/t0
curl -s -X POST $BASE/agents/jobs -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"engagement_id\":\"$EID\",\"job_type\":\"discovery\",
       \"params\":{\"scan_type\":\"discovery\",\"targets\":[\"<AUTHORIZED_RANGE>\"],\"scope_cidrs\":[\"<AUTHORIZED_CIDR>\"]}}"

# Full assessment — the funnel across all service branches
curl -s -X POST $BASE/agents/jobs -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"engagement_id\":\"$EID\",\"job_type\":\"discovery\",
       \"params\":{\"scan_type\":\"assessment\",\"targets\":[\"<AUTHORIZED_RANGE>\"],\"scope_cidrs\":[\"<AUTHORIZED_CIDR>\"]}}"
```

**For real CVE fidelity, add authenticated inventory** (the accurate version data source) — supply
credentials in the job params so the probe reads installed packages/KBs:
```jsonc
"params": { "scan_type": "assessment", "targets": ["<host>"], "scope_cidrs": ["<cidr>"],
            "ssh_creds": { "user": "audit", "key_path": "/keys/audit" },      // Linux
            "win_creds": { "user": "audit", "domain": "CORP" } }              // Windows (WinRM)
```

Watch it run (scope-enforced, one job at a time): dashboard Scanner status live, or
`docker logs -f vedha-probe`.

**⏱ Scan duration** (enqueue → `done`) and **throughput** (hosts ÷ minutes).
✅ Pass: probe logs show scope enforcement + a submitted result; job reaches `done`; **nothing
outside scope was contacted.**

---

## 7. Real findings ⏱

On submit, the backend ingests facts → detection engine → **real findings** persisted to the DB.

```bash
curl -s "$BASE/findings?engagement_id=$EID" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -40
echo "scan+detect elapsed: $(( $(date +%s) - $(cat /tmp/t0) ))s"
```
**Dashboard → Findings:** the **Priority Queue** surfaces actively-exploited / KEV / SLA-breached
first; each finding opens to Threat-Intel / Evidence / Remediation / Compliance tabs — all driven
by real detection output (CVE, CVSS, KEV, EPSS).

**⏱ Detection latency:** submit → findings visible.
✅ Pass: findings returned by the API and shown on the dashboard, ranked by real risk. If the scope
was quiet you may get few/none — that is a **real** result, not a bug.

---

## 8. Performance checkpoints (fill in)

| Metric | How | Result |
|---|---|---|
| Manager boot (cold/warm) | `time make up` | ___ |
| API latency | `curl -w "%{time_total}"` on `/docs` | ___ |
| Probe registration | install → `online` | ___ |
| Scan duration | enqueue → `done` | ___ |
| Throughput | hosts ÷ scan minutes | ___ |
| Detection latency | submit → findings | ___ |
| Resource use (during scan) | `docker stats` on the manager + probe hosts | ___ |
| Dashboard load | browser DevTools → Network (Findings) | ___ |

---

## 9. Production hardening checklist

- [ ] TLS in front of API + dashboard (probe talks `https` only)
- [ ] Strong `JWT_SECRET`, DB password, admin password (no `.env.docker.example` defaults)
- [ ] Postgres volume backed up (`pgdata`) — findings and evidence live here
- [ ] Probe deployed with a **license** + scoped **PAT** (not an operator password)
- [ ] `NEO4J_ENABLED` off unless you're using a real (non-demo) attack graph
- [ ] Scope (`scope_cidrs`) matches written authorization for every engagement
- [ ] Log retention on api/worker/probe; alerting on probe offline
- [ ] AI keys set only if using AI reporting; AI Brain treated as not-yet-real

---

## 10. Ongoing ops & teardown

```bash
make ps                     # service health
docker compose logs -f api worker      # backend + detection
docker logs -f vedha-probe             # probe (in the target network)
make down                   # stop manager, keep the database
make clean                  # stop AND wipe volumes (destroys findings) — use with care
```

---

## 11. Troubleshooting

| Symptom | Fix |
|---|---|
| Probe won't register | check `PLATFORM_URL` is the public `https` manager URL; license valid; `docker logs vedha-probe` |
| Probe warns about plain http | put the manager behind TLS; the probe should not ship tokens/results over `http` to a remote manager |
| Scan refused / 0 targets | target not in `scope_cidrs` — the probe **correctly** refuses out-of-scope; fix scope or target |
| No findings after `done` | `docker compose logs worker api` — confirm facts were submitted and detection ran; a quiet scope legitimately yields few |
| Thin findings (no CVEs) | add **authenticated inventory** (Stage 6 creds) — unauthenticated scans are version-poor |
| AI Brain shows canned text | expected — it's mock until the OpenRouter wiring lands; don't use it for findings |
| Port conflict | change `API_PORT` / `FRONTEND_PORT` in `.env`, `make down && make up` |

---

### Success criteria
Manager healthy behind TLS → probe **online** from inside the target network → engagement scoped to
**authorized** ranges → assessment job `done` → **real findings** on the Priority Queue, produced by
the real detection pipeline — with **nothing outside scope contacted** and your performance envelope
recorded.
