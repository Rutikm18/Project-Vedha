"""
portal_metrics.py — pure aggregations for the customer dashboard.

Kept pure (no DB, no request) so the dashboard's numbers are unit-testable in
isolation; the route just fetches scoped findings and feeds them in. Mirrors the
shape of services/posture.FindingView.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

_SEVERITIES = ("critical", "high", "medium", "low", "info")
# Statuses that mean "no longer an active exposure" for the customer's open/closed
# split. Everything else (open, confirmed) counts as open.
_CLOSED_STATUSES = frozenset({"remediated", "accepted", "fp"})


@dataclass
class MetricFinding:
    severity: str
    status: str
    first_seen: datetime | None
    resolved_at: datetime | None


def _is_closed(f: MetricFinding) -> bool:
    return f.status in _CLOSED_STATUSES or f.resolved_at is not None


def severity_breakdown(findings: list[MetricFinding], *, open_only: bool = True) -> dict[str, int]:
    """Count findings by severity (all five buckets always present, zero-filled).
    open_only restricts to still-open findings — what a customer acts on."""
    counts = Counter()
    for f in findings:
        if open_only and _is_closed(f):
            continue
        sev = f.severity if f.severity in _SEVERITIES else "info"
        counts[sev] += 1
    return {sev: counts.get(sev, 0) for sev in _SEVERITIES}


def open_closed_counts(findings: list[MetricFinding]) -> tuple[int, int]:
    """(open, closed) totals over the given findings."""
    closed = sum(1 for f in findings if _is_closed(f))
    return len(findings) - closed, closed


def _period(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


def status_timeline(findings: list[MetricFinding], *, months: int = 6,
                    now: datetime | None = None) -> list[dict]:
    """Per-month {period, opened, closed} for the last `months` months.

    opened = first_seen fell in that month; closed = resolved_at fell in that
    month. Months with no activity are still emitted (zero-filled) so the line
    chart has a continuous x-axis.
    """
    now = now or datetime.now(timezone.utc)
    # Build the ordered list of the last `months` YYYY-MM labels, oldest first.
    labels: list[str] = []
    y, m = now.year, now.month
    for _ in range(months):
        labels.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    labels.reverse()
    label_set = set(labels)

    opened = Counter()
    closed = Counter()
    for f in findings:
        if f.first_seen is not None:
            p = _period(f.first_seen)
            if p in label_set:
                opened[p] += 1
        if f.resolved_at is not None:
            p = _period(f.resolved_at)
            if p in label_set:
                closed[p] += 1
    return [{"period": p, "opened": opened.get(p, 0), "closed": closed.get(p, 0)}
            for p in labels]
