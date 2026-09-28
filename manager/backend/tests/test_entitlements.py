"""
test_entitlements.py — POC / licensed plans and the portal scan quota.

The evaluation is pure (state from a row + a clock). Consumption and refunds
are tested against a mocked session: what matters is the order of checks, the
row lock, and that a refund can only ever happen once.
"""
from __future__ import annotations

import asyncio
import re
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.customer_entitlement import CustomerEntitlement
from app.routers import customer_access as ca
from app.schemas.auth import CurrentUser
from app.services import entitlements as ent

NOW = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)


def _row(**kw):
    base = dict(plan_type="poc", starts_at=NOW - timedelta(days=1),
                expires_at=NOW + timedelta(days=13, hours=1), scan_quota=10,
                scans_used=3, license_key=None, notes=None, engagement_id=uuid.uuid4())
    base.update(kw)
    return SimpleNamespace(**base)


class TestEvaluate:
    def test_unconfigured(self):
        v = ent.evaluate(None, now=NOW)
        assert v.state == "unconfigured" and not v.can_scan
        assert "activate" in v.reason.lower()

    def test_active_poc_with_quota_and_days(self):
        v = ent.evaluate(_row(), now=NOW)
        assert v.state == "active" and v.can_scan
        assert v.scans_left == 7
        assert v.days_left == 14          # partial day rounds up: 13d 1h → 14

    def test_unlimited_quota(self):
        v = ent.evaluate(_row(scan_quota=None, scans_used=500), now=NOW)
        assert v.can_scan and v.scans_left is None

    def test_no_expiry(self):
        v = ent.evaluate(_row(plan_type="licensed", expires_at=None), now=NOW)
        assert v.can_scan and v.days_left is None

    def test_expired_beats_quota(self):
        v = ent.evaluate(_row(expires_at=NOW - timedelta(seconds=1)), now=NOW)
        assert v.state == "expired" and not v.can_scan and v.days_left == 0
        assert "poc" in v.reason.lower() and "expired" in v.reason.lower()

    def test_not_started(self):
        v = ent.evaluate(_row(starts_at=NOW + timedelta(days=2)), now=NOW)
        assert v.state == "not_started" and not v.can_scan

    def test_exhausted(self):
        v = ent.evaluate(_row(scan_quota=5, scans_used=5), now=NOW)
        assert v.state == "exhausted" and not v.can_scan and v.scans_left == 0

    def test_quota_lowered_below_usage_never_goes_negative(self):
        v = ent.evaluate(_row(scan_quota=2, scans_used=5), now=NOW)
        assert v.scans_left == 0 and v.state == "exhausted"


class TestLicenseKey:
    def test_format_and_uniqueness(self):
        keys = {ent.generate_license_key() for _ in range(200)}
        assert len(keys) == 200
        assert all(re.fullmatch(r"VDH-[A-HJ-NP-Z2-9]{4}(-[A-HJ-NP-Z2-9]{4}){3}", k) for k in keys)


def _db_with(row):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
    db.flush = AsyncMock()
    return db


class TestConsume:
    def test_consume_increments_under_a_row_lock(self):
        row = _row(scans_used=3)
        db = _db_with(row)
        asyncio.run(ent.consume_scan(db, row.engagement_id, now=NOW))
        assert row.scans_used == 4
        stmt = db.execute.await_args.args[0]
        assert stmt._for_update_arg is not None     # SELECT … FOR UPDATE

    @pytest.mark.parametrize("row", [
        None,
        _row(expires_at=NOW - timedelta(hours=1)),
        _row(scan_quota=3, scans_used=3),
        _row(starts_at=NOW + timedelta(hours=1)),
    ])
    def test_refused_states_are_403_and_do_not_increment(self, row):
        db = _db_with(row)
        before = getattr(row, "scans_used", None)
        with pytest.raises(HTTPException) as e:
            asyncio.run(ent.consume_scan(db, uuid.uuid4(), now=NOW))
        assert e.value.status_code == 403
        assert getattr(row, "scans_used", None) == before


class TestRefund:
    def test_refund_request_once(self):
        row = _row(scans_used=4)
        sr = SimpleNamespace(engagement_id=row.engagement_id, quota_consumed=True)
        db = _db_with(row)
        asyncio.run(ent.refund_for_request(db, sr))
        assert row.scans_used == 3 and sr.quota_consumed is False
        asyncio.run(ent.refund_for_request(db, sr))  # second call is a no-op
        assert row.scans_used == 3

    def test_refund_job_once(self):
        row = _row(scans_used=1)
        job = SimpleNamespace(engagement_id=row.engagement_id,
                              result={"_quota_consumed": True, "mode": "scan"})
        db = _db_with(row)
        asyncio.run(ent.refund_for_job(db, job))
        assert row.scans_used == 0
        assert job.result == {"_quota_consumed": False, "mode": "scan"}
        asyncio.run(ent.refund_for_job(db, job))
        assert row.scans_used == 0

    def test_operator_job_is_never_refunded(self):
        db = _db_with(_row())
        job = SimpleNamespace(engagement_id=uuid.uuid4(), result={"mode": "scan"})
        asyncio.run(ent.refund_for_job(db, job))
        db.execute.assert_not_awaited()

    def test_refund_never_goes_below_zero(self):
        row = _row(scans_used=0)
        sr = SimpleNamespace(engagement_id=row.engagement_id, quota_consumed=True)
        asyncio.run(ent.refund_for_request(_db_with(row), sr))
        assert row.scans_used == 0


