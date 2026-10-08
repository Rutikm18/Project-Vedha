"""
test_attack_paths_p0.py — P0 engine-correctness fixes for attack-path generation.

Each test pins one failure mode from manager/docs/ATTACK_PATH_PLAN.md §9 so it
cannot silently come back. Pure in-memory graphs; no DB.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

import networkx as nx

from app.graph.analyzer import (
    CYPHER_BLAST_RADIUS, CYPHER_CHOKEPOINTS, CYPHER_SHORTEST_PATH, PathAnalyzer,
    step_likelihood,
)
from app.graph.builder import GraphBuilder, is_live_finding
from app.routers.attack_paths import path_id_for


# ── tiny graph helpers ───────────────────────────────────────────────────────
def _graph(assets: dict[str, dict], edges: list[tuple[str, str, str]],
           exploits: dict[str, dict] | None = None) -> nx.MultiDiGraph:
    """assets: name -> node attrs; edges: (src, dst, rel); exploits: name -> finding attrs."""
    g = nx.MultiDiGraph()
    for name, attrs in assets.items():
        g.add_node(f"asset:{name}", type="Asset", entity_id=name,
                   criticality=attrs.get("criticality", "medium"),
                   internet_exposed=attrs.get("internet_exposed", False))
    for name, fattrs in (exploits or {}).items():
        fid = f"finding:{name}"
        g.add_node(fid, type="Finding", entity_id=f"f-{name}", exploitable=True,
                   cvss=fattrs.get("cvss", 7.0), severity=fattrs.get("severity", "high"),
                   **{k: v for k, v in fattrs.items() if k not in ("cvss", "severity")})
        g.add_edge(f"asset:{name}", fid, type="HAS_FINDING")
        g.add_edge(fid, f"asset:{name}", type="EXPLOITS", weight=1.0)
    for src, dst, rel in edges:
        g.add_edge(f"asset:{src}", f"asset:{dst}", type=rel, weight=1.0)
    return g


# ── FM-05: monotonic control ─────────────────────────────────────────────────
def test_no_pivot_through_a_host_that_cannot_be_compromised():
    g = _graph({"A": {"internet_exposed": True}, "B": {}, "C": {"criticality": "critical"}},
               [("A", "B", "CONNECTS_TO"), ("B", "C", "CONNECTS_TO")],
               exploits={"C": {}})
    assert PathAnalyzer(g).find_paths_to_target("C") == []


def test_credential_reuse_grants_control_without_an_exploit():
    # A is the foothold (exposed AND exploitable); B has no exploit but valid creds reach it.
    g = _graph({"A": {"internet_exposed": True}, "B": {}, "C": {"criticality": "critical"}},
               [("A", "B", "CREDENTIAL_REUSE"), ("B", "C", "CONNECTS_TO")],
               exploits={"A": {}, "C": {}})
    paths = PathAnalyzer(g).find_paths_to_target("C")
    assert [p["nodes"] for p in paths] == [["A", "B", "C"]]
    assert paths[0]["edges"][0]["technique"] == "CREDENTIAL_REUSE"


def test_blast_radius_counts_only_hosts_the_attacker_can_control():
    g = _graph({"A": {}, "B": {}, "C": {}},
               [("A", "B", "CONNECTS_TO"), ("A", "C", "CONNECTS_TO")],
               exploits={"C": {}})
    r = PathAnalyzer(g).find_blast_radius("A")
    assert r["reachable"] == ["C"]          # B is reachable but not compromisable


# ── FM-17 / 18 / 19: likelihood scoring ──────────────────────────────────────
def test_short_critical_path_outranks_long_mediocre_chain():
    pa = PathAnalyzer(nx.MultiDiGraph())
    short = {"hops": 1, "edges": [{"cvss": 9.8, "technique": "CONNECTS_TO"}]}
    long_ = {"hops": 4, "edges": [{"cvss": 7.0, "technique": "SAME_SEGMENT"}] * 4}
    assert pa.score_path(short) > pa.score_path(long_)   # was 18.1 vs 50.0


def test_likelihood_never_increases_with_more_steps():
    pa = PathAnalyzer(nx.MultiDiGraph())
    step = {"likelihood": 0.9, "technique": "CONNECTS_TO"}
    scores = [pa.path_likelihood({"hops": n, "edges": [step] * n}) for n in range(1, 7)]
    assert scores == sorted(scores, reverse=True)


def test_misconfiguration_only_path_has_nonzero_score():
    pa = PathAnalyzer(nx.MultiDiGraph())
    misconf = {"hops": 2, "edges": [{"cvss": 0.0, "technique": "SAME_SEGMENT"}] * 2}
    assert pa.score_path(misconf) > 0                    # was 0.0


def test_epss_raises_and_low_confidence_lowers_step_likelihood():
    base = {"severity": "medium"}
    assert step_likelihood({**base, "epss": 0.9}) > step_likelihood(base)
    assert step_likelihood({**base, "confidence": 40}) < step_likelihood(base)
    assert step_likelihood({"exploit_validated": True}) >= step_likelihood({"severity": "critical"})


def test_target_criticality_scales_risk_not_likelihood():
    pa = PathAnalyzer(nx.MultiDiGraph())
    e = [{"likelihood": 0.8, "technique": "CONNECTS_TO"}]
    crit = {"hops": 1, "edges": e, "target_criticality": "critical"}
    low = {"hops": 1, "edges": e, "target_criticality": "low"}
    assert pa.path_likelihood(crit) == pa.path_likelihood(low)
    assert pa.score_path(crit) > pa.score_path(low)


def test_paths_are_returned_most_likely_first():
    g = _graph({"A": {"internet_exposed": True}, "B": {}, "C": {"criticality": "critical"}},
               [("A", "C", "CONNECTS_TO"), ("A", "B", "CONNECTS_TO"), ("B", "C", "CONNECTS_TO")],
               exploits={"A": {}, "B": {"exploit_validated": True}, "C": {"severity": "low"}})
    paths = PathAnalyzer(g).find_paths_to_target("C")
    assert len(paths) == 2            # direct and via B — guards against a vacuous pass
    scores = [p["risk_score"] for p in paths]
    assert scores == sorted(scores, reverse=True)
    assert all("likelihood" in p for p in paths)


# ── FM-06: only live findings are attack steps ───────────────────────────────
@dataclass
class _A:
    id: uuid.UUID
    ip_address: str = "10.0.0.1"
    hostname: str | None = None
    criticality: str = "medium"
    environment: str | None = None
    tags: dict = field(default_factory=dict)


@dataclass
class _F:
    id: uuid.UUID
    asset_id: uuid.UUID
    status: str
    title: str = "t"
    severity: str = "high"
    cvss_score: Decimal | None = Decimal("8.0")
    exploitable: bool = True
    exploit_validated: bool = False


def test_remediated_accepted_and_fp_findings_are_not_steps():
    a = _A(uuid.uuid4())
    findings = [_F(uuid.uuid4(), a.id, s) for s in ("open", "confirmed", "remediated", "accepted", "fp")]
    g = GraphBuilder().build_asset_graph("e", [a], [], findings)
    titles = {d["entity_id"] for _, d in g.nodes(data=True) if d.get("type") == "Finding"}
    assert titles == {str(findings[0].id), str(findings[1].id)}
    assert is_live_finding(_F(uuid.uuid4(), a.id, "open"))
    assert not is_live_finding(_F(uuid.uuid4(), a.id, "remediated"))


# ── FM-21 / 23: bounded search on a flat subnet ──────────────────────────────
def test_flat_subnet_mesh_stays_fast_and_bounded():
    n = 40   # all_simple_paths on a 11-host mesh already took ~7s
    names = [f"h{i}" for i in range(n)]
    assets = {nm: {} for nm in names}
    assets["h0"]["internet_exposed"] = True
    assets[names[-1]]["criticality"] = "critical"
    edges = [(a, b, "SAME_SEGMENT") for a in names for b in names if a != b]
    g = _graph(assets, edges, exploits={nm: {} for nm in names})
    t = time.time()
    paths = PathAnalyzer(g).find_paths_to_target(names[-1], max_paths_per_source=5)
    assert time.time() - t < 5.0
    assert 1 <= len(paths) <= 5
    assert paths[0]["hops"] == 1                         # most likely = direct


def test_max_hops_is_respected():
    chain = [f"c{i}" for i in range(6)]
    assets = {c: {} for c in chain}
    assets["c0"]["internet_exposed"] = True
    g = _graph(assets, [(a, b, "CONNECTS_TO") for a, b in zip(chain, chain[1:])],
               exploits={c: {} for c in chain})
    pa = PathAnalyzer(g)
    assert pa.find_paths_to_target("c5", max_hops=3) == []
    assert pa.find_paths_to_target("c5", max_hops=5)[0]["hops"] == 5


# ── FM-30: an empty result explains itself ───────────────────────────────────
def test_diagnose_names_every_missing_precondition():
    g = _graph({"A": {}, "B": {}}, [])
    d = PathAnalyzer(g).diagnose([])
    codes = {r["code"] for r in d["reasons"]}
    assert {"no_entry_points", "no_targets", "no_reachability", "no_exploitable_steps"} <= codes


def test_diagnose_flags_reachable_but_uncompromisable():
    g = _graph({"A": {"internet_exposed": True}, "B": {"criticality": "critical"}},
               [("A", "B", "CONNECTS_TO")])
    g.add_node("finding:x", type="Finding", entity_id="fx", exploitable=True)  # orphan exploit
    d = PathAnalyzer(g).diagnose(["B"])
    assert "no_control_edges" in {r["code"] for r in d["reasons"]}


def test_diagnose_clean_when_paths_possible():
    g = _graph({"A": {"internet_exposed": True}, "B": {"criticality": "critical"}},
               [("A", "B", "CONNECTS_TO")], exploits={"A": {}, "B": {}})
    assert PathAnalyzer(g).diagnose(["B"])["reasons"] == []


# ── FM-24: stable, engagement-scoped path ids ────────────────────────────────
def test_path_id_is_deterministic_and_engagement_scoped():
    e1, e2 = uuid.uuid4(), uuid.uuid4()
    nodes = ["a", "b", "c"]
    assert path_id_for(e1, nodes) == path_id_for(e1, list(nodes))
    assert path_id_for(e1, nodes) != path_id_for(e2, nodes)
    assert path_id_for(e1, nodes) != path_id_for(e1, ["a", "c"])


# ── FM-27: Cypher is engagement-scoped ───────────────────────────────────────
def test_every_cypher_query_is_engagement_scoped():
    for q in (CYPHER_SHORTEST_PATH, CYPHER_BLAST_RADIUS, CYPHER_CHOKEPOINTS):
        assert "$engagement_id" in q


# ── FM-24: recompute UPSERTS by id (no delete-all), stale paths removed ──────
import asyncio  # noqa: E402
from unittest.mock import patch  # noqa: E402

from app.routers import attack_paths as R  # noqa: E402


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return self

    def all(self):
        return list(self._rows)


class _FakeDB:
    """Records deletes/adds; returns the current AttackPath rows for selects."""

    def __init__(self):
        self.rows: dict = {}
        self.deleted_ids: list = []

    async def execute(self, stmt, params=None):
        sql = str(stmt)
        if sql.startswith("DELETE"):
            ids = stmt.whereclause.clauses[-1].right.value  # AttackPath.id IN (...)
            for i in ids:
                self.rows.pop(i, None)
            self.deleted_ids.extend(ids)
            return _Result([])
        if "pg_advisory_xact_lock" in sql:
            return _Result([])
        return _Result(self.rows.values())

    def add(self, row):
        self.rows[row.id] = row

    async def flush(self):
        return None


def _analyzer_returning(paths):
    class _A:
        def find_paths_to_target(self, _tid):
            return [dict(p) for p in paths]

        def identify_chokepoints(self, _paths):
            return []

        def diagnose(self, _t):
            return {"reasons": []}
    return _A()


def _p(nodes, score):
    return {"nodes": nodes, "edges": [], "risk_score": score, "hops": len(nodes) - 1}


def test_recompute_keeps_ids_and_removes_only_stale_paths():
    eng = uuid.uuid4()
    db = _FakeDB()
    first = [_p(["a", "b", "z"], 60.0), _p(["a", "c", "z"], 40.0)]
    second = [_p(["a", "b", "z"], 70.0), _p(["a", "d", "z"], 30.0)]   # c-path gone, d-path new

    async def run(paths):
        async def _build(_db, _eid):
            return _analyzer_returning(paths), None

        async def _targets(_db, _eid, _t):
            return ["z"]
        with patch.object(R, "_build_analyzer", _build), patch.object(R, "_target_ids", _targets):
            await R._recompute_and_store(db, eng, None)

    asyncio.run(run(first))
    keep_id = R.path_id_for(eng, ["a", "b", "z"])
    gone_id = R.path_id_for(eng, ["a", "c", "z"])
    kept_row = db.rows[keep_id]
    assert set(db.rows) == {keep_id, gone_id}

    asyncio.run(run(second))
    assert set(db.rows) == {keep_id, R.path_id_for(eng, ["a", "d", "z"])}
    assert db.deleted_ids == [gone_id]                   # only the stale path deleted
    assert db.rows[keep_id] is kept_row                  # same row, updated in place
    assert float(kept_row.risk_score) == 70.0
