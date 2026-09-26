"""
portal.py — the CUSTOMER-facing engagement API (Part 2, Phase 2). Every route is scoped
to the client's one bound engagement via `client_scoped` / `assert_client` (the
Phase-0 choke point), so a route physically cannot return another engagement's
data. Customers can perform finding lifecycle actions and submit scoped scan
requests and update their assigned engagement; every write is pinned to the
engagement in the authenticated portal session, so they cannot select or access
another engagement.

Data-exposure controls:
  * legacy summary findings use ClientFindingOut; the authenticated workspace
    uses the manager FindingOut contract so both surfaces share one workflow
  * reports are gated to review_status == approved (drafts/internal never leak)
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated, Literal

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select

from app.auth.portal_scope import ClientUser, assert_client, client_scoped
from app.dependencies import DB, RedisConn
from app.models.agent import Agent, AgentStatus
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import (
    DetectionStatus, FindingSeverity, FindingStatus, ReviewStatus, ScanJobStatus, ScanJobType,
)
from app.models.finding import Finding
from app.models.llm_output import LLMOutput
from app.models.probe_enrollment import ProbeEnrollmentRequest
from app.models.probe_site import ProbeSite
from app.models.remediation_plan import RemediationPlan
from app.models.scan_job import ScanJob
from app.models.scan_request import ScanRequest, SR_PENDING
from app.schemas.ai import AiGenerateRequest, AiMessage
from app.schemas.common import PaginatedResponse
from app.schemas.finding import FindingEventOut, FindingOut, FindingPatch, FindingReopen, FindingTimeline
from app.schemas.portal import (
    ClientAssistantAsk,
    ClientAssistantReply,
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
from app.services import finding_events, finding_workflow, portal_metrics
from app.services.domain_context import domain_brief_for
from app.services.llm import AiRuntimeError, ManagerLlmService
from app.services import posture as posture_service
from app.services.audit import record_audit
from app.remediation.loader import load_finding_context
from app.remediation.plan import build_plan, os_for_context
from app.services.remediation_kb import os_key
from app.services.scope_targets import validate_targets_in_scope
from app.routers.agents import EnqueueJobRequest

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


class PortalEnrollmentApprove(BaseModel):
    """Bind a device-code enrollment to the session's engagement.

    The browser supplies only the short-lived verification code and an optional
    display name. Tenant, Site policy, authorized CIDRs and the final engagement
    assignment are all derived server-side.
    """

    user_code: str = Field(min_length=8, max_length=9, pattern=r"^[A-Za-z0-9]{4}-?[A-Za-z0-9]{4}$")
    probe_name: str | None = Field(default=None, min_length=1, max_length=255)


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


@router.get("/findings/{finding_id}/events", response_model=FindingTimeline,
            summary="Finding lifecycle timeline for the assigned engagement")
async def portal_finding_timeline(finding_id: uuid.UUID, user: ClientUser, db: DB):
    finding = await finding_workflow.get_finding_for_action(
        db,
        finding_id,
        tenant_id=user.tenant_id,
        engagement_id=assert_client(user),
    )
    timeline = await finding_events.build_timeline(db, finding)
    return FindingTimeline(
        finding_id=finding.id,
        events=[FindingEventOut(**event) for event in timeline],
    )


@router.patch("/findings/{finding_id}", response_model=FindingOut,
              summary="Apply the shared finding workflow in the assigned engagement")
async def patch_portal_finding(
    finding_id: uuid.UUID,
    body: FindingPatch,
    user: ClientUser,
    db: DB,
):
    finding = await finding_workflow.get_finding_for_action(
        db,
        finding_id,
        tenant_id=user.tenant_id,
        engagement_id=assert_client(user),
    )
    return await finding_workflow.patch_finding(
        db,
        finding,
        body,
        actor_id=user.user_id,
        actor_type="customer",
        origin="portal",
    )


@router.post("/findings/{finding_id}/reopen", response_model=FindingOut,
             summary="Reopen a remediated finding in the assigned engagement")
async def reopen_portal_finding(
    finding_id: uuid.UUID,
    user: ClientUser,
    db: DB,
    body: FindingReopen | None = None,
):
    finding = await finding_workflow.get_finding_for_action(
        db,
        finding_id,
        tenant_id=user.tenant_id,
        engagement_id=assert_client(user),
    )
    return await finding_workflow.reopen_finding(
        db,
        finding,
        actor_id=user.user_id,
        actor_type="customer",
        origin="portal",
        reason=body.reason if body is not None else None,
    )


@router.get("/findings/{finding_id}/remediation",
            summary="Structured remediation plan (KB always; AI only once reviewed)")
async def portal_finding_remediation(
    finding_id: uuid.UUID, user: ClientUser, db: DB,
    os: str | None = Query(default=None),
):
    """Customer-facing structured remediation, replacing the plain `remediation`
    string. The contextual KB plan is served ALWAYS; a stored AI plan reaches the
    customer only once an operator has reviewed it — the same approval gate the
    reports route uses, so an unreviewed AI plan never leaks."""
    finding = (await db.execute(
        client_scoped(select(Finding).where(Finding.id == finding_id),
                      user, Finding.engagement_id)
    )).scalar_one_or_none()
    if finding is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")

    ctx = await load_finding_context(db, finding)
    key = os_key(os) if os else os_for_context(ctx)
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
        plan = build_plan(finding, ctx, os=key)
        source = plan["source"]
    return {"finding_id": str(finding_id), "os": key, "source": source, "plan": plan}


def _posture_select():
    """Findings joined to the criticality of the asset underneath them.

    OUTER join, matching analytics.load_posture_views: a finding with no asset
    keeps a null criticality and posture.py treats that as the neutral 0.5,
    rather than being dropped from the score entirely.
    """
    return (
        select(Finding, Asset.criticality.label("asset_criticality"))
        .outerjoin(Asset, Finding.asset_id == Asset.id)
    )


@router.get("/posture", response_model=ClientPostureOut,
            summary="Posture scorecard for the customer's engagement")
async def portal_posture(user: ClientUser, db: DB):
    rows = (await db.execute(
        client_scoped(_posture_select(), user, Finding.engagement_id)
        .where(Finding.status.in_(_OPEN_STATES))
    )).all()
    views = [_posture_view(f, crit) for f, crit in rows]
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


def _posture_view(f: Finding, asset_criticality=None) -> posture_service.FindingView:
    """Map a joined (Finding, Asset.criticality) row to a scoring view.

    `asset_criticality` MUST come from the join — it used to be hard-coded None
    here, which made posture's _CRIT_WEIGHT fall back to the neutral 0.5 for
    every asset. The operator's /analytics/posture joins the real column, so the
    SAME engagement scored differently depending on which console you looked at,
    and the customer had no way to know theirs was the approximation. A posture
    grade the two parties can't both quote is worse than no grade.
    """
    return posture_service.FindingView(
        id=str(f.id), severity=_enum_val(f.severity),
        risk_score=float(f.risk_score) if f.risk_score is not None else None,
        epss_score=float(f.epss_score) if f.epss_score is not None else None,
        exploitable=bool(f.exploitable), exploit_validated=bool(f.exploit_validated),
        asset_criticality=(
            _enum_val(asset_criticality) if asset_criticality is not None else None
        ),
        first_seen=f.first_seen, last_seen=f.last_seen,
        status=_enum_val(f.status),
    )


@router.get("/summary", response_model=ClientSummaryOut,
            summary="Dashboard summary: posture + KPI counts + queue state")
async def portal_summary(user: ClientUser, db: DB):
    rows = (await db.execute(
        client_scoped(_posture_select(), user, Finding.engagement_id)
    )).all()
    open_views = [_posture_view(f, crit) for f, crit in rows
                  if f.status in _OPEN_STATES]
    s = posture_service.compute_scores(open_views)
    metrics = [_metric_finding(f) for f, _ in rows]
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


# ── AI assistant ──────────────────────────────────────────────────────────────
# A customer-facing assistant, scoped two ways at once:
#
#   DATA scope   — the grounding context is built HERE, server-side, from this
#                  client's own engagement via client_scoped(). The request body
#                  carries no context, so a crafted client cannot ask about
#                  another tenant's findings or smuggle its own "facts" in.
#   SUBJECT scope — the model runs the `client_assistant` task, whose rules
#                  restrict it to information security and decline anything else.
#
# Unlike the reports and remediation routes, replies are NOT operator-reviewed:
# this was an explicit product decision, so the UI labels every answer as
# AI-generated and unverified rather than presenting it as assessed fact.
_ASSISTANT_MAX_FINDINGS = 40


def _assistant_finding_view(f: Finding) -> dict:
    """The whitelist that reaches the model — deliberately the same shape the
    customer can already see in ClientFindingOut. No internal triage notes,
    evidence blobs or exploit metadata."""
    return {
        "id": str(f.id),
        "title": f.title,
        "severity": getattr(f.severity, "value", f.severity),
        "status": getattr(f.status, "value", f.status),
        "cvss_score": float(f.cvss_score) if f.cvss_score is not None else None,
        "risk_score": f.risk_score,
        "cve_ids": f.cve_ids,
        "first_seen": f.first_seen.isoformat() if f.first_seen else None,
        "remediation": f.remediation,
    }


@router.post("/assistant/chat", response_model=ClientAssistantReply,
             summary="Ask about your own assessment (security topics only)")
async def portal_assistant_chat(body: ClientAssistantAsk, user: ClientUser, db: DB):
    eng_id = assert_client(user)

    eng = (await db.execute(
        select(Engagement).where(Engagement.id == eng_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")

    open_rows = (await db.execute(
        client_scoped(
            select(Finding)
            .where(Finding.status.in_(_OPEN_STATES))
            .order_by(Finding.risk_score.desc().nullslast(), Finding.severity)
            .limit(_ASSISTANT_MAX_FINDINGS),
            user, Finding.engagement_id)
    )).scalars().all()

    focus = None
    focus_row = None
    if body.finding_id is not None:
        row = (await db.execute(
            client_scoped(select(Finding).where(Finding.id == body.finding_id),
                          user, Finding.engagement_id)
        )).scalar_one_or_none()
        if row is None:
            # 404 rather than 403: a client must not be able to probe whether a
            # finding id exists in someone else's engagement.
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")
        focus = _assistant_finding_view(row)
        focus_row = row

    context = {
        "engagement": {
            "name": eng.name,
            "status": getattr(eng.status, "value", eng.status),
            "authorised_scope": list(eng.scope_cidrs or []),
        },
        "open_finding_count": len(open_rows),
        "open_findings": [_assistant_finding_view(f) for f in open_rows],
    }
    if focus is not None:
        context["question_is_about"] = focus

    request = AiGenerateRequest(
        task="client_assistant",
        messages=[AiMessage(role=m.role, content=m.content) for m in body.messages],
        context=context,
        # Adaptive-depth answers: simple questions stay short, but a full
        # structured finding brief (impact / what-we-found / what-to-do / verify)
        # needs headroom so it is never truncated mid-remediation. Ceiling only —
        # short answers still cost only what they generate.
        max_tokens=1600,
        provider=body.provider,
        model=body.model,
    )
    # Sector/jurisdiction expertise, built server-side from trusted data only.
    # A focused finding shapes which control themes the brief carries.
    brief = await domain_brief_for(db, eng, [focus_row] if focus_row is not None else open_rows)
    llm = ManagerLlmService()
    try:
        content, runtime, _fallback = await llm.generate_with_fallback(
            request, domain_brief=brief.text if brief else None)
    except AiRuntimeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    from app.ai.audit_chain import persist_ai_calls
    await persist_ai_calls(db, list(getattr(llm, "audit_records", None) or []),
                           actor_id=user.user_id, engagement_id=eng_id)

    from app.compliance.citations import check_citations
    unverified = check_citations(content)["unverified"]
    record_audit(
        db, actor_id=user.user_id, action="portal.assistant.chat",
        engagement_id=eng_id, resource_type="engagement", resource_id=eng_id,
        detail={"turns": len(body.messages), "finding_id": str(body.finding_id)
                if body.finding_id else None, "model": runtime.model,
                "skill": brief.skill_id if brief else None,
                "unverified_citations": unverified},
    )
    await db.flush()
    return ClientAssistantReply(
        content=content, provider=runtime.provider, model=runtime.model,
        grounded=bool(open_rows or focus),
        skill=brief.skill_id if brief else None,
        skill_label=brief.skill_label if brief else None,
        jurisdictions=brief.jurisdictions if brief else [],
        unverified_citations=unverified,
        generated_at=datetime.now(timezone.utc),
    )


@router.get("/workspace/ai/status", summary="Manager AI runtime options")
async def portal_workspace_ai_status(user: ClientUser):
    """Expose the same non-secret runtime catalog used by the manager UI."""
    assert_client(user)
    from app.routers.ai import ai_status
    return await ai_status(current_user=user)


@router.get(
    "/workspace/findings",
    response_model=PaginatedResponse[FindingOut],
    summary="Manager-parity finding queue for the assigned engagement",
)
async def portal_workspace_findings(
    user: ClientUser,
    db: DB,
    severity: FindingSeverity | None = Query(default=None),
    status_filter: FindingStatus | None = Query(default=None, alias="status"),
    active_only: bool = Query(default=False),
    asset_id: uuid.UUID | None = Query(default=None),
    asset_ip: str | None = Query(default=None, min_length=1, max_length=45),
    agent_id: uuid.UUID | None = Query(default=None),
    mitre_technique: str | None = Query(default=None),
    scan: str | None = Query(default=None, min_length=1, max_length=64),
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
    from app.routers.findings import list_findings as operator_findings
    return await operator_findings(
        db=db,
        current_user=user,
        severity=severity,
        status_filter=status_filter,
        active_only=active_only,
        asset_id=asset_id,
        asset_ip=asset_ip,
        mitre_technique=mitre_technique,
        engagement_id=assert_client(user),
        agent_id=agent_id,
        scan=scan,
        search=search,
        detection_status=detection_status,
        exploit_validated=exploit_validated,
        verification_state=verification_state,
        needs_review=needs_review,
        sla_breached=sla_breached,
        sort=sort,
        page=page,
        page_size=page_size,
    )


@router.get("/workspace/findings/assets",
            summary="Affected assets (IP filter options) for the assigned engagement")
async def portal_workspace_finding_assets(
    user: ClientUser,
    db: DB,
    active_only: bool = Query(default=False),
):
    from app.routers.findings import finding_assets as operator_finding_assets
    return await operator_finding_assets(
        db=db, current_user=user, engagement_id=assert_client(user), active_only=active_only,
    )


@router.get("/workspace/findings/summary", summary="Manager-parity finding summary for the assigned engagement")
async def portal_workspace_finding_summary(
    user: ClientUser,
    db: DB,
    agent_id: uuid.UUID | None = Query(default=None),
):
    from app.routers.findings import finding_summary as operator_summary
    return await operator_summary(
        db=db,
        current_user=user,
        engagement_id=assert_client(user),
        agent_id=agent_id,
    )


@router.get("/workspace/findings/scans",
            summary="Scans that produced findings in the assigned engagement")
async def portal_workspace_finding_scans(user: ClientUser, db: DB):
    from app.routers.findings import finding_scans as operator_finding_scans
    return await operator_finding_scans(
        db=db, current_user=user, engagement_id=assert_client(user))


@router.get("/workspace/findings/compare",
            summary="Diff two scans (new / fixed / still present) in the assigned engagement")
async def portal_workspace_finding_compare(
    user: ClientUser,
    db: DB,
    a: str = Query(..., min_length=1, max_length=64),
    b: str = Query(..., min_length=1, max_length=64),
):
    # Pinned to the client's own engagement — the operator handler scopes both scan
    # resolution and the finding load to it, so a sibling engagement in the same
    # tenant is unreachable.
    from app.routers.findings import compare_scans as operator_compare
    return await operator_compare(
        db=db, current_user=user, a=a, b=b, engagement_id=assert_client(user))


@router.get("/workspace/findings/{finding_id}", response_model=FindingOut,
            summary="Manager-parity finding detail for the assigned engagement")
async def portal_workspace_finding_detail(finding_id: uuid.UUID, user: ClientUser, db: DB):
    finding = await finding_workflow.get_finding_for_action(
        db,
        finding_id,
        tenant_id=user.tenant_id,
        engagement_id=assert_client(user),
    )
    from app.routers.findings import _finding_detail_out
    return await _finding_detail_out(db, finding)


@router.get("/workspace/findings/{finding_id}/obligations",
            summary="Regional obligations for a finding in the assigned engagement")
async def portal_finding_obligations(finding_id: uuid.UUID, user: ClientUser, db: DB):
    from app.services.compliance_brief import finding_compliance_view
    finding, eng = await _portal_finding_and_engagement(db, finding_id, user)
    return await finding_compliance_view(db, finding, eng)


@router.post("/workspace/findings/{finding_id}/compliance-brief",
             summary="Sector-expert compliance impact brief (AI-generated, unverified)")
async def portal_finding_compliance_brief(finding_id: uuid.UUID, user: ClientUser, db: DB):
    from app.services.compliance_brief import generate_compliance_brief
    finding, eng = await _portal_finding_and_engagement(db, finding_id, user)
    out = await generate_compliance_brief(db, finding, eng, actor_id=user.user_id)
    record_audit(db, actor_id=user.user_id, action="portal.finding.compliance_brief",
                 engagement_id=eng.id, resource_type="finding", resource_id=finding.id,
                 detail={"skill": out["skill"], "generated": out["content"] is not None})
    await db.flush()
    return out


async def _portal_finding_and_engagement(db, finding_id: uuid.UUID, user):
    """Pinned to the client's own engagement; another engagement's id is a 404."""
    finding = await finding_workflow.get_finding_for_action(
        db, finding_id, tenant_id=user.tenant_id, engagement_id=assert_client(user))
    eng = (await db.execute(select(Engagement).where(Engagement.id == finding.engagement_id))).scalar_one()
    return finding, eng


@router.get("/workspace/engagement",
            summary="Manager-parity engagement detail for the assigned engagement")
async def portal_workspace_engagement(user: ClientUser, db: DB):
    """Return the canonical engagement-detail contract, pinned by the session.

    The customer never supplies an engagement id. Reusing the operator handler
    keeps counts and future contract changes identical on both dashboards while
    the server-side binding remains the authorization boundary.
    """
    from app.routers.engagements import get_engagement as operator_engagement
    return await operator_engagement(
        engagement_id=assert_client(user),
        db=db,
        current_user=user,
    )


@router.patch("/workspace/engagement", summary="Update the assigned engagement")
async def portal_workspace_update_engagement(body: dict, user: ClientUser, db: DB):
    """Use the manager's canonical update workflow with session-pinned identity."""
    from app.routers.engagements import EngagementUpdate, update_engagement
    parsed = EngagementUpdate.model_validate(body)
    updated = await update_engagement(
        engagement_id=assert_client(user), body=parsed, db=db, current_user=user,
    )
    record_audit(
        db, actor_id=user.user_id, action="portal.engagement.updated",
        engagement_id=assert_client(user), resource_type="engagement",
        resource_id=assert_client(user), detail={"origin": "portal", "fields": sorted(body)},
    )
    await db.flush()
    return updated


