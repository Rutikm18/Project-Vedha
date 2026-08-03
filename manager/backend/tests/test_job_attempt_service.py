from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.scan_job_attempt import ScanJobAttempt
from app.services.job_attempt_service import claim_job_attempt, renew_job_attempt


@pytest.mark.asyncio
async def test_claim_creates_immutable_attempt_with_returned_fence() -> None:
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(first=lambda: (2, 7)))
    db.flush = AsyncMock()
    job_id = uuid.uuid4()
    agent_id = uuid.uuid4()

    claim = await claim_job_attempt(
        db,
        job_id=job_id,
        agent_id=agent_id,
        tenant_id=uuid.uuid4(),
    )

    assert claim is not None
    assert claim.attempt_number == 2
    assert claim.fence == 7
    attempt = db.add.call_args.args[0]
    assert isinstance(attempt, ScanJobAttempt)
    assert attempt.id == claim.attempt_id
    assert attempt.job_id == job_id
    assert attempt.agent_id == agent_id
    assert attempt.status == "running"
    db.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_lost_claim_does_not_create_attempt() -> None:
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(first=lambda: None))
    db.flush = AsyncMock()

    claim = await claim_job_attempt(
        db,
        job_id=uuid.uuid4(),
        agent_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
    )

    assert claim is None
    db.add.assert_not_called()
    db.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_stale_fence_cannot_renew_attempt() -> None:
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(rowcount=0))

    renewed = await renew_job_attempt(
        db,
        job_id=uuid.uuid4(),
        attempt_id=uuid.uuid4(),
        fence=4,
        agent_id=uuid.uuid4(),
    )

    assert renewed is False
    assert db.execute.await_count == 1


@pytest.mark.asyncio
async def test_current_fence_renews_attempt_and_logical_job() -> None:
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(rowcount=1),
        MagicMock(rowcount=1),
    ])

    renewed = await renew_job_attempt(
        db,
        job_id=uuid.uuid4(),
        attempt_id=uuid.uuid4(),
        fence=4,
        agent_id=uuid.uuid4(),
    )

    assert renewed is True
    assert db.execute.await_count == 2
