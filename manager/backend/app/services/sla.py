"""
SLA policy engine.

Turns a severity + "first seen" timestamp into a remediation deadline and an
SLA state, using the per-severity windows in Settings. This is the single source
of truth for "is this finding overdue?" — the dashboard SLA widget, the header
breach chip, and any future notifier all read from here so they never disagree.

Design notes:
- The clock starts at `first_seen` (when detection first produced the finding),
  falling back to `created_at` for non-engine sources. Using first_seen keeps a
  finding's deadline stable even if the row is rewritten by a later run.
- Only open/confirmed findings carry a live SLA. Remediated/accepted/false-positive
  findings have discharged the operator's obligation, so they are not tracked.
- A window of 0 (info, by default) means "no SLA" — such findings are untracked.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.config import get_settings
from app.models.enums import FindingStatus
from app.models.finding import Finding

# Findings whose SLA clock is still running (operator still owns remediation).
_TRACKED_STATUSES = {FindingStatus.open, FindingStatus.confirmed}

# Fraction-of-window-remaining thresholds for the non-breached states.
_AT_RISK_FRACTION = 0.25   # < 25% of the window left
_DUE_SOON_FRACTION = 0.50  # < 50% of the window left


def _windows() -> dict[str, int]:
    s = get_settings()
    return {
        "critical": s.sla_hours_critical,
        "high": s.sla_hours_high,
        "medium": s.sla_hours_medium,
        "low": s.sla_hours_low,
        "info": s.sla_hours_info,
    }


@dataclass
class SlaResult:
    finding_id: str
    title: str
    severity: str
    deadline: datetime | None
    hours_remaining: float | None
    hours_total: int | None
    state: str  # breached | at_risk | due_soon | on_track | untracked

    @property
    def is_tracked(self) -> bool:
        return self.state != "untracked"


def compute(finding: Finding, now: datetime | None = None) -> SlaResult:
    """Compute the SLA state for one finding. Never raises on missing data."""
    now = now or datetime.now(timezone.utc)
    severity = finding.severity.value if hasattr(finding.severity, "value") else str(finding.severity)
    status = finding.status if isinstance(finding.status, FindingStatus) else None

    window_hours = _windows().get(severity, 0)
    started = finding.first_seen or finding.created_at

    # Untracked: closed finding, no SLA window for this severity, or no start time.
    if status not in _TRACKED_STATUSES or window_hours <= 0 or started is None:
        return SlaResult(
            finding_id=str(finding.id), title=finding.title, severity=severity,
            deadline=None, hours_remaining=None, hours_total=None, state="untracked",
        )

    # Normalize naive timestamps to UTC so arithmetic is always tz-aware.
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)

    deadline = started + timedelta(hours=window_hours)
    hours_remaining = (deadline - now).total_seconds() / 3600.0
    fraction_left = hours_remaining / window_hours

    if hours_remaining <= 0:
        state = "breached"
    elif fraction_left < _AT_RISK_FRACTION:
        state = "at_risk"
    elif fraction_left < _DUE_SOON_FRACTION:
        state = "due_soon"
    else:
        state = "on_track"

    return SlaResult(
        finding_id=str(finding.id), title=finding.title, severity=severity,
        deadline=deadline, hours_remaining=round(hours_remaining, 2),
        hours_total=window_hours, state=state,
    )


def summarize(findings: list[Finding], now: datetime | None = None, item_limit: int = 25) -> dict:
    """
    Aggregate SLA states across a set of findings.

    Returns counts per state plus the most urgent `item_limit` tracked findings
    (breached first, then by soonest deadline) for the dashboard's SLA rows.
    """
    now = now or datetime.now(timezone.utc)
    results = [compute(f, now) for f in findings]
    tracked = [r for r in results if r.is_tracked]

    counts = {"breached": 0, "at_risk": 0, "due_soon": 0, "on_track": 0}
    for r in tracked:
        counts[r.state] = counts.get(r.state, 0) + 1

    # Urgency order: breached first, then whoever is closest to (or past) deadline.
    _state_rank = {"breached": 0, "at_risk": 1, "due_soon": 2, "on_track": 3}
    tracked.sort(key=lambda r: (_state_rank[r.state], r.hours_remaining if r.hours_remaining is not None else 0))

    items = [
        {
            "finding_id": r.finding_id,
            "title": r.title,
            "severity": r.severity,
            "deadline": r.deadline,
            "hours_remaining": r.hours_remaining,
            "hours_total": r.hours_total,
            "state": r.state,
        }
        for r in tracked[:item_limit]
    ]

    return {**counts, "total_tracked": len(tracked), "items": items}
