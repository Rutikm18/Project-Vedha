import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import structlog
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import Text, and_, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, ReadDB, AuthUser
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.common import PaginatedResponse, paginate
from app.schemas.finding import FindingOut, FindingPatch, FindingSummary, SlaSummary
from app.services import sla as sla_service
from app.utils.db import get_or_404
from app.utils.pagination import paginate_query

router = APIRouter(prefix="/findings", tags=["findings"])
logger = structlog.get_logger()


async def _tenant_finding(db: AsyncSession, finding_id: uuid.UUID, tenant_id: uuid.UUID) -> Finding:
    """Fetch a finding scoped to the caller's tenant via its parent engagement.

    Findings have no ``tenant_id`` column — tenancy is enforced through the
    engagement — so the generic ``get_or_404(..., tenant_field="tenant_id")``
    raises AttributeError here. Scope through the engagement join instead.
    """
    q = (
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.id == finding_id, Engagement.tenant_id == tenant_id)
    )
    finding = (await db.execute(q)).scalar_one_or_none()
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding


@router.get("/sla-summary", response_model=SlaSummary, summary="SLA breach/at-risk summary for the tenant")
async def sla_summary(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    """
    Compute SLA state across the tenant's tracked findings (open/confirmed).
    Optionally scope to a single engagement. Read-only aggregate → routed to the
    read replica when one is configured. Deadlines/states come from the SLA
    policy engine (app.services.sla) so every surface agrees.
    """
    q = (
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == current_user.tenant_id)
        .where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
    )
    if engagement_id:
        q = q.where(Finding.engagement_id == engagement_id)

    findings = (await db.execute(q)).scalars().all()
    return sla_service.summarize(list(findings))


@router.get("", response_model=PaginatedResponse[FindingOut], summary="List findings with filters")
async def list_findings(
    db: DB,
    current_user: AuthUser,
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
    asset_id: uuid.UUID | None = Query(default=None),
    mitre_technique: str | None = Query(default=None),
    engagement_id: uuid.UUID | None = Query(default=None),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    detection_status: DetectionStatus | None = Query(default=None),
    exploit_validated: bool | None = Query(default=None),
    sla_breached: bool = Query(default=False),
    sort: Literal["risk", "cvss", "epss", "date"] = Query(default="risk"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    # Scope to tenant via engagement join
    q = (
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == current_user.tenant_id)
    )

    if severity:
        q = q.where(Finding.severity == severity)
    if status_filter:
        q = q.where(Finding.status == status_filter)
    if asset_id:
        q = q.where(Finding.asset_id == asset_id)
    if engagement_id:
        q = q.where(Finding.engagement_id == engagement_id)
    if mitre_technique:
        q = q.where(Finding.mitre_techniques.any(mitre_technique))
    if search:
        term = f"%{search.strip()}%"
        q = q.where(or_(
            Finding.title.ilike(term),
            cast(Finding.id, Text).ilike(term),
            cast(Finding.cve_ids, Text).ilike(term),
        ))
    if detection_status:
        q = q.where(Finding.detection_status == detection_status)
    if exploit_validated is not None:
        q = q.where(Finding.exploit_validated == exploit_validated)
    if sla_breached:
        now = datetime.now(timezone.utc)
        q = q.where(
            Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]),
            or_(
                and_(
                    Finding.severity == FindingSeverity.critical,
                    Finding.created_at < now - timedelta(hours=24),
                ),
                and_(
                    Finding.severity == FindingSeverity.high,
                    Finding.created_at < now - timedelta(hours=72),
                ),
                and_(
                    Finding.severity == FindingSeverity.medium,
                    Finding.created_at < now - timedelta(days=7),
                ),
                and_(
                    Finding.severity == FindingSeverity.low,
                    Finding.created_at < now - timedelta(days=30),
                ),
            ),
        )

    effective_risk = func.coalesce(
        Finding.risk_score,
        Finding.cvss_score * 100,
        0,
    )
    order_by = {
        "risk": effective_risk.desc(),
        "cvss": Finding.cvss_score.desc().nullslast(),
        "epss": Finding.epss_score.desc().nullslast(),
        "date": Finding.created_at.desc(),
    }[sort]
    q = q.order_by(order_by, Finding.created_at.desc(), Finding.id)
    items, total = await paginate_query(db, q, page, page_size)
    return paginate(items, total, page, page_size)


@router.get("/summary", response_model=FindingSummary, summary="Tenant finding aggregates")
async def finding_summary(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    tracked = Finding.status.in_([FindingStatus.open, FindingStatus.confirmed])
    q = (
        select(
            func.count(Finding.id),
            func.count(Finding.id).filter(tracked),
            func.count(Finding.id).filter(
                Finding.severity == FindingSeverity.critical,
                tracked,
            ),
            func.count(Finding.id).filter(Finding.severity == FindingSeverity.high, tracked),
            func.count(Finding.id).filter(Finding.severity == FindingSeverity.medium, tracked),
            func.count(Finding.id).filter(Finding.severity == FindingSeverity.low, tracked),
            func.count(Finding.id).filter(Finding.severity == FindingSeverity.info, tracked),
            func.count(Finding.id).filter(Finding.exploit_validated.is_(True)),
            func.count(Finding.id).filter(Finding.detection_status == DetectionStatus.missed),
            func.avg(func.coalesce(Finding.risk_score, Finding.cvss_score * 100, 0)),
        )
        .select_from(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == current_user.tenant_id)
    )
    if engagement_id:
        q = q.where(Finding.engagement_id == engagement_id)
    (
        total, open_total, critical_open, high_open, medium_open, low_open,
        info_open, validated, blind, average_risk,
    ) = (await db.execute(q)).one()
    return FindingSummary(
        total=int(total or 0),
        open_total=int(open_total or 0),
        critical_open=int(critical_open or 0),
        high_open=int(high_open or 0),
        medium_open=int(medium_open or 0),
        low_open=int(low_open or 0),
        info_open=int(info_open or 0),
        validated=int(validated or 0),
        blind=int(blind or 0),
        average_risk=round(float(average_risk or 0)),
    )


@router.get("/{finding_id}", response_model=FindingOut, summary="Finding detail")
async def get_finding(
    finding_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    return await _tenant_finding(db, finding_id, current_user.tenant_id)


@router.patch("/{finding_id}", response_model=FindingOut, summary="Update finding status, owner, or notes")
async def patch_finding(
    finding_id: uuid.UUID,
    body: FindingPatch,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester", "analyst"])],
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)

    patch = body.model_dump(exclude_unset=True)

    if "notes" in patch:
        notes = patch.pop("notes")
        finding.remediation = (
            f"{finding.remediation}\n\n[Note] {notes}" if finding.remediation else f"[Note] {notes}"
        )

    for field, value in patch.items():
        setattr(finding, field, value)

    await db.flush()
    await db.refresh(finding)
    logger.info("finding.patched", id=str(finding_id), changes=list(patch.keys()))
    return finding


# `get_or_404` lives in app/utils/db.py — imported at top of file.
