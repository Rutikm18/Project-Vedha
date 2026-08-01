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
| **Is** | `probe/` (collector workflow + transport agent) | `manager/backend` + `manager/detection_engine` + `manager/frontend` |
| **Runs** | inside each client's network (one per client) | central / cloud, multi-tenant |
| **Does** | collection only — scans, produces **raw facts**, ships them up | analysis — facts → findings → attack mapping → reporting → dashboard |
| **Holds** | no vulnerability DB, no client data at rest beyond its identity | the pinned vuln DB, all findings, all tenant data |

**Design rule:** the probe is *thin* (collection), the manager is *fat* (analysis). The
vulnerability database lives **only** on the manager — versioned, auditable, re-runnable
without re-scanning, and never copied into a client's network.

```
┌─ PROBE  (client network) ─────────────────┐        ┌─ MANAGER  (cloud) ─────────────────────┐
│  probe/                                    │        │  manager/backend (FastAPI + Postgres)│
│    scanner/    13 scanners (ScanResult)    │  jobs  │    ingest facts → Asset                │
│    workflow/   per-target sequencing+cache │◀───────│    detection_engine/  facts → findings │
│    agent/      register·poll·scan·submit   │  facts │    ad/ graph/ exploit/  attack mapping │
│                                            │───────▶│    ai/   AI reporting                  │
│  enforces ScopeGuard before any packet     │        │  manager/frontend (Next.js dashboard)│
└────────────────────────────────────────────┘        └────────────────────────────────────────┘
```

---

## 2. The probe (`probe/`)

### 2.1 Runtime boundary

The production image is built from `probe/`. Its Python agent registers capabilities,
claims tenant-scoped jobs, enforces authoritative scope, runs the gated workflow, and
durably submits raw facts. It is the **only supported product probe**. `probe-go/` is a
non-shipping parity workspace; it must not be deployed until it passes the capability
and security gates documented in its README.

### 2.2 Layout
```
probe/                          ← THE PRODUCTION PROBE
├── scanner/                    ← native collectors + standalone validators
│   ├── scanner_base.py         ←   ScanResult schema, BaseScanner, ScopeGuard
│   └── *_scanner.py / *_collector.py
├── workflow/                   ← bounded, fail-isolated per-target sequencing
│   ├── workflow_engine.py · execution.py · asset.py · cache.py · gates.py
│   ├── router.py · modes.py · report.py · cli.py
├── agent/                      ← manager transport and durable result delivery
│   ├── agent.py                ←   register→heartbeat→poll→scan→submit loop
│   ├── transport.py            ←   authenticated HTTP/WebSocket client
│   ├── task_runner.py          ←   scope validation and job lifecycle
│   └── result_spool.py         ←   atomic private spool + acknowledged removal
├── run_scan.py                 ← standalone local CLI
├── Dockerfile · install.sh · probe.env.example
└── requirements.txt
```

### 2.3 Job → scan dispatch
The agent maps the finite use-case catalog to the workflow engine. The workflow owns
bounded host fan-out, per-target failure isolation, dynamic branch routing, and structured
component telemetry. Invalid profile, target, expansion, or authoritative-scope input fails
before the workflow can emit packets.

### 2.4 Engine transparency

`engine: "scanner_module"` remains the stable wire identifier for compatibility. It does
not hide component identity:

- `engine_manifest.orchestrator` identifies the Vedha workflow build.
- `engine_manifest.components` lists every native collector and its role.
- `scanner_runs` records targets, facts, errors, and
  `completed|cached|skipped|degraded|failed` for each planned component.
- `issues` carries stable error codes, retryability, and remediation.
- Nmap and Masscan appear under `external_engines` as `standalone_validation`;
  availability never implies execution.

---

## 3. Scope provisioning (manager → probe)

This is the canonical manager-to-probe authorization path.

