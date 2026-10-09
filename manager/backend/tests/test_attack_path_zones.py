"""
The zone view: stored routes aggregated into the subnets they cross.

Expectations come from the analyzer run on the repo's validation fixtures (real routes, real `via`
lists), because what matters is whether the aggregation says what the model said: where routes
start and end, which step between subnets rests on an assumed link, and what it refuses to place.
"""
from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.graph.analyzer import PathAnalyzer
from app.graph.coverage import coverage_report, freshness_report
from app.graph.validation import build_graph
from app.graph.zones import MAX_ZONES, build_zones, node_zones, route_links
from app.routers import attack_paths as R

FIXTURES = Path(__file__).parent / "fixtures" / "attack_paths"
NOW = datetime(2026, 10, 9, 9, 0, tzinfo=timezone.utc)
E1 = uuid.UUID(int=11)


def _real(name: str):
    fx = json.loads((FIXTURES / f"{name}.json").read_text())
    graph = build_graph(fx)
    analyzer = PathAnalyzer(graph)
    paths = [p for t in fx["targets"] for p in analyzer.find_paths_to_target(t)]
    analysis = {"choke": analyzer.choke_analysis(list(fx["targets"])), "coverage": coverage_report(graph),
                "freshness": freshness_report(graph), "diagnostics": analyzer.diagnose(list(fx["targets"]))}
    return analysis, [{"nodes": p["nodes"], "edges": p["edges"]} for p in paths]


def _zones(name: str):
    analysis, routes = _real(name)
    return build_zones(analysis=analysis, routes=routes, computed_at=NOW, engagement_id=E1)


def _by_label(out):
    return {z["label"]: z for z in out["zones"]}


def test_a_flat_network_is_one_assumed_step_between_two_subnets():
    out = _zones("01_flat_internal")                      # entry 10.0.1.5 -> jewel 10.0.3.5, subnets assumed reachable
    zones = _by_label(out)
    assert set(zones) == {"10.0.1.0/24", "10.0.3.0/24"}
    assert zones["10.0.1.0/24"]["entry"] is True and zones["10.0.1.0/24"]["jewel"] is False
    assert zones["10.0.3.0/24"]["jewel"] is True and zones["10.0.3.0/24"]["entry"] is False
    assert out["links"] == [{"from": "10.0.1.0/24", "to": "10.0.3.0/24", "routes": 1, "basis": "assumed", "weak": True}]
    assert out["other_zones"] == 1                         # 10.0.2.0/24 has a host that no stored route touches
    assert zones["10.0.1.0/24"]["fix"] is True             # the entry host is the minimum fix set here


def test_a_gateway_hop_places_the_gateway_in_the_subnet_before_it():
    out = _zones("02_segmented_gateway")                   # entry > gw (same subnet) > jewel (assumed, through the gateway)
    zones = _by_label(out)
    assert set(zones) == {"10.0.1.0/24", "10.0.2.0/24"}
    assert zones["10.0.1.0/24"]["entry"] and zones["10.0.1.0/24"]["fix"], "the gateway sits in the entry's subnet and is on the fix list"
    assert zones["10.0.2.0/24"]["jewel"]
    assert out["links"] == [{"from": "10.0.1.0/24", "to": "10.0.2.0/24", "routes": 1, "basis": "assumed", "weak": True}]


def test_a_route_that_stays_in_one_subnet_is_one_zone_and_no_link():
    analysis, routes = _real("09_single_bottleneck_many_entries")
    out = build_zones(analysis=analysis, routes=routes, computed_at=NOW)
    assert len(out["zones"]) == 2                           # entries and gateway in one subnet, the jewel in another
    entry = next(z for z in out["zones"] if z["entry"])
    assert entry["routes"] == len(routes) == 8 and entry["fix"] is True
    assert [l["routes"] for l in out["links"]] == [8]       # all eight listed routes take the one step
    inside = build_zones(analysis=analysis, routes=[{"nodes": ["a", "b"], "edges": [{"via": ["10.9.9.0/24"], "technique": "SAME_SUBNET", "basis": "same_subnet"}]}])
    assert len(inside["zones"]) == 1 and inside["links"] == []
    assert inside["zones"][0]["entry"] and inside["zones"][0]["jewel"]


