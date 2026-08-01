# Probe Fleet Automation — Design Spec

**Date:** 2026-08-02
**Status:** Approved for Phase 0 implementation
**Author:** brainstorming session (Rutik + Claude)

## Goal

Move Vedha's probe fleet from manual, multi-input onboarding toward a
**one-command, mostly-automated** model with a **centralized manager** and
**dashboard-driven job-queue control**:

> `install.sh <engagement-token>` → probe auto-connects, auto-authenticates,
> auto-pulls its authorized scope, and starts taking prioritized jobs the
> operator manages entirely from the dashboard. Minimal manual intervention.

This spec documents the full target architecture, then specifies **Phase 0** in
implementation-ready detail. Phases 1–3 are scoped here for context; each gets
its own spec → plan → build cycle.

---

## Current reality (verified in code)

- **Enrollment:** probe calls `POST /agents/register` authenticated with an
  **operator PAT** (`vpat_…`, role admin/manager) and receives a 1-year agent
  JWT (`agents.py:456`). `install.sh` requires five manual inputs:
  `OPERATOR_TOKEN`, `PLATFORM_URL`, `PROBE_NETWORK_SEGMENTS`, `PROBE_LICENSE`,
  `PROBE_LICENSE_PUBKEY`.
- **Binding:** an Agent is bound to a **tenant**, not an engagement. Any
  capable + reachable probe in the tenant claims jobs.
- **Queue:** jobs are claimed **FIFO by `created_at`** via an atomic conditional
  `UPDATE` (`agents.py:642`). There is **no priority**, no dashboard queue
  control, no cancel/pause. A lease + reaper requeues jobs from dead probes.
- **Agent model** (`app/models/agent.py`): `id, tenant_id, name, location,
  capabilities, network_segments, status, last_heartbeat, current_job_id,
  public_key`. **No `disabled` field** — agent JWTs are stateless 1-year tokens
  with **no revocation path**.
- **ScanJob model** (`app/models/scan_job.py`): `id, engagement_id, job_type,
  status, agent_id, started_at, completed_at, result, lease_expires_at`. **No
  `priority`**. `use_case_id` is carried inside job params (`job.result`).
- **Two claim paths:** HTTP poll `get_agent_jobs` (`agents.py:613`) and a
  WebSocket push path `_claim_pushed_job` (`agent_ws.py:47`). The WS path claims
  a specific offered `job_id`; the HTTP path selects via `order_by`.

---

## Target architecture — the Enrollment Token keystone

A new token type `venr_…`, minted **per engagement** from the dashboard. It is
**self-describing**: a base64url-encoded bundle of
`{ manager_url, tenant_id, engagement_id, secret }`. This is what lets the
install command take **only the token**:

1. **Auto-connect** — `manager_url` is inside the token → no `PLATFORM_URL`.
2. **Auto-auth** — probe calls `POST /agents/enroll` (unauthenticated; the token
   *is* the credential). Manager validates the hashed `secret`, creates or reuses
   the Agent, returns a long-lived **agent JWT**.
3. **Auto-scope** — the enroll response carries the engagement's `scope_cidrs`.
   The manager's engagement scope stays **authoritative**; the probe only
   advertises which of those subnets it can actually *reach* → no
   `PROBE_NETWORK_SEGMENTS`.
4. **Auto-license** — the manager mints the signed license **during enroll** →
   no `PROBE_LICENSE` / pubkey.
5. **Restart-safe** — probe persists the agent JWT in its state volume and
   reuses it on restart; the enrollment token is only touched on first boot.

### Edge cases & decisions (the parts that bite)

