# Agentic VA Scanner — System Architecture

> Status: **implemented & validated** (2026-06-25). The consolidation below is done;
> the tree was restructured into functional, deployable-boundary names.

## 0. Repository layout (canonical)

```
Agentic VA Scanner/
├── docker-compose.yml          orchestrates the whole stack
├── Makefile  .env(.example)    one-command ops + config
├── README.md  ARCHITECTURE.md
├── probe/                      DEPLOYABLE — scanning agent (runs in client network)
│   ├── scanner/                  the 13 scanners (ScanResult schema)
│   ├── workflow/                 per-target sequencing + caching
│   ├── agent/                    manager transport (register→poll→scan→submit)
│   └── Dockerfile install.sh probe.env.example
└── manager/                    the cloud platform
    ├── backend/                  FastAPI + Postgres (app/detection/engine_bridge.py wires detection)
    ├── frontend/                 Next.js dashboard (BFF → backend)
    ├── detection_engine/         facts → findings (pinned vuln DB lives here)
    └── docs/
```

> Naming maps: `scanner_module/`→`probe/`, `vedha/`→`manager/`, the old standalone
> `detection_engine/`→`manager/detection_engine/`. References to those old names in the
> historical sections below now live at the paths above.

---

## 1. The two deployables

| | **Probe** | **Manager** |
|---|---|---|
| **Is** | `scanner_module/` (scan engine + transport agent) | `vedha/backend` + `detection_engine/` + `vedha/frontend` |
| **Runs** | inside each client's network (one per client) | central / cloud, multi-tenant |
| **Does** | collection only — scans, produces **raw facts**, ships them up | analysis — facts → findings → attack mapping → reporting → dashboard |
| **Holds** | no vulnerability DB, no client data at rest beyond its identity | the pinned vuln DB, all findings, all tenant data |

**Design rule:** the probe is *thin* (collection), the manager is *fat* (analysis). The
vulnerability database lives **only** on the manager — versioned, auditable, re-runnable
without re-scanning, and never copied into a client's network.

```
┌─ PROBE  (client network) ─────────────────┐        ┌─ MANAGER  (cloud) ─────────────────────┐
│  scanner_module/                           │        │  vedha/backend  (FastAPI + Postgres) │
│    scanner/    13 scanners (ScanResult)    │  jobs  │    ingest facts → Asset                │
│    workflow/   per-target sequencing+cache │◀───────│    detection_engine/  facts → findings │
│    agent/      register·poll·scan·submit   │  facts │    ad/ graph/ exploit/  attack mapping │
│                                            │───────▶│    ai/   AI reporting                  │
│  enforces ScopeGuard before any packet     │        │  vedha/frontend  (Next.js dashboard) │
└────────────────────────────────────────────┘        └────────────────────────────────────────┘
```

---

## 2. The probe (`scanner_module/`)

### 2.1 Why it changes
`scanner_module` today is **CLI-only** — it scans but cannot talk to the manager. The
working transport already exists in `vedha/probe/agent.py` (register → heartbeat → poll →
submit, host-bound encrypted identity, anti-copy license, resilient retry, `./probe` CLI).
We **port that transport in** and swap its duplicate engine (`vedha/probe/scanners/`) for
the real `scanner_module` engine. `vedha/probe/` is then removed.

