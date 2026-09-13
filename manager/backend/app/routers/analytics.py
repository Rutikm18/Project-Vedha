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
    #: Worst severity among findings attributable to this service; None = clean.
    severity: str | None = None
    #: Severity weight 0-100 — drives the meter bar length ONLY. The row's band
    #: label comes from `severity`, never from thresholding this.
    value: int
    #: How many open findings were attributed to this service, and how many
    #: assets expose it — so a row says how much it rests on.
    findings: int = 0
    assets: int = 0


class ZoneHealth(BaseModel):
    name: str
    score: int
    assets: int = 0
    affected: int = 0


class ExposureAnalytics(BaseModel):
    protocols: list[ProtocolRisk]
    zones: list[ZoneHealth]
    #: Open findings that name no port, or a port with no known service, so they
    #: cannot honestly be charged to a protocol.
    unattributed_findings: int = 0


@router.get("/exposure", response_model=ExposureAnalytics, summary="Protocol risk + zone health")
async def exposure(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    tenant_id = current_user.tenant_id

    # Column projections, not whole entities: this endpoint polls every 60s over
    # every open finding in the tenant, and Finding carries description,
    # remediation and content_overrides that nothing here reads. `evidence` IS
    # needed — protocol attribution reads the port out of it.
    asset_q = (
        select(Asset.id, Asset.environment)
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
    )
    service_q = (
        select(Service.asset_id, Service.service_name, Service.port)
        .join(Asset, Service.asset_id == Asset.id)
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
    )
    finding_q = (
        select(Finding.asset_id, Finding.severity, Finding.evidence)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
        .where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
    )
    if engagement_id:
        asset_q = asset_q.where(Asset.engagement_id == engagement_id)
        service_q = service_q.where(Asset.engagement_id == engagement_id)
        finding_q = finding_q.where(Finding.engagement_id == engagement_id)

    assets = (await db.execute(asset_q)).all()
    services = (await db.execute(service_q)).all()
    findings = (await db.execute(finding_q)).all()

    return analytics_service.compute_exposure(list(assets), list(services), list(findings))


def _enum_str(value) -> str:
    """Unwrap a SQLAlchemy enum column to its string value (severity, asset
    criticality, finding status) — plain strings pass straight through."""
    return value.value if hasattr(value, "value") else str(value)


def _finding_views(rows) -> list[posture_service.FindingView]:
    """Map joined (Finding, Asset.criticality) rows to duck-typed views."""
    return [
        posture_service.FindingView(
            id=str(r.id),
            severity=_enum_str(r.severity),
            risk_score=float(r.risk_score) if r.risk_score is not None else None,
            epss_score=float(r.epss_score) if r.epss_score is not None else None,
            exploitable=bool(r.exploitable),
            exploit_validated=bool(r.exploit_validated),
            asset_criticality=(
                _enum_str(r.asset_criticality) if getattr(r, "asset_criticality", None) is not None else None
            ),
            first_seen=r.first_seen,
            last_seen=r.last_seen,
            status=_enum_str(r.status) if getattr(r, "status", None) is not None else "open",
        )
        for r in rows
    ]


# Statuses posture comparison loads. `remediated` is REQUIRED — it is the status
# a fixed finding ends up in, so leaving it out makes "Patched" and "risk burned
# down" structurally unable to count real remediation (see posture.compare).
# `accepted` and `fp` stay out: risk-accepted is not a fix, and a false positive
# was never an exposure, so neither belongs in a patch ledger.
POSTURE_STATUSES = [
    FindingStatus.open, FindingStatus.confirmed, FindingStatus.remediated,
]


async def load_posture_views(db, engagement_id) -> list[posture_service.FindingView]:
    """The finding rows behind posture scoring and patch comparison.

    Shared by the dashboard analytics endpoint and the AI report's
    "Posture & Remediation Progress" section, which previously each wrote this
    query by hand and so drifted to the same wrong answer twice.
    """
    rows = (await db.execute(
        select(
            Finding.id, Finding.severity, Finding.risk_score, Finding.epss_score,
            Finding.exploitable, Finding.exploit_validated,
            Finding.first_seen, Finding.last_seen, Finding.status,
            Asset.criticality.label("asset_criticality"),
        )
        .outerjoin(Asset, Finding.asset_id == Asset.id)
        .where(Finding.engagement_id == engagement_id,
               Finding.status.in_(POSTURE_STATUSES))
    )).all()
    return _finding_views(rows)


async def _two_latest_completed_runs(db, engagement_id, tenant_id):
    rows = (await db.execute(
        select(DetectionRun.id, DetectionRun.started_at)
        .join(Engagement, DetectionRun.engagement_id == Engagement.id)
        .where(
            DetectionRun.engagement_id == engagement_id,
            Engagement.tenant_id == tenant_id,
            DetectionRun.status == RUN_COMPLETED,
        )
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
    engagement = await get_or_404(db, Engagement, engagement_id, tenant_id)

    prev_run, latest_run = await _two_latest_completed_runs(db, engagement_id, tenant_id)

    views = await load_posture_views(db, engagement_id)
    payload = posture_service.build_posture(views, prev_run, latest_run)
    # Name the engagement these numbers describe.
    #
    # Posture and patch-comparison are necessarily PER-ENGAGEMENT — a grade
    # averaged across unrelated customers means nothing — while every other panel
    # on the operator dashboard is tenant-wide. With no engagement_id this
    # endpoint silently picks whichever engagement scanned most recently, so an
    # unlabelled "C" sat next to a tenant-wide finding count and read as the
    # whole tenant's grade, switching to a different customer the moment a
    # different engagement finished a scan. The console renders this name so the
    # reader always knows whose posture they are looking at.
    payload["engagement"] = {"id": str(engagement_id), "name": engagement.name}
    return payload
