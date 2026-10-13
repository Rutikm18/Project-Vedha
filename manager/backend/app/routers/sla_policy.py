"""
sla_policy.py — operator management of the tenant's custom SLA remediation windows.

GET returns the effective windows (custom row if set, else env defaults, flagged by
`is_custom`); PUT upserts the tenant's policy. `resolve_windows` is the shared
lookup other routers use to feed `services/sla.py` so a saved policy takes effect on
every SLA surface. Operator-only; customers only see the resulting SLA states.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.models.sla_policy import SlaPolicy
from app.services import deadlines, sla
from app.services.audit import record_audit

router = APIRouter(prefix="/sla-policy", tags=["sla"])
_OPERATOR = require_role(["admin", "manager"])

_H = Field(ge=0, le=8760)   # 0 hours … 1 year


class SlaPolicyOut(BaseModel):
    critical_hours: int
    high_hours: int
    medium_hours: int
    low_hours: int
    info_hours: int
    is_custom: bool     # False → these are the env defaults (no tenant row yet)


class SlaPolicyIn(BaseModel):
    critical_hours: int = _H
    high_hours: int = _H
    medium_hours: int = _H
    low_hours: int = _H
    info_hours: int = _H


async def _row(db: AsyncSession, tenant_id: uuid.UUID) -> SlaPolicy | None:
    return (await db.execute(
        select(SlaPolicy).where(SlaPolicy.tenant_id == tenant_id)
    )).scalar_one_or_none()


def _windows_of(row: SlaPolicy) -> dict[str, int]:
    return {"critical": row.critical_hours, "high": row.high_hours,
            "medium": row.medium_hours, "low": row.low_hours, "info": row.info_hours}


async def resolve_windows(db: AsyncSession, tenant_id: uuid.UUID) -> dict[str, int]:
    """The tenant's custom SLA windows if set, else the env defaults. Shared by any
    router that renders SLA so custom policies apply consistently. Per-engagement
    policies layer on top via services/deadlines.py."""
    return await deadlines.tenant_windows(db, tenant_id) or sla.default_windows()


def _out(row: SlaPolicy | None) -> SlaPolicyOut:
    if row is None:
        w = sla.default_windows()
        return SlaPolicyOut(critical_hours=w["critical"], high_hours=w["high"],
                            medium_hours=w["medium"], low_hours=w["low"],
                            info_hours=w["info"], is_custom=False)
    return SlaPolicyOut(**_windows_of_named(row), is_custom=True)


def _windows_of_named(row: SlaPolicy) -> dict[str, int]:
    return {"critical_hours": row.critical_hours, "high_hours": row.high_hours,
            "medium_hours": row.medium_hours, "low_hours": row.low_hours,
            "info_hours": row.info_hours}


@router.get("", response_model=SlaPolicyOut, summary="Effective SLA windows for the tenant")
async def get_sla_policy(db: DB, current_user: Annotated[AuthUser, _OPERATOR]):
    return _out(await _row(db, current_user.tenant_id))


@router.put("", response_model=SlaPolicyOut, summary="Set the tenant's custom SLA windows")
async def put_sla_policy(body: SlaPolicyIn, db: DB,
                         current_user: Annotated[AuthUser, _OPERATOR]):
    row = await _row(db, current_user.tenant_id)
    if row is None:
        row = SlaPolicy(tenant_id=current_user.tenant_id, **body.model_dump())
        db.add(row)
    else:
        for key, value in body.model_dump().items():
            setattr(row, key, value)
    await db.flush()
    record_audit(db, actor_id=current_user.user_id, action="sla_policy.updated",
                 resource_type="sla_policy", resource_id=row.id, detail=body.model_dump())
    await db.flush()
    return _out(row)


# ── per-engagement policy (overrides the tenant policy for one engagement) ─────
# Stored in engagements.rules_of_engagement["sla_policy"], next to the regulatory
# profile — customer contracts differ, so each engagement may set its own clock.

engagement_router = APIRouter(prefix="/engagements", tags=["sla"])
_READER = require_role(["admin", "manager", "tester", "analyst", "auditor"])


class EngagementSlaPolicyOut(BaseModel):
    critical_hours: int
    high_hours: int
    medium_hours: int
    low_hours: int
    info_hours: int
    source: str          # engagement | tenant | default — where these windows come from


async def _engagement(db: AsyncSession, engagement_id: uuid.UUID, tenant_id: uuid.UUID) -> Engagement:
    eng = (await db.execute(
        select(Engagement).where(Engagement.id == engagement_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    return eng


def _eng_out(windows: dict[str, int], source: str) -> EngagementSlaPolicyOut:
    return EngagementSlaPolicyOut(**{f"{k}_hours": v for k, v in windows.items()}, source=source)


@engagement_router.get("/{engagement_id}/sla-policy", response_model=EngagementSlaPolicyOut,
                       summary="Effective SLA windows for an engagement")
async def get_engagement_sla_policy(engagement_id: uuid.UUID, db: DB,
                                    current_user: Annotated[AuthUser, _READER]):
    eng = await _engagement(db, engagement_id, current_user.tenant_id)
    windows, source = await deadlines.windows_for(db, current_user.tenant_id, eng)
    return _eng_out(windows, source)


@engagement_router.put("/{engagement_id}/sla-policy", response_model=EngagementSlaPolicyOut,
                       summary="Set this engagement's SLA windows (overrides the tenant policy)")
async def put_engagement_sla_policy(engagement_id: uuid.UUID, body: SlaPolicyIn, db: DB,
                                    current_user: Annotated[AuthUser, _OPERATOR]):
    eng = await _engagement(db, engagement_id, current_user.tenant_id)
    roe = dict(eng.rules_of_engagement or {})       # reassign → JSONB change is detected
    roe["sla_policy"] = body.model_dump()
    eng.rules_of_engagement = roe
    await db.flush()
    return _eng_out(deadlines.engagement_windows(eng) or sla.default_windows(), "engagement")


@engagement_router.delete("/{engagement_id}/sla-policy", response_model=EngagementSlaPolicyOut,
                          summary="Remove this engagement's SLA override (fall back to tenant)")
async def delete_engagement_sla_policy(engagement_id: uuid.UUID, db: DB,
                                       current_user: Annotated[AuthUser, _OPERATOR]):
    eng = await _engagement(db, engagement_id, current_user.tenant_id)
    roe = dict(eng.rules_of_engagement or {})
    roe.pop("sla_policy", None)
    eng.rules_of_engagement = roe
    await db.flush()
    windows, source = await deadlines.windows_for(db, current_user.tenant_id, eng)
    return _eng_out(windows, source)
