"""
The "what's NEW" half of the run delta.

`/latest/delta` already answered half the question: which open findings were NOT
reaffirmed by the newest run (resolution candidates). It never answered the other
half — what APPEARED. "A new SOCKS proxy, new hosts and new ports weren't
surfaced as deltas" was the verified gap, and on a repeat assessment that is the
single most actionable line in the report.

Deliberately built on the SAME mechanism as the existing half — `first_seen` /
`last_seen` against `run.started_at` — rather than a separate run-id diff. Two
independent notions of "what changed" would drift apart, and the one that
disagreed would be silently wrong.

`first_seen >= run.started_at` means the finding was first produced BY this run.
A finding re-observed from an earlier run has an older first_seen and is
correctly not "new", even though this run reaffirmed it.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import FindingSeverity, FindingStatus
from app.routers import detection_runs as dr

_NOW = datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)


def _run(started=_NOW):
    return SimpleNamespace(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), trigger="facts_ready",
        status="completed", started_at=started, finished_at=started,
        facts_count=10, findings_new=1, findings_reaffirmed=0,
        findings_current=1, error=None, stats={}, created_at=started,
        vuln_db_version="v1", vuln_db_fetched_at=None, scan_result_id=None,
    )


def _finding(title, first_seen):
    return SimpleNamespace(
        id=uuid.uuid4(), title=title, severity=FindingSeverity.high,
        status=FindingStatus.open, last_seen=_NOW, first_seen=first_seen,
    )


class TestNewFindingsAreSurfaced:
    def test_helper_selects_only_findings_first_seen_in_this_run(self):
        """A finding carried over from an earlier run is not 'new', even though
        this run reaffirmed it."""
        run = _run()
        brand_new = _finding("new SOCKS proxy on 1080", first_seen=_NOW)
        carried_over = _finding("SMBv1 enabled", first_seen=_NOW - timedelta(days=7))
        picked = dr._select_new_since(
            [brand_new, carried_over], run_started_at=run.started_at)
        assert [f.title for f in picked] == ["new SOCKS proxy on 1080"]

    def test_finding_first_seen_exactly_at_run_start_counts_as_new(self):
        """The run's own findings share its start instant; a strict > would drop
        every one of them."""
        run = _run()
        f = _finding("exactly at start", first_seen=run.started_at)
        assert dr._select_new_since([f], run_started_at=run.started_at) == [f]

    def test_missing_first_seen_is_not_claimed_as_new(self):
        """Legacy rows predate the time series; calling them new on every rescan
        would flood the delta forever."""
        f = _finding("legacy", first_seen=None)
        assert dr._select_new_since([f], run_started_at=_NOW) == []

    def test_empty_input(self):
        assert dr._select_new_since([], run_started_at=_NOW) == []


class TestEndpointShape:
    def _db(self, run, new_rows, cand_rows):
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: run),           # newest run
            MagicMock(scalar_one=lambda: len(cand_rows)),        # candidate count
            MagicMock(scalars=lambda: MagicMock(all=lambda: cand_rows)),
            MagicMock(scalars=lambda: MagicMock(all=lambda: new_rows)),
        ])
        return db

    @pytest.mark.asyncio
    async def test_delta_reports_both_halves(self, monkeypatch):
        run = _run()
        new_rows = [_finding("new SOCKS proxy on 1080", first_seen=_NOW)]
        monkeypatch.setattr(dr, "get_or_404", AsyncMock(return_value=object()))
        # candidates_limit must be passed explicitly: calling the handler
        # directly bypasses FastAPI, so the default is still a Query object.
        out = await dr.latest_run_delta(
            run.engagement_id, self._db(run, new_rows, []),
            SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin"),
            candidates_limit=50)
        assert out["has_runs"] is True
        assert out["new_findings_count"] == 1
        assert out["new_findings"][0]["title"] == "new SOCKS proxy on 1080"
        assert "resolution_candidates" in out          # existing half intact

    @pytest.mark.asyncio
    async def test_no_runs_short_circuits_before_querying_findings(self, monkeypatch):
        monkeypatch.setattr(dr, "get_or_404", AsyncMock(return_value=object()))
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None))
        out = await dr.latest_run_delta(
            uuid.uuid4(), db,
            SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin"),
            candidates_limit=50)
        assert out == {"has_runs": False}
