"""
Dashboard exposure analytics endpoint.

Serves protocol-risk + zone-health aggregates computed by app.services.analytics
from real assets / services / open findings. Read-only → routed to the read
replica when one is configured.
"""
import uuid

import structlog
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import select

from app.dependencies import ReadDB, AuthUser
from app.models.asset import Asset
from app.models.detection_run import DetectionRun, RUN_COMPLETED
from app.models.engagement import Engagement
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.models.service import Service
from app.services import analytics as analytics_service
from app.services import posture as posture_service
from app.utils.db import get_or_404

router = APIRouter(prefix="/analytics", tags=["analytics"])
logger = structlog.get_logger()


class ProtocolRisk(BaseModel):
    name: str
    value: int


class ZoneHealth(BaseModel):
    name: str
    score: int


class ExposureAnalytics(BaseModel):
    protocols: list[ProtocolRisk]
    zones: list[ZoneHealth]


@router.get("/exposure", response_model=ExposureAnalytics, summary="Protocol risk + zone health")
async def exposure(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    tenant_id = current_user.tenant_id

    asset_q = (
        select(Asset)
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
    )
    service_q = (
        select(Service)
        .join(Asset, Service.asset_id == Asset.id)
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
    )
    finding_q = (
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
        .where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
    )
    if engagement_id:
        asset_q = asset_q.where(Asset.engagement_id == engagement_id)
        service_q = service_q.where(Asset.engagement_id == engagement_id)
        finding_q = finding_q.where(Finding.engagement_id == engagement_id)

    assets = (await db.execute(asset_q)).scalars().all()
    services = (await db.execute(service_q)).scalars().all()
    findings = (await db.execute(finding_q)).scalars().all()

    return analytics_service.compute_exposure(list(assets), list(services), list(findings))


def _sev_str(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _finding_views(rows) -> list[posture_service.FindingView]:
    """Map joined (Finding, Asset.criticality) rows to duck-typed views."""
    return [
        posture_service.FindingView(
            id=str(r.id),
            severity=_sev_str(r.severity),
            risk_score=float(r.risk_score) if r.risk_score is not None else None,
            epss_score=float(r.epss_score) if r.epss_score is not None else None,
            exploitable=bool(r.exploitable),
            exploit_validated=bool(r.exploit_validated),
            asset_criticality=(
                _sev_str(r.asset_criticality) if getattr(r, "asset_criticality", None) is not None else None
            ),
            first_seen=r.first_seen,
            last_seen=r.last_seen,
        )
        for r in rows
    ]


async def _two_latest_completed_runs(db, engagement_id):
    rows = (await db.execute(
        select(DetectionRun.id, DetectionRun.started_at)
        .where(DetectionRun.engagement_id == engagement_id, DetectionRun.status == RUN_COMPLETED)
        .order_by(DetectionRun.started_at.desc())
        .limit(2)
    )).all()
    latest = {"id": str(rows[0].id), "started_at": rows[0].started_at} if len(rows) >= 1 else None
    prev = {"id": str(rows[1].id), "started_at": rows[1].started_at} if len(rows) >= 2 else None
    return prev, latest


@router.get("/posture", summary="Posture scores + patch comparison (prev vs latest run)")
async def posture(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    tenant_id = current_user.tenant_id

    # Resolve engagement: explicit, else the one owning the newest completed run.
    if engagement_id is None:
        row = (await db.execute(
            select(DetectionRun.engagement_id)
            .join(Engagement, DetectionRun.engagement_id == Engagement.id)
            .where(Engagement.tenant_id == tenant_id, DetectionRun.status == RUN_COMPLETED)
            .order_by(DetectionRun.started_at.desc())
            .limit(1)
        )).first()
        if row is None:
            return {"has_runs": False}
        engagement_id = row.engagement_id
    else:
        await get_or_404(db, Engagement, engagement_id, tenant_id)

    prev_run, latest_run = await _two_latest_completed_runs(db, engagement_id)

    finding_rows = (await db.execute(
        select(
            Finding.id, Finding.severity, Finding.risk_score, Finding.epss_score,
            Finding.exploitable, Finding.exploit_validated,
            Finding.first_seen, Finding.last_seen,
            Asset.criticality.label("asset_criticality"),
        )
        .outerjoin(Asset, Finding.asset_id == Asset.id)
        .where(Finding.engagement_id == engagement_id)
    )).all()

    views = _finding_views(finding_rows)
    return posture_service.build_posture(views, prev_run, latest_run)
