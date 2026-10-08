"""
test_attack_paths_p5.py — P5: which host should be fixed first, measured on the
network instead of counted on a truncated path list (FM-20, FM-25).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal

import pytest

from app.detection.reachability import POSTURE_SEGMENTED, derive_topology
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder


@dataclass
class _A:
    id: str
    ip_address: str | None
    device_role: str | None = None
    criticality: str = "medium"
    environment: str | None = None
    hostname: str | None = None
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


def _analyzer(assets, exploitable, scope, posture=POSTURE_SEGMENTED):
    b = GraphBuilder()
    b.build_asset_graph("eng", assets, [], [_F(uuid.uuid4(), a) for a in exploitable])
    b.add_segment_topology(derive_topology(assets, scope, posture))
    return PathAnalyzer(b.graph)


SCOPE = ["10.0.1.0/24", "10.0.2.0/24"]


def _bottleneck():
    """Two exposed hosts; the ONLY way into the inner network is one gateway."""
    return _analyzer(
        [_A("e1", "10.0.1.5", environment="dmz"), _A("e2", "10.0.1.6", environment="dmz"),
         _A("gw", "10.0.1.1", device_role="network_device"),
         _A("jewel", "10.0.2.9", criticality="critical")],
        ["e1", "e2", "gw", "jewel"], SCOPE)


def test_the_single_bottleneck_is_the_minimum_fix_set():
    result = _bottleneck().choke_analysis(["jewel"])
    assert result["min_fix_set"]["size"] == 1 and result["min_fix_set"]["assets"] == ["gw"]
    assert result["min_fix_set"]["independent_routes"] == {"jewel": 1}


def test_fixing_the_bottleneck_ranks_first_and_cuts_the_target_off():
    ranked = _bottleneck().choke_analysis(["jewel"])["ranked"]
    assert ranked[0]["asset_id"] == "gw" and ranked[0]["targets_cut_off"] == ["jewel"]
    assert ranked[0]["risk_removed"] > 0 and ranked[0]["remediation_priority"] == "critical"


def test_the_crown_jewel_itself_is_never_a_candidate():
    assert "jewel" not in {r["asset_id"] for r in _bottleneck().choke_analysis(["jewel"])["ranked"]}


def _two_routes():
    """Two exposed hosts, two gateways: two vertex-disjoint routes to the jewel."""
    return _analyzer(
        [_A("e1", "10.0.1.5", environment="dmz"), _A("e2", "10.0.1.6", environment="dmz"),
         _A("gw1", "10.0.1.1", device_role="network_device"), _A("gw2", "10.0.1.2", device_role="network_device"),
         _A("jewel", "10.0.2.9", criticality="critical")],
        ["e1", "e2", "gw1", "gw2", "jewel"], SCOPE)


def test_independent_routes_are_counted_as_vertex_disjoint_paths():
    result = _two_routes().choke_analysis(["jewel"])
    assert result["min_fix_set"]["independent_routes"] == {"jewel": 2}
    assert result["min_fix_set"]["size"] == 2


def test_fixing_one_of_two_redundant_routes_does_not_cut_the_target_off():
    for entry in _two_routes().choke_analysis(["jewel"])["ranked"]:
        assert entry["targets_cut_off"] == []                      # the other route survives


def test_a_host_on_no_route_removes_no_risk():
    a = _analyzer([_A("e1", "10.0.1.5", environment="dmz"), _A("jewel", "10.0.1.9", criticality="critical"),
                   _A("bystander", "10.0.2.5")], ["e1", "jewel"], SCOPE)
    assert "bystander" not in {r["asset_id"] for r in a.choke_analysis(["jewel"])["ranked"]}


def test_target_risk_is_the_best_path_not_a_sum_of_overlapping_paths():
    result = _two_routes().choke_analysis(["jewel"])
    (target,) = result["targets"]
    paths = _two_routes().find_paths_to_target("jewel")
    assert target["best_likelihood"] == pytest.approx(max(p["likelihood"] for p in paths), rel=0.02)
    assert target["best_likelihood"] <= 1.0                            # a sum of several routes could exceed 1


def test_no_entry_points_or_no_targets_is_an_empty_analysis():
    a = _analyzer([_A("a", "10.0.1.5"), _A("jewel", "10.0.1.9", criticality="critical")], ["jewel"], SCOPE)
    r = a.choke_analysis(["jewel"])
    assert r["ranked"] == [] and r["min_fix_set"]["size"] == 0 and r["entry_points"] == 0
    assert _bottleneck().choke_analysis([])["ranked"] == []
    assert _bottleneck().choke_analysis(["not-an-asset"])["targets"] == []


def test_the_analysis_does_not_depend_on_how_many_paths_were_enumerated():
    """The old path-frequency choke points looked only at the first five paths per source."""
    many = [_A(f"e{i}", f"10.0.1.{10 + i}", environment="dmz") for i in range(8)]
    a = _analyzer(many + [_A("gw", "10.0.1.1", device_role="network_device"),
                          _A("jewel", "10.0.2.9", criticality="critical")],
                  [x.id for x in many] + ["gw", "jewel"], SCOPE)
    r = a.choke_analysis(["jewel"])
    assert r["min_fix_set"]["assets"] == ["gw"] and r["ranked"][0]["asset_id"] == "gw"


def test_the_result_is_deterministic():
    assert _two_routes().choke_analysis(["jewel"]) == _two_routes().choke_analysis(["jewel"])


# ── what gets stored and returned ────────────────────────────────────────────

CHOKE = {
    "ranked": [{"asset_id": "gw", "risk_removed": 40.0, "targets_cut_off": ["jewel"], "remediation_priority": "critical"},
               {"asset_id": "e1", "risk_removed": 5.0, "targets_cut_off": [], "remediation_priority": "medium"},
               {"asset_id": "x", "risk_removed": 0.0, "targets_cut_off": [], "remediation_priority": "medium"}],
    "min_fix_set": {"size": 1, "assets": ["gw"], "independent_routes": {"jewel": 1}},
    "targets": [{"asset_id": "jewel", "best_likelihood": 0.4, "risk": 40.0}],
    "entry_points": 2, "method": "m",
}


def test_each_path_row_keeps_only_the_choke_points_on_that_path():
    from app.routers.attack_paths import path_chokepoints
    assert path_chokepoints(["e1", "gw", "jewel"], CHOKE) == ["e1", "gw"]
    assert path_chokepoints(["e2", "other", "jewel"], CHOKE) == []                 # not the whole engagement's list
    assert path_chokepoints(["x"], CHOKE) == []                                    # zero effect is no choke point
    assert path_chokepoints([], {}) == []


def test_labelled_choke_adds_readable_names_and_keeps_ids():
    from app.routers.attack_paths import labelled_choke
    out = labelled_choke(CHOKE, {"gw": "gateway-1", "jewel": "dc01"})
    assert out["ranked"][0]["label"] == "gateway-1" and out["ranked"][0]["asset_id"] == "gw"
    assert out["ranked"][0]["targets_cut_off_labels"] == ["dc01"]
    assert out["min_fix_set"]["assets"] == [{"asset_id": "gw", "label": "gateway-1"}]
    assert out["min_fix_set"]["independent_routes"] == {"dc01": 1}
    assert out["targets"][0]["label"] == "dc01"
    assert out["ranked"][1]["label"] == "e1"                                       # unknown label falls back to the id


def test_labelling_an_empty_analysis_is_safe():
    from app.routers.attack_paths import labelled_choke
    out = labelled_choke({}, {})
    assert out["ranked"] == [] and out["min_fix_set"]["size"] == 0 and out["targets"] == []


def test_the_analysis_is_stored_once_per_engagement_and_replaced_on_recompute():
    import asyncio
    from types import SimpleNamespace

    from app.routers.attack_paths import _store_analysis

    class DB:
        def __init__(self):
            self.rows = {}

        async def get(self, model, key):
            return self.rows.get(key)

        def add(self, row):
            self.rows[row.engagement_id] = row

    db, eng = DB(), uuid.uuid4()
    asyncio.run(_store_analysis(db, eng, {"choke": {"ranked": []}}, 3))
    first = db.rows[eng]
    assert first.path_count == 3 and first.analysis == {"choke": {"ranked": []}} and first.computed_at is not None
    asyncio.run(_store_analysis(db, eng, {"choke": {"ranked": [1]}}, 5))
    assert db.rows[eng] is first and first.path_count == 5 and first.analysis["choke"]["ranked"] == [1]
    assert len(db.rows) == 1


def test_the_stored_analysis_is_json_serialisable():
    import json
    json.dumps(_bottleneck().choke_analysis(["jewel"]))
