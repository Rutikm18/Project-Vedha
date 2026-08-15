"""
test_scope_targets.py — the pure scope-authorization core shared by the dispatch
gate (agents.py) and the customer-portal request gate. The highest-severity bug
class here is scope escape, so these tests are exhaustive about the boundary.
"""
from __future__ import annotations

import ipaddress

import pytest

from app.services.scope_targets import validate_targets_in_scope


class TestNoScopeAuthorizesNothing:
    @pytest.mark.parametrize("scope", [None, []])
    def test_empty_scope_denies_all(self, scope):
        assert validate_targets_in_scope(["192.0.2.10"], scope) is None
        # Even with no targets requested, no scope → nothing routable.
        assert validate_targets_in_scope(None, scope) is None


class TestTargetsWithinScope:
    def test_single_ip_in_scope(self):
        assert validate_targets_in_scope(["10.0.0.5"], ["10.0.0.0/24"]) == ["10.0.0.5/32"]

    def test_string_target_is_accepted(self):
        assert validate_targets_in_scope("10.0.0.5", ["10.0.0.0/24"]) == ["10.0.0.5/32"]

    def test_cidr_subset_in_scope(self):
        assert validate_targets_in_scope(["10.0.1.0/28"], ["10.0.0.0/16"]) == ["10.0.1.0/28"]

    def test_range_expands_to_covered_networks(self):
        assert validate_targets_in_scope(["10.0.8.10-10.0.8.20"], ["10.0.0.0/16"]) == [
            "10.0.8.10/31", "10.0.8.12/30", "10.0.8.16/30", "10.0.8.20/32",
        ]

    def test_no_targets_returns_whole_scope(self):
        assert validate_targets_in_scope(None, ["10.0.0.0/24", "192.168.1.0/24"]) == [
            "10.0.0.0/24", "192.168.1.0/24",
        ]


class TestOutOfScopeIsRejected:
    def test_ip_outside_scope(self):
        assert validate_targets_in_scope(["192.0.2.10"], ["10.0.0.0/8"]) is None

    def test_cidr_broader_than_scope(self):
        # /8 is not subnet_of a /16 — overlap is not enough.
        assert validate_targets_in_scope(["10.0.0.0/8"], ["10.0.0.0/16"]) is None

    def test_one_bad_target_rejects_the_whole_request(self):
        assert validate_targets_in_scope(
            ["10.0.0.5", "192.0.2.9"], ["10.0.0.0/24"]
        ) is None

    def test_explicit_empty_list_is_rejected(self):
        assert validate_targets_in_scope([], ["10.0.0.0/8"]) is None

    def test_hostname_is_not_routable(self):
        assert validate_targets_in_scope(["host.example.com"], ["10.0.0.0/8"]) is None

    def test_blank_token_is_rejected(self):
        assert validate_targets_in_scope(["  "], ["10.0.0.0/8"]) is None

    def test_reversed_range_is_rejected(self):
        assert validate_targets_in_scope(["10.0.0.20-10.0.0.10"], ["10.0.0.0/24"]) is None


class TestExclusions:
    def test_target_inside_an_exclusion_is_rejected(self):
        assert validate_targets_in_scope(
            ["10.0.0.5"], ["10.0.0.0/24"], ["10.0.0.0/28"]
        ) is None

    def test_target_overlapping_an_exclusion_is_rejected(self):
        # The /25 request straddles the excluded /28 → reject the whole request.
        assert validate_targets_in_scope(
            ["10.0.0.0/25"], ["10.0.0.0/24"], ["10.0.0.0/28"]
        ) is None

    def test_target_clear_of_exclusions_is_allowed(self):
        assert validate_targets_in_scope(
            ["10.0.0.200"], ["10.0.0.0/24"], ["10.0.0.0/28"]
        ) == ["10.0.0.200/32"]


class TestIpVersionSafety:
    def test_v6_target_against_v4_scope_is_rejected(self):
        assert validate_targets_in_scope(["2001:db8::1"], ["10.0.0.0/8"]) is None

    def test_v6_in_v6_scope(self):
        assert validate_targets_in_scope(
            ["2001:db8::1"], ["2001:db8::/32"]
        ) == ["2001:db8::1/128"]


def test_property_every_accepted_target_is_subnet_of_scope():
    """Whatever the validator accepts must be provably inside the scope."""
    scope = ["10.0.0.0/16", "192.168.0.0/24"]
    scope_nets = [ipaddress.ip_network(c) for c in scope]
    candidates = [
        ["10.0.5.5"], ["10.0.0.0/20"], ["192.168.0.10-192.168.0.20"],
        ["10.0.1.1", "192.168.0.1"],
    ]
    for targets in candidates:
        result = validate_targets_in_scope(targets, scope)
        assert result is not None
        for net in result:
            n = ipaddress.ip_network(net)
            assert any(n.version == s.version and n.subnet_of(s) for s in scope_nets)
