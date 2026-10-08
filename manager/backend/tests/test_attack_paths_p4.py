"""
test_attack_paths_p4.py — P4a: internet entry points from the fleet-fused
service exposure verdict (manager/docs/ATTACK_PATH_PLAN.md §3.2, FM-02).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal

from app.detection.reachability import derive_topology
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder, asset_node_id


@dataclass
class _A:
    id: str
    ip_address: str
    criticality: str = "medium"
    hostname: str | None = None
    environment: str | None = None
    tags: dict = field(default_factory=dict)


@dataclass
class _S:
    id: uuid.UUID
    asset_id: str
    port: int
    exposure: str | None = None
    service_name: str = "svc"


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


def _build(assets, services, exploitable_ids, scope):
    b = GraphBuilder()
    b.build_asset_graph("eng", assets, services, [_F(uuid.uuid4(), a) for a in exploitable_ids])
    b.add_segment_topology(derive_topology(assets, scope))
    return b.graph


def test_external_service_marks_its_host_as_internet_exposed():
    web = _A("web", "10.0.1.5")
    g = _build([web], [_S(uuid.uuid4(), "web", 443, "external"),
                       _S(uuid.uuid4(), "web", 22, "internal_only")], [], ["10.0.1.0/24"])
    node = g.nodes[asset_node_id("web")]
    assert node["internet_exposed"] is True
    assert node["exposure_basis"] == "service_exposure"
    assert node["exposed_ports"] == [443]          # only the externally-seen port


def test_internal_only_or_ambiguous_exposure_is_not_an_entry_point():
    a = _A("a", "10.0.1.5")
    g = _build([a], [_S(uuid.uuid4(), "a", 80, "internal_only"),
                     _S(uuid.uuid4(), "a", 81, "ambiguous"),
                     _S(uuid.uuid4(), "a", 82, None)], [], ["10.0.1.0/24"])
    assert g.nodes[asset_node_id("a")]["internet_exposed"] is False


def test_service_exposure_alone_now_yields_a_path():
    # The end-to-end gap P4a closes: before, nothing read Service.exposure, so a
    # host seen open from an external probe never started a path.
    web = _A("web", "10.0.1.5")
    db = _A("db", "10.0.2.9", criticality="critical")
    g = _build([web, db], [_S(uuid.uuid4(), "web", 443, "external")],
               ["web", "db"], ["10.0.1.0/24", "10.0.2.0/24"])
    paths = PathAnalyzer(g).find_paths_to_target("db")
    assert paths and paths[0]["nodes"] == ["web", "db"]


def test_exposed_host_without_an_exploitable_finding_is_not_a_foothold():
    web = _A("web", "10.0.1.5")
    db = _A("db", "10.0.1.9", criticality="critical")
    g = _build([web, db], [_S(uuid.uuid4(), "web", 443, "external")],
               ["db"], ["10.0.1.0/24"])
    pa = PathAnalyzer(g)
    assert pa.find_paths_to_target("db") == []
    codes = {r["code"] for r in pa.diagnose(["db"])["reasons"]}
    assert "entry_points_not_compromisable" in codes
    assert "no_entry_points" not in codes


def test_diagnose_reports_no_exposure_when_nothing_is_external():
    a = _A("a", "10.0.1.5")
    g = _build([a], [_S(uuid.uuid4(), "a", 22, "internal_only")], ["a"], ["10.0.1.0/24"])
    d = PathAnalyzer(g).diagnose(["a"])
    assert {r["code"] for r in d["reasons"]} >= {"no_entry_points"}
    assert d["internet_exposed_assets"] == 0


def test_asset_tag_exposure_still_works_and_is_labelled():
    web = _A("web", "10.0.1.5", tags={"internet_exposed": True})
    g = _build([web], [], ["web"], ["10.0.1.0/24"])
    node = g.nodes[asset_node_id("web")]
    assert node["internet_exposed"] is True and node["exposure_basis"] == "asset_tag"
