import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import structlog
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import Text, and_, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, ReadDB, AuthUser
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.common import PaginatedResponse, paginate
from app.schemas.finding import (
    FindingAssetContext, FindingEventOut, FindingOut, FindingPatch, FindingReopen,
    FindingSummary, FindingTimeline, SlaSummary,
)
from app.services import finding_events as events_service
from app.services import finding_workflow
from app.services import sla as sla_service
from app.services.finding_enrichment import detail_enrichment
from app.services.finding_priority import severity_order_case
from app.services.risk_rank import compute_risk_rank
from app.routers.sla_policy import resolve_windows
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


async def _finding_detail_out(db: AsyncSession, finding: Finding) -> FindingOut:
    """Build the detail contract with bounded asset context.

    Portfolio/list responses deliberately stay finding-only. A detail read pays
    for one explicit asset lookup so the UI can identify the affected system
    without guessing from an opaque asset UUID.
    """
    asset_context = None
    if finding.asset_id is not None:
        asset = (await db.execute(
            select(Asset).where(
                Asset.id == finding.asset_id,
                Asset.engagement_id == finding.engagement_id,
            )
        )).scalar_one_or_none()
        if asset is not None:
            asset_context = FindingAssetContext(
                id=asset.id,
                ip_address=asset.ip_address,
                hostname=asset.hostname,
                fqdn=asset.fqdn,
                os=asset.os,
                os_version=asset.os_version,
                asset_type=getattr(asset.asset_type, "value", asset.asset_type),
                criticality=getattr(asset.criticality, "value", asset.criticality),
                owner=asset.owner,
                environment=asset.environment,
            )
    update: dict = {"asset_context": asset_context}
    # On the detail read we know the asset, so recompute the explainable rank WITH
    # real criticality/exposure instead of the neutral defaults the list path uses.
    # Exposure (internet_facing/auth_enforced) is only honoured if the engine
    # actually recorded it in evidence — never guessed. When absent it stays None
    # and compute_risk_rank treats it as neutral (see risk_rank.py's contract).
    if asset_context is not None:
        ev = finding.evidence if isinstance(finding.evidence, dict) else {}
        enr = ev.get("enrichment") if isinstance(ev.get("enrichment"), dict) else {}
        update["risk_rank"] = compute_risk_rank(
            severity=str(getattr(finding.severity, "value", finding.severity)),
            cvss_score=float(finding.cvss_score) if finding.cvss_score is not None else None,
            epss_score=float(finding.epss_score) if finding.epss_score is not None else None,
            kev=bool(ev.get("kev") or enr.get("kev")),
            exploit_validated=bool(finding.exploit_validated),
            verification_state=finding.verification_state,
            confidence=finding.verification_confidence,
            asset_criticality=asset_context.criticality,
            internet_facing=ev.get("internet_facing"),
            auth_enforced=ev.get("auth_enforced"),
        )
    # Detail-only heavy enrichment: explanation, business impact, technical detail,
    # exploitation posture, evidence-as-facts, and five-framework compliance. The
    # list endpoint deliberately omits this to stay bounded (see the schema note).
    update.update(detail_enrichment(
        finding,
        asset_criticality=(asset_context.criticality if asset_context is not None else None),
    ))
    return FindingOut.model_validate(finding).model_copy(update=update)


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
    windows = await resolve_windows(db, current_user.tenant_id)   # tenant custom policy or env
    return sla_service.summarize(list(findings), windows=windows)


@router.get("", response_model=PaginatedResponse[FindingOut], summary="List findings with filters")
async def list_findings(
    db: DB,
    current_user: AuthUser,
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
    asset_id: uuid.UUID | None = Query(default=None),
    mitre_technique: str | None = Query(default=None),
    engagement_id: uuid.UUID | None = Query(default=None),
    agent_id: uuid.UUID | None = Query(default=None),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    detection_status: DetectionStatus | None = Query(default=None),
    exploit_validated: bool | None = Query(default=None),
    verification_state: str | None = Query(default=None),
    needs_review: bool | None = Query(default=None),
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
    if agent_id:
        q = q.where(Engagement.assigned_agent_id == agent_id)
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
    if verification_state:
        q = q.where(Finding.verification_state == verification_state)
    if needs_review is not None:
        q = q.where(Finding.needs_review == needs_review)
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
    # "Critical always on top": the default risk view sorts by SEVERITY TIER first
    # (so a KEV'd high can never jump above an ordinary critical), then by the
    # composite risk within the tier. The explicit cvss/epss/date sorts stay pure
    # single-axis views — an operator picking those is deliberately overriding the
    # tier grouping. See services/finding_priority.py for the shared definition.
    sev_tier = severity_order_case(Finding.severity)
    order_by = {
        "risk": [sev_tier.desc(), effective_risk.desc()],
        "cvss": [Finding.cvss_score.desc().nullslast()],
        "epss": [Finding.epss_score.desc().nullslast()],
        "date": [Finding.created_at.desc()],
    }[sort]
    q = q.order_by(*order_by, Finding.created_at.desc(), Finding.id)
    items, total = await paginate_query(db, q, page, page_size)
    return paginate(items, total, page, page_size)


@router.get("/summary", response_model=FindingSummary, summary="Tenant finding aggregates")
async def finding_summary(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
    agent_id: uuid.UUID | None = Query(default=None),
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
    if agent_id:
        q = q.where(Engagement.assigned_agent_id == agent_id)
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
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    return await _finding_detail_out(db, finding)


@router.get("/{finding_id}/events", response_model=FindingTimeline,
            summary="Finding lifecycle timeline (audit trail)")
async def finding_timeline(
    finding_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    """The finding's full lifecycle, oldest-first: stored audit events (who did
    what, when) merged with the events its own timestamps imply (detected,
    re-observed, resolved). Every entry carries a full timestamp."""
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    timeline = await events_service.build_timeline(db, finding)
    return FindingTimeline(
        finding_id=finding.id,
        events=[FindingEventOut(**e) for e in timeline],
    )


@router.patch("/{finding_id}", response_model=FindingOut, summary="Update finding status, owner, or notes")
async def patch_finding(
    finding_id: uuid.UUID,
    body: FindingPatch,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester", "analyst"])],
):
    finding = await finding_workflow.get_finding_for_action(
        db,
        finding_id,
        tenant_id=current_user.tenant_id,
    )
    updated = await finding_workflow.patch_finding(
        db,
        finding,
        body,
        actor_id=current_user.user_id,
        actor_type="manager",
        origin="manager",
    )
    logger.info("finding.patched", id=str(finding_id), by=str(current_user.user_id))
    return updated


@router.post("/{finding_id}/reopen", response_model=FindingOut,
             summary="Reopen an auto/manually-resolved finding")
async def reopen_finding(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    body: FindingReopen | None = None,
):
    """Operator reverses a resolution (auto or manual). Only a `remediated`
    finding can be reopened; history (reopened_count) is preserved and the
    reopening user is recorded in evidence."""
    finding = await finding_workflow.get_finding_for_action(
        db,
        finding_id,
        tenant_id=current_user.tenant_id,
    )
    updated = await finding_workflow.reopen_finding(
        db,
        finding,
        actor_id=current_user.user_id,
        actor_type="manager",
        origin="manager",
        reason=body.reason if body is not None else None,
    )
    logger.info("finding.reopened", id=str(finding_id), by=str(current_user.user_id))
    return updated


# `get_or_404` lives in app/utils/db.py — imported at top of file.
