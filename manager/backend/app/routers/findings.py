import ipaddress
import re
import uuid
from dataclasses import dataclass
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import Select, Text, and_, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, ReadDB, AuthUser
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.detection_run import DetectionRun
from app.models.detection_run_finding import (
    DetectionRunFinding, RUN_FINDING_NEW, RUN_FINDING_REAFFIRMED, RUN_FINDING_RESOLVED,
)
from app.models.scan_job import ScanJob
from app.models.service import Service
from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.common import PaginatedResponse, paginate
from app.schemas.finding_groups import FindingGroupPage
from app.schemas.finding import (
    FindingAssetContext, FindingAssetOption, FindingEventOut, FindingOut, FindingPatch, FindingReopen,
    FindingScanRef, FindingSummary, FindingTimeline, ScanCompareChange, ScanCompareCounts, ScanCompareOut,
    ScanCompareSnapshot, ScanCompareSummary, ScanOption, SlaSummary,
)
from app.services import finding_events as events_service
from app.services.finding_metrics import compute_mttr
from app.services import finding_workflow
from app.services import sla as sla_service
from app.services.finding_enrichment import detail_enrichment
from app.services.finding_workflow import suggest_risk_owner
from app.services.finding_groups import GroupRow, build_groups
from app.services.finding_priority import severity_order_case
from app.services import deadlines, sla as sla_service
from app.services.finding_priority import explain_priority
from app.services import risk_context
from app.services.risk_inputs import exposure_source, risk_inputs, strongest_exposure
from app.services.risk_rank import compute_risk_rank, explain_risk_rank
from app.routers.sla_policy import resolve_windows
from app.services.deadlines import engagement_windows
from app.utils.csv_safe import csv_cell
from app.utils.pagination import paginate_query
from app.detection.resolution import normalize_port

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


_IP_PREFIX = re.compile(r"^[0-9A-Fa-f:.]{1,45}$")


def asset_ip_clause(value: str):
    """Filter on the affected asset's IP: a complete address matches exactly;
    a partial one ("192.168.1.") matches as a prefix. Anything that is not
    IP-shaped is a 422 — the charset excludes LIKE wildcards, so a prefix
    cannot widen into a pattern."""
    value = value.strip()
    try:
        return Asset.ip_address == str(ipaddress.ip_address(value))
    except ValueError:
        pass
    if not _IP_PREFIX.match(value):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="asset_ip must be an IP address or an IP prefix")
    return Asset.ip_address.startswith(value)


async def _scan_refs(db: AsyncSession, findings: list[Finding]) -> dict[uuid.UUID, FindingScanRef]:
    """Resolve each finding's scan — detection_run_id → detection_runs → scan_jobs —
    in ONE query for the whole page, never one per row. Keyed by run id. Findings
    with no detection_run_id (legacy / probe self-assessed) are simply absent."""
    run_ids = {f.detection_run_id for f in findings if f.detection_run_id is not None}
    if not run_ids:
        return {}
    rows = (await db.execute(
        select(
            DetectionRun.id, DetectionRun.started_at, DetectionRun.job_id,
            ScanJob.reference, ScanJob.use_case_id, ScanJob.intensity,
            ScanJob.completed_at, ScanJob.started_at,
        )
        .join(ScanJob, ScanJob.id == DetectionRun.job_id, isouter=True)
        .where(DetectionRun.id.in_(run_ids))
    )).all()
    refs: dict[uuid.UUID, FindingScanRef] = {}
    for run_id, run_started, job_id, reference, use_case_id, intensity, job_done, job_started in rows:
        refs[run_id] = FindingScanRef(
            run_id=run_id, job_id=job_id, reference=reference,
            use_case_id=use_case_id, intensity=intensity,
            # When the scan produced this data: prefer the scan's own completion,
            # then its start, then the detection run's start as a last resort.
            scanned_at=job_done or job_started or run_started,
        )
    return refs


async def _resolve_scan_run_ids(
    db: AsyncSession, scan: str, tenant_id: uuid.UUID,
    *, engagement_id: uuid.UUID | None = None) -> set[uuid.UUID]:
    """Map a scan selector — an SCN-YYMMDD-XXXXXX reference, a scan-job id, or a
    detection-run id — to the detection-run ids it covers, tenant-scoped (and, when
    ``engagement_id`` is given, pinned to that engagement so a portal client can
    never reach a sibling engagement's scans in the same tenant). One scan (job) can
    have more than one run (e.g. chunked submissions), so the filter unions them.
    Unknown selector → empty set (caller shows an empty page rather than erroring,
    matching every other findings filter)."""
    scan = scan.strip()
    try:
        as_uuid: uuid.UUID | None = uuid.UUID(scan)
    except ValueError:
        as_uuid = None
    if as_uuid is not None:
        # A UUID is either a run id or a job id; the two spaces don't collide, so
        # accept whichever matches without asking the caller which they meant.
        q = (
            select(DetectionRun.id)
            .join(Engagement, DetectionRun.engagement_id == Engagement.id)
            .where(Engagement.tenant_id == tenant_id,
                   or_(DetectionRun.id == as_uuid, DetectionRun.job_id == as_uuid))
        )
        if engagement_id is not None:
            q = q.where(DetectionRun.engagement_id == engagement_id)
        return set((await db.execute(q)).scalars().all())
    # Otherwise a human reference (SCN-…). References are stored upper-case; fold
    # so the filter is case-insensitive.
    q = (
        select(DetectionRun.id)
        .join(ScanJob, ScanJob.id == DetectionRun.job_id)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id, ScanJob.reference == scan.upper())
    )
    if engagement_id is not None:
        q = q.where(ScanJob.engagement_id == engagement_id)
    return set((await db.execute(q)).scalars().all())


