"""portal_locks.py — the server-side guard behind portal plan locks.

A customer's plan can lock finding severities (e.g. Critical + High on a POC).
Locked findings must never reach that customer's browser — not through a list,
a group, an asset view, a fix bundle, a report or the AI assistant's context.
The portal has about twenty routes that read findings, and several reuse the
operator's handlers, so patching routes one by one would leak sooner or later.

Instead, while a customer request is being served (``require_client`` calls
``activate``), a SQLAlchemy ``do_orm_execute`` hook adds
``severity NOT IN (<locked>)`` to EVERY ORM query that touches the findings
table: whole rows, single columns, counts, subqueries and joins alike. The
value lives in a ContextVar, so it is scoped to that request's task and never
affects operator requests running concurrently.

The only deliberate exception is ``lifted()`` — used to count locked findings
for the teaser rows and to tell "locked" apart from "not found".
"""
from __future__ import annotations

import uuid
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from fastapi import HTTPException, status
from sqlalchemy import event, func, select
from sqlalchemy.orm import ORMExecuteState, Session, with_loader_criteria

from app.models.customer_entitlement import LOCKABLE_SEVERITIES
from app.models.finding import Finding

LOCKED_MESSAGE = "This finding is available on a licensed plan."
TEASER_MESSAGE = "Available on a licensed plan."
WRITTEN_REPORTS_MESSAGE = (
    "Full written reports are available on a licensed plan. The report views below cover "
    "the findings included in your plan.")
FEATURE_MESSAGES = {
    "ai_assistant": "The AI assistant is available on a licensed plan.",
    "reports": "Reports are available on a licensed plan.",
    "remediation": "Remediation plans and fix bundles are available on a licensed plan.",
    "compliance": "Compliance briefs are available on a licensed plan.",
}

_LOCKED: ContextVar[frozenset[str] | None] = ContextVar("vedha_portal_locked_severities", default=None)
_FEATURES: ContextVar[frozenset[str] | None] = ContextVar("vedha_portal_locked_features", default=None)


def activate(locked_severities: Iterable[str], locked_features: Iterable[str] = ()) -> None:
    """Apply a customer's plan locks for the rest of the current request."""
    locked = frozenset(str(s).lower() for s in locked_severities or ())
    features = frozenset(str(f).lower() for f in locked_features or ())
    _LOCKED.set(locked or None)
    _FEATURES.set(features or None)


def current() -> frozenset[str]:
    return _LOCKED.get() or frozenset()


def feature_locked(feature: str) -> bool:
    return feature in (_FEATURES.get() or frozenset())


def ensure_feature_unlocked(feature: str) -> None:
    if feature_locked(feature):
        raise HTTPException(status.HTTP_403_FORBIDDEN, FEATURE_MESSAGES[feature])


def ensure_written_reports_available() -> None:
    """Written reports are free text and can't be redacted per finding, so they
    are withheld while any severity is locked (and when Reports is locked)."""
    ensure_feature_unlocked("reports")
    if current():
        raise HTTPException(status.HTTP_403_FORBIDDEN, WRITTEN_REPORTS_MESSAGE)


async def ensure_finding_unlocked(db, finding_id: uuid.UUID, engagement_id: uuid.UUID) -> None:
    """403 for a finding the customer's plan locks. A missing finding passes, so
    the route's own 404 still applies — locked and missing stay distinguishable
    only where the customer is entitled to know (their own engagement)."""
    locked = current()
    if not locked:
        return
    with lifted():
        severity = (await db.execute(
            select(Finding.severity).where(Finding.id == finding_id,
                                           Finding.engagement_id == engagement_id)
        )).scalar_one_or_none()
    if str(getattr(severity, "value", severity)) in locked:
        raise HTTPException(status.HTTP_403_FORBIDDEN, LOCKED_MESSAGE)


async def locked_teaser(db, engagement_id: uuid.UUID) -> dict:
    """How many findings each locked severity holds — the only facts about a
    locked finding a customer may see."""
    locked = current()
    ordered = [s for s in LOCKABLE_SEVERITIES if s in locked]
    if not locked:
        return {"locked_severities": [], "counts": {}, "total": 0, "message": TEASER_MESSAGE}
    with lifted():
        rows = (await db.execute(
            select(Finding.severity, func.count())
            .where(Finding.engagement_id == engagement_id, Finding.severity.in_(ordered))
            .group_by(Finding.severity)
        )).all()
    found = {str(getattr(sev, "value", sev)): int(n) for sev, n in rows}
    counts = {s: found[s] for s in ordered if found.get(s)}
    return {"locked_severities": ordered, "counts": counts, "total": sum(counts.values()),
            "message": TEASER_MESSAGE}


@contextmanager
def lifted() -> Iterator[None]:
    """Read without the guard — only for counts of locked findings and for
    telling a locked finding apart from a missing one. Never for content."""
    token = _LOCKED.set(None)
    try:
        yield
    finally:
        _LOCKED.reset(token)


def guarded(statement):
    """The statement with the lock criteria applied, or unchanged when no
    severity is locked in this request."""
    locked = _LOCKED.get()
    if not locked:
        return statement
    values = sorted(locked)
    return statement.options(with_loader_criteria(
        Finding, lambda cls: cls.severity.notin_(values), include_aliases=True))


def _on_execute(state: ORMExecuteState) -> None:
    if state.is_select and _LOCKED.get():
        state.statement = guarded(state.statement)


# Session-class listener: AsyncSession runs on a sync Session underneath, so this
# covers every session the app creates.
if not event.contains(Session, "do_orm_execute", _on_execute):
    event.listen(Session, "do_orm_execute", _on_execute)
