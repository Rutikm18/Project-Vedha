"""
customer_access.py — operator-facing management of the customer portal (Part 2,
Phase 1). Lives on the manager dashboard; every route is operator-only.

Three jobs:
  1. Provision / reset / disable the ONE client login bound to an engagement.
  2. Assign the engagement's agent (the probe a customer's scan runs on).
  3. The scan-request inbox: list, approve (→ dispatch a ScanJob on the assigned
     agent), reject. Customers create requests (Phase 3); operators decide here.

All mutating actions are written to the append-only audit log. The customer never
runs a scan directly — this request→approval split is the control.
"""
from __future__ import annotations

import re
import secrets
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.agent import Agent
from app.models.engagement import Engagement
from app.models.enums import ScanJobStatus, ScanJobType, UserRole
from app.models.scan_job import ScanJob
from app.models.scan_request import ScanRequest, SR_APPROVED, SR_PENDING, SR_REJECTED
from app.models.user import User
from app.services.audit import record_audit
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements", tags=["customer-access"])
# Tenant-wide customer directory for the operator "Customers" dashboard section
# (the per-engagement routes above manage ONE login; this lists them all).
customers_router = APIRouter(prefix="/customers", tags=["customer-access"])
logger = structlog.get_logger()

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

_OPERATOR = require_role(["admin", "manager"])


# ── schemas ───────────────────────────────────────────────────────────────────

class ClientUserCreate(BaseModel):
    email: EmailStr
    password: str | None = None      # generated if omitted


class ClientUserPatch(BaseModel):
    reset_password: bool = False
    is_active: bool | None = None


class ClientUserOut(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool
    engagement_id: uuid.UUID
    portal_slug: str | None = None    # the customer's stable handle / future subdomain
    temp_password: str | None = None  # returned ONCE on create/reset


class AssignAgentBody(BaseModel):
    agent_id: uuid.UUID


class ScanRequestOut(BaseModel):
    id: uuid.UUID
    engagement_id: uuid.UUID
    scan_type: str
    status: str
    note: str | None
    requested_by: uuid.UUID | None
    requested_at: datetime
    scan_job_id: uuid.UUID | None
    reviewed_by: uuid.UUID | None
    reviewed_at: datetime | None
    review_reason: str | None


class RejectBody(BaseModel):
    reason: str | None = None


# ── helpers (unit-testable) ────────────────────────────────────────────────────

def generate_password(n: int = 16) -> str:
    """A URL-safe temporary password the operator hands to the customer once."""
    return secrets.token_urlsafe(n)


def _slugify(raw: str) -> str:
    """A lowercase, hyphenated, DNS-label-safe base for a customer portal handle
    (so it can later become <slug>.portal.<domain> with no rewriting)."""
    s = re.sub(r"[^a-z0-9]+", "-", (raw or "").lower()).strip("-")
    return (s or "customer")[:40]


async def _unique_portal_slug(db, tenant_id: uuid.UUID, base: str) -> str:
    """Per-tenant-unique portal slug: <base>, else <base>-2, <base>-3, … Two
    customers can never collide on a handle (and therefore a future subdomain)."""
    root = _slugify(base)
    candidate, n = root, 1
    while (await db.execute(
        select(User.id).where(User.tenant_id == tenant_id,
                              User.portal_slug == candidate)
    )).first() is not None:
        n += 1
        candidate = f"{root}-{n}"[:63]
    return candidate


def build_scan_job(scan_request: ScanRequest, engagement: Engagement) -> ScanJob:
    """Pure: turn an approved request into a pending ScanJob on the engagement's
    assigned agent. Raises ValueError if no agent is assigned (caller → 409).

    The customer's chosen targets + intensity ride into ``result`` so the existing
    dispatch-time scope gate (agents.py) and the probe consume them. Targets were
    already validated ⊆ scope at request time; the dispatch gate re-validates."""
    if engagement.assigned_agent_id is None:
        raise ValueError("engagement has no assigned agent")
    try:
        job_type = ScanJobType(scan_request.scan_type)
    except ValueError:
        job_type = ScanJobType.vuln_scan
    result: dict = {
        "mode": "scan",
        "scan_request_id": str(scan_request.id),
        "requested_by": (str(scan_request.requested_by)
                         if scan_request.requested_by else None),
        "scope_cidrs": list(engagement.scope_cidrs or []),
    }
    if getattr(scan_request, "targets", None):
        result["targets"] = list(scan_request.targets)
    if getattr(scan_request, "intensity", None):
        result["intensity"] = scan_request.intensity
    return ScanJob(
        engagement_id=engagement.id,
        job_type=job_type,
        status=ScanJobStatus.pending,
        agent_id=str(engagement.assigned_agent_id),
        result=result,
    )


async def _existing_client_user(db, engagement_id: uuid.UUID) -> User | None:
    return (await db.execute(
        select(User).where(
            User.client_engagement_id == engagement_id,
            User.role == UserRole.client,
        )
    )).scalar_one_or_none()


# ── provisioning ────────────────────────────────────────────────────────────

@router.post("/{engagement_id}/client-user", response_model=ClientUserOut,
             status_code=status.HTTP_201_CREATED,
             summary="Provision the customer login for an engagement")
async def provision_client_user(
    engagement_id: uuid.UUID,
    body: ClientUserCreate,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    if await _existing_client_user(db, engagement_id) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "A customer login already exists for this engagement "
                            "(use PATCH to reset the password)")
    # The users table is UNIQUE(tenant_id, email). An email already used ANYWHERE
    # in the tenant — the operator's own login, or a client login already made for
    # another engagement ("one more") — would violate that constraint at flush and
    # surface as an opaque 500. Pre-check for a clear, actionable 409 instead.
    if (await db.execute(
        select(User).where(User.tenant_id == eng.tenant_id, User.email == body.email)
    )).scalar_one_or_none() is not None:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "A user with this email already exists in this tenant")
    temp = body.password or generate_password()
    slug = await _unique_portal_slug(
        db, eng.tenant_id, getattr(eng, "name", None) or body.email.split("@")[0])
    user = User(
        tenant_id=eng.tenant_id,
        email=body.email,
        hashed_password=_pwd.hash(temp),
        role=UserRole.client,
        client_engagement_id=engagement_id,
        portal_slug=slug,
        is_active=True,
    )
    db.add(user)
    try:
        await db.flush()
        await db.refresh(user)
    except IntegrityError:
        # Defense-in-depth for the TOCTOU race between the pre-check above and this
        # insert: another request may have claimed the email/slug first. Roll back
        # and report the same clean 409 rather than leaking a 500.
        await db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "A user with this email already exists in this tenant")
    record_audit(db, actor_id=current_user.user_id, action="client_user.provisioned",
                 engagement_id=engagement_id, resource_type="user", resource_id=user.id,
                 detail={"email": body.email, "portal_slug": slug})
    await db.flush()
    logger.info("client_user.provisioned", engagement_id=str(engagement_id),
                user_id=str(user.id), portal_slug=slug, by=str(current_user.user_id))
    return ClientUserOut(id=user.id, email=user.email, is_active=user.is_active,
                         engagement_id=engagement_id, portal_slug=slug, temp_password=temp)


