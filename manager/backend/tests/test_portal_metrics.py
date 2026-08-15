"""test_portal_metrics.py — pure dashboard aggregations."""
from __future__ import annotations

from datetime import datetime, timezone

from app.services.portal_metrics import (
    MetricFinding,
    open_closed_counts,
    severity_breakdown,
    status_timeline,
)


def _f(severity="high", status="open", first_seen=None, resolved_at=None):
    return MetricFinding(severity=severity, status=status,
                         first_seen=first_seen, resolved_at=resolved_at)


class TestSeverityBreakdown:
    def test_all_buckets_present_zero_filled(self):
        assert severity_breakdown([]) == {
            "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

    def test_open_only_excludes_closed(self):
        findings = [_f("critical"), _f("critical", status="remediated"),
                    _f("high", resolved_at=datetime.now(timezone.utc))]
        b = severity_breakdown(findings, open_only=True)
        assert b["critical"] == 1 and b["high"] == 0

    def test_unknown_severity_falls_into_info(self):
        assert severity_breakdown([_f("bogus")])["info"] == 1


class TestOpenClosed:
    def test_counts_by_status_and_resolved_at(self):
        findings = [_f(), _f(status="confirmed"),
                    _f(status="fp"), _f(resolved_at=datetime.now(timezone.utc))]
        assert open_closed_counts(findings) == (2, 2)


class TestStatusTimeline:
    def test_emits_continuous_zero_filled_months(self):
        now = datetime(2026, 8, 15, tzinfo=timezone.utc)
        tl = status_timeline([], months=6, now=now)
        assert [p["period"] for p in tl] == [
            "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08"]
        assert all(p["opened"] == 0 and p["closed"] == 0 for p in tl)

    def test_buckets_opened_and_closed(self):
        now = datetime(2026, 8, 15, tzinfo=timezone.utc)
        findings = [
            _f(first_seen=datetime(2026, 7, 3, tzinfo=timezone.utc)),
            _f(first_seen=datetime(2026, 8, 1, tzinfo=timezone.utc),
               resolved_at=datetime(2026, 8, 9, tzinfo=timezone.utc)),
        ]
        tl = {p["period"]: p for p in status_timeline(findings, months=6, now=now)}
        assert tl["2026-07"]["opened"] == 1
        assert tl["2026-08"]["opened"] == 1 and tl["2026-08"]["closed"] == 1

    def test_activity_outside_window_is_ignored(self):
        now = datetime(2026, 8, 15, tzinfo=timezone.utc)
        old = _f(first_seen=datetime(2025, 1, 1, tzinfo=timezone.utc))
        assert all(p["opened"] == 0 for p in status_timeline([old], months=6, now=now))