| # | Challenge | Decision |
|---|-----------|----------|
| 1 | Enroll endpoint is unauthenticated — token = credential | Short TTL, **revocable**, **rate-limited**, hashed at rest, bound to `hw_id` on first use, every enroll **audit-logged** |
| 2 | Redeploy loses state → re-enroll, but token "used" | Tokens are **reusable within TTL** (not strictly one-time) + revocable; dedup Agent by **`hw_id`** (not name) so redeploys never spawn duplicates |
| 3 | Auto-scope must never scan more than authorized | Manager `scope_cidrs` authoritative; probe reports *reachable* subnets as metadata; intersection enforced; unreachable scope → job **fails loud**, not silent |
| 4 | Revoke a rogue/stale probe (JWT is stateless 1yr) | Add `agent.disabled`; the job-poll already loads the Agent row → deny disabled → instant kill-switch |
| 5 | Priority starvation (low-pri never runs) | Claim order `(priority desc, created_at asc)` + **aging** (Phase 3) |
| 6 | Cancelling a *running* job (probe already has it) | Cooperative cancel via a flag the probe checks on heartbeat/poll — **Phase 3** |
| 7 | Token leaks via shell history / argv | Prefer stdin/env, short TTL, one-glance dashboard revoke |
| 8 | Clock skew on token TTL / JWT exp | Small validation leeway |
| 9 | Flaky network → enroll retried | Enroll is **idempotent** on `(hw_id, token)` — same Agent, no duplicates |
| 10 | Back-compat | Enroll is **additive**; PAT-based `register` keeps working |

### Phased decomposition

- **Phase 0 — Queue control + revocation** *(this spec; no new token)*.
- **Phase 1 — Enrollment token primitive**: `enrollment_tokens` table, mint
  endpoint + dashboard mint UI, `POST /agents/enroll`, audit log, revoke.
- **Phase 2 — One-command install**: rewrite `install.sh <token>` — self-describing
  token, auto-scope, manager-issued license, JWT persistence, `hw_id` dedup;
  collapse 5 inputs → 1.
- **Phase 3 — Advanced queue**: cooperative cancel of running jobs, pause/resume,
  pin-to-probe, anti-starvation aging.

---

## Phase 0 — Queue Control + Revocation (implementation-ready)

Lowest-risk, independently valuable, and de-risks Phases 1–2. Delivers the
operator's ability to **see and steer** the fleet before we automate onboarding.

### 0.1 Data model changes

1. **`ScanJob.priority`** — `Mapped[int]`, `nullable=False`, `server_default="0"`,
   indexed. Higher runs first. Alembic migration; existing rows default to 0.
2. **`ScanJobStatus.canceled`** — new enum value. Migration adds it to the
   Postgres enum type `scanjobstatus`.
3. **`Agent.disabled`** — `Mapped[bool]`, `nullable=False`,
   `server_default="false"`. Migration.

### 0.2 Backend behavior changes

1. **Priority-ordered claim** — in `get_agent_jobs` (`agents.py:642`) change
   `.order_by(ScanJob.created_at)` →
   `.order_by(ScanJob.priority.desc(), ScanJob.created_at.asc())`. If the WS push
   path selects which pending job to offer, apply the same ordering there;
   `_claim_pushed_job` itself claims by `job_id` and needs no change.
2. **Kill-switch** — after loading the Agent in `get_agent_jobs` and in the
   heartbeat handler, if `agent.disabled` → `HTTP 403 "agent disabled"`. A
   disabled probe stops receiving *new* jobs within one poll; its current leased
   job runs to completion (documented).

### 0.3 New / changed endpoints (all tenant-scoped via `AuthUser`)

1. **`GET /agents/jobs/recent?limit=N`** *(new)* — tenant-wide recent jobs for the
   dashboard queue view. Returns, newest-first:
   `{ job_id, engagement_id, engagement_name, use_case_id, job_type, status,
   priority, agent_id, agent_name, created_at, started_at, completed_at }`.
   `use_case_id` is read from `job.result` params; `engagement_name`/`agent_name`
   via joins. Default `limit=5`, max 100.
2. **`PATCH /agents/jobs/{job_id}`** *(new)* — body `{ priority?, action? }`:
   - `priority`: set priority. **Conditional** on `status = pending` — a job may be
     claimed between the UI read and the PATCH; if already running, return
     `409 "job already running"`.
   - `action: "cancel"`: `pending → canceled`, also conditional; `409` if running
     (running-job cancel is Phase 3).
