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
from app.models.audit_log import AuditLog
from app.models.probe_enrollment import AgentCredential, ProbeEnrollmentRequest
from app.models.probe_site import ProbeSite
from app.schemas.engagement import validate_scope_entries

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
    source = request.client.host if request.client else "unknown"
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

    @field_validator("signing_public_key", "encryption_public_key")
    @classmethod
    def validate_key(cls, value: str, info):
        _decode_public_key(value, info.field_name)
        return value


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
    return {
        "request_id": str(row.id),
        "device_secret": device_secret,
        "user_code": user_code,
        "verification_path": "/fleet/enroll",
        "poll_interval_seconds": 5,
        "expires_at": row.expires_at.isoformat(),
    }


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
    duplicate_name = (await db.execute(
        select(Agent).where(
            Agent.tenant_id == current_user.tenant_id,
            Agent.name == body.probe_name.strip(),
        )
    )).scalar_one_or_none()
    if duplicate_name is not None:
        raise HTTPException(409, "A probe with this name already exists in the tenant")

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
        approved_capabilities = list(site.approved_capabilities or [])
        approved_networks = list(site.authorized_cidrs or [])
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
        approved_capabilities = list(body.approved_capabilities)
        approved_networks = list(body.authorized_cidrs)

    if not set(approved_capabilities).issubset(set(row.reported_capabilities)):
        raise HTTPException(422, "Site capabilities must be a subset of device-reported capabilities")

    agent = Agent(
        tenant_id=current_user.tenant_id,
        site_id=site.id,
        name=body.probe_name.strip(),
        location=body.location or site.location,
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
    row.tenant_id = current_user.tenant_id
    row.site_id = site.id
    row.agent_id = agent.id
    row.assigned_name = agent.name
    row.approved_by = str(current_user.user_id)
    row.approved_at = now
    row.activation_challenge = secrets.token_urlsafe(32)
    row.version += 1
    db.add(AuditLog(
        actor_id=str(current_user.user_id),
        action="probe.enrollment.approved",
        resource_type="agent",
        resource_id=agent.id,
        detail={"site_id": str(site.id), "request_id": str(row.id), "fingerprint": row.signing_key_fingerprint},
        timestamp=now,
    ))
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
    return {
        "state": "active",
        "agent_id": str(agent.id),
        "access_token": token,
        "access_expires_in_seconds": 600,
        "refresh_secret": refresh_secret,
        "credential_generation": agent.credential_generation,
        "policy": _policy(site),
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
