# Probe Fleet Phase 0 — Queue Control + Revocation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give operators dashboard-driven control of the scan-job queue (priority + cancel) and a probe kill-switch (disable), so the fleet can be steered from the manager before onboarding is automated in later phases.

**Architecture:** Add a `priority` int and a `canceled` status to `ScanJob`, and a `disabled` bool to `Agent`. The HTTP job-claim query orders by `(priority desc, created_at asc)` and rejects disabled agents. New operator endpoints set priority, cancel pending jobs, toggle agent disable, and list recent jobs tenant-wide. A `RecentJobs` queue section on the scan page renders and drives them through thin Next.js BFF proxies.

**Tech Stack:** FastAPI + SQLAlchemy 2.0 (async) + Alembic + Postgres (backend); Next.js 16 App Router + React (frontend). Tests: pytest (backend unit style — mock DB with `AsyncMock` side_effects).

## Global Constraints

- Backend router file: `manager/backend/app/routers/agents.py` (prefix `/agents`); engagement routes in `manager/backend/app/routers/engagements.py`.
- All operator endpoints authenticate via `AuthUser` (FastAPI dependency) and filter by `current_user.tenant_id`. Agent enable/disable requires `require_role(["admin", "manager"])`.
- Migrations are sequential integer revisions in `manager/backend/alembic/versions/`. Current head is `0015`. Confirm with `ls manager/backend/alembic/versions | sort | tail -1` before writing; chain `down_revision` accordingly.
- Postgres 12+ is assumed (enum `ADD VALUE` runs inside the migration transaction because the new value is not used in the same transaction).
- Frontend: this is Next.js 16 with breaking changes vs. training data — dynamic route context is `{ params: Promise<{ id: string }> }`. Read `manager/frontend/node_modules/next/dist/docs/` before writing route handlers (per `manager/frontend/AGENTS.md`).
- Priority operator model: 3 UI levels **High / Normal / Low → `10 / 0 / -10`** over the int column.
- Run backend tests from `manager/backend/` with `pytest`. Run frontend build from `manager/frontend/`.
- Reprioritize/cancel affect **pending jobs only**; the conditional `UPDATE ... WHERE status = pending` returns `409` on a race with a claim.

---

### Task 1: `Agent.disabled` kill-switch (model + migration + poll/heartbeat rejection)

**Files:**
- Modify: `manager/backend/app/models/agent.py` (add column after `public_key`, ~line 39)
- Create: `manager/backend/alembic/versions/0016_agent_disabled.py`
- Modify: `manager/backend/app/routers/agents.py:613` (`get_agent_jobs`) and `:543` (`heartbeat`)
- Test: `manager/backend/tests/test_agents.py`

**Interfaces:**
- Produces: `Agent.disabled: bool` (default `False`). `get_agent_jobs` and `heartbeat` raise `HTTPException(403, "agent disabled")` when `agent.disabled` is true.

- [ ] **Step 1: Write the failing test**

Add to `manager/backend/tests/test_agents.py` inside `class TestGetAgentJobs`:

```python
    @pytest.mark.asyncio
    async def test_disabled_agent_is_denied_jobs(self):
        agent = SimpleNamespace(
            id=uuid.uuid4(),
            tenant_id=uuid.uuid4(),
            capabilities=["discovery"],
            network_segments=[],
            disabled=True,
        )
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
        ])
        with pytest.raises(HTTPException) as exc:
            await ag.get_agent_jobs(agent.id, db, limit=1)
        assert exc.value.status_code == 403
```

