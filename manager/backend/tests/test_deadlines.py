"""test_deadlines.py — one due-date resolver: extension > engagement > tenant > default."""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.enums import FindingSeverity, FindingStatus
from app.schemas.auth import CurrentUser
from app.services import deadlines, sla

T0 = datetime(2026, 9, 1, tzinfo=timezone.utc)
NOW = datetime(2026, 9, 3, tzinfo=timezone.utc)

_ENG_POLICY = {"critical_hours": 48, "high_hours": 96, "medium_hours": 336, "low_hours": 720,
               "info_hours": 0}


def _finding(severity="high", status=FindingStatus.open, due_at=None, engagement_id=None):
    return SimpleNamespace(id=uuid.uuid4(), title="t", severity=FindingSeverity(severity),
                           status=status, first_seen=T0, created_at=T0, due_at=due_at,
                           due_at_source="extension" if due_at else None,
                           engagement_id=engagement_id or uuid.uuid4())


def _eng(policy=None):
    roe = {"profile": {"sector": "banking"}}
    if policy is not None:
        roe["sla_policy"] = policy
    return SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), rules_of_engagement=roe)


def _db(tenant_row=None):
    db = MagicMock()
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=tenant_row)
    db.execute = AsyncMock(return_value=r)
    return db


class TestEngagementWindows:
    def test_reads_policy(self):
        assert deadlines.engagement_windows(_eng(_ENG_POLICY))["high"] == 96

    def test_absent_is_none(self):
        assert deadlines.engagement_windows(_eng()) is None

    @pytest.mark.parametrize("bad", [{"high_hours": 5}, {**_ENG_POLICY, "high_hours": -1},
                                     {**_ENG_POLICY, "high_hours": "x"}, "nope",
                                     {**_ENG_POLICY, "high_hours": 9000}])
    def test_invalid_policy_ignored(self, bad):
        assert deadlines.engagement_windows(_eng(bad)) is None


class TestPrecedence:
    def test_engagement_beats_tenant(self):
        tenant_row = SimpleNamespace(critical_hours=1, high_hours=2, medium_hours=3, low_hours=4, info_hours=0)
        w, src = asyncio.run(deadlines.windows_for(_db(tenant_row), uuid.uuid4(), _eng(_ENG_POLICY)))
        assert src == "engagement" and w["high"] == 96

    def test_tenant_beats_default(self):
        tenant_row = SimpleNamespace(critical_hours=1, high_hours=2, medium_hours=3, low_hours=4, info_hours=0)
        w, src = asyncio.run(deadlines.windows_for(_db(tenant_row), uuid.uuid4(), _eng()))
        assert src == "tenant" and w["high"] == 2

    def test_default_last(self):
        w, src = asyncio.run(deadlines.windows_for(_db(None), uuid.uuid4(), _eng()))
        assert src == "default" and w == sla.default_windows()

    def test_extension_beats_policy(self):
        ext = T0 + timedelta(days=60)
        due = deadlines.due_for(_finding(due_at=ext), {"high": 96}, "engagement")
        assert due == {"at": ext, "source": "extension"}

    def test_policy_due(self):
        due = deadlines.due_for(_finding(), {"high": 96}, "engagement")
        assert due == {"at": T0 + timedelta(hours=96), "source": "engagement"}

    def test_closed_has_no_due(self):
        due = deadlines.due_for(_finding(status=FindingStatus.remediated), {"high": 96}, "tenant")
        assert due == {"at": None, "source": None}


class TestSlaHonoursOverride:
    def test_extension_moves_deadline_and_state(self):
        f = _finding(due_at=T0 + timedelta(days=30))
        r = sla.compute(f, now=NOW, windows={"high": 24})       # policy alone would be breached
        assert r.deadline == T0 + timedelta(days=30)
        assert r.state == "on_track"

    def test_summarize_uses_engagement_windows(self):
        eid = uuid.uuid4()
        f = _finding(engagement_id=eid)                          # high, first seen 2 days ago
        out = sla.summarize([f], now=NOW, windows={"high": 24}, engagement_windows={eid: {"high": 96}})
        assert out["breached"] == 0 and out["total_tracked"] == 1


class TestEngagementPolicyRoutes:
    def _user(self, role="manager"):
        return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role=role)

    def test_put_stores_in_roe_and_keeps_profile(self):
        from app.routers import sla_policy as R
        eng = _eng()
        db = _db(eng)
        db.flush = AsyncMock()
        out = asyncio.run(R.put_engagement_sla_policy(eng.id, R.SlaPolicyIn(**_ENG_POLICY), db, self._user()))
        assert eng.rules_of_engagement["sla_policy"]["high_hours"] == 96
        assert eng.rules_of_engagement["profile"] == {"sector": "banking"}
        assert out.source == "engagement"

    def test_delete_clears(self):
        from app.routers import sla_policy as R
        eng = _eng(_ENG_POLICY)
        db = MagicMock()
        results = [MagicMock(scalar_one_or_none=MagicMock(return_value=eng)),
                   MagicMock(scalar_one_or_none=MagicMock(return_value=None))]
        db.execute = AsyncMock(side_effect=results)
        db.flush = AsyncMock()
        out = asyncio.run(R.delete_engagement_sla_policy(eng.id, db, self._user()))
        assert "sla_policy" not in eng.rules_of_engagement
        assert out.source == "default"

    def test_unknown_engagement_is_404(self):
        from app.routers import sla_policy as R
        with pytest.raises(HTTPException) as e:
            asyncio.run(R.get_engagement_sla_policy(uuid.uuid4(), _db(None), self._user()))
        assert e.value.status_code == 404

    def test_bounds(self):
        from app.routers import sla_policy as R
        with pytest.raises(ValidationError):
            R.SlaPolicyIn(**{**_ENG_POLICY, "critical_hours": 9000})


class TestSlaSummaryRoute:
    def test_engagement_override_applies(self):
        from app.routers import findings as FR
        eid = uuid.uuid4()
        f = _finding(engagement_id=eid)
        f.first_seen = f.created_at = datetime.now(timezone.utc) - timedelta(hours=30)
        rs = [MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[f])))),
              MagicMock(scalar_one_or_none=MagicMock(return_value=SimpleNamespace(
                  critical_hours=24, high_hours=24, medium_hours=24, low_hours=24, info_hours=0))),
              MagicMock(all=MagicMock(return_value=[(eid, {"sla_policy": _ENG_POLICY})]))]
        db = MagicMock()
        db.execute = AsyncMock(side_effect=rs)
        user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")
        out = asyncio.run(FR.sla_summary(db=db, current_user=user, engagement_id=eid))
        # tenant says 24h (breached at 30h); the engagement's 96h policy wins
        assert out["breached"] == 0 and out["total_tracked"] == 1
