from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update

from app.config import get_settings
from app.models.engagement import Engagement
from app.models.enums import ScanJobStatus
from app.models.scan_job import ScanJob
from app.models.scan_job_attempt import ScanJobAttempt


@dataclass(frozen=True)
class AttemptClaim:
    attempt_id: uuid.UUID
    attempt_number: int
    fence: int
    lease_expires_at: datetime


async def claim_job_attempt(
    db,
    *,
    job_id: uuid.UUID,
    agent_id: uuid.UUID,
    tenant_id: uuid.UUID,
) -> AttemptClaim | None:
    """Atomically claim a pending job and create its fenced attempt ledger row."""
    now = datetime.now(timezone.utc)
    lease_until = now + timedelta(seconds=get_settings().job_lease_seconds)
    attempt_id = uuid.uuid4()

    claimed = await db.execute(
        update(ScanJob)
        .where(
            ScanJob.id == job_id,
            ScanJob.status == ScanJobStatus.pending,
            ScanJob.agent_id.is_(None),
            ScanJob.attempt_count < ScanJob.max_attempts,
            ScanJob.engagement_id.in_(
                select(Engagement.id).where(Engagement.tenant_id == tenant_id)
            ),
        )
        .values(
            agent_id=str(agent_id),
            status=ScanJobStatus.running,
            started_at=now,
            lease_expires_at=lease_until,
            current_attempt_id=attempt_id,
            current_fence=ScanJob.current_fence + 1,
            attempt_count=ScanJob.attempt_count + 1,
        )
        .returning(ScanJob.attempt_count, ScanJob.current_fence)
        .execution_options(synchronize_session=False)
    )
    claimed_row = claimed.first()
    if claimed_row is None:
        return None

    attempt_number = int(claimed_row[0])
    fence = int(claimed_row[1])
    db.add(ScanJobAttempt(
        id=attempt_id,
        job_id=job_id,
        attempt_number=attempt_number,
        fence=fence,
        agent_id=agent_id,
        status="running",
        claimed_at=now,
        started_at=now,
        heartbeat_at=now,
        lease_expires_at=lease_until,
    ))
    await db.flush()
    return AttemptClaim(
        attempt_id=attempt_id,
        attempt_number=attempt_number,
        fence=fence,
        lease_expires_at=lease_until,
    )


async def renew_job_attempt(
    db,
    *,
    job_id: uuid.UUID,
    attempt_id: uuid.UUID,
    fence: int,
    agent_id: uuid.UUID,
) -> bool:
    """Renew only the currently installed running attempt/fence."""
    now = datetime.now(timezone.utc)
    lease_until = now + timedelta(seconds=get_settings().job_lease_seconds)
    renewed = (await db.execute(
        update(ScanJobAttempt)
        .where(
            ScanJobAttempt.id == attempt_id,
            ScanJobAttempt.job_id == job_id,
            ScanJobAttempt.agent_id == agent_id,
            ScanJobAttempt.fence == fence,
            ScanJobAttempt.status == "running",
            ScanJobAttempt.id.in_(
                select(ScanJob.current_attempt_id).where(
                    ScanJob.id == job_id,
                    ScanJob.status == ScanJobStatus.running,
                    ScanJob.agent_id == str(agent_id),
                    ScanJob.current_fence == fence,
                )
            ),
        )
        .values(heartbeat_at=now, lease_expires_at=lease_until)
        .execution_options(synchronize_session=False)
    )).rowcount
    if not renewed:
        return False
    await db.execute(
        update(ScanJob)
        .where(
            ScanJob.id == job_id,
            ScanJob.current_attempt_id == attempt_id,
            ScanJob.current_fence == fence,
            ScanJob.status == ScanJobStatus.running,
        )
        .values(lease_expires_at=lease_until)
        .execution_options(synchronize_session=False)
    )
    return True
