"""Portal plan locks — which finding severities and features a customer may open.

Settings live on the customer's plan (customer_entitlements): locked_severities
and locked_features. New POC customers start with Critical + High locked; new
licensed plans and every existing customer start with nothing locked. The
operator changes either list at any time from the Plan panel.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.models.customer_entitlement import CustomerEntitlement
from app.routers import customer_access as ca
from app.services import entitlements as ent

NOW = datetime(2026, 10, 2, 12, 0, tzinfo=timezone.utc)


def _fresh():
    return CustomerEntitlement(tenant_id=uuid.uuid4(), engagement_id=uuid.uuid4(), scans_used=0)


def _poc(**kw):
    return ca.EntitlementConfig(plan_type="poc", duration_days=14, **kw)


class TestDefaults:
    def test_new_poc_locks_critical_and_high(self):
        row = _fresh()
        ca.apply_entitlement_config(row, _poc(), now=NOW)
        assert row.locked_severities == ["critical", "high"]
        assert row.locked_features == []

    def test_new_licensed_plan_locks_nothing(self):
        row = _fresh()
        ca.apply_entitlement_config(row, ca.EntitlementConfig(plan_type="licensed"), now=NOW)
        assert row.locked_severities == []
        assert row.locked_features == []

    def test_existing_customer_keeps_its_locks_when_they_are_not_sent(self):
        row = _fresh()
        row.locked_severities, row.locked_features = [], ["reports"]     # e.g. migrated row
        ca.apply_entitlement_config(row, _poc(), now=NOW)
        assert row.locked_severities == []          # access is never taken away implicitly
        assert row.locked_features == ["reports"]


class TestOperatorChanges:
    def test_explicit_locks_are_applied_in_a_stable_order(self):
        row = _fresh()
        ca.apply_entitlement_config(row, _poc(
            locked_severities=["low", "critical", "critical"],
            locked_features=["reports", "ai_assistant"]), now=NOW)
        assert row.locked_severities == ["critical", "low"]
        assert row.locked_features == ["ai_assistant", "reports"]

    def test_unlocking_everything_is_allowed_at_any_time(self):
        row = _fresh()
        ca.apply_entitlement_config(row, _poc(), now=NOW)
        ca.apply_entitlement_config(row, _poc(locked_severities=[], locked_features=[]), now=NOW)
        assert row.locked_severities == [] and row.locked_features == []

    def test_licensed_plans_can_lock_features_too(self):
        row = _fresh()
        ca.apply_entitlement_config(row, ca.EntitlementConfig(
            plan_type="licensed", locked_features=["remediation", "compliance"]), now=NOW)
        assert row.locked_features == ["compliance", "remediation"]

    @pytest.mark.parametrize("field,value", [
        ("locked_severities", ["urgent"]),
        ("locked_features", ["billing"]),
    ])
    def test_unknown_values_are_rejected(self, field, value):
        with pytest.raises(ValidationError):
            _poc(**{field: value})


class TestPortalView:
    def _row(self, **kw):
        base = dict(plan_type="poc", starts_at=NOW - timedelta(days=1), expires_at=NOW + timedelta(days=13),
                    scan_quota=None, scans_used=0, license_key=None, notes=None,
                    engagement_id=uuid.uuid4(), stealth_quota=None, normal_quota=None,
                    aggressive_quota=0, deep_quota=0, stealth_used=0, normal_used=0,
                    aggressive_used=0, deep_used=0, deep_repeat_policy="distinct",
                    deep_scanned_targets=[], locked_severities=["critical", "high"],
                    locked_features=["ai_assistant"])
        base.update(kw)
        return SimpleNamespace(**base)

    def test_view_carries_the_locks(self):
        view = ent.evaluate(self._row(), now=NOW)
        assert view.locked_severities == ["critical", "high"]
        assert view.locked_features == ["ai_assistant"]
        # Written (free-text) reports cannot be redacted per finding.
        assert view.written_reports_withheld is True

    def test_nothing_locked_means_written_reports_are_available(self):
        view = ent.evaluate(self._row(locked_severities=[]), now=NOW)
        assert view.written_reports_withheld is False

    def test_unconfigured_customer_has_no_locks(self):
        view = ent.evaluate(None, now=NOW)
        assert view.locked_severities == [] and view.locked_features == []
        assert view.written_reports_withheld is False
