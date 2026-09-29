"""
test_portal_scan_policy.py — how a portal scan maps to a scan type (the
allowance it spends), and the rules that hold whatever the plan says: full-port
coverage only as a Deep scan on exactly one in-scope asset, an always-explicit
intensity, and no raw rate/concurrency overrides.
"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.services import portal_scan_policy as policy


class TestResolvePortalMode:
    @pytest.mark.parametrize("value,expected", [
        ("stealth", ("stealth", "light")), ("light", ("stealth", "light")), (1, ("stealth", "light")),
        ("normal", ("normal", "standard")), ("standard", ("normal", "standard")), ("2", ("normal", "standard")),
        ("aggressive", ("aggressive", "deep")), ("deep", ("aggressive", "deep")), (3, ("aggressive", "deep")),
    ])
    def test_intensity_maps_to_a_scan_type(self, value, expected):
        assert policy.resolve_portal_mode(value, use_case_id=None) == expected

    def test_unknown_value_is_422(self):
        with pytest.raises(HTTPException) as e:
            policy.resolve_portal_mode("turbo", use_case_id=None)
        assert e.value.status_code == 422

    def test_unset_is_materialized_never_left_to_the_probe(self):
        assert policy.resolve_portal_mode(None, use_case_id=None) == ("normal", "standard")
        assert policy.resolve_portal_mode("", use_case_id="uc_device_inventory") == ("normal", "standard")

    @pytest.mark.parametrize("uc", ["uc_full_port_audit", "uc_deep_port_sweep"])
    @pytest.mark.parametrize("value", [None, "stealth", "aggressive"])
    def test_full_port_use_cases_only_run_as_a_deep_scan(self, uc, value):
        with pytest.raises(HTTPException) as e:
            policy.resolve_portal_mode(value, use_case_id=uc)
        assert e.value.status_code == 403 and "Deep scan" in e.value.detail


class TestValidateDeepTarget:
    SCOPE = ["10.0.0.0/24"]

    @pytest.mark.parametrize("given", [["10.0.0.5"], ["10.0.0.5/32"], [" 10.0.0.5 "]])
    def test_one_in_scope_host(self, given):
        assert policy.validate_deep_target(given, self.SCOPE, []) == "10.0.0.5/32"

    @pytest.mark.parametrize("given,phrase", [
        ([], "exactly one asset"),
        (["10.0.0.5", "10.0.0.6"], "exactly one asset"),
        (["10.0.0.0/30"], "is a range"),
        (["10.0.0.0/24"], "is a range"),
        (["not-an-ip"], "isn't an IP"),
        (["192.0.2.9"], "outside your authorized scope"),
    ])
    def test_refusals(self, given, phrase):
        with pytest.raises(HTTPException) as e:
            policy.validate_deep_target(given, self.SCOPE, [])
        assert e.value.status_code == 422 and phrase in e.value.detail

    def test_excluded_host_is_refused(self):
        with pytest.raises(HTTPException):
            policy.validate_deep_target(["10.0.0.5"], self.SCOPE, ["10.0.0.0/28"])


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
    def test_full_port_use_cases_are_reached_through_deep_scan(self):
        assert not policy.portal_use_case_allowed("uc_full_port_audit")
        assert not policy.portal_use_case_allowed("uc_deep_port_sweep")

    def test_normal_use_cases_are_offered(self):
        assert policy.portal_use_case_allowed("uc_device_inventory")
        assert policy.portal_use_case_allowed("uc_network_va")
