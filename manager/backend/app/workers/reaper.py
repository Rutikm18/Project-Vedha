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
from datetime import datetime, timezone

import structlog
from sqlalchemy import func, select

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.scan_job import ScanJob
from app.models.scan_job_attempt import ScanJobAttempt
from app.models.enums import ScanJobStatus

logger = structlog.get_logger()


def expire_attempt(attempt, job, now: datetime) -> bool:
    """Expire one fenced attempt; return True when the job may be retried."""
    attempt.status = "expired"
    attempt.ended_at = now
    attempt.error = "lease expired before completion"
    job.agent_id = None
    job.lease_expires_at = None
    job.current_attempt_id = None
    if job.attempt_count >= job.max_attempts:
        job.status = ScanJobStatus.failed
        job.completed_at = now
        prior = job.result if isinstance(job.result, dict) else {}
        job.result = {
            **prior,
            "error": "maximum execution attempts exhausted after lease expiry",
        }
        return False

    job.status = ScanJobStatus.pending
    job.started_at = None
    return True


async def reap_once() -> list[str]:
    """Expire current attempts and requeue only jobs within their retry budget."""
    async with AsyncSessionLocal() as db:
        rows = (await db.execute(
            select(ScanJobAttempt, ScanJob)
            .join(ScanJob, ScanJob.current_attempt_id == ScanJobAttempt.id)
            .where(
                ScanJob.status == ScanJobStatus.running,
                ScanJobAttempt.status == "running",
                ScanJobAttempt.lease_expires_at < func.now(),
            )
            .order_by(ScanJobAttempt.lease_expires_at)
            .limit(100)
            .with_for_update(of=ScanJobAttempt, skip_locked=True)
        )).all()

        now = datetime.now(timezone.utc)
        requeued: list[str] = []
        for attempt, job in rows:
            if not expire_attempt(attempt, job, now):
                logger.error(
                    "reaper.attempts_exhausted",
                    job_id=str(job.id),
                    attempt_count=job.attempt_count,
                )
            else:
                requeued.append(str(job.id))
        await db.commit()
        return requeued


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