Ensure the test module imports `HTTPException` (add `from fastapi import HTTPException` near the top of the test file if absent).

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && pytest tests/test_agents.py::TestGetAgentJobs::test_disabled_agent_is_denied_jobs -v`
Expected: FAIL — `AttributeError`/no 403 raised (column + check don't exist).

- [ ] **Step 3: Add the model column**

In `manager/backend/app/models/agent.py`, after the `public_key` line (~39):

```python
    public_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Operator kill-switch. A disabled probe keeps its JWT but is denied new jobs
    # and heartbeats at the API boundary (stateless-JWT revocation path).
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
```

Ensure `Boolean` is imported — the top of `agent.py` imports from `sqlalchemy`; add `Boolean` to that import list if missing.

- [ ] **Step 4: Add the migration**

Create `manager/backend/alembic/versions/0016_agent_disabled.py`:

```python
"""Add Agent.disabled kill-switch.

Revision ID: 0016
Revises: 0015
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0016"
down_revision: Union[str, None] = "0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "agents",
        sa.Column("disabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )


def downgrade() -> None:
    op.drop_column("agents", "disabled")
```

(Confirm `agents` is the table name via `Agent.__tablename__`; adjust if different.)

- [ ] **Step 5: Add the kill-switch checks**

In `get_agent_jobs` (`agents.py`), right after the `if not agent: raise HTTPException(404, ...)` block (~line 628):

```python
    if not agent:
        raise HTTPException(404, "Agent not found")
    if getattr(agent, "disabled", False):
        raise HTTPException(403, "agent disabled")
```

In `heartbeat` (`agents.py`), after its `if not agent: raise HTTPException(404, ...)` (~line 552):

```python
    if not agent:
        raise HTTPException(404, "Agent not found")
    if getattr(agent, "disabled", False):
        raise HTTPException(403, "agent disabled")
```

(`getattr(..., False)` keeps the existing `SimpleNamespace`-based tests that omit `disabled` green.)

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd manager/backend && pytest tests/test_agents.py::TestGetAgentJobs -v`
Expected: PASS (new test + all existing `TestGetAgentJobs` tests).

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/models/agent.py manager/backend/alembic/versions/0016_agent_disabled.py manager/backend/app/routers/agents.py manager/backend/tests/test_agents.py
git commit -m "feat(agents): add Agent.disabled kill-switch denying jobs + heartbeat"
```

---

### Task 2: `ScanJob.priority` + `canceled` status + priority-ordered claim

**Files:**
- Modify: `manager/backend/app/models/scan_job.py` (add `priority` column)
- Modify: `manager/backend/app/models/enums.py:69` (`ScanJobStatus` — add `canceled`)
- Create: `manager/backend/alembic/versions/0017_scanjob_priority.py`
- Modify: `manager/backend/app/routers/agents.py:642` (claim `order_by`)
- Test: `manager/backend/tests/test_agents.py`

**Interfaces:**
- Produces: `ScanJob.priority: int` (default `0`, indexed), `ScanJobStatus.canceled = "canceled"`. Claim query orders by `ScanJob.priority.desc(), ScanJob.created_at.asc()`.

- [ ] **Step 1: Write the failing test**

Add to `manager/backend/tests/test_agents.py` inside `class TestGetAgentJobs`:

```python
    @pytest.mark.asyncio
    async def test_claim_query_orders_by_priority_then_created(self):
        agent = SimpleNamespace(
            id=uuid.uuid4(), tenant_id=uuid.uuid4(),
            capabilities=["discovery"], network_segments=["10.0.0.0/16"],
            disabled=False,
        )
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(all=lambda: []),
        ])
        await ag.get_agent_jobs(agent.id, db, limit=1)
        candidate_query = str(db.execute.await_args_list[1].args[0]).lower()
        assert "priority" in candidate_query
        assert candidate_query.index("priority") < candidate_query.index("created_at")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && pytest tests/test_agents.py::TestGetAgentJobs::test_claim_query_orders_by_priority_then_created -v`
Expected: FAIL — `priority` not in the ORDER BY.

- [ ] **Step 3: Add the enum value**

In `manager/backend/app/models/enums.py`, extend `ScanJobStatus`:

```python
class ScanJobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    canceled = "canceled"
```

- [ ] **Step 4: Add the model column**

In `manager/backend/app/models/scan_job.py`, after the `status` column (~line 25) add:

```python
    # Operator-set claim priority. Higher runs first; ties break FIFO by created_at.
    # Anti-starvation aging is a later phase (documented limitation).
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0", index=True
    )
```

Add `Integer` to the `from sqlalchemy import ...` line at the top of `scan_job.py`.

- [ ] **Step 5: Add the migration**

Create `manager/backend/alembic/versions/0017_scanjob_priority.py`:

```python
"""Add ScanJob.priority and the 'canceled' job status.

Revision ID: 0017
Revises: 0016
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0017"
down_revision: Union[str, None] = "0016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "scan_jobs",
        sa.Column("priority", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )
    op.create_index("ix_scan_jobs_priority", "scan_jobs", ["priority"])
    # PG 12+: ADD VALUE is safe inside the migration txn because it is not used here.
    op.execute("ALTER TYPE scanjobstatus ADD VALUE IF NOT EXISTS 'canceled'")


def downgrade() -> None:
    op.drop_index("ix_scan_jobs_priority", table_name="scan_jobs")
    op.drop_column("scan_jobs", "priority")
    # Postgres cannot drop an enum value cleanly; 'canceled' is left in place.
```

- [ ] **Step 6: Change the claim ordering**

In `agents.py` `get_agent_jobs` (~line 642), replace:

```python
        .order_by(ScanJob.created_at)