### 2.2 Target layout
```
scanner_module/                 ← THE PROBE (one deployable artifact)
├── scanner/                    ← engine: 13 scanners (UNCHANGED — never modified)
│   ├── scanner_base.py         ←   ScanResult schema, BaseScanner, ScopeGuard
│   └── *_scanner.py / *_collector.py
├── workflow/                   ← per-target sequencing + caching (existing)
│   ├── workflow_engine.py · asset.py · cache.py · gates.py
│   ├── router.py · modes.py · report.py · cli.py
├── agent/                      ← NEW: transport (ported from vedha/probe)
│   ├── agent.py                ←   register→heartbeat→poll→scan→submit loop
│   ├── transport.py            ←   httpx client, retry, auth
│   ├── identity.py             ←   host-bound encrypted state cache  (ported)
│   ├── license.py              ←   host-locked anti-copy gate        (ported, optional)
│   └── submit.py               ←   serialize ScanResult facts → result payload
├── run_scan.py                 ← existing standalone CLI (kept for local testing)
├── pipeline.py                 ← existing fixed pipeline (kept as fallback)
├── Dockerfile                  ← NEW: probe image
├── install.sh                  ← NEW: Docker- or systemd-based deploy
├── probe.env.example           ← NEW: config template
└── requirements.txt
```
> `scanner/` is treated as **frozen** — the consolidation wires *around* it, never edits the
> scanners themselves (matches the standing "don't modify the scanner scripts" rule).

### 2.3 Job → scan dispatch
The agent maps a manager `job_type`/`scan_type` to the workflow engine (preferred) or a
single scanner, passing the job's scope/params straight through. The workflow engine already
owns sequencing, caching, and dynamic routing, so the agent stays a thin driver.

---

## 3. Scope provisioning (manager → probe)

Already half-built on both ends; we make it the canonical path.

```
Engagement.scope_cidrs            (manager, per-tenant authorization boundary)
        │  operator starts a scan
        ▼
ScanJob.params = {                (enqueued via POST /agents/jobs)
   scope_cidrs:  ["10.0.0.0/24"],     ← the allowlist
   targets:      ["10.0.0.0/24"],     ← what to actually scan (⊆ scope)
   excluded_cidrs: [...],
   profile:      "it" | "iot" | "ot", ← tunes ports/rate (workflow profiles)
   mode:         "triage" | "assessment" | "service-specific" | "re-scan"
}
        │  probe polls GET /agents/{id}/jobs
        ▼
Probe builds ScopeGuard.from_list(scope_cidrs)
        │
        ▼
ScopeGuard.assert_in_scope(target)  ← HARD allowlist, BEFORE any packet leaves
```

**Dual enforcement** (defence in depth): the manager refuses to enqueue out-of-scope targets,
**and** the probe refuses to scan anything outside `scope_cidrs` regardless of what a job says.
`ot` profile is structurally passive-only on both ends.

---

## 4. Findings: raw facts up

The probe ships **raw facts**, not findings. The job-result payload reuses the existing
endpoint `POST /agents/{id}/jobs/{job_id}/result`:

```jsonc
{
  "success": true,
  "result": {
    "ok": true,
    "engine": "scanner_module",
    "scan_type": "assessment",
    "facts": [                       // ← array of ScanResult dicts (the scanners' native output)
      {"scanner":"tls_scan","target":"10.0.0.5","port":443,"proto":"tcp",
       "status":"open","data":{"accepted_versions":["TLSv1.2"],"certificate":{...}},
       "evidence":"...","timestamp":"..."}
    ],
    "host_count": 1, "service_count": 4, "finding_count": 0   // counts only; NO CVEs
  },
  "error": null
}
```
Rule: **the probe never emits a CVE or a vuln verdict.** Those come only from the manager's
`detection_engine` against the pinned DB.

---

## 5. The manager

### 5.1 Detection wiring (`detection_engine/` → `vedha/backend`)
On job-result ingest the backend runs the deterministic pipeline already built:

```
facts (ScanResult JSONL)
   → detection_engine.ingest          → Asset (per-host)
   → cpe_normalizer (+ ai_normalizer)  → CPE candidates
   → vuln_db (pinned snapshot) + matcher → range-matched findings
   → enrichment (CVSS / KEV / EPSS)    → prioritized
   → correlate (dedup, suppress, composite)
   → Finding[]  (cve_id, state, source_confidence, evidence_refs,
                 cvss, kev, epss, priority, ai_assisted)
   → persist to `findings`
   → trigger attack mapping (ad/ graph/ exploit/)
```
The pinned vuln DB snapshot ships **with the manager image / a mounted volume**, version-
stamped in every run's metadata (already implemented in `detection_engine/vuln_db.py`).

