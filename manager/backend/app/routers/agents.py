"""
Agent registration, heartbeat, job polling, and result submission.
"""
import ipaddress
import secrets
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import select

from app.auth.jwt import create_access_token
from app.auth.rbac import require_role
from app.config import get_settings
from app.dependencies import DB, AuthUser, RedisConn
from app.models.agent import Agent, AgentStatus
from app.models.tenant import Tenant
from app.models.asset import Asset as Asset  # re-exported for tests (ag.Asset)
from app.models.engagement import Engagement
from app.models.enums import ScanJobStatus, ScanJobType
from app.models.scan_job import ScanJob
from app.models.service import Service as Service  # re-exported for tests (ag.Service)
from app.services.job_result_service import _promote_assets as _promote_assets
from app.services.scope_targets import validate_targets_in_scope

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

    Delegates to the shared :func:`validate_targets_in_scope` so the dispatch
    gate and the customer-portal request gate share one implementation.
    """
    job_params = params or {}
    requested = job_params.get("targets")
    if requested is None:
        requested = job_params.get("target")
    return validate_targets_in_scope(requested, authoritative_scope)


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
    attempt_id: uuid.UUID | None = None
    fence: int | None = Field(default=None, ge=1)
    status: str = "online"

    @model_validator(mode="after")
    def require_fence_for_running_job(self):
        if self.current_job_id and (self.attempt_id is None or self.fence is None):
            raise ValueError("current_job_id requires attempt_id and fence")
        if not self.current_job_id and (self.attempt_id is not None or self.fence is not None):
            raise ValueError("attempt_id and fence require current_job_id")
        return self


class AgentRefreshRequest(BaseModel):
    capabilities: list[str] = Field(default_factory=list)
    network_segments: list[str] = Field(default_factory=list)
    public_key: str | None = None

    _validate_network_segments = field_validator("network_segments")(
        AgentRegisterRequest.validate_network_segments.__func__
    )


class JobResultRequest(BaseModel):
    attempt_id: uuid.UUID
    fence: int = Field(ge=1)
    success: bool
    result: dict = Field(default_factory=dict)
    error: str | None = None


# The probe's scan-hardness knob (probe/workflow/intensity.py). Duplicated here
# for the same reason as _USE_CASES: manager and probe are separate processes.
_VALID_INTENSITIES = {"light", "standard", "deep"}

# ── Numeric protocol (mirrors probe/agent/use_cases.py) ───────────────────────
# The operator picks a NUMBER; the wire carries the number; the probe maps it to
# the scan pipeline. Codes are banded and MUST stay byte-identical to the probe's
# USE_CASE_CODES — a parity test enforces it. Only ever append, never renumber.
_USE_CASE_CODES: dict[int, str] = {
    1:  "uc_discovery_only",
    2:  "uc_device_inventory",
    10: "uc_full_assessment",
    11: "uc_rescan_delta",
    12: "uc_network_va",
    20: "uc_external_web_triage",
    21: "uc_web_app_triage",
    30: "uc_windows_estate",
    40: "uc_db_exposure",
    50: "uc_snmp_exposure",
    51: "uc_udp_service_exposure",
    60: "uc_iot_device_survey",
    61: "uc_ai_endpoint_sweep",
    70: "uc_ot_passive",
    80: "uc_full_port_audit",
    81: "uc_exposure_matrix",
}
_INTENSITY_CODES: dict[int, str] = {1: "light", 2: "standard", 3: "deep"}
_USE_CASE_ID_TO_CODE: dict[str, int] = {v: k for k, v in _USE_CASE_CODES.items()}
_INTENSITY_NAME_TO_CODE: dict[str, int] = {v: k for k, v in _INTENSITY_CODES.items()}


# The Scanner UI historically uses nmap-style names; map them onto the probe's
# scan-hardness scale so both vocabularies work on the wire.
_INTENSITY_ALIASES = {"stealth": "light", "normal": "standard", "aggressive": "deep"}


def _normalize_intensity_name(value) -> str | None:
    """Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a
    UI alias (stealth/normal/aggressive). Empty/None → None (use the use-case
    default). Raises ValueError only on a genuinely unknown value."""
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("intensity must be a code (1/2/3) or a name")
    # Empty string (unset form field) → fall back to the use-case default.
    if isinstance(value, str) and not value.strip():
        return None
    if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()):
        name = _INTENSITY_CODES.get(int(value))
        if name is None:
            raise ValueError(f"intensity code must be one of {sorted(_INTENSITY_CODES)}")
        return name
    name = str(value).strip().lower()
    name = _INTENSITY_ALIASES.get(name, name)
    if name not in _VALID_INTENSITIES:
        raise ValueError(
            f"intensity must be one of {sorted(_VALID_INTENSITIES)} "
            f"or {sorted(_INTENSITY_ALIASES)}"
        )
    return name


class EnqueueJobRequest(BaseModel):
    engagement_id: uuid.UUID
    job_type: ScanJobType = ScanJobType.discovery
    params: dict = Field(default_factory=dict)
    use_case_id: str | None = None   # maps to probe's use-case library (techprompt §A3)
    # Numeric use-case code (1–99) — the compact alternative to use_case_id.
    uc: int | None = None
    # Optional scan-hardness override: a code (1/2/3) or a name (light/standard/deep).
    # When omitted the probe applies the use-case's own default intensity.
    intensity: int | str | None = None

    @field_validator("uc")
    @classmethod
    def _validate_uc(cls, v: int | None) -> int | None:
        if v is not None and v not in _USE_CASE_CODES:
            raise ValueError(f"unknown use-case code {v}; see GET /agents/use-cases")
        return v

    @field_validator("intensity")
    @classmethod
    def _validate_intensity(cls, v):
        _normalize_intensity_name(v)   # raises on an invalid code/name
        return v


# ── Use-case library (mirrored from probe/agent/use_cases.py) ─────────────────
# Duplicated intentionally: manager and probe are separate deployable processes.
# The manager exposes this so the frontend can show the operator a picker;
# the probe enforces it at execution time — the operator cannot invent a new
# use_case_id that the probe will execute.

_USE_CASES = {
    # Ordered by the numeric USE_CASE_CODES taxonomy (discovery → assessment →
    # web → windows → db → network-services → iot/ai → ot → deep) so the catalog
    # reads — and the UI renders — in the natural security-workflow sequence.
    # Customer-facing copy: names lead with the asset/outcome; descriptions follow
    # a "what we do → why it matters" shape.

    # ── Discovery / inventory (codes 1–9) ──────────────────────────────────────
    "uc_discovery_only": {
        "display_name": "Network Discovery",
        "description": (
            "Maps every live device and the open ports each exposes — a fast, "
            "no-impact inventory of what is actually on this network."
        ),
        "scan_type": "discovery",
        "profile": "it",
        "expected_runtime_hint": "2–5 min per /24",
    },
    "uc_device_inventory": {
        "display_name": "Device Inventory & Classification",
        "description": (
            "Identifies each live device and infers its role — workstation, "
            "server, network device, printer, hypervisor, or IoT — from OS family, "
            "open ports, and service banners (evidence-based, never a hostname guess)."
        ),
        "scan_type": "device_inventory",
        "profile": "it",
        "intensity": "standard",
        "expected_runtime_hint": "5–15 min per /24",
    },
    # ── Full assessment (codes 10–19) ──────────────────────────────────────────
    "uc_full_assessment": {
        "display_name": "Full Security Assessment",
        "description": (
            "The complete sweep: discovers hosts, maps every service, fingerprints "
            "the OS, and inspects TLS, web, SMB, database, and SNMP exposure — your "
            "baseline security posture in one run."
        ),
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    "uc_rescan_delta": {
        "display_name": "Re-scan & Change Detection",
        "status": "coming_soon",
        "description": (
            "Re-runs a full assessment and highlights what changed since the last "
            "run — new hosts, newly opened ports, and configuration drift."
        ),
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    "uc_network_va": {
        "display_name": "Network Vulnerability Assessment (Full Campaign)",
        "description": (
            "The end-to-end campaign, run as one sequential background job with "
            "live per-stage progress: discovers every host, inventories and "
            "classifies devices, deep-assesses each open service, checks "
            "Windows/SMB, SNMP, and UDP amplification exposure, maps internet "
            "exposure, and correlates observed versions to prioritized CVE "
            "candidates — a complete network vulnerability assessment in one run."
        ),
        "scan_type": "network_va",
        "profile": "it",
        "expected_runtime_hint": "30–90 min per /24",
    },
    # ── Web / TLS (codes 20–29) ────────────────────────────────────────────────
    "uc_external_web_triage": {
        "display_name": "Web & TLS/SSL Security Check",
        "status": "coming_soon",
        "description": (
            "Scans web servers for exposed HTTP/HTTPS services and grades TLS/SSL "
            "configuration — protocol versions, cipher strength, and certificate health."
        ),
        "scan_type": "web_tls_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_web_app_triage": {
        "display_name": "Web Application Security Check",
        "status": "coming_soon",
        "description": (
            "Fingerprints web applications — supported HTTP methods, response and "
            "security headers, and server technology — a pre-flight before a full "
            "web-app penetration test."
        ),
        "scan_type": "web_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    # ── Windows / SMB (codes 30–39) ────────────────────────────────────────────
    "uc_windows_estate": {
        "display_name": "Windows & File-Sharing (SMB) Security",
        "description": (
            "Confirms Windows file-sharing is hardened — that the legacy SMBv1 "
            "protocol is disabled and that SMB signing is required to block relay "
            "and tampering attacks."
        ),
        "scan_type": "smb_enum",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    # ── Database (codes 40–49) ─────────────────────────────────────────────────
    "uc_db_exposure": {
        "display_name": "Database Exposure Check",
        "status": "coming_soon",
        "description": (
            "Checks whether databases (MySQL, PostgreSQL, SQL Server, Redis, "
            "MongoDB) are reachable on the network and whether they accept "
            "unauthenticated connections."
        ),
        "scan_type": "db_fingerprint",
        "profile": "it",
        "expected_runtime_hint": "3–10 min",
    },
    # ── Network services (codes 50–59) ─────────────────────────────────────────
    "uc_snmp_exposure": {
        "display_name": "SNMP Weak-Credential Check",
        "description": (
            "Tests routers, switches, printers, and appliances for SNMP services "
            "that accept default or weak community strings — a common way attackers "
            "read and alter device configuration."
        ),
        "scan_type": "snmp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    "uc_udp_service_exposure": {
        "display_name": "UDP & Amplification Exposure",
        "description": (
            "Probes UDP services (DNS, NTP, SNMP, memcached, NetBIOS) for open "
            "resolvers and amplification weaknesses that attackers abuse to launch "
            "reflected DDoS attacks."
        ),
        "scan_type": "udp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    # ── IoT / AI (codes 60–69) ─────────────────────────────────────────────────
    "uc_iot_device_survey": {
        "display_name": "IoT & Embedded Device Discovery",
        "description": (
            "Finds IoT and embedded devices — IP cameras (RTSP), MQTT brokers, "
            "printers, DVRs, and Telnet-exposed gear — and captures their service "
            "banners for inventory."
        ),
        "scan_type": "service_fingerprint",
        "profile": "iot",
        "expected_runtime_hint": "3–10 min per /24",
    },
    "uc_ai_endpoint_sweep": {
        "display_name": "AI & MCP Endpoint Discovery",
        "status": "coming_soon",
        "description": (
            "Discovers exposed AI inference endpoints and Model Context Protocol "
            "(MCP) servers — a fast-growing, often-unmonitored attack surface."
        ),
        "scan_type": "mcp_discovery",
        "profile": "it",
        "expected_runtime_hint": "3–8 min",
    },
    # ── OT / ICS (codes 70–79) ─────────────────────────────────────────────────
    "uc_ot_passive": {
        "display_name": "OT / ICS Passive Discovery",
        "status": "coming_soon",
        "description": (
            "Listen-only discovery for operational-technology (OT/ICS/SCADA) "
            "networks — inventories devices with zero active packets, so fragile "
            "industrial equipment is never probed."
        ),
        "scan_type": "passive_discovery",
        "profile": "ot",
        "expected_runtime_hint": "listen-only, duration set by operator",
    },
    # ── Deep / specialized (codes 80–99) ───────────────────────────────────────
    "uc_full_port_audit": {
        "display_name": "Full-Port Audit (all 65,535)",
        "description": (
            "Scans every TCP port on a host to surface services hiding on "
            "non-standard ports, with a completeness + self-health check so a clean "
            "result is genuinely clean, not just an incomplete scan."
        ),
        "scan_type": "full_port_audit",
        "profile": "it",
        "intensity": "deep",
        "expected_runtime_hint": "20–90 min per host",
    },
    "uc_exposure_matrix": {
        "display_name": "Internet-Exposure Mapping",
        "description": (
            "Records which ports are reachable from each probe's vantage point; "
            "with two or more probes, the platform separates truly internet-exposed "
            "services from internal-only ones."
        ),
        "scan_type": "exposure_matrix",
        "profile": "it",
        "intensity": "standard",
        "expected_runtime_hint": "5–15 min per /24",
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


class AgentBootstrapRequest(BaseModel):
    bootstrap_key: str
    name: str = Field(..., min_length=1, max_length=255)
    location: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    network_segments: list[str] = Field(default_factory=list)
    public_key: str | None = None

    @field_validator("network_segments")
    @classmethod
    def validate_network_segments(cls, values: list[str]) -> list[str]:
        return AgentRegisterRequest.validate_network_segments(values)


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/use-cases", summary="List available pre-defined scan use-cases (probe action library)")
async def list_use_cases(current_user: AuthUser):
    """Returns the finite library of scan use-cases operators can dispatch to probes.
    Each entry now carries its numeric `code` (the compact dispatch protocol) and
    default `intensity`. The probe enforces this list at execution time — an
    unknown use-case is rejected before any packet leaves the host."""
    return [
        {"use_case_id": uid, "code": _USE_CASE_ID_TO_CODE.get(uid), **meta}
        for uid, meta in _USE_CASES.items()
    ]


@router.get("/intensities", summary="List scan intensity codes (light/standard/deep)")
async def list_intensities(current_user: AuthUser):
    """The numeric scan-hardness scale: 1 light, 2 standard, 3 deep."""
    return [{"code": c, "name": n} for c, n in sorted(_INTENSITY_CODES.items())]


@router.post(
    "/bootstrap",
    response_model=AgentRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Probe self-registers using a shared bootstrap key (no user login required)",
)
async def bootstrap_agent(body: AgentBootstrapRequest, db: DB):
    """Allows a probe to register without an admin-issued PAT.

    The manager must have PROBE_BOOTSTRAP_KEY set in its environment. The probe
    presents that key; on success it receives a long-lived agent JWT identical
    to the one issued by /agents/register. Leave PROBE_BOOTSTRAP_KEY empty to
    disable this endpoint (returns 403).
    """
    settings = get_settings()
    if not settings.allow_unsafe_legacy_probe_bootstrap:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=(
                "Legacy shared-secret probe bootstrap is disabled. "
                "Use device enrollment or an explicitly supported legacy registration path."
            ),
        )
    bootstrap_key = settings.probe_bootstrap_key

    if not bootstrap_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Probe bootstrap is disabled on this manager. Set PROBE_BOOTSTRAP_KEY.",
        )

    if not secrets.compare_digest(body.bootstrap_key, bootstrap_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bootstrap key.",
        )

    # Resolve the first active tenant (bootstrap probes join the default tenant)
    tenant = (
        await db.execute(
            select(Tenant).where(Tenant.is_active == True).order_by(Tenant.created_at).limit(1)
        )
    ).scalar_one_or_none()

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No active tenant found. Seed the manager first.",
        )

    existing = (
        await db.execute(
            select(Agent)
            .where(Agent.tenant_id == tenant.id, Agent.name == body.name)
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
        if body.public_key:
            agent.public_key = body.public_key
    else:
        agent = Agent(
            tenant_id=tenant.id,
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

    token = create_access_token(
        subject=str(agent.id),
        tenant_id=str(tenant.id),
        role="agent",
        expires_minutes=60 * 24 * 365,
    )
    logger.info("agent.bootstrapped", agent_id=str(agent.id), name=body.name,
                tenant_id=str(tenant.id), reused=existing is not None)
    return AgentRegisterResponse(agent_id=str(agent.id), token=token)


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
            "site_id": str(a.site_id) if getattr(a, "site_id", None) else None,
            "lifecycle_status": getattr(a, "lifecycle_status", "active"),
            "credential_generation": getattr(a, "credential_generation", 0),
            "approved_capabilities": getattr(a, "approved_capabilities", []) or [],
            "approved_networks": getattr(a, "approved_networks", []) or [],
            "agent_version": getattr(a, "agent_version", None),
            "installer_version": getattr(a, "installer_version", None),
            "build_digest": getattr(a, "build_digest", None),
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
    # Heartbeats always carry current_job_id. Persisting None is important: if
    # we only write truthy IDs, completed probes remain stuck as "busy" forever.
    agent.current_job_id = (
        uuid.UUID(body.current_job_id) if body.current_job_id else None
    )
    if body.current_job_id:
        job_uuid = agent.current_job_id
        from app.services.job_attempt_service import renew_job_attempt
        renewed = await renew_job_attempt(
            db,
            job_id=job_uuid,
            attempt_id=body.attempt_id,
            fence=body.fence,
            agent_id=agent_id,
        )
        if not renewed:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Job attempt lease is stale or no longer current",
            )

    await db.flush()
    return {"ok": True, "lease_valid": True}


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

    if getattr(agent, "signing_key_fingerprint", None):
        if agent.lifecycle_status != "active":
            raise HTTPException(403, "Enrolled probe is not active")
        if not set(body.capabilities).issubset(set(agent.approved_capabilities or [])):
            raise HTTPException(422, "Reported capabilities exceed Manager-approved capabilities")
        if not _scope_is_reachable(agent.approved_networks or [], body.network_segments):
            raise HTTPException(422, "Reported networks exceed Manager-approved Site policy")
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
    response = {"ok": True}
    if getattr(agent, "site_id", None):
        from app.models.probe_site import ProbeSite
        from app.routers.probe_enrollment import _policy

        site = (await db.execute(
            select(ProbeSite).where(
                ProbeSite.id == agent.site_id,
                ProbeSite.tenant_id == agent.tenant_id,
                ProbeSite.status == "active",
            )
        )).scalar_one_or_none()
        if site is None:
            raise HTTPException(403, "Probe Site is disabled or unavailable")
        response["policy"] = _policy(site)
    return response


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

    # A shared atomic claim primitive creates a separate immutable attempt row
    # and installs its monotonically increasing fence on the logical job.
    claim_limit = max(0, min(int(limit), 100))
    jobs: list[tuple[ScanJob, object]] = []
    for job, engagement in candidates:
        if len(jobs) >= claim_limit:
            break
        params = job.result or {}
        # Honor an operator-pinned probe: a job targeted at a specific agent is
        # only claimable by that agent. Untargeted jobs (no preferred_agent_id)
        # remain claimable by any compatible probe.
        preferred = params.get("preferred_agent_id")
        if preferred and str(preferred) != str(agent_id):
            continue
        if not _agent_can_execute_job(
            agent, job.job_type, params, engagement.scope_cidrs or [],
        ):
            continue

        from app.services.job_attempt_service import claim_job_attempt
        claim = await claim_job_attempt(
            db,
            job_id=job.id,
            agent_id=agent_id,
            tenant_id=agent.tenant_id,
        )
        if claim:
            jobs.append((job, claim))

    # Build response — Phase 4: encrypt scope for this specific agent
    response_jobs = []
    for j, claim in jobs:
        params = j.result or {}
        encrypted_scope = await _encrypt_scope_for_agent(db, str(agent_id), params)
        job_dict = {
            "job_id": str(j.id),
            "engagement_id": str(j.engagement_id),
            "job_type": j.job_type.value,
            "status": ScanJobStatus.running.value,
            "params": params,
            "attempt_id": str(claim.attempt_id),
            "attempt_number": claim.attempt_number,
            "fence": claim.fence,
            "lease_expires_at": claim.lease_expires_at.isoformat(),
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


@router.get("/{agent_id}/job-history",
            summary="Scan jobs claimed by this probe (running + history) for the Fleet UI")
async def get_agent_job_history(
    agent_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    limit: int = 25,
):
    """Read-only per-probe job list — the probe's running job (its serial queue head)
    plus recent completed/failed jobs, newest first. Distinct from GET /{agent_id}/jobs,
    which atomically CLAIMS a pending job for the probe to execute."""
    limit = max(1, min(int(limit), 100))
    rows = (await db.execute(
        select(ScanJob)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(
            ScanJob.agent_id == str(agent_id),
            Engagement.tenant_id == current_user.tenant_id,
        )
        .order_by(ScanJob.created_at.desc())
        .limit(limit)
    )).scalars().all()

    def _summ(r: ScanJob) -> dict:
        res = r.result if isinstance(r.result, dict) else {}
        return {
            "job_id": str(r.id),
            "engagement_id": str(r.engagement_id),
            "job_type": r.job_type.value,
            "status": r.status.value,
            "use_case_id": res.get("use_case_id"),
            "host_count": res.get("host_count"),
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
        }

    return [_summ(r) for r in rows]


@router.post(
    "/jobs",
    status_code=status.HTTP_201_CREATED,
    summary="Enqueue an agent-executable scan job (discovery/lateral/cloud) for probes to pick up",
)
async def enqueue_agent_job(
    body: EnqueueJobRequest,
    db: DB,
    redis: RedisConn,
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

    # Resolve the use-case from EITHER the numeric code (uc) or the string id.
    # The number is the operator's compact interface; the string is authoritative
    # against the library. uc is already schema-validated to a known code.
    resolved_use_case_id = body.use_case_id or (
        _USE_CASE_CODES.get(body.uc) if body.uc is not None else None
    )
    if resolved_use_case_id and resolved_use_case_id not in _USE_CASES:
        raise HTTPException(
            400,
            f"Unknown use_case_id '{resolved_use_case_id}'. "
            f"Call GET /agents/use-cases to see the available use-cases.",
        )

    scan_profile = (eng.rules_of_engagement or {}).get("scan_profile", "it")

    # When a use-case is given, resolve the scan_type from the library so
    # OT-profile enforcement can check it.
    if resolved_use_case_id:
        resolved_scan_type = _USE_CASES[resolved_use_case_id]["scan_type"]
        # Backend gate: "coming soon" capabilities are UI-disabled and must also be
        # refused at dispatch so an unverified use-case can't run via a raw API call.
        if _USE_CASES[resolved_use_case_id].get("status") == "coming_soon":
            raise HTTPException(
                422,
                f"Use case '{resolved_use_case_id}' is coming soon and not yet "
                f"available for dispatch.",
            )
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
    # Scan intensity: the first-class field wins, else an intensity embedded in
    # params (as a code or a name). Validate here so a typo is rejected at enqueue,
    # not silently at the probe. When neither is set the probe applies the
    # use-case's own default.
    try:
        intensity_name = _normalize_intensity_name(
            body.intensity if body.intensity is not None else body.params.get("intensity")
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))

    job_params = {**body.params}
    # Wire the compact numeric protocol to the probe: uc + intensity as NUMBERS.
    # use_case_id (string) rides along for provenance/allowlisting — the probe
    # resolves either and gets the same pipeline.
    uc_code = body.uc if body.uc is not None else _USE_CASE_ID_TO_CODE.get(resolved_use_case_id)
    if uc_code is not None:
        job_params["uc"] = uc_code
    if intensity_name:
        job_params["intensity"] = _INTENSITY_NAME_TO_CODE[intensity_name]
    if resolved_use_case_id:
        job_params["use_case_id"] = resolved_use_case_id
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
                use_case_id=resolved_use_case_id, uc=uc_code)

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
    # Select online agents from the DB — authoritative across ALL API workers,
    # unlike the process-local WS registry. Each is then delivered via deliver_job:
    # sent directly if its socket is on THIS worker, else published so the worker
    # holding it forwards (Redis backplane). Legacy probes without the claim feature
    # are filtered at send time and fall through to HTTP polling. A fresh payload
    # PER agent — encrypted_scope is per-agent (a different public key each).
    online_rows = (await db.execute(
        select(Agent).where(
            Agent.tenant_id == current_user.tenant_id,
            Agent.status == AgentStatus.online,
        )
    )).scalars().all()
    eligible_agents = [
        candidate for candidate in online_rows
        if _agent_can_execute_job(candidate, job.job_type, job_params, eng.scope_cidrs or [])
    ]

    # The claim runs in another DB session, so commit before offering the job.
    await db.commit()

    for candidate in eligible_agents:
        agent_id = str(candidate.id)
        per_agent_payload = {**job_payload}  # shallow copy — params are read-only
        try:
            encrypted = await _encrypt_scope_for_agent(db, agent_id, job_params)
            if encrypted:
                per_agent_payload["encrypted_scope"] = encrypted
        except Exception:
            pass
        delivered_locally = await agent_ws_manager.deliver_job(
            redis,
            agent_id,
            per_agent_payload,
            required_feature="atomic_job_claim_v1",
        )
        logger.info("agent.job.push_dispatched", job_id=str(job.id),
                    agent_id=agent_id, local=delivered_locally)
        break  # dispatch to the first eligible agent; HTTP poll covers any miss

    return {
        "job_id": str(job.id),
        "job_type": body.job_type.value,
        "use_case_id": resolved_use_case_id,
        "uc": uc_code,
        "intensity": intensity_name,
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
        body.attempt_id, body.fence,
    )
    if not summary.get("ok"):
        raise HTTPException(
            summary.get("status_code", 404),
            summary.get("error", "Job not found"),
        )

    # P3: if this job was an approved safe active-validation, turn its result into
    # a finding verdict. Best-effort and gated — a normal scan result never even
    # triggers a lookup (see looks_like_validation_result), and any failure here
    # must not fail the probe's spool-clearing submit.
    if summary.get("accepted") is not False:
        try:
            from app.services.validation_ingest import ingest_validation_result
            await ingest_validation_result(db, job_id, body.result)
        except Exception as exc:  # noqa: BLE001 — best-effort, never break submit
            logger.warning("validation.ingest.failed", job_id=str(job_id), error=str(exc))

    return summary
