"""
job_result_service.py — shared job result processing.
Single source of truth for what happens when a probe submits scan results.
Both the HTTP router (agents.py) and WebSocket handler (agent_ws.py) call
process_job_result().  No more copy-paste.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import AssetType, ScanJobStatus
from app.models.scan_job import ScanJob
from app.models.scan_result import ScanResult
from app.models.service import Service

logger = structlog.get_logger()


async def process_job_result(
    db: AsyncSession,
    agent_id: uuid.UUID,
    job_id: uuid.UUID,
    success: bool,
    result: dict | None,
    error: str | None,
) -> dict:
    """Process a scan job result.  Called from both HTTP and WebSocket paths.

    Returns {"ok": True, "assets_promoted": int, "findings_created": int}.
    """
    row = (await db.execute(
        select(ScanJob).where(
            ScanJob.id == job_id,
            ScanJob.agent_id == str(agent_id),
        )
    )).scalar_one_or_none()

    if not row:
        return {"ok": False, "error": "Job not found or not assigned to this agent"}

    # ── Idempotency: result submission is at-least-once ─────────────────────
    # A probe retries when it doesn't see an ACK (the ACK can be lost even after
    # we committed). Without this guard a retry appends a duplicate scan_results
    # row and re-enqueues the detection pipeline → duplicate findings. If this
    # job already reached a terminal state, treat the resubmission as a no-op
    # and return HTTP 200 so the probe clears its spool. Failed submissions are
    # retried after a lost ACK just like successful ones.
    if row.status in (ScanJobStatus.completed, ScanJobStatus.failed):
        logger.info(
            "job.result_duplicate_ignored",
            job_id=str(job_id),
            agent_id=str(agent_id),
            terminal_status=row.status.value,
        )
        return {"ok": True, "duplicate": True,
                "assets_promoted": 0, "findings_created": 0}

    # ── Update job status ──────────────────────────────────────────────────
    row.status = ScanJobStatus.completed if success else ScanJobStatus.failed
    row.completed_at = datetime.now(timezone.utc)

    result = result or {}
    facts = result.get("facts") if isinstance(result, dict) else None

    # ── Persist raw facts to the append-only scan_results table ─────────────
    scan_result_row: ScanResult | None = None
    if isinstance(facts, list) and facts:
        scan_result_row = ScanResult(
            engagement_id=row.engagement_id,
            job_id=row.id,
            scan_type=result.get("scan_type"),
            fact_count=len(facts),
            facts=facts,
        )
        db.add(scan_result_row)
        lean = {k: v for k, v in result.items() if k != "facts"}
        row.result = {**lean, "fact_count": len(facts), "error": error}
    else:
        row.result = {**result, "error": error}

    await db.flush()   # assigns scan_result_row.id (needed for the outbox event)

    # ── Promote discovered hosts ───────────────────────────────────────────
    promoted = 0
    findings_created = 0
    if success and isinstance(result, dict):
        if result.get("hosts"):
            try:
                async with db.begin_nested():
                    promoted = await _promote_assets(db, row.engagement_id, result)
            except Exception as exc:  # noqa: BLE001 — best-effort, never fail the submit
                logger.warning("job.promote_failed", job_id=str(job_id), error=str(exc))

        # ── Self-assessed findings (tls_scan, smb_enum, etc.) ─────────────
        try:
            from app.discovery.finding_translator import create_findings_from_probe_result
            async with db.begin_nested():
                findings_created = await create_findings_from_probe_result(
                    db, row.engagement_id, result,
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning("job.findings_failed", job_id=str(job_id), error=str(exc))

        # ── Durable detection via transactional outbox ─────────────────────
        # Enqueue in THIS transaction so the event commits atomically with the
        # facts above. The outbox worker (python -m app.workers.outbox) runs the
        # detection pipeline. This replaces the old asyncio.create_task, which
        # ran in-process and silently dropped work on any crash/restart between
        # the commit and the coroutine executing (no durability, retry, or DLQ).
        if scan_result_row is not None:
            from app.models.outbox import TOPIC_FACTS_READY
            from app.workers.outbox import enqueue
            enqueue(
                db, TOPIC_FACTS_READY,
                engagement_id=row.engagement_id,
                scan_result_id=scan_result_row.id,
            )

    logger.info(
        "job.result_processed",
        agent_id=str(agent_id),
        job_id=str(job_id),
        success=success,
        assets_promoted=promoted,
        findings_created=findings_created,
    )
    return {"ok": True, "assets_promoted": promoted, "findings_created": findings_created}


# ── Private helpers ─────────────────────────────────────────────────────────

async def _promote_assets(
    db: AsyncSession,
    engagement_id: uuid.UUID,
    result: dict,
) -> int:
    """Upsert discovered hosts/services into the asset inventory.

    Keyed by (engagement_id, ip) for assets and (asset, port, protocol) for
    services, so repeated scans update in place instead of duplicating.
    Returns the number of newly-created assets.
    """
    hosts = (result or {}).get("hosts") or []
    promoted = 0
    # One probe result can contain multiple facts for the same host/port
    # (for example an HTTP redirect fact plus a web fingerprint fact). Keep an
    # in-batch cache so repeated ports update one Service object instead of
    # creating two pending inserts that violate uq_service_asset_port_proto.
    service_cache: dict[tuple[uuid.UUID | None, int, str], Service] = {}

    for h in hosts:
        ip = h.get("ip")
        if not ip:
            continue

        asset = (await db.execute(
            select(Asset).where(
                Asset.engagement_id == engagement_id,
                Asset.ip_address == ip,
            )
        )).scalar_one_or_none()

        if asset:
            asset.hostname = h.get("hostname") or asset.hostname
            asset.os = h.get("os") or asset.os
            asset.last_seen = datetime.now(timezone.utc)
        else:
            asset = Asset(
                engagement_id=engagement_id,
                ip_address=ip,
                hostname=h.get("hostname"),
                os=h.get("os"),
                asset_type=AssetType.server,
                last_seen=datetime.now(timezone.utc),
            )
            db.add(asset)
            await db.flush()
            promoted += 1

        # Upsert services
        for p in h.get("ports") or []:
            port_no = p.get("port")
            if port_no is None:
                continue
            try:
                port_no = int(port_no)
            except (TypeError, ValueError):
                continue

            proto = str(p.get("protocol") or "tcp").lower()
            cpe = p.get("cpe")
            cpe_str = ",".join(cpe) if isinstance(cpe, list) else cpe
            key = (asset.id, port_no, proto)

            svc = service_cache.get(key)
            if svc is None:
                svc = (await db.execute(
                    select(Service).where(
                        Service.asset_id == asset.id,
                        Service.port == port_no,
                        Service.protocol == proto,
                    )
                )).scalar_one_or_none()

                if svc is None:
                    svc = Service(
                        asset_id=asset.id,
                        port=port_no,
                        protocol=proto,
                    )
                    db.add(svc)
                service_cache[key] = svc

            svc.service_name = p.get("service") or svc.service_name
            svc.product = p.get("product") or svc.product
            svc.version = p.get("version") or svc.version
            svc.cpe = cpe_str or svc.cpe
            svc.banner = p.get("banner") or svc.banner
            extra = p.get("extra_info") or p.get("data")
            if isinstance(extra, dict):
                svc.extra_info = {**(svc.extra_info or {}), **extra}
        await db.flush()

    return promoted