```

with:

```python
        .order_by(ScanJob.priority.desc(), ScanJob.created_at.asc())
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `cd manager/backend && pytest tests/test_agents.py::TestGetAgentJobs -v`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add manager/backend/app/models/scan_job.py manager/backend/app/models/enums.py manager/backend/alembic/versions/0017_scanjob_priority.py manager/backend/app/routers/agents.py manager/backend/tests/test_agents.py
git commit -m "feat(jobs): priority-ordered claim + canceled status"
```

---

### Task 3: `GET /agents/jobs/recent` — tenant-wide queue feed

**Files:**
- Modify: `manager/backend/app/routers/agents.py` (add endpoint near `get_job_status`, ~line 704)
- Test: `manager/backend/tests/test_agents.py`

**Interfaces:**
- Produces: `GET /agents/jobs/recent?limit=N` → list (newest-first) of
  `{ job_id, engagement_id, engagement_name, use_case_id, job_type, status, priority, agent_id, agent_name, created_at, started_at, completed_at }`.
  `use_case_id` read from `job.result` params; names via left joins. Default `limit=5`, max `100`.

- [ ] **Step 1: Write the failing test**

Add a new class to `manager/backend/tests/test_agents.py`:

```python
class TestRecentJobs:

    @pytest.mark.asyncio
    async def test_recent_jobs_shape(self):
        tenant_id = uuid.uuid4()
        job = SimpleNamespace(
            id=uuid.uuid4(), engagement_id=uuid.uuid4(),
            job_type=SimpleNamespace(value="discovery"),
            status=SimpleNamespace(value="pending"),
            priority=10, agent_id=None,
            result={"use_case_id": "uc_discovery_only"},
            created_at=None, started_at=None, completed_at=None,
        )
        row = (job, "Acme Q3", None)  # (ScanJob, engagement_name, agent_name)
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(all=lambda: [row]))
        current_user = SimpleNamespace(tenant_id=tenant_id)

        out = await ag.recent_jobs(db, current_user, limit=5)
        assert out[0]["use_case_id"] == "uc_discovery_only"
        assert out[0]["engagement_name"] == "Acme Q3"
        assert out[0]["priority"] == 10
        assert out[0]["status"] == "pending"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && pytest tests/test_agents.py::TestRecentJobs -v`
Expected: FAIL — `recent_jobs` does not exist.

- [ ] **Step 3: Implement the endpoint**

In `agents.py`, add (after `get_job_status`, and add `Query` to the `fastapi` import: `from fastapi import APIRouter, HTTPException, Query, Request, status`):

```python
@router.get("/jobs/recent", summary="Tenant-wide recent scan jobs for the dashboard queue")
async def recent_jobs(
    db: DB,
    current_user: AuthUser,
    limit: int = Query(default=5, ge=1, le=100),
):
    rows = (await db.execute(
        select(ScanJob, Engagement.name, Agent.name)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .outerjoin(Agent, ScanJob.agent_id == func.cast(Agent.id, String))
        .where(Engagement.tenant_id == current_user.tenant_id)
        .order_by(ScanJob.created_at.desc())
        .limit(limit)
    )).all()

    out = []
    for job, engagement_name, agent_name in rows:
        params = job.result or {}
        out.append({
            "job_id": str(job.id),
            "engagement_id": str(job.engagement_id),
            "engagement_name": engagement_name,
            "use_case_id": params.get("use_case_id"),
            "job_type": job.job_type.value if hasattr(job.job_type, "value") else str(job.job_type),
            "status": job.status.value if hasattr(job.status, "value") else str(job.status),
            "priority": getattr(job, "priority", 0),
            "agent_id": job.agent_id,
            "agent_name": agent_name,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        })
    return out
```

Add the imports this uses at the top of `agents.py`:
- `from sqlalchemy import String, func, select, update` (extend the existing `from sqlalchemy import select, update`).

Note: `ScanJob.agent_id` is a `String` column holding the agent UUID as text, so the outer join casts `Agent.id` to `String`. Verify against `Agent.id` type; if a direct comparison already works in this codebase, prefer it.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && pytest tests/test_agents.py::TestRecentJobs -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/routers/agents.py manager/backend/tests/test_agents.py
git commit -m "feat(agents): GET /agents/jobs/recent tenant-wide queue feed"
```

---

### Task 4: `PATCH /agents/jobs/{job_id}` — set priority / cancel (conditional)

**Files:**
- Modify: `manager/backend/app/routers/agents.py` (add endpoint + request model)
- Test: `manager/backend/tests/test_agents.py`

