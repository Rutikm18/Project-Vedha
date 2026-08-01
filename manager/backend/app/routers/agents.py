"""
Agent registration, heartbeat, job polling, and result submission.
"""
import ipaddress
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token
from app.auth.rbac import require_role
from app.config import get_settings
from app.dependencies import DB, AuthUser
from app.discovery.finding_translator import create_findings_from_probe_result
from app.models.agent import Agent, AgentStatus
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import AssetType, ScanJobStatus, ScanJobType
from app.models.scan_job import ScanJob
from app.models.scan_result import ScanResult
from app.models.service import Service
from app.services.job_result_service import _promote_assets as _promote_assets

router = APIRouter(prefix="/agents", tags=["agents"])
logger = structlog.get_logger()

# Job types a remote probe may execute. Server-side background jobs (vuln_scan,
# ad_enum, detection, ai_report) are excluded so a polling probe can never steal
# and fail a job the API is already handling itself.
AGENT_EXECUTABLE_TYPES = (
    ScanJobType.discovery,
    ScanJobType.lateral,
    ScanJobType.cloud_scan,
)

# Default capability for the API's coarse job types. The resolved value is
# materialized into params at enqueue time so the independently deployed probe
# runs the same scan type the manager checked.
_DEFAULT_SCAN_FOR_JOBTYPE = {"discovery": "discovery", "lateral": "smb_enum", "cloud_scan": "vuln_scan"}

# Profiles that restrict which scan_type a job may resolve to, stored in an
# engagement's rules_of_engagement JSONB (same field critical_webhook_url
# already piggybacks on — see vuln/tasks.py). "ot" is PASSIVE ONLY, mirroring
# pipeline.py's PROFILES dict in the Agentic VA Scanner project: an
# unsolicited active probe to a PLC/RTU/safety controller can hang or reboot
# fragile control hardware. This is a HARD gate enforced at job-creation
# time, not a default an operator can override per job — same as
# pipeline.py's own structural (non-flag) OT block.
_OT_ALLOWED_SCAN_TYPES = {"passive_discovery"}

# Job parameters are persisted in ``scan_jobs.result`` while pending. Until a
# dedicated ephemeral secret broker exists, accepting credential material here
# would write it to Postgres in plaintext. Reject it at the Manager boundary
# instead of relying on response redaction.
_JOB_SECRET_KEYS = {
    "api_key",
    "credential",
    "credentials",
    "password",
    "passwd",
    "private_key",
    "secret",
    "ssh_creds",
    "token",
    "win_creds",
}


def _job_params_contain_secret(value) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in _JOB_SECRET_KEYS:
                return True
            if _job_params_contain_secret(nested):
                return True
        return False
    if isinstance(value, (list, tuple)):
        return any(_job_params_contain_secret(item) for item in value)
    return False


def _resolve_scan_type(job_type: str, params: dict) -> str:
    return params.get("scan_type") or _DEFAULT_SCAN_FOR_JOBTYPE.get(job_type, "discovery")


def _required_scan_type(job_type: ScanJobType | str, params: dict | None) -> str:
    """Resolve the capability a probe must advertise for a job."""
    job_type_value = job_type.value if hasattr(job_type, "value") else str(job_type)
    job_params = params or {}
    use_case_id = job_params.get("use_case_id")
    if use_case_id in _USE_CASES:
        return _USE_CASES[use_case_id]["scan_type"]
    return _resolve_scan_type(job_type_value, job_params)


def _scope_is_reachable(
    network_segments: list[str] | None,
    scope_cidrs: list[str] | None,
) -> bool:
    """Return whether a probe's declared networks fully cover a job's scope.

    A probe must explicitly declare its reachable CIDRs. Every requested scope
    network must be contained by one of them; overlap alone is not sufficient
    because it could dispatch a broader scan than the probe can safely reach.
    """
    if not network_segments:
        return False
    if not scope_cidrs:
        return False

    try:
        segments = [
            ipaddress.ip_network(str(value).strip(), strict=False)
            for value in network_segments
        ]
        scope = [
            ipaddress.ip_network(str(value).strip(), strict=False)
            for value in scope_cidrs
        ]
    except (ValueError, TypeError):
        return False

    return all(
        any(
            target.version == segment.version and target.subnet_of(segment)
            for segment in segments
        )
        for target in scope
    )


