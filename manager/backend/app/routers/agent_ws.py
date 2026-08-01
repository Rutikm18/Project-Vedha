"""
agent_ws.py — WebSocket endpoint for probe push connectivity.

Probes connect via wss://manager/agents/ws with an Authorization header, and the manager
pushes scan jobs directly over this persistent connection instead of the
probe polling HTTP every 10s. The probe also sends heartbeats and submits
results over the same WebSocket.

Architecture:
  - /agents/ws  — WebSocket endpoint (mounted under /agents prefix)
  - Auth via Bearer JWT header (validated on connect, role must be "agent")
  - Heartbeats, result submission, and job acks use JSON frames
  - Manager pushes jobs as {type: "job_push", job: {...}} frames
  - Result processing is identical to the HTTP path (shared helper)

Fallback: if WebSocket fails, the probe falls back to HTTP polling
(GET /agents/{id}/jobs). The manager leaves jobs as "pending" for HTTP
pickup when no agent is connected via WS.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import structlog
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select, update

from app.auth.jwt import decode_token
from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.agent import Agent, AgentStatus
from app.models.engagement import Engagement
from app.models.scan_job import ScanJob, ScanJobStatus
from app.websocket.manager import agent_ws_manager

logger = structlog.get_logger()
router = APIRouter(prefix="/agents", tags=["agent-websocket"])


def _agent_token_from_websocket(websocket: WebSocket) -> str:
    """Read an agent bearer token exclusively from the non-logged auth header."""
    authorization = websocket.headers.get("authorization", "")
    return authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""


async def _claim_pushed_job(
    db,
    agent_id: str,
    tenant_id: str,
    job_id: uuid.UUID,
) -> tuple[bool, str]:
    """Validate eligibility and atomically claim a WebSocket job offer."""
    from app.routers.agents import (
        AGENT_EXECUTABLE_TYPES,
        _agent_can_execute_job,
    )

    try:
        agent_uuid = uuid.UUID(str(agent_id))
        tenant_uuid = uuid.UUID(str(tenant_id))
    except (ValueError, TypeError, AttributeError):
        return False, "not_eligible"

    agent = (await db.execute(
        select(Agent).where(
            Agent.id == agent_uuid,
            Agent.tenant_id == tenant_uuid,
        )
    )).scalar_one_or_none()
    if agent is None:
        return False, "not_eligible"

    row = (await db.execute(
        select(ScanJob, Engagement)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(
            ScanJob.id == job_id,
            Engagement.tenant_id == tenant_uuid,
        )
    )).one_or_none()
    if row is None:
        return False, "not_available"

    job, engagement = row
    if (
        job.status != ScanJobStatus.pending
        or job.agent_id is not None
        or job.job_type not in AGENT_EXECUTABLE_TYPES
        or not _agent_can_execute_job(
            agent,
            job.job_type,
            job.result or {},
            engagement.scope_cidrs or [],
        )
    ):
        return False, "not_eligible"

    now = datetime.now(timezone.utc)
    claimed = (await db.execute(
        update(ScanJob)
        .where(
            ScanJob.id == job_id,
            ScanJob.status == ScanJobStatus.pending,
            ScanJob.agent_id.is_(None),
            ScanJob.engagement_id.in_(
                select(Engagement.id).where(
                    Engagement.tenant_id == tenant_uuid,
                )
            ),
        )
        .values(
            agent_id=agent_id,
            status=ScanJobStatus.running,
            started_at=now,
            lease_expires_at=now
            + timedelta(seconds=get_settings().job_lease_seconds),
        )
        .execution_options(synchronize_session=False)
    )).rowcount
    await db.commit()
    if not claimed:
        return False, "claim_lost"
    return True, "claimed"


# ── WebSocket endpoint ────────────────────────────────────────────────────────

@router.websocket("/ws")
async def agent_websocket_endpoint(websocket: WebSocket):
    """Persistent WebSocket for probe → manager push communication.

    Authentication:
        Authorization: Bearer <agent JWT>

    Query-string credentials are intentionally rejected so access logs and
    proxy traces cannot capture an agent token.

    Protocol (JSON frames):

    PROBE → MANAGER:
        {"type":"hello","agent_id":"...","protocol_version":2,
         "features":["atomic_job_claim_v1"]}
        {"type":"heartbeat","status":"online"|"busy","current_job_id":"..."}
        {"type":"result","job_id":"...","success":bool,"result":{...},"error":"..."}
        {"type":"job_ack","job_id":"...","accepted":bool}

    MANAGER → PROBE:
        {"type":"hello_ok","protocol_version":2,"features":["atomic_job_claim_v1"]}
        {"type":"error","message":"..."}
        {"type":"job_push","job":{"job_id":"...","engagement_id":"...","job_type":"...","params":{...}}}
        {"type":"job_claim","job_id":"...","claimed":bool,"reason":"..."}
        {"type":"result_ack","job_id":"..."}
    """
    # ── Validate token ────────────────────────────────────────────────────
    token = _agent_token_from_websocket(websocket)
    if not token:
        await websocket.close(code=4001, reason="Missing agent token")
        return

    try:
        payload = decode_token(token)
    except Exception as exc:
        logger.warning("agent.ws.auth_failed", reason=str(exc))
        await websocket.close(code=4001, reason="Invalid or expired token")
        return

    if payload.get("type") != "access" or payload.get("role") != "agent":
        await websocket.close(code=4003, reason="Token not valid for agent WS")
        return

    agent_id = payload["sub"]
    tenant_id = payload["tenant_id"]
    try:
        agent_uuid = uuid.UUID(str(agent_id))
        tenant_uuid = uuid.UUID(str(tenant_id))
    except (ValueError, TypeError, AttributeError):
        await websocket.close(code=4003, reason="Invalid agent token claims")
        return

    # ── Verify agent record ───────────────────────────────────────────────
    async with AsyncSessionLocal() as db:
        agent = (await db.execute(
            select(Agent).where(
                Agent.id == agent_uuid,
                Agent.tenant_id == tenant_uuid,
            )
        )).scalar_one_or_none()

        if agent is None:
            logger.warning("agent.ws.unknown_agent", agent_id=agent_id)
            await websocket.close(code=4004, reason="Agent not found")
            return

        # Accept the connection
        await websocket.accept()
        await agent_ws_manager.register(agent_id, tenant_id, websocket)
        # Update agent status in DB
        agent.status = AgentStatus.online
        agent.last_heartbeat = datetime.now(timezone.utc)
        await db.commit()

    logger.info("agent.ws.accepted", agent_id=agent_id, agent_name=agent.name)

    # ── Message loop ──────────────────────────────────────────────────────
    try:
        # Send welcome
        await websocket.send_json({
            "type": "hello_ok",
            "protocol_version": 2,
            "features": ["atomic_job_claim_v1"],
        })

        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "")

            if msg_type == "heartbeat":
                status = data.get("status", "online")
                current_job = data.get("current_job_id")
                await agent_ws_manager.record_heartbeat(agent_id, status, current_job)

                # Also update DB (throttled — every heartbeat, but cheap: 1 row UPDATE)
                async with AsyncSessionLocal() as db:
                    ag = (await db.execute(
                        select(Agent).where(Agent.id == agent_id)
                    )).scalar_one_or_none()
                    if ag:
                        ag.last_heartbeat = datetime.now(timezone.utc)
                        try:
                            ag.status = AgentStatus(status)
                        except ValueError:
                            ag.status = AgentStatus.online
                        if current_job:
                            job_uuid = uuid.UUID(current_job)
                            ag.current_job_id = job_uuid
                            # Renew the lease on this agent's running job so the reaper
                            # doesn't requeue live work (scoped to job + owner + running).
                            await db.execute(
                                update(ScanJob)
                                .where(
                                    ScanJob.id == job_uuid,
                                    ScanJob.agent_id == agent_id,
                                    ScanJob.status == ScanJobStatus.running,
                                )
                                .values(lease_expires_at=datetime.now(timezone.utc)
                                        + timedelta(seconds=get_settings().job_lease_seconds))
                            )
                        await db.commit()

            elif msg_type == "result":
                job_id_str = data.get("job_id", "")
                success = data.get("success", False)
                result_dict = data.get("result", {})
                error_str = data.get("error")

                try:
                    job_uuid = uuid.UUID(job_id_str)
                except (ValueError, AttributeError):
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Invalid job_id: {job_id_str}",
                    })
                    continue

                # Process result via shared service (same logic as HTTP path)
                async with AsyncSessionLocal() as db:
                    from app.services.job_result_service import process_job_result
                    summary = await process_job_result(
                        db, uuid.UUID(agent_id), job_uuid,
                        success, result_dict, error_str,
                    )
                    await db.commit()

                await websocket.send_json({
                    "type": "result_ack",
                    "job_id": job_id_str,
                    "assets_promoted": summary.get("assets_promoted", 0),
                    "findings_created": summary.get("findings_created", 0),
                })

                # Mark agent back to online after result
                await agent_ws_manager.record_heartbeat(agent_id, "online", None)

            elif msg_type == "job_ack":
                job_id_str = data.get("job_id", "")
                accepted = data.get("accepted", False)
                claimed = False
                reason = "declined"

                try:
                    job_uuid = uuid.UUID(job_id_str)
                except (ValueError, TypeError, AttributeError):
                    reason = "invalid_job_id"
                else:
                    if accepted:
                        try:
                            async with AsyncSessionLocal() as db:
                                claimed, reason = await _claim_pushed_job(
                                    db, agent_id, tenant_id, job_uuid,
                                )
                        except Exception as exc:
                            reason = "claim_error"
                            logger.error(
                                "agent.ws.job_claim_error",
                                agent_id=agent_id,
                                job_id=job_id_str,
                                error=str(exc),
                            )

                # This confirmation is the execution barrier: current probes do
                # not run an offered job unless and until claimed is true.
                await websocket.send_json({
                    "type": "job_claim",
                    "job_id": job_id_str,
                    "claimed": claimed,
                    "reason": reason,
                })

                if claimed:
                    logger.info(
                        "agent.ws.job_accepted",
                        agent_id=agent_id,
                        job_id=job_id_str,
                    )
                    await agent_ws_manager.record_heartbeat(
                        agent_id, "busy", job_id_str,
                    )
                else:
                    logger.info(
                        "agent.ws.job_rejected",
                        agent_id=agent_id,
                        job_id=job_id_str,
                        reason=reason,
                    )
                    await agent_ws_manager.record_heartbeat(
                        agent_id, "online", None,
                    )

            elif msg_type == "hello":
                features = data.get("features") or []
                if not isinstance(features, list):
                    features = []
                await agent_ws_manager.record_features(agent_id, features)

            else:
                logger.debug("agent.ws.unknown_message",
                            agent_id=agent_id, type=msg_type)

    except WebSocketDisconnect:
        logger.info("agent.ws.disconnect", agent_id=agent_id)
    except Exception as exc:
        logger.error("agent.ws.error", agent_id=agent_id, error=str(exc))
    finally:
        removed = await agent_ws_manager.unregister(agent_id, websocket)
        if removed:
            # Only the handler that removed the current socket may persist
            # offline. A displaced handler can finish after a reconnect.
            try:
                async with AsyncSessionLocal() as db:
                    ag = (await db.execute(
                        select(Agent).where(Agent.id == agent_id)
                    )).scalar_one_or_none()
                    if ag:
                        ag.status = AgentStatus.offline
                        await db.commit()
            except Exception:
                pass
