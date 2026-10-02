"""
notification_rules.py — which events notify a tenant, and through which channels.

The catalogue below is the single list of events an operator can switch on or
off. `connected` says whether anything in the product emits that event today: the
Settings page shows the unconnected ones as "not connected yet" instead of
letting an operator believe an alert is armed when no code would ever send it.

A tenant with no stored row for an event uses the default here, so new installs
need no seeding and a new event type needs no migration. `notify_event` is the
producer API: it consults the rule and only then enqueues a durable notification
routed to the chosen channels.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Iterable

import structlog
from sqlalchemy import select

from app.models.notification_rule import NotificationRule

logger = structlog.get_logger()

# The channels the rules matrix offers. They are integration kinds
# (app.models.integration), delivered by app.services.notifications.
CHANNELS: tuple[str, ...] = ("email", "slack")


@dataclass(frozen=True)
class EventDef:
    key: str
    label: str
    cadence: str
    default_channels: tuple[str, ...]
    default_enabled: bool
    connected: bool          # does any product code emit this event today?


EVENTS: tuple[EventDef, ...] = (
    EventDef("critical_finding", "Critical finding opened", "Immediate", ("email", "slack"), True, True),
    EventDef("high_finding", "High finding opened", "Near-real-time", ("slack",), True, True),
    EventDef("sla_at_risk", "SLA enters at-risk state", "At threshold", ("email", "slack"), True, False),
    EventDef("finding_status_changed", "Finding status changed", "Digest", ("email",), False, False),
    EventDef("report_approved", "Report approved", "Immediate", ("email",), True, True),
    EventDef("probe_enrolled", "New probe enrolled", "Immediate", ("slack",), True, True),
    EventDef("coverage_gap", "Detection coverage gap found", "Immediate", ("email", "slack"), False, False),
)
_BY_KEY = {e.key: e for e in EVENTS}


class RuleError(ValueError):
    """An update names an unknown event or channel."""


def event_def(key: str) -> EventDef | None:
    return _BY_KEY.get(key)


def _ordered(channels: Iterable[str]) -> list[str]:
    wanted = set(channels)
    return [c for c in CHANNELS if c in wanted]


def _view(ev: EventDef, row: NotificationRule | None) -> dict[str, Any]:
    return {
        "event": ev.key,
        "label": ev.label,
        "cadence": ev.cadence,
        "enabled": row.enabled if row is not None else ev.default_enabled,
        "channels": _ordered(row.channels or []) if row is not None else list(ev.default_channels),
        "connected": ev.connected,
        "is_custom": row is not None,
    }


async def _rows(db: Any, tenant_id: uuid.UUID) -> dict[str, NotificationRule]:
    found = (await db.execute(
        select(NotificationRule).where(NotificationRule.tenant_id == tenant_id)
    )).scalars().all()
    return {r.event_key: r for r in found}


async def effective_rules(db: Any, tenant_id: uuid.UUID) -> list[dict[str, Any]]:
    """Every catalogue event with the tenant's choice, or the default."""
    rows = await _rows(db, tenant_id)
    return [_view(ev, rows.get(ev.key)) for ev in EVENTS]


async def save_rules(db: Any, tenant_id: uuid.UUID, updates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Upsert the given rules (validated first, so a bad request changes nothing)."""
    clean: list[tuple[EventDef, bool, list[str]]] = []
    for u in updates:
        ev = _BY_KEY.get(u.get("event", ""))
        if ev is None:
            raise RuleError(f"Unknown event '{u.get('event')}'")
        channels = list(u.get("channels") or [])
        bad = [c for c in channels if c not in CHANNELS]
        if bad:
            raise RuleError(f"Unknown channel '{bad[0]}' (use: {', '.join(CHANNELS)})")
        clean.append((ev, bool(u.get("enabled")), _ordered(channels)))

    rows = await _rows(db, tenant_id)
    for ev, enabled, channels in clean:
        row = rows.get(ev.key)
        if row is None:
            row = NotificationRule(tenant_id=tenant_id, event_key=ev.key,
                                   enabled=enabled, channels=channels)
            db.add(row)
            rows[ev.key] = row
        else:
            row.enabled = enabled
            row.channels = channels
    await db.flush()
    return [_view(ev, rows.get(ev.key)) for ev in EVENTS]


async def notify_event(db: Any, tenant_id: uuid.UUID, event_key: str,
                       subject: str, body: str) -> bool:
    """Producer API. Enqueue a notification for `event_key` if the tenant's rule
    says so, routed to the rule's channels only. Returns whether one was queued.
    The caller owns the transaction (the outbox row commits with it)."""
    ev = _BY_KEY.get(event_key)
    if ev is None:
        logger.warning("notify.unknown_event", event_key=event_key)
        return False
    rule = (await _rows(db, tenant_id)).get(event_key)
    enabled = rule.enabled if rule is not None else ev.default_enabled
    channels = _ordered(rule.channels or []) if rule is not None else list(ev.default_channels)
    if not enabled or not channels:
        return False
    from app.services.notifications import enqueue_notification
    enqueue_notification(db, tenant_id, subject, body, channels=channels, event=event_key)
    return True


async def notify_event_safe(db: Any, tenant_id: uuid.UUID, event_key: str,
                            subject: str, body: str) -> bool:
    """`notify_event` for producers that must never fail because of it (a scan
    result, an approval, an enrolment). Runs in a savepoint so a database error
    here cannot poison the caller's transaction; any failure is logged and
    swallowed."""
    try:
        async with db.begin_nested():
            return await notify_event(db, tenant_id, event_key, subject, body)
    except Exception as exc:  # noqa: BLE001 — a notification must not break its trigger
        logger.warning("notify.event_failed", event_key=event_key, error=str(exc))
        return False
