"""acceptance_watch.py — an accepted risk has an expiry; when it passes, the finding comes back.

Accepting a risk now requires an owner, an expiry and a compensating control. An expiry that
nothing enforces is only a label, so this watcher (same worker process as the outbox consumer,
the reaper and the SLA watcher) reopens every accepted finding whose recorded expiry has passed,
with an immutable `reopened` event that names the owner and the terms that lapsed. The finding
then falls back under the SLA clock and the normal workflow instead of staying hidden.

An accepted finding with NO recorded expiry (accepted before terms were required) is left alone:
that is a hygiene gap the report already flags, not a deadline we can compute.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.models.finding_event import FindingEvent
from app.services import finding_events

logger = structlog.get_logger()

ACTOR = "risk-acceptance-watch"
BATCH = 500


def parse_expiry(value) -> datetime | None:
    """A timezone-aware datetime from a recorded `expires_at`, or None if absent/invalid."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo is not None else None


def latest_terms(events) -> dict | None:
    """The risk-acceptance terms from the most recent `accepted` event, or None."""
    accepted = [e for e in events if getattr(e, "event_type", None) == "accepted"
                and isinstance(getattr(e, "detail", None), dict)]
    if not accepted:
        return None
    last = max(accepted, key=lambda e: e.occurred_at)
    d = last.detail
    return {"risk_owner": d.get("risk_owner"), "expires_at": d.get("expires_at"),
            "compensating_controls": d.get("compensating_controls")}


async def reopen_expired(db, now: datetime | None = None) -> int:
    """Reopen every accepted finding whose acceptance expired. Returns how many."""
    now = now or datetime.now(timezone.utc)
    reopened = 0
    last_id: uuid.UUID | None = None
    while True:
        q = (select(Finding).where(Finding.status == FindingStatus.accepted)
             .order_by(Finding.id).limit(BATCH))
        if last_id is not None:
            q = q.where(Finding.id > last_id)
        findings = (await db.execute(q)).scalars().all()
        if not findings:
            break
        last_id = findings[-1].id
        events = (await db.execute(
            select(FindingEvent).where(
                FindingEvent.finding_id.in_([f.id for f in findings]),
                FindingEvent.event_type == "accepted")
        )).scalars().all()
        by_finding: dict[uuid.UUID, list] = {}
        for e in events:
            by_finding.setdefault(e.finding_id, []).append(e)
        for f in findings:
            terms = latest_terms(by_finding.get(f.id, []))
            expiry = parse_expiry(terms["expires_at"]) if terms else None
            if expiry is None or expiry > now:
                continue
            f.status = FindingStatus.open
            f.reopened_count = (f.reopened_count or 0) + 1
            f.resolution_miss_count = 0
            ev = dict(f.evidence) if isinstance(f.evidence, dict) else {}
            ev["risk_acceptance_expired"] = {**terms, "expired_at": now.isoformat()}
            f.evidence = ev
            await finding_events.record_event(
                db, f, "reopened", actor=ACTOR, actor_type="system",
                from_status=FindingStatus.accepted, to_status=FindingStatus.open,
                detail={"origin": "risk_acceptance_expiry", "reason": "Risk acceptance expired",
                        "reopened_count": f.reopened_count, **terms})
            reopened += 1
    await db.flush()
    return reopened


async def watch_once() -> int:
    async with AsyncSessionLocal() as db:
        n = await reopen_expired(db)
        await db.commit()
    return n


async def run_acceptance_watch(stop: asyncio.Event | None = None) -> None:
    stop = stop or asyncio.Event()
    interval = get_settings().acceptance_watch_interval_seconds
    if interval <= 0:
        logger.info("acceptance_watch.disabled")
        return
    logger.info("acceptance_watch.start", interval_s=interval)
    try:
        await asyncio.wait_for(stop.wait(), timeout=min(90, interval))
        return
    except asyncio.TimeoutError:
        pass
    while not stop.is_set():
        try:
            n = await watch_once()
            if n:
                logger.info("acceptance_watch.reopened", count=n)
        except Exception as exc:  # noqa: BLE001 — a transient blip must not kill the loop
            logger.error("acceptance_watch.failed", error=str(exc))
        try:
            await asyncio.wait_for(stop.wait(), timeout=interval)
        except asyncio.TimeoutError:
            pass
    logger.info("acceptance_watch.stop")
