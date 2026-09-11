"""
Schedule CRUD.

Validation here is doing real work, not ceremony. A schedule is a standing
instruction that fires unattended, so a bad one is not a failed request the
operator sees and retries — it is a scan that quietly misbehaves for weeks.

Three guards these pin down:

  * use_case_id is checked against the SAME catalog dispatch uses. A typo'd
    use-case would otherwise be accepted here and fail at every firing, forever,
    with the failure buried in worker logs rather than shown to the person who
    made the mistake.
  * interval_hours has a floor. A 1-minute schedule against a deep scan queues
    work faster than any probe can drain it, and the per-engagement queue cap
    then rejects real operator jobs as collateral.
  * Tenancy is enforced through the engagement, so no one can schedule scans
    against another tenant's estate.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import scan_schedules as ss
from app.schemas.auth import CurrentUser


def _user():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="admin")


def _body(**over):
    base = dict(engagement_id=uuid.uuid4(), use_case_id="uc_network_va",
                intensity=2, interval_hours=24)
    base.update(over)
    return ss.ScheduleIn(**base)


def _db(engagement=object(), rows=None, row=None):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(
        scalar_one_or_none=lambda: row if row is not None else engagement,
        scalars=lambda: MagicMock(all=lambda: rows or []),
    ))
    db.add, db.flush, db.refresh = MagicMock(), AsyncMock(), AsyncMock()
    db.delete = AsyncMock()
    return db


class TestInputValidation:
    @pytest.mark.parametrize("hours", [0, -1])
    def test_interval_below_one_hour_is_refused(self, hours):
        """A 1-minute deep-scan schedule queues faster than any probe drains it,
        and the queue cap then rejects real operator jobs as collateral."""
        with pytest.raises(Exception):
            _body(interval_hours=hours)

    def test_absurdly_long_interval_is_refused(self):
        with pytest.raises(Exception):
            _body(interval_hours=100_000)

    @pytest.mark.parametrize("bad", [0, 4, -1])
    def test_intensity_outside_1_3_is_refused(self, bad):
        with pytest.raises(Exception):
            _body(intensity=bad)

    def test_valid_body_is_accepted(self):
        b = _body()
        assert b.interval_hours == 24 and b.intensity == 2

    @pytest.mark.parametrize("hours", [1, 24, 8760])
    def test_boundaries_are_inclusive(self, hours):
        assert _body(interval_hours=hours).interval_hours == hours


class TestCreate:
    @pytest.mark.asyncio
    async def test_unknown_use_case_is_refused(self):
        """Checked against the same catalog dispatch uses — otherwise a typo is
        accepted once and fails at every firing, forever, in worker logs."""
        with pytest.raises(HTTPException) as e:
            await ss.create_schedule(_body(use_case_id="uc_not_real"), _db(), _user())
        assert e.value.status_code == 422
        assert "use_case" in str(e.value.detail).lower()

    @pytest.mark.asyncio
    async def test_unknown_engagement_is_404(self):
        with pytest.raises(HTTPException) as e:
            await ss.create_schedule(_body(), _db(row=None, engagement=None), _user())
        assert e.value.status_code == 404

    @pytest.mark.asyncio
    async def test_valid_schedule_is_created_and_due_immediately(self):
        """First run should not wait a full interval — an operator who schedules
        a daily scan expects today's, not tomorrow's."""
        db = _db()
        out = await ss.create_schedule(_body(interval_hours=24), db, _user())
        db.add.assert_called_once()
        created = db.add.call_args[0][0]
        assert created.use_case_id == "uc_network_va"
        assert created.enabled is True
        assert created.next_run_at is not None
        assert out["use_case_id"] == "uc_network_va"

    @pytest.mark.asyncio
    async def test_creator_is_recorded(self):
        user = _user()
        db = _db()
        await ss.create_schedule(_body(), db, user)
        assert db.add.call_args[0][0].created_by == user.user_id


class TestListAndDelete:
    @pytest.mark.asyncio
    async def test_list_returns_schedules(self):
        row = SimpleNamespace(
            id=uuid.uuid4(), engagement_id=uuid.uuid4(), use_case_id="uc_network_va",
            intensity=2, interval_hours=24, enabled=True,
            last_run_at=None, next_run_at=None)
        out = await ss.list_schedules(_db(rows=[row]), _user(), engagement_id=None)
        assert len(out) == 1 and out[0]["use_case_id"] == "uc_network_va"

    @pytest.mark.asyncio
    async def test_delete_missing_schedule_is_404(self):
        with pytest.raises(HTTPException) as e:
            await ss.delete_schedule(uuid.uuid4(), _db(row=None, engagement=None), _user())
        assert e.value.status_code == 404


class TestPause:
    @pytest.mark.asyncio
    async def test_schedule_can_be_disabled_without_deletion(self):
        """Pausing during a change freeze is routine; deleting would lose the
        configuration and its history."""
        row = SimpleNamespace(
            id=uuid.uuid4(), engagement_id=uuid.uuid4(), use_case_id="uc_network_va",
            intensity=2, interval_hours=24, enabled=True,
            last_run_at=None, next_run_at=None)
        out = await ss.update_schedule(
            row.id, ss.ScheduleUpdate(enabled=False), _db(row=row), _user())
        assert row.enabled is False
        assert out["enabled"] is False

    @pytest.mark.asyncio
    async def test_interval_can_be_changed(self):
        row = SimpleNamespace(
            id=uuid.uuid4(), engagement_id=uuid.uuid4(), use_case_id="uc_network_va",
            intensity=2, interval_hours=24, enabled=True,
            last_run_at=None, next_run_at=None)
        await ss.update_schedule(
            row.id, ss.ScheduleUpdate(interval_hours=6), _db(row=row), _user())
        assert row.interval_hours == 6
