"""test_sla_policy.py — per-tenant custom SLA windows (item 4)."""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from app.models.enums import FindingSeverity, FindingStatus
from app.routers import sla_policy as sp
from app.schemas.auth import CurrentUser
from app.services import sla


def _finding(hours_ago):
    now = datetime.now(timezone.utc)
    ts = now - timedelta(hours=hours_ago)
    return SimpleNamespace(id=uuid.uuid4(), title="crit", severity=FindingSeverity.critical,
                           status=FindingStatus.open, first_seen=ts, created_at=ts)


class TestPolicyAwareCompute:
    def test_default_window_breaches(self):
        assert sla.compute(_finding(30)).state == "breached"      # env critical = 24h

    def test_custom_window_relaxes_state(self):
        wide = {"critical": 168, "high": 72, "medium": 168, "low": 720, "info": 0}
        assert sla.compute(_finding(30), windows=wide).state == "on_track"


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _db(row):
    db = MagicMock()
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=row)
    db.execute = AsyncMock(return_value=r)
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


def _row(**kw):
    base = dict(critical_hours=1, high_hours=2, medium_hours=3, low_hours=4, info_hours=5)
    base.update(kw)
    return SimpleNamespace(**base)


class TestSlaPolicyRoutes:
    def test_get_env_defaults_when_no_row(self):
        res = asyncio.run(sp.get_sla_policy(_db(None), _operator()))
        assert res.is_custom is False
        assert res.critical_hours == sla.default_windows()["critical"]

    def test_get_custom_when_row_present(self):
        res = asyncio.run(sp.get_sla_policy(_db(_row()), _operator()))
        assert res.is_custom is True
        assert res.critical_hours == 1 and res.info_hours == 5

    def test_put_creates_when_absent(self):
        db = _db(None)
        body = sp.SlaPolicyIn(critical_hours=12, high_hours=48, medium_hours=100,
                              low_hours=500, info_hours=0)
        res = asyncio.run(sp.put_sla_policy(body, db, _operator()))
        assert res.is_custom is True and res.critical_hours == 12
        assert db.add.called

    def test_resolve_windows_fallback_and_custom(self):
        assert asyncio.run(sp.resolve_windows(_db(None), uuid.uuid4())) == sla.default_windows()
        assert asyncio.run(sp.resolve_windows(_db(_row()), uuid.uuid4()))["critical"] == 1
