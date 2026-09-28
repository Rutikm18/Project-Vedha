"""
test_portal_scan_policy.py — the customer portal may run stealth or normal
scans only. Aggressive (the `deep` preset) is blocked server-side on every
portal path, including the ways it could be reached without saying "deep":
a use case whose default is deep, a numeric code, or raw rate/concurrency
overrides that rebuild an aggressive envelope.
"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.services import portal_scan_policy as policy


class TestResolvePortalIntensity:
    @pytest.mark.parametrize("value,expected", [
        ("stealth", "light"), ("normal", "standard"),
        ("light", "light"), ("standard", "standard"),
        (1, "light"), (2, "standard"), ("2", "standard"),
    ])
    def test_allowed_values_resolve(self, value, expected):
        assert policy.resolve_portal_intensity(value, use_case_id=None) == expected

    @pytest.mark.parametrize("value", ["aggressive", "deep", "DEEP", 3, "3"])
    def test_aggressive_is_forbidden(self, value):
        with pytest.raises(HTTPException) as e:
            policy.resolve_portal_intensity(value, use_case_id=None)
        assert e.value.status_code == 403
        assert "aggressive" in e.value.detail.lower()

    def test_unknown_value_is_422(self):
        with pytest.raises(HTTPException) as e:
            policy.resolve_portal_intensity("turbo", use_case_id=None)
        assert e.value.status_code == 422

    def test_unset_defaults_to_normal_never_to_probe_default(self):
        # Always materialized, so the probe can never fall back to a deep preset.
        assert policy.resolve_portal_intensity(None, use_case_id=None) == "standard"
        assert policy.resolve_portal_intensity("", use_case_id=None) == "standard"

    def test_unset_uses_an_allowed_use_case_default(self):
        assert policy.resolve_portal_intensity(
            None, use_case_id="uc_device_inventory") == "standard"

    def test_unset_with_deep_default_use_case_is_forbidden(self):
        with pytest.raises(HTTPException) as e:
            policy.resolve_portal_intensity(None, use_case_id="uc_full_port_audit")
        assert e.value.status_code == 403

    def test_explicit_normal_cannot_launder_a_deep_only_use_case(self):
        # A deep-only use case is not offered on the portal at all.
        with pytest.raises(HTTPException) as e:
            policy.resolve_portal_intensity("normal", use_case_id="uc_deep_port_sweep")
        assert e.value.status_code == 403


class TestStripTuningOverrides:
    def test_removes_every_probe_tuning_key(self):
        params = {"rate": 5000, "concurrency": 900, "timeout": 0.1, "retries": 0,
                  "disc_timeout": 0.1, "max_host_seconds": 99999,
                  "allow_degraded_kernel": True, "allow_infeasible": True,
                  "targets": ["10.0.0.1"], "note": "x"}
        out = policy.strip_tuning_overrides(params)
        assert out == {"targets": ["10.0.0.1"], "note": "x"}
        assert params["rate"] == 5000          # input not mutated


class TestCatalogueFilter:
    def test_deep_default_use_cases_are_not_offered(self):
        assert not policy.portal_use_case_allowed("uc_full_port_audit")
        assert not policy.portal_use_case_allowed("uc_deep_port_sweep")

    def test_normal_use_cases_are_offered(self):
        assert policy.portal_use_case_allowed("uc_device_inventory")
        assert policy.portal_use_case_allowed("uc_discovery_only")