def test_a_machine_on_two_addresses_is_not_assumed_to_share_its_subnets():
    """edgeNIC (10.0.1.5) and innerNIC (10.0.2.5) are one machine in TWO subnets; the route places only
    what its hops say, so the entry is not given the inner subnet."""
    analysis, routes = _real("04_dual_homed_pivot")
    zs = node_zones(len(routes[0]["nodes"]), routes[0]["edges"])
    assert zs == [None, "10.0.2.0/24", "10.0.2.0/24"]
    out = build_zones(analysis=analysis, routes=routes, computed_at=NOW)
    assert out["entry_unplaced"] == 1 and out["jewel_unplaced"] == 0
    assert not any(z["entry"] for z in out["zones"]), "no entry subnet is claimed for a host the model did not place"
    assert [z["jewel"] for z in out["zones"]] == [True]


def test_a_hop_with_no_subnet_information_leaves_its_hosts_unplaced_not_guessed():
    zs = node_zones(3, [{"via": [], "technique": "CONNECTS_TO"}, {"via": ["10.0.2.0/24"], "technique": "SAME_SUBNET"}])
    assert zs == [None, "10.0.2.0/24", "10.0.2.0/24"]
    assert route_links(zs, [{"basis": "observed"}, {"basis": "same_subnet"}]) == []


def test_a_link_takes_the_weakest_basis_of_the_hops_it_covers():
    zs = ["a", None, "b"]                                   # the middle host is not placed: one link spans both hops
    assert route_links(zs, [{"basis": "same_subnet"}, {"basis": "assumed"}]) == [("a", "b", "assumed")]
    assert route_links(["a", "b"], [{"basis": "observed"}]) == [("a", "b", "observed")]
    assert route_links(["a", "b"], [{"basis": None}]) == [("a", "b", "observed")]


def test_one_assumed_use_makes_the_link_assumed_and_routes_are_counted_once_each():
    seg_a, seg_b = "10.1.0.0/24", "10.2.0.0/24"
    hop = lambda basis: {"via": [seg_a, seg_b], "technique": "CROSS_SUBNET", "basis": basis}  # noqa: E731
    cov = {"segments": [{"segment": seg_a, "cidr": seg_a, "hosts": 3}, {"segment": seg_b, "cidr": seg_b, "hosts": 2}]}
    out = build_zones(analysis={"choke": {}, "coverage": cov},
                      routes=[{"nodes": ["x", "y"], "edges": [hop("observed")]}, {"nodes": ["p", "q"], "edges": [hop("assumed")]}])
    assert out["links"] == [{"from": seg_a, "to": seg_b, "routes": 2, "basis": "assumed", "weak": True}]
    strong = build_zones(analysis={"choke": {}, "coverage": cov}, routes=[{"nodes": ["x", "y"], "edges": [hop("observed")]}])
    assert strong["links"][0]["weak"] is False and strong["links"][0]["basis"] == "observed"


def test_subnet_labels_carry_the_site_when_two_sites_could_share_a_range():
    key = "10.0.0.0/24@site-1"
    cov = {"segments": [{"segment": key, "cidr": "10.0.0.0/24", "site": "11111111-1111-1111-1111-111111111111", "hosts": 4}]}
    out = build_zones(analysis={"choke": {}, "coverage": cov},
                      routes=[{"nodes": ["a", "b"], "edges": [{"via": [key], "technique": "SAME_SUBNET", "basis": "same_subnet"}]}],
                      site_names={"11111111-1111-1111-1111-111111111111": "HQ"})
    assert out["zones"][0]["label"] == "10.0.0.0/24 @ HQ" and out["zones"][0]["key"] == key and out["zones"][0]["hosts"] == 4


def test_never_computed_draws_nothing_and_says_so():
    out = build_zones(analysis=None, routes=[{"nodes": ["a"], "edges": []}], engagement_id=E1)
    assert out["computed"] is False and out["zones"] == [] and out["links"] == [] and out["routes_considered"] is None


def test_computed_with_no_stored_routes_is_an_empty_view_not_a_safe_one():
    analysis, _ = _real("05_exposure_is_not_ownership")
    out = build_zones(analysis=analysis, routes=[], computed_at=NOW)
    assert out["computed"] is True and out["zones"] == [] and out["routes_considered"] == 0
    assert out["other_zones"] >= 0 and out["unplaced_assets"] is not None


