"""Device-code enrollment for probes; no human credential is installed on a probe."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import structlog
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import select

from app.auth.jwt import create_device_access_token
from app.auth.rbac import require_role
from app.config import get_settings
from app.dependencies import AuthUser, DB, RedisConn
from app.models.agent import Agent, AgentStatus
from app.agent_access import EXPIRED_MESSAGE, is_expired
from app.models.audit_log import AuditLog
from app.models.engagement import Engagement
from app.models.probe_enrollment import AgentCredential, ProbeEnrollmentRequest, ProbeEnrollmentToken
from app.models.probe_site import ProbeSite
from app.models.tenant import Tenant
from app.ratelimit import client_ip
from app.schemas.engagement import validate_scope_entries
from app.services.audit import record_audit

router = APIRouter(prefix="/probe-enrollment", tags=["probe-enrollment"])
logger = structlog.get_logger()
_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _secret_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _keyed_hash(value: str) -> str:
    return hmac.new(
        get_settings().jwt_secret.encode("utf-8"),
        value.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _derive_refresh_secret(request_id: uuid.UUID, device_secret: str) -> str:
    digest = hmac.new(
        get_settings().jwt_secret.encode("utf-8"),
        f"refresh:{request_id}:{device_secret}".encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


# ── Pre-authorized, Site-bound enrollment tokens ────────────────────────────
ENROLL_TOKEN_PREFIX = "vet_"

# Engagement install-command lifetimes offered in Fleet: 1 h, 24 h, 7 days.
ENGAGEMENT_TOKEN_TTL_MINUTES = 24 * 60
INSTALL_TOKEN_LIFETIMES = (60, 24 * 60, 7 * 24 * 60)
MAX_LIVE_ENGAGEMENT_TOKENS = 5


def generate_enroll_token() -> tuple[str, str, str]:
    """Return (raw_token, token_hash, token_prefix). Raw is shown once."""
    raw = ENROLL_TOKEN_PREFIX + secrets.token_urlsafe(32)
    return raw, _secret_hash(raw), raw[:12]


def enroll_token_is_usable(token, now: datetime) -> bool:
    """A token can auto-approve only while live, unrevoked, and under max_uses."""
    return (
        token is not None
        and token.revoked_at is None
        and token.expires_at > now
        and token.uses < token.max_uses
    )


def _decode_public_key(value: str, label: str) -> bytes:
    try:
        raw = base64.b64decode(value, validate=True)
    except Exception as exc:
        raise ValueError(f"{label} must be canonical base64") from exc
    if len(raw) != 32:
        raise ValueError(f"{label} must encode exactly 32 bytes")
    return raw


def _verify_signature(public_key_b64: str, message: str, signature_b64: str) -> None:
    try:
        public_key = Ed25519PublicKey.from_public_bytes(
            _decode_public_key(public_key_b64, "signing_public_key")
        )
        signature = base64.b64decode(signature_b64, validate=True)
        public_key.verify(signature, message.encode("utf-8"))
    except (InvalidSignature, ValueError, TypeError) as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid device proof-of-possession signature") from exc


async def _rate_limit(redis, request: Request, bucket: str, limit: int) -> None:
    # Proxy-aware: behind Caddy the socket peer is Caddy for every probe.
    source = client_ip(request)
    key = f"probe-enrollment:{bucket}:{source}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, 60)
    except Exception as exc:
        logger.error("probe_enrollment.rate_limit_unavailable", error=str(exc))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Enrollment rate limiter unavailable") from exc
    if count > limit:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Enrollment request rate exceeded")


class EnrollmentCreate(BaseModel):
    signing_public_key: str
    encryption_public_key: str
    nonce: str = Field(min_length=16, max_length=64)
    hostname_hint: str | None = Field(default=None, max_length=255)
    platform: str = Field(min_length=1, max_length=64)
    architecture: str = Field(min_length=1, max_length=64)
    agent_version: str = Field(min_length=1, max_length=64)
    installer_version: str = Field(min_length=1, max_length=64)
    build_digest: str = Field(min_length=8, max_length=128)
    capabilities: list[str] = Field(default_factory=list, max_length=100)
    enroll_token: str | None = Field(default=None, min_length=8, max_length=128)

    @field_validator("signing_public_key", "encryption_public_key")
    @classmethod
    def validate_key(cls, value: str, info):
        _decode_public_key(value, info.field_name)
        return value


class EnrollTokenCreate(BaseModel):
    """A token installs an agent either into a pre-built Site (``site_id``) or for
    an engagement (``engagement_id``): the Site is then built from the
    engagement's scope at enrolment and the agent is assigned to it."""
    name: str = Field(min_length=1, max_length=120)
    site_id: uuid.UUID | None = None
    engagement_id: uuid.UUID | None = None
    expires_in_minutes: int = Field(default=ENGAGEMENT_TOKEN_TTL_MINUTES, ge=5, le=10080)
    max_uses: int = Field(default=1, ge=1, le=1000)

    @model_validator(mode="after")
    def exactly_one_target(self):
        if (self.site_id is None) == (self.engagement_id is None):
            raise ValueError("provide exactly one of site_id or engagement_id")
        if self.engagement_id is not None:
            if self.max_uses != 1:
                raise ValueError("an engagement token installs exactly one agent (max_uses must be 1)")
            if self.expires_in_minutes not in INSTALL_TOKEN_LIFETIMES:
                raise ValueError(f"expires_in_minutes must be one of {sorted(INSTALL_TOKEN_LIFETIMES)}")
        elif self.expires_in_minutes > 1440:
            raise ValueError("a Site token may live at most 1440 minutes (24 h)")
        return self


