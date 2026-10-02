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

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from sqlalchemy import event
from sqlalchemy.orm import ORMExecuteState, Session, with_loader_criteria

from app.models.finding import Finding

LOCKED_MESSAGE = "This finding is available on a licensed plan."

_LOCKED: ContextVar[frozenset[str] | None] = ContextVar("vedha_portal_locked_severities", default=None)


def activate(locked_severities: Iterable[str]) -> None:
    """Start hiding these severities for the rest of the current request."""
    locked = frozenset(str(s).lower() for s in locked_severities or ())
    _LOCKED.set(locked or None)


def current() -> frozenset[str]:
    return _LOCKED.get() or frozenset()


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