async def _scan_meta(db: AsyncSession, run_ids: set[uuid.UUID]) -> FindingScanRef | None:
    """The scan (job) identity behind a set of detection runs, for labelling a
    compare side. One selector resolves to one job, so a single row suffices."""
    if not run_ids:
        return None
    row = (await db.execute(
        select(
            ScanJob.id, ScanJob.reference, ScanJob.use_case_id, ScanJob.intensity,
            ScanJob.completed_at, ScanJob.started_at, func.min(DetectionRun.started_at),
        )
        .join(DetectionRun, DetectionRun.job_id == ScanJob.id)
        .where(DetectionRun.id.in_(run_ids))
        .group_by(ScanJob.id)
        .limit(1)
    )).first()
    if row is None:
        return None
    jid, reference, use_case_id, intensity, job_done, job_started, run_started = row
    return FindingScanRef(
        job_id=jid, reference=reference, use_case_id=use_case_id, intensity=intensity,
        scanned_at=job_done or job_started or run_started)


def _present_finding_ids(run_ids: set[uuid.UUID]):
    """Subquery of finding ids a scan's runs saw as still-present (new or
    reaffirmed). Resolved findings are deliberately excluded — a scan that closed
    a finding did not 'have' it."""
    return (
        select(DetectionRunFinding.finding_id)
        .where(DetectionRunFinding.run_id.in_(run_ids),
               DetectionRunFinding.outcome.in_((RUN_FINDING_NEW, RUN_FINDING_REAFFIRMED)))
    )


# When a scan (job) spans several runs, a finding can carry more than one outcome;
# surface the most significant. new (first appearance) outranks reaffirmed
# (still there) outranks resolved (this scan closed it).
_OUTCOME_RANK = {RUN_FINDING_NEW: 3, RUN_FINDING_REAFFIRMED: 2, RUN_FINDING_RESOLVED: 1}


async def _scan_outcomes(
    db: AsyncSession, run_ids: set[uuid.UUID], finding_ids: list[uuid.UUID],
) -> dict[uuid.UUID, str]:
    """What a scan's runs did to each of `finding_ids` — new / reaffirmed / resolved
    — collapsed to the most significant outcome per finding. One query for the page."""
    if not finding_ids:
        return {}
    rows = (await db.execute(
        select(DetectionRunFinding.finding_id, DetectionRunFinding.outcome)
        .where(DetectionRunFinding.run_id.in_(run_ids),
               DetectionRunFinding.finding_id.in_(finding_ids))
    )).all()
    best: dict[uuid.UUID, str] = {}
    for fid, outcome in rows:
        if _OUTCOME_RANK.get(outcome, 0) > _OUTCOME_RANK.get(best.get(fid, ""), 0):
            best[fid] = outcome
    return best


# The asset context and rank now live in services/risk_context.py (the report needs them too).
_asset_risk_context = risk_context.asset_risk_context


async def _sla_states(db: AsyncSession, findings: list[Finding]) -> dict:
    """finding id → SLA state, using each finding's engagement policy, then the tenant's,
    then the defaults (the order services/deadlines.py defines). Two bulk queries."""
    eng_ids = {f.engagement_id for f in findings}
    if not eng_ids:
        return {}
    engs = {e.id: e for e in (await db.execute(
        select(Engagement).where(Engagement.id.in_(eng_ids))
    )).scalars().all()}
    tenant_id = next(iter(engs.values())).tenant_id if engs else None
    tenant = await deadlines.tenant_windows(db, tenant_id) if tenant_id else None
    default = sla_service.default_windows()
    out = {}
    for f in findings:
        eng = engs.get(f.engagement_id)
        windows = (deadlines.engagement_windows(eng) if eng else None) or tenant or default
        out[f.id] = sla_service.compute(f, windows=windows).state
    return out


def priority_for(finding: Finding, sla_state: str | None) -> dict:
    inputs = risk_inputs(finding)
    return explain_priority(
        severity=inputs["severity"], kev=inputs["kev"], exploit_validated=inputs["exploit_validated"],
        epss_score=inputs["epss_score"], sla_state=sla_state, status=finding.status)


_rank_for = risk_context.rank_for
risk_ranks_for = risk_context.risk_ranks_for


async def _with_asset_identity(db: AsyncSession, findings: list[Finding]) -> list[FindingOut]:
    """Serialize a page with each finding's asset IP/hostname, originating scan and
    the canonical risk rank (real asset criticality and exposure)."""
    ctx = await _asset_risk_context(db, findings)
    scan_refs = await _scan_refs(db, findings)
    states = await _sla_states(db, findings)
    out = []
    for f in findings:
        a = ctx.get(f.asset_id, {})
        pri = priority_for(f, states.get(f.id))
        out.append(FindingOut.model_validate(f).model_copy(
            update={"asset_ip": a.get("ip"), "asset_hostname": a.get("hostname"),
                    "risk_rank": _rank_for(f, ctx),
                    "priority": pri["priority"], "priority_reason": pri["reason"],
                    "scan": scan_refs.get(f.detection_run_id)}))
    return out