**Interfaces:**
- Produces: `PATCH /agents/jobs/{job_id}` with body `JobPatchRequest { priority: int | None, action: "cancel" | None }`.
  Conditional `UPDATE ... WHERE id=job_id AND status=pending AND engagement in tenant`. Returns `{ "ok": True, "job_id", "priority?", "status?" }`. Raises `409` if no row updated (already running/claimed) and `404` if the job isn't in the caller's tenant.

- [ ] **Step 1: Write the failing test**

Add to `manager/backend/tests/test_agents.py`:

```python
class TestPatchJob:

    @pytest.mark.asyncio
    async def test_set_priority_on_pending_job(self):
        job_id = uuid.uuid4()
        current_user = SimpleNamespace(tenant_id=uuid.uuid4())
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: job_id),   # tenant/existence check
            SimpleNamespace(rowcount=1),                     # conditional update
        ])
        db.flush = AsyncMock()
        body = ag.JobPatchRequest(priority=10, action=None)
        out = await ag.patch_job(job_id, body, db, current_user)
        assert out["ok"] is True
        assert out["priority"] == 10

    @pytest.mark.asyncio
    async def test_cancel_running_job_conflicts(self):
        job_id = uuid.uuid4()
        current_user = SimpleNamespace(tenant_id=uuid.uuid4())
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: job_id),   # exists in tenant
            SimpleNamespace(rowcount=0),                     # nothing pending to cancel
        ])
        db.flush = AsyncMock()
        body = ag.JobPatchRequest(priority=None, action="cancel")
        with pytest.raises(HTTPException) as exc:
            await ag.patch_job(job_id, body, db, current_user)
        assert exc.value.status_code == 409
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && pytest tests/test_agents.py::TestPatchJob -v`
Expected: FAIL — `JobPatchRequest` / `patch_job` do not exist.

- [ ] **Step 3: Implement the model + endpoint**

In `agents.py` add the request model (near the other `BaseModel` request classes):

```python
class JobPatchRequest(BaseModel):
    priority: int | None = None
    action: str | None = None  # "cancel" | None

    @field_validator("action")
    @classmethod
    def _valid_action(cls, v):
        if v not in (None, "cancel"):
            raise ValueError("action must be 'cancel' or omitted")
        return v
```

And the endpoint:

```python
@router.patch("/jobs/{job_id}", summary="Set priority or cancel a pending scan job")
async def patch_job(
    job_id: uuid.UUID,
    body: JobPatchRequest,
    db: DB,
    current_user: AuthUser,
):
    # Existence + tenant scoping: the job's engagement must belong to the caller's tenant.
    owned = (await db.execute(
        select(ScanJob.id)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(ScanJob.id == job_id, Engagement.tenant_id == current_user.tenant_id)
    )).scalar_one_or_none()
    if owned is None:
        raise HTTPException(404, "Job not found")

    values: dict = {}
    if body.priority is not None:
        values["priority"] = body.priority
    if body.action == "cancel":
        values["status"] = ScanJobStatus.canceled
    if not values:
        raise HTTPException(400, "nothing to update")

    # Conditional: only a still-pending job may be reprioritized or canceled.
    # A job claimed between the read above and this update yields rowcount == 0.
    rowcount = (await db.execute(
        update(ScanJob)
        .where(ScanJob.id == job_id, ScanJob.status == ScanJobStatus.pending)
        .values(**values)
        .execution_options(synchronize_session=False)
    )).rowcount
    if not rowcount:
        raise HTTPException(409, "job already running or not pending")
    await db.flush()

    out: dict = {"ok": True, "job_id": str(job_id)}
    if body.priority is not None:
        out["priority"] = body.priority
    if body.action == "cancel":
        out["status"] = ScanJobStatus.canceled.value
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd manager/backend && pytest tests/test_agents.py::TestPatchJob -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/routers/agents.py manager/backend/tests/test_agents.py
git commit -m "feat(agents): PATCH /agents/jobs/{id} set-priority + cancel (conditional 409)"
```

---

### Task 5: `PATCH /agents/{agent_id}` disable toggle + extend engagement jobs

**Files:**
- Modify: `manager/backend/app/routers/agents.py` (add `patch_agent` + `AgentPatchRequest`)
- Modify: `manager/backend/app/routers/engagements.py:608-620` (`list_engagement_jobs` response)
- Test: `manager/backend/tests/test_agents.py`

