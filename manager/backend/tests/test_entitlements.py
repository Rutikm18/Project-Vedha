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
                expires_at=NOW + timedelta(days=13, hours=1), scan_quota=None,
                scans_used=3, license_key=None, notes=None, engagement_id=uuid.uuid4(),
                stealth_quota=None, normal_quota=10, aggressive_quota=0, deep_quota=2,
                stealth_used=0, normal_used=3, aggressive_used=0, deep_used=0,
                deep_repeat_policy="distinct", deep_scanned_targets=[])
    base.update(kw)
    return SimpleNamespace(**base)


class TestEvaluate:
    def test_unconfigured(self):
        v = ent.evaluate(None, now=NOW)
        assert v.state == "unconfigured" and not v.can_scan
        assert "activate" in v.reason.lower()
        assert not any(m.can_scan for m in v.modes.values())

    def test_per_mode_allowances(self):
        v = ent.evaluate(_row(), now=NOW)
        assert v.state == "active" and v.can_scan
        assert v.days_left == 14          # partial day rounds up: 13d 1h → 14
        assert v.modes["stealth"].left is None and v.modes["stealth"].can_scan   # unlimited
        assert v.modes["normal"].left == 7
        assert not v.modes["aggressive"].enabled and not v.modes["aggressive"].can_scan
        assert "aren't included" in v.modes["aggressive"].reason
        assert v.modes["deep"].left == 2

    def test_one_mode_used_up_leaves_the_others(self):
        v = ent.evaluate(_row(normal_quota=3, normal_used=3), now=NOW)
        assert v.state == "active"
        assert not v.modes["normal"].can_scan and "normal scans" in v.modes["normal"].reason
        assert v.modes["stealth"].can_scan

    def test_overall_cap_blocks_every_mode(self):
        v = ent.evaluate(_row(scan_quota=3, scans_used=3), now=NOW)
        assert v.state == "exhausted" and not v.can_scan
        assert not any(m.can_scan for m in v.modes.values())

    def test_exhausted_when_no_mode_has_anything_left(self):
        v = ent.evaluate(_row(stealth_quota=0, normal_quota=3, normal_used=3,
                              deep_quota=1, deep_used=1), now=NOW)
        assert v.state == "exhausted" and not v.can_scan

    def test_expired_blocks_every_mode_with_the_plan_reason(self):
        v = ent.evaluate(_row(expires_at=NOW - timedelta(seconds=1)), now=NOW)
        assert v.state == "expired" and v.days_left == 0
        assert all("expired" in m.reason for m in v.modes.values())

    def test_not_started(self):
        v = ent.evaluate(_row(starts_at=NOW + timedelta(days=2)), now=NOW)
        assert v.state == "not_started" and not v.can_scan

    def test_quota_lowered_below_usage_never_goes_negative(self):
        v = ent.evaluate(_row(normal_quota=2, normal_used=5), now=NOW)
        assert v.modes["normal"].left == 0

    def test_licence_key_hidden_while_on_a_poc(self):
        assert ent.evaluate(_row(plan_type="poc", license_key="VDH-X"), now=NOW).license_key is None
        assert ent.evaluate(_row(plan_type="licensed", license_key="VDH-X"), now=NOW).license_key == "VDH-X"

    def test_view_dict_is_plain(self):
        d = ent.view_dict(ent.evaluate(_row(), now=NOW))
        assert d["modes"]["deep"]["left"] == 2 and d["deep_repeat_policy"] == "distinct"


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
    def test_consume_increments_mode_and_total_under_a_row_lock(self):
        row = _row()
        db = _db_with(row)
        asyncio.run(ent.consume_scan(db, row.engagement_id, "normal", now=NOW))
        assert row.normal_used == 4 and row.scans_used == 4
        stmt = db.execute.await_args.args[0]
        assert stmt._for_update_arg is not None     # SELECT … FOR UPDATE

    @pytest.mark.parametrize("row,mode", [
        (None, "normal"),
        (_row(expires_at=NOW - timedelta(hours=1)), "stealth"),
        (_row(normal_quota=3, normal_used=3), "normal"),
        (_row(), "aggressive"),                      # not in the plan
        (_row(scan_quota=3, scans_used=3), "stealth"),
        (_row(starts_at=NOW + timedelta(hours=1)), "normal"),
    ])
    def test_refused_states_are_403_and_do_not_increment(self, row, mode):
        db = _db_with(row)
        before = getattr(row, "scans_used", None)
        with pytest.raises(HTTPException) as e:
            asyncio.run(ent.consume_scan(db, uuid.uuid4(), mode, now=NOW))
        assert e.value.status_code == 403
        assert getattr(row, "scans_used", None) == before

    def test_deep_records_the_asset(self):
        row = _row()
        asyncio.run(ent.consume_scan(_db_with(row), row.engagement_id, "deep",
                                     deep_target="10.0.0.5/32", now=NOW))
        assert row.deep_used == 1 and row.deep_scanned_targets == ["10.0.0.5/32"]

    def test_distinct_policy_refuses_the_same_asset_twice(self):
        row = _row(deep_scanned_targets=["10.0.0.5/32"], deep_used=1)
        with pytest.raises(HTTPException) as e:
            asyncio.run(ent.consume_scan(_db_with(row), row.engagement_id, "deep",
                                         deep_target="10.0.0.5/32", now=NOW))
        assert e.value.status_code == 403 and "different asset" in e.value.detail
        assert row.deep_used == 1
        asyncio.run(ent.consume_scan(_db_with(row), row.engagement_id, "deep",
                                     deep_target="10.0.0.6/32", now=NOW))
        assert row.deep_scanned_targets == ["10.0.0.5/32", "10.0.0.6/32"]

    def test_repeat_policy_allows_the_same_asset(self):
        row = _row(deep_repeat_policy="repeat", deep_scanned_targets=["10.0.0.5/32"], deep_used=1)
        asyncio.run(ent.consume_scan(_db_with(row), row.engagement_id, "deep",
                                     deep_target="10.0.0.5/32", now=NOW))
        assert row.deep_used == 2

    def test_deep_without_a_target_is_a_programming_error(self):
        with pytest.raises(ValueError):
            asyncio.run(ent.consume_scan(_db_with(_row()), uuid.uuid4(), "deep", now=NOW))