### 5.2 Existing manager engines
`backend/app/ad/`, `graph/`, `exploit/`, `ai/` consume `Finding[]` for attack-path mapping,
AD assessment, exploit correlation, and AI reporting — unchanged in responsibility, now fed
by the canonical detection layer instead of the ad-hoc `backend/app/vuln` path.

---

## 6. Data model (Postgres, existing tables extended)

| Table | Role | Change |
|---|---|---|
| `agents` | registered probes (identity, caps, heartbeat) | none |
| `engagements` | scope, RoE, tenant | none |
| `scan_jobs` | queued/most-recent job + raw result | result now holds the **facts** array |
| `assets` / `services` | per-host inventory from facts | populated from ingest |
| `findings` | detection output | extend to detection_engine's full schema (state, source_confidence, evidence_refs, cvss/kev/epss, priority, ai_assisted) |
| `scan_results` *(new, optional)* | append-only raw facts for re-detection | enables "re-run detection with newer DB without re-scanning" |

---

## 7. Docker images & deployment

| Image | Contents | Where |
|---|---|---|
| `vedha-probe` | scanner_module + agent; **no vuln DB** | client network (Docker or systemd via `install.sh`) |
| `vedha-backend` | FastAPI + detection_engine + **pinned vuln DB snapshot** | cloud |
| `vedha-frontend` | Next.js dashboard (BFF → backend) | cloud |
| `postgres`, `redis` | state / queue | cloud |

**Probe deployment** (best approach for client-network placement):
- **Docker** (default): `install.sh` → `docker run --env-file probe.env vedha-probe`. One
  container, dials *out* only (no inbound ports), persists encrypted identity in a volume.
- **systemd** (`install.sh --native`): for hosts without Docker.
- Config via `probe.env`: `PLATFORM_URL`, operator creds (or pre-provisioned `AGENT_ID/TOKEN`),
  `PROBE_NETWORK_SEGMENTS`, license. Scope itself arrives per-job, not baked into the image.

---

## 8. Validation & accuracy

| Layer | How it's validated |
|---|---|
| Scanners | existing per-scanner accuracy tests (scanner_module) |
| Workflow engine | validated end-to-end against this host (caching, dynamic routing, modes) |
| detection_engine | precision/recall harness + dpkg cross-validation + epoch/backport traps (done) |
| **Wire contract** | NEW: schema test asserting probe facts payload ⟷ what backend ingest expects |
| **End-to-end** | NEW: probe scans a known fixture → facts → manager detection → asserted findings → dashboard renders them |
| Scope safety | NEW: out-of-scope target is refused at both manager and probe |

---

## 9. Consolidation steps (ordered, each reversible)

1. **Port transport** `vedha/probe/{agent,security,toolchain,license}` → `scanner_module/agent/`, swapping the engine to scanner_module. *(no deletion yet)*
2. **Scope** wiring + dual ScopeGuard enforcement + contract test.
3. **Probe image** Dockerfile/install.sh/probe.env; bring up a probe from scanner_module.
4. **Detection** wire detection_engine into backend job-result ingest; persist full findings.
5. **End-to-end** validation (fixture → facts → findings → dashboard).
6. **Remove** `vedha/probe/` and the duplicate `Vedha copy/` only after 1–5 pass.

---

## 10. Open decisions captured

- ✅ scanner_module **is** the probe; the other probe is removed (after its transport is absorbed).
- ✅ Probe ships **raw facts**; manager runs detection.
- ✅ Pinned vuln DB lives on the **manager** only.
- ⬜ Keep `license.py` host-lock for probes? (port as-is; can disable via env — default keep)
- ⬜ Add the append-only `scan_results` table now, or defer until re-detection is needed?