```
Engagement.scope_cidrs            (manager, per-tenant authorization boundary)
        │  operator starts a scan
        ▼
ScanJob.params = {                (enqueued via POST /agents/jobs)
   scope_cidrs:  ["10.0.0.0/24"],     ← the allowlist
   targets:      ["10.0.0.0/24"],     ← what to actually scan (⊆ scope)
   excluded_cidrs: [...],
   profile:      "it" | "iot" | "ot", ← tunes ports/rate (workflow profiles)
   scan_type:    one advertised finite capability
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
    "outcome": "partial",
    "engine": "scanner_module",
    "engine_manifest": {
      "orchestrator": {"id": "scanner_module", "label": "Vedha Probe Collector", "version": "2.0.0"},
      "components": [...],
      "external_engines": [...]
    },
    "scan_type": "assessment",
    "scanner_runs": [
      {"id":"host_discovery","status":"completed","fact_count":1,"error_count":0},
      {"id":"tls_scan","status":"degraded","fact_count":1,"error_count":1}
    ],
    "issues": [
      {"code":"scanner_timeout","scanner":"tls_scan","target":"10.0.0.6","retryable":true}
    ],
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

### 5.1 Detection wiring (`manager/detection_engine/` → `manager/backend`)
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
| `vedha-probe` | scanner_module + agent; **no vuln DB** | client network (hardened Docker image) |
| `vedha-backend` | FastAPI + detection_engine + **pinned vuln DB snapshot** | cloud |
| `vedha-frontend` | Next.js dashboard (BFF → backend) | cloud |
| `postgres`, `redis` | state / queue | cloud |

**Probe deployment** (best approach for client-network placement):
- **Docker** (default): `install.sh` → one non-root, read-only container that dials *out* only
  (no inbound ports). Identity state is atomic and mode `0600` in a private volume; volume/disk
  encryption is a deployment requirement because application-layer state encryption is not yet implemented.
- **Host-Python development** is available through the probe CLI, but the production installer
  currently supports the hardened Docker artifact only.
- Bootstrap config: `PLATFORM_URL`, a scoped PAT, mandatory
  `PROBE_NETWORK_SEGMENTS`, execution ceilings, and optional license material.
  Job scope arrives from the Manager and must also fit the probe-local ceiling;
  the bootstrap PAT is removed from steady-state container metadata.

---

## 8. Validation & accuracy

| Layer | How it's validated |
|---|---|
| Scanners | parser, protocol, timeout, malformed-output, and accuracy tests |
| Workflow engine | bounded fan-out, partial preservation, routing, cache, and mode tests |
| `detection_engine` | precision/recall harness + dpkg cross-validation + epoch/backport traps |
| Wire contract | use-case parity and probe facts payload/manager ingest tests |
| Dispatch | tenant, capability, network-segment, and atomic-claim tests |
| Scope safety | out-of-scope and excluded targets are refused at manager and probe |
| Result durability | atomic spool, acknowledged deletion, reconnect, and path-safety tests |

---

## 9. Deployment invariants

1. Production Compose builds only `probe/` for field collection; no Manager or
   dashboard process has scanner binaries or network-scanning capabilities.
2. A probe receives jobs only for its tenant, advertised capability, and reachable segment.
3. WebSocket offers execute only after the manager atomically confirms the claim.
4. Result evidence is spooled before delivery and removed only after manager acceptance.
5. External tools must pass their own launch, dependency, output, and parser checks; zero
   findings after an engine error is never a successful scan.
6. Cross-run change reporting is a manager diff of full assessments until persistent
   probe cache ownership is explicitly implemented.
7. Scan job parameters never contain passwords, tokens, private keys, or other
   credential material. Authenticated collection remains disabled until an
   ephemeral credential broker can deliver secrets without persisting them in
   `scan_jobs`.

---

## 10. Open decisions captured

- ✅ `probe/` is the only production probe; `probe-go/` is non-shipping research until parity.
- ✅ Probe ships **raw facts**; manager runs detection.
- ✅ Pinned vuln DB lives on the **manager** only.
- ✅ Reject credential-bearing job params instead of storing target secrets in Postgres.
- ⬜ Integrate an OS keyring/KMS-backed envelope key for probe identity-token encryption at rest.
  Until then, require encrypted host storage and restrict access to the private probe state volume.
- ⬜ Keep `license.py` host-lock for probes? (port as-is; can disable via env — default keep)
- ⬜ Add the append-only `scan_results` table now, or defer until re-detection is needed?