@router.get("/workspace/engagement/assets", summary="Assets in the assigned engagement")
async def portal_workspace_engagement_assets(user: ClientUser, db: DB):
    from app.routers.engagements import list_engagement_assets
    return await list_engagement_assets(
        engagement_id=assert_client(user), db=db, current_user=user,
    )


@router.get("/workspace/compliance", summary="Regulatory profile, applicable frameworks and reporting clocks")
async def portal_workspace_compliance(user: ClientUser, db: DB):
    """Read-only for the customer: the operator sets the profile."""
    from app.routers.compliance import engagement_compliance
    return await engagement_compliance(engagement_id=assert_client(user), db=db, current_user=user)


@router.post("/workspace/engagement/import-facts", status_code=status.HTTP_202_ACCEPTED,
             summary="Import evidence into the assigned engagement")
async def portal_workspace_import_facts(
    user: ClientUser,
    db: DB,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    from app.routers.engagements import import_facts
    result = await import_facts(
        engagement_id=assert_client(user), db=db, current_user=user,
        background_tasks=background_tasks, file=file,
    )
    record_audit(
        db, actor_id=user.user_id, action="portal.engagement.evidence_imported",
        engagement_id=assert_client(user), resource_type="engagement",
        resource_id=assert_client(user), detail={"origin": "portal", "file": file.filename},
    )
    await db.flush()
    return result


# ── scanner parity: canonical jobs, session-pinned engagement and probe ──────

@router.get("/workspace/scan/use-cases",
            summary="Manager scanner capability catalog")
async def portal_workspace_scan_use_cases(user: ClientUser):
    assert_client(user)
    from app.routers.agents import list_use_cases
    return await list_use_cases(current_user=user)


@router.get("/workspace/scan/jobs",
            summary="Manager-parity jobs for the assigned engagement")
async def portal_workspace_scan_jobs(user: ClientUser, db: DB):
    from app.routers.engagements import list_engagement_jobs
    return await list_engagement_jobs(
        engagement_id=assert_client(user), db=db, current_user=user,
    )


@router.get("/workspace/scan/jobs/{job_id}",
            summary="Manager-parity job status in the assigned engagement")
async def portal_workspace_scan_job(job_id: uuid.UUID, user: ClientUser, db: DB):
    row = (await db.execute(select(ScanJob.id).where(
        ScanJob.id == job_id,
        ScanJob.engagement_id == assert_client(user),
    ))).scalar_one_or_none()
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    from app.routers.agents import get_job_status
    return await get_job_status(job_id=job_id, db=db, current_user=user)


@router.post("/workspace/scan/jobs", status_code=status.HTTP_201_CREATED,
             summary="Launch a scan in the assigned engagement")
async def portal_workspace_scan_launch(
    body: EnqueueJobRequest,
    user: ClientUser,
    db: DB,
    redis: RedisConn,
):
    eng_id = assert_client(user)
    eng = (await db.execute(select(Engagement).where(
        Engagement.id == eng_id,
        Engagement.tenant_id == user.tenant_id,
    ))).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    if eng.assigned_agent_id is None:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "No vedha-agent is assigned to this engagement")

    params = dict(body.params)
    requested_agent = params.get("preferred_agent_id")
    if requested_agent and str(requested_agent) != str(eng.assigned_agent_id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "The selected vedha-agent is not assigned to this engagement")
    # A crafted client cannot route work to another tenant probe. The session's
    # engagement binding is authoritative for both fields.
    params["preferred_agent_id"] = str(eng.assigned_agent_id)
    pinned = body.model_copy(update={"engagement_id": eng_id, "params": params})

    from app.routers.agents import enqueue_agent_job
    result = await enqueue_agent_job(
        body=pinned, db=db, redis=redis, current_user=user,
    )
    record_audit(
        db, actor_id=user.user_id, action="scan_job.created",
        engagement_id=eng_id, resource_type="scan_job",
        resource_id=uuid.UUID(result["job_id"]),
        detail={"origin": "portal", "use_case_id": body.use_case_id},
    )
    await db.flush()
    return result


