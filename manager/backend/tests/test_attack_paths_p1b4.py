"""
test_attack_paths_p1b4.py — P1b-4: graph identity.

Three ways the graph's idea of "which host / which network" was wrong
(manager/docs/ATTACK_PATH_PLAN.md FM-14/15/16/32):

  * two sites that both use 10.0.0.0/24 shared ONE subnet hub, so hosts of
    unconnected networks were drawn as adjacent;
  * one machine seen at two addresses was two unrelated assets, hiding the
    dual-homed pivot — the most important way across subnets;
  * assets not seen for weeks counted as fully trustworthy steps.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.detection.asset_identity import (
    BASIS_SAME_HOST_FQDN, BASIS_SAME_HOST_NAME, CONF_LINK_FQDN, CONF_LINK_NAME, MAX_NICS,
    is_stale, link_machines,
)
from app.detection.reachability import (
    BASIS_CROSS_SITE, CONF_CROSS_SITE, POSTURE_FLAT, POSTURE_SEGMENTED, derive_topology,
)
from app.graph.analyzer import P_STALE_FACTOR, PathAnalyzer
from app.graph.builder import GraphBuilder, freshness_days_from_roe

SITE_A, SITE_B = str(uuid.uuid4()), str(uuid.uuid4())
NOW = datetime(2026, 10, 8, tzinfo=timezone.utc)


@dataclass
class _A:
    id: str
    ip_address: str | None
    site_id: str | None = None
    hostname: str | None = None
    fqdn: str | None = None
    device_role: str | None = None
    criticality: str = "medium"
    environment: str | None = None
    tags: dict = field(default_factory=dict)
    last_seen: datetime | None = None


@dataclass
class _F:
    id: uuid.UUID
    asset_id: str
    title: str = "t"
    severity: str = "high"
    cvss_score: Decimal | None = Decimal("8.0")
    exploitable: bool = True
    exploit_validated: bool = False
    status: str = "open"


# ── site-keyed segments ──────────────────────────────────────────────────────

def test_equal_cidrs_at_two_sites_are_two_segments_under_per_site():
    assets = [_A("a1", "10.0.0.5", SITE_A), _A("b1", "10.0.0.5", SITE_B), _A("a2", "10.0.0.6", SITE_A)]
    topo = derive_topology(assets, ["10.0.0.0/24"], identity_mode="per_site")
    assert set(topo["segments"]) == {f"10.0.0.0/24@{SITE_A}", f"10.0.0.0/24@{SITE_B}"}
    assert topo["segments"][f"10.0.0.0/24@{SITE_A}"]["members"] == ["a1", "a2"]
    assert topo["segments"][f"10.0.0.0/24@{SITE_B}"]["site"] == SITE_B


def test_global_mode_keeps_one_segment_per_cidr_as_before():
    assets = [_A("a1", "10.0.0.5", SITE_A), _A("b1", "10.0.0.9", SITE_B)]
    topo = derive_topology(assets, ["10.0.0.0/24"])
    assert list(topo["segments"]) == ["10.0.0.0/24"] and topo["segments"]["10.0.0.0/24"]["site"] is None


def test_a_public_subnet_is_shared_even_in_per_site_mode():
    assets = [_A("a", "8.8.8.8", SITE_A), _A("b", "8.8.8.9", SITE_B)]
    topo = derive_topology(assets, [], identity_mode="per_site")
    assert list(topo["segments"]) == ["8.8.8.0/24"]


def test_cross_site_links_are_labelled_and_weak_but_same_site_links_are_not():
    assets = [_A("a1", "10.0.1.5", SITE_A), _A("a2", "10.0.2.5", SITE_A), _A("b1", "10.0.1.7", SITE_B),
              _A("p", "8.8.8.8", SITE_A)]
    topo = derive_topology(assets, ["10.0.1.0/24", "10.0.2.0/24"], identity_mode="per_site")
    by = {(l["src"], l["dst"]): l for l in topo["links"]}
    a1, a2, b1 = f"10.0.1.0/24@{SITE_A}", f"10.0.2.0/24@{SITE_A}", f"10.0.1.0/24@{SITE_B}"
    assert by[(a1, a2)]["basis"] == "assumed"                              # one site's two networks
    assert by[(a1, b1)]["basis"] == BASIS_CROSS_SITE and by[(a1, b1)]["confidence"] == CONF_CROSS_SITE
    assert by[(a1, "8.8.8.0/24")]["basis"] == "assumed"                    # the shared internet side


def test_segmented_posture_has_no_cross_site_link_and_a_gateway_stays_in_its_site():
    assets = [_A("gwA", "10.0.1.1", SITE_A, device_role="network_device"), _A("a2", "10.0.2.5", SITE_A),
              _A("b1", "10.0.1.7", SITE_B), _A("pub", "8.8.8.8", SITE_A)]
    topo = derive_topology(assets, ["10.0.1.0/24", "10.0.2.0/24"], POSTURE_SEGMENTED, identity_mode="per_site")
    assert topo["links"] == []
    routed = {r["segment"] for r in topo["routes"]}
    assert f"10.0.2.0/24@{SITE_A}" in routed and "8.8.8.0/24" in routed       # own site + shared side
    assert f"10.0.1.0/24@{SITE_B}" not in routed                              # never another site's private net


def _attack_graph(assets, exploitable, scope, posture, mode, links=()):
    b = GraphBuilder()
    b.build_asset_graph("eng", assets, [], [_F(uuid.uuid4(), a) for a in exploitable], now=NOW)
    b.add_segment_topology(derive_topology(assets, scope, posture, identity_mode=mode))
    b.add_machine_links(links)
    return b.graph


def test_unconnected_sites_no_longer_get_a_free_path_between_them():
    """Site A's exposed host and site B's crown jewel share a CIDR but not a network."""
    entry = _A("entryA", "10.0.0.5", SITE_A, environment="dmz")
    target = _A("crownB", "10.0.0.9", SITE_B, criticality="critical")
    scope = ["10.0.0.0/24"]
    merged = PathAnalyzer(_attack_graph([entry, target], ["entryA", "crownB"], scope, POSTURE_FLAT, "global"))
    split_seg = PathAnalyzer(_attack_graph([entry, target], ["entryA", "crownB"], scope, POSTURE_SEGMENTED, "per_site"))
    assert merged.find_paths_to_target("crownB"), "global identity merges the two networks (the old behaviour)"
    assert split_seg.find_paths_to_target("crownB") == []


def test_per_site_flat_posture_still_finds_the_cross_site_path_but_marks_it_weak():
    entry = _A("entryA", "10.0.0.5", SITE_A, environment="dmz")
    target = _A("crownB", "10.0.0.9", SITE_B, criticality="critical")
    g = _attack_graph([entry, target], ["entryA", "crownB"], ["10.0.0.0/24"], POSTURE_FLAT, "per_site")
    flat_global = PathAnalyzer(_attack_graph([entry, target], ["entryA", "crownB"], ["10.0.0.0/24"], POSTURE_FLAT, "global"))
    (path,) = PathAnalyzer(g).find_paths_to_target("crownB")
    assert path["edges"][0]["basis"] == BASIS_CROSS_SITE
    assert path["likelihood"] < flat_global.find_paths_to_target("crownB")[0]["likelihood"]


# ── one machine, several addresses ───────────────────────────────────────────

def test_same_fqdn_at_two_addresses_is_one_machine():
    groups = link_machines([_A("x", "10.0.1.5", hostname="fileserver01", fqdn="fileserver01.corp.local"),
                            _A("y", "10.0.2.5", hostname="fileserver01", fqdn="fileserver01.corp.local")])
    assert groups == [{"members": ["x", "y"], "name": "fileserver01", "basis": BASIS_SAME_HOST_FQDN,
                       "confidence": CONF_LINK_FQDN}]


def test_same_short_name_without_an_fqdn_is_a_weaker_link():
    (g,) = link_machines([_A("x", "10.0.1.5", hostname="FILESERVER01"), _A("y", "10.0.2.5", hostname="fileserver01.")])
    assert g["basis"] == BASIS_SAME_HOST_NAME and g["confidence"] == CONF_LINK_NAME


def test_different_domains_with_one_short_name_are_different_machines():
    assert link_machines([_A("x", "10.0.1.5", hostname="web01", fqdn="web01.a.corp"),
                          _A("y", "10.0.2.5", hostname="web01", fqdn="web01.b.corp")]) == []


@pytest.mark.parametrize("name", ["router", "localhost", "10.0.0.7", "pc", "", None])
def test_generic_or_ip_names_prove_nothing(name):
    assert link_machines([_A("x", "10.0.1.5", hostname=name), _A("y", "10.0.2.5", hostname=name)]) == []


def test_one_address_twice_is_not_a_second_nic():
    assert link_machines([_A("x", "10.0.1.5", hostname="db01"), _A("y", "10.0.1.5", hostname="db01")]) == []


def test_per_site_never_links_two_sites_but_a_siteless_nic_may_join_one_site():
    two_sites = [_A("x", "10.0.1.5", SITE_A, hostname="web01"), _A("y", "10.0.1.5", SITE_B, hostname="web01")]
    assert link_machines(two_sites, "per_site") == []
    edge_host = [_A("pub", "203.0.114.9", None, hostname="edge01"), _A("lan", "10.0.1.5", SITE_A, hostname="edge01")]
    assert [g["members"] for g in link_machines(edge_host, "per_site")] == [["lan", "pub"]]


def test_a_nameless_bridge_between_two_sites_is_ambiguous_and_links_nothing():
    trio = [_A("x", "10.0.1.5", SITE_A, hostname="app01"), _A("pub", "8.8.8.8", None, hostname="app01"),
            _A("y", "10.9.1.5", SITE_B, hostname="app01")]
    assert link_machines(trio, "per_site") == []


def test_more_same_named_assets_than_a_machine_can_have_is_a_naming_scheme():
    many = [_A(f"n{i}", f"10.0.{i}.5", hostname="kiosk01") for i in range(MAX_NICS + 1)]
    assert link_machines(many) == []


def test_stale_assets_are_not_linked_and_unknown_age_is_not_stale():
    old = NOW - timedelta(days=90)
    assert link_machines([_A("x", "10.0.1.5", hostname="app02", last_seen=old),
                          _A("y", "10.0.2.5", hostname="app02", last_seen=NOW)], now=NOW) == []
    assert link_machines([_A("x", "10.0.1.5", hostname="app02", last_seen=None),
                          _A("y", "10.0.2.5", hostname="app02", last_seen=NOW)], now=NOW)


def test_linking_is_deterministic_regardless_of_input_order():
    a = [_A("x", "10.0.1.5", hostname="srv01"), _A("y", "10.0.2.5", hostname="srv01")]
    assert link_machines(a) == link_machines(list(reversed(a)))


def _dual_homed_graph(posture, linked):
    # edge NIC (exploitable, exposed) on 10.0.1.0/24; the same machine's inner NIC (NOT exploitable) on
    # 10.0.2.0/24; the crown jewel is exploitable and lives only on the inner network.
    edge = _A("edgeNIC", "10.0.1.5", hostname="gateway-app", environment="dmz")
    inner = _A("innerNIC", "10.0.2.5", hostname="gateway-app")
    jewel = _A("jewel", "10.0.2.9", criticality="critical")
    assets = [edge, inner, jewel]
    return _attack_graph(assets, ["edgeNIC", "jewel"], ["10.0.1.0/24", "10.0.2.0/24"], posture, "global",
                         links=link_machines(assets) if linked else ())


def test_a_dual_homed_machine_is_the_pivot_into_the_inner_network():
    (path,) = PathAnalyzer(_dual_homed_graph(POSTURE_SEGMENTED, linked=True)).find_paths_to_target("jewel")
    techniques = [e["technique"] for e in path["edges"]]
    assert path["nodes"] == ["edgeNIC", "innerNIC", "jewel"] and techniques[0] == "SAME_HOST"
    assert path["edges"][0]["exploited"] is False                    # no exploit needed: it is the same box
    assert path["edges"][0]["basis"] == BASIS_SAME_HOST_NAME


def test_without_the_link_the_segmented_network_hides_that_pivot():
    assert PathAnalyzer(_dual_homed_graph(POSTURE_SEGMENTED, linked=False)).find_paths_to_target("jewel") == []


def test_the_link_confidence_lowers_the_path_likelihood():
    (linked,) = PathAnalyzer(_dual_homed_graph(POSTURE_SEGMENTED, linked=True)).find_paths_to_target("jewel")
    assert linked["edges"][0]["likelihood"] == pytest.approx(CONF_LINK_NAME, abs=1e-3)


# ── staleness ────────────────────────────────────────────────────────────────

def test_is_stale_semantics():
    assert is_stale(NOW - timedelta(days=31), NOW, 30) and not is_stale(NOW - timedelta(days=29), NOW, 30)
    assert not is_stale(None, NOW, 30)                                    # unknown age is not evidence of age
    assert not is_stale(NOW - timedelta(days=999), NOW, 0)                # disabled
    assert is_stale(datetime(2026, 1, 1), NOW, 30)                        # naive timestamps are treated as UTC


def test_freshness_window_from_the_engagement():
    assert freshness_days_from_roe(None) == 30
    assert freshness_days_from_roe({"attack_path_freshness_days": 7}) == 7
    assert freshness_days_from_roe({"attack_path_freshness_days": 0}) is None        # disabled
    assert freshness_days_from_roe({"attack_path_freshness_days": "7"}) == 30        # junk -> default
    assert freshness_days_from_roe({"attack_path_freshness_days": -3}) == 30
    assert freshness_days_from_roe({"attack_path_freshness_days": True}) == 30


def _one_hop(jewel_last_seen):
    entry = _A("entry", "10.0.0.5", environment="dmz", last_seen=NOW)
    jewel = _A("jewel", "10.0.0.7", criticality="critical", last_seen=jewel_last_seen)
    return _attack_graph([entry, jewel], ["entry", "jewel"], ["10.0.0.0/24"], POSTURE_FLAT, "global")


def test_a_step_onto_a_stale_asset_is_down_weighted_and_the_path_says_so():
    (fresh,) = PathAnalyzer(_one_hop(NOW)).find_paths_to_target("jewel")
    (stale,) = PathAnalyzer(_one_hop(NOW - timedelta(days=60))).find_paths_to_target("jewel")
    assert fresh["freshness"] == "fresh" and fresh["stale_steps"] == 0 and not fresh["edges"][0]["stale"]
    assert stale["freshness"] == "stale" and stale["stale_steps"] == 1 and stale["edges"][0]["stale"]
    assert stale["likelihood"] == pytest.approx(fresh["likelihood"] * P_STALE_FACTOR, rel=0.05)
    assert stale["risk_score"] < fresh["risk_score"]


def test_a_path_with_one_stale_step_among_fresh_ones_is_partly_stale():
    # segmented network: the only way across is through two gateways, the second one stale
    entry = _A("entry", "10.0.1.5", environment="dmz", last_seen=NOW)
    gw1 = _A("gw1", "10.0.1.1", device_role="network_device", last_seen=NOW)
    gw2 = _A("gw2", "10.0.2.1", device_role="network_device", last_seen=NOW - timedelta(days=60))
    jewel = _A("jewel", "10.0.3.5", criticality="critical", last_seen=NOW)
    g = _attack_graph([entry, gw1, gw2, jewel], ["entry", "gw1", "gw2", "jewel"],
                      ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"], POSTURE_SEGMENTED, "global")
    paths = PathAnalyzer(g).find_paths_to_target("jewel")
    via_gw2 = next(p for p in paths if "gw2" in p["nodes"])
    assert via_gw2["nodes"] == ["entry", "gw1", "gw2", "jewel"]
    assert via_gw2["freshness"] == "partly_stale" and via_gw2["stale_steps"] == 1
    assert [e["stale"] for e in via_gw2["edges"]] == [False, True, False]
    direct = next(p for p in paths if "gw2" not in p["nodes"])      # the route that avoids the stale host
    assert direct["freshness"] == "fresh" and direct["likelihood"] > via_gw2["likelihood"]


def test_the_graph_records_when_each_asset_was_last_seen():
    g = _one_hop(NOW - timedelta(days=60))
    assert g.nodes["asset:jewel"]["stale"] is True and g.nodes["asset:jewel"]["last_seen"].startswith("2026-08")
    assert g.nodes["asset:entry"]["stale"] is False


def test_a_graph_with_no_timestamps_is_unchanged():
    entry = _A("entry", "10.0.0.5", environment="dmz")
    jewel = _A("jewel", "10.0.0.7", criticality="critical")
    g = _attack_graph([entry, jewel], ["entry", "jewel"], ["10.0.0.0/24"], POSTURE_FLAT, "global")
    (p,) = PathAnalyzer(g).find_paths_to_target("jewel")
    assert p["freshness"] == "fresh" and g.nodes["asset:jewel"]["last_seen"] is None


# ── what the API says about it ───────────────────────────────────────────────

def test_labels_stay_exactly_as_they_were_when_unique():
    from app.routers.attack_paths import disambiguated_labels
    rows = [("1", "web01", "10.0.0.5", None), ("2", None, "10.0.0.6", None), ("3", None, None, None)]
    assert disambiguated_labels(rows, {}) == {"1": "web01", "2": "10.0.0.6", "3": "3"}


def test_two_machines_sharing_an_address_get_their_site_in_the_label():
    from app.routers.attack_paths import disambiguated_labels
    rows = [("1", None, "10.0.0.5", SITE_A), ("2", None, "10.0.0.5", SITE_B), ("3", None, "10.0.0.9", SITE_A)]
    labels = disambiguated_labels(rows, {SITE_A: "HQ", SITE_B: "Branch"})
    assert labels == {"1": "10.0.0.5 @ HQ", "2": "10.0.0.5 @ Branch", "3": "10.0.0.9"}


def test_an_unknown_site_name_falls_back_to_a_short_id():
    from app.routers.attack_paths import disambiguated_labels
    rows = [("1", None, "10.0.0.5", SITE_A), ("2", None, "10.0.0.5", SITE_B)]
    assert disambiguated_labels(rows, {})["1"] == f"10.0.0.5 @ {SITE_A[:8]}"


def test_hop_explanations_carry_the_caveats_that_matter():
    from app.routers.attack_paths import _explain_hop
    labels = {"a": "A", "b": "B"}
    base = {"source": "a", "target": "b", "technique": "CROSS_SUBNET", "via": ["x", "y"]}
    assert "SITES' private networks" in _explain_hop({**base, "basis": "assumed_cross_site"}, labels)
    assert "verify segmentation" in _explain_hop({**base, "basis": "assumed"}, labels)
    same = {"source": "a", "target": "b", "technique": "SAME_HOST", "via": []}
    assert "same machine" in _explain_hop({**same, "basis": "same_host_fqdn"}, labels)
    assert "host name only" in _explain_hop({**same, "basis": "same_host_name"}, labels)
    assert "not seen recently" in _explain_hop({**base, "basis": "assumed", "stale": True}, labels)
    assert "not seen recently" not in _explain_hop({**base, "basis": "assumed"}, labels)


def test_path_freshness_summary():
    from app.routers.attack_paths import path_freshness
    assert path_freshness([]) == "fresh" and path_freshness([{"stale": False}]) == "fresh"
    assert path_freshness([{"stale": True}, {"stale": False}]) == "partly_stale"
    assert path_freshness([{"stale": True}, {"stale": True}]) == "stale"