**Interfaces:**
- Produces: `PATCH /agents/{agent_id}` body `AgentPatchRequest { disabled: bool }`, role admin/manager → `{ "ok": True, "agent_id", "disabled" }`, `404` if not in tenant. `list_engagement_jobs` rows gain `priority` and `use_case_id`.

- [ ] **Step 1: Write the failing test**

Add to `manager/backend/tests/test_agents.py`:

```python
class TestPatchAgent:

    @pytest.mark.asyncio
    async def test_disable_agent(self):
        agent = SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), disabled=False)
        current_user = SimpleNamespace(tenant_id=agent.tenant_id)
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: agent))
        db.flush = AsyncMock()
        out = await ag.patch_agent(agent.id, ag.AgentPatchRequest(disabled=True), db, current_user)
        assert out["disabled"] is True
        assert agent.disabled is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && pytest tests/test_agents.py::TestPatchAgent -v`
Expected: FAIL — `patch_agent` / `AgentPatchRequest` do not exist.

- [ ] **Step 3: Implement the model + endpoint**

In `agents.py`:

```python
class AgentPatchRequest(BaseModel):
    disabled: bool


@router.patch("/{agent_id}", summary="Enable/disable a probe (operator kill-switch)")
async def patch_agent(
    agent_id: uuid.UUID,
    body: AgentPatchRequest,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    agent = (await db.execute(
        select(Agent).where(Agent.id == agent_id, Agent.tenant_id == current_user.tenant_id)
    )).scalar_one_or_none()
    if agent is None:
        raise HTTPException(404, "Agent not found")
    agent.disabled = body.disabled
    await db.flush()
    return {"ok": True, "agent_id": str(agent_id), "disabled": body.disabled}
```

- [ ] **Step 4: Extend `list_engagement_jobs`**

In `engagements.py` (~line 608), add `priority` and `use_case_id` to each returned dict:

```python
    return [
        {
            "id": str(j.id),
            "job_type": j.job_type.value if hasattr(j.job_type, "value") else str(j.job_type),
            "status": j.status.value if hasattr(j.status, "value") else str(j.status),
            "priority": getattr(j, "priority", 0),
            "use_case_id": (j.result or {}).get("use_case_id"),
            "agent_id": j.agent_id,
            "result": j.result,
            "created_at": j.created_at.isoformat() if j.created_at else None,
            "started_at": j.started_at.isoformat() if j.started_at else None,
            "completed_at": j.completed_at.isoformat() if j.completed_at else None,
        }
        for j in rows
    ]
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd manager/backend && pytest tests/test_agents.py::TestPatchAgent tests/test_engagement_lists.py -v`
Expected: PASS.

- [ ] **Step 6: Run the full backend suite (guard against regressions)**

Run: `cd manager/backend && pytest -q`
Expected: PASS (no regressions in agents/engagements/job tests).

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/routers/agents.py manager/backend/app/routers/engagements.py manager/backend/tests/test_agents.py
git commit -m "feat(agents): PATCH /agents/{id} disable toggle; engagement jobs expose priority + use_case_id"
```

---

### Task 6: BFF proxies — recent-jobs, job PATCH, probe PATCH

**Files:**
- Modify: `manager/frontend/app/api/scan/jobs/[id]/route.ts` (add `PATCH`)
- Create: `manager/frontend/app/api/scan/recent-jobs/route.ts`
- Create: `manager/frontend/app/api/scan/probes/[id]/route.ts`

**Interfaces:**
- Consumes: backend `GET /agents/jobs/recent`, `PATCH /agents/jobs/{id}`, `PATCH /agents/{id}`.
- Produces: `GET /api/scan/recent-jobs`, `PATCH /api/scan/jobs/{id}`, `PATCH /api/scan/probes/{id}` (all bearer-authenticated via `withBackend`).

- [ ] **Step 1: Add `GET /api/scan/recent-jobs`**

Create `manager/frontend/app/api/scan/recent-jobs/route.ts`:

```ts
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

// GET /api/scan/recent-jobs → proxies to manager GET /agents/jobs/recent
export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const limit = url.searchParams.get("limit") ?? "5";
  const jobs = await backend<unknown[]>("/agents/jobs/recent", { token, query: { limit } });
  return NextResponse.json(jobs ?? []);
});
```

- [ ] **Step 2: Add `PATCH` to the job route**

In `manager/frontend/app/api/scan/jobs/[id]/route.ts`, append (keep the existing `GET` export and imports; the file already imports `backend`, `withBackend`, `NextRequest`, `NextResponse`):

```ts
// PATCH /api/scan/jobs/[id] → proxies to manager PATCH /agents/jobs/{job_id}
export const PATCH = withBackend(async (
  req: NextRequest,
  { token },
  params?: { id?: string },
) => {
  const jobId = params?.id;
  if (!jobId) {
    return NextResponse.json({ error: "job id required" }, { status: 400 });
  }
  const body = await req.json();
  const res = await backend<unknown>(`/agents/jobs/${jobId}`, { token, method: "PATCH", body });
  return NextResponse.json(res);
});
```

- [ ] **Step 3: Add `PATCH /api/scan/probes/[id]`**

Create `manager/frontend/app/api/scan/probes/[id]/route.ts`:

```ts
import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { withBackend } from "../../../../../lib/with-backend";

