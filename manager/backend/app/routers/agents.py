"""
Agent registration, heartbeat, job polling, and result submission.
"""
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token
from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.discovery.finding_translator import create_findings_from_probe_result
from app.models.agent import Agent, AgentStatus
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import AssetType, ScanJobStatus, ScanJobType
from app.models.scan_job import ScanJob
from app.models.scan_result import ScanResult
from app.models.service import Service

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

# Mirrors probe/scanners/__init__.py's DEFAULT_SCAN_FOR_JOBTYPE. Duplicated
# deliberately — the manager and probe are separate deployable processes (no
# shared Python import), so this lets the manager enforce policy against the
# SAME scan_type the probe will actually resolve and run, not guess at it.
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


def _resolve_scan_type(job_type: str, params: dict) -> str:
    return params.get("scan_type") or _DEFAULT_SCAN_FOR_JOBTYPE.get(job_type, "discovery")


# ── Schemas ───────────────────────────────────────────────────────────────────

class AgentRegisterRequest(BaseModel):
    name: str
    location: str | None = None
    capabilities: list[str] = []
    network_segments: list[str] = []


class AgentRegisterResponse(BaseModel):
    agent_id: str
    token: str


class HeartbeatRequest(BaseModel):
    agent_id: str
    current_job_id: str | None = None
    status: str = "online"


class JobResultRequest(BaseModel):
    success: bool
    result: dict = {}
    error: str | None = None


class EnqueueJobRequest(BaseModel):
    engagement_id: uuid.UUID
    job_type: ScanJobType = ScanJobType.discovery
    params: dict = {}
    use_case_id: str | None = None   # maps to probe's use-case library (techprompt §A3)


# ── Use-case library (mirrored from probe/agent/use_cases.py) ─────────────────
# Duplicated intentionally: manager and probe are separate deployable processes.
# The manager exposes this so the frontend can show the operator a picker;
# the probe enforces it at execution time — the operator cannot invent a new
# use_case_id that the probe will execute.