class TestRefund:
    def test_refund_request_once_to_its_mode(self):
        row = _row(scans_used=4, normal_used=4)
        sr = SimpleNamespace(engagement_id=row.engagement_id, quota_consumed=True,
                             quota_mode="normal", targets=None)
        db = _db_with(row)
        asyncio.run(ent.refund_for_request(db, sr))
        assert row.scans_used == 3 and row.normal_used == 3 and sr.quota_consumed is False
        asyncio.run(ent.refund_for_request(db, sr))  # second call is a no-op
        assert row.scans_used == 3

    def test_deep_refund_releases_the_asset(self):
        row = _row(deep_used=2, deep_scanned_targets=["10.0.0.5/32", "10.0.0.6/32"])
        job = SimpleNamespace(engagement_id=row.engagement_id,
                              result={"_quota_consumed": True, "_quota_mode": "deep",
                                      "_deep_target": "10.0.0.6/32"})
        db = _db_with(row)
        asyncio.run(ent.refund_for_job(db, job))
        assert row.deep_used == 1 and row.deep_scanned_targets == ["10.0.0.5/32"]
        assert job.result["_quota_consumed"] is False
        asyncio.run(ent.refund_for_job(db, job))
        assert row.deep_used == 1

    def test_legacy_spend_without_a_mode_refunds_the_total_only(self):
        row = _row(scans_used=1, normal_used=3)
        sr = SimpleNamespace(engagement_id=row.engagement_id, quota_consumed=True)
        asyncio.run(ent.refund_for_request(_db_with(row), sr))
        assert row.scans_used == 0 and row.normal_used == 3

    def test_operator_job_is_never_refunded(self):
        db = _db_with(_row())
        job = SimpleNamespace(engagement_id=uuid.uuid4(), result={"mode": "scan"})
        asyncio.run(ent.refund_for_job(db, job))
        db.execute.assert_not_awaited()

    def test_refund_never_goes_below_zero(self):
        row = _row(scans_used=0, normal_used=0)
        sr = SimpleNamespace(engagement_id=row.engagement_id, quota_consumed=True,
                             quota_mode="normal")
        asyncio.run(ent.refund_for_request(_db_with(row), sr))
        assert row.scans_used == 0 and row.normal_used == 0


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


