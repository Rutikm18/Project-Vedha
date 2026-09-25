import ipaddress
import re
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
from app.models.detection_run import DetectionRun
from app.models.detection_run_finding import (
    DetectionRunFinding, RUN_FINDING_NEW, RUN_FINDING_REAFFIRMED,
)
from app.models.scan_job import ScanJob
from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.common import PaginatedResponse, paginate
from app.schemas.finding import (
    FindingAssetContext, FindingAssetOption, FindingEventOut, FindingOut, FindingPatch, FindingReopen,
    FindingScanRef, FindingSummary, FindingTimeline, ScanCompareCounts, ScanCompareOut,
    ScanOption, SlaSummary,
)
from app.services import finding_events as events_service
from app.services.finding_metrics import compute_mttr
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


async def _with_asset_identity(db: AsyncSession, findings: list[Finding]) -> list[FindingOut]:
    """Serialize a page with each finding's asset IP/hostname and originating scan
    — ONE query each for the page, never one per row."""
    ids = {f.asset_id for f in findings if f.asset_id is not None}
    identity: dict = {}
    if ids:
        rows = (await db.execute(
            select(Asset.id, Asset.ip_address, Asset.hostname).where(Asset.id.in_(ids))
        )).all()
        identity = {aid: (ip, host) for aid, ip, host in rows}
    scan_refs = await _scan_refs(db, findings)
    out = []
    for f in findings:
        ip, host = identity.get(f.asset_id, (None, None))
        out.append(FindingOut.model_validate(f).model_copy(
            update={"asset_ip": ip, "asset_hostname": host,
                    "scan": scan_refs.get(f.detection_run_id)}))
    return out


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
    scan_refs = await _scan_refs(db, [finding])
    update: dict = {
        "asset_context": asset_context,
        "asset_ip": asset_context.ip_address if asset_context else None,
        "asset_hostname": asset_context.hostname if asset_context else None,
        "scan": scan_refs.get(finding.detection_run_id),
    }
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
    if scan:
        run_ids = await _resolve_scan_run_ids(
            db, scan, current_user.tenant_id, engagement_id=engagement_id)
        if not run_ids:
            return paginate([], 0, page, page_size)
        q = q.where(Finding.id.in_(
            select(DetectionRunFinding.finding_id)
            .where(DetectionRunFinding.run_id.in_(run_ids))
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
    return paginate(await _with_asset_identity(db, items), total, page, page_size)


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


@router.get("/compare", response_model=ScanCompareOut,
            summary="Diff two scans — what's new, fixed, and still present")
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
      still_present = present in both.
    `counts` are the true totals; each finding list is capped at 500, most-severe
    first. An unknown scan (no detection runs) is a 404."""
    a_runs = await _resolve_scan_run_ids(
        db, a, current_user.tenant_id, engagement_id=engagement_id)
    b_runs = await _resolve_scan_run_ids(
        db, b, current_user.tenant_id, engagement_id=engagement_id)
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
            .where(Engagement.tenant_id == current_user.tenant_id,
                   Finding.id.in_(all_ids))
        )
        if engagement_id is not None:
            load = load.where(Finding.engagement_id == engagement_id)
        rows = (await db.execute(load)).scalars().all()
        serialized = {fo.id: fo for fo in await _with_asset_identity(db, rows)}

    def bucket(ids: set[uuid.UUID]) -> list[FindingOut]:
        items = [serialized[i] for i in ids if i in serialized]
        items.sort(key=lambda f: (f.risk_rank or 0), reverse=True)
        return items[:_COMPARE_BUCKET_CAP]

    return ScanCompareOut(
        a=await _scan_meta(db, a_runs),
        b=await _scan_meta(db, b_runs),
        counts=ScanCompareCounts(
            new=len(new_ids), fixed=len(fixed_ids), still_present=len(still_ids)),
        new=bucket(new_ids), fixed=bucket(fixed_ids), still_present=bucket(still_ids),
    )


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