async def _assert_portal_job(job_id: uuid.UUID, user: ClientUser, db: DB) -> None:
    exists = (await db.execute(select(ScanJob.id).where(
        ScanJob.id == job_id,
        ScanJob.engagement_id == assert_client(user),
    ))).scalar_one_or_none()
    if exists is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")


@router.post("/workspace/scan/jobs/{job_id}/cancel",
             summary="Cancel an assigned-engagement scan job")
async def portal_workspace_scan_cancel(job_id: uuid.UUID, user: ClientUser, db: DB):
    await _assert_portal_job(job_id, user, db)
    from app.routers.agents import cancel_agent_job
    result = await cancel_agent_job(job_id=job_id, db=db, current_user=user)
    record_audit(
        db, actor_id=user.user_id, action="scan_job.cancelled",
        engagement_id=assert_client(user), resource_type="scan_job",
        resource_id=job_id, detail={"origin": "portal"},
    )
    await db.flush()
    return result


@router.get("/workspace/scan/campaign-progress",
            summary="VA campaign progress for the assigned engagement")
async def portal_workspace_campaign_progress(user: ClientUser, db: DB):
    from app.routers.engagements import campaign_progress
    return await campaign_progress(
        engagement_id=assert_client(user), db=db, current_user=user,
    )


@router.get("/workspace/scan/raw-facts",
            summary="Raw scanner facts for the assigned engagement")