# ── operator configuration ─────────────────────────────────────────────────────


def _fresh():
    return CustomerEntitlement(tenant_id=uuid.uuid4(), engagement_id=uuid.uuid4(), scans_used=0)


class TestEntitlementConfig:
    def test_poc_requires_a_window(self):
        with pytest.raises(ValidationError):
            ca.EntitlementConfig(plan_type="poc", scan_quota=5)

    def test_duration_and_end_date_are_exclusive(self):
        with pytest.raises(ValidationError):
            ca.EntitlementConfig(plan_type="poc", duration_days=14, expires_at=NOW)

    def test_licensed_may_be_open_ended(self):
        ca.EntitlementConfig(plan_type="licensed")

    def test_poc_duration_sets_expiry_from_start(self):
        row = _fresh()
        ca.apply_entitlement_config(
            row, ca.EntitlementConfig(plan_type="poc", duration_days=14, scan_quota=10), now=NOW)
        assert row.starts_at == NOW and row.expires_at == NOW + timedelta(days=14)
        assert row.scan_quota == 10 and row.license_key is None

    def test_licensed_gets_a_key_once(self):
        row = _fresh()
        cfg = ca.EntitlementConfig(plan_type="licensed", expires_at=NOW + timedelta(days=365))
        ca.apply_entitlement_config(row, cfg, now=NOW)
        key = row.license_key
        assert key and key.startswith("VDH-")
        ca.apply_entitlement_config(row, cfg, now=NOW)
        assert row.license_key == key          # stable across re-configuration

    def test_end_before_start_is_422(self):
        row = _fresh()
        with pytest.raises(HTTPException) as e:
            ca.apply_entitlement_config(
                row, ca.EntitlementConfig(plan_type="licensed", starts_at=NOW,
                                          expires_at=NOW - timedelta(days=1)), now=NOW)
        assert e.value.status_code == 422

    def test_reconfigure_keeps_usage(self):
        row = _fresh()
        row.scans_used = 4
        ca.apply_entitlement_config(
            row, ca.EntitlementConfig(plan_type="poc", duration_days=7, scan_quota=3), now=NOW)
        assert row.scans_used == 4
        assert ent.evaluate(row, now=NOW).state == "exhausted"


def _operator():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _route_db(*scalars):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[MagicMock(scalar_one_or_none=(lambda v=v: v)) for v in scalars])
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock()
    return db


class TestOperatorRoutes:
    def test_put_creates_row_and_audits(self, monkeypatch):
        op = _operator()
        eng = SimpleNamespace(id=uuid.uuid4(), tenant_id=op.tenant_id)
        monkeypatch.setattr(ca, "get_or_404", AsyncMock(return_value=eng))
        db = _route_db(None)                   # no existing entitlement
        out = asyncio.run(ca.put_entitlement(
            eng.id, ca.EntitlementConfig(plan_type="poc", duration_days=14, scan_quota=10), db, op))
        added = [c.args[0] for c in db.add.call_args_list]
        row = next(a for a in added if isinstance(a, CustomerEntitlement))
        assert row.engagement_id == eng.id and row.tenant_id == op.tenant_id
        assert any(getattr(a, "action", None) == "entitlement.configured" for a in added)
        assert out.configured and out.state == "active" and out.scans_left == 10

    def test_adjust_needs_a_plan(self, monkeypatch):
        op = _operator()
        monkeypatch.setattr(ca, "get_or_404", AsyncMock())
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.adjust_entitlement(uuid.uuid4(), ca.EntitlementAdjust(add_scans=5),
                                              _route_db(None), op))
        assert e.value.status_code == 404

    def test_extending_an_expired_poc_counts_from_today(self, monkeypatch):
        op = _operator()
        monkeypatch.setattr(ca, "get_or_404", AsyncMock())
        row = _fresh()
        row.plan_type, row.scan_quota, row.scans_used = "poc", 5, 5
        row.starts_at = datetime.now(timezone.utc) - timedelta(days=30)
        row.expires_at = datetime.now(timezone.utc) - timedelta(days=10)
        out = asyncio.run(ca.adjust_entitlement(
            uuid.uuid4(), ca.EntitlementAdjust(add_scans=5, extend_days=7), _route_db(row), op))
        assert row.scan_quota == 10
        assert out.state == "active" and out.days_left == 7 and out.scans_left == 5
