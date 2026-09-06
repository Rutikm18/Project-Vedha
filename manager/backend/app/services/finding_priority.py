"""finding_priority.py — the single definition of *finding urgency ordering*.

"Critical always on top" is a hard product rule: a critical finding must never be
displayed below a lower-severity one, no matter how the composite risk score
shakes out. Without a tier gate this breaks — a KEV-listed, actively-exploited
*high* can out-score an ordinary *critical* on the 0–1000 composite and jump above
it in the list, which reads as "the tool buried a critical" to an operator.

So ordering is **severity tier first**, and only *within* a tier do we break ties
by the composite risk. This module keeps that tier definition in exactly one place,
consumed by both:

  * the SQL list query — ``severity_order_case(Finding.severity).desc()`` as the
    primary ORDER BY key, and
  * any in-memory ordering / tests — ``priority_key(severity, risk)``,

so the database sort and the Python sort can never silently diverge.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import case

from app.models.enums import FindingSeverity

# Higher = more urgent. Small dense integers: the tier value always dominates the
# fractional/0–1000 risk score when the two are composed into one sort key.
SEVERITY_RANK: dict[str, int] = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "info": 1,
}


def severity_rank(severity: Any) -> int:
    """Rank a severity (enum member or string, any case). Unknown/None → 0 (last).

    Accepts both the ``FindingSeverity`` enum and raw strings so the same helper
    works on ORM rows, Pydantic values, and test fixtures without callers having
    to normalize first.
    """
    value = getattr(severity, "value", severity)
    return SEVERITY_RANK.get(str(value).lower(), 0)


def priority_key(severity: Any, risk: float | int | None = 0.0) -> tuple[int, float]:
    """In-memory urgency key: ``(severity_tier, composite_risk)``.

    Sort with ``sorted(items, key=lambda f: priority_key(f.severity, f.risk),
    reverse=True)`` to reproduce exactly what the dashboard shows — criticals
    first, then risk within each tier. Mirrors ``severity_order_case`` in SQL.
    """
    return (severity_rank(severity), float(risk or 0.0))


def severity_order_case(severity_column: Any):
    """A SQLAlchemy CASE mapping a severity column to its tier rank.

    Use it as the primary ORDER BY key:
    ``query.order_by(severity_order_case(Finding.severity).desc(), risk.desc())``.

    Takes the column as an argument instead of importing the model, so this stays
    a leaf module with no import cycle back into ``app.models``/routers.
    """
    return case(
        (severity_column == FindingSeverity.critical, SEVERITY_RANK["critical"]),
        (severity_column == FindingSeverity.high, SEVERITY_RANK["high"]),
        (severity_column == FindingSeverity.medium, SEVERITY_RANK["medium"]),
        (severity_column == FindingSeverity.low, SEVERITY_RANK["low"]),
        (severity_column == FindingSeverity.info, SEVERITY_RANK["info"]),
        else_=0,
    )
