"""
test_asset_identity.py — P1b identity policy (app/detection/asset_identity.py).
"""
from __future__ import annotations

from app.detection.asset_identity import (
    MODE_GLOBAL, MODE_PER_SITE, RECOMMEND_KEEP, RECOMMEND_PER_SITE,
    RECOMMEND_PER_SITE_STRONG, identity_conflicts, identity_site, is_partitionable,
    mode_from_roe, normalize_name, overlapping_private_ranges, recommend,
)


def test_mode_defaults_to_global():
    assert mode_from_roe(None) == MODE_GLOBAL
    assert mode_from_roe({"asset_identity": "per_site"}) == MODE_PER_SITE
    assert mode_from_roe({"asset_identity": "nonsense"}) == MODE_GLOBAL


def test_only_non_global_ips_are_partitionable():
    for ip in ("10.0.0.5", "172.16.3.4", "192.168.1.1", "100.64.0.9", "169.254.1.1",
               "fd00::1", "fe80::1"):
        assert is_partitionable(ip), ip
    for ip in ("8.8.8.8", "1.1.1.1", "2606:4700::1111"):
        assert not is_partitionable(ip), ip
    # documentation ranges (TEST-NET-3) are not globally routable either
    assert is_partitionable("203.0.113.10")
    assert not is_partitionable("server01.corp.local")      # names are not split
    assert not is_partitionable(None)


def test_global_mode_never_scopes_by_site():
    assert identity_site("10.0.0.5", "site-a", MODE_GLOBAL) is None


def test_per_site_scopes_private_ips_only():
    assert identity_site("10.0.0.5", "site-a", MODE_PER_SITE) == "site-a"
    # a public host scanned from several sites is ONE asset (multi-vantage fusion)
    assert identity_site("1.1.1.1", "site-a", MODE_PER_SITE) is None
    # a probe with no site cannot scope anything
    assert identity_site("10.0.0.5", None, MODE_PER_SITE) is None


def test_overlapping_private_ranges():
    overlaps = overlapping_private_ranges({
        "a": ["10.0.0.0/16", "8.8.8.0/24"],
        "b": ["10.0.5.0/24"],
        "c": ["192.168.0.0/24"],
    })
    assert overlaps == [{"site_a": "a", "site_b": "b", "overlap": ["10.0.5.0/24"]}]


def test_public_range_overlap_is_not_an_identity_risk():
    assert overlapping_private_ranges({"a": ["8.8.8.0/24"], "b": ["8.8.8.0/24"]}) == []


def test_name_normalisation_rejects_generic_and_ip_names():
    assert normalize_name("DESKTOP-34M18MB.corp.local.") == "desktop-34m18mb"
    assert normalize_name("localhost") is None
    assert normalize_name("router") is None
    assert normalize_name("10.0.0.5") is None
    assert normalize_name("") is None and normalize_name(None) is None


def test_conflict_when_two_sites_name_the_same_private_ip_differently():
    conflicts = identity_conflicts([
        ("site-a", "10.0.0.5", "FILESRV01"),
        ("site-b", "10.0.0.5", "nas-branch"),
    ])
    assert conflicts == [{"ip": "10.0.0.5",
                          "names_by_site": {"site-a": ["filesrv01"], "site-b": ["nas-branch"]},
                          "distinct_names": ["filesrv01", "nas-branch"]}]


def test_same_name_from_two_sites_is_one_host_not_a_conflict():
    assert identity_conflicts([("a", "10.0.0.5", "FILESRV01.corp"),
                               ("b", "10.0.0.5", "filesrv01")]) == []


def test_public_ips_and_siteless_observations_are_ignored():
    assert identity_conflicts([("a", "1.1.1.1", "one"), ("b", "1.1.1.1", "two"),
                               (None, "10.0.0.9", "x1"), ("b", "10.0.0.9", "y1")]) == []


def test_recommendation_escalates_with_evidence():
    assert recommend(MODE_GLOBAL, [], [])["action"] == RECOMMEND_KEEP
    assert recommend(MODE_GLOBAL, [{"x": 1}], [])["action"] == RECOMMEND_PER_SITE
    assert recommend(MODE_GLOBAL, [], [{"ip": "10.0.0.5"}])["action"] == RECOMMEND_PER_SITE_STRONG
    assert recommend(MODE_PER_SITE, [], [{"ip": "x"}])["action"] == "none"
