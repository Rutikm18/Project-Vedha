"""
sla_watch.py — announce findings that enter "at risk" or "breached".

SLA state is derived from time (services/sla.py), so nothing "happens" when a
finding crosses a threshold. This periodic watcher, in the same worker process as
the outbox consumer and the reaper, evaluates open findings against each tenant's
policy and sends ONE notification per tenant per run listing the findings that
newly crossed. "Newly" is decided atomically by inserting into sla_alerts with
ON CONFLICT DO NOTHING and keeping only the rows that insert, so several workers,
restarts, or a rule that was switched off at the time can never re-announce a
transition (and switching a rule on later does not flood old ones).
"""
from __future__ import annotations

import asyncio
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from types import SimpleNamespace

import structlog
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models.engagement import Engagement
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.models.sla_alert import SlaAlert
from app.routers.sla_policy import resolve_windows
from app.services import sla as sla_service
from app.services.deadlines import engagement_windows
from app.services.notification_rules import notify_event

logger = structlog.get_logger()

ALERT_STATES = ("at_risk", "breached")
BATCH = 1000
LIST_LIMIT = 10


async def new_transitions(db, now: datetime | None = None) -> dict[uuid.UUID, dict[str, list[dict]]]:
    """{tenant_id: {state: [finding summaries]}} for transitions not yet announced.
    Records them as announced in the caller's transaction."""
    now = now or datetime.now(timezone.utc)
    out: dict[uuid.UUID, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    windows_cache: dict[uuid.UUID, dict] = {}
    roe_cache: dict[uuid.UUID, dict | None] = {}
    last_id: uuid.UUID | None = None

    while True:
        q = (select(Finding, Engagement.tenant_id, Engagement.rules_of_engagement)
             .join(Engagement, Finding.engagement_id == Engagement.id)
             .where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
             .order_by(Finding.id).limit(BATCH))
        if last_id is not None:
            q = q.where(Finding.id > last_id)
        rows = (await db.execute(q)).all()
        if not rows:
            break
        last_id = rows[-1][0].id

        candidates: list[tuple[Finding, uuid.UUID, sla_service.SlaResult]] = []
        for finding, tenant_id, roe in rows:
            if tenant_id not in windows_cache:
                windows_cache[tenant_id] = await resolve_windows(db, tenant_id)
            own = None
            if roe:
                own = engagement_windows(SimpleNamespace(rules_of_engagement=roe))
            result = sla_service.compute(finding, now, own if own is not None else windows_cache[tenant_id])
            if result.state in ALERT_STATES:
                candidates.append((finding, tenant_id, result))
        if not candidates:
            continue

        # Atomic "have we announced this?": only rows that insert are new.
        inserted = (await db.execute(
            pg_insert(SlaAlert)
            .values([{"finding_id": f.id, "state": r.state} for f, _t, r in candidates])
            .on_conflict_do_nothing(constraint="uq_sla_alert_finding_state")
            .returning(SlaAlert.finding_id, SlaAlert.state)
        )).all()
        fresh = {(fid, state) for fid, state in inserted}
        for finding, tenant_id, result in candidates:
            if (finding.id, result.state) in fresh:
                out[tenant_id][result.state].append({
                    "title": " ".join(str(finding.title).split())[:160],
                    "severity": result.severity,
                    "hours_remaining": result.hours_remaining,
                })
    return out


def _message(state: str, items: list[dict]) -> tuple[str, str]:
    items = sorted(items, key=lambda i: (i["hours_remaining"] if i["hours_remaining"] is not None else 0))
    n = len(items)
    if state == "breached":
        subject = f"Vedha: {n} finding{'s' if n != 1 else ''} breached the remediation SLA"
        verb = "have passed their remediation deadline"
    else:
        subject = f"Vedha: {n} finding{'s' if n != 1 else ''} at risk of missing the remediation SLA"
        verb = "are close to their remediation deadline"
    lines = []
    for item in items[:LIST_LIMIT]:
        left = item["hours_remaining"]
        when = "" if left is None else (f", {abs(left):.0f} h overdue" if left <= 0 else f", {left:.0f} h left")
        lines.append(f"- [{item['severity']}] {item['title']}{when}")
    more = f"\n…and {n - LIST_LIMIT} more" if n > LIST_LIMIT else ""
    return subject, f"{n} finding{'s' if n != 1 else ''} {verb}:\n" + "\n".join(lines) + more


async def watch_once() -> int:
    """One pass. Returns how many notifications were queued."""
    queued = 0
    async with AsyncSessionLocal() as db:
        transitions = await new_transitions(db)
        for tenant_id, by_state in transitions.items():
            for state in ALERT_STATES:
                items = by_state.get(state)
                if not items:
                    continue
                subject, body = _message(state, items)
                if await notify_event(db, tenant_id, "sla_at_risk", subject, body):
                    queued += 1
        await db.commit()
    return queued


async def run_sla_watch(stop: asyncio.Event | None = None) -> None:
    stop = stop or asyncio.Event()
    interval = get_settings().sla_watch_interval_seconds
    if interval <= 0:
        logger.info("sla_watch.disabled")
        return
    logger.info("sla_watch.start", interval_s=interval)
    # Let the API and migrations settle before the first pass.
    try:
        await asyncio.wait_for(stop.wait(), timeout=min(60, interval))
        return
    except asyncio.TimeoutError:
        pass
    while not stop.is_set():
        try:
            queued = await watch_once()
            if queued:
                logger.info("sla_watch.notified", count=queued)
        except Exception as exc:  # noqa: BLE001 — a transient blip must not kill the loop
            logger.error("sla_watch.failed", error=str(exc))
        try:
            await asyncio.wait_for(stop.wait(), timeout=interval)
        except asyncio.TimeoutError:
            pass
    logger.info("sla_watch.stop")