// PATCH /api/scan/probes/[id] → proxies to manager PATCH /agents/{agent_id}
export const PATCH = withBackend(async (
  req: NextRequest,
  { token },
  params?: { id?: string },
) => {
  const agentId = params?.id;
  if (!agentId) {
    return NextResponse.json({ error: "agent id required" }, { status: 400 });
  }
  const body = await req.json();
  const res = await backend<unknown>(`/agents/${agentId}`, { token, method: "PATCH", body });
  return NextResponse.json(res);
});
```

- [ ] **Step 4: Verify the frontend compiles**

Run: `cd manager/frontend && npx tsc --noEmit -p tsconfig.json`
Expected: no new type errors in the three touched files.

- [ ] **Step 5: Commit**

```bash
git add manager/frontend/app/api/scan/recent-jobs/route.ts manager/frontend/app/api/scan/jobs/[id]/route.ts manager/frontend/app/api/scan/probes/[id]/route.ts
git commit -m "feat(bff): recent-jobs feed + job/probe PATCH proxies"
```

---

### Task 7: Scan page `RecentJobs` queue section (render + priority + cancel)

**Files:**
- Modify: `manager/frontend/app/scan/page.tsx` (add `RecentJob` type, `RecentJobs` component, render below the Active Job section, refetch wiring)

**Interfaces:**
- Consumes: `GET /api/scan/recent-jobs`, `PATCH /api/scan/jobs/{id}`.
- Produces: a `RecentJobs` React component rendered after the Active Job `<section>`.

- [ ] **Step 1: Add the type**

In `manager/frontend/app/scan/page.tsx`, after the `JobStatus` interface (~line 58) add:

```tsx
interface RecentJob {
  job_id: string;
  engagement_id: string;
  engagement_name: string | null;
  use_case_id: string | null;
  job_type: string;
  status: "pending" | "running" | "completed" | "failed" | "canceled";
  priority: number;
  agent_id: string | null;
  agent_name: string | null;
  created_at: string | null;
  started_at: string | null;
  completed_at: string | null;
}

const PRIORITY_LEVELS: { label: string; value: number }[] = [
  { label: "High",   value: 10 },
  { label: "Normal", value: 0 },
  { label: "Low",    value: -10 },
];
```

- [ ] **Step 2: Add the `RecentJobs` component**

In `page.tsx`, before `export default function ScanPage()`:

```tsx
function relTime(iso: string | null): string {
  if (!iso) return "—";
  const s = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 1000));
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return `${Math.floor(s / 86400)}d ago`;
}

