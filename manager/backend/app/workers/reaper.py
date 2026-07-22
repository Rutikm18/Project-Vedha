"""
reaper.py — requeue jobs abandoned by a dead probe.

A job is claimed with a lease (scan_jobs.lease_expires_at) that the probe renews
on every heartbeat. If the probe crashes / loses connectivity mid-scan, the lease
expires and the job would otherwise sit in 'running' forever — never retried,
never surfaced. This periodic reaper flips such jobs back to 'pending' (clearing
agent_id / started_at / lease) so they re-enter the dispatch pool and get picked
up by the next poll or WS job_ack.

Runs inside the same background worker process as the outbox consumer
(python -m app.workers.outbox). The requeue is a single atomic UPDATE keyed on
the DB clock (func.now()), so it is safe to run from more than one worker — the
worst case is a duplicate log line, not a double requeue.
"""
from __future__ import annotations

import asyncio

import structlog
from sqlalchemy import func, update

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.scan_job import ScanJob
from app.models.enums import ScanJobStatus

logger = structlog.get_logger()


async def reap_once() -> list[str]:
    """Requeue every running job whose lease has expired. Returns the job ids."""
    async with AsyncSessionLocal() as db:
        res = await db.execute(
            update(ScanJob)
            .where(
                ScanJob.status == ScanJobStatus.running,
                ScanJob.lease_expires_at.isnot(None),
                ScanJob.lease_expires_at < func.now(),   # DB clock — no app/DB skew
            )
            .values(
                status=ScanJobStatus.pending,
                agent_id=None,
                started_at=None,
                lease_expires_at=None,
            )
            .returning(ScanJob.id)
        )
        ids = [str(row[0]) for row in res.fetchall()]
        await db.commit()
        return ids


async def run_reaper(stop: asyncio.Event | None = None) -> None:
    """Poll loop: requeue expired jobs every reaper_interval_seconds until stopped."""
    stop = stop or asyncio.Event()
    interval = get_settings().reaper_interval_seconds
    logger.info("reaper.start", interval_s=interval, lease_s=get_settings().job_lease_seconds)
    while not stop.is_set():
        try:
            requeued = await reap_once()
            if requeued:
                logger.warning("reaper.requeued", count=len(requeued), job_ids=requeued)
        except Exception as exc:  # noqa: BLE001 — a transient DB blip must not kill the loop
            logger.error("reaper.failed", error=str(exc))
        try:
            await asyncio.wait_for(stop.wait(), timeout=interval)
        except asyncio.TimeoutError:
            pass
    logger.info("reaper.stop")