async def _asset_exposure(db: AsyncSession, asset_id) -> str | None:
    """The asset's strongest service exposure (external beats internal), or None."""
    if asset_id is None:
        return None
    vals = (await db.execute(
        select(Service.exposure).where(Service.asset_id == asset_id)
    )).scalars().all()
    return strongest_exposure(vals)


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
                suggested_risk_owner=suggest_risk_owner(asset),
            )
    scan_refs = await _scan_refs(db, [finding])
    update: dict = {
        "asset_context": asset_context,
        "asset_ip": asset_context.ip_address if asset_context else None,
        "asset_hostname": asset_context.hostname if asset_context else None,
        "scan": scan_refs.get(finding.detection_run_id),
    }
    states = await _sla_states(db, [finding])
    pri = priority_for(finding, states.get(finding.id))
    update["priority"], update["priority_reason"] = pri["priority"], pri["reason"]
    # Same inputs as the list (shared builder), so a finding reads the same everywhere.
    exposure = await _asset_exposure(db, finding.asset_id)
    update["risk_rank"] = compute_risk_rank(**risk_inputs(
        finding,
        asset_criticality=asset_context.criticality if asset_context is not None else None,
        exposure=exposure,
    ))
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
    # Per-engagement SLA overrides (rules_of_engagement["sla_policy"]) layer on top.
    eng_q = select(Engagement.id, Engagement.rules_of_engagement).where(
        Engagement.tenant_id == current_user.tenant_id)
    if engagement_id:
        eng_q = eng_q.where(Engagement.id == engagement_id)
    per_engagement = {}
    for eid, roe in (await db.execute(eng_q)).all():
        own = engagement_windows(SimpleNamespace(rules_of_engagement=roe))
        if own is not None:
            per_engagement[eid] = own
    return sla_service.summarize(list(findings), windows=windows, engagement_windows=per_engagement)


@router.get("/metrics", summary="MTTR + ownership metrics")
async def finding_metrics(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    """Mobilization metrics: how fast findings actually close, and who owns the
    open ones.

    Detection answers "what is wrong"; this answers "are we fixing it". Both
    inputs already existed on the model — first_seen from the run that produced
    the finding, resolved_at from the auto-resolver or a manual close — so this
    is aggregation, not new bookkeeping.

    Tenant-scoped through the engagement join like every other route here, and
    read-only, so it routes to the read replica when one is configured.
    """
    def _scoped(q):
        q = q.join(Engagement, Finding.engagement_id == Engagement.id).where(
            Engagement.tenant_id == current_user.tenant_id)
        return q.where(Finding.engagement_id == engagement_id) if engagement_id else q

    # MTTR over findings that actually closed.
    pairs = (await db.execute(_scoped(
        select(Finding.first_seen, Finding.resolved_at)
    ).where(Finding.resolved_at.is_not(None)))).all()

    # Open work by owner. `unassigned` is a first-class bucket, not an omission:
    # a large unassigned pile is itself the finding a manager needs to see.
    owner_rows = (await db.execute(_scoped(
        select(Finding.assigned_to, func.count())
    ).where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
     .group_by(Finding.assigned_to))).all()

    open_count = sum(int(n) for _, n in owner_rows)
    return {
        "mttr": compute_mttr([(seen, resolved) for seen, resolved in pairs]),
        "open_by_owner": {
            (str(owner) if owner else "unassigned"): int(n) for owner, n in owner_rows
        },
        "open_count": open_count,
        "resolved_count": len(pairs),
    }


async def _filtered_findings(
    base: Select,
    db: AsyncSession,
    current_user: AuthUser,
    *,
    severity: FindingSeverity | None = None,
    status_filter: FindingStatus | None = None,
    active_only: bool = False,
    asset_id: uuid.UUID | None = None,
    asset_ip: str | None = None,
    mitre_technique: str | None = None,
    engagement_id: uuid.UUID | None = None,
    agent_id: uuid.UUID | None = None,
    scan: str | None = None,
    search: str | None = None,
    detection_status: DetectionStatus | None = None,
    exploit_validated: bool | None = None,
    verification_state: str | None = None,
    needs_review: bool | None = None,
    sla_breached: bool = False,
) -> tuple[Select | None, set[uuid.UUID] | None]:
    """Apply the findings-queue filters to ``base`` (any select over Finding).

    The ONE definition of "which findings does this filter set mean", shared by
    the list and the grouped view so the two can never disagree. Returns
    ``(None, set())`` when a scan filter resolves to no run — the caller answers
    with an empty result without querying findings at all.
    """
    # Scope to tenant via engagement join
    q = (
        base
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == current_user.tenant_id)
    )

    if severity:
        q = q.where(Finding.severity == severity)
    if status_filter:
        q = q.where(Finding.status == status_filter)
    if active_only:
        q = q.where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
    if asset_id:
        q = q.where(Finding.asset_id == asset_id)
    if asset_ip:
        q = q.join(Asset, Asset.id == Finding.asset_id).where(asset_ip_clause(asset_ip))
    if engagement_id:
        q = q.where(Finding.engagement_id == engagement_id)
    if agent_id:
        q = q.where(Engagement.assigned_agent_id == agent_id)
    scan_run_ids: set[uuid.UUID] | None = None
    if scan:
        scan_run_ids = await _resolve_scan_run_ids(
            db, scan, current_user.tenant_id, engagement_id=engagement_id)
        if not scan_run_ids:
            return None, scan_run_ids
        q = q.where(Finding.id.in_(
            select(DetectionRunFinding.finding_id)
            .where(DetectionRunFinding.run_id.in_(scan_run_ids))
        ))
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
    return q, scan_run_ids