def _job_reachability_scope(
    params: dict | None,
    authoritative_scope: list[str] | None,
) -> list[str] | None:
    """Return the narrow IP scope needed to route this job.

    The engagement scope remains the execution allowlist. This helper only
    avoids requiring one probe to reach unrelated subnets when the operator
    requested a concrete IP/CIDR/range subset. Hostnames are rejected because
    engagements are IP/CIDR-only and Manager/Probe DNS could disagree.
    ``None`` means a requested target was invalid or outside authorization.
    """
    job_params = params or {}
    requested = job_params.get("targets")
    if requested is None:
        requested = job_params.get("target")
    if requested is None:
        return list(authoritative_scope or [])

    values = [requested] if isinstance(requested, str) else requested
    if not isinstance(values, (list, tuple)) or not values:
        return None

    try:
        allowed = [
            ipaddress.ip_network(str(value).strip(), strict=False)
            for value in (authoritative_scope or [])
        ]
    except (ValueError, TypeError):
        return None

    requested_networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
    try:
        for raw_value in values:
            if not isinstance(raw_value, str) or not raw_value.strip():
                return list(authoritative_scope or [])
            value = raw_value.strip()
            if "-" in value:
                start_raw, end_raw = (
                    part.strip() for part in value.split("-", 1)
                )
                start = ipaddress.ip_address(start_raw)
                end = ipaddress.ip_address(end_raw)
                if start.version != end.version or int(start) > int(end):
                    return None
                requested_networks.extend(
                    ipaddress.summarize_address_range(start, end)
                )
            else:
                requested_networks.append(
                    ipaddress.ip_network(value, strict=False)
                )
    except (ValueError, TypeError):
        return None

    if allowed and not all(
        any(
            target.version == scope.version and target.subnet_of(scope)
            for scope in allowed
        )
        for target in requested_networks
    ):
        return None
    return [str(network) for network in requested_networks]


def _agent_can_execute_job(
    agent: Agent,
    job_type: ScanJobType | str,
    params: dict | None,
    scope_cidrs: list[str] | None,
) -> bool:
    """Apply capability and network reachability policy to one dispatch."""
    required_capability = _required_scan_type(job_type, params)
    capabilities = {str(value).strip() for value in (agent.capabilities or [])}
    if required_capability not in capabilities:
        return False
    dispatch_scope = _job_reachability_scope(params, scope_cidrs)
    if dispatch_scope is None:
        return False
    return _scope_is_reachable(agent.network_segments, dispatch_scope)


# ── Schemas ───────────────────────────────────────────────────────────────────

class AgentRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    location: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    network_segments: list[str] = Field(default_factory=list)
    public_key: str | None = None   # X25519 public key (base64) for scope encryption

    @field_validator("network_segments")
    @classmethod
    def validate_network_segments(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            try:
                network = str(ipaddress.ip_network(value.strip(), strict=False))
            except (ValueError, TypeError, AttributeError) as exc:
                raise ValueError(f"invalid probe network CIDR: {value!r}") from exc
            if network not in normalized:
                normalized.append(network)
        return normalized


class AgentRegisterResponse(BaseModel):
    agent_id: str
    token: str


class HeartbeatRequest(BaseModel):
    agent_id: str
    current_job_id: str | None = None
    status: str = "online"


class AgentRefreshRequest(BaseModel):
    capabilities: list[str] = Field(default_factory=list)
    network_segments: list[str] = Field(default_factory=list)
    public_key: str | None = None

    _validate_network_segments = field_validator("network_segments")(
        AgentRegisterRequest.validate_network_segments.__func__
    )


class JobResultRequest(BaseModel):
    success: bool
    result: dict = Field(default_factory=dict)
    error: str | None = None


class EnqueueJobRequest(BaseModel):
    engagement_id: uuid.UUID
    job_type: ScanJobType = ScanJobType.discovery
    params: dict = Field(default_factory=dict)
    use_case_id: str | None = None   # maps to probe's use-case library (techprompt §A3)


# ── Use-case library (mirrored from probe/agent/use_cases.py) ─────────────────
# Duplicated intentionally: manager and probe are separate deployable processes.
# The manager exposes this so the frontend can show the operator a picker;
# the probe enforces it at execution time — the operator cannot invent a new
# use_case_id that the probe will execute.

_USE_CASES = {
    "uc_discovery_only": {
        "display_name": "Network Discovery",
        "description": "Fast host-discovery + port scan only. Use for 'what's alive here?' triage.",
        "scan_type": "discovery",
        "profile": "it",
        "expected_runtime_hint": "2–5 min per /24",
    },
    "uc_full_assessment": {
        "display_name": "Full Assessment",
        "description": "Complete assessment: discovery → ports → banners → all service branches.",
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    "uc_external_web_triage": {
        "display_name": "External Web Triage",
        "description": "Web + TLS surface only. Fast check for exposed web services and cert facts.",
        "scan_type": "web_tls_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_db_exposure": {
        "display_name": "Database Exposure Check",
        "description": "Protocol-handshake fingerprint of database ports. Are any DBs exposed or unauthenticated?",
        "scan_type": "db_fingerprint",
        "profile": "it",
        "expected_runtime_hint": "3–10 min",
    },
    "uc_windows_estate": {
        "display_name": "Windows Estate",
        "description": "SMB dialect + signing detection. Is SMBv1 enabled? Is SMB signing required?",
        "scan_type": "smb_enum",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_ot_passive": {
        "display_name": "OT / ICS Passive Discovery",
        "description": "PASSIVE ONLY — zero active packets. Safe for OT/ICS/SCADA segments.",
        "scan_type": "passive_discovery",
        "profile": "ot",
        "expected_runtime_hint": "listen-only, duration set by operator",
    },
    "uc_ai_endpoint_sweep": {
        "display_name": "AI / MCP Endpoint Sweep",
        "description": "Discover exposed AI inference endpoints and MCP servers.",
        "scan_type": "mcp_discovery",
        "profile": "it",
        "expected_runtime_hint": "3–8 min",
    },
    "uc_rescan_delta": {
        "display_name": "Re-scan (delta from prior engagement)",
        "description": "Full re-assessment identical to uc_full_assessment. Manager diffs against prior run.",
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    # ── Real-world customer use-cases (mirrored from probe/agent/use_cases.py) ──
    "uc_iot_device_survey": {
        "display_name": "IoT / Embedded Device Survey",
        "description": (
            "Inventory IoT and embedded devices on the IoT port set: "
            "MQTT (1883/8883), RTSP (554), CoAP (5683), Telnet (23), printer/DVR ports. "
            "Discovery + service banner."
        ),
        "scan_type": "service_fingerprint",
        "profile": "iot",
        "expected_runtime_hint": "3–10 min per /24",
    },
    "uc_web_app_triage": {
        "display_name": "Web Application Triage",
        "description": (
            "Web-layer fingerprint: HTTP methods (OPTIONS), response headers, "
            "server tech stack, and security-header posture on all web ports "
            "(80, 443, 8080, 8443, 8000…). Use before a dedicated web app pentest."
        ),
        "scan_type": "web_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_udp_service_exposure": {
        "display_name": "UDP Service Exposure",
        "description": (
            "UDP attack surface + amplification checks: NTP monlist (123), "
            "DNS open recursion (53), Memcached (11211), SNMP public (161), "
            "NetBIOS-NS (137)."
        ),
        "scan_type": "udp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    "uc_snmp_exposure": {
        "display_name": "SNMP Exposure Check",
        "description": (
            "Read-only SNMP sysDescr checks using common community strings. "
            "Use to find default or weak read communities on routers, printers, "
            "switches, and monitoring appliances."
        ),
        "scan_type": "snmp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
}


async def _encrypt_scope_for_agent(db, agent_id: str, job_params: dict) -> str | None:
    """Encrypt the engagement scope for a specific agent's public key.

    Reads agent.public_key from the DB. Returns None if the agent has no
    public key (scope is sent in the clear inside the TLS tunnel).
    """
    scope_cidrs = job_params.get("_scope_cidrs") or job_params.get("scope_cidrs") or []
    excluded_cidrs = job_params.get("_excluded_cidrs") or []
    engagement_id = job_params.get("engagement_id", "")

    if not scope_cidrs:
        return None  # nothing to encrypt

    agent = (await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )).scalar_one_or_none()

    if not agent or not agent.public_key:
        return None  # agent hasn't registered a public key yet

    from app.services.scope_crypto import public_key_from_b64, encrypt_scope_b64

    pk_bytes = public_key_from_b64(agent.public_key)
    if not pk_bytes:
        return None

    scope_dict = {
        "scope_cidrs": list(scope_cidrs),
        "excluded_cidrs": list(excluded_cidrs),
        "engagement_id": engagement_id,
    }
    try:
        return encrypt_scope_b64(scope_dict, pk_bytes)
    except Exception as exc:
        logger.warning("scope_crypto.encrypt_failed", agent_id=agent_id, error=str(exc))
        return None


def _agent_ownership_check(request: Request, agent_id_str: str) -> None:
    """Verify that the JWT token bearer IS the agent they claim to be.

    Every heartbeat, job poll, and result submission must pass this check.
    Prevents a compromised low-privilege JWT from impersonating another agent.
    """
    token_sub = getattr(request.state, "user_id", None)
    if token_sub is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if str(token_sub) != str(agent_id_str):
        raise HTTPException(
            status_code=403,
            detail="Token subject does not match the requested agent_id",
        )


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/use-cases", summary="List available pre-defined scan use-cases (probe action library)")
async def list_use_cases(current_user: AuthUser):
    """Returns the finite library of scan use-cases operators can dispatch to probes.
    The probe enforces this list at execution time — an unknown use_case_id is
    rejected by the probe before any packet leaves the host."""
    return [{"use_case_id": uid, **meta} for uid, meta in _USE_CASES.items()]


@router.post(
    "/register",
    response_model=AgentRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Agent self-registers with platform, receives JWT",
)
async def register_agent(
    body: AgentRegisterRequest,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    # Idempotent registration: reuse an existing probe with the same name in this
    # tenant instead of creating a duplicate every time it restarts/re-registers.
    existing = (
        await db.execute(
            select(Agent)
            .where(Agent.tenant_id == current_user.tenant_id, Agent.name == body.name)
            .order_by(Agent.last_heartbeat.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    if existing is not None:
        agent = existing
        agent.location = body.location
        agent.capabilities = body.capabilities
        agent.network_segments = body.network_segments
        agent.status = AgentStatus.online
        agent.last_heartbeat = datetime.now(timezone.utc)
        # Phase 4: update public key if the probe sent one (re-registration)
        if body.public_key:
            agent.public_key = body.public_key
    else:
        agent = Agent(
            tenant_id=current_user.tenant_id,
            name=body.name,
            location=body.location,
            capabilities=body.capabilities,
            network_segments=body.network_segments,
            public_key=body.public_key,
            status=AgentStatus.online,
            last_heartbeat=datetime.now(timezone.utc),
        )
        db.add(agent)
    await db.flush()
    await db.refresh(agent)

    # Probes are long-running; issue a 1-year token so it doesn't lapse every 15 min
    # (which previously forced a re-register and spawned duplicate agent rows).
    token = create_access_token(
        subject=str(agent.id),
        tenant_id=str(current_user.tenant_id),
        role="agent",
        expires_minutes=60 * 24 * 365,
    )
    logger.info("agent.registered", agent_id=str(agent.id), name=body.name,
                reused=existing is not None)
    return AgentRegisterResponse(agent_id=str(agent.id), token=token)


@router.get("", summary="List registered agents/probes for the tenant")
async def list_agents(db: DB, current_user: AuthUser):
    rows = (await db.execute(
        select(Agent).where(Agent.tenant_id == current_user.tenant_id)
        .order_by(Agent.last_heartbeat.desc().nullslast())
    )).scalars().all()
    now = datetime.now(timezone.utc)
    out = []
    for a in rows:
        persisted_status = a.status.value if hasattr(a.status, "value") else str(a.status)
        heartbeat_fresh = bool(
            a.last_heartbeat and (now - a.last_heartbeat).total_seconds() < 90
        )
        # WebSocket disconnects explicitly persist "offline". A final recent
        # heartbeat must not keep a disconnected probe looking online.
        online = heartbeat_fresh and persisted_status in {
            AgentStatus.online.value,
            AgentStatus.busy.value,
        }
        out.append({
            "id": str(a.id),
            "name": a.name,
            "location": a.location,
            "status": persisted_status,
            "capabilities": a.capabilities,
            "network_segments": a.network_segments,
            "last_heartbeat": a.last_heartbeat.isoformat() if a.last_heartbeat else None,
            "current_job_id": str(a.current_job_id) if a.current_job_id else None,
            "online": online,
        })
    return out


@router.post("/heartbeat", summary="Agent sends health ping every 30s")
async def heartbeat(body: HeartbeatRequest, db: DB, request: Request):
    # Verify the agent sending the heartbeat owns this agent_id (auth gap fix)
    _agent_ownership_check(request, body.agent_id)

    agent_id = uuid.UUID(body.agent_id)
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(404, "Agent not found")

    now = datetime.now(timezone.utc)
    agent.last_heartbeat = now
    try:
        agent.status = AgentStatus(body.status)
    except ValueError:
        agent.status = AgentStatus.online
    if body.current_job_id:
        job_uuid = uuid.UUID(body.current_job_id)
        agent.current_job_id = job_uuid
        # Renew the lease on the job this probe is actively running, so the reaper
        # doesn't requeue live work. Scoped to (job, this agent, running) so a probe
        # can't extend a job it doesn't own or one already finished.
        await db.execute(
            update(ScanJob)
            .where(
                ScanJob.id == job_uuid,
                ScanJob.agent_id == body.agent_id,
                ScanJob.status == ScanJobStatus.running,
            )
            .values(lease_expires_at=now + timedelta(seconds=get_settings().job_lease_seconds))
        )

    await db.flush()
    return {"ok": True}


@router.post(
    "/{agent_id}/refresh",
    summary="Agent refreshes its own capability and routing metadata",
)
async def refresh_agent_registration(
    agent_id: uuid.UUID,
    body: AgentRefreshRequest,
    db: DB,
    request: Request,
):
    _agent_ownership_check(request, str(agent_id))
    agent = (await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )).scalar_one_or_none()
    if agent is None:
        raise HTTPException(410, "Agent registration no longer exists")

    agent.capabilities = body.capabilities
    agent.network_segments = body.network_segments
    if body.public_key:
        agent.public_key = body.public_key
    agent.status = AgentStatus.online
    agent.last_heartbeat = datetime.now(timezone.utc)
    await db.flush()
    logger.info(
        "agent.registration.refreshed",
        agent_id=str(agent_id),
        capability_count=len(body.capabilities),
        segment_count=len(body.network_segments),
    )
    return {"ok": True}


@router.get("/{agent_id}/jobs", summary="Agent polls for pending ScanJobs")
async def get_agent_jobs(
    agent_id: uuid.UUID,
    db: DB,
    request: Request = None,
    limit: int = 1,
):
    if request is not None:
        _agent_ownership_check(request, str(agent_id))

    result = await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(404, "Agent not found")

    # Tenant filtering happens in SQL so a probe can never observe another
    # tenant's job. Capability and reachability depend on JSON/ARRAY metadata and
    # are evaluated below before an atomic conditional UPDATE claims each row.
    candidate_result = await db.execute(
        select(ScanJob, Engagement)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(
            Engagement.tenant_id == agent.tenant_id,
            ScanJob.status == ScanJobStatus.pending,
            ScanJob.agent_id.is_(None),
            ScanJob.job_type.in_(AGENT_EXECUTABLE_TYPES),
        )
        .order_by(ScanJob.created_at)
    )
    candidates = candidate_result.all()

    # Conditional UPDATE is the claim primitive shared conceptually with the WS
    # path. Under concurrent pollers only one transaction can change a row that
    # is still pending and unassigned; losing pollers get rowcount == 0.
    claim_limit = max(0, min(int(limit), 100))
    now = datetime.now(timezone.utc)
    lease_until = now + timedelta(seconds=get_settings().job_lease_seconds)
    jobs: list[ScanJob] = []
    for job, engagement in candidates:
        if len(jobs) >= claim_limit:
            break
        params = job.result or {}
        if not _agent_can_execute_job(
            agent, job.job_type, params, engagement.scope_cidrs or [],
        ):
            continue

        claimed = (await db.execute(
            update(ScanJob)
            .where(
                ScanJob.id == job.id,
                ScanJob.status == ScanJobStatus.pending,
                ScanJob.agent_id.is_(None),
                ScanJob.engagement_id.in_(
                    select(Engagement.id).where(
                        Engagement.tenant_id == agent.tenant_id,
                    )
                ),
            )
            .values(
                agent_id=str(agent_id),
                status=ScanJobStatus.running,
                started_at=now,
                lease_expires_at=lease_until,
            )
            .execution_options(synchronize_session=False)
        )).rowcount
        if claimed:
            jobs.append(job)

    # Build response — Phase 4: encrypt scope for this specific agent
    response_jobs = []
    for j in jobs:
        params = j.result or {}
        encrypted_scope = await _encrypt_scope_for_agent(db, str(agent_id), params)
        job_dict = {
            "job_id": str(j.id),
            "engagement_id": str(j.engagement_id),
            "job_type": j.job_type.value,
            "status": ScanJobStatus.running.value,
            "params": params,
        }
        if encrypted_scope:
            job_dict["encrypted_scope"] = encrypted_scope
        response_jobs.append(job_dict)

    return response_jobs


@router.get("/jobs/{job_id}", summary="Get job status for frontend polling")
async def get_job_status(job_id: uuid.UUID, db: DB, current_user: AuthUser):
    """Lets the frontend poll a specific job's status without knowing which agent has it."""
    row = (await db.execute(
        select(ScanJob)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(ScanJob.id == job_id, Engagement.tenant_id == current_user.tenant_id)
    )).scalar_one_or_none()
    if not row:
        raise HTTPException(404, "Job not found")

    agent_name = None
    if row.agent_id:
        a = (await db.execute(
            select(Agent).where(Agent.id == uuid.UUID(str(row.agent_id)))
        )).scalar_one_or_none()
        agent_name = a.name if a else None

    # Echo the job's lean result to the frontend, but never the raw facts blob.
    # Secret-bearing params are rejected at enqueue; legacy rows are still
    # defensively redacted here.
    _REDACT = {"facts", "ssh_creds", "win_creds"}
    lean_result = None
    if row.result:
        lean_result = {k: v for k, v in row.result.items() if k not in _REDACT}

    return {
        "job_id": str(row.id),
        "engagement_id": str(row.engagement_id),
        "job_type": row.job_type.value,
        "status": row.status.value,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "started_at": row.started_at.isoformat() if row.started_at else None,
        "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        "agent_id": str(row.agent_id) if row.agent_id else None,
        "agent_name": agent_name,
        "use_case_id": (row.result or {}).get("use_case_id"),
        "result": lean_result,
    }


@router.post(
    "/jobs",
    status_code=status.HTTP_201_CREATED,
    summary="Enqueue an agent-executable scan job (discovery/lateral/cloud) for probes to pick up",
)
async def enqueue_agent_job(
    body: EnqueueJobRequest,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
):
    if body.job_type not in AGENT_EXECUTABLE_TYPES:
        raise HTTPException(
            400,
            f"job_type '{body.job_type.value}' is not agent-executable; "
            f"allowed: {[t.value for t in AGENT_EXECUTABLE_TYPES]}",
        )
    if _job_params_contain_secret(body.params):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Credential or secret material is not accepted in scan job params. "
            "Vedha does not persist target credentials; use unauthenticated "
            "collection until an ephemeral credential broker is configured.",
        )
    eng = (await db.execute(
        select(Engagement).where(
            Engagement.id == body.engagement_id,
            Engagement.tenant_id == current_user.tenant_id,
        )
    )).scalar_one_or_none()
    if not eng:
        raise HTTPException(404, "Engagement not found")

    requested_scope = _job_reachability_scope(
        body.params,
        getattr(eng, "scope_cidrs", None) or [],
    )
    if requested_scope is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "targets must be non-empty IP/CIDR/range values fully contained "
            "inside the engagement scope",
        )

    # Validate use_case_id against the known library if provided
    if body.use_case_id and body.use_case_id not in _USE_CASES:
        raise HTTPException(
            400,
            f"Unknown use_case_id '{body.use_case_id}'. "
            f"Call GET /agents/use-cases to see the available use-cases.",
        )

    scan_profile = (eng.rules_of_engagement or {}).get("scan_profile", "it")

    # When a use_case_id is given, resolve the scan_type from the library so
    # OT-profile enforcement can check it.
    if body.use_case_id:
        resolved_scan_type = _USE_CASES[body.use_case_id]["scan_type"]
    else:
        resolved_scan_type = _resolve_scan_type(body.job_type.value, body.params)

    if scan_profile == "ot" and resolved_scan_type not in _OT_ALLOWED_SCAN_TYPES:
        raise HTTPException(
            400,
            f"engagement scan_profile is 'ot' (OT/ICS — passive only); "
            f"scan_type '{resolved_scan_type}' is active and is structurally "
            f"blocked, not just discouraged. Only {sorted(_OT_ALLOWED_SCAN_TYPES)} "
            f"is allowed on this engagement — change rules_of_engagement.scan_profile "
            f"if this is not actually an OT/ICS segment.",
        )

    # Merge use_case_id into params so the probe can read it from the job payload.
    # Also embed the engagement's scope so the probe has it without a second round-trip
    # (the probe still independently fetches /scope for re-validation — this is
    # belt-AND-suspenders: params scope is the fast path, /scope fetch is the guard).
    job_params = {**body.params}
    if body.use_case_id:
        job_params["use_case_id"] = body.use_case_id
    # Materialize the manager's resolved capability into the wire payload. This
    # keeps direct lateral/cloud jobs aligned with the probe's params-first
    # resolver instead of making the scheduler and runner infer different types.
    job_params.setdefault("scan_type", resolved_scan_type)
    # Scope comes only from the tenant-owned engagement. Never honor caller
    # overrides for these fields: they also feed per-agent scope encryption.
    job_params.pop("scope_cidrs", None)
    job_params.pop("_scope_cidrs", None)
    if eng.scope_cidrs:
        job_params["scope_cidrs"] = list(eng.scope_cidrs)
        job_params["_scope_cidrs"] = list(eng.scope_cidrs)
    excluded_cidrs = getattr(eng, "excluded_cidrs", None) or []
    job_params.pop("_excluded_cidrs", None)
    if excluded_cidrs:
        job_params["_excluded_cidrs"] = list(excluded_cidrs)

    job = ScanJob(
        engagement_id=body.engagement_id,
        job_type=body.job_type,
        status=ScanJobStatus.pending,
        result=job_params,  # params travel in `result` until the probe overwrites it
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)
    logger.info("agent.job.enqueued", job_id=str(job.id), job_type=body.job_type.value,
                use_case_id=body.use_case_id)

    # ── P2: Push job to connected agents via WebSocket ───────────────────────
    # If no compatible agent is connected, the committed job stays pending and
    # will be picked up through the same eligibility checks in HTTP polling.
    from app.websocket.manager import agent_ws_manager
    job_payload = {
        "job_id": str(job.id),
        "engagement_id": str(job.engagement_id),
        "job_type": job.job_type.value,
        "params": job_params,
    }
    # Phase 4: try to push to the first compatible online agent in this tenant.
    # Legacy probes that do not advertise the claim-confirmation feature stay on
    # HTTP polling, where reservation already happens before the job is returned.
    # Build a fresh payload PER agent — encrypted_scope is per-agent (different
    # public key for each), so mutating a shared dict would leak one agent's
    # encrypted scope to the next agent in the loop.
    online_agent_ids = agent_ws_manager.online_agents_for_tenant(
        str(current_user.tenant_id),
        required_feature="atomic_job_claim_v1",
    )
    online_agents: dict[str, Agent] = {}
    if online_agent_ids:
        valid_agent_ids = []
        for connected_agent_id in online_agent_ids:
            try:
                valid_agent_ids.append(uuid.UUID(connected_agent_id))
            except (ValueError, TypeError, AttributeError):
                logger.warning(
                    "agent.ws.invalid_connected_agent_id",
                    agent_id=connected_agent_id,
                )
        if valid_agent_ids:
            rows = (await db.execute(
                select(Agent).where(
                    Agent.id.in_(valid_agent_ids),
                    Agent.tenant_id == current_user.tenant_id,
                )
            )).scalars().all()
            online_agents = {str(candidate.id): candidate for candidate in rows}

    eligible_online_agent_ids = []
    for agent_id in online_agent_ids:
        candidate = online_agents.get(agent_id)
        if candidate is not None and _agent_can_execute_job(
            candidate, job.job_type, job_params, eng.scope_cidrs or [],
        ):
            eligible_online_agent_ids.append(agent_id)

    # The WS acknowledgement is processed in another database session. Complete
    # all fallible selection work, then commit before offering the job so that
    # session can see and atomically claim it.
    await db.commit()

    for agent_id in eligible_online_agent_ids:
        per_agent_payload = {**job_payload}  # shallow copy — params are read-only
        encrypted = None
        try:
            encrypted = await _encrypt_scope_for_agent(db, agent_id, job_params)
        except Exception:
            pass
        if encrypted:
            per_agent_payload["encrypted_scope"] = encrypted
        pushed = await agent_ws_manager.push_job(
            agent_id,
            per_agent_payload,
            required_feature="atomic_job_claim_v1",
        )
        if pushed:
            logger.info("agent.job.pushed_via_ws",
                        job_id=str(job.id), agent_id=agent_id)
            break

    return {
        "job_id": str(job.id),
        "job_type": body.job_type.value,
        "use_case_id": body.use_case_id,
        "status": job.status.value,
    }


@router.post("/{agent_id}/jobs/{job_id}/result", summary="Agent submits job result")
async def submit_job_result(
    agent_id: uuid.UUID,
    job_id: uuid.UUID,
    body: JobResultRequest,
    db: DB,
    request: Request,
):
    # Ownership check: agent submitting must own this agent_id
    _agent_ownership_check(request, str(agent_id))

    from app.services.job_result_service import process_job_result
    summary = await process_job_result(
        db, agent_id, job_id, body.success, body.result, body.error,
    )
    if not summary.get("ok"):
        raise HTTPException(404, summary.get("error", "Job not found"))
    return summary
