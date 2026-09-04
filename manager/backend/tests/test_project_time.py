"""
Manager-side project time: render in IST, stay timezone-AWARE.

The manager stores instants and must keep doing so — 88 call sites use
`datetime.now(timezone.utc)` and Postgres `timestamptz` keeps an instant
regardless of the offset it was written with. Only RENDERING moves to IST.

The specific defect fixed alongside this: `app/websocket/manager.py` pushed
`datetime.utcnow().isoformat()` to clients — a NAIVE string with no offset at
all, so a client could not tell what zone it was in. Ambiguous on the wire, and
deprecated since 3.12.
"""
from __future__ import annotations

import importlib
from datetime import datetime, timedelta, timezone

import pytest

from app.services import project_time as pt


class TestRendering:
    def test_default_is_ist(self):
        assert pt.project_now().utcoffset() == timedelta(hours=5, minutes=30)

    def test_timestamp_carries_an_offset(self):
        ts = pt.project_timestamp()
        assert ts.endswith("+05:30"), ts
        assert datetime.fromisoformat(ts).tzinfo is not None, "must never be naive"

    def test_same_instant_as_utc(self):
        drift = abs((datetime.fromisoformat(pt.project_timestamp())
                     - datetime.now(timezone.utc)).total_seconds())
        assert drift < 5, "rendering moved; the instant must not"

    def test_still_orders_against_utc_rows(self):
        """The property that makes this safe next to existing UTC data."""
        before = datetime.now(timezone.utc) - timedelta(seconds=1)
        after = datetime.now(timezone.utc) + timedelta(seconds=1)
        assert before < datetime.fromisoformat(pt.project_timestamp()) < after


class TestToProjectTz:
    def test_naive_is_assumed_utc(self):
        """Every naive datetime in this codebase's history came from utcnow().
        Assuming local instead would shift historical rows by 5h30m."""
        out = pt.to_project_tz(datetime(2026, 9, 3, 12, 0, 0))
        assert out.isoformat() == "2026-09-03T17:30:00+05:30"

    def test_aware_input_keeps_its_instant(self):
        src = datetime(2026, 9, 3, 12, 0, tzinfo=timezone.utc)
        out = pt.to_project_tz(src)
        assert out == src and out.utcoffset() == timedelta(hours=5, minutes=30)

    def test_none_passes_through(self):
        assert pt.to_project_tz(None) is None


class TestFileStamp:
    def test_no_z_suffix_on_local_time(self):
        assert not pt.project_file_stamp().endswith("Z")

    def test_filename_safe(self):
        assert not (set(pt.project_file_stamp()) & set('/\\:*?"<>| '))


class TestOverrideAndFallback:
    def test_vedha_tz_override(self, monkeypatch):
        monkeypatch.setenv("VEDHA_TZ", "UTC")
        assert importlib.reload(pt).project_now().utcoffset() == timedelta(0)
        monkeypatch.delenv("VEDHA_TZ")
        importlib.reload(pt)

    def test_bad_zone_does_not_crash_the_api(self, monkeypatch):
        monkeypatch.setenv("VEDHA_TZ", "Not/AZone")
        assert importlib.reload(pt).project_now().tzinfo is not None
        monkeypatch.delenv("VEDHA_TZ")
        importlib.reload(pt)

    def test_ist_survives_missing_tzdata(self, monkeypatch):
        monkeypatch.setattr(pt, "ZoneInfo", None)
        assert pt._resolve_project_tz().utcoffset(None) == timedelta(hours=5, minutes=30)


def test_websocket_no_longer_emits_naive_timestamps():
    """Guards the actual bug: utcnow() strings carried no offset."""
    src = (__import__("pathlib").Path(__file__).resolve().parent.parent
           / "app" / "websocket" / "manager.py").read_text()
    assert "utcnow()" not in src, "utcnow() emits a naive, ambiguous timestamp"