@dataclass
class FindingFilters:
    """The findings-queue filter set as one value, for endpoints that need to
    honour "whatever the user filtered to" without listing (e.g. the report's
    Excel/CSV export). Field names match ``_filtered_findings`` keywords."""
    severity: FindingSeverity | None = None
    status_filter: FindingStatus | None = None
    active_only: bool = False
    asset_ip: str | None = None
    scan: str | None = None
    search: str | None = None
    detection_status: DetectionStatus | None = None
    exploit_validated: bool | None = None
    verification_state: str | None = None
    needs_review: bool | None = None
    sla_breached: bool = False

    def active(self) -> bool:
        return any((
            self.severity, self.status_filter, self.active_only, self.asset_ip, self.scan,
            (self.search or "").strip(), self.detection_status, self.exploit_validated is not None,
            self.verification_state, self.needs_review is not None, self.sla_breached,
        ))


def finding_filters(
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
    active_only: bool = Query(default=False),
    asset_ip: str | None = Query(default=None, min_length=1, max_length=45),
    scan: str | None = Query(default=None, min_length=1, max_length=64),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    detection_status: DetectionStatus | None = Query(default=None),
    exploit_validated: bool | None = Query(default=None),
    verification_state: str | None = Query(default=None),
    needs_review: bool | None = Query(default=None),
    sla_breached: bool = Query(default=False),
) -> FindingFilters:
    """FastAPI dependency: the same query parameters the findings list takes."""
    return FindingFilters(
        severity=severity, status_filter=status_filter, active_only=active_only, asset_ip=asset_ip,
        scan=scan, search=search, detection_status=detection_status, exploit_validated=exploit_validated,
        verification_state=verification_state, needs_review=needs_review, sla_breached=sla_breached,
    )


async def filtered_finding_ids(
    db: AsyncSession, current_user: AuthUser, engagement_id: uuid.UUID, filters: FindingFilters,
    *, agent_id: uuid.UUID | None = None,
) -> set[uuid.UUID] | None:
    """Ids of the engagement's findings matching ``filters``; None = no filter.

    ``agent_id`` is an extra axis the Findings list filters on but ``FindingFilters``
    does not carry; threaded through so a findings export matches an agent-filtered view.
    """
    if not filters.active() and agent_id is None:
        return None
    q, _ = await _filtered_findings(
        select(Finding.id), db, current_user, engagement_id=engagement_id,
        severity=filters.severity, status_filter=filters.status_filter, active_only=filters.active_only,
        asset_ip=filters.asset_ip, scan=filters.scan, search=filters.search,
        detection_status=filters.detection_status, exploit_validated=filters.exploit_validated,
        verification_state=filters.verification_state, needs_review=filters.needs_review,
        sla_breached=filters.sla_breached, agent_id=agent_id,
    )
    if q is None:
        return set()
    return set((await db.execute(q)).scalars().all())


