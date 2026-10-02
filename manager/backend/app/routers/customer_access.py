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
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import structlog
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, model_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth.password import hash_password
from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.agent import Agent
from app.models.customer_entitlement import (
    DEFAULT_POC_LOCKED_SEVERITIES, LOCKABLE_FEATURES, LOCKABLE_SEVERITIES, PLAN_LICENSED,
    PLAN_POC, SCAN_MODES, CustomerEntitlement,
)
from app.models.engagement import Engagement
from app.models.enums import ScanJobStatus, ScanJobType, UserRole
from app.models.scan_job import ScanJob
from app.models.scan_request import ScanRequest, SR_APPROVED, SR_PENDING, SR_REJECTED
from app.models.user import User
from app.schemas.portal import EntitlementOut
from app.services import entitlements
from app.services.audit import record_audit
from app.services.credential_crypto import decrypt_credential, encrypt_credential
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements", tags=["customer-access"])
# Tenant-wide customer directory for the operator "Customers" dashboard section
# (the per-engagement routes above manage ONE login; this lists them all).
customers_router = APIRouter(prefix="/customers", tags=["customer-access"])
logger = structlog.get_logger()

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


class EntitlementConfig(BaseModel):
    """Operator's plan configuration for one customer.

    POC: give ``duration_days`` (from ``starts_at``, default now) or an explicit
    ``expires_at`` — a POC must end. Licensed: ``expires_at`` is the licence term
    end, or omit it for no end date.

    Scan allowances: ``scan_quota`` is an optional overall cap across every type
    (None = no cap). Each type has its own: None = unlimited, 0 = not included.
    Aggressive and deep are opt-in (default 0). A deep scan covers exactly one
    asset; ``deep_repeat_policy`` says whether that asset may be deep-scanned
    again ("repeat") or each deep scan must be a different asset ("distinct")."""
    plan_type: Literal["poc", "licensed"]
    starts_at: datetime | None = None
    duration_days: int | None = Field(default=None, ge=1, le=3650)
    expires_at: datetime | None = None
    scan_quota: int | None = Field(default=None, ge=0, le=100_000)
    stealth_quota: int | None = Field(default=None, ge=0, le=100_000)
    normal_quota: int | None = Field(default=None, ge=0, le=100_000)
    aggressive_quota: int | None = Field(default=0, ge=0, le=100_000)
    deep_quota: int | None = Field(default=0, ge=0, le=100_000)
    deep_repeat_policy: Literal["distinct", "repeat"] = "distinct"
    notes: str | None = Field(default=None, max_length=2000)
    # Portal locks. None = leave as they are (a new POC starts with Critical +
    # High locked, anything else with nothing locked); a list replaces them.
    locked_severities: list[Literal["critical", "high", "medium", "low", "info"]] | None = None
    locked_features: list[Literal["ai_assistant", "compliance", "remediation", "reports"]] | None = None

    @model_validator(mode="after")
    def _window(self):
        if self.duration_days is not None and self.expires_at is not None:
            raise ValueError("give duration_days or expires_at, not both")
        if self.plan_type == PLAN_POC and self.duration_days is None and self.expires_at is None:
            raise ValueError("a POC needs a duration (duration_days) or an end date (expires_at)")
        return self


class EntitlementAdjust(BaseModel):
    """Top-up without re-configuring: add scans (to one scan type, or to the
    overall cap when ``mode`` is omitted) and/or extend the end date."""
    add_scans: int = Field(default=0, ge=0, le=100_000)
    mode: Literal["stealth", "normal", "aggressive", "deep"] | None = None
    extend_days: int = Field(default=0, ge=0, le=3650)
    reset_usage: bool = False


class EntitlementAdminOut(EntitlementOut):
    configured: bool
    notes: str | None = None
    updated_at: datetime | None = None


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
    if getattr(scan_request, "quota_consumed", False):
        # The request's quota spend moves to the job: cancelling it before a
        # probe starts it gives the scan back (entitlements.refund_for_job).
        result[entitlements.JOB_QUOTA_FLAG] = True
        mode = getattr(scan_request, "quota_mode", None)
        if mode:
            result[entitlements.JOB_QUOTA_MODE] = mode
            targets = list(getattr(scan_request, "targets", None) or [])
            if mode == "deep" and len(targets) == 1:
                result[entitlements.JOB_DEEP_TARGET] = targets[0]
    if getattr(scan_request, "use_case_id", None):
        # The exact capability use-case the customer chose — the probe runs this.
        result["use_case_id"] = scan_request.use_case_id
    return ScanJob(
        engagement_id=engagement.id,
        job_type=job_type,
        status=ScanJobStatus.pending,
        agent_id=str(engagement.assigned_agent_id),
        result=result,
    )


