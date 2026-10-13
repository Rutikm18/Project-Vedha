"""
P5d — the Neo4j mirror stays correct (FM-28/29) and stored attack paths follow the
findings (recompute after detection).

No live Neo4j: a fake driver records every statement and transaction event, which is
what these properties are about — what is deleted, in what order, in how many
transactions, scoped to which engagement.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import networkx as nx
import pytest

from app.detection import engine_bridge
from app.graph import neo4j_client as nc
from app.graph.builder import GraphBuilder, _neo4j_props
from app.graph.neo4j_client import Neo4jClient
from app.routers import attack_paths as R


# ── a fake driver ────────────────────────────────────────────────────────────

class _Tx:
    def __init__(self, log, fail_on=None):
        self.log, self.fail_on, self.committed, self.closed = log, fail_on, False, False

    def run(self, cypher, **params):
        if self.fail_on and self.fail_on in cypher:
            raise RuntimeError("boom")
        self.log.append(("run", cypher, params))

    def commit(self):
        self.committed = True
        self.log.append(("commit",))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.closed = True
        if not self.committed:
            self.log.append(("rollback",))
        return False


class _Session:
    def __init__(self, log, fail_on=None):
        self.log, self.fail_on = log, fail_on

    def begin_transaction(self):
        self.log.append(("begin",))
        return _Tx(self.log, self.fail_on)

    def run(self, cypher, **params):
        self.log.append(("session_run", cypher))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _Driver:
    def __init__(self, fail_on=None):
        self.log, self.fail_on = [], fail_on

    def session(self):
        return _Session(self.log, self.fail_on)


def _client(fail_on=None) -> tuple[Neo4jClient, _Driver]:
    c = Neo4jClient("bolt://x", "u", "p")
    c._driver = _Driver(fail_on)
    return c, c._driver


def _graph():
    g = nx.MultiDiGraph()
    g.graph["engagement_id"] = "E1"
    g.add_node("asset:1", type="Asset", entity_id="1", criticality="high", stale=False)
    g.add_node("asset:2", type="Asset", entity_id="2", criticality="critical")
    g.add_node("segment:10.0.0.0/24", type="NetworkSegment", label="10.0.0.0/24")
    g.add_edge("asset:1", "asset:2", type="CREDENTIAL_REUSE", label="svc-backup")
    g.add_edge("asset:1", "asset:2", type="CREDENTIAL_REUSE", label="admin")     # same pair, same type
    g.add_edge("asset:1", "segment:10.0.0.0/24", type="IN_SEGMENT")
    return g


def _builder(client: Neo4jClient) -> GraphBuilder:
    b = GraphBuilder(neo4j=client)
    b.graph = _graph()
    return b


# ── FM-28: indexes on the label the mirror writes ────────────────────────────

def test_schema_indexes_the_label_that_is_actually_written():
    joined = " ".join(nc.SCHEMA_STATEMENTS)
    assert "FOR (n:GraphNode) ON (n.engagement_id, n.type)" in joined
    assert "FOR (n:GraphNode) ON (n.engagement_id, n.key)" in joined
    # and every statement is idempotent
    assert all("IF NOT EXISTS" in s for s in nc.SCHEMA_STATEMENTS)
    # the label the sync writes is the label the index covers
    assert ":GraphNode" in nc.MIRROR_NODES


def test_a_failed_index_statement_is_logged_not_silent():
    c, _ = _client()

    class _FailingSession(_Session):
        def run(self, cypher, **p):
            raise RuntimeError("no privilege")

    c._driver.session = lambda: _FailingSession([])
    with patch.object(nc.logger, "warning") as warn:
        c.ensure_schema()
    assert warn.call_count == len(nc.SCHEMA_STATEMENTS)


# ── FM-29: replace the engagement's mirror, atomically ───────────────────────

def test_sync_deletes_then_writes_in_one_transaction_scoped_to_the_engagement():
    c, d = _client()
    out = _builder(c).sync_to_neo4j("E1")
    assert out == {"nodes": 3, "edges": 3}
    events = [e[0] for e in d.log if e[0] != "session_run"]
    assert events == ["begin", "run", "run", "run", "commit"]            # one transaction
    runs = [e for e in d.log if e[0] == "run"]
    assert runs[0][1] == nc.MIRROR_DELETE and runs[0][2] == {"engagement_id": "E1"}
    assert runs[1][1] == nc.MIRROR_NODES and runs[2][1] == nc.MIRROR_EDGES
    assert "DETACH DELETE" in nc.MIRROR_DELETE and "$engagement_id" in nc.MIRROR_DELETE


def test_a_fixed_weakness_leaves_the_mirror():
    """The second sync deletes the engagement's old nodes first, so a node that is no
    longer in the graph is not left behind (the old code only ever MERGEd)."""
    c, d = _client()
    b = _builder(c)
    b.sync_to_neo4j("E1")
    b.graph.remove_node("asset:2")
    d.log.clear()
    assert b.sync_to_neo4j("E1") == {"nodes": 2, "edges": 1}
    runs = [e for e in d.log if e[0] == "run"]
    assert runs[0][1] == nc.MIRROR_DELETE                                # wiped before the rewrite
    assert {n["key"] for n in runs[1][2]["batch"]} == {"asset:1", "segment:10.0.0.0/24"}


def test_parallel_edges_stay_distinct():
    c, d = _client()
    _builder(c).sync_to_neo4j("E1")
    edges = next(e for e in d.log if e[0] == "run" and e[1] == nc.MIRROR_EDGES)[2]["batch"]
    pair = [e for e in edges if e["src"] == "asset:1" and e["dst"] == "asset:2"]
    assert len(pair) == 2 and len({e["ekey"] for e in pair}) == 2        # not collapsed on (a, b, type)
    assert {e["label"] for e in pair} == {"svc-backup", "admin"}
    assert "CREATE (a)-[r:REL]->(b)" in nc.MIRROR_EDGES and "MERGE (a)-[" not in nc.MIRROR_EDGES


def test_node_identity_includes_the_engagement():
    """'segment:10.0.0.0/24' exists in every engagement that uses that subnet, so the
    node key alone would merge two tenants' hubs into one node."""
    assert "MERGE (x:GraphNode {engagement_id: n.engagement_id, key: n.key})" in nc.MIRROR_NODES
    assert "engagement_id: e.engagement_id, key: e.src" in nc.MIRROR_EDGES
    assert "engagement_id: e.engagement_id, key: e.dst" in nc.MIRROR_EDGES
    for eid in ("E1", "E2"):
        c, d = _client()
        _builder(c).sync_to_neo4j(eid)
        batch = next(e for e in d.log if e[0] == "run" and e[1] == nc.MIRROR_NODES)[2]["batch"]
        assert {n["engagement_id"] for n in batch} == {eid}
        edges = next(e for e in d.log if e[0] == "run" and e[1] == nc.MIRROR_EDGES)[2]["batch"]
        assert {e["engagement_id"] for e in edges} == {eid}


