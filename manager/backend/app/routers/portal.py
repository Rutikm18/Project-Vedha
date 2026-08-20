"""
portal.py — the CUSTOMER-facing read API (Part 2, Phase 2). Every route is scoped
to the client's one bound engagement via `client_scoped` / `assert_client` (the
Phase-0 choke point), so a route physically cannot return another engagement's
data. Read-only; customers cannot create engagements, run scans, or see fleet.

Data-exposure controls:
  * findings are serialized through the ClientFindingOut whitelist (no internal
    triage/exploit/evidence fields)
  * reports are gated to review_status == approved (drafts/internal never leak)
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select

from app.auth.portal_scope import ClientUser, assert_client, client_scoped
from app.dependencies import DB
from app.models.engagement import Engagement
from app.models.enums import (
    FindingSeverity, FindingStatus, ReviewStatus, ScanJobStatus, ScanJobType,
)
from app.models.finding import Finding
from app.models.llm_output import LLMOutput
from app.models.remediation_plan import RemediationPlan
from app.models.scan_job import ScanJob
from app.models.scan_request import ScanRequest, SR_PENDING
from app.schemas.portal import (
    ClientEngagementOut,
    ClientFindingOut,
    ClientPostureOut,
    ClientReportContent,
    ClientReportOut,
    ClientScanOut,
    ClientScanRequestOut,
    ClientSummaryOut,
    ClientTrendsOut,
    ScanRequestCreate,
)
from app.services import portal_metrics
from app.services import posture as posture_service
from app.services.audit import record_audit
from app.services.remediation_kb import os_key, recipe_for_finding
from app.services.scope_targets import validate_targets_in_scope

router = APIRouter(prefix="/portal", tags=["portal"])

_OPEN_STATES = (FindingStatus.open, FindingStatus.confirmed)
# How many requests a customer may have awaiting operator review at once. Requests
# queue (they don't block at one), but a cap keeps a customer from flooding the
# operator inbox.
_MAX_PENDING_REQUESTS = 5
_VALID_SCAN_TYPES = {t.value for t in ScanJobType}

# The capability use-cases a customer may request — a curated subset of the
# operator use-case catalog (agents._USE_CASES), so the portal never offers a
# use case the probe cannot perform. Imported lazily to avoid an import cycle.
_PORTAL_USE_CASE_IDS = (
    "uc_discovery_only", "uc_device_inventory", "uc_full_assessment",
    "uc_external_web_triage", "uc_web_app_triage", "uc_db_exposure",
    "uc_windows_estate", "uc_snmp_exposure", "uc_udp_service_exposure",
    "uc_iot_device_survey", "uc_ai_endpoint_sweep", "uc_full_port_audit",
    "uc_ot_passive",
)


def _portal_use_cases() -> dict:
    """The operator use-case catalog (single source of truth), curated to what a
    customer may request. Lazy import breaks the router import cycle."""
    from app.routers.agents import _USE_CASES
    return {uid: _USE_CASES[uid] for uid in _PORTAL_USE_CASE_IDS if uid in _USE_CASES}


def _enum_val(v) -> str:
    return v.value if hasattr(v, "value") else str(v)


@router.get("/engagement", response_model=ClientEngagementOut,
            summary="The customer's assigned engagement")
async def portal_engagement(user: ClientUser, db: DB):
    eng_id = assert_client(user)
    eng = (await db.execute(
        select(Engagement).where(Engagement.id == eng_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    return ClientEngagementOut(
        id=eng.id, name=eng.name, status=_enum_val(eng.status),
        scope_cidr_count=len(eng.scope_cidrs or []),
        scope_cidrs=list(eng.scope_cidrs or []),
        has_assigned_agent=eng.assigned_agent_id is not None,
    )


@router.get("/findings", response_model=list[ClientFindingOut],
            summary="Findings for the customer's engagement")
async def portal_findings(
    user: ClientUser,
    db: DB,
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
):
    q = client_scoped(select(Finding), user, Finding.engagement_id)
    if severity:
        q = q.where(Finding.severity == severity)
    if status_filter:
        q = q.where(Finding.status == status_filter)
    q = q.order_by(Finding.risk_score.desc().nullslast())
    rows = (await db.execute(q)).scalars().all()
    return [ClientFindingOut.model_validate(r) for r in rows]


@router.get("/findings/{finding_id}", response_model=ClientFindingOut,
            summary="A single finding (scoped)")
async def portal_finding(finding_id: uuid.UUID, user: ClientUser, db: DB):
    r = (await db.execute(
        client_scoped(select(Finding).where(Finding.id == finding_id),
                      user, Finding.engagement_id)
    )).scalar_one_or_none()
    if r is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")
    return ClientFindingOut.model_validate(r)


@router.get("/findings/{finding_id}/remediation",
            summary="Structured remediation plan (KB always; AI only once reviewed)")
async def portal_finding_remediation(
    finding_id: uuid.UUID, user: ClientUser, db: DB,
    os: str = Query(default="generic"),
):
    """Customer-facing structured remediation, replacing the plain `remediation`
    string. The deterministic KB recipe is served ALWAYS; a stored AI plan reaches
    the customer only once an operator has reviewed it — the same approval gate the
    reports route uses, so an unreviewed AI plan never leaks."""
    finding = (await db.execute(
        client_scoped(select(Finding).where(Finding.id == finding_id),
                      user, Finding.engagement_id)
    )).scalar_one_or_none()
    if finding is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")

    key = os_key(os)
    row = (await db.execute(
        select(RemediationPlan).where(
            RemediationPlan.finding_id == finding_id,
            RemediationPlan.os == key,
        )
    )).scalar_one_or_none()
    if row is not None and row.reviewed:
        # Strip operator-only metadata (e.g. the AI model name) from the
        # customer payload — the reviewed plan content is what's approved for them.
        plan = {k: v for k, v in row.plan.items() if k != "model"}
        source = plan.get("source", row.source)
    else:
        plan = recipe_for_finding(finding, key)
        source = plan["source"]
    return {"finding_id": str(finding_id), "os": key, "source": source, "plan": plan}


@router.get("/posture", response_model=ClientPostureOut,
            summary="Posture scorecard for the customer's engagement")
async def portal_posture(user: ClientUser, db: DB):
    rows = (await db.execute(
        client_scoped(select(Finding), user, Finding.engagement_id)
        .where(Finding.status.in_(_OPEN_STATES))
    )).scalars().all()
    views = [_posture_view(f) for f in rows]
    s = posture_service.compute_scores(views)
    return ClientPostureOut(
        risk_index=s.risk_index, exploitable_score=s.exploitable_score,
        posture_score=s.posture_score, grade=s.grade, open_findings=len(views),
    )


def _metric_finding(f: Finding) -> portal_metrics.MetricFinding:
    return portal_metrics.MetricFinding(
        severity=_enum_val(f.severity), status=_enum_val(f.status),
        first_seen=f.first_seen, resolved_at=f.resolved_at,
    )


def _posture_view(f: Finding) -> posture_service.FindingView:
    return posture_service.FindingView(
        id=str(f.id), severity=_enum_val(f.severity),
        risk_score=float(f.risk_score) if f.risk_score is not None else None,
        epss_score=float(f.epss_score) if f.epss_score is not None else None,
        exploitable=bool(f.exploitable), exploit_validated=bool(f.exploit_validated),
        asset_criticality=None, first_seen=f.first_seen, last_seen=f.last_seen,
    )


@router.get("/summary", response_model=ClientSummaryOut,
            summary="Dashboard summary: posture + KPI counts + queue state")
async def portal_summary(user: ClientUser, db: DB):
    findings = (await db.execute(
        client_scoped(select(Finding), user, Finding.engagement_id)
    )).scalars().all()
    open_views = [_posture_view(f) for f in findings
                  if f.status in _OPEN_STATES]
    s = posture_service.compute_scores(open_views)
    metrics = [_metric_finding(f) for f in findings]
    open_count, closed_count = portal_metrics.open_closed_counts(metrics)

    pending = (await db.execute(
        client_scoped(select(func.count()).select_from(ScanRequest),
                      user, ScanRequest.engagement_id)
        .where(ScanRequest.status == SR_PENDING)
    )).scalar_one()
    running = (await db.execute(
        client_scoped(select(func.count()).select_from(ScanJob),
                      user, ScanJob.engagement_id)
        .where(ScanJob.status.in_((ScanJobStatus.pending, ScanJobStatus.running)))
    )).scalar_one()

    return ClientSummaryOut(
        posture=ClientPostureOut(
            risk_index=s.risk_index, exploitable_score=s.exploitable_score,
            posture_score=s.posture_score, grade=s.grade, open_findings=len(open_views)),
        open_findings=open_count, closed_findings=closed_count,
        severity_counts=portal_metrics.severity_breakdown(metrics, open_only=True),
        pending_requests=int(pending), running_jobs=int(running),
    )


@router.get("/trends", response_model=ClientTrendsOut,
            summary="Severity breakdown + opened/closed timeline")
async def portal_trends(user: ClientUser, db: DB):
    findings = (await db.execute(
        client_scoped(select(Finding), user, Finding.engagement_id)
    )).scalars().all()
    metrics = [_metric_finding(f) for f in findings]
    return ClientTrendsOut(
        by_severity=portal_metrics.severity_breakdown(metrics, open_only=True),
        timeline=portal_metrics.status_timeline(metrics),
    )


@router.get("/reports", response_model=list[ClientReportOut],
            summary="Approved reports for the customer's engagement")
async def portal_reports(user: ClientUser, db: DB):
    rows = (await db.execute(
        client_scoped(select(LLMOutput), user, LLMOutput.engagement_id)
        .where(LLMOutput.review_status == ReviewStatus.approved)
        .order_by(LLMOutput.generated_at.desc())
    )).scalars().all()
    return [ClientReportOut.model_validate(r) for r in rows]


@router.get("/reports/{report_id}", response_model=ClientReportContent,
            summary="Download an approved report")
async def portal_report(report_id: uuid.UUID, user: ClientUser, db: DB):
    # An unapproved / out-of-scope report is filtered out → 404, so a customer
    # cannot even learn that a draft exists.
    r = (await db.execute(
        client_scoped(select(LLMOutput).where(LLMOutput.id == report_id),
                      user, LLMOutput.engagement_id)
        .where(LLMOutput.review_status == ReviewStatus.approved)
    )).scalar_one_or_none()
    if r is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    return ClientReportContent(id=r.id, output_type=r.output_type, model=r.model,
                               generated_at=r.generated_at, content=r.output)


@router.get("/scans", response_model=list[ClientScanOut],
            summary="Scan history + request status for the customer's engagement")
async def portal_scans(user: ClientUser, db: DB):
    jobs = (await db.execute(
        client_scoped(select(ScanJob), user, ScanJob.engagement_id)
        .order_by(ScanJob.created_at.desc())
    )).scalars().all()
    reqs = (await db.execute(
        client_scoped(select(ScanRequest), user, ScanRequest.engagement_id)
        .order_by(ScanRequest.requested_at.desc())
    )).scalars().all()
    out = [
        ClientScanOut(id=j.id, kind="job", scan_type=_enum_val(j.job_type),
                      status=_enum_val(j.status), at=j.created_at)
        for j in jobs
    ]
    # A request that was approved becomes a ScanJob (linked via scan_job_id); it is
    # already represented by that job row above, so listing it again would show the
    # same logical scan twice. Only surface requests that have NOT been dispatched
    # (pending / rejected) — the ones the customer still needs visibility into.
    out += [
        ClientScanOut(id=r.id, kind="request", scan_type=r.scan_type,
                      status=r.status, at=r.requested_at)
        for r in reqs
        if r.scan_job_id is None
    ]
    return out


@router.get("/use-cases",
            summary="Capability use-cases the customer may request (mirrors the operator catalog)")
async def portal_use_cases(user: ClientUser):
    assert_client(user)
    return [
        {"use_case_id": uid,
         "display_name": uc.get("display_name", uid),
         "status": uc.get("status", "available"),
         "description": uc.get("description", ""),
         "profile": uc.get("profile"),
         "intensity": uc.get("intensity"),
         "expected_runtime_hint": uc.get("expected_runtime_hint")}
        for uid, uc in _portal_use_cases().items()
    ]


@router.post("/scan-requests", response_model=ClientScanRequestOut,
             status_code=status.HTTP_201_CREATED,
             summary="Request a scan — an operator approves before it runs")
async def create_scan_request(body: ScanRequestCreate, user: ClientUser, db: DB):
    eng_id = assert_client(user)

    # Resolve against the capability catalog. Preferred: the customer picks a
    # use_case_id (GET /use-cases) → derive its scan_type and store the id so the
    # approved job runs exactly that use case. Legacy: a bare scan_type validated
    # against the ScanJobType enum. Either way the vocabulary can't drift.
    if body.use_case_id:
        uc = _portal_use_cases().get(body.use_case_id)
        if uc is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                f"Unknown use_case_id '{body.use_case_id}'")
        # Backend gate: a "coming soon" capability is disabled in the UI, but the
        # API must refuse it too so it can't be dispatched by a crafted request.
        if uc.get("status") == "coming_soon":
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                f"Use case '{body.use_case_id}' is coming soon and not yet available")
        scan_type = uc["scan_type"]
        use_case_id = body.use_case_id
    else:
        if body.scan_type not in _VALID_SCAN_TYPES:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                f"Unknown scan_type '{body.scan_type}'")
        scan_type = body.scan_type
        use_case_id = None

    eng = (await db.execute(
        select(Engagement).where(Engagement.id == eng_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")

    # Re-validate every requested target against the engagement scope server-side.
    # This is the request-time gate; the dispatch-time gate (agents.py) re-checks
    # the same way via the same shared helper, so the two can never disagree.
    normalized_targets: list[str] | None = None
    if body.targets:
        normalized_targets = validate_targets_in_scope(
            body.targets, eng.scope_cidrs, eng.excluded_cidrs)
        if normalized_targets is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "One or more targets are outside the engagement scope "
                "(or overlap an excluded range). Only in-scope IP/CIDR/range "
                "values are allowed.")

    # Requests queue for operator review; a small cap keeps the inbox sane.
    pending_count = (await db.execute(
        client_scoped(select(func.count()).select_from(ScanRequest),
                      user, ScanRequest.engagement_id)
        .where(ScanRequest.status == SR_PENDING)
    )).scalar_one()
    if pending_count >= _MAX_PENDING_REQUESTS:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"You already have {pending_count} scan requests awaiting review "
            f"(max {_MAX_PENDING_REQUESTS}). Please wait for your security team.")

    sr = ScanRequest(
        tenant_id=user.tenant_id, engagement_id=eng_id, requested_by=user.user_id,
        scan_type=scan_type, use_case_id=use_case_id, status=SR_PENDING, note=body.note,
        targets=normalized_targets, intensity=body.intensity,
    )
    db.add(sr)
    await db.flush()
    await db.refresh(sr)
    # Client actions are audited (customer-facing surface). Record targets +
    # intensity so an out-of-scope ATTEMPT is forensically visible even though it
    # was rejected before reaching here.
    record_audit(db, actor_id=user.user_id, action="scan_request.created",
                 engagement_id=eng_id, resource_type="scan_request", resource_id=sr.id,
                 detail={"scan_type": scan_type, "use_case_id": use_case_id,
                         "targets": normalized_targets, "intensity": body.intensity})
    await db.flush()
    return ClientScanRequestOut(id=sr.id, scan_type=sr.scan_type, use_case_id=sr.use_case_id,
                                status=sr.status, targets=sr.targets, intensity=sr.intensity,
                                note=sr.note, requested_at=sr.requested_at)