3. **`PATCH /agents/{agent_id}`** *(new, or `POST /agents/{id}/disable|enable`)* —
   body `{ disabled: bool }`. Role admin/manager. Toggles the kill-switch.
4. **`GET /engagements/{id}/jobs`** *(extend)* — add `priority` and `use_case_id`
   to each row (currently omitted).

### 0.4 BFF proxies (Next.js `app/api/…`)

- `GET /api/scan/recent-jobs` → `/agents/jobs/recent`.
- `PATCH /api/scan/jobs/[id]` → `PATCH /agents/jobs/{id}` (add PATCH to the
  existing route file).
- `PATCH /api/scan/probes/[id]` → `PATCH /agents/{id}` (agent enable/disable).

All are thin pass-throughs following the existing `withBackend` pattern. Read
`node_modules/next/dist/docs/` before writing route handlers (per frontend
`AGENTS.md`, this Next.js has breaking changes vs. training data).

### 0.5 Frontend — Scan page (`app/scan/page.tsx`)

Stacked top-to-bottom, matching the page's existing HUD/mono aesthetic:

1. Fleet strip + launch grid (unchanged).
2. **Active Job** section (unchanged).
3. **↓ NEW: Queue / Recent Jobs** — a `RecentJobs` component below Active Job:
   the last N jobs, each row = engagement · use-case · status chip
   (queued/running/done/failed/canceled) · **priority control** · timestamp.
   Controls per **pending** row: raise/lower priority (High/Normal/Low or ↑/↓) →
   `PATCH`, and **cancel** → `PATCH action:cancel`. Optimistic update, then
   reconcile from the next fetch. Re-fetches when the active `job` flips to
   completed/failed (reusing the existing poll signal), plus a 15s idle poll.
4. Optional: a small **disable-probe** control in `FleetStrip` (kill-switch).

Priority UI reads as a 3-level control (High / Normal / Low mapping to e.g.
`10 / 0 / -10`) to keep the operator model simple; the column stores the int.

### 0.6 Edge cases (Phase 0)

- Reprioritize/cancel affect **pending only**; PATCH is conditional
  (`WHERE status = pending`) → `409` on race with a claim.
- Canceled jobs are invisible to the claim query (filtered by `status = pending`).
- Disabled agent mid-job: current leased job completes; no new claims; heartbeat
  `403` → the agent surfaces as offline in the fleet list.
- Migrations: `priority` defaults 0 for existing rows; `canceled` added to the
  enum without rewriting rows; `disabled` defaults false.
- Multi-tenancy: every new endpoint filters by `current_user.tenant_id`.

### 0.7 Testing (Phase 0)

**Backend (pytest):**
- Priority ordering: two pending jobs, higher `priority` is claimed first.
- Aging is out of scope (Phase 3) — a same-priority pair still claims FIFO.
- Disabled agent: `get_agent_jobs` and heartbeat return `403`.
- Cancel pending → job no longer claimable; cancel running → `409`.
- Reprioritize running → `409`.
- `recent` endpoint returns tenant-scoped rows with `use_case_id`/names.
- Migration smoke: upgrade + downgrade clean.

**Frontend:**
- Queue renders each status; priority control issues the correct `PATCH`;
  optimistic update reconciles with the follow-up fetch.

### 0.8 Success criteria

- An operator sets a pending job's priority from the dashboard and the probe
  claims higher-priority jobs first.
- An operator cancels a pending job from the dashboard.
- An operator disables a probe and it stops receiving new jobs within one poll.
- The recent-jobs queue is visible on the scan page with live status.

### 0.9 Non-goals (Phase 0)

Enrollment token; running-job cancel; pause/resume; pin-to-probe; anti-starvation
aging; the Revalidation Matrix (tracked separately as an analytics add-on).

---

## Open follow-ups (not blocking Phase 0)

- **Revalidation Matrix** (per-scan New / Patched / Open + severity) — a separate
  analytics feature built on the existing `detection_runs` data; deferred.
- **Weak default secret** — `.env` contains a literal `ChangeMe123!`. Flag for
  rotation before any non-local deployment; unrelated to this spec but noted.