function RecentJobs({ jobs, onPriority, onCancel }: {
  jobs: RecentJob[];
  onPriority: (jobId: string, value: number) => void;
  onCancel: (jobId: string) => void;
}) {
  const CHIP: Record<RecentJob["status"], { color: string; label: string }> = {
    pending:   { color: "var(--text-muted)",         label: "Queued"    },
    running:   { color: "var(--accent)",             label: "Running"   },
    completed: { color: "var(--nominal-color)",      label: "Done"      },
    failed:    { color: "var(--sev-critical-color)", label: "Failed"    },
    canceled:  { color: "var(--text-faint)",         label: "Canceled"  },
  };
  if (!jobs.length) {
    return <div style={{ fontSize: 12, color: "var(--text-muted)", padding: "8px 2px" }}>No recent jobs yet.</div>;
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {jobs.map((j) => {
        const chip = CHIP[j.status] ?? CHIP.pending;
        const pending = j.status === "pending";
        return (
          <div key={j.job_id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 14px", borderRadius: 10, background: "var(--bg-panel)", border: "0.5px solid var(--border-subtle)" }}>
            <span style={{ width: 7, height: 7, borderRadius: "50%", background: chip.color, flexShrink: 0 }} />
            <div style={{ minWidth: 0, flex: 1 }}>
              <div style={{ fontSize: 12.5, fontWeight: 600, color: "var(--text-primary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {j.engagement_name ?? j.engagement_id.slice(0, 8)}
                <span style={{ color: "var(--text-faint)", fontWeight: 400 }}> · {j.use_case_id ?? j.job_type}</span>
              </div>
              <div style={{ fontSize: 10.5, color: "var(--text-muted)", fontFamily: "var(--font-mono)", marginTop: 2 }}>
                {chip.label} · {relTime(j.created_at)}{j.agent_name ? ` · ${j.agent_name}` : ""}
              </div>
            </div>
            {pending ? (
              <>
                <select
                  aria-label="priority"
                  value={j.priority}
                  onChange={(e) => onPriority(j.job_id, Number(e.target.value))}
                  className="scn-input scn-select"
                  style={{ width: 96, fontSize: 11 }}
                >
                  {PRIORITY_LEVELS.map((p) => <option key={p.value} value={p.value}>{p.label}</option>)}
                </select>
                <button onClick={() => onCancel(j.job_id)} className="scn-chip" title="Cancel this queued job">Cancel</button>
              </>
            ) : (
              <span style={{ fontSize: 10, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>
                {j.priority > 0 ? "High" : j.priority < 0 ? "Low" : "Normal"}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}
```

- [ ] **Step 3: Add state + fetch + handlers in `ScanPage`**

Inside `ScanPage`, after the existing `job` state (~line 569), add:

```tsx
  const [recentJobs, setRecentJobs] = useState<RecentJob[]>([]);

  const loadRecentJobs = useCallback(async () => {
    try {
      const rows = await apiFetch<RecentJob[]>("/api/scan/recent-jobs?limit=5");
      setRecentJobs(rows);
    } catch { /* transient */ }
  }, []);

  useEffect(() => {
    loadRecentJobs();
    const t = setInterval(loadRecentJobs, 15000);
    return () => clearInterval(t);
  }, [loadRecentJobs]);

  // Refresh the queue whenever the active job reaches a terminal state.
  useEffect(() => {
    if (job && (job.status === "completed" || job.status === "failed")) loadRecentJobs();
  }, [job?.status]); // eslint-disable-line react-hooks/exhaustive-deps

  const setJobPriority = useCallback(async (jobId: string, value: number) => {
    setRecentJobs((prev) => prev.map((j) => j.job_id === jobId ? { ...j, priority: value } : j));
    try {
      await apiFetch(`/api/scan/jobs/${jobId}`, { method: "PATCH", body: JSON.stringify({ priority: value }) });
      toastOk("Priority updated");
    } catch (e) { toastErr("Update failed", (e as Error).message); }
    loadRecentJobs();
  }, [loadRecentJobs, toastOk, toastErr]);

  const cancelJob = useCallback(async (jobId: string) => {
    try {
      await apiFetch(`/api/scan/jobs/${jobId}`, { method: "PATCH", body: JSON.stringify({ action: "cancel" }) });
      toastOk("Job canceled");
    } catch (e) { toastErr("Cancel failed", (e as Error).message); }
    loadRecentJobs();
  }, [loadRecentJobs, toastOk, toastErr]);
```

Also call `loadRecentJobs()` at the end of the existing `launch()` success path (right after `toastOk("Job queued", ...)`), so a freshly queued job appears immediately.

- [ ] **Step 4: Render the section**

In `page.tsx`, immediately after the closing `</section>` of the Active Job block (the `{job && (<section>…</section>)}`, ~line 914), add:

```tsx
        <section>
          <SectionLabel>Queue · Recent Jobs</SectionLabel>
          <RecentJobs jobs={recentJobs} onPriority={setJobPriority} onCancel={cancelJob} />
        </section>
```

- [ ] **Step 5: Verify the frontend compiles**

Run: `cd manager/frontend && npx tsc --noEmit -p tsconfig.json`
Expected: no new type errors.

- [ ] **Step 6: Manual smoke (if a dev stack is available)**

Run the manager + frontend (`docker compose up -d` per repo docs), open `/scan`, launch a scan, confirm the job appears under "Queue · Recent Jobs", that changing its priority while pending persists after refresh, and that Cancel moves it to Canceled. If no stack is available, note this step as deferred to QA.

- [ ] **Step 7: Commit**

```bash
git add manager/frontend/app/scan/page.tsx
git commit -m "feat(scan): Queue/Recent Jobs section with priority + cancel controls"
```

---

### Task 8: Probe kill-switch control in the fleet strip

**Files:**
- Modify: `manager/frontend/app/scan/page.tsx` (`FleetStrip` — add a disable toggle per probe; pass a handler from `ScanPage`)

**Interfaces:**
- Consumes: `PATCH /api/scan/probes/{id}`.
- Produces: a per-probe enable/disable control that refreshes the probe list.

- [ ] **Step 1: Add a disable handler + probe reload in `ScanPage`**

In `ScanPage`, add (near `loadRecentJobs`):

```tsx
  const reloadProbes = useCallback(async () => {
    try { setProbes(await apiFetch<Probe[]>("/api/scan/probes")); } catch { /* transient */ }
  }, []);

  const setProbeDisabled = useCallback(async (agentId: string, disabled: boolean) => {
    try {
      await apiFetch(`/api/scan/probes/${agentId}`, { method: "PATCH", body: JSON.stringify({ disabled }) });
      toastOk(disabled ? "Probe disabled" : "Probe enabled");
    } catch (e) { toastErr("Update failed", (e as Error).message); }
    reloadProbes();
  }, [reloadProbes, toastOk, toastErr]);
```

- [ ] **Step 2: Thread the handler into `FleetStrip`**

Change the `FleetStrip` signature and its call site:

```tsx
function FleetStrip({ probes, loading, onToggleDisabled }: { probes: Probe[]; loading: boolean; onToggleDisabled: (agentId: string, disabled: boolean) => void }) {
```

Add a `disabled?: boolean` field to the `Probe` interface (~line 27):

```tsx
  online: boolean;
  disabled?: boolean;
```

In the per-probe chip (inside `probes.map`), add a small toggle button after the capabilities count:

```tsx
                  <button
                    onClick={() => onToggleDisabled(p.id, !p.disabled)}
                    className="scn-chip"
                    title={p.disabled ? "Enable probe" : "Disable probe (stops new jobs)"}
                    style={{ marginLeft: 4 }}
                  >
                    {p.disabled ? "Enable" : "Disable"}
                  </button>
```

Update the render call in `ScanPage`:

```tsx
        <FleetStrip probes={probes} loading={loadingData} onToggleDisabled={setProbeDisabled} />
```

- [ ] **Step 3: Surface `disabled` from the probes list**

The probes list comes from backend `GET /agents` (`list_agents`). Add `"disabled": a.disabled` to each dict in `list_agents` (`agents.py:529-539`), and pass it through the BFF (the `/api/scan/probes` GET returns the backend array as-is, so no BFF change needed).

- [ ] **Step 4: Verify the frontend compiles + backend test still green**

Run: `cd manager/frontend && npx tsc --noEmit -p tsconfig.json`
Run: `cd manager/backend && pytest tests/test_agents.py -q`
Expected: no type errors; backend tests pass.

- [ ] **Step 5: Commit**

```bash
git add manager/frontend/app/scan/page.tsx manager/backend/app/routers/agents.py
git commit -m "feat(scan): per-probe disable kill-switch in fleet strip"
```

---

## Self-Review

**Spec coverage:**
- 0.1 data model → Task 1 (`Agent.disabled`), Task 2 (`ScanJob.priority`, `canceled`). ✓
- 0.2 behavior (priority claim, kill-switch) → Task 2 (order_by), Task 1 (403 on poll + heartbeat). ✓
- 0.3 endpoints → recent (Task 3), PATCH job (Task 4), PATCH agent + extend engagement jobs (Task 5). ✓
- 0.4 BFF proxies → Task 6. ✓
- 0.5 frontend queue → Task 7; probe disable control → Task 8. ✓
- 0.6 edge cases (pending-only conditional 409, disabled surfaced) → Tasks 4, 1, 8. ✓
- 0.7 testing → tests in Tasks 1–5, tsc in 6–8, full suite in Task 5 Step 6. ✓

**Placeholder scan:** No TBD/TODO; every code step contains full code. The only deferred item is Task 7 Step 6 manual smoke, explicitly gated on stack availability (acceptable — it's a QA action, not code).

**Type consistency:** `JobPatchRequest{priority,action}` (Task 4) matches the BFF body `{ priority }` / `{ action: "cancel" }` (Task 6/7). `AgentPatchRequest{disabled}` (Task 5) matches `{ disabled }` (Task 6/8). `recent_jobs` response keys (Task 3) match the `RecentJob` interface (Task 7). `Agent.disabled` (Task 1) is read in `list_agents` (Task 8 Step 3) and the poll/heartbeat checks (Task 1).

**Known follow-ups (out of Phase 0 scope):** anti-starvation aging; cooperative cancel of *running* jobs; the WS push-selection ordering (only relevant if the WS path selects pending jobs — verify during Task 2 and mirror the order_by there if so).