async def _apply_fragile_guard(db, engagement: Engagement, job: ScanJob) -> None:
    """Customer-requested scans never touch fragile assets (HSM / ATM / SWIFT / ICS)
    intrusively — there is no override on this path; an operator who needs it
    launches a separate, audited override job."""
    from app.routers.agents import _USE_CASES, _normalize_intensity_name
    from app.services.fragile_guard import merge_excluded, plan_for_job

    params = job.result or {}
    use_case = _USE_CASES.get(params.get("use_case_id") or "", {})
    scan_type = use_case.get("scan_type") or getattr(job.job_type, "value", job.job_type)
    try:
        intensity = _normalize_intensity_name(params.get("intensity")) or use_case.get("intensity")
    except ValueError:
        intensity = None
    job_scope = list(params.get("targets") or engagement.scope_cidrs or [])
    plan = await plan_for_job(db, engagement.id, scan_type=scan_type, intensity=intensity,
                              job_scope=job_scope)
    if plan is None:
        return
    if plan.fully_blocked:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Every requested target is a fragile asset (HSM / ATM / SWIFT / ICS); this scan "
            "would do nothing. Reject it, or launch an audited operator override instead.")
    job.result = {**params,
                  "_excluded_cidrs": merge_excluded(
                      params.get("_excluded_cidrs") or list(engagement.excluded_cidrs or []),
                      plan.cidrs),
                  "_fragile_excluded": plan.hosts}


async def _apply_scan_policy(db, tenant_id: uuid.UUID, role: str, job: ScanJob) -> dict | None:
    """The organisation's scan policy for a job built outside the normal enqueue
    path: refuse during a blackout (an admin may override when the policy allows,
    returned so the caller can audit it) and merge the global exclusions."""
    from app.services import org_settings

    policy = await org_settings.get_section(db, tenant_id, "scan")
    window = org_settings.active_blackout(policy)
    override = None
    if window is not None:
        if policy.admin_override and role == "admin":
            override = {"window": window.name}
        else:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Scanning is paused by the blackout window '{window.name}'."
                + (" An admin can override it." if policy.admin_override else ""))
    if policy.global_exclusions:
        params = job.result or {}
        job.result = {**params, "_excluded_cidrs": org_settings.merge_global_exclusions(
            params.get("_excluded_cidrs"), policy)}
    return override


def apply_entitlement_config(row: CustomerEntitlement, body: EntitlementConfig,
                             *, now: datetime, defaults=None) -> None:
    """Pure: write a configuration onto a (new or existing) entitlement row.
    Usage (scans_used) is kept — re-configuring a plan never hands back scans
    silently; that's what ``reset_usage`` on /adjust is for."""
    starts = body.starts_at or row.starts_at or now
    if starts.tzinfo is None:
        starts = starts.replace(tzinfo=timezone.utc)
    row.plan_type = body.plan_type
    row.starts_at = starts
    if body.duration_days is not None:
        row.expires_at = starts + timedelta(days=body.duration_days)
    else:
        row.expires_at = body.expires_at
    if row.expires_at is not None and row.expires_at <= starts:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "The end date must be after the start date")
    row.scan_quota = body.scan_quota
    for mode in SCAN_MODES:
        setattr(row, f"{mode}_quota", getattr(body, f"{mode}_quota"))
    row.deep_repeat_policy = body.deep_repeat_policy
    row.notes = body.notes
    _apply_locks(row, body, defaults)
    if body.plan_type == PLAN_LICENSED and not row.license_key:
        row.license_key = entitlements.generate_license_key()


