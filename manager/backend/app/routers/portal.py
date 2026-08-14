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
from sqlalchemy import select

from app.auth.portal_scope import ClientUser, assert_client, client_scoped
from app.dependencies import DB
from app.models.engagement import Engagement
from app.models.enums import FindingSeverity, FindingStatus, ReviewStatus
from app.models.finding import Finding
from app.models.llm_output import LLMOutput
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
    ScanRequestCreate,
)
from app.services import posture as posture_service
from app.services.audit import record_audit

router = APIRouter(prefix="/portal", tags=["portal"])

_OPEN_STATES = (FindingStatus.open, FindingStatus.confirmed)


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


@router.get("/posture", response_model=ClientPostureOut,
            summary="Posture scorecard for the customer's engagement")
async def portal_posture(user: ClientUser, db: DB):
    rows = (await db.execute(
        client_scoped(select(Finding), user, Finding.engagement_id)
        .where(Finding.status.in_(_OPEN_STATES))
    )).scalars().all()
    views = [
        posture_service.FindingView(
            id=str(f.id), severity=_enum_val(f.severity),
            risk_score=float(f.risk_score) if f.risk_score is not None else None,
            epss_score=float(f.epss_score) if f.epss_score is not None else None,
            exploitable=bool(f.exploitable), exploit_validated=bool(f.exploit_validated),
            asset_criticality=None, first_seen=f.first_seen, last_seen=f.last_seen,
        )
        for f in rows
    ]
    s = posture_service.compute_scores(views)
    return ClientPostureOut(
        risk_index=s.risk_index, exploitable_score=s.exploitable_score,
        posture_score=s.posture_score, grade=s.grade, open_findings=len(views),
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
    out += [
        ClientScanOut(id=r.id, kind="request", scan_type=r.scan_type,
                      status=r.status, at=r.requested_at)
        for r in reqs
    ]
    return out


@router.post("/scan-requests", response_model=ClientScanRequestOut,
             status_code=status.HTTP_201_CREATED,
             summary="Request a scan — an operator approves before it runs")
async def create_scan_request(body: ScanRequestCreate, user: ClientUser, db: DB):
    eng_id = assert_client(user)
    # Dedupe / cooldown: at most one PENDING request per engagement, so a customer
    # cannot flood the operator inbox. A prior approved/rejected request never blocks.
    pending = (await db.execute(
        client_scoped(select(ScanRequest), user, ScanRequest.engagement_id)
        .where(ScanRequest.status == SR_PENDING).limit(1)
    )).scalars().first()
    if pending is not None:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "A scan request is already pending for this engagement")
    sr = ScanRequest(
        tenant_id=user.tenant_id, engagement_id=eng_id, requested_by=user.user_id,
        scan_type=body.scan_type, status=SR_PENDING, note=body.note,
    )
    db.add(sr)
    await db.flush()
    await db.refresh(sr)
    # Client actions are audited (customer-facing surface).
    record_audit(db, actor_id=user.user_id, action="scan_request.created",
                 engagement_id=eng_id, resource_type="scan_request", resource_id=sr.id,
                 detail={"scan_type": body.scan_type})
    await db.flush()
    return ClientScanRequestOut(id=sr.id, scan_type=sr.scan_type, status=sr.status,
                                note=sr.note, requested_at=sr.requested_at)