@router.get("/{engagement_id}/client-user", response_model=ClientUserOut,
            summary="View the customer login for an engagement")
async def get_client_user(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    user = await _existing_client_user(db, engagement_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No customer login provisioned")
    return ClientUserOut(id=user.id, email=user.email, is_active=user.is_active,
                         engagement_id=engagement_id, portal_slug=user.portal_slug)


@router.patch("/{engagement_id}/client-user", response_model=ClientUserOut,
              summary="Reset password or enable/disable the customer login")
async def patch_client_user(
    engagement_id: uuid.UUID,
    body: ClientUserPatch,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    user = await _existing_client_user(db, engagement_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No customer login provisioned")
    temp = None
    if body.reset_password:
        temp = generate_password()
        user.hashed_password = _pwd.hash(temp)
    if body.is_active is not None:
        user.is_active = body.is_active
    record_audit(db, actor_id=current_user.user_id, action="client_user.updated",
                 engagement_id=engagement_id, resource_type="user", resource_id=user.id,
                 detail={"reset_password": body.reset_password, "is_active": body.is_active})
    await db.flush()
    return ClientUserOut(id=user.id, email=user.email, is_active=user.is_active,
                         engagement_id=engagement_id, portal_slug=user.portal_slug,
                         temp_password=temp)


@router.patch("/{engagement_id}/assign-agent",
              summary="Assign the agent this engagement's scans run on")
async def assign_agent(
    engagement_id: uuid.UUID,
    body: AssignAgentBody,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    agent = (await db.execute(
        select(Agent).where(Agent.id == body.agent_id,
                            Agent.tenant_id == current_user.tenant_id)
    )).scalar_one_or_none()
    if agent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agent not found in this tenant")
    eng.assigned_agent_id = agent.id
    record_audit(db, actor_id=current_user.user_id, action="engagement.agent_assigned",
                 engagement_id=engagement_id, resource_type="agent", resource_id=agent.id)
    await db.flush()
    return {"engagement_id": str(engagement_id), "assigned_agent_id": str(agent.id)}


# ── scan-request inbox ────────────────────────────────────────────────────────

async def _get_scan_request(db, engagement_id: uuid.UUID, request_id: uuid.UUID,
                            tenant_id: uuid.UUID) -> ScanRequest:
    sr = (await db.execute(
        select(ScanRequest).where(
            ScanRequest.id == request_id,
            ScanRequest.engagement_id == engagement_id,
            ScanRequest.tenant_id == tenant_id,
        )
    )).scalar_one_or_none()
    if sr is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scan request not found")
    return sr


@router.get("/{engagement_id}/scan-requests", response_model=list[ScanRequestOut],
            summary="List scan requests for an engagement (operator inbox)")
async def list_scan_requests(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    rows = (await db.execute(
        select(ScanRequest)
        .where(ScanRequest.engagement_id == engagement_id,
               ScanRequest.tenant_id == current_user.tenant_id)
        .order_by(ScanRequest.requested_at.desc())
    )).scalars().all()
    return [ScanRequestOut.model_validate(r, from_attributes=True) for r in rows]


@router.post("/{engagement_id}/scan-requests/{request_id}/approve",
             summary="Approve a scan request → dispatch a job on the assigned agent")
async def approve_scan_request(
    engagement_id: uuid.UUID,
    request_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    sr = await _get_scan_request(db, engagement_id, request_id, current_user.tenant_id)
    if sr.status != SR_PENDING:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Scan request is already {sr.status}")
    try:
        job = build_scan_job(sr, eng)
    except ValueError:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "Assign an agent to this engagement before approving scans")
    db.add(job)
    await db.flush()
    await db.refresh(job)
    sr.status = SR_APPROVED
    sr.reviewed_by = current_user.user_id
    sr.reviewed_at = datetime.now(timezone.utc)
    sr.scan_job_id = job.id
    record_audit(db, actor_id=current_user.user_id, action="scan_request.approved",
                 engagement_id=engagement_id, resource_type="scan_request", resource_id=sr.id,
                 detail={"job_id": str(job.id)})
    await db.flush()
    logger.info("scan_request.approved", request_id=str(request_id),
                job_id=str(job.id), by=str(current_user.user_id))
    return {"approved": True, "request_id": str(request_id), "job_id": str(job.id)}


@router.post("/{engagement_id}/scan-requests/{request_id}/reject",
             summary="Reject a scan request")
async def reject_scan_request(
    engagement_id: uuid.UUID,
    request_id: uuid.UUID,
    body: RejectBody,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    sr = await _get_scan_request(db, engagement_id, request_id, current_user.tenant_id)
    if sr.status != SR_PENDING:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Scan request is already {sr.status}")
    sr.status = SR_REJECTED
    sr.reviewed_by = current_user.user_id
    sr.reviewed_at = datetime.now(timezone.utc)
    sr.review_reason = body.reason
    record_audit(db, actor_id=current_user.user_id, action="scan_request.rejected",
                 engagement_id=engagement_id, resource_type="scan_request", resource_id=sr.id,
                 detail={"reason": body.reason})
    await db.flush()
    return {"rejected": True, "request_id": str(request_id)}


# ── Tenant-wide customer directory (operator "Customers" dashboard) ─────────────

class CustomerListItem(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool
    engagement_id: uuid.UUID | None
    engagement_name: str | None
    portal_slug: str | None
    created_at: datetime | None


@customers_router.get("", response_model=list[CustomerListItem],
                      summary="List every customer login for the tenant")
async def list_customers(
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    """Every provisioned customer login (role=client) in the tenant, with its
    bound engagement and portal handle — powers the operator Customers section."""
    rows = (await db.execute(
        select(User, Engagement.name)
        .join(Engagement, User.client_engagement_id == Engagement.id, isouter=True)
        .where(User.tenant_id == current_user.tenant_id,
               User.role == UserRole.client)
        .order_by(User.created_at.desc())
    )).all()
    return [
        CustomerListItem(
            id=u.id, email=u.email, is_active=u.is_active,
            engagement_id=u.client_engagement_id, engagement_name=eng_name,
            portal_slug=u.portal_slug, created_at=u.created_at,
        )
        for u, eng_name in rows
    ]
