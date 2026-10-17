"""Readiness flags a report whose stated assessment window does not contain the
testing it reports on (testing-round gap 13: the window ended before the scan)."""
from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

from app.services.report_document import _testing_outside_window

D = lambda day: datetime(2026, 10, day, 12, tzinfo=timezone.utc)  # noqa: E731


def _eng(start, end):
    return SimpleNamespace(start_time=start, end_time=end)


def _f(first, last):
    return SimpleNamespace(first_seen=first, last_seen=last)


def test_observation_after_the_window_is_flagged():
    assert _testing_outside_window(_eng(D(1), D(3)), [_f(D(2), D(5))])


def test_observation_before_the_window_is_flagged():
    assert _testing_outside_window(_eng(D(4), D(9)), [_f(D(2), D(5))])


def test_observations_inside_the_window_are_fine():
    assert not _testing_outside_window(_eng(D(1), D(9)), [_f(D(2), D(5))])


def test_no_window_or_no_times_is_not_a_gap():
    assert not _testing_outside_window(_eng(None, None), [_f(D(2), D(5))])
    assert not _testing_outside_window(_eng(D(1), D(3)), [_f(None, None)])


def test_naive_engagement_times_are_read_as_utc():
    naive_end = datetime(2026, 10, 3, 12)
    assert _testing_outside_window(_eng(None, naive_end), [_f(D(2), D(5))])
