"""M12 hardening — an accepted risk expires: the finding comes back, with the lapsed terms on record."""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import FindingStatus
from app.workers import acceptance_watch as W

NOW = datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc)


def _finding():
    return SimpleNamespace(id=uuid.uuid4(), status=FindingStatus.accepted, reopened_count=0,
                           resolution_miss_count=3, evidence={"rule_id": "X"})


def _event(fid, expires, **extra):
    return SimpleNamespace(finding_id=fid, event_type="accepted", occurred_at=NOW - timedelta(days=30),
                           detail={"risk_owner": "CISO", "expires_at": expires,
                                   "compensating_controls": "ACL", **extra})


def _db(findings, events):
    def res(rows):
        r = MagicMock()
        r.scalars.return_value.all.return_value = rows
        return r
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.execute = AsyncMock(side_effect=[res(findings), res(events), res([])])
    return db


def test_parse_expiry_accepts_aware_iso_and_rejects_the_rest():
    assert W.parse_expiry("2026-10-01T00:00:00+00:00") == datetime(2026, 10, 1, tzinfo=timezone.utc)
    assert W.parse_expiry("2026-10-01T00:00:00Z").tzinfo is not None
    for bad in (None, "", "not a date", "2026-10-01T00:00:00", 5):
        assert W.parse_expiry(bad) is None


def test_latest_terms_uses_the_most_recent_acceptance():
    fid = uuid.uuid4()
    old = _event(fid, "2026-01-01T00:00:00+00:00")
    old.occurred_at = NOW - timedelta(days=200)
    new = _event(fid, "2027-01-01T00:00:00+00:00")
    assert W.latest_terms([old, new])["expires_at"] == "2027-01-01T00:00:00+00:00"
    assert W.latest_terms([]) is None


@pytest.mark.asyncio
async def test_expired_acceptance_reopens_with_the_lapsed_terms_on_record():
    f = _finding()
    db = _db([f], [_event(f.id, (NOW - timedelta(days=1)).isoformat())])
    assert await W.reopen_expired(db, NOW) == 1
    assert f.status == FindingStatus.open and f.reopened_count == 1 and f.resolution_miss_count == 0
    assert f.evidence["risk_acceptance_expired"]["risk_owner"] == "CISO"
    event = db.add.call_args.args[0]
    assert event.event_type == "reopened" and event.actor == "risk-acceptance-watch"
    assert event.detail["origin"] == "risk_acceptance_expiry" and event.detail["risk_owner"] == "CISO"


@pytest.mark.asyncio
async def test_a_live_acceptance_is_left_alone():
    f = _finding()
    db = _db([f], [_event(f.id, (NOW + timedelta(days=30)).isoformat())])
    assert await W.reopen_expired(db, NOW) == 0
    assert f.status == FindingStatus.accepted
    db.add.assert_not_called()


@pytest.mark.asyncio
async def test_acceptance_without_a_recorded_expiry_is_not_guessed_at():
    legacy = _finding()
    no_terms = SimpleNamespace(finding_id=legacy.id, event_type="accepted",
                               occurred_at=NOW - timedelta(days=400), detail={"reason": "old exception"})
    db = _db([legacy], [no_terms])
    assert await W.reopen_expired(db, NOW) == 0
    assert legacy.status == FindingStatus.accepted


@pytest.mark.asyncio
async def test_watcher_is_disabled_when_interval_is_zero(monkeypatch):
    monkeypatch.setattr(W, "get_settings", lambda: SimpleNamespace(acceptance_watch_interval_seconds=0))
    await W.run_acceptance_watch()          # returns immediately, does not loop


def test_the_worker_process_starts_it():
    import inspect
    from app.workers import outbox
    assert "run_acceptance_watch" in inspect.getsource(outbox.main)
