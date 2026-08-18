# Design — Installer warning, Fleet job visibility, Engagement host-chaining

**Date:** 2026-08-19
**Branch:** `feat/complete-pending-work`
**Landing:** implement all three → verify → direct merge + push to `main`

Three independent changes bundled into one delivery. Each is self-contained and
testable on its own.

---

## Item 1 — Installer: silence the http warning once insecure is opted into

**Problem.** `probe/install.sh` warns on *any* `http://` non-local manager, even
when the operator explicitly passed `--insecure` (i.e. already acknowledged
plaintext). The warning is noise for a deliberate http testing setup.

**Change.** In the DOCKER-mode `case "$PLATFORM_URL"` block (`install.sh:435–439`),
gate the `http://*` warning on `PROBE_ALLOW_INSECURE`:

- `PROBE_ALLOW_INSECURE=true` (set by `--insecure`) → **no warning**.
- `http://` non-local **without** `--insecure` → warning still emitted (guards
  against accidental plaintext).
- `https://` / localhost / `host.docker.internal` / `api` → unchanged.

**Scope.** Cosmetic/log-only. No behavioural change to transport security — the
probe still talks http; only the message is suppressed when intended.

**Tests.** Shell-level: run installer in `PROBE_INSTALL_DRY_RUN=true` with an
`http://` manager, once with `--insecure` (assert no warning line) and once
without (assert warning present).

---

## Item 2 — Persistent job visibility, grouped under each probe (Fleet page)

**Problem.** `/scan` stores the just-launched dispatch in ephemeral React state
(`setDispatched`, `app/scan/page.tsx:568`). Navigating away loses it, even though
the `ScanJob` row persists server-side. The Fleet page shows only a probe's
current `current_job_id`, no history.

### Backend
New read-only, operator-authenticated, tenant-scoped endpoint:

```
GET /agents/{agent_id}/job-history?limit=20
```
- Returns recent `ScanJob`s for that agent, newest first: `id`, `job_type`,
  `status`, `started_at`, `completed_at`, `use_case_id` (from `result.use_case_id`),
  and a compact target/host summary (`host_count` if present in result).
- **Distinct** from the existing `GET /{agent_id}/jobs` (which *claims* pending
  jobs for the probe — must not be touched). Tenant filtering mirrors the
  existing agent endpoints (join `Engagement`, filter by caller tenant).
- Redacts the same keys as the single-job endpoint (`_REDACT`, `agents.py:966`).

### Frontend
- **Fleet page** (`app/fleet/page.tsx`): each probe card becomes expandable.
  Expanding fetches job history via a new Next proxy route
  `app/api/fleet/agents/[id]/jobs/route.ts` → backend `job-history`. Renders the
  running job (existing `current_job_id`) plus recent history with status chips.
  Polls (~8s) while any listed job is active; stops when idle.
- **`/scan` page**: on launch, keep the returned `job_id`; hydrate status from
  the server (`GET /agents/jobs/{job_id}`, `agents.py:942`) on mount and while
  in flight, instead of relying solely on the local `dispatched` variable. A
  just-launched job therefore survives navigation and re-hydrates on return.

**Tests.** Backend: `job-history` returns only the caller-tenant's jobs, honours
`limit`, orders newest-first, redacts secrets. Frontend: covered by manual/QA
verification (expand card shows running + past; navigate away/back on `/scan`
keeps the job).

---

## Item 3 — Engagement-scoped active-host chaining

Two layers: keep the existing in-run chaining, add cross-job sharing.

### 3a. Single-run (already works — keep + document)
Within one `run_engagement`, host discovery gates port/service/deep stages on
`live_hosts` (`workflow_engine.py:321,328`). No code change; documented in
`PROBE_USECASES.md` as the intended in-run behaviour.

### 3b. Cross-job sharing within an engagement (new)

**New table `engagement_live_hosts`** (Alembic `0033`, after `0032`):

| column | type | notes |
|---|---|---|
| `id` | UUID PK | `gen_random_uuid()` |
| `engagement_id` | UUID FK → engagements.id ON DELETE CASCADE | indexed |
| `host` | String(64) | IP string |
| `last_seen_at` | timestamptz | updated on each sighting |
| `source_job_id` | UUID FK → scan_jobs.id ON DELETE SET NULL | provenance |

Unique constraint on `(engagement_id, host)`.

**Upsert on result submit.** In `process_job_result`
(`app/services/job_result_service.py:127`), after the job is loaded and results
processed, extract alive hosts from `result["hosts"]` (each `host["ip"]`; the
probe only includes affirmatively-alive hosts — `engine.py:297`) and upsert them
into `engagement_live_hosts` for `job.engagement_id`, setting
`last_seen_at=now`, `source_job_id=job_id`. Best-effort: wrapped so it never
fails the probe's spool-clearing submit.

**`requires_live_hosts` flag on the use-case catalog.** Add the key to `_USE_CASES`
(`agents.py:331`):
- `true` — targeted service use-cases: `uc_full_assessment`,
  `uc_external_web_triage`, `uc_db_exposure`, `uc_windows_estate`,
  `uc_ai_endpoint_sweep`, `uc_rescan_delta`, `uc_iot_device_survey`,
  `uc_web_app_triage`, and any other service-branch UC.
- `false` — `uc_discovery_only` (it *finds* hosts) and `uc_ot_passive` (passive,
  zero active packets).
Default when unspecified: `false` (safe — no seeding).

**Seed on dispatch.** At job creation (`agents.py:~1100`), if the resolved UC
`requires_live_hosts` **and** the operator pinned no explicit `targets`, seed
`job_params` targets from `engagement_live_hosts` for **that engagement only**.
Fallbacks: if the table has no hosts for the engagement yet, leave targets as-is
(full engagement scope) so a first-ever run still works.

**Guarantees.**
- Strictly engagement-scoped — a query never reads another engagement's hosts.
- Operator-chosen explicit targets are never overridden.
- Discovery / OT-passive UCs are unaffected.

**Tests.**
- Host extraction from a sample `result["hosts"]` payload.
- Upsert idempotency (same host twice → one row, `last_seen_at` advanced).
- Seeding matrix: `requires_live_hosts` × (explicit targets? ) × (table empty?).
  - requires + no explicit + hosts known → seeded with those hosts.
  - requires + explicit targets → untouched.
  - requires + empty table → untouched (full scope).
  - not-requires → untouched.
- Engagement-scoping: hosts from engagement A never seed a job in engagement B.

---

## Delivery / sequencing

1. Item 1 (installer) — isolated, fastest.
2. Item 3 (backend + migration + probe doc) — schema, upsert, seed, tests.
3. Item 2 (backend endpoint + frontend) — depends on nothing but is the largest UI surface.
4. Run focused tests (backend pytest, targeted; probe tests with timeout per repo gotchas).
5. Commit on `feat/complete-pending-work`, merge to `main`, push `origin main`.

## Out of scope (YAGNI)
- No cross-engagement host sharing.
- No live-host history/delta UI (table stores `last_seen_at`; no timeline view).
- No new global "all jobs" page — job visibility lives under each probe on Fleet.
