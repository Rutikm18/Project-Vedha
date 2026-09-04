"""
Operator job control: stop a running job, remove a queued one, and cap the queue.

The behaviours these lock down:
  * Cancelling a RUNNING job must BUMP THE FENCE and release the agent. The fence
    bump is the whole abort mechanism — lease renewal refuses a superseded fence,
    so the probe's next heartbeat 409s and it abandons the scan. Without the
    bump, cancel is cosmetic and the probe keeps working.
  * A cancelled job is terminal and is never re-offered to a probe.
  * `cancelled` is not `failed` — an operator decision must not read as a system
    fault.
  * The queue cap counts PENDING only, so it bounds the backlog rather than
    throttling work already underway.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import ScanJobStatus, ScanJobType
from app.routers import agents as ag
from app.schemas.auth import CurrentUser


def _user(user_id: uuid.UUID | None = None):
    """The REAL CurrentUser, not a SimpleNamespace.

    A hand-rolled stand-in is what let this endpoint ship broken: the fake had an
    `email` attribute, the real frozen JWT-claims model does not, and every test
    passed while production raised
    `AttributeError: 'CurrentUser' object has no attribute 'email'` -> HTTP 500.
    Constructing the actual model means the tests fail the moment the endpoint
    touches a field the token cannot carry."""
    return CurrentUser(
        user_id=user_id or uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="admin",
    )


def _job(status=ScanJobStatus.running, *, agent_id=None, attempt_id=None, fence=4):
    return SimpleNamespace(
        id=uuid.uuid4(),
        engagement_id=uuid.uuid4(),
        job_type=ScanJobType.discovery,
        status=status,
        agent_id=agent_id,
        current_attempt_id=attempt_id,
        current_fence=fence,
        lease_expires_at="lease",
        completed_at=None,
        result={"use_case_id": "network_va"},
    )


def _one(value):
    """A db.execute() result whose scalar_one_or_none() yields `value`."""
    return MagicMock(scalar_one_or_none=lambda: value)


def _count(n):
    return MagicMock(scalar_one=lambda: n)


def _db(*results):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=list(results))
    db.flush = AsyncMock()
    return db


# ── cancelling a queued job ──────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_pending_job_is_cancelled_and_freed():
    job = _job(ScanJobStatus.pending)
    db = _db(_one(job), _count(0))
    out = await ag.cancel_agent_job(job.id, db, _user())

    assert job.status is ScanJobStatus.cancelled
    assert out["was_running"] is False
    assert out["released_agent_id"] is None
    assert job.result["cancelled_while"] == "queued"


@pytest.mark.asyncio
async def test_cancel_records_who_did_it():
    """Attribution must come from a field the JWT actually carries."""
    actor = uuid.uuid4()
    job = _job(ScanJobStatus.pending)
    db = _db(_one(job), _count(0))
    await ag.cancel_agent_job(job.id, db, _user(actor))
    assert job.result["cancelled_by"] == str(actor)
    assert job.result["cancelled_at"]


# ── cancelling a running job: the fence bump IS the abort ────────────────────
@pytest.mark.asyncio
async def test_running_job_bumps_the_fence_to_abort_the_probe():
    job = _job(ScanJobStatus.running, agent_id=str(uuid.uuid4()), fence=7)
    db = _db(_one(job), _count(0))
    out = await ag.cancel_agent_job(job.id, db, _user())

    # The probe renews its lease against `current_fence`; a superseded fence makes
    # renew_job_attempt refuse, the heartbeat 409s, and the probe abandons the job.
    assert job.current_fence == 8, "fence must be superseded or cancel is cosmetic"
    assert job.status is ScanJobStatus.cancelled
    assert out["was_running"] is True


@pytest.mark.asyncio
async def test_running_job_releases_the_agent_for_the_next_queued_job():
    agent_id = str(uuid.uuid4())
    job = _job(ScanJobStatus.running, agent_id=agent_id)
    db = _db(_one(job), _count(2))
    out = await ag.cancel_agent_job(job.id, db, _user())

    assert job.agent_id is None and job.lease_expires_at is None
    assert job.current_attempt_id is None
    assert out["released_agent_id"] == agent_id
    assert out["pending_remaining"] == 2      # what the probe picks up next


@pytest.mark.asyncio
async def test_open_attempt_is_closed_as_cancelled():
    attempt = SimpleNamespace(id=uuid.uuid4(), status="running",
                              ended_at=None, error=None)
    job = _job(ScanJobStatus.running, agent_id=str(uuid.uuid4()),
               attempt_id=attempt.id)
    actor = uuid.uuid4()
    db = _db(_one(job), _one(attempt), _count(0))
    await ag.cancel_agent_job(job.id, db, _user(actor))

    assert attempt.status == "cancelled"      # audit trail shows a stop, not a gap
    assert attempt.ended_at is not None
    assert str(actor) in attempt.error


@pytest.mark.asyncio
async def test_missing_attempt_row_does_not_break_cancel():
    job = _job(ScanJobStatus.running, agent_id=str(uuid.uuid4()),
               attempt_id=uuid.uuid4())
    db = _db(_one(job), _one(None), _count(0))
    await ag.cancel_agent_job(job.id, db, _user())
    assert job.status is ScanJobStatus.cancelled


# ── refusals ─────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
@pytest.mark.parametrize("terminal", [ScanJobStatus.completed,
                                      ScanJobStatus.failed,
                                      ScanJobStatus.cancelled])
async def test_terminal_jobs_cannot_be_cancelled(terminal):
    job = _job(terminal)
    db = _db(_one(job))
    with pytest.raises(HTTPException) as e:
        await ag.cancel_agent_job(job.id, db, _user())
    assert e.value.status_code == 409
    assert job.status is terminal             # untouched


@pytest.mark.asyncio
async def test_job_outside_the_tenant_is_not_found():
    # The query joins on tenant_id, so a foreign job resolves to None -> 404,
    # never a 403 that would confirm the job exists.
    db = _db(_one(None))
    with pytest.raises(HTTPException) as e:
        await ag.cancel_agent_job(uuid.uuid4(), db, _user())
    assert e.value.status_code == 404


def test_cancelled_is_distinct_from_failed():
    """An operator stop must never be mistaken for a system fault."""
    assert ScanJobStatus.cancelled.value == "cancelled"
    assert ScanJobStatus.cancelled is not ScanJobStatus.failed


# ── queue depth cap ──────────────────────────────────────────────────────────
class TestQueueLimit:
    def test_limit_is_three(self):
        assert ag.MAX_PENDING_JOBS_PER_ENGAGEMENT == 3

    @pytest.mark.asyncio
    async def test_pending_count_helper_counts(self):
        db = _db(_count(2))
        assert await ag._pending_job_count(db, uuid.uuid4()) == 2

    @pytest.mark.asyncio
    async def test_fourth_queued_job_is_refused(self):
        user = _user()
        eng = SimpleNamespace(id=uuid.uuid4(), tenant_id=user.tenant_id,
                              scope_cidrs=["10.0.0.0/24"], rules_of_engagement={},
                              excluded_cidrs=[])
        body = SimpleNamespace(
            job_type=ScanJobType.discovery, engagement_id=eng.id,
            params={"targets": ["10.0.0.5"]}, use_case_id=None, uc=None)
        db = _db(_one(eng), _count(3))          # engagement, then the queue count
        with pytest.raises(HTTPException) as e:
            await ag.enqueue_agent_job(body, db, MagicMock(), user)
        assert e.value.status_code == 409
        assert "Queue is full" in e.value.detail

    @pytest.mark.asyncio
    async def test_third_queued_job_is_still_accepted(self):
        """Two queued jobs must leave room for a third — an off-by-one here
        would silently cost the operator a slot."""
        user = _user()
        eng = SimpleNamespace(id=uuid.uuid4(), tenant_id=user.tenant_id,
                              scope_cidrs=["10.0.0.0/24"], rules_of_engagement={},
                              excluded_cidrs=[])
        body = SimpleNamespace(
            job_type=ScanJobType.discovery, engagement_id=eng.id,
            params={"targets": ["10.0.0.5"]}, use_case_id=None, uc=None)
        db = _db(_one(eng), _count(2))
        with pytest.raises(Exception) as e:      # proceeds past the cap, fails later
            await ag.enqueue_agent_job(body, db, MagicMock(), user)
        detail = getattr(e.value, "detail", "")
        assert "Queue is full" not in str(detail)


def test_current_user_has_no_email_field():
    """Pins the reason this endpoint may not reference `.email`.

    If CurrentUser ever gains an email claim, delete this test deliberately —
    do not let the endpoint start depending on one silently."""
    assert "email" not in CurrentUser.model_fields