def test_a_failure_part_way_rolls_back_and_is_reported_not_raised():
    c, d = _client(fail_on="UNWIND $batch AS e")                          # the edge write fails
    out = _builder(c).sync_to_neo4j("E1")
    assert out["nodes"] == 0 and out["edges"] == 0 and "error" in out
    assert ("commit",) not in d.log and ("rollback",) in d.log            # the delete is undone, too


def test_large_graphs_are_written_in_batches():
    c, d = _client()
    b = GraphBuilder(neo4j=c)
    b.graph = nx.MultiDiGraph()
    n = nc.MIRROR_BATCH_SIZE * 2 + 7
    for i in range(n):
        b.graph.add_node(f"asset:{i}", type="Asset")
    b.sync_to_neo4j("E1")
    node_runs = [e for e in d.log if e[0] == "run" and e[1] == nc.MIRROR_NODES]
    assert [len(e[2]["batch"]) for e in node_runs] == [nc.MIRROR_BATCH_SIZE, nc.MIRROR_BATCH_SIZE, 7]
    assert sum(1 for e in d.log if e[0] == "begin") == 1                  # still one transaction


def test_not_connected_is_a_quiet_no_op():
    c = Neo4jClient("bolt://x", "u", "p")                                 # never connected
    assert c.replace_engagement("E1", [], []) is False
    assert GraphBuilder(neo4j=None).sync_to_neo4j("E1") == {"nodes": 0, "edges": 0}


def test_an_outage_on_the_first_statement_is_reported_not_raised():
    """An unreachable mirror must not stop the in-memory analysis (build_from_db
    calls sync_to_neo4j and ignores a failed mirror)."""
    c, _ = _client(fail_on="DETACH DELETE")
    b = _builder(c)
    assert "error" in b.sync_to_neo4j("E1")                               # reported, not raised


# ── property sanitising ──────────────────────────────────────────────────────

def test_neo4j_props_only_emit_values_the_database_accepts():
    out = _neo4j_props({
        "none": None, "nested": {"a": 1}, "ints": [1, 2], "mixed": [1, "a"], "set": {3, 1},
        "dec": Decimal("1.5"), "when": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "dicts": [{"a": 1}], "flag": True, "empty": [], "id": uuid.UUID(int=5),
    })
    assert "none" not in out
    assert out["nested"] == '{"a": 1}' and out["mixed"] == '[1, "a"]' and out["dicts"] == '[{"a": 1}]'
    assert out["ints"] == [1, 2] and out["set"] == [1, 3] and out["empty"] == []
    assert out["dec"] == 1.5 and out["flag"] is True
    assert out["when"].startswith("2026-01-01") and out["id"] == str(uuid.UUID(int=5))
    for v in out.values():
        assert isinstance(v, (str, int, float, bool, list))


def test_mirror_keys_cannot_be_overwritten_by_attributes():
    c, d = _client()
    b = GraphBuilder(neo4j=c)
    b.graph = nx.MultiDiGraph()
    b.graph.add_node("asset:1", type="Asset", key="evil", engagement_id="other")
    b.sync_to_neo4j("E1")
    node = next(e for e in d.log if e[0] == "run" and e[1] == nc.MIRROR_NODES)[2]["batch"][0]
    assert node["key"] == "asset:1" and node["engagement_id"] == "E1"


