"""
test_attack_paths_p1.py — P1a: subnet topology derivation and hub-based,
multi-subnet attack paths (manager/docs/ATTACK_PATH_PLAN.md §3.1, §7).
"""
from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from unittest.mock import patch

from app.detection.reachability import (
    BASIS_ASSUMED, POSTURE_FLAT, POSTURE_SEGMENTED, derive_topology, posture_from_roe,
    segment_for, _parse_networks,
)
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder


@dataclass
class _A:
    id: str
    ip_address: str | None
    device_role: str | None = None
    hostname: str | None = None
    criticality: str = "medium"
    environment: str | None = None
    tags: dict = field(default_factory=dict)


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


def _graph(assets, exploitable_ids, scope, posture=POSTURE_FLAT):
    findings = [_F(uuid.uuid4(), aid) for aid in exploitable_ids]
    b = GraphBuilder()
    b.build_asset_graph("eng", assets, [], findings)
    b.add_segment_topology(derive_topology(assets, scope, posture))
    return b.graph


# ── topology derivation ──────────────────────────────────────────────────────
def test_assets_join_most_specific_scope_subnet():
    scope = _parse_networks(["10.0.0.0/16", "10.0.1.0/24"])
    net, inferred, scoped = segment_for("10.0.1.7", scope)
    assert str(net) == "10.0.1.0/24" and not inferred and scoped


def test_broad_scope_is_bucketed_to_slash24_and_marked_inferred():
    net, inferred, scoped = segment_for("10.20.30.40", _parse_networks(["10.0.0.0/8"]))
    assert str(net) == "10.20.30.0/24" and inferred and scoped


def test_out_of_scope_and_unparseable_hosts_are_never_dropped():
    topo = derive_topology([_A("a", "192.168.9.9"), _A("b", None), _A("c", "not-an-ip")],
                           ["10.0.0.0/24"])
    seg = topo["segments"]["192.168.9.0/24"]
    assert seg["members"] == ["a"] and seg["scoped"] is False and seg["inferred"] is True
    assert topo["unplaced"] == ["b", "c"]


def test_ipv6_buckets_to_slash64():
    net, inferred, _ = segment_for("2001:db8:0:1::5", _parse_networks(["2001:db8::/32"]))
    assert str(net) == "2001:db8:0:1::/64" and inferred


