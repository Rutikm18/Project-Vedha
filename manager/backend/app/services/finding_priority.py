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


# ── Response priority (P0-P5) ────────────────────────────────────────────────
# Severity says how bad the weakness is. Priority says what to do first. They were
# the same thing in practice: the frontend relabelled severity (Critical -> P0,
# High -> P1, Medium -> P2, else P3) and the backend never computed a priority.
#
# The rules below are evaluated top to bottom; the FIRST match wins. They are data,
# not code paths, so the explanation can show every rule and which one fired, and
# changing a threshold is a one-line edit here.
PRIORITY_LABELS: dict[str, str] = {
    "P0": "Immediate", "P1": "Urgent", "P2": "Planned",
    "P3": "Monitor", "P4": "Low", "P5": "Informational",
}
STRONG_EPSS = 0.50      # EPSS at or above this counts as a strong exploit signal

PRIORITY_RULES: list[tuple[str, str, str]] = [
    # (id, priority, plain-language condition)
    ("exploited_high_impact", "P0", "Known exploited (CISA KEV or validated) and severity is Critical or High"),
    ("critical_past_sla", "P0", "Severity is Critical and the SLA is breached"),
    ("critical", "P1", "Severity is Critical"),
    ("exploited", "P1", "Known exploited (CISA KEV or validated) at any other severity"),
    ("high_strong_epss", "P1", f"Severity is High and EPSS is at least {STRONG_EPSS:.2f}"),
    ("high", "P2", "Severity is High"),
    ("medium_strong_epss", "P2", f"Severity is Medium and EPSS is at least {STRONG_EPSS:.2f}"),
    ("medium", "P3", "Severity is Medium"),
    ("low", "P4", "Severity is Low"),
    ("info", "P5", "Severity is Informational (also the fallback for an unrecognised severity)"),
]


def _rule_matches(rule_id: str, *, sev: str, exploited: bool, epss: float | None, sla_breached: bool) -> bool:
    strong = epss is not None and epss >= STRONG_EPSS
    return {
        "exploited_high_impact": exploited and sev in ("critical", "high"),
        "critical_past_sla": sev == "critical" and sla_breached,
        "critical": sev == "critical",
        "exploited": exploited,
        "high_strong_epss": sev == "high" and strong,
        "high": sev == "high",
        "medium_strong_epss": sev == "medium" and strong,
        "medium": sev == "medium",
        "low": sev == "low",
        "info": True,
    }[rule_id]


def explain_priority(*, severity: Any, kev: bool, exploit_validated: bool,
                     epss_score: float | None, sla_state: str | None, status: Any = None) -> dict:
    """The response priority of one finding and the rule that decided it.

    ``sla_state`` is the SLA engine's state (``breached`` | ``at_risk`` | ``due_soon``
    | ``on_track`` | ``untracked``); only ``breached`` matters here. Asset context
    and exposure shape the 0-1000 score, not this label.

    Priority is the order to RESPOND in, so it applies to findings still owned by the
    operator (open or confirmed, the same set the SLA clock tracks). A remediated,
    accepted or false-positive finding has no response left to prioritise: it gets
    ``priority: None`` rather than a misleading "P0 Immediate".
    """
    status_value = str(getattr(status, "value", status) or "").lower()
    if status is not None and status_value not in ("open", "confirmed"):
        return {"priority": None, "label": None, "rule": "closed",
                "reason": "Closed findings (remediated, accepted or false positive) have no response priority",
                "inputs": {"status": status_value}, "rules": []}
    sev = str(getattr(severity, "value", severity) or "info").lower()
    if sev not in SEVERITY_RANK:
        sev = "info"
    exploited = bool(kev) or bool(exploit_validated)
    breached = sla_state == "breached"
    inputs = {"severity": sev, "exploited": exploited, "kev": bool(kev),
              "exploit_validated": bool(exploit_validated),
              "epss": epss_score, "sla_state": sla_state or "untracked"}
    rules, fired = [], None
    for rule_id, priority, condition in PRIORITY_RULES:
        matched = _rule_matches(rule_id, sev=sev, exploited=exploited, epss=epss_score, sla_breached=breached)
        won = matched and fired is None
        if won:
            fired = (rule_id, priority, condition)
        rules.append({"id": rule_id, "priority": priority, "condition": condition,
                      "matched": matched, "decisive": won})
    assert fired is not None    # the final rule always matches
    return {"priority": fired[1], "label": PRIORITY_LABELS[fired[1]], "rule": fired[0],
            "reason": fired[2], "inputs": inputs, "rules": rules}