def test_routes_that_place_no_host_are_counted_not_drawn():
    out = build_zones(analysis={"choke": {}, "coverage": {"segments": []}},
                      routes=[{"nodes": ["a", "b"], "edges": [{"via": [], "technique": "CONNECTS_TO", "basis": "observed"}]}])
    assert out["zones"] == [] and out["routes_unplaced"] == 1


def test_at_most_twelve_zones_are_drawn_roles_first_and_the_rest_counted():
    n = MAX_ZONES + 5
    segs = [{"segment": f"10.{i}.0.0/24", "cidr": f"10.{i}.0.0/24", "hosts": 1} for i in range(n)]
    routes = [{"nodes": [f"h{i}", f"h{i + 1}"], "edges": [{"via": [f"10.{i}.0.0/24", f"10.{i + 1}.0.0/24"], "technique": "CROSS_SUBNET", "basis": "assumed"}]}
              for i in range(n - 1)]
    out = build_zones(analysis={"choke": {}, "coverage": {"segments": segs}}, routes=routes)
    assert len(out["zones"]) == MAX_ZONES and out["zones_hidden"] == n - MAX_ZONES
    kept = {z["key"] for z in out["zones"]}
    assert all(l["from"] in kept and l["to"] in kept for l in out["links"]) and out["links_hidden"] > 0


def test_the_output_is_json_and_does_not_depend_on_route_order():
    analysis, routes = _real("09_single_bottleneck_many_entries")
    a = build_zones(analysis=analysis, routes=routes, computed_at=NOW)
    b = build_zones(analysis=analysis, routes=list(reversed(routes)), computed_at=NOW)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# ── the route ────────────────────────────────────────────────────────────────

class _Result:
    def __init__(self, rows=(), one=None):
        self._rows, self._one = list(rows), one

    def all(self):
        return self._rows

    def scalar_one_or_none(self):
        return self._one

    def scalars(self):
        return self


class _DB:
    def __init__(self, *results, stored=None):
        self._results, self._stored, self.sql = list(results), stored, []

    async def execute(self, stmt, params=None):
        self.sql.append(str(stmt))
        return self._results.pop(0)

    async def get(self, model, key):
        self.sql.append(f"GET {model.__name__}")
        return self._stored


def _call(db, eid=E1):
    user = SimpleNamespace(role="analyst", tenant_id=uuid.UUID(int=77))
    return asyncio.run(R.attack_path_zones(engagement_id=eid, db=db, current_user=user))


@pytest.fixture
def no_compute(monkeypatch):
    async def boom(*a, **k):
        raise AssertionError("the zones route must never compute")
    for name in ("_recompute_and_store", "_build_analyzer", "_store_analysis", "_record_snapshot"):
        monkeypatch.setattr(R, name, boom)


def test_the_route_is_registered_beta_and_get_only():
    from app.main import app
    op = app.openapi()["paths"]["/engagements/{engagement_id}/attack-path-zones"]
    assert list(op) == ["get"] and op["get"]["tags"] == ["attack-paths (beta)"]


def test_the_route_aggregates_what_is_stored_and_writes_nothing(no_compute):
    analysis, routes = _real("01_flat_internal")
    stored = SimpleNamespace(computed_at=NOW, path_count=1, analysis=analysis)
    db = _DB(_Result(one=SimpleNamespace(id=E1)), _Result(rows=[(r["nodes"], r["edges"]) for r in routes]), stored=stored)
    out = _call(db)
    assert out["computed"] is True and len(out["zones"]) == 2 and out["routes_truncated"] is False
    assert all(s.lstrip().lower().startswith(("select", "get ")) for s in db.sql)


def test_the_route_for_a_never_computed_engagement_computes_nothing(no_compute):
    out = _call(_DB(_Result(one=SimpleNamespace(id=E1)), stored=None))
    assert out["computed"] is False and out["zones"] == []


def test_the_route_is_tenant_scoped(no_compute):
    db = _DB(_Result(one=None))
    with pytest.raises(HTTPException) as exc:
        _call(db)
    assert exc.value.status_code == 404 and "engagements.tenant_id" in db.sql[0]
