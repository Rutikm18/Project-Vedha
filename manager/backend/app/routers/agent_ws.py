"""
agent_ws.py — WebSocket endpoint for probe push connectivity.

Probes connect via wss://manager/agents/ws?token=<JWT>, and the manager
pushes scan jobs directly over this persistent connection instead of the
probe polling HTTP every 10s. The probe also sends heartbeats and submits
results over the same WebSocket.

Architecture:
  - /agents/ws  — WebSocket endpoint (mounted under /agents prefix)
  - Auth via JWT in query param (validated on connect, role must be "agent")
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
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from sqlalchemy import select, update

from app.auth.jwt import decode_token
from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.agent import Agent, AgentStatus
from app.models.scan_job import ScanJob, ScanJobStatus
from app.websocket.manager import agent_ws_manager

logger = structlog.get_logger()
router = APIRouter(prefix="/agents", tags=["agent-websocket"])


# ── WebSocket endpoint ────────────────────────────────────────────────────────

@router.websocket("/ws")
async def agent_websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """Persistent WebSocket for probe → manager push communication.

    Query params:
        token: JWT access token (role must be "agent").

    Protocol (JSON frames):

    PROBE → MANAGER:
        {"type":"hello","agent_id":"...","token":"..."}
        {"type":"heartbeat","status":"online"|"busy","current_job_id":"..."}
        {"type":"result","job_id":"...","success":bool,"result":{...},"error":"..."}
        {"type":"job_ack","job_id":"...","accepted":bool}

    MANAGER → PROBE:
        {"type":"hello_ok"}
        {"type":"error","message":"..."}
        {"type":"job_push","job":{"job_id":"...","engagement_id":"...","job_type":"...","params":{...}}}
        {"type":"result_ack","job_id":"..."}
    """
    # ── Validate token ────────────────────────────────────────────────────
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

    # ── Verify agent record ───────────────────────────────────────────────
    async with AsyncSessionLocal() as db:
        agent = (await db.execute(
            select(Agent).where(Agent.id == agent_id)
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
        await websocket.send_json({"type": "hello_ok"})

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

                if accepted:
                    # Assign the job to this agent in the DB
                    try:
                        job_uuid = uuid.UUID(job_id_str)
                    except (ValueError, AttributeError):
                        continue

                    # Atomic claim: only this agent wins the row, and only if it
                    # is still unassigned. The WHERE agent_id IS NULL guard makes
                    # the UPDATE conditional, so a concurrent HTTP poll (which uses
                    # FOR UPDATE SKIP LOCKED) can't also grab the same job. We act
                    # on rowcount instead of a read-then-write, closing the race.
                    async with AsyncSessionLocal() as db:
                        claimed = (await db.execute(
                            update(ScanJob)
                            .where(
                                ScanJob.id == job_uuid,
                                ScanJob.agent_id.is_(None),
                            )
                            .values(
                                agent_id=agent_id,
                                status=ScanJobStatus.running,
                                started_at=datetime.now(timezone.utc),
                                lease_expires_at=datetime.now(timezone.utc)
                                + timedelta(seconds=get_settings().job_lease_seconds),
                            )
                        )).rowcount
                        await db.commit()
                        if claimed:
                            logger.info(
                                "agent.ws.job_accepted",
                                agent_id=agent_id, job_id=job_id_str,
                            )
                        else:
                            logger.info(
                                "agent.ws.job_claim_lost",
                                agent_id=agent_id, job_id=job_id_str,
                            )

                await agent_ws_manager.record_heartbeat(agent_id, "busy", job_id_str)

            elif msg_type == "hello":
                # Re-auth — probe re-sent hello (shouldn't normally happen)
                pass

            else:
                logger.debug("agent.ws.unknown_message",
                            agent_id=agent_id, type=msg_type)

    except WebSocketDisconnect:
        logger.info("agent.ws.disconnect", agent_id=agent_id)
    except Exception as exc:
        logger.error("agent.ws.error", agent_id=agent_id, error=str(exc))
    finally:
        await agent_ws_manager.unregister(agent_id)
        # Mark agent offline in DB (best-effort)
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
