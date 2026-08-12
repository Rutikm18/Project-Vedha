"""
Approval-gated safe active-validation API (P3).

POST /engagements/{id}/findings/{finding_id}/validate   — request a safe live re-check
GET  /engagements/{id}/validation-requests              — list requests (pending by default)
POST /validation-requests/{id}/approve                  — approve → enqueue a scoped validate job
POST /validation-requests/{id}/reject                   — reject

A ValidationRequest is the approval-gated record. On approval a single-target
``vuln_scan`` job with ``result.mode == "validate"`` is enqueued to the probe
(job parameters live in ``scan_jobs.result`` while pending — see agents.py).
Only NON-destructive checks are ever emitted (tls_handshake / banner_regrab /
safe_poc); OT engagements and RoE that forbids active validation are refused
before any job is enqueued. Interpretation of the returned result lives in
``app.detection.active_validation`` (pure) and the result-ingestion path.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.models.enums import ScanJobStatus, ScanJobType
from app.models.finding import Finding
from app.models.scan_job import ScanJob
from app.models.validation_request import (
    CHECK_BANNER,
    CHECK_SAFE_POC,
    CHECK_TLS,
    VR_APPROVED,
    VR_PENDING,
    VR_REJECTED,
    ValidationRequest,
)

router = APIRouter(tags=["validation"])
logger = structlog.get_logger()

_SAFE_CHECKS = {CHECK_TLS, CHECK_BANNER, CHECK_SAFE_POC}


# ── Schemas ───────────────────────────────────────────────────────────────────

class ValidateRequest(BaseModel):
    target_ip: str
    target_port: int | None = None
    check_kind: str | None = None  # defaults from the finding's evidence


class RejectBody(BaseModel):
    reason: str | None = None


class ValidationRequestOut(BaseModel):
    id: uuid.UUID
    engagement_id: uuid.UUID
    finding_id: uuid.UUID | None
    target_ip: str
    target_port: int | None
    check_kind: str
    status: str
    outcome: str | None
    job_id: uuid.UUID | None
    requested_by: str | None
    requested_at: datetime
    reviewed_by: str | None
    reviewed_at: datetime | None


# ── helpers ───────────────────────────────────────────────────────────────────

def _roe_allows_active_validation(engagement: Engagement) -> bool:
    """RoE gate: active validation is allowed unless the engagement's RoE
    explicitly opts out. A packet only leaves on approve, where this is checked."""
    roe = engagement.rules_of_engagement or {}
    return bool(roe.get("active_validation_allowed", True))


def _default_check_kind(finding: Finding | None) -> str:
    """Pick a safe check for the finding. TLS findings → tls_handshake, else a
    banner re-grab. safe_poc is only ever chosen explicitly (needs a pinned
    template), never auto-defaulted."""
    if finding is not None:
        hay = f"{getattr(finding, 'title', '') or ''} {getattr(finding, 'evidence', '') or ''}".lower()
        if "tls" in hay or "ssl" in hay or "certificate" in hay:
            return CHECK_TLS
    return CHECK_BANNER


async def _load_finding_and_eng(
    db: AsyncSession, finding_id: uuid.UUID, engagement_id: uuid.UUID, tenant_id: uuid.UUID
) -> tuple[Finding, Engagement]:
    engagement = (await db.execute(
        select(Engagement).where(Engagement.id == engagement_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if not engagement:
        raise HTTPException(404, "Engagement not found")
    finding = (await db.execute(
        select(Finding).where(Finding.id == finding_id, Finding.engagement_id == engagement_id)
    )).scalar_one_or_none()
    if not finding:
        raise HTTPException(404, "Finding not found")
    return finding, engagement


async def _get_request_or_404(
    db: AsyncSession, request_id: uuid.UUID, tenant_id: uuid.UUID
) -> ValidationRequest:
    vr = (await db.execute(
        select(ValidationRequest)
        .join(Engagement, ValidationRequest.engagement_id == Engagement.id)
        .where(ValidationRequest.id == request_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if not vr:
        raise HTTPException(404, "Validation request not found")
    return vr


def _request_out(vr: ValidationRequest) -> ValidationRequestOut:
    return ValidationRequestOut(
        id=vr.id, engagement_id=vr.engagement_id, finding_id=vr.finding_id,
        target_ip=vr.target_ip, target_port=vr.target_port, check_kind=vr.check_kind,
        status=vr.status, outcome=vr.outcome, job_id=vr.job_id,
        requested_by=vr.requested_by, requested_at=vr.requested_at,
        reviewed_by=vr.reviewed_by, reviewed_at=vr.reviewed_at,
    )


# ── POST …/validate — create an approval-gated request ────────────────────────

@router.post(
    "/engagements/{engagement_id}/findings/{finding_id}/validate",
    status_code=status.HTTP_201_CREATED,
    summary="Request a safe, approval-gated live re-check of a finding",
)
async def create_validation_request(
    engagement_id: uuid.UUID,
    finding_id: uuid.UUID,
    body: ValidateRequest,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
):
    finding, engagement = await _load_finding_and_eng(
        db, finding_id, engagement_id, current_user.tenant_id
    )
    if not _roe_allows_active_validation(engagement):
        raise HTTPException(403, "Active validation is not permitted by this engagement's RoE")

    check_kind = body.check_kind or _default_check_kind(finding)
    if check_kind not in _SAFE_CHECKS:
        raise HTTPException(400, f"Unsupported check_kind: {check_kind}")

    vr = ValidationRequest(
        engagement_id=engagement_id,
        finding_id=finding_id,
        target_ip=body.target_ip,
        target_port=body.target_port,
        check_kind=check_kind,
        status=VR_PENDING,
        requested_by=str(current_user.user_id),
    )
    db.add(vr)
    await db.flush()
    await db.refresh(vr)
    logger.info("validation.request.created", request_id=str(vr.id),
                finding_id=str(finding_id), check_kind=check_kind)
    return _request_out(vr)


# ── GET …/validation-requests ─────────────────────────────────────────────────

@router.get(
    "/engagements/{engagement_id}/validation-requests",
    response_model=list[ValidationRequestOut],
    summary="List validation requests (pending by default)",
)
async def list_validation_requests(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    status_filter: str | None = Query(default=VR_PENDING, alias="status"),
):
    q = (
        select(ValidationRequest)
        .join(Engagement, ValidationRequest.engagement_id == Engagement.id)
        .where(
            Engagement.tenant_id == current_user.tenant_id,
            ValidationRequest.engagement_id == engagement_id,
        )
    )
    if status_filter:
        q = q.where(ValidationRequest.status == status_filter)
    q = q.order_by(ValidationRequest.requested_at.desc())
    rows = (await db.execute(q)).scalars().all()
    return [_request_out(r) for r in rows]


# ── POST /validation-requests/{id}/approve — approve → enqueue ────────────────

@router.post(
    "/validation-requests/{request_id}/approve",
    status_code=status.HTTP_200_OK,
    summary="Approve a validation request — enqueues a single-target safe validate job",
)
async def approve_validation(
    request_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    vr = await _get_request_or_404(db, request_id, current_user.tenant_id)
    if vr.status != VR_PENDING:
        raise HTTPException(409, f"Validation request is already {vr.status}")

    engagement = (await db.execute(
        select(Engagement).where(Engagement.id == vr.engagement_id)
    )).scalar_one_or_none()
    if engagement is None:
        raise HTTPException(404, "Engagement not found")
    if not _roe_allows_active_validation(engagement):
        raise HTTPException(403, "Active validation is not permitted by this engagement's RoE")

    # Enqueue a single-target, safe-allowlisted validate job. Job params live in
    # scan_jobs.result while pending (see agents.py dispatch: params = job.result).
    job = ScanJob(
        engagement_id=vr.engagement_id,
        job_type=ScanJobType.vuln_scan,
        status=ScanJobStatus.pending,
        result={
            "mode": "validate",
            "validation_request_id": str(vr.id),
            "finding_id": str(vr.finding_id) if vr.finding_id else None,
            "target": vr.target_ip,
            "targets": [vr.target_ip],
            "port": vr.target_port,
            "check_kind": vr.check_kind,
            "scope_cidrs": [f"{vr.target_ip}/32"],
            "allowlist": "safe",
        },
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)

    vr.status = VR_APPROVED
    vr.reviewed_by = str(current_user.user_id)
    vr.reviewed_at = datetime.now(timezone.utc)
    vr.job_id = job.id
    await db.flush()

    logger.info("validation.request.approved", request_id=str(request_id),
                job_id=str(job.id), approver=str(current_user.user_id))
    return {"approved": True, "request_id": str(request_id), "job_id": str(job.id)}


# ── POST /validation-requests/{id}/reject ─────────────────────────────────────

@router.post(
    "/validation-requests/{request_id}/reject",
    status_code=status.HTTP_200_OK,
    summary="Reject a validation request",
)
async def reject_validation(
    request_id: uuid.UUID,
    body: RejectBody,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    vr = await _get_request_or_404(db, request_id, current_user.tenant_id)
    if vr.status != VR_PENDING:
        raise HTTPException(409, f"Validation request is already {vr.status}")
    vr.status = VR_REJECTED
    vr.reviewed_by = str(current_user.user_id)
    vr.reviewed_at = datetime.now(timezone.utc)
    await db.flush()
    logger.info("validation.request.rejected", request_id=str(request_id),
                reason=body.reason)
    return {"rejected": True, "request_id": str(request_id)}