_USE_CASES = {
    "uc_discovery_only": {
        "display_name": "Network Discovery",
        "description": "Fast host-discovery + port scan. Use for 'what's alive here?' triage.",
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
        "scan_type": "tls_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_db_exposure": {
        "display_name": "Database Exposure Check",
        "description": "Protocol-handshake fingerprint of database ports.",
        "scan_type": "db_fingerprint",
        "profile": "it",
        "expected_runtime_hint": "3–10 min",
    },
    "uc_windows_estate": {
        "display_name": "Windows Estate",
        "description": "SMB dialect detection. Is SMBv1 enabled? Are shares exposed?",
        "scan_type": "smb_enum",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_ot_passive": {
        "display_name": "OT / ICS Passive Discovery",
        "description": "PASSIVE ONLY — zero active packets. Safe for OT/ICS/SCADA segments.",
        "scan_type": "passive_discovery",
        "profile": "ot",
        "expected_runtime_hint": "listen-only",
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
        "description": "Full re-assessment. Manager diffs against prior run to surface what changed.",
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
}


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
    else:
        agent = Agent(
            tenant_id=current_user.tenant_id,
            name=body.name,
            location=body.location,
            capabilities=body.capabilities,
            network_segments=body.network_segments,
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
        online = bool(a.last_heartbeat and (now - a.last_heartbeat).total_seconds() < 90)
        out.append({
            "id": str(a.id),
            "name": a.name,
            "location": a.location,
            "status": a.status.value if hasattr(a.status, "value") else str(a.status),
            "capabilities": a.capabilities,
            "network_segments": a.network_segments,
            "last_heartbeat": a.last_heartbeat.isoformat() if a.last_heartbeat else None,
            "current_job_id": str(a.current_job_id) if a.current_job_id else None,
            "online": online,
        })
    return out


@router.post("/heartbeat", summary="Agent sends health ping every 30s")
async def heartbeat(body: HeartbeatRequest, db: DB):
    agent_id = uuid.UUID(body.agent_id)
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(404, "Agent not found")

    agent.last_heartbeat = datetime.now(timezone.utc)
    try:
        agent.status = AgentStatus(body.status)
    except ValueError:
        agent.status = AgentStatus.online
    if body.current_job_id:
        agent.current_job_id = uuid.UUID(body.current_job_id)

    await db.flush()
    return {"ok": True}


@router.get("/{agent_id}/jobs", summary="Agent polls for pending ScanJobs")
async def get_agent_jobs(
    agent_id: uuid.UUID,
    db: DB,
    limit: int = 1,
):
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(404, "Agent not found")

    jobs_result = await db.execute(
        select(ScanJob)
        .where(
            ScanJob.status == ScanJobStatus.pending,
            ScanJob.agent_id == None,
            ScanJob.job_type.in_(AGENT_EXECUTABLE_TYPES),
        )
        .order_by(ScanJob.created_at)
        .limit(limit)
    )
    jobs = jobs_result.scalars().all()

    # Assign jobs to this agent
    for job in jobs:
        job.agent_id = str(agent_id)
        job.status = ScanJobStatus.running
        job.started_at = datetime.now(timezone.utc)

    await db.flush()

    return [
        {
            "job_id": str(j.id),
            "engagement_id": str(j.engagement_id),
            "job_type": j.job_type.value,
            "status": j.status.value,
            # Scan parameters (targets, ports, rate…) the probe needs to execute.
            "params": j.result or {},
        }
        for j in jobs
    ]


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
    eng = (await db.execute(
        select(Engagement).where(
            Engagement.id == body.engagement_id,
            Engagement.tenant_id == current_user.tenant_id,
        )
    )).scalar_one_or_none()
    if not eng:
        raise HTTPException(404, "Engagement not found")

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
    if eng.scope_cidrs:
        job_params.setdefault("scope_cidrs", eng.scope_cidrs)

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
    return {
        "job_id": str(job.id),
        "job_type": body.job_type.value,
        "use_case_id": body.use_case_id,
        "status": job.status.value,
    }


async def _promote_assets(db, engagement_id: uuid.UUID, result: dict) -> int:
    """Upsert hosts/services discovered by a probe into the assets/services tables.

    Keyed by (engagement_id, ip) for assets and (asset, port, protocol) for services,
    so repeated scans update in place instead of duplicating. Returns the number of
    newly-created assets. Any host without an IP is skipped.
    """
    hosts = (result or {}).get("hosts") or []
    promoted = 0
    for h in hosts:
        ip = h.get("ip")
        if not ip:
            continue
        asset = (await db.execute(
            select(Asset).where(Asset.engagement_id == engagement_id, Asset.ip_address == ip)
        )).scalar_one_or_none()
        if asset:
            asset.hostname = h.get("hostname") or asset.hostname
            asset.os = h.get("os") or asset.os
            asset.last_seen = datetime.now(timezone.utc)
        else:
            asset = Asset(
                engagement_id=engagement_id, ip_address=ip,
                hostname=h.get("hostname"), os=h.get("os"),
                asset_type=AssetType.server, last_seen=datetime.now(timezone.utc),
            )
            db.add(asset)
            await db.flush()
            promoted += 1

        for p in h.get("ports") or []:
            port_no = p.get("port")
            if port_no is None:
                continue
            proto = p.get("protocol") or "tcp"
            cpe = p.get("cpe")
            cpe_str = ",".join(cpe) if isinstance(cpe, list) else cpe
            svc = (await db.execute(
                select(Service).where(
                    Service.asset_id == asset.id, Service.port == port_no, Service.protocol == proto)
            )).scalar_one_or_none()
            if svc:
                svc.service_name = p.get("service") or svc.service_name
                svc.product = p.get("product") or svc.product
                svc.version = p.get("version") or svc.version
                svc.cpe = cpe_str or svc.cpe
            else:
                db.add(Service(
                    asset_id=asset.id, port=port_no, protocol=proto,
                    service_name=p.get("service"), product=p.get("product"),
                    version=p.get("version"), cpe=cpe_str,
                ))
        await db.flush()
    return promoted


@router.post("/{agent_id}/jobs/{job_id}/result", summary="Agent submits job result")
async def submit_job_result(
    agent_id: uuid.UUID,
    job_id: uuid.UUID,
    body: JobResultRequest,
    db: DB,
    background_tasks: BackgroundTasks,
):
    result = await db.execute(
        select(ScanJob).where(ScanJob.id == job_id, ScanJob.agent_id == str(agent_id))
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found or not assigned to this agent")

    job.status = ScanJobStatus.completed if body.success else ScanJobStatus.failed
    job.completed_at = datetime.now(timezone.utc)

    # P3-#10: persist raw facts to the append-only scan_results table and keep
    # them OUT of scan_jobs.result (which would otherwise bloat every job row
    # with the full facts array). The durable copy in scan_results is what makes
    # re-detection-without-re-scan possible. job.result keeps the lean summary.
    facts = body.result.get("facts") if isinstance(body.result, dict) else None
    if isinstance(facts, list) and facts:
        db.add(ScanResult(
            engagement_id=job.engagement_id, job_id=job.id,
            scan_type=body.result.get("scan_type"), fact_count=len(facts), facts=facts))
        lean = {k: v for k, v in body.result.items() if k != "facts"}
        job.result = {**lean, "fact_count": len(facts), "error": body.error}
    else:
        job.result = {**body.result, "error": body.error}
    await db.flush()

    # Promote discovered hosts into the attack-surface inventory (best-effort:
    # a promotion failure must never fail the probe's result submission).
    promoted = 0
    findings_created = 0
    if body.success and isinstance(body.result, dict):
        if body.result.get("hosts"):
            try:
                promoted = await _promote_assets(db, job.engagement_id, body.result)
            except Exception as exc:  # noqa: BLE001
                logger.warning("agent.job.promote_failed", job_id=str(job_id), error=str(exc))

        # tls_scan/smb_enum/mcp_discovery/ai_service_discovery already self-assess
        # severity-tagged findings (see finding_translator.py) — without this,
        # those findings landed only in job.result and never reached the
        # dashboard's Findings table at all.
        try:
            findings_created = await create_findings_from_probe_result(
                db, job.engagement_id, body.result)
        except Exception as exc:  # noqa: BLE001
            logger.warning("agent.job.findings_failed", job_id=str(job_id), error=str(exc))

        # New raw-facts path: run detection_engine on result['facts']. P1 —
        # detection is the EXPENSIVE step (full CPE→vuln-DB→verify pipeline over
        # a potentially large facts payload), so it runs OFF the request path as
        # a background task (its own DB session). The probe's submit returns
        # immediately; findings appear shortly after. Keeps probe throughput
        # decoupled from analysis cost.
        if isinstance(body.result.get("facts"), list) and body.result["facts"]:
            from app.detection.engine_bridge import run_detection_job
            background_tasks.add_task(run_detection_job, job.engagement_id, body.result)

    logger.info(
        "agent.job.result",
        agent_id=str(agent_id),
        job_id=str(job_id),
        success=body.success,
        assets_promoted=promoted,
        findings_created=findings_created,
    )
    return {"ok": True, "assets_promoted": promoted, "findings_created": findings_created}