async def portal_workspace_raw_facts(
    user: ClientUser,
    db: DB,
    job_id: uuid.UUID | None = None,
    scanner: str | None = None,
    limit: int = 5,
    max_facts: int = 2000,
):
    from app.routers.engagements import raw_facts
    return await raw_facts(
        engagement_id=assert_client(user), db=db, current_user=user,
        job_id=job_id, scanner=scanner, limit=limit, max_facts=max_facts,
    )


@router.get("/workspace/fleet/jobs",
            summary="Manager Fleet job feed for the assigned engagement")
async def portal_workspace_fleet_jobs(
    user: ClientUser,
    db: DB,
    agent_id: uuid.UUID | None = None,
    status_filter: ScanJobStatus | None = Query(default=None, alias="status"),
    running: bool = False,
    limit: int = 100,
):
    eng_id = assert_client(user)
    eng = (await db.execute(select(Engagement).where(
        Engagement.id == eng_id,
        Engagement.tenant_id == user.tenant_id,
    ))).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    if agent_id is not None and str(agent_id) != str(eng.assigned_agent_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "vedha-agent not found")
    from app.routers.agents import list_all_jobs
    return await list_all_jobs(
        db=db, current_user=user, agent_id=agent_id,
        engagement_id=eng_id, status=status_filter,
        running=running, limit=limit,
    )