def _apply_locks(row: CustomerEntitlement, body: EntitlementConfig, defaults=None) -> None:
    """Locks are never taken away or added implicitly on an existing plan: an
    omitted list keeps the current one. A brand-new row (attributes still None
    before its first flush) gets the organisation's new-customer defaults, or the
    built-in ones when none are set."""
    poc_severities = list(defaults.poc_locked_severities) if defaults else list(DEFAULT_POC_LOCKED_SEVERITIES)
    poc_features = list(defaults.poc_locked_features) if defaults else []
    if body.locked_severities is not None:
        chosen = set(body.locked_severities)
        row.locked_severities = [s for s in LOCKABLE_SEVERITIES if s in chosen]
    elif row.locked_severities is None:
        row.locked_severities = [s for s in LOCKABLE_SEVERITIES if s in poc_severities] if body.plan_type == PLAN_POC else []
    if body.locked_features is not None:
        chosen = set(body.locked_features)
        row.locked_features = [f for f in LOCKABLE_FEATURES if f in chosen]
    elif row.locked_features is None:
        row.locked_features = [f for f in LOCKABLE_FEATURES if f in poc_features] if body.plan_type == PLAN_POC else []


def _admin_view(row: CustomerEntitlement | None) -> EntitlementAdminOut:
    view = entitlements.evaluate(row)
    return EntitlementAdminOut(**entitlements.view_dict(view), configured=row is not None,
                               notes=getattr(row, "notes", None),
                               updated_at=getattr(row, "updated_at", None))


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
        hashed_password=await hash_password(temp),
        portal_password_enc=encrypt_credential(temp),  # recoverable copy for reveal
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
        user.hashed_password = await hash_password(temp)
        user.portal_password_enc = encrypt_credential(temp)  # keep recoverable copy in sync
    if body.is_active is not None:
        user.is_active = body.is_active
    record_audit(db, actor_id=current_user.user_id, action="client_user.updated",
                 engagement_id=engagement_id, resource_type="user", resource_id=user.id,
                 detail={"reset_password": body.reset_password, "is_active": body.is_active})
    await db.flush()
    return ClientUserOut(id=user.id, email=user.email, is_active=user.is_active,
                         engagement_id=engagement_id, portal_slug=user.portal_slug,
                         temp_password=temp)


# ── plan / licence configuration ─────────────────────────────────────────────

@router.get("/{engagement_id}/entitlement", response_model=EntitlementAdminOut,
            summary="The customer's plan (POC / licensed), quota and usage")