class EnrollmentSecret(BaseModel):
    device_secret: str = Field(min_length=32, max_length=128)


class EnrollmentActivate(EnrollmentSecret):
    signature: str = Field(min_length=40, max_length=256)


class SitePolicyInput(BaseModel):
    user_code: str = Field(min_length=8, max_length=9)
    probe_name: str = Field(min_length=1, max_length=255)
    site_id: uuid.UUID | None = None
    site_name: str | None = Field(default=None, min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    authorized_cidrs: list[str] = Field(min_length=1)
    excluded_cidrs: list[str] = Field(default_factory=list)
    approved_capabilities: list[str] = Field(min_length=1, max_length=100)
    max_targets: int = Field(default=4096, ge=1, le=65536)
    max_job_seconds: int = Field(default=7200, ge=30, le=86400)
    max_rate_pps: int = Field(default=1000, ge=1, le=100000)
    update_channel: str = Field(default="stable", pattern=r"^(stable|canary|pinned)$")

    @field_validator("authorized_cidrs", "excluded_cidrs")
    @classmethod
    def validate_networks(cls, values: list[str]) -> list[str]:
        return validate_scope_entries(values)

    @model_validator(mode="after")
    def require_site_reference(self):
        if (self.site_id is None) == (self.site_name is None):
            raise ValueError("provide exactly one of site_id or site_name")
        requested = set(self.approved_capabilities)
        if not requested:
            raise ValueError("approved_capabilities cannot be empty")
        import ipaddress
        allowed = [ipaddress.ip_network(value, strict=False) for value in self.authorized_cidrs]
        for value in self.excluded_cidrs:
            excluded = ipaddress.ip_network(value, strict=False)
            if not any(
                excluded.version == network.version and excluded.subnet_of(network)
                for network in allowed
            ):
                raise ValueError(f"excluded CIDR {value} is not inside authorized_cidrs")
        return self


class TokenRefresh(BaseModel):
    agent_id: uuid.UUID
    generation: int = Field(ge=1)
    refresh_secret: str = Field(min_length=32, max_length=128)
    nonce: str = Field(min_length=16, max_length=128)
    signature: str = Field(min_length=40, max_length=256)


def _policy(site: ProbeSite) -> dict:
    policy = {
        "site_id": str(site.id),
        "version": site.policy_version,
        "authorized_cidrs": list(site.authorized_cidrs or []),
        "excluded_cidrs": list(site.excluded_cidrs or []),
        "approved_capabilities": list(site.approved_capabilities or []),
        "max_targets": site.max_targets,
        "max_job_seconds": site.max_job_seconds,
        "max_rate_pps": site.max_rate_pps,
        "update_channel": site.update_channel,
    }
    canonical = json.dumps(policy, sort_keys=True, separators=(",", ":"))
    policy["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    settings = get_settings()
    if settings.probe_policy_signing_key:
        try:
            signing_seed = base64.b64decode(
                settings.probe_policy_signing_key, validate=True,
            )
        except Exception as exc:
            raise HTTPException(503, "Manager Site policy signing key is invalid") from exc
        if len(signing_seed) != 32:
            raise HTTPException(503, "Manager Site policy signing key must encode 32 bytes")
    elif settings.is_production:
        raise HTTPException(503, "Manager Site policy signing key is not configured")
    else:
        signing_seed = hmac.new(
            settings.jwt_secret.encode(), b"vedha-site-policy-signing-v1", hashlib.sha256,
        ).digest()
    private_key = Ed25519PrivateKey.from_private_bytes(signing_seed)
    public_key = private_key.public_key().public_bytes_raw()
    signed_payload = json.dumps(policy, sort_keys=True, separators=(",", ":"))
    policy["signing_public_key"] = base64.b64encode(public_key).decode()
    policy["signing_key_id"] = hashlib.sha256(public_key).hexdigest()[:16]
    policy["signature"] = base64.b64encode(
        private_key.sign(signed_payload.encode())
    ).decode()
    return policy


async def _provision_agent_for_site(
    db,
    *,
    row: ProbeEnrollmentRequest,
    site: ProbeSite,
    tenant_id: uuid.UUID,
    probe_name: str,
    location: str | None,
    approved_by: str,
    now: datetime,
    auto: bool,
) -> Agent:
    """Bind a request to a Site policy and create the provisioning Agent.

    Shared by the manual user_code approval and the pre-authorized token
    auto-approval so both paths enforce the identical capability-subset check,
    name-uniqueness rule, state transition, and audit trail.
    """
    duplicate_name = (await db.execute(
        select(Agent).where(Agent.tenant_id == tenant_id, Agent.name == probe_name.strip())
    )).scalar_one_or_none()
    if duplicate_name is not None:
        raise HTTPException(409, "A probe with this name already exists in the tenant")

    approved_capabilities = list(site.approved_capabilities or [])
    approved_networks = list(site.authorized_cidrs or [])
    if not set(approved_capabilities).issubset(set(row.reported_capabilities)):
        raise HTTPException(422, "Site capabilities must be a subset of device-reported capabilities")

    agent = Agent(
        tenant_id=tenant_id,
        site_id=site.id,
        name=probe_name.strip(),
        location=location or site.location,
        capabilities=approved_capabilities,
        approved_capabilities=approved_capabilities,
        network_segments=approved_networks,
        approved_networks=approved_networks,
        public_key=row.encryption_public_key,
        signing_public_key=row.signing_public_key,
        signing_key_fingerprint=row.signing_key_fingerprint,
        lifecycle_status="provisioning",
        status=AgentStatus.offline,
        agent_version=row.agent_version,
        installer_version=row.installer_version,
        build_digest=row.build_digest,
    )
    db.add(agent)
    await db.flush()
    row.state = "approved"
    row.tenant_id = tenant_id
    row.site_id = site.id
    row.agent_id = agent.id
    row.assigned_name = agent.name
    row.approved_by = approved_by
    row.approved_at = now
    row.activation_challenge = secrets.token_urlsafe(32)
    row.version += 1
    db.add(AuditLog(
        actor_id=approved_by,
        action="probe.enrollment.approved",
        resource_type="agent",
        resource_id=agent.id,
        detail={
            "site_id": str(site.id),
            "request_id": str(row.id),
            "fingerprint": row.signing_key_fingerprint,
            "auto": auto,
        },
        timestamp=now,
    ))
    return agent


# ── Engagement-bound enrolment (Fleet → Add agent) ───────────────────────────
# A customer (portal) or operator creates a single-use token FOR an engagement;
# the agent that enrols with it gets a Site built from that engagement's scope
# and is assigned to the engagement. Same outcome as approving a device code in
# the portal, minus the code — so both paths share these helpers.
# (MAX_LIVE_ENGAGEMENT_TOKENS, ENGAGEMENT_TOKEN_TTL_MINUTES and
# INSTALL_TOKEN_LIFETIMES are defined near the top, before EnrollTokenCreate.)


def engagement_site(engagement: Engagement, tenant_id: uuid.UUID, request_row: ProbeEnrollmentRequest) -> ProbeSite:
    """The Site an agent gets when it is enrolled for an engagement: the
    engagement's scope and exclusions as they are at enrolment time, and exactly
    the capabilities the device reported (so the provisioning subset-check holds)."""
    return ProbeSite(
        tenant_id=tenant_id,
        name=f"engagement-{str(engagement.id)[:8]}-{str(request_row.id)[:8]}",
        status="active",
        authorized_cidrs=list(engagement.scope_cidrs or []),
        excluded_cidrs=list(engagement.excluded_cidrs or []),
        approved_capabilities=list(dict.fromkeys(request_row.reported_capabilities or [])),
    )


def engagement_enrollment_blocker(engagement: Engagement | None) -> str | None:
    """Why an engagement cannot take a new agent right now; None when it can."""
    if engagement is None:
        return "Engagement not found"
    if engagement.assigned_agent_id is not None:
        return "This engagement already has an assigned vedha-agent"
    if not list(engagement.scope_cidrs or []):
        return "Add an authorized engagement scope before enrolling a vedha-agent"
    return None


def _live_token_filter(now: datetime):
    return (
        ProbeEnrollmentToken.revoked_at.is_(None),
        ProbeEnrollmentToken.expires_at > now,
        ProbeEnrollmentToken.uses < ProbeEnrollmentToken.max_uses,
    )


async def issue_engagement_token(
    db,
    *,
    tenant_id: uuid.UUID,
    engagement: Engagement | None,
    name: str,
    created_by: str,
    now: datetime,
    expires_in_minutes: int = ENGAGEMENT_TOKEN_TTL_MINUTES,
) -> tuple[ProbeEnrollmentToken, str]:
    """Create a single-use install token for an engagement. Returns (row, raw);
    the raw token is shown once and only its hash is stored."""
    blocker = engagement_enrollment_blocker(engagement)
    if blocker is not None:
        raise HTTPException(404 if engagement is None else 409, blocker)
    live = (await db.execute(
        select(ProbeEnrollmentToken.id).where(
            ProbeEnrollmentToken.engagement_id == engagement.id, *_live_token_filter(now),
        )
    )).scalars().all()
    if len(live) >= MAX_LIVE_ENGAGEMENT_TOKENS:
        raise HTTPException(
            409,
            f"{len(live)} install commands are still unused — revoke one before creating another",
        )
    raw, token_hash, token_prefix = generate_enroll_token()
    token = ProbeEnrollmentToken(
        tenant_id=tenant_id,
        engagement_id=engagement.id,
        site_id=None,
        name=name.strip() or "vedha-agent",
        token_hash=token_hash,
        token_prefix=token_prefix,
        max_uses=1,
        expires_at=now + timedelta(minutes=expires_in_minutes),
        created_by=created_by,
    )
    db.add(token)
    await db.flush()
    record_audit(
        db,
        actor_id=created_by,
        action="probe.enrollment_token.created",
        engagement_id=engagement.id,
        resource_type="probe_enrollment_token",
        resource_id=token.id,
        detail={"engagement_id": str(engagement.id), "max_uses": 1,
                "expires_at": token.expires_at.isoformat()},
    )
    return token, raw


def token_out(row: ProbeEnrollmentToken, now: datetime) -> dict:
    """A token as Fleet lists it — never the raw value or its hash."""
    if row.revoked_at is not None:
        state = "revoked"
    elif row.uses >= row.max_uses:
        state = "used"
    elif row.expires_at <= now:
        state = "expired"
    else:
        state = "active"
    return {
        "id": str(row.id),
        "name": row.name,
        "token_prefix": row.token_prefix,
        "site_id": str(row.site_id) if row.site_id else None,
        "engagement_id": str(row.engagement_id) if row.engagement_id else None,
        "max_uses": row.max_uses,
        "uses": row.uses,
        "created_at": row.created_at.isoformat() if getattr(row, "created_at", None) else None,
        "expires_at": row.expires_at.isoformat(),
        "last_used_at": row.last_used_at.isoformat() if row.last_used_at else None,
        "revoked_at": row.revoked_at.isoformat() if row.revoked_at else None,
        "usable": enroll_token_is_usable(row, now),
        "state": state,
    }


# ── Trust-on-first-use auto-enrollment (single-owner fleets) ─────────────────
_AUTO_ENROLL_SITE_NAME = "auto-enroll"


def auto_enroll_cidrs() -> list[str]:
    """Parse settings.probe_auto_enroll_cidrs → a non-empty CIDR list (RFC1918
    default). Pure; unit-testable."""
    raw = get_settings().probe_auto_enroll_cidrs or ""
    cidrs = [c.strip() for c in raw.split(",") if c.strip()]
    return cidrs or ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]


async def _get_or_create_auto_enroll_site(db, reported_capabilities: list[str], now):
    """The singleton per-tenant Site that trust-on-first-use enrollment binds to.

    Bound to the first (single-owner) tenant. Its approved_capabilities are set to
    the enrolling probe's OWN reported set, so the provision subset-check always
    passes and each probe is granted exactly what it advertises. Returns None if
    no tenant exists yet (fresh DB before the admin seed runs) — the caller then
    falls back to the normal manual-approval path.
    """
    tenant = (await db.execute(
        select(Tenant).where(Tenant.is_active.is_(True)).order_by(Tenant.created_at).limit(1)
    )).scalar_one_or_none()
    if tenant is None:
        return None
    caps = list(dict.fromkeys(reported_capabilities))
    site = (await db.execute(
        select(ProbeSite).where(
            ProbeSite.tenant_id == tenant.id,
            ProbeSite.name == _AUTO_ENROLL_SITE_NAME,
            ProbeSite.status == "active",
        )
    )).scalar_one_or_none()
    if site is None:
        site = ProbeSite(
            tenant_id=tenant.id,
            name=_AUTO_ENROLL_SITE_NAME,
            status="active",
            authorized_cidrs=auto_enroll_cidrs(),
            approved_capabilities=caps,
        )
        db.add(site)
        await db.flush()
    else:
        # grant exactly this probe's reported capabilities (keeps subset-check valid
        # across mixed builds); agents snapshot caps at provision time.
        site.approved_capabilities = caps
    return site


@router.post("/requests", status_code=status.HTTP_201_CREATED)
async def create_enrollment_request(
    body: EnrollmentCreate,
    request: Request,
    db: DB,
    redis: RedisConn,
):
    await _rate_limit(redis, request, "create", 10)
    now = datetime.now(timezone.utc)
    signing_raw = _decode_public_key(body.signing_public_key, "signing_public_key")
    fingerprint = hashlib.sha256(signing_raw).hexdigest()
    existing_agent = (await db.execute(
        select(Agent).where(Agent.signing_key_fingerprint == fingerprint)
    )).scalar_one_or_none()
    if existing_agent is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "This device key is already enrolled")

    device_secret = secrets.token_urlsafe(32)
    raw_code = "".join(secrets.choice(_CODE_ALPHABET) for _ in range(8))
    user_code = f"{raw_code[:4]}-{raw_code[4:]}"
    row = ProbeEnrollmentRequest(
        state="awaiting_approval",
        device_secret_hash=_secret_hash(device_secret),
        user_code_hash=_keyed_hash(raw_code),
        signing_public_key=body.signing_public_key,
        encryption_public_key=body.encryption_public_key,
        signing_key_fingerprint=fingerprint,
        nonce=body.nonce,
        hostname_hint=body.hostname_hint,
        platform=body.platform,
        architecture=body.architecture,
        agent_version=body.agent_version,
        installer_version=body.installer_version,
        build_digest=body.build_digest,
        reported_capabilities=list(dict.fromkeys(body.capabilities)),
        source_ip=request.client.host if request.client else None,
        expires_at=now + timedelta(minutes=15),
    )
    db.add(row)
    await db.flush()

    # Pre-authorized, Site-bound token → auto-approve (no operator user_code
    # step). An invalid/expired/revoked/exhausted token degrades gracefully to
    # the manual approval path rather than failing the install.
    auto_approved = False
    if body.enroll_token:
        token = (await db.execute(
            select(ProbeEnrollmentToken)
            .where(ProbeEnrollmentToken.token_hash == _secret_hash(body.enroll_token))
            .with_for_update()
        )).scalar_one_or_none()
        if enroll_token_is_usable(token, now):
            site = None
            engagement = None
            if token.engagement_id is not None:
                # Engagement token: build the Site from the engagement's scope as
                # it is NOW and assign the agent to it. If the engagement can no
                # longer take an agent, degrade to manual approval (never widen).
                engagement = (await db.execute(
                    select(Engagement).where(
                        Engagement.id == token.engagement_id,
                        Engagement.tenant_id == token.tenant_id,
                    ).with_for_update()
                )).scalar_one_or_none()
                blocker = engagement_enrollment_blocker(engagement)
                if blocker is None and row.reported_capabilities:
                    site = engagement_site(engagement, token.tenant_id, row)
                    db.add(site)
                    await db.flush()
                else:
                    logger.warning(
                        "probe_enrollment.engagement_token_degraded",
                        token_id=str(token.id),
                        reason=blocker or "device reported no capabilities",
                    )
            elif token.site_id is not None:
                site = (await db.execute(
                    select(ProbeSite).where(
                        ProbeSite.id == token.site_id,
                        ProbeSite.tenant_id == token.tenant_id,
                        ProbeSite.status == "active",
                    )
                )).scalar_one_or_none()
            if site is not None:
                base_name = (row.hostname_hint or "probe").strip() or "probe"
                probe_name = f"{base_name}-{fingerprint[:8]}"
                agent = await _provision_agent_for_site(
                    db,
                    row=row,
                    site=site,
                    tenant_id=token.tenant_id,
                    probe_name=probe_name,
                    location=None,
                    approved_by=f"enroll-token:{token.id}",
                    now=now,
                    auto=True,
                )
                token.uses += 1
                token.last_used_at = now
                auto_approved = True
                if engagement is not None:
                    engagement.assigned_agent_id = agent.id
                    record_audit(
                        db,
                        actor_id=f"enroll-token:{token.id}",
                        action="portal.agent.assigned",
                        engagement_id=engagement.id,
                        resource_type="agent",
                        resource_id=agent.id,
                        detail={"origin": "enroll-token", "token_id": str(token.id),
                                "site_id": str(site.id)},
                    )

    # Trust-on-first-use: no token, but the operator has opted the whole Manager
    # into auto-enroll (settings.probe_auto_enroll, single-owner fleets). The
    # probe's device key is its id; we issue a token with no operator action.
    # Audited via _provision_agent_for_site (action=probe.enrollment.approved,
    # approved_by="auto-enroll"). Falls through to manual approval if disabled or
    # no tenant exists yet.
    if not auto_approved and get_settings().probe_auto_enroll:
        site = await _get_or_create_auto_enroll_site(db, row.reported_capabilities, now)
        if site is not None:
            base_name = (row.hostname_hint or "probe").strip() or "probe"
            probe_name = f"{base_name}-{fingerprint[:8]}"
            await _provision_agent_for_site(
                db,
                row=row,
                site=site,
                tenant_id=site.tenant_id,
                probe_name=probe_name,
                location=None,
                approved_by="auto-enroll",
                now=now,
                auto=True,
            )
            auto_approved = True

    # Commit BEFORE answering. get_db commits in dependency teardown, which this
    # FastAPI runs after the response is sent; an auto-approved device polls
    # straight away, can reach the other worker first, get 404 for its own
    # request, and spend its single-use install token on nothing.
    await db.commit()
    response: dict = {
        "request_id": str(row.id),
        "device_secret": device_secret,
        "poll_interval_seconds": 5,
        "expires_at": row.expires_at.isoformat(),
        "state": row.state,
    }
    if auto_approved:
        response["activation_challenge"] = row.activation_challenge
        response["agent_id"] = str(row.agent_id)
    else:
        response["user_code"] = user_code
        response["verification_path"] = "/fleet/enroll"
    return response


