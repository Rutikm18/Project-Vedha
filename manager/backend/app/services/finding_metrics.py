"""
finding_metrics.py — mobilization metrics over the findings lifecycle.

Detection answers "what is wrong". These answer "are we actually fixing it, and
who is on the hook" — the half of a VA programme that turns a report into work.

Pure aggregation: every input already exists on the Finding model. `first_seen`
is written by the detection run that first produced a finding; `resolved_at` by
the coverage-gated auto-resolver or a manual close. Nothing here needs new schema.

The functions are kept free of database access on purpose, so the definition of
MTTR is unit-testable against hand-built pairs rather than only through a router
with a mocked session. The router does the querying; this decides the arithmetic.
"""
from __future__ import annotations

from datetime import datetime


def compute_mttr(pairs: list[tuple[datetime | None, datetime | None]]) -> dict:
    """Mean time to remediate, over findings that ACTUALLY CLOSED.

    `pairs` is (first_seen, resolved_at) per closed finding.

    Only closed findings count. Including still-open ones as "elapsed so far"
    would make the number drop whenever a new finding appears and climb as the
    backlog ages — a metric that moves for reasons unrelated to remediation speed
    is worse than no metric.

    Dirty pairs (missing either timestamp, or resolved before first seen) are
    DROPPED rather than clamped to zero. Clamping would quietly drag the mean
    toward zero and make remediation look faster than it was; dropping keeps
    `count` honest about how much was actually measurable.
    """
    durations = [
        (resolved - seen).total_seconds() / 3600.0
        for seen, resolved in pairs
        if seen is not None and resolved is not None and resolved >= seen
    ]
    if not durations:
        return {"count": 0, "mttr_hours": 0.0, "mttr_days": 0.0}
    mean_hours = sum(durations) / len(durations)
    return {
        "count": len(durations),
        "mttr_hours": round(mean_hours, 2),
        "mttr_days": round(mean_hours / 24.0, 3),
    }
