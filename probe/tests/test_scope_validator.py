"""Tests for agent/scope_validator.py"""
from __future__ import annotations

import pytest

from agent.scope_validator import (
    fetch_engagement_scope,
    validate_targets_in_scope,
    targets_in_excludes,
    merge_exclusions,
)


class TestValidateTargetsInScope:
    def test_ip_in_cidr_allowed(self):
        allowed, rejected = validate_targets_in_scope(
            ["10.0.0.1", "10.0.0.2"], ["10.0.0.0/24"],
        )
        assert allowed == ["10.0.0.1", "10.0.0.2"]
        assert rejected == []

    def test_outside_cidr_rejected(self):
        allowed, rejected = validate_targets_in_scope(
            ["10.0.0.1", "192.168.1.1"], ["10.0.0.0/24"],
        )
        assert allowed == ["10.0.0.1"]
        assert rejected == ["192.168.1.1"]

    def test_hostname_passes_through(self):
        allowed, rejected = validate_targets_in_scope(
            ["scanme.example.com", "10.0.0.1"], ["10.0.0.0/24"],
        )
        assert "scanme.example.com" in allowed

    def test_empty_targets(self):
        allowed, rejected = validate_targets_in_scope([], ["10.0.0.0/24"])
        assert allowed == []
        assert rejected == []

    def test_invalid_cidr_ignored(self):
        allowed, rejected = validate_targets_in_scope(
            ["10.0.0.1"], ["not-a-cidr", "10.0.0.0/24"],
        )
        assert allowed == ["10.0.0.1"]

    def test_port_suffix_stripped(self):
        allowed, rejected = validate_targets_in_scope(
            ["10.0.0.1:8080", "10.0.1.1:443"], ["10.0.0.0/24"],
        )
        assert allowed == ["10.0.0.1:8080"]
        assert rejected == ["10.0.1.1:443"]

    def test_multiple_cidrs(self):
        allowed, rejected = validate_targets_in_scope(
            ["10.0.0.1", "192.168.1.1", "172.16.0.1"],
            ["10.0.0.0/24", "192.168.0.0/16"],
        )
        assert set(allowed) == {"10.0.0.1", "192.168.1.1"}
        assert rejected == ["172.16.0.1"]


class TestTargetsInExcludes:
    def test_drops_excluded_ip(self):
        kept, dropped = targets_in_excludes(
            ["10.0.0.1", "10.0.0.5", "10.0.0.10"], ["10.0.0.5/32"],
        )
        assert kept == ["10.0.0.1", "10.0.0.10"]
        assert dropped == ["10.0.0.5"]

    def test_drops_excluded_subnet(self):
        kept, dropped = targets_in_excludes(
            ["10.0.0.1", "10.0.1.1"], ["10.0.1.0/24"],
        )
        assert kept == ["10.0.0.1"]
        assert dropped == ["10.0.1.1"]

    def test_no_excludes_returns_all(self):
        kept, dropped = targets_in_excludes(
            ["10.0.0.1", "10.0.0.2"], [],
        )
        assert kept == ["10.0.0.1", "10.0.0.2"]
        assert dropped == []

    def test_hostname_passes_through(self):
        kept, dropped = targets_in_excludes(
            ["10.0.0.1", "scanme.example.com"], ["10.0.0.1/32"],
        )
        assert kept == ["scanme.example.com"]
        assert dropped == ["10.0.0.1"]

    def test_port_suffix_stripped(self):
        kept, dropped = targets_in_excludes(
            ["10.0.0.5:443"], ["10.0.0.5/32"],
        )
        assert kept == []
        assert dropped == ["10.0.0.5:443"]

    def test_all_excluded_returns_empty(self):
        kept, dropped = targets_in_excludes(
            ["10.0.0.1", "10.0.0.2"], ["10.0.0.0/24"],
        )
        assert kept == []
        assert dropped == ["10.0.0.1", "10.0.0.2"]


class TestMergeExclusions:
    def test_merges_no_duplicates(self):
        result = merge_exclusions(["10.0.0.0/24"], ["10.0.0.0/24", "10.0.1.0/24"])
        assert result == ["10.0.0.0/24", "10.0.1.0/24"]

    def test_empty_job_excludes(self):
        result = merge_exclusions(["10.0.0.0/24"], [])
        assert result == ["10.0.0.0/24"]

    def test_none_job_excludes(self):
        result = merge_exclusions(["10.0.0.0/24"], None)
        assert result == ["10.0.0.0/24"]

    def test_empty_engagement_excludes(self):
        result = merge_exclusions([], ["10.0.1.0/24"])
        assert result == ["10.0.1.0/24"]

    def test_both_empty(self):
        result = merge_exclusions([], [])
        assert result == []

    def test_strips_whitespace(self):
        result = merge_exclusions(["  10.0.0.0/24  "], ["  10.0.1.0/24  "])
        assert result == ["10.0.0.0/24", "10.0.1.0/24"]


class TestFetchEngagementScope:
    def test_returns_scope_from_http_get(self):
        def http_get(path):
            assert "/engagements/abc/scope" in path
            return {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": []}

        scope, excludes = fetch_engagement_scope("abc", http_get)
        assert scope == ["10.0.0.0/24"]
        assert excludes == []

    def test_returns_excludes(self):
        def http_get(path):
            return {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": ["10.0.0.5/32"]}

        _scope, excludes = fetch_engagement_scope("abc", http_get)
        assert excludes == ["10.0.0.5/32"]

    def test_http_get_returns_none(self):
        def http_get(path):
            return None

        scope, excludes = fetch_engagement_scope("abc", http_get)
        assert scope is None
        assert excludes == []

    def test_http_get_raises(self):
        def http_get(path):
            raise ConnectionError("network error")

        scope, excludes = fetch_engagement_scope("abc", http_get)
        assert scope is None
        assert excludes == []

    def test_http_get_returns_incomplete(self):
        def http_get(path):
            return {"scope_cidrs": ["10.0.0.0/24"]}  # missing excluded_cidrs

        scope, excludes = fetch_engagement_scope("abc", http_get)
        assert scope == ["10.0.0.0/24"]
        assert excludes == []
