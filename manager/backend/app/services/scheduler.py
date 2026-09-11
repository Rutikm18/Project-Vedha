"""
scheduler.py — decide which scan schedules are due, and advance them.

Kept as pure functions, separate from the worker that calls them, so the two
things most likely to be wrong — "is it due?" and "when next?" — are testable
without a database or a wall clock. The worker owns querying and committing;
this owns the arithmetic.

WHY ADVANCE FROM `now`, NOT FROM `next_run_at`
----------------------------------------------
If the manager is down for two days, a 24-hour schedule wakes up two intervals
behind. Advancing from the missed `next_run_at` would fire it repeatedly to
"catch up" — a thundering herd of scans against an estate that only needed one.
Advancing from `now` skips the missed windows deliberately: for a VULNERABILITY
SCAN the current state is the only interesting state, and three stale scans are
strictly worse than one fresh one.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Iterable


def due_schedules(rows: Iterable[Any], now: datetime) -> list:
    """Schedules that should fire at `now`: enabled, and past their due time.

    Disabled schedules are skipped without advancing — a paused schedule must not
    silently accumulate, then fire the moment it is re-enabled.
    """
    return [s for s in rows if s.enabled and s.next_run_at <= now]


def advance(schedule: Any, now: datetime) -> None:
    """Mark a schedule run and set its next due time.

    Deliberately `now + interval`, never `next_run_at + interval` — see the
    module docstring on catch-up storms.
    """
    schedule.last_run_at = now
    schedule.next_run_at = now + timedelta(hours=schedule.interval_hours)


async def run_due(
    rows: Iterable[Any],
    now: datetime,
    enqueue: Callable[[Any], Awaitable[Any]],
) -> dict:
    """Enqueue every due schedule, then advance it.

    `enqueue` is injected so this stays db-free and so the worker can pass the
    SAME enqueue path an operator's manual scan uses — scope validation,
    capability matching and the per-engagement queue cap must all still apply to
    a scheduled job. A schedule is not a way to bypass the rules.

    A schedule is advanced ONLY if its enqueue succeeded. Advancing a failed one
    would silently skip that window, and the estate would go unscanned with
    nothing in the record explaining why. One failure never stops the others:
    a single bad schedule must not wedge the whole fleet's scanning.
    """
    enqueued, failed = 0, []
    for schedule in due_schedules(rows, now):
        try:
            await enqueue(schedule)
        except Exception as exc:            # noqa: BLE001 - one bad schedule must not stop the rest
            failed.append((getattr(schedule, "id", None), str(exc)))
            continue
        advance(schedule, now)
        enqueued += 1
    return {"enqueued": enqueued, "failed": failed}
