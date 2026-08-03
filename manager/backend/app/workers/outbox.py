"""
outbox.py (worker) — durable consumer for the transactional outbox.

Run as its own process:  python -m app.workers.outbox

Producers call `enqueue(db, topic, ...)` inside the SAME transaction that writes
the durable data (see app/services/job_result_service.py). This process then
claims events with FOR UPDATE SKIP LOCKED (so N workers scale out safely),
dispatches to the registered handler for the topic, and marks the event done —
or reschedules it with exponential backoff, or dead-letters it after
`max_attempts`. Nothing is lost across restarts because the queue is a table.
"""
from __future__ import annotations

import asyncio
import signal
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable

import structlog
from sqlalchemy import func, select, update

from app.database import AsyncSessionLocal
from app.models.outbox import (
    OutboxEvent, OUTBOX_PENDING, OUTBOX_PROCESSING, OUTBOX_DONE, OUTBOX_FAILED,
    TOPIC_FACTS_READY,
)

logger = structlog.get_logger()

POLL_INTERVAL_SEC = 2.0        # how often to look for work when the queue is empty
BATCH_SIZE = 16                # events claimed per poll
BACKOFF_BASE_SEC = 15          # retry delay = BACKOFF_BASE * 2**(attempts-1), capped
BACKOFF_CAP_SEC = 15 * 60
PROCESSING_LEASE_SEC = 5 * 60  # a claimed event must finish within this or be reclaimed
RECLAIM_INTERVAL_SEC = 30      # how often to sweep for stranded PROCESSING rows


def is_stale_processing(
    status: str,
    locked_at: datetime | None,
    now: datetime,
    lease_sec: float = PROCESSING_LEASE_SEC,
) -> bool:
    """Return whether a claimed event was stranded by a dead worker.

    `_claim_batch` only selects PENDING rows, so an event whose worker crashed
    between claim and completion sits in PROCESSING forever unless it is
    reclaimed. A crashed worker leaves `locked_at` in the past; once the lease
    elapses the event is fair game to requeue.
    """
    if status != OUTBOX_PROCESSING or locked_at is None:
        return False
    return (now - locked_at).total_seconds() >= lease_sec


# ── Event payload passed to handlers (plain data, detached from the session) ──

@dataclass(frozen=True)
class Event:
    id: str
    topic: str
    engagement_id: str | None
    scan_result_id: str | None
    payload: dict | None
    attempts: int


Handler = Callable[[Event], Awaitable[None]]
_HANDLERS: dict[str, Handler] = {}


def register(topic: str):
    """Decorator: bind an async handler to a topic."""
    def _wrap(fn: Handler) -> Handler:
        _HANDLERS[topic] = fn
        return fn
    return _wrap


# ── Producer API (called from request/transaction context) ────────────────────

def enqueue(db, topic: str, *, engagement_id=None, scan_result_id=None,
            payload: dict | None = None) -> OutboxEvent:
    """Add an outbox event to the caller's session. Does NOT commit — it commits
    atomically with the caller's data, which is the whole point of the pattern."""
    ev = OutboxEvent(
        topic=topic,
        engagement_id=engagement_id,
        scan_result_id=scan_result_id,
        payload=payload,
    )
    db.add(ev)
    return ev


# ── Handlers ───────────────────────────────────────────────────────────────────

@register(TOPIC_FACTS_READY)
async def _handle_facts_ready(event: Event) -> None:
    """Run the deterministic detection pipeline on a submitted facts payload.
    Re-reads the durable facts from scan_results (never carried in the event)."""
    import uuid
    from app.models.scan_result import ScanResult
    from app.detection.engine_bridge import create_findings_from_facts

    if not event.scan_result_id:
        logger.warning("outbox.facts_ready.no_scan_result", event_id=event.id)
        return

    async with AsyncSessionLocal() as db:
        sr = await db.get(ScanResult, uuid.UUID(event.scan_result_id))
        if sr is None:
            logger.warning("outbox.facts_ready.missing_scan_result",
                           scan_result_id=event.scan_result_id)
            return
        n = await create_findings_from_facts(
            db, sr.engagement_id, {"facts": sr.facts}, scan_result_id=sr.id,
        )
        await db.commit()
    logger.info("outbox.facts_ready.done",
                engagement_id=event.engagement_id, findings=n)


# ── Worker internals ───────────────────────────────────────────────────────────

async def _claim_batch(batch_size: int) -> list[Event]:
    """Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED
    means concurrent workers never grab the same row."""
    async with AsyncSessionLocal() as db:
        rows = (await db.execute(
            select(OutboxEvent)
            .where(
                OutboxEvent.status == OUTBOX_PENDING,
                OutboxEvent.available_at <= func.now(),
            )
            .order_by(OutboxEvent.created_at)
            .limit(batch_size)
            .with_for_update(skip_locked=True)
        )).scalars().all()

        now = datetime.now(timezone.utc)
        claimed: list[Event] = []
        for ev in rows:
            ev.status = OUTBOX_PROCESSING
            ev.locked_at = now
            ev.attempts += 1
            claimed.append(Event(
                id=str(ev.id),
                topic=ev.topic,
                engagement_id=str(ev.engagement_id) if ev.engagement_id else None,
                scan_result_id=str(ev.scan_result_id) if ev.scan_result_id else None,
                payload=ev.payload,
                attempts=ev.attempts,
            ))
        await db.commit()
        return claimed


def _stale_cutoff(now: datetime, lease_sec: float = PROCESSING_LEASE_SEC) -> datetime:
    """The `locked_at` boundary before which a PROCESSING row is considered dead."""
    return now - timedelta(seconds=lease_sec)


