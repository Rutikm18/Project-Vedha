"""
audit_retention.py — remove audit entries older than each organisation's retention period.

Runs daily in the worker process (next to the outbox consumer, reaper and watchers). For
each tenant it reads the organisation's audit policy, deletes what is past it (never under
the 180-day floor, see services/audit_integrity), and records what it did as an audit entry
of its own. Entries leave oldest-first, so the hash chain stays verifiable from the first one
that remains.
"""
from __future__ import annotations

import asyncio

import structlog
from sqlalchemy import select

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.services import audit as audit_service
from app.services import audit_integrity, org_settings

logger = structlog.get_logger()


async def purge_once() -> int:
    """One pass over every tenant (and the platform chain). Returns entries removed."""
    removed_total = 0
    async with AsyncSessionLocal() as db:
        tenant_ids = list((await db.execute(select(Tenant.id))).scalars().all())

    for tenant_id in [*tenant_ids, None]:
        try:
            async with AsyncSessionLocal() as db:
                days = None
                if tenant_id is not None:
                    policy = await org_settings.get_section(db, tenant_id, "audit")
                    days = policy.retention_days
                removed = await audit_integrity.purge_expired(db, tenant_id, days)
                if removed:
                    audit_service.record_audit(
                        db, actor_id="system", actor_type="system", tenant_id=tenant_id,
                        action="audit.retention_purged", resource_type="audit_log",
                        detail={"removed": removed,
                                "retention_days": audit_integrity.clamp_retention_days(days)})
                await db.commit()
                removed_total += removed
        except Exception as exc:  # noqa: BLE001 — one tenant's failure must not stop the others
            logger.error("audit_retention.tenant_failed", tenant_id=str(tenant_id), error=str(exc))
    return removed_total


async def run_audit_retention(stop: asyncio.Event | None = None) -> None:
    stop = stop or asyncio.Event()
    interval = get_settings().audit_retention_interval_seconds
    if interval <= 0:
        logger.info("audit_retention.disabled")
        return
    logger.info("audit_retention.start", interval_s=interval)
    try:
        await asyncio.wait_for(stop.wait(), timeout=min(300, interval))
        return
    except asyncio.TimeoutError:
        pass
    while not stop.is_set():
        try:
            removed = await purge_once()
            if removed:
                logger.info("audit_retention.purged", removed=removed)
        except Exception as exc:  # noqa: BLE001 — a transient blip must not kill the loop
            logger.error("audit_retention.failed", error=str(exc))
        try:
            await asyncio.wait_for(stop.wait(), timeout=interval)
        except asyncio.TimeoutError:
            pass
    logger.info("audit_retention.stop")