@router.get("", response_model=PaginatedResponse[FindingOut], summary="List findings with filters")
async def list_findings(
    db: DB,
    current_user: AuthUser,
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
    active_only: bool = Query(
        default=False,
        description=(
            "Restrict to findings that are still an active exposure "
            "(status open or confirmed) — the same 'tracked' set /summary, "
            "/sla-summary and the analytics endpoints count. Use this instead "
            "of status=open, which drops confirmed findings."
        ),
    ),
    asset_id: uuid.UUID | None = Query(default=None),
    asset_ip: str | None = Query(
        default=None, min_length=1, max_length=45,
        description="Affected asset IP — exact address, or a prefix such as 192.168.1.",
    ),
    mitre_technique: str | None = Query(default=None),
    engagement_id: uuid.UUID | None = Query(default=None),
    agent_id: uuid.UUID | None = Query(default=None),
    scan: str | None = Query(
        default=None, min_length=1, max_length=64,
        description=(
            "Restrict to findings a single scan TOUCHED — new, reaffirmed or "
            "resolved — via the per-run membership table. Accepts an "
            "SCN-YYMMDD-XXXXXX reference, a scan-job id, or a detection-run id. "
            "An unknown scan returns an empty page."
        ),
    ),
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
    q, scan_run_ids = await _filtered_findings(
        select(Finding), db, current_user,
        severity=severity, status_filter=status_filter, active_only=active_only,
        asset_id=asset_id, asset_ip=asset_ip, mitre_technique=mitre_technique,
        engagement_id=engagement_id, agent_id=agent_id, scan=scan, search=search,
        detection_status=detection_status, exploit_validated=exploit_validated,
        verification_state=verification_state, needs_review=needs_review,
        sla_breached=sla_breached,
    )
    if q is None:
        return paginate([], 0, page, page_size)

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
    page_out = await _with_asset_identity(db, items)
    if scan_run_ids:
        # Filtering by scan → tell each finding what THIS scan did to it (new /
        # reaffirmed / resolved), so the filtered view answers "what did scan X find"
        # rather than just narrowing the list.
        outcomes = await _scan_outcomes(db, scan_run_ids, [f.id for f in page_out])
        page_out = [f.model_copy(update={"scan_outcome": outcomes.get(f.id)}) for f in page_out]
    return paginate(page_out, total, page, page_size)


# Rows loaded to build groups. Far above any real engagement; a hit is reported
# (truncated=true) rather than silently producing partial counts.
GROUP_ROW_CAP = 25_000
_JSON_FALSEY = {"", "false", "0", "null", "none"}


def _json_flag(value: str | None) -> bool:
    return value is not None and value.strip().lower() not in _JSON_FALSEY


def _json_port(value: str | None) -> int | None:
    try:
        return normalize_port(value)
    except ValueError:
        return None


def _group_select() -> Select:
    """Lean columns for grouping — never the whole evidence blob."""
    ev = Finding.evidence
    return select(
        Finding.id, Finding.engagement_id, Finding.title, Finding.severity, Finding.status,
        Finding.cvss_score, Finding.risk_score, Finding.epss_score, Finding.cve_ids,
        Finding.asset_id, Finding.exploit_validated, Finding.first_seen,
        Finding.last_seen, Finding.created_at,
        ev["rule_id"].astext.label("rule_id"),
        ev["port"].astext.label("port"),
        ev["cpe"].astext.label("cpe"),
        ev["kev"].astext.label("kev"),
        ev["enrichment"]["kev"].astext.label("enrichment_kev"),
    )


def _group_row(r, identity: dict) -> GroupRow:
    ip, host = identity.get(r.asset_id, (None, None))
    cvss = float(r.cvss_score) if r.cvss_score is not None else None
    # Same effective risk the list's "risk" sort uses: risk_score, else CVSS×100.
    # Decimal arithmetic, as in SQL, so 9.8 × 100 is exactly 980.
    risk = float(r.risk_score if r.risk_score is not None
                 else r.cvss_score * 100 if r.cvss_score is not None else 0)
    return GroupRow(
        id=r.id, engagement_id=r.engagement_id, title=r.title,
        severity=getattr(r.severity, "value", r.severity),
        status=getattr(r.status, "value", r.status),
        cvss=cvss, risk=risk,
        epss=float(r.epss_score) if r.epss_score is not None else None,
        cve_ids=tuple(r.cve_ids or ()),
        asset_id=r.asset_id, asset_ip=ip, asset_hostname=host,
        port=_json_port(r.port), rule_id=r.rule_id or None, cpe=r.cpe or None,
        kev=_json_flag(r.kev) or _json_flag(r.enrichment_kev),
        exploit_validated=bool(r.exploit_validated),
        first_seen=r.first_seen or r.created_at, last_seen=r.last_seen,
    )


@router.get("/groups", response_model=FindingGroupPage,
            summary="Similar findings grouped into one-fix units, in priority order")
async def list_finding_groups(
    db: DB,
    current_user: AuthUser,
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
    active_only: bool = Query(default=False),
    asset_id: uuid.UUID | None = Query(default=None),
    asset_ip: str | None = Query(default=None, min_length=1, max_length=45),
    mitre_technique: str | None = Query(default=None),
    engagement_id: uuid.UUID | None = Query(default=None),
    agent_id: uuid.UUID | None = Query(default=None),
    scan: str | None = Query(default=None, min_length=1, max_length=64),
    search: str | None = Query(default=None, min_length=1, max_length=200),
    detection_status: DetectionStatus | None = Query(default=None),
    exploit_validated: bool | None = Query(default=None),
    verification_state: str | None = Query(default=None),
    needs_review: bool | None = Query(default=None),
    sla_breached: bool = Query(default=False),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    """The same filter set as ``GET /findings`` (shared ``_filtered_findings``),
    grouped by services/finding_groups. Each group carries its members, so the
    UI can expand a group and open any finding without a second filter."""
    q, _scan_runs = await _filtered_findings(
        _group_select(), db, current_user,
        severity=severity, status_filter=status_filter, active_only=active_only,
        asset_id=asset_id, asset_ip=asset_ip, mitre_technique=mitre_technique,
        engagement_id=engagement_id, agent_id=agent_id, scan=scan, search=search,
        detection_status=detection_status, exploit_validated=exploit_validated,
        verification_state=verification_state, needs_review=needs_review,
        sla_breached=sla_breached,
    )
    if q is None:
        return FindingGroupPage(items=[], total=0, page=page, page_size=page_size,
                                pages=1, finding_total=0)
    rows = (await db.execute(q.order_by(Finding.id).limit(GROUP_ROW_CAP + 1))).all()
    truncated = len(rows) > GROUP_ROW_CAP
    rows = rows[:GROUP_ROW_CAP]

    asset_ids = {r.asset_id for r in rows if r.asset_id is not None}
    identity: dict = {}
    if asset_ids:
        identity = {aid: (ip, host) for aid, ip, host in (await db.execute(
            select(Asset.id, Asset.ip_address, Asset.hostname).where(Asset.id.in_(asset_ids))
        )).all()}

    groups = build_groups(_group_row(r, identity) for r in rows)
    total = len(groups)
    pages = max(1, -(-total // page_size))
    start = (page - 1) * page_size
    return FindingGroupPage(
        items=groups[start:start + page_size], total=total, page=page,
        page_size=page_size, pages=pages, finding_total=len(rows), truncated=truncated,
    )


@router.get("/assets", response_model=list[FindingAssetOption],
            summary="Assets that have findings — feeds the IP filter")
async def finding_assets(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
    active_only: bool = Query(default=False),
):
    """Distinct affected assets with their finding counts, most-affected first,
    tenant-scoped through the engagement. Bounded to 500 rows."""
    q = (
        select(Asset.id, Asset.ip_address, Asset.hostname, func.count(Finding.id))
        .join(Finding, Finding.asset_id == Asset.id)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == current_user.tenant_id)
        .where(Asset.ip_address.isnot(None))
    )
    if engagement_id:
        q = q.where(Finding.engagement_id == engagement_id)
    if active_only:
        q = q.where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
    q = (q.group_by(Asset.id, Asset.ip_address, Asset.hostname)
         .order_by(func.count(Finding.id).desc(), Asset.ip_address)
         .limit(500))
    rows = (await db.execute(q)).all()
    return [FindingAssetOption(asset_id=aid, ip_address=ip, hostname=host, findings=n)
            for aid, ip, host, n in rows]


@router.get("/scans", response_model=list[ScanOption],
            summary="Scans that produced findings — feeds the scan filter & compare")
async def finding_scans(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    """Distinct scans (jobs) that have at least one detection run, each with the
    count of findings it touched, newest first, tenant-scoped through the
    engagement. Bounded to 200 rows. Feeds the findings 'filter by scan' control
    and the two-scan compare picker."""
    scanned_at = func.coalesce(
        ScanJob.completed_at, ScanJob.started_at, func.max(DetectionRun.started_at))
    q = (
        select(
            ScanJob.id, ScanJob.reference, ScanJob.use_case_id, ScanJob.intensity,
            scanned_at.label("scanned_at"), ScanJob.status,
            func.count(func.distinct(DetectionRunFinding.finding_id)),
        )
        .select_from(ScanJob)
        .join(DetectionRun, DetectionRun.job_id == ScanJob.id)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .outerjoin(DetectionRunFinding, DetectionRunFinding.run_id == DetectionRun.id)
        .where(Engagement.tenant_id == current_user.tenant_id)
    )
    if engagement_id:
        q = q.where(ScanJob.engagement_id == engagement_id)
    q = (q.group_by(ScanJob.id)
         .order_by(scanned_at.desc().nullslast(), ScanJob.id)
         .limit(200))
    rows = (await db.execute(q)).all()
    return [
        ScanOption(
            job_id=jid, reference=ref, use_case_id=uc, intensity=inten,
            scanned_at=at, status=getattr(st, "value", st), findings=int(n or 0),
        )
        for jid, ref, uc, inten, at, st, n in rows
    ]


_COMPARE_BUCKET_CAP = 500
_SEVERITY_KEYS = ("critical", "high", "medium", "low", "info")


async def _scan_snapshots(
    db: AsyncSession, run_ids: set[uuid.UUID],
) -> dict[uuid.UUID, ScanCompareSnapshot]:
    """Each present finding as the scan saw it. When a scan spans several runs the
    latest run's snapshot wins. A row recorded before snapshots existed has no
    severity and reads as 'no snapshot'."""
    rows = (await db.execute(
        select(DetectionRunFinding.finding_id, DetectionRunFinding.severity,
               DetectionRunFinding.risk_score, DetectionRunFinding.status)
        .join(DetectionRun, DetectionRun.id == DetectionRunFinding.run_id)
        .where(DetectionRunFinding.run_id.in_(run_ids),
               DetectionRunFinding.outcome.in_((RUN_FINDING_NEW, RUN_FINDING_REAFFIRMED)))
        .order_by(DetectionRun.started_at.asc())
    )).all()
    return {
        fid: ScanCompareSnapshot(
            severity=sev, risk_score=float(risk) if risk is not None else None, status=st)
        for fid, sev, risk, st in rows
    }


def _snapshot_change(
    before: ScanCompareSnapshot | None, after: ScanCompareSnapshot | None,
) -> tuple[bool, bool, float | None] | None:
    """(severity changed, status changed, risk delta) between two scans' snapshots of
    one finding, or None when nothing differs or either side has no snapshot."""
    if before is None or after is None or before.severity is None or after.severity is None:
        return None
    sev = before.severity != after.severity
    st = before.status != after.status
    delta = None
    if before.risk_score is not None and after.risk_score is not None:
        delta = round(after.risk_score - before.risk_score, 2)
    if not (sev or st or (delta not in (None, 0))):
        return None
    return sev, st, delta


def _scan_summary(
    ids: set[uuid.UUID], snaps: dict[uuid.UUID, ScanCompareSnapshot],
    findings: dict[uuid.UUID, FindingOut],
) -> ScanCompareSummary:
    by_sev = {k: 0 for k in _SEVERITY_KEYS}
    risks: list[float] = []
    from_snapshot = True
    for fid in ids:
        snap = snaps.get(fid)
        fo = findings.get(fid)
        sev = snap.severity if snap and snap.severity else None
        if sev is None:
            from_snapshot = False
            sev = str(getattr(fo.severity, "value", fo.severity)) if fo else None
        if sev in by_sev:
            by_sev[sev] += 1
        risk = snap.risk_score if snap and snap.risk_score is not None else (
            float(fo.risk_rank) if fo and fo.risk_rank is not None else None)
        if risk is not None:
            risks.append(risk)
    return ScanCompareSummary(
        total=len(ids), by_severity=by_sev,
        average_risk=round(sum(risks) / len(risks), 1) if risks else None,
        from_snapshot=from_snapshot)


async def build_scan_compare(
    db: AsyncSession, tenant_id: uuid.UUID, a: str, b: str,
    *, engagement_id: uuid.UUID | None = None, cap: int | None = _COMPARE_BUCKET_CAP,
) -> ScanCompareOut:
    """The diff itself, shared by the JSON endpoint, the portal and the export."""
    a_runs = await _resolve_scan_run_ids(db, a, tenant_id, engagement_id=engagement_id)
    b_runs = await _resolve_scan_run_ids(db, b, tenant_id, engagement_id=engagement_id)
    if not a_runs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Scan not found: {a}")
    if not b_runs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Scan not found: {b}")

    present_a = set((await db.execute(_present_finding_ids(a_runs))).scalars().all())
    present_b = set((await db.execute(_present_finding_ids(b_runs))).scalars().all())
    new_ids = present_b - present_a
    fixed_ids = present_a - present_b
    still_ids = present_a & present_b

    # Load the union ONCE, tenant-scoped, and serialise with asset + scan identity;
    # then bucket. (The tenant join also drops any id that isn't the caller's.)
    all_ids = new_ids | fixed_ids | still_ids
    serialized: dict[uuid.UUID, FindingOut] = {}
    if all_ids:
        load = (
            select(Finding)
            .join(Engagement, Finding.engagement_id == Engagement.id)
            .where(Engagement.tenant_id == tenant_id,
                   Finding.id.in_(all_ids))
        )
        if engagement_id is not None:
            load = load.where(Finding.engagement_id == engagement_id)
        rows = (await db.execute(load)).scalars().all()
        serialized = {fo.id: fo for fo in await _with_asset_identity(db, rows)}

    snaps_a = await _scan_snapshots(db, a_runs)
    snaps_b = await _scan_snapshots(db, b_runs)

    def bucket(ids: set[uuid.UUID]) -> list[FindingOut]:
        items = [serialized[i] for i in ids if i in serialized]
        items.sort(key=lambda f: (f.risk_rank or 0), reverse=True)
        return items if cap is None else items[:cap]

    changes: list[ScanCompareChange] = []
    for fid in still_ids:
        if fid not in serialized:
            continue
        diff = _snapshot_change(snaps_a.get(fid), snaps_b.get(fid))
        if diff is None:
            continue
        sev_changed, status_changed, delta = diff
        changes.append(ScanCompareChange(
            finding=serialized[fid], before=snaps_a[fid], after=snaps_b[fid],
            severity_changed=sev_changed, status_changed=status_changed, risk_delta=delta))
    # What matters most first: a severity change, then the size of the score move.
    changes.sort(key=lambda c: (c.severity_changed, abs(c.risk_delta or 0)), reverse=True)

    return ScanCompareOut(
        a=await _scan_meta(db, a_runs),
        b=await _scan_meta(db, b_runs),
        counts=ScanCompareCounts(
            new=len(new_ids), fixed=len(fixed_ids), still_present=len(still_ids),
            changed=len(changes)),
        summary_a=_scan_summary(present_a, snaps_a, serialized),
        summary_b=_scan_summary(present_b, snaps_b, serialized),
        new=bucket(new_ids), fixed=bucket(fixed_ids), still_present=bucket(still_ids),
        changed=changes if cap is None else changes[:cap],
    )


@router.get("/compare", response_model=ScanCompareOut,
            summary="Diff two scans — new, fixed, still present, and what changed")
async def compare_scans(
    db: ReadDB,
    current_user: AuthUser,
    a: str = Query(
        ..., min_length=1, max_length=64,
        description="Baseline scan — SCN-YYMMDD-XXXXXX reference, job id, or run id."),
    b: str = Query(
        ..., min_length=1, max_length=64,
        description="Target scan — same accepted forms as `a`."),
    engagement_id: uuid.UUID | None = Query(
        default=None,
        description="Pin both scans and the finding load to one engagement "
                    "(the portal always sets this)."),
):
    """Diff two scans through the per-run membership table. A finding is 'present' in
    a scan when that scan saw it new or reaffirmed; then
      new           = present in b but not a,
      fixed         = present in a but not b,
      still_present = present in both,
      changed       = still_present whose severity, risk score or status differs
                      between the two scans' snapshots.
    `counts` are the true totals; each finding list is capped at 500, most-severe
    first. An unknown scan (no detection runs) is a 404."""
    return await build_scan_compare(
        db, current_user.tenant_id, a, b, engagement_id=engagement_id)


def compare_to_csv(result: ScanCompareOut) -> str:
    """One row per finding with its bucket and each scan's recorded severity, score and
    status. 'Before' is scan A and 'After' is scan B."""
    import csv
    import io

    header = ["bucket", "finding_id", "title", "host", "cve", "severity_now", "risk_now",
              "severity_a", "severity_b", "risk_a", "risk_b", "risk_change",
              "status_a", "status_b"]
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(header)

    def host(f: FindingOut) -> str:
        return f.asset_ip or f.asset_hostname or ""

    def line(bucket: str, f: FindingOut, before=None, after=None, delta=None):
        w.writerow([csv_cell(v) for v in (
            bucket, str(f.id), f.title, host(f), ";".join(f.cve_ids or []),
            getattr(f.severity, "value", f.severity), f.risk_rank,
            before.severity if before else None, after.severity if after else None,
            before.risk_score if before else None, after.risk_score if after else None,
            delta, before.status if before else None, after.status if after else None)])

    for f in result.new:
        line("new", f)
    for f in result.fixed:
        line("fixed", f)
    changed_ids = {c.finding.id for c in result.changed}
    for c in result.changed:
        line("changed", c.finding, c.before, c.after, c.risk_delta)
    for f in result.still_present:
        if f.id not in changed_ids:
            line("unchanged", f)
    return "\ufeff" + out.getvalue()


@router.get("/compare/export", summary="Download a two-scan comparison as CSV or JSON")
async def export_scan_compare(
    db: ReadDB,
    current_user: AuthUser,
    a: str = Query(..., min_length=1, max_length=64),
    b: str = Query(..., min_length=1, max_length=64),
    format: Literal["csv", "json"] = Query(default="csv"),
    engagement_id: uuid.UUID | None = Query(default=None),
):
    """The whole comparison, uncapped — an export that silently dropped rows past 500
    would be worse than none."""
    result = await build_scan_compare(
        db, current_user.tenant_id, a, b, engagement_id=engagement_id, cap=None)
    ref_a = result.a.reference if result.a and result.a.reference else "A"
    ref_b = result.b.reference if result.b and result.b.reference else "B"
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"compare-{ref_a}-vs-{ref_b}")
    if format == "json":
        return Response(
            content=result.model_dump_json(),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{name}.json"'})
    return Response(
        content=compare_to_csv(result).encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}.csv"'})


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


@router.get(
    "/ids",
    summary="Finding ids matching the current filters, for scoping a findings export",
)
async def list_finding_ids(
    db: DB,
    current_user: AuthUser,
    engagement_id: uuid.UUID = Query(..., description="Engagement to scope the export to"),
    agent_id: uuid.UUID | None = Query(default=None),
    filters: FindingFilters = Depends(finding_filters),
) -> dict:
    """The ids the Findings page would export under the active filters.

    ``finding_ids`` is ``null`` when no finding-level filter is active — the
    caller then exports the whole engagement instead of sending a long id list.
    Declared before ``/{finding_id}`` so the literal path wins over the UUID
    parameter route.
    """
    ids = await filtered_finding_ids(db, current_user, engagement_id, filters, agent_id=agent_id)
    return {"finding_ids": None if ids is None else sorted(str(i) for i in ids)}


@router.get("/{finding_id}", response_model=FindingOut, summary="Finding detail")
async def get_finding(
    finding_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    return await _finding_detail_out(db, finding)


async def risk_explanation_for(db: AsyncSession, finding: Finding) -> dict:
    """The full working of the finding's risk rank, from the same inputs as the list,
    the detail and the sort. Shared by the operator and customer-portal routes."""
    asset = None
    if finding.asset_id is not None:
        asset = (await db.execute(
            select(Asset).where(Asset.id == finding.asset_id,
                                Asset.engagement_id == finding.engagement_id)
        )).scalar_one_or_none()
    exposure = await _asset_exposure(db, finding.asset_id) if asset is not None else None
    criticality = getattr(asset.criticality, "value", asset.criticality) if asset is not None else None
    explanation = explain_risk_rank(**risk_inputs(
        finding, asset_criticality=criticality, exposure=exposure))
    source = exposure_source(finding, exposure)
    for dim in explanation["dimensions"]:
        for item in dim["inputs"]:
            if item["key"] == "internet_facing" and item["source"] == "recorded":
                item["note"] = f"{item['note']} (from {source})"
    stored = float(finding.risk_score) if finding.risk_score is not None else None
    explanation["context"] = {
        "asset": ({"ip_address": asset.ip_address, "hostname": asset.hostname,
                   "criticality": criticality} if asset is not None else None),
        "internet_exposure_source": source,
        "service_exposure": exposure,
    }
    # The stored score is what "Highest risk" sorts on. It is recomputed from these same
    # inputs after every scan; a mismatch means the sort key is waiting for a refresh.
    explanation["stored_score"] = stored
    explanation["stored_in_sync"] = stored is not None and round(stored) == explanation["score"]
    states = await _sla_states(db, [finding])
    explanation["priority"] = priority_for(finding, states.get(finding.id))
    return explanation


@router.get("/{finding_id}/risk-explanation",
            summary="How this finding's 0-1000 risk score is calculated")
async def finding_risk_explanation(
    finding_id: uuid.UUID,
    db: ReadDB,
    current_user: AuthUser,
):
    """Every input, weight, dimension and the severity band behind the score, with each
    unrecorded input marked as a default. Read-only; tenant-scoped like the detail."""
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    return await risk_explanation_for(db, finding)


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
        tenant_id=current_user.tenant_id,
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