@router.post("/workspace/fleet/enrollment/approve",
             summary="Approve and bind a vedha-agent to the assigned engagement")
async def portal_workspace_fleet_approve(
    body: PortalEnrollmentApprove,
    user: ClientUser,
    db: DB,
):
    """Complete device-code enrollment without trusting browser scope fields.

    Possession of the short-lived installer code identifies the pending device.
    The Site policy comes from the authenticated engagement, so a crafted portal
    request cannot widen scope, select another tenant, or bind a different job.
    """
    from app.routers.probe_enrollment import (
        _keyed_hash,
        _next_probe_name,
        _provision_agent_for_site,
    )

    engagement_id = assert_client(user)
    engagement = (await db.execute(
        select(Engagement).where(
            Engagement.id == engagement_id,
            Engagement.tenant_id == user.tenant_id,
        ).with_for_update()
    )).scalar_one_or_none()
    if engagement is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    if engagement.assigned_agent_id is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "This engagement already has an assigned vedha-agent",
        )

    code = body.user_code.replace("-", "").upper()
    request_row = (await db.execute(
        select(ProbeEnrollmentRequest)
        .where(ProbeEnrollmentRequest.user_code_hash == _keyed_hash(code))
        .with_for_update()
    )).scalar_one_or_none()
    now = datetime.now(timezone.utc)
    if request_row is None or (
        request_row.tenant_id is not None and request_row.tenant_id != user.tenant_id
    ):
        # 404 avoids disclosing whether a code belongs to another tenant.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Enrollment code not found")
    if request_row.expires_at <= now:
        request_row.state = "expired"
        raise HTTPException(status.HTTP_410_GONE, "Enrollment code expired; restart the installer")
    if request_row.state != "awaiting_approval":
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Enrollment request is already {request_row.state}",
        )

    authorized_cidrs = list(engagement.scope_cidrs or [])
    if not authorized_cidrs:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Add an authorized engagement scope before enrolling a vedha-agent",
        )
    capabilities = list(dict.fromkeys(request_row.reported_capabilities or []))
    if not capabilities:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "The vedha-agent did not report any supported capabilities",
        )

    probe_name = (body.probe_name or "").strip()
    if not probe_name:
        probe_name = await _next_probe_name(db, user.tenant_id)
    site = ProbeSite(
        tenant_id=user.tenant_id,
        name=f"engagement-{str(engagement_id)[:8]}-{str(request_row.id)[:8]}",
        status="active",
        authorized_cidrs=authorized_cidrs,
        excluded_cidrs=list(engagement.excluded_cidrs or []),
        approved_capabilities=capabilities,
    )
    db.add(site)
    await db.flush()

    agent = await _provision_agent_for_site(
        db,
        row=request_row,
        site=site,
        tenant_id=user.tenant_id,
        probe_name=probe_name,
        location=None,
        approved_by=str(user.user_id),
        now=now,
        auto=False,
    )
    engagement.assigned_agent_id = agent.id
    record_audit(
        db,
        actor_id=user.user_id,
        action="portal.agent.assigned",
        engagement_id=engagement_id,
        resource_type="agent",
        resource_id=agent.id,
        detail={"origin": "portal", "site_id": str(site.id)},
    )
    await db.flush()
    return {
        "request_id": str(request_row.id),
        "agent_id": str(agent.id),
        "site_id": str(site.id),
        "state": request_row.state,
        "probe_name": probe_name,
    }