# ── recompute after detection ────────────────────────────────────────────────

class _FakeResult:
    def __init__(self, first=None):
        self._first = first

    def first(self):
        return self._first


class _FakeDB:
    def __init__(self, has_path=False, analysis=None):
        self.has_path, self.analysis = has_path, analysis
        self.nested = 0

    async def execute(self, stmt, params=None):
        return _FakeResult((uuid.uuid4(),) if self.has_path else None)

    async def get(self, model, key):
        return self.analysis

    def begin_nested(self):
        db = self

        class _CM:
            async def __aenter__(self):
                db.nested += 1

            async def __aexit__(self, *exc):
                return False
        return _CM()


@pytest.mark.asyncio
async def test_nothing_is_computed_for_an_engagement_with_no_stored_results():
    db = _FakeDB()
    with patch.object(R, "_recompute_and_store", new=AsyncMock()) as rc:
        assert await R.refresh_if_materialised(db, uuid.uuid4()) is False
    rc.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("db", [_FakeDB(has_path=True), _FakeDB(analysis=object())])
async def test_stored_results_are_recomputed_in_a_savepoint(db):
    eng = uuid.uuid4()
    with patch.object(R, "_recompute_and_store", new=AsyncMock()) as rc:
        assert await R.refresh_if_materialised(db, eng) is True
    rc.assert_awaited_once_with(db, eng, None, trigger="detection")      # history says why it was recomputed
    assert db.nested == 1                      # a failure inside rolls back only the savepoint


@pytest.mark.asyncio
async def test_a_refresh_failure_never_reaches_the_detection_run():
    with patch.object(R, "refresh_if_materialised", new=AsyncMock(side_effect=RuntimeError("graph build failed"))):
        await engine_bridge._refresh_attack_paths(MagicMock(), uuid.uuid4())      # does not raise


async def _run_detection(resolved: int, detected: list | None = None):
    result = {"facts": [{"scanner": "tls_scan", "target": "10.0.0.5:443", "status": "open"}],
              "scanner_runs": [{"id": "tls_scan", "status": "completed"}]}
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))
    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_all_from_facts_traced",
                      return_value=(detected or [], [], {"coverage": {}, "verdicts": {}})), \
         patch.object(engine_bridge, "evaluate_resolutions", new=AsyncMock(return_value=resolved)), \
         patch.object(engine_bridge, "_refresh_attack_paths", new=AsyncMock()) as refresh:
        await engine_bridge.create_findings_from_facts(db, uuid.uuid4(), result)
    return refresh


@pytest.mark.asyncio
async def test_detection_that_resolved_something_refreshes_stored_paths():
    refresh = await _run_detection(resolved=2)
    refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_detection_that_changed_nothing_does_not_recompute():
    refresh = await _run_detection(resolved=0)
    refresh.assert_not_awaited()


# ── the list endpoint's rows are readable (UI contract) ──────────────────────

def test_path_summary_carries_labels_and_freshness_beside_the_authoritative_ids():
    from types import SimpleNamespace
    row = SimpleNamespace(
        id=uuid.UUID(int=1), risk_score=Decimal("42.5"),
        path_nodes=["asset:a", "asset:b", "asset:c"], chokepoints=["asset:b"],
        path_edges=[{"stale": False}, {"stale": True}])
    out = R._path_summary(row, {"asset:a": "web-1", "asset:c": "db-1 @ HQ"})
    assert out["source"] == "asset:a" and out["target"] == "asset:c"          # ids stay authoritative
    assert out["source_label"] == "web-1" and out["target_label"] == "db-1 @ HQ"
    assert out["freshness"] == "partly_stale" and out["hops"] == 2 and out["chokepoint_count"] == 1
    # the whole route, with the asset's own id (what the choke-point analysis names), not the node key
    assert out["nodes"] == [{"asset_id": "a", "label": "web-1"}, {"asset_id": "b", "label": "asset:b"},
                            {"asset_id": "c", "label": "db-1 @ HQ"}]


def test_path_summary_without_labels_falls_back_to_the_ids():
    from types import SimpleNamespace
    row = SimpleNamespace(id=uuid.UUID(int=2), risk_score=None, path_nodes=["asset:a", "asset:b"],
                          chokepoints=None, path_edges=None)
    out = R._path_summary(row)
    assert out["source_label"] == "asset:a" and out["target_label"] == "asset:b"
    assert out["risk_score"] is None and out["freshness"] == "fresh" and out["chokepoint_count"] == 0


def test_no_targets_message_does_not_claim_an_auto_selection():
    """Targets are operator-defined; nothing auto-selects crown jewels."""
    from app.graph.analyzer import PathAnalyzer
    reasons = PathAnalyzer(nx.MultiDiGraph()).diagnose([])["reasons"]
    detail = next(r["detail"] for r in reasons if r["code"] == "no_targets")
    assert "auto" not in detail.lower() and "marked critical" in detail


def test_the_api_is_labelled_beta():
    assert R.router.tags == ["attack-paths (beta)"]
    assert "BETA" in (R.__doc__ or "")
