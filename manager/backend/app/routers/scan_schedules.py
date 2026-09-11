"""
scan_schedules.py — operator management of recurring scans.

Vedha could only be told "scan now", so every run started from scratch and
nothing re-checked an estate on its own. These endpoints let an operator say
"this engagement, this use-case, every N hours".

Validation matters more here than on a normal endpoint. A schedule is a STANDING
INSTRUCTION that fires unattended: a bad one is not a failed request somebody
sees and retries, it is a scan that quietly misbehaves for weeks. So the
use-case is checked against the same catalog dispatch uses (a typo would
otherwise be accepted once and then fail at every firing, forever, in worker
logs), and the interval has a floor (a 1-minute deep-scan schedule queues work
faster than any probe drains it, and the per-engagement queue cap would then
reject real operator jobs as collateral).

Tenancy is enforced through the engagement on every route, so nobody can schedule
scans against another tenant's estate.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.models.scan_schedule import ScanSchedule
from app.routers.agents import _USE_CASES
from app.services.project_time import project_now

router = APIRouter(prefix="/scan-schedules", tags=["scheduling"])
_OPERATOR = require_role(["admin", "manager"])


class ScheduleIn(BaseModel):
    engagement_id: uuid.UUID
    use_case_id: str = Field(min_length=1, max_length=64)
    # 1..3 mirrors the probe's INTENSITY_CODES (light/standard/deep).
    intensity: int = Field(default=2, ge=1, le=3)
    # Floor of 1h: anything faster queues work no probe can drain, and the
    # per-engagement queue cap then rejects an operator's own jobs. Ceiling of
    # one year, so a typo'd interval cannot silently disable a schedule forever.
    interval_hours: int = Field(ge=1, le=8760)


class ScheduleUpdate(BaseModel):
    enabled: bool | None = None
    interval_hours: int | None = Field(default=None, ge=1, le=8760)
    intensity: int | None = Field(default=None, ge=1, le=3)


def _out(row: ScanSchedule) -> dict:
    return {
        "id": str(row.id),
        "engagement_id": str(row.engagement_id),
        "use_case_id": row.use_case_id,
        "intensity": row.intensity,
        "interval_hours": row.interval_hours,
        "enabled": row.enabled,
        "last_run_at": row.last_run_at.isoformat() if row.last_run_at else None,
        "next_run_at": row.next_run_at.isoformat() if row.next_run_at else None,
    }


async def _engagement_or_404(db, engagement_id: uuid.UUID, tenant_id: uuid.UUID):
    eng = (await db.execute(
        select(Engagement).where(
            Engagement.id == engagement_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if eng is None:
        # 404, not 403: confirming the engagement exists would leak another
        # tenant's inventory.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    return eng


async def _schedule_or_404(db, schedule_id: uuid.UUID, tenant_id: uuid.UUID):
    row = (await db.execute(
        select(ScanSchedule)
        .join(Engagement, ScanSchedule.engagement_id == Engagement.id)
        .where(ScanSchedule.id == schedule_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Schedule not found")
    return row


@router.post("", status_code=status.HTTP_201_CREATED,
             summary="Create a recurring scan schedule")
async def create_schedule(
    body: ScheduleIn,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    if body.use_case_id not in _USE_CASES:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown use_case_id '{body.use_case_id}'. A schedule fires "
            f"unattended, so an unknown use-case is rejected here rather than "
            f"failing silently at every run. See GET /agents/use-cases.",
        )
    await _engagement_or_404(db, body.engagement_id, current_user.tenant_id)

    # Due immediately: an operator who schedules a daily scan expects today's
    # run, not tomorrow's. The worker picks it up on its next tick.
    row = ScanSchedule(
        tenant_id=current_user.tenant_id,
        engagement_id=body.engagement_id,
        use_case_id=body.use_case_id,
        intensity=body.intensity,
        interval_hours=body.interval_hours,
        enabled=True,
        next_run_at=project_now(),
        created_by=current_user.user_id,
    )
    db.add(row)
    await db.flush()
    return _out(row)


@router.get("", summary="List scan schedules")
async def list_schedules(
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
    engagement_id: uuid.UUID | None = Query(default=None),
):
    q = (select(ScanSchedule)
         .join(Engagement, ScanSchedule.engagement_id == Engagement.id)
         .where(Engagement.tenant_id == current_user.tenant_id))
    if engagement_id:
        q = q.where(ScanSchedule.engagement_id == engagement_id)
    return [_out(r) for r in (await db.execute(q)).scalars().all()]


@router.patch("/{schedule_id}", summary="Pause, resume, or retune a schedule")
async def update_schedule(
    schedule_id: uuid.UUID,
    body: ScheduleUpdate,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    """Pausing is first-class: disabling during a change freeze is routine, and
    deleting would lose the configuration and its run history."""
    row = await _schedule_or_404(db, schedule_id, current_user.tenant_id)
    if body.enabled is not None:
        row.enabled = body.enabled
    if body.interval_hours is not None:
        row.interval_hours = body.interval_hours
    if body.intensity is not None:
        row.intensity = body.intensity
    await db.flush()
    return _out(row)


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a schedule")
async def delete_schedule(
    schedule_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    row = await _schedule_or_404(db, schedule_id, current_user.tenant_id)
    await db.delete(row)
    return None