@router.get("/workspace/fleet/agents/{agent_id}/jobs",
            summary="Assigned vedha-agent job history in this engagement")
async def portal_workspace_fleet_agent_jobs(
    agent_id: uuid.UUID,
    user: ClientUser,
    db: DB,
    limit: int = 25,
):
    eng_id = assert_client(user)
    eng = (await db.execute(select(Engagement).where(
        Engagement.id == eng_id,
        Engagement.tenant_id == user.tenant_id,
        Engagement.assigned_agent_id == agent_id,
    ))).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "vedha-agent not found")
    from app.routers.agents import get_agent_job_history
    return await get_agent_job_history(
        agent_id=agent_id, db=db, current_user=user, limit=limit,
        engagement_id=eng_id,
    )


# ── console parity: the same analytics the operator dashboard renders ─────────
# The customer console shows the SAME components as the operator console
# (components/dashboard/*), so it needs the SAME response shapes. Rather than
# fork the aggregation — which would drift the moment either side changed — these
# routes DELEGATE to the operator handlers with `engagement_id` pinned to the
# caller's own engagement.
#
# Those handlers already take an optional engagement_id and filter on it, and
# they scope every query by `current_user.tenant_id` on top. A client token
# carries the client's tenant, so the delegation is scoped twice: by tenant
# inside the handler, and by the engagement we pin here. `assert_client` refuses
# any caller that is not a bound client before we get that far.
#
# The win is structural: a change to the operator's exposure/posture/SLA
# aggregation reaches the customer console automatically, because it is the same
# function.