async def get_entitlement(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    return _admin_view(await entitlements.get_entitlement(db, engagement_id))


@router.put("/{engagement_id}/entitlement", response_model=EntitlementAdminOut,
            summary="Configure the customer's plan: POC with a duration, or a licence term")
async def put_entitlement(
    engagement_id: uuid.UUID,
    body: EntitlementConfig,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    row = await entitlements.get_entitlement(db, engagement_id, for_update=True)
    created = row is None
    if created:
        row = CustomerEntitlement(tenant_id=eng.tenant_id, engagement_id=engagement_id,
                                  scans_used=0, stealth_used=0, normal_used=0,
                                  aggressive_used=0, deep_used=0, deep_scanned_targets=[])
        db.add(row)
    def _snapshot(r) -> dict:
        return {"plan_type": r.plan_type,
                "expires_at": r.expires_at and r.expires_at.isoformat(),
                "scan_quota": r.scan_quota,
                **{f"{m}_quota": getattr(r, f"{m}_quota") for m in SCAN_MODES},
                "deep_repeat_policy": r.deep_repeat_policy,
                "locked_severities": list(r.locked_severities or []),
                "locked_features": list(r.locked_features or [])}
    before = None if created else _snapshot(row)
    from app.services import org_settings
    defaults = await org_settings.get_section(db, current_user.tenant_id, "customer-defaults") if created else None
    apply_entitlement_config(row, body, now=datetime.now(timezone.utc), defaults=defaults)
    row.updated_by = current_user.user_id
    await db.flush()
    await db.refresh(row)
    record_audit(db, actor_id=current_user.user_id, action="entitlement.configured",
                 engagement_id=engagement_id, resource_type="entitlement", resource_id=row.id,
                 detail={"before": before, "after": _snapshot(row)})
    await db.flush()
    return _admin_view(row)


@router.post("/{engagement_id}/entitlement/adjust", response_model=EntitlementAdminOut,
             summary="Add scans, extend the end date, or reset usage")
async def adjust_entitlement(
    engagement_id: uuid.UUID,
    body: EntitlementAdjust,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    row = await entitlements.get_entitlement(db, engagement_id, for_update=True)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            "Configure a plan for this customer first")
    if body.add_scans and body.mode:
        # Adding to an excluded type (quota 0) turns it on with that many scans;
        # an unlimited type stays unlimited.
        current = getattr(row, f"{body.mode}_quota")
        if current is not None:
            setattr(row, f"{body.mode}_quota", current + body.add_scans)
    elif body.add_scans and row.scan_quota is not None:
        row.scan_quota += body.add_scans
    if body.extend_days and row.expires_at is not None:
        # Extending an already-expired POC counts from today, not from the past.
        base = max(row.expires_at, datetime.now(timezone.utc))
        row.expires_at = base + timedelta(days=body.extend_days)
    if body.reset_usage:
        row.scans_used = 0
        for mode in SCAN_MODES:
            setattr(row, f"{mode}_used", 0)
        # The repeat history is usage too: a reset starts deep coverage over.
        row.deep_scanned_targets = []
    row.updated_by = current_user.user_id
    await db.flush()
    await db.refresh(row)
    record_audit(db, actor_id=current_user.user_id, action="entitlement.adjusted",
                 engagement_id=engagement_id, resource_type="entitlement", resource_id=row.id,
                 detail=body.model_dump())
    await db.flush()
    return _admin_view(row)


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
    await _apply_fragile_guard(db, eng, job)
    blackout_override = await _apply_scan_policy(db, current_user.tenant_id, current_user.role, job)
    db.add(job)
    await db.flush()
    await db.refresh(job)
    if blackout_override is not None:
        record_audit(db, actor_id=current_user.user_id, action="scan.blackout_override",
                     engagement_id=engagement_id, resource_type="scan_job", resource_id=job.id,
                     detail=blackout_override)
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
    await entitlements.refund_for_request(db, sr)
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
    entitlement: EntitlementOut | None = None   # None → no plan configured


@customers_router.get("", response_model=list[CustomerListItem],
                      summary="List every customer login for the tenant")
async def list_customers(
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    """Every provisioned customer login (role=client) in the tenant, with its
    bound engagement and portal handle — powers the operator Customers section."""
    rows = (await db.execute(
        select(User, Engagement.name, CustomerEntitlement)
        .join(Engagement, User.client_engagement_id == Engagement.id, isouter=True)
        .join(CustomerEntitlement,
              CustomerEntitlement.engagement_id == User.client_engagement_id, isouter=True)
        .where(User.tenant_id == current_user.tenant_id,
               User.role == UserRole.client)
        .order_by(User.created_at.desc())
    )).all()
    return [
        CustomerListItem(
            id=u.id, email=u.email, is_active=u.is_active,
            engagement_id=u.client_engagement_id, engagement_name=eng_name,
            portal_slug=u.portal_slug, created_at=u.created_at,
            entitlement=(EntitlementOut(**entitlements.view_dict(entitlements.evaluate(ent)))
                         if ent is not None else None),
        )
        for u, eng_name, ent in rows
    ]


class RevealOut(BaseModel):
    id: uuid.UUID
    email: str
    password: str | None      # None → login predates encrypted storage; Reset to populate


@customers_router.get("/{user_id}/reveal", response_model=RevealOut,
                      summary="Reveal a customer login's password (operator-only, audited)")
async def reveal_customer_password(
    user_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
):
    """Decrypt and return a customer login's stored password. Tenant-scoped and
    written to the append-only audit log on every access — revealing a credential
    is itself an audited operator action."""
    user = (await db.execute(
        select(User).where(
            User.id == user_id,
            User.tenant_id == current_user.tenant_id,
            User.role == UserRole.client,
        )
    )).scalar_one_or_none()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer login not found")
    password = decrypt_credential(user.portal_password_enc)
    record_audit(db, actor_id=current_user.user_id, action="client_user.password_revealed",
                 engagement_id=user.client_engagement_id, resource_type="user", resource_id=user.id,
                 detail={"email": user.email})
    await db.flush()
    return RevealOut(id=user.id, email=user.email, password=password)
