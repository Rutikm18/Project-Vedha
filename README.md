# Agentic VA Scanner

An automated network VA platform split into two deployables by responsibility:

| | **Probe** (`probe/`) | **Manager** (`manager/`) |
|---|---|---|
| Runs | inside each client network (one per client) | central / cloud |
| Does | **collection only** — scans, ships raw facts up | **analysis** — facts → findings → attack mapping → dashboard |
| Holds | no vulnerability DB; dials out only | the pinned vuln DB, all findings, all tenant data |

The probe is thin (collection); the manager is fat (analysis). The probe never
emits a CVE — detection runs on the manager against a pinned, versioned vuln DB
that never leaves the cloud.

```
Agentic VA Scanner/
├── docker-compose.yml · Makefile · .env     one-command orchestration
├── ARCHITECTURE.md                          system design (read this)
├── probe/                                   the scanning agent (deploy in client net)
│   ├── scanner/      13 stdlib scanners (ScanResult schema)
│   ├── workflow/     per-target sequencing, caching, dynamic routing
│   ├── agent/        manager transport (register→poll→scan→submit)
│   └── Dockerfile · install.sh · probe.env.example
└── manager/                                 the cloud platform
    ├── backend/          FastAPI + Postgres (app/detection/engine_bridge.py)
    ├── frontend/         Next.js dashboard (BFF → backend)
    ├── detection_engine/ facts → findings: CPE match → CVSS/KEV/EPSS → verify
    └── docs/
```

## Quick start (local, Docker)

```bash
cp .env.docker.example .env     # set JWT_SECRET + SEED_ADMIN_PASSWORD
make full                       # postgres + redis + api + probe + dashboard
```

| Service | URL | |
|---|---|---|
| Dashboard | http://localhost:3000 | sign in with `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD` |
| API + docs | http://localhost:18080 · `/docs` | FastAPI |

Defaults: `admin@adversa.io` / `ChangeMe123!` (change them in `.env`).

### Make targets

```
make run      # api + local probe (no dashboard) — fast
make full     # everything incl. the Next.js dashboard
make api-only # platform only (no probe, no dashboard)
make ui       # just the dashboard (api must be up)
make down     # stop (keeps the database)   |   make clean  # stop + wipe DB
make ps       # status   |   make logs  # tail api   |   make test  # backend tests
```

## How a scan flows end to end

1. Create an **engagement** with a scope (CIDRs) in the dashboard or API.
2. Enqueue a scan job → the **probe** (inside the client net) polls it.
3. Probe builds a `ScopeGuard` hard allowlist, runs the scanners, ships **raw
   facts** (`ScanResult` JSONL) back — never CVEs.
4. **Manager** ingests facts → `detection_engine` matches them against the
   pinned vuln DB → enriches (CVSS/KEV/EPSS) → correlates → **verifies**
   (confidence + evidence tier, anti-FP) → persists findings.
5. Findings render in the dashboard; attack-path / AD / AI-report engines
   consume them.

Scope is enforced at **both** ends (manager won't dispatch out-of-scope; probe
refuses to scan it). `ot` profile is structurally passive-only.

## Deploying a probe to a real client network

The probe is a standalone, dial-out-only artifact (no inbound ports, no vuln DB):

```bash
cd probe
cp probe.env.example probe.env     # set PLATFORM_URL + operator creds
./install.sh                       # Docker  (or ./install.sh --native for host Python)
```
See `probe/README.md`. Scope arrives per-job from the manager, not baked into the probe.

## Running components standalone (dev)

```bash
# Probe scan engine, no manager — pure stdlib, CLI:
cd probe && python3 -m workflow.cli -t 127.0.0.1 -s scope.txt --mode assessment

# Detection engine on a facts JSONL, no platform:
cd manager/detection_engine && python3 -c "from pipeline import run_pipeline; \
  print(len(run_pipeline(['/path/to/facts.jsonl'])[0]), 'findings')"

# Backend tests:
make test     # (needs manager/backend/.venv)
```

## Detection pipeline (manager/detection_engine)

Deterministic and offline at every step except the explicit, separate snapshot
sync (`update_snapshot.py`). Built in phases:

- **P1** ingest → CPE-normalize → version-range match (dpkg-accurate) → CVSS/KEV/EPSS enrich → dedup/correlate/suppress
- **P2** AI normalization assist (rule-based first, AI only on misses, NVD-validated, never emits a CVE)
- **P3** generalized verifier — every finding gets a calibrated `confidence`, `evidence_reason`, and `checks{}` audit; only ever lowers certainty (anti-FP)
- **P5** N-run consistency — appearance rate + Wilson CI, stable vs intermittent (`consistency.py`)

See `ARCHITECTURE.md` for the full design.