@router.get("/analytics/exposure", summary="Protocol risk + zone health for your engagement")
async def portal_exposure(user: ClientUser, db: DB):
    from app.routers.analytics import exposure as _operator_exposure
    return await _operator_exposure(db=db, current_user=user,
                                    engagement_id=assert_client(user))


@router.get("/analytics/posture", summary="Posture scores + patch comparison for your engagement")
async def portal_posture_analytics(user: ClientUser, db: DB):
    from app.routers.analytics import posture as _operator_posture
    return await _operator_posture(db=db, current_user=user,
                                   engagement_id=assert_client(user))


@router.get("/sla-summary", summary="Remediation-deadline summary for your engagement")
async def portal_sla_summary(user: ClientUser, db: DB):
    from app.routers.findings import sla_summary as _operator_sla
    return await _operator_sla(db=db, current_user=user,
                               engagement_id=assert_client(user))


@router.get("/activity", summary="Recent activity in your engagement")
async def portal_activity(user: ClientUser, db: DB,
                          limit: int = Query(default=20, ge=1, le=100)):
    from app.routers.activity import recent_activity as _operator_activity
    return await _operator_activity(db=db, current_user=user, limit=limit,
                                    engagement_id=assert_client(user))


@router.get("/agents", summary="The probe(s) assigned to your engagement")
async def portal_agents(user: ClientUser, db: DB):
    """The customer's own probe fleet — normally one. Deliberately a NARROW
    projection: a customer sees whether their probe is reachable and what it is
    doing, never enrollment secrets, tokens, hardware identifiers or the other
    tenants an operator would see on /fleet."""
    eng_id = assert_client(user)
    eng = (await db.execute(
        select(Engagement).where(Engagement.id == eng_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")

    agent_id = getattr(eng, "assigned_agent_id", None)
    if agent_id is None:
        return []

    agent = (await db.execute(
        select(Agent).where(Agent.id == agent_id, Agent.tenant_id == user.tenant_id)
    )).scalar_one_or_none()
    if agent is None:
        return []

    persisted_status = str(getattr(agent.status, "value", agent.status))
    now = datetime.now(timezone.utc)
    online = bool(
        agent.last_heartbeat
        and (now - agent.last_heartbeat).total_seconds() < 90
        and persisted_status in {AgentStatus.online.value, AgentStatus.busy.value}
    )
    # `status` MUST be derived from `online`, not from the persisted column.
    # A probe that dies without a clean WebSocket disconnect leaves status="online"
    # in the database with a stale heartbeat; the operator fleet view already
    # ignores that (routers/agents.py), so returning the raw column here told the
    # CUSTOMER their probe was connected while the operator saw it offline. The
    # customer would believe they were being scanned when they were not.
    if not online:
        status_value = "OFFLINE"
    elif persisted_status == AgentStatus.busy.value or agent.current_job_id is not None:
        status_value = "BUSY"
    else:
        status_value = "ONLINE"
    # `activity` is the one-line state the shared AgentMonitor panel renders. The
    # operator fleet view derives it the same way; a customer sees only whether
    # their own probe is working, never which job or whose.
    if status_value == "BUSY":
        activity = "Running a scan"
    elif status_value == "ONLINE":
        activity = "Idle — ready to scan"
    else:
        activity = "Not connected"
    return [{
        "id": str(agent.id),
        "name": agent.name,
        "status": status_value,
        "activity": activity,
        "location": agent.location,
        "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
        "capabilities": list(agent.capabilities or []),
        "network_segments": list(agent.network_segments or []),
        "current_job_id": str(agent.current_job_id) if agent.current_job_id else None,
        "online": online,
    }]