def test_flat_posture_links_every_subnet_pair_as_assumed():
    assets = [_A("a", "10.0.1.5"), _A("b", "10.0.2.5"), _A("c", "10.0.3.5")]
    topo = derive_topology(assets, ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"])
    assert len(topo["links"]) == 6                       # 3 subnets, ordered pairs
    assert {l["basis"] for l in topo["links"]} == {BASIS_ASSUMED}


def test_segmented_posture_has_no_direct_links_only_gateway_routes():
    assets = [_A("a", "10.0.1.5"), _A("gw", "10.0.1.1", device_role="network_device"),
              _A("b", "10.0.2.5")]
    topo = derive_topology(assets, ["10.0.1.0/24", "10.0.2.0/24"], POSTURE_SEGMENTED)
    assert topo["links"] == []
    assert topo["routes"] == [{"gateway": "gw", "segment": "10.0.2.0/24",
                               "basis": "assumed", "confidence": 0.6}]
    assert topo["segments"]["10.0.1.0/24"]["gateways"] == ["gw"]


def test_posture_defaults_to_flat_and_ignores_unknown_values():
    assert posture_from_roe(None) == POSTURE_FLAT
    assert posture_from_roe({"attack_path_reachability": "segmented"}) == POSTURE_SEGMENTED
    assert posture_from_roe({"attack_path_reachability": "bogus"}) == POSTURE_FLAT


def test_derivation_is_deterministic():
    assets = [_A(str(i), f"10.0.{i % 3}.{i}") for i in range(1, 30)]
    assert derive_topology(assets, ["10.0.0.0/16"]) == derive_topology(list(reversed(assets)), ["10.0.0.0/16"])


# ── hub-based paths ──────────────────────────────────────────────────────────
def test_same_subnet_path_goes_through_the_hub():
    assets = [_A("web", "10.0.1.5", criticality="high"), _A("db", "10.0.1.9", criticality="critical")]
    assets[0].tags = {"internet_exposed": True}
    g = _graph(assets, ["web", "db"], ["10.0.1.0/24"])
    paths = PathAnalyzer(g).find_paths_to_target("db")
    assert [p["nodes"] for p in paths] == [["web", "db"]]
    hop = paths[0]["edges"][0]
    assert hop["technique"] == "SAME_SUBNET" and hop["via"] == ["10.0.1.0/24"]
    assert hop["basis"] == "same_subnet"


def test_cross_subnet_path_is_labelled_assumed_and_less_likely():
    web = _A("web", "10.0.1.5", tags={"internet_exposed": True})
    near = _A("near", "10.0.1.9", criticality="critical")
    far = _A("far", "10.0.2.9", criticality="critical")
    g = _graph([web, near, far], ["web", "near", "far"], ["10.0.1.0/24", "10.0.2.0/24"])
    pa = PathAnalyzer(g)
    p_near = pa.find_paths_to_target("near")[0]
    p_far = pa.find_paths_to_target("far")[0]
    assert p_far["nodes"] == ["web", "far"]
    assert p_far["edges"][0]["technique"] == "CROSS_SUBNET"
    assert p_far["edges"][0]["via"] == ["10.0.1.0/24", "10.0.2.0/24"]
    assert p_far["edges"][0]["basis"] == "assumed"
    assert p_far["likelihood"] < p_near["likelihood"]
    assert p_far["segments"] == ["10.0.1.0/24", "10.0.2.0/24"]


def test_hub_never_hands_control_of_an_uncompromisable_host():
    web = _A("web", "10.0.1.5", tags={"internet_exposed": True})
    hard = _A("hard", "10.0.1.6")                      # no exploitable finding
    db = _A("db", "10.0.2.9", criticality="critical")
    g = _graph([web, hard, db], ["web", "db"], ["10.0.1.0/24", "10.0.2.0/24"])
    for p in PathAnalyzer(g).find_paths_to_target("db"):
        assert "hard" not in p["nodes"]


def test_segmented_posture_requires_a_compromised_gateway():
    web = _A("web", "10.0.1.5", tags={"internet_exposed": True})
    gw = _A("gw", "10.0.1.1", device_role="network_device")
    db = _A("db", "10.0.2.9", criticality="critical")
    scope = ["10.0.1.0/24", "10.0.2.0/24"]
    # gateway not compromisable -> no way across
    g = _graph([web, gw, db], ["web", "db"], scope, POSTURE_SEGMENTED)
    assert PathAnalyzer(g).find_paths_to_target("db") == []
    # gateway compromisable -> path goes THROUGH it
    g = _graph([web, gw, db], ["web", "gw", "db"], scope, POSTURE_SEGMENTED)
    paths = PathAnalyzer(g).find_paths_to_target("db")
    assert paths and paths[0]["nodes"] == ["web", "gw", "db"]
    assert paths[0]["edges"][1]["technique"] == "GATEWAY_ROUTE"


def test_hops_count_hosts_not_hubs():
    chain = [_A(f"h{i}", f"10.0.{i}.5") for i in range(4)]
    chain[0].tags = {"internet_exposed": True}
    chain[-1].criticality = "critical"
    # Segmented posture with no gateway: the subnets are unreachable from each other.
    g = _graph(chain, [a.id for a in chain], [f"10.0.{i}.0/24" for i in range(4)],
               POSTURE_SEGMENTED)
    assert PathAnalyzer(g).find_paths_to_target("h3") == []
    # Flat posture: h0 -> hub(10.0.0) -> hub(10.0.3) -> h3 is ONE host hop.
    g = _graph(chain, [a.id for a in chain], [f"10.0.{i}.0/24" for i in range(4)])
    p = PathAnalyzer(g).find_paths_to_target("h3", max_hops=1)[0]
    assert p["hops"] == 1 and p["nodes"] == ["h0", "h3"]


def test_blast_radius_crosses_subnets_in_host_hops():
    a = _A("a", "10.0.1.5")
    b = _A("b", "10.0.1.6")
    c = _A("c", "10.0.2.6")
    g = _graph([a, b, c], ["b", "c"], ["10.0.1.0/24", "10.0.2.0/24"])
    r = PathAnalyzer(g).find_blast_radius("a")
    assert set(r["reachable"]) == {"b", "c"}
    # both are one HOST away (subnet hubs cost nothing), even though c is in another subnet
    assert set(r["by_distance"]["1"]) == {"b", "c"} and list(r["by_distance"]) == ["1"]


def test_diagnose_reports_topology():
    web = _A("web", "10.0.1.5", tags={"internet_exposed": True})
    db = _A("db", "10.0.2.9", criticality="critical")
    d = PathAnalyzer(_graph([web, db], ["db"], ["10.0.1.0/24", "10.0.2.0/24"])).diagnose(["db"])
    assert d["segments"] == 2 and d["reachability_posture"] == POSTURE_FLAT
    assert d["reasons"] == []


def test_large_multi_subnet_engagement_stays_fast():
    # 600 hosts in 6 subnets, every host exploitable: the old pairwise mesh
    # would need ~60k edges per subnet; hubs keep this linear.
    assets = [_A(f"h{s}-{i}", f"10.0.{s}.{i}") for s in range(6) for i in range(1, 101)]
    assets[0].tags = {"internet_exposed": True}
    assets[-1].criticality = "critical"
    g = _graph(assets, [a.id for a in assets], [f"10.0.{s}.0/24" for s in range(6)])
    t = time.time()
    pa = PathAnalyzer(g)
    paths = pa.find_paths_to_target(assets[-1].id)
    elapsed = time.time() - t
    assert paths and elapsed < 5.0, elapsed
    assert pa.movement_graph().number_of_edges() < 3000


# ── build_from_db wiring ─────────────────────────────────────────────────────
class _Rows:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return self

    def all(self):
        return list(self._rows)


class _DB:
    def __init__(self, assets, findings, engagement):
        self._assets, self._findings, self._engagement = assets, findings, engagement
        self.calls = 0

    async def execute(self, stmt):
        self.calls += 1
        sql = str(stmt)
        if "FROM assets" in sql:
            return _Rows(self._assets)
        if "FROM findings" in sql:
            return _Rows(self._findings)
        return _Rows([])

    async def get(self, _model, _ident):
        return self._engagement


def test_build_from_db_supplies_subnet_topology():
    web = _A("11111111-1111-1111-1111-111111111111", "10.0.1.5", tags={"internet_exposed": True})
    db = _A("22222222-2222-2222-2222-222222222222", "10.0.2.9", criticality="critical")
    eng = type("E", (), {"scope_cidrs": ["10.0.1.0/24", "10.0.2.0/24"],
                         "rules_of_engagement": {}})()
    fake = _DB([web, db], [_F(uuid.uuid4(), web.id), _F(uuid.uuid4(), db.id)], eng)
    g = asyncio.run(GraphBuilder().build_from_db(fake, uuid.uuid4()))
    segs = sorted(d["cidr"] for _, d in g.nodes(data=True) if d.get("type") == "NetworkSegment")
    assert segs == ["10.0.1.0/24", "10.0.2.0/24"]
    paths = PathAnalyzer(g).find_paths_to_target(db.id)
    assert paths and paths[0]["nodes"] == [web.id, db.id]


def test_hop_explanation_flags_assumed_cross_subnet_reachability():
    from app.routers.attack_paths import _explain_hop
    text = _explain_hop({"source": "a", "target": "b", "technique": "CROSS_SUBNET",
                         "via": ["10.0.1.0/24", "10.0.2.0/24"], "basis": "assumed",
                         "exploited": True, "cvss": 9.1}, {"a": "web01", "b": "db01"})
    assert "10.0.1.0/24" in text and "10.0.2.0/24" in text
    assert "assumed" in text and "verify segmentation" in text