class TestPerModeConfiguration:
    def test_per_mode_quotas_and_deep_policy_are_saved(self):
        row = _fresh()
        ca.apply_entitlement_config(row, ca.EntitlementConfig(
            plan_type="poc", duration_days=14, stealth_quota=None, normal_quota=10,
            aggressive_quota=2, deep_quota=3, deep_repeat_policy="repeat"), now=NOW)
        assert (row.stealth_quota, row.normal_quota, row.aggressive_quota, row.deep_quota) \
            == (None, 10, 2, 3)
        assert row.deep_repeat_policy == "repeat"

    def test_aggressive_and_deep_are_opt_in_by_default(self):
        cfg = ca.EntitlementConfig(plan_type="licensed")
        assert cfg.aggressive_quota == 0 and cfg.deep_quota == 0
        assert cfg.stealth_quota is None and cfg.normal_quota is None
        assert cfg.deep_repeat_policy == "distinct"

    def test_adjust_adds_to_one_mode_and_can_switch_it_on(self, monkeypatch):
        monkeypatch.setattr(ca, "get_or_404", AsyncMock())
        row = _fresh()
        ca.apply_entitlement_config(row, ca.EntitlementConfig(
            plan_type="licensed", normal_quota=5), now=NOW)
        out = asyncio.run(ca.adjust_entitlement(
            uuid.uuid4(), ca.EntitlementAdjust(add_scans=2, mode="deep"), _route_db(row), _operator()))
        assert row.deep_quota == 2 and out.modes["deep"].enabled
        asyncio.run(ca.adjust_entitlement(
            uuid.uuid4(), ca.EntitlementAdjust(add_scans=1, mode="stealth"), _route_db(row), _operator()))
        assert row.stealth_quota is None            # unlimited stays unlimited

    def test_reset_clears_every_counter_and_the_deep_history(self, monkeypatch):
        monkeypatch.setattr(ca, "get_or_404", AsyncMock())
        row = _fresh()
        ca.apply_entitlement_config(row, ca.EntitlementConfig(plan_type="licensed", deep_quota=1), now=NOW)
        row.scans_used, row.deep_used, row.normal_used = 3, 1, 2
        row.deep_scanned_targets = ["10.0.0.5/32"]
        asyncio.run(ca.adjust_entitlement(
            uuid.uuid4(), ca.EntitlementAdjust(reset_usage=True), _route_db(row), _operator()))
        assert (row.scans_used, row.deep_used, row.normal_used) == (0, 0, 0)
        assert row.deep_scanned_targets == []


def test_approved_deep_request_carries_its_mode_and_asset_to_the_job():
    eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
    sr = SimpleNamespace(id=uuid.uuid4(), scan_type="deep_port_sweep", requested_by=None,
                         quota_consumed=True, quota_mode="deep", targets=["10.0.0.5/32"],
                         intensity="deep", use_case_id="uc_deep_port_sweep")
    result = ca.build_scan_job(sr, eng).result
    assert result["_quota_mode"] == "deep" and result["_deep_target"] == "10.0.0.5/32"
    assert result["targets"] == ["10.0.0.5/32"] and result["intensity"] == "deep"


def test_used_up_wording_is_grammatical():
    one = ent.evaluate(_row(aggressive_quota=1, aggressive_used=1), now=NOW)
    assert one.modes["aggressive"].reason.startswith("You've used your 1 aggressive scan in")
    many = ent.evaluate(_row(normal_quota=3, normal_used=3), now=NOW)
    assert many.modes["normal"].reason.startswith("You've used all 3 normal scans in")
    total = ent.evaluate(_row(scan_quota=1, scans_used=1), now=NOW)
    assert total.reason.startswith("You've used your 1 scan in your POC")
