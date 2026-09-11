"""
Mobilization metrics: MTTR and ownership distribution.

"No trend metrics — nothing covers MTTR" was a verified gap, but the inputs were
already there: first_seen (the run that first produced a finding) and resolved_at
(written by the auto-resolver or a manual close). This is aggregation only.

Two decisions the tests pin down:

  * MTTR counts only findings that ACTUALLY CLOSED. Including still-open findings
    as "time so far" would make the number fall every time a new finding appears
    and rise as the backlog ages — a metric that moves for reasons unrelated to
    remediation speed is worse than none.
  * Dirty pairs (resolved before first seen) are DROPPED, never clamped to zero.
    A clamp would quietly pull the mean toward zero and make remediation look
    faster than it is; dropping keeps the reported count honest about what was
    measurable.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.services.finding_metrics import compute_mttr

_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _pair(hours: float):
    return (_BASE, _BASE + timedelta(hours=hours))


class TestComputeMttr:
    def test_mean_of_two(self):
        m = compute_mttr([_pair(10), _pair(20)])
        assert m["count"] == 2
        assert m["mttr_hours"] == 15.0
        assert round(m["mttr_days"], 3) == 0.625

    def test_single_finding(self):
        m = compute_mttr([_pair(6)])
        assert m["count"] == 1 and m["mttr_hours"] == 6.0

    def test_empty_is_zero_not_a_crash(self):
        """An engagement with nothing closed yet must render, not 500."""
        m = compute_mttr([])
        assert m == {"count": 0, "mttr_hours": 0.0, "mttr_days": 0.0}

    def test_negative_durations_are_dropped_not_clamped(self):
        """Clamping to zero would quietly pull the mean down and make
        remediation look faster than it was."""
        m = compute_mttr([(_BASE, _BASE - timedelta(hours=5)), _pair(10)])
        assert m["count"] == 1
        assert m["mttr_hours"] == 10.0

    def test_none_values_are_dropped(self):
        """A finding closed before first_seen was recorded has no measurable
        duration — it must not count as instant remediation."""
        m = compute_mttr([(None, _BASE), (_BASE, None), _pair(4)])
        assert m["count"] == 1 and m["mttr_hours"] == 4.0

    def test_all_dirty_is_zero_count(self):
        m = compute_mttr([(None, None)])
        assert m["count"] == 0 and m["mttr_hours"] == 0.0

    def test_zero_duration_is_counted(self):
        """Resolved in the same instant is legitimate (a duplicate closed at
        creation) — it is not dirty data."""
        m = compute_mttr([_pair(0)])
        assert m["count"] == 1 and m["mttr_hours"] == 0.0

    def test_days_is_hours_over_24(self):
        m = compute_mttr([_pair(48)])
        assert m["mttr_days"] == 2.0


# ── the endpoint ─────────────────────────────────────────────────────────────
import uuid                                          # noqa: E402
from unittest.mock import AsyncMock, MagicMock       # noqa: E402

import pytest                                        # noqa: E402

from app.routers import findings as fr               # noqa: E402
from app.schemas.auth import CurrentUser             # noqa: E402


def _user():
    """The REAL CurrentUser — a SimpleNamespace stand-in once let an endpoint
    ship referencing a field the JWT cannot carry (see test_job_cancel.py)."""
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="admin")


def _db(pairs, owner_rows):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(all=lambda: pairs),
        MagicMock(all=lambda: owner_rows),
    ])
    return db


class TestMetricsEndpoint:
    @pytest.mark.asyncio
    async def test_shape_is_stable_when_empty(self):
        out = await fr.finding_metrics(_db([], []), _user())
        assert set(out) == {"mttr", "open_by_owner", "open_count", "resolved_count"}
        assert out["mttr"]["count"] == 0
        assert out["open_count"] == 0 and out["resolved_count"] == 0

    @pytest.mark.asyncio
    async def test_aggregates_mttr_and_owners(self):
        owner = uuid.uuid4()
        db = _db(pairs=[_pair(10), _pair(20)], owner_rows=[(owner, 3), (None, 2)])
        out = await fr.finding_metrics(db, _user())
        assert out["mttr"]["mttr_hours"] == 15.0
        assert out["resolved_count"] == 2
        assert out["open_by_owner"][str(owner)] == 3
        assert out["open_by_owner"]["unassigned"] == 2
        assert out["open_count"] == 5

    @pytest.mark.asyncio
    async def test_unassigned_is_a_first_class_bucket(self):
        """A large unassigned pile is itself the thing a manager needs to see —
        it must never be silently dropped from the breakdown."""
        out = await fr.finding_metrics(_db([], [(None, 7)]), _user())
        assert out["open_by_owner"] == {"unassigned": 7}
        assert out["open_count"] == 7