def _dead_letter_stale_stmt(cutoff: datetime):
    """Stranded events that already exhausted their retry budget → dead-letter.
    Bounded by `attempts >= max_attempts` so a poison event cannot loop forever."""
    return (
        update(OutboxEvent)
        .where(
            OutboxEvent.status == OUTBOX_PROCESSING,
            OutboxEvent.locked_at < cutoff,
            OutboxEvent.attempts >= OutboxEvent.max_attempts,
        )
        .values(
            status=OUTBOX_FAILED,
            last_error="dead-lettered after stale processing lock; attempts exhausted",
        )
    )


def _requeue_stale_stmt(cutoff: datetime):
    """Stranded events with retry budget left → make due now so a live worker
    re-claims them. `attempts` was already incremented at claim time."""
    return (
        update(OutboxEvent)
        .where(
            OutboxEvent.status == OUTBOX_PROCESSING,
            OutboxEvent.locked_at < cutoff,
            OutboxEvent.attempts < OutboxEvent.max_attempts,
        )
        .values(
            status=OUTBOX_PENDING,
            available_at=func.now(),
            last_error="requeued after stale processing lock",
        )
    )


async def _reclaim_stale() -> int:
    """Requeue events a dead worker left in PROCESSING past the lease.

    `_claim_batch` only selects PENDING rows, so without this sweep an event
    whose worker crashed mid-handler stays PROCESSING forever. Handlers must be
    idempotent (the normal retry path already re-runs them), so a duplicate run
    of reclaimed work is safe.
    """
    cutoff = _stale_cutoff(datetime.now(timezone.utc))
    async with AsyncSessionLocal() as db:
        dead = await db.execute(_dead_letter_stale_stmt(cutoff))
        requeued = await db.execute(_requeue_stale_stmt(cutoff))
        await db.commit()
    n = (dead.rowcount or 0) + (requeued.rowcount or 0)
    if n:
        logger.warning("outbox.reclaimed_stale", count=n,
                       dead_lettered=dead.rowcount or 0, requeued=requeued.rowcount or 0)
    return n


async def _mark_done(event_id: str) -> None:
    async with AsyncSessionLocal() as db:
        await db.execute(
            update(OutboxEvent).where(OutboxEvent.id == uuid.UUID(event_id))
            .values(status=OUTBOX_DONE, last_error=None)
        )
        await db.commit()


async def _mark_retry_or_dead(event: Event, error: str) -> None:
    """Reschedule with exponential backoff, or dead-letter once attempts are
    exhausted (attempts was already incremented at claim time)."""
    async with AsyncSessionLocal() as db:
        row = await db.get(OutboxEvent, uuid.UUID(event.id))
        if row is None:
            return
        if row.attempts >= row.max_attempts:
            row.status = OUTBOX_FAILED
            row.last_error = error[:2000]
            logger.error("outbox.dead_letter", event_id=event.id,
                         topic=event.topic, attempts=row.attempts, error=error)
        else:
            delay = min(BACKOFF_BASE_SEC * (2 ** (row.attempts - 1)), BACKOFF_CAP_SEC)
            row.status = OUTBOX_PENDING
            row.available_at = datetime.now(timezone.utc) + timedelta(seconds=delay)
            row.last_error = error[:2000]
            logger.warning("outbox.retry_scheduled", event_id=event.id,
                           topic=event.topic, attempt=row.attempts, retry_in_s=delay)
        await db.commit()


async def _process(event: Event) -> None:
    handler = _HANDLERS.get(event.topic)
    if handler is None:
        await _mark_retry_or_dead(event, f"no handler registered for topic {event.topic!r}")
        return
    try:
        await handler(event)
        await _mark_done(event.id)
    except Exception as exc:  # noqa: BLE001 — failure must reschedule, not crash the worker
        await _mark_retry_or_dead(event, f"{type(exc).__name__}: {exc}")


async def run_worker(stop: asyncio.Event | None = None) -> None:
    """Main loop: claim → process → repeat. Sleeps only when the queue is idle,
    so latency stays low under load and cost stays near-zero when empty."""
    stop = stop or asyncio.Event()
    logger.info("outbox.worker.start", topics=sorted(_HANDLERS.keys()))
    last_reclaim = 0.0
    while not stop.is_set():
        # Periodically requeue events stranded in PROCESSING by a crashed worker,
        # so no acknowledged-durable event is silently lost.
        if time.monotonic() - last_reclaim >= RECLAIM_INTERVAL_SEC:
            try:
                await _reclaim_stale()
            except Exception as exc:  # noqa: BLE001 — reclaim must never kill the loop
                logger.error("outbox.reclaim_failed", error=str(exc))
            last_reclaim = time.monotonic()

        try:
            events = await _claim_batch(BATCH_SIZE)
        except Exception as exc:  # noqa: BLE001 — a transient DB blip must not kill the loop
            logger.error("outbox.claim_failed", error=str(exc))
            await asyncio.sleep(POLL_INTERVAL_SEC)
            continue

        if not events:
            try:
                await asyncio.wait_for(stop.wait(), timeout=POLL_INTERVAL_SEC)
            except asyncio.TimeoutError:
                pass
            continue

        # Process the batch concurrently; each handler owns its own DB session.
        await asyncio.gather(*(_process(ev) for ev in events), return_exceptions=True)

    logger.info("outbox.worker.stop")


def main() -> None:
    stop = asyncio.Event()

    async def _run() -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, stop.set)
            except NotImplementedError:  # e.g. Windows
                pass
        # This background process runs two durable loops: the outbox consumer
        # (detection etc.) and the lease reaper (requeue jobs from dead probes).
        from app.workers.reaper import run_reaper
        await asyncio.gather(run_worker(stop), run_reaper(stop))

    asyncio.run(_run())


if __name__ == "__main__":
    main()