async def _authenticated_request(db, request_id: uuid.UUID, device_secret: str, *, lock: bool = False):
    query = select(ProbeEnrollmentRequest).where(ProbeEnrollmentRequest.id == request_id)
    if lock:
        query = query.with_for_update()
    row = (await db.execute(query)).scalar_one_or_none()
    if row is None or not hmac.compare_digest(row.device_secret_hash, _secret_hash(device_secret)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Enrollment request not found")
    now = datetime.now(timezone.utc)
    if row.expires_at <= now and row.state not in {"active", "denied"}:
        row.state = "expired"
    return row


@router.post("/requests/{request_id}/poll")
async def poll_enrollment(request_id: uuid.UUID, body: EnrollmentSecret, request: Request, db: DB, redis: RedisConn):
    await _rate_limit(redis, request, "poll", 120)
    row = await _authenticated_request(db, request_id, body.device_secret, lock=True)
    row.poll_count += 1
    response = {"state": row.state, "poll_interval_seconds": 5}
    if row.state in {"approved", "active"}:
        response.update({"activation_challenge": row.activation_challenge, "agent_id": str(row.agent_id)})
    if row.state == "denied":
        response["reason"] = row.denied_reason or "Denied by administrator"
    return response


@router.get("/requests")
async def list_enrollment_requests(
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    rows = (await db.execute(
        select(ProbeEnrollmentRequest)
        .where(
            (ProbeEnrollmentRequest.tenant_id == current_user.tenant_id)
            | (ProbeEnrollmentRequest.tenant_id.is_(None)),
            ProbeEnrollmentRequest.state.in_(["awaiting_approval", "approved"]),
        )
        .order_by(ProbeEnrollmentRequest.created_at)
    )).scalars().all()
    return [{
        "request_id": str(row.id),
        "state": row.state,
        "hostname_hint": row.hostname_hint,
        "platform": row.platform,
        "architecture": row.architecture,
        "agent_version": row.agent_version,
        "capabilities": row.reported_capabilities,
        "fingerprint": row.signing_key_fingerprint,
        "expires_at": row.expires_at.isoformat(),
    } for row in rows]


class SimpleApproveInput(BaseModel):
    """One-click "Approve Site": every field is an OPTIONAL override — left blank,
    the name auto-assigns (vedha_agent_NN), capabilities default to exactly what the
    vedha-agent reported, and scope defaults to the auto-enroll CIDRs. No user_code —
    the operator approves a pending request straight from the fleet list."""
    probe_name: str | None = Field(default=None, max_length=255)
    authorized_cidrs: list[str] | None = None
    excluded_cidrs: list[str] = Field(default_factory=list)
    approved_capabilities: list[str] | None = None

    @field_validator("authorized_cidrs", "excluded_cidrs")
    @classmethod
    def _validate_networks(cls, values: list[str] | None) -> list[str] | None:
        return validate_scope_entries(values) if values else values


async def _next_probe_name(db, tenant_id: uuid.UUID) -> str:
    """Auto-assign the next sequential vedha-agent name (vedha_agent_01, _02, …) so
    the operator never has to invent one. Scoped per tenant; gaps are not reused.
    Legacy vedha_probe_NN names are still counted so numbering stays monotonic
    across the probe→vedha-agent rename (no collisions on existing deployments)."""
    names = (await db.execute(
        select(Agent.name).where(Agent.tenant_id == tenant_id)
    )).scalars().all()
    highest = 0
    for name in names:
        for prefix in ("vedha_agent_", "vedha_probe_"):
            if name and name.startswith(prefix):
                suffix = name[len(prefix):]
                if suffix.isdigit():
                    highest = max(highest, int(suffix))
                break
    return f"vedha_agent_{highest + 1:02d}"


@router.post("/requests/{request_id}/approve",
             summary="One-click approve a pending probe (auto-fills name/caps/scope)")
async def approve_request_simple(
    request_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
    body: SimpleApproveInput | None = None,
):
    body = body or SimpleApproveInput()
    now = datetime.now(timezone.utc)
    row = (await db.execute(
        select(ProbeEnrollmentRequest)
        .where(ProbeEnrollmentRequest.id == request_id)
        .with_for_update()
    )).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "Enrollment request not found")
    if row.expires_at <= now:
        row.state = "expired"
        raise HTTPException(410, "Enrollment request expired")
    if row.state != "awaiting_approval":
        raise HTTPException(409, f"Enrollment request is already {row.state}")

    # Auto-fill everything the operator would otherwise type; blanks fall back to
    # the device's own reported data so the subset-check in _provision always passes.
    caps = body.approved_capabilities or list(dict.fromkeys(row.reported_capabilities or []))
    cidrs = body.authorized_cidrs or auto_enroll_cidrs()
    name = (body.probe_name or "").strip() or await _next_probe_name(db, current_user.tenant_id)

    site = ProbeSite(
        tenant_id=current_user.tenant_id,
        name=f"{name}-site",
        status="active",
        authorized_cidrs=cidrs,
        excluded_cidrs=body.excluded_cidrs,
        approved_capabilities=caps,
    )
    db.add(site)
    await db.flush()

    agent = await _provision_agent_for_site(
        db, row=row, site=site, tenant_id=current_user.tenant_id,
        probe_name=name, location=None, approved_by=str(current_user.user_id),
        now=now, auto=False,
    )
    return {"request_id": str(row.id), "agent_id": str(agent.id),
            "site_id": str(site.id), "state": row.state, "probe_name": name}


@router.post("/approve")
async def approve_enrollment(
    body: SitePolicyInput,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    code = body.user_code.replace("-", "").upper()
    row = (await db.execute(
        select(ProbeEnrollmentRequest)
        .where(ProbeEnrollmentRequest.user_code_hash == _keyed_hash(code))
        .with_for_update()
    )).scalar_one_or_none()
    now = datetime.now(timezone.utc)
    if row is None:
        raise HTTPException(404, "Enrollment code not found")
    if row.expires_at <= now:
        row.state = "expired"
        raise HTTPException(410, "Enrollment code expired")
    if row.state != "awaiting_approval":
        raise HTTPException(409, f"Enrollment request is already {row.state}")

    if body.site_id:
        site = (await db.execute(
            select(ProbeSite).where(
                ProbeSite.id == body.site_id,
                ProbeSite.tenant_id == current_user.tenant_id,
                ProbeSite.status == "active",
            )
        )).scalar_one_or_none()
        if site is None:
            raise HTTPException(404, "Site not found")
    else:
        existing_site = (await db.execute(
            select(ProbeSite).where(
                ProbeSite.tenant_id == current_user.tenant_id,
                ProbeSite.name == body.site_name.strip(),
            )
        )).scalar_one_or_none()
        if existing_site is not None:
            raise HTTPException(409, "A Site with this name already exists in the tenant")
        site = ProbeSite(
            tenant_id=current_user.tenant_id,
            name=body.site_name.strip(),
            location=body.location,
            authorized_cidrs=body.authorized_cidrs,
            excluded_cidrs=body.excluded_cidrs,
            approved_capabilities=body.approved_capabilities,
            max_targets=body.max_targets,
            max_job_seconds=body.max_job_seconds,
            max_rate_pps=body.max_rate_pps,
            update_channel=body.update_channel,
        )
        db.add(site)
        await db.flush()

    agent = await _provision_agent_for_site(
        db,
        row=row,
        site=site,
        tenant_id=current_user.tenant_id,
        probe_name=body.probe_name,
        location=body.location,
        approved_by=str(current_user.user_id),
        now=now,
        auto=False,
    )
    return {"request_id": str(row.id), "agent_id": str(agent.id), "site_id": str(site.id), "state": row.state}


@router.post("/requests/{request_id}/activate")
async def activate_enrollment(request_id: uuid.UUID, body: EnrollmentActivate, request: Request, db: DB, redis: RedisConn):
    await _rate_limit(redis, request, "activate", 30)
    row = await _authenticated_request(db, request_id, body.device_secret, lock=True)
    if row.state not in {"approved", "active"} or not row.agent_id or not row.tenant_id or not row.site_id:
        raise HTTPException(409, f"Enrollment request is {row.state}")
    message = f"vedha-enrollment:{row.id}:{row.activation_challenge}"
    _verify_signature(row.signing_public_key, message, body.signature)
    agent = (await db.execute(select(Agent).where(Agent.id == row.agent_id).with_for_update())).scalar_one()
    site = (await db.execute(select(ProbeSite).where(ProbeSite.id == row.site_id))).scalar_one()
    refresh_secret = _derive_refresh_secret(row.id, body.device_secret)
    now = datetime.now(timezone.utc)
    if row.state == "approved":
        agent.credential_generation += 1
        agent.lifecycle_status = "active"
        credential = AgentCredential(
            agent_id=agent.id,
            generation=agent.credential_generation,
            refresh_secret_hash=_secret_hash(refresh_secret),
            signing_public_key=row.signing_public_key,
            signing_key_fingerprint=row.signing_key_fingerprint,
            issued_at=now,
            expires_at=now + timedelta(days=90),
        )
        db.add(credential)
        row.state = "active"
        row.activated_at = now
        row.version += 1
    token = create_device_access_token(str(agent.id), str(agent.tenant_id), agent.credential_generation)
    policy = _policy(site)
    # The device uses this credential immediately; the middleware rejects it
    # unless the agent row already reads lifecycle_status=active. Commit first
    # (see create_enrollment_request).
    await db.commit()
    return {
        "state": "active",
        "agent_id": str(agent.id),
        "access_token": token,
        "access_expires_in_seconds": 600,
        "refresh_secret": refresh_secret,
        "credential_generation": agent.credential_generation,
        "policy": policy,
    }


@router.post("/token")
async def refresh_device_token(body: TokenRefresh, request: Request, db: DB, redis: RedisConn):
    await _rate_limit(redis, request, "token", 120)
    now = datetime.now(timezone.utc)
    credential = (await db.execute(
        select(AgentCredential).where(
            AgentCredential.agent_id == body.agent_id,
            AgentCredential.generation == body.generation,
        ).with_for_update()
    )).scalar_one_or_none()
    if (
        credential is None
        or credential.revoked_at is not None
        or credential.expires_at <= now
        or not hmac.compare_digest(credential.refresh_secret_hash, _secret_hash(body.refresh_secret))
    ):
        raise HTTPException(401, "Invalid, expired, or revoked device credential")
    message = f"vedha-refresh:{body.agent_id}:{body.generation}:{body.nonce}"
    _verify_signature(credential.signing_public_key, message, body.signature)
    agent = (await db.execute(select(Agent).where(Agent.id == body.agent_id))).scalar_one_or_none()
    if agent is None or agent.lifecycle_status != "active" or agent.credential_generation != body.generation:
        raise HTTPException(401, "Device is disabled, revoked, or on a newer credential generation")
    # Access expiry (set in Fleet): refuse to mint a fresh access token past it, so
    # an expired agent cannot keep working even though its refresh secret is valid.
    if is_expired(agent.access_expires_at, now):
        raise HTTPException(403, EXPIRED_MESSAGE)
    # A single last_nonce column only prevents immediate replay (A,A), not
    # non-consecutive replay (A,B,A). Redis tracks every accepted nonce for the
    # access/refresh window and fails closed if replay protection is unavailable.
    replay_key = (
        f"probe-enrollment:refresh-nonce:{body.agent_id}:"
        f"{body.generation}:{_secret_hash(body.nonce)}"
    )
    try:
        first_use = await redis.set(replay_key, "1", ex=900, nx=True)
    except Exception as exc:
        logger.error("probe_enrollment.replay_store_unavailable", error=str(exc))
        raise HTTPException(503, "Device replay protection unavailable") from exc
    if not first_use:
        raise HTTPException(409, "Device refresh nonce was already used")
    credential.last_nonce = body.nonce
    credential.last_used_at = now
    return {
        "access_token": create_device_access_token(str(agent.id), str(agent.tenant_id), body.generation),
        "access_expires_in_seconds": 600,
    }


# ── Pre-authorized enrollment token management (operator, admin/manager) ─────

@router.post("/enroll-tokens", status_code=status.HTTP_201_CREATED)
async def create_enroll_token(
    body: EnrollTokenCreate,
    request: Request,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    from app.routers.agent_distribution import install_commands, manager_url_for

    now = datetime.now(timezone.utc)
    if body.engagement_id is not None:
        engagement = (await db.execute(
            select(Engagement).where(
                Engagement.id == body.engagement_id,
                Engagement.tenant_id == current_user.tenant_id,
            ).with_for_update()
        )).scalar_one_or_none()
        token, raw = await issue_engagement_token(
            db,
            tenant_id=current_user.tenant_id,
            engagement=engagement,
            name=body.name,
            created_by=str(current_user.user_id),
            now=now,
            expires_in_minutes=body.expires_in_minutes,
        )
    else:
        site = (await db.execute(
            select(ProbeSite).where(
                ProbeSite.id == body.site_id,
                ProbeSite.tenant_id == current_user.tenant_id,
                ProbeSite.status == "active",
            )
        )).scalar_one_or_none()
        if site is None:
            raise HTTPException(404, "Site not found")

        raw, token_hash, token_prefix = generate_enroll_token()
        token = ProbeEnrollmentToken(
            tenant_id=current_user.tenant_id,
            site_id=site.id,
            name=body.name.strip(),
            token_hash=token_hash,
            token_prefix=token_prefix,
            max_uses=body.max_uses,
            expires_at=now + timedelta(minutes=body.expires_in_minutes),
            created_by=str(current_user.user_id),
        )
        db.add(token)
        await db.flush()
        db.add(AuditLog(
            actor_id=str(current_user.user_id),
            action="probe.enrollment_token.created",
            resource_type="probe_enrollment_token",
            resource_id=token.id,
            detail={"site_id": str(site.id), "max_uses": token.max_uses},
            timestamp=now,
        ))
    manager_url, _ = manager_url_for(request)
    out = {**token_out(token, now), "token": raw, "commands": install_commands(manager_url, raw)}
    await db.commit()  # Fleet lists tokens right after creating one; raw token shown once
    return out


@router.get("/enroll-tokens")
async def list_enroll_tokens(
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
    engagement_id: uuid.UUID | None = None,
):
    query = (
        select(ProbeEnrollmentToken)
        .where(ProbeEnrollmentToken.tenant_id == current_user.tenant_id)
        .order_by(ProbeEnrollmentToken.created_at.desc())
        .limit(200)
    )
    if engagement_id is not None:
        query = query.where(ProbeEnrollmentToken.engagement_id == engagement_id)
    rows = (await db.execute(query)).scalars().all()
    now = datetime.now(timezone.utc)
    return [token_out(row, now) for row in rows]


@router.delete("/enroll-tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_enroll_token(
    token_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    row = (await db.execute(
        select(ProbeEnrollmentToken).where(
            ProbeEnrollmentToken.id == token_id,
            ProbeEnrollmentToken.tenant_id == current_user.tenant_id,
        ).with_for_update()
    )).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "Enrollment token not found")
    if row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        db.add(AuditLog(
            actor_id=str(current_user.user_id),
            action="probe.enrollment_token.revoked",
            resource_type="probe_enrollment_token",
            resource_id=row.id,
            detail={"site_id": str(row.site_id) if row.site_id else None,
                    "engagement_id": str(row.engagement_id) if row.engagement_id else None},
            timestamp=row.revoked_at,
        ))
    return None
