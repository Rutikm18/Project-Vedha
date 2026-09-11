"""
Which schedules are due, and when they run next.

Three decisions these pin down, each of which is an outage if wrong:

  * A disabled schedule is skipped WITHOUT advancing. Advancing it would let a
    paused schedule accumulate silently and then fire the instant it is
    re-enabled.
  * next_run_at advances from NOW, not from the missed due time. If the manager
    is down for two days, a 24h schedule is two intervals behind; catching up
    would fire a herd of scans at an estate that needed exactly one. For a
    vulnerability scan the current state is the only interesting state.
  * A schedule is advanced ONLY if its enqueue succeeded, and one failure never
    stops the others. Advancing a failure would silently skip the window with
    nothing in the record explaining why the estate went unscanned.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.services.scheduler import advance, due_schedules, run_due

_NOW = datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)


def _sched(*, enabled=True, due_offset_h=-1, interval=24):
    return SimpleNamespace(
        id=uuid.uuid4(), enabled=enabled, interval_hours=interval,
        next_run_at=_NOW + timedelta(hours=due_offset_h), last_run_at=None,
        engagement_id=uuid.uuid4(), use_case_id="uc_network_va", intensity=2,
    )


class TestDueSelection:
    def test_past_due_and_enabled_is_selected(self):
        s = _sched(due_offset_h=-1)
        assert due_schedules([s], _NOW) == [s]

    def test_exactly_due_is_selected(self):
        """<= not <: a schedule due this instant must fire, not wait a tick."""
        s = _sched(due_offset_h=0)
        assert due_schedules([s], _NOW) == [s]

    def test_future_is_not_selected(self):
        assert due_schedules([_sched(due_offset_h=5)], _NOW) == []

    def test_disabled_is_never_selected_even_when_overdue(self):
        assert due_schedules([_sched(enabled=False, due_offset_h=-100)], _NOW) == []

    def test_mixed_set(self):
        due, future, off = (_sched(due_offset_h=-1), _sched(due_offset_h=5),
                            _sched(enabled=False, due_offset_h=-1))
        assert due_schedules([due, future, off], _NOW) == [due]

    def test_empty(self):
        assert due_schedules([], _NOW) == []


class TestAdvance:
    def test_sets_last_run_and_next_by_interval(self):
        s = _sched(interval=12)
        advance(s, _NOW)
        assert s.last_run_at == _NOW
        assert s.next_run_at == _NOW + timedelta(hours=12)

    def test_advances_from_now_not_from_the_missed_due_time(self):
        """The catch-up-storm guard: two days late on a 24h schedule must produce
        ONE next run 24h from now, not a backlog to work through."""
        s = _sched(due_offset_h=-48, interval=24)
        advance(s, _NOW)
        assert s.next_run_at == _NOW + timedelta(hours=24)
        assert s.next_run_at > _NOW

    def test_is_never_left_in_the_past(self):
        s = _sched(due_offset_h=-1000, interval=1)
        advance(s, _NOW)
        assert s.next_run_at > _NOW


class TestRunDue:
    @pytest.mark.asyncio
    async def test_enqueues_and_advances_due_only(self):
        due, future = _sched(due_offset_h=-1), _sched(due_offset_h=5)
        enqueue = AsyncMock()
        out = await run_due([due, future], _NOW, enqueue)
        assert out["enqueued"] == 1
        enqueue.assert_awaited_once_with(due)
        assert due.next_run_at == _NOW + timedelta(hours=24)
        assert future.last_run_at is None          # untouched

    @pytest.mark.asyncio
    async def test_failed_enqueue_does_not_advance(self):
        """Advancing a failure would silently skip the window, and the estate
        would go unscanned with nothing explaining why."""
        s = _sched(due_offset_h=-1)
        original_next = s.next_run_at
        out = await run_due([s], _NOW, AsyncMock(side_effect=RuntimeError("queue full")))
        assert out["enqueued"] == 0 and len(out["failed"]) == 1
        assert s.next_run_at == original_next
        assert s.last_run_at is None

    @pytest.mark.asyncio
    async def test_one_failure_does_not_stop_the_others(self):
        """A single bad schedule must not wedge the whole fleet's scanning."""
        bad, good = _sched(due_offset_h=-1), _sched(due_offset_h=-1)
        calls = {"n": 0}

        async def _enqueue(s):
            calls["n"] += 1
            if s is bad:
                raise RuntimeError("boom")

        out = await run_due([bad, good], _NOW, _enqueue)
        assert calls["n"] == 2
        assert out["enqueued"] == 1 and len(out["failed"]) == 1
        assert good.last_run_at == _NOW and bad.last_run_at is None

    @pytest.mark.asyncio
    async def test_nothing_due_is_a_no_op(self):
        enqueue = AsyncMock()
        out = await run_due([_sched(due_offset_h=5)], _NOW, enqueue)
        assert out == {"enqueued": 0, "failed": []}
        enqueue.assert_not_awaited()
