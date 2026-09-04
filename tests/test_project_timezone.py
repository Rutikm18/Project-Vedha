"""
Project timestamps render in IST, and stay timezone-AWARE while doing it.

Operators read scan directory names, run.log lines and the timestamps inside
result files. Rendering those in UTC made every reading a translation exercise
("the scan I watched at 17:31 is filed under 12:01"). The project renders local
time instead — IST by default, `VEDHA_TZ` to override.

The safety property these tests exist to protect: the values are AWARE
(`...+05:30`), never naive local strings. An aware timestamp is still an exact
instant — it sorts correctly against the UTC rows already in the database and
round-trips through Postgres `timestamptz` unchanged. Naive local strings would
silently corrupt ordering and break interop, which is a much worse bug than the
readability one being fixed.
"""
from __future__ import annotations

import importlib
from datetime import datetime, timedelta, timezone

import pytest

from scanner import scanner_base as sb


class TestProjectTimezone:
    def test_default_is_ist(self):
        assert sb.project_now().utcoffset() == timedelta(hours=5, minutes=30)

    def test_timestamp_is_iso_with_offset_not_naive(self):
        ts = sb.project_timestamp()
        assert ts.endswith("+05:30"), ts
        assert datetime.fromisoformat(ts).tzinfo is not None

    def test_timestamp_is_the_same_instant_as_utc(self):
        """Rendering moved; the instant did not."""
        local = datetime.fromisoformat(sb.project_timestamp())
        drift = abs((local - datetime.now(timezone.utc)).total_seconds())
        assert drift < 5, f"instant drifted by {drift}s — that is a real bug"

    def test_aware_timestamps_still_compare_against_utc(self):
        """The ordering guarantee that makes this change safe."""
        before = datetime.now(timezone.utc) - timedelta(seconds=1)
        after = datetime.now(timezone.utc) + timedelta(seconds=1)
        local = datetime.fromisoformat(sb.project_timestamp())
        assert before < local < after


class TestFileStamps:
    def test_file_stamp_has_no_z_suffix(self):
        """A `Z` on a local-time stamp is an outright lie."""
        assert not sb.project_file_stamp().endswith("Z")

    def test_file_stamp_is_local_wall_clock(self):
        assert sb.project_file_stamp() == sb.project_now().strftime("%Y%m%dT%H%M%S")

    def test_file_stamp_is_filename_safe(self):
        stamp = sb.project_file_stamp()
        assert not (set(stamp) & set('/\\:*?"<>| +'))

    def test_file_stamp_sorts_chronologically(self):
        a = sb.project_now()
        b = a + timedelta(minutes=1)
        assert a.strftime("%Y%m%dT%H%M%S") < b.strftime("%Y%m%dT%H%M%S")

    def test_custom_format_is_honoured(self):
        assert len(sb.project_file_stamp("%Y%m%d")) == 8


class TestScanResultUsesProjectTime:
    def test_scan_result_timestamp_is_ist(self):
        """The timestamp that ends up inside every result file."""
        r = sb.ScanResult("port_scan", "192.168.1.65", status="open", port=445)
        assert r.timestamp.endswith("+05:30"), r.timestamp
        assert datetime.fromisoformat(r.timestamp).tzinfo is not None


class TestOverrideAndFallback:
    def test_vedha_tz_overrides_the_default(self, monkeypatch):
        monkeypatch.setenv("VEDHA_TZ", "UTC")
        assert importlib.reload(sb).project_now().utcoffset() == timedelta(0)
        monkeypatch.delenv("VEDHA_TZ")
        importlib.reload(sb)            # restore for the rest of the session

    def test_unknown_zone_falls_back_without_crashing(self, monkeypatch):
        """A bad VEDHA_TZ must never take a scan down mid-engagement."""
        monkeypatch.setenv("VEDHA_TZ", "Not/AZone")
        assert importlib.reload(sb).project_now().tzinfo is not None
        monkeypatch.delenv("VEDHA_TZ")
        importlib.reload(sb)

    def test_ist_survives_a_missing_tzdata(self, monkeypatch):
        """Sealed/slim images may ship no tzdata. IST has no DST, so the fixed
        +05:30 fallback is an EXACT stand-in rather than an approximation."""
        monkeypatch.setattr(sb, "ZoneInfo", None)
        assert sb._resolve_project_tz().utcoffset(None) == timedelta(hours=5, minutes=30)
