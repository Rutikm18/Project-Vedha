"""
Neo4jClient — thin, optional wrapper around the neo4j Python driver.

Neo4j is *optional*: the attack-path engine builds and analyses an in-memory
NetworkX graph regardless, and mirrors it into Neo4j only when a client is
provided and connected. This keeps the engine fully testable without a running
database while still supporting Cypher shortest-path queries at scale.

Indexing strategy for large graphs (>10k nodes):
  * UNIQUE constraint on :Asset(id) — also creates a backing index, makes node
    MERGE O(log n) instead of a label scan.
  * Range indexes on :Asset(engagement_id), :Asset(criticality), and
    :Asset(internet_exposed) so source/target selection and per-engagement
    sub-graph extraction don't scan every node.
  * Index on :Finding(cvss) to let path scoring pull exploit weights via index.
  * The mirror itself writes ONE label, :GraphNode (the real node type is a property,
    so APOC is not required). :GraphNode is indexed on (engagement_id, type) for the
    source/target lookups in analyzer.CYPHER_* and on (engagement_id, key) for node
    identity, so a per-engagement sync never scans another tenant's nodes (FM-28).
  * shortestPath/allShortestPaths with a bounded variable-length pattern
    (`[*..10]`) so traversal cost stays bounded on dense graphs.
"""
from __future__ import annotations

from typing import Any

import structlog

logger = structlog.get_logger()

try:
    from neo4j import GraphDatabase

    _HAS_NEO4J = True
except ImportError:  # pragma: no cover
    GraphDatabase = None  # type: ignore
    _HAS_NEO4J = False


# Constraints + indexes applied once per database (idempotent).
SCHEMA_STATEMENTS: list[str] = [
    "CREATE CONSTRAINT asset_id IF NOT EXISTS FOR (a:Asset) REQUIRE a.id IS UNIQUE",
    "CREATE CONSTRAINT finding_id IF NOT EXISTS FOR (f:Finding) REQUIRE f.id IS UNIQUE",
    "CREATE CONSTRAINT service_id IF NOT EXISTS FOR (s:Service) REQUIRE s.id IS UNIQUE",
    "CREATE INDEX asset_engagement IF NOT EXISTS FOR (a:Asset) ON (a.engagement_id)",
    "CREATE INDEX asset_criticality IF NOT EXISTS FOR (a:Asset) ON (a.criticality)",
    "CREATE INDEX asset_exposed IF NOT EXISTS FOR (a:Asset) ON (a.internet_exposed)",
    "CREATE INDEX finding_cvss IF NOT EXISTS FOR (f:Finding) ON (f.cvss)",
    # The label the mirror actually writes (FM-28). The :Asset/:Finding/:Service
    # statements above are kept for databases that already carry those labels.
    "CREATE INDEX graphnode_engagement_type IF NOT EXISTS FOR (n:GraphNode) ON (n.engagement_id, n.type)",
    "CREATE INDEX graphnode_engagement_key IF NOT EXISTS FOR (n:GraphNode) ON (n.engagement_id, n.key)",
]

# ── per-engagement mirror (FM-29) ─────────────────────────────────────────────
# The mirror is REPLACED, never merged: a weakness that was fixed must disappear
# from it, and two relationships of one type between the same pair of hosts are two
# relationships. Everything is scoped by engagement_id, and node identity is
# (engagement_id, key) — a subnet hub is called "segment:10.0.0.0/24" in EVERY
# engagement that uses that subnet, so a key alone would merge tenants' nodes.
MIRROR_DELETE = "MATCH (n:GraphNode {engagement_id: $engagement_id}) DETACH DELETE n"
MIRROR_NODES = (
    "UNWIND $batch AS n "
    "MERGE (x:GraphNode {engagement_id: n.engagement_id, key: n.key}) SET x += n"
)
MIRROR_EDGES = (
    "UNWIND $batch AS e "
    "MATCH (a:GraphNode {engagement_id: e.engagement_id, key: e.src}) "
    "MATCH (b:GraphNode {engagement_id: e.engagement_id, key: e.dst}) "
    "CREATE (a)-[r:REL]->(b) SET r += e"
)
MIRROR_BATCH_SIZE = 5000


class Neo4jClient:
    """Connection holder + query helper. No-ops cleanly when the driver is absent."""

    def __init__(self, uri: str, user: str, password: str):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver: Any = None

    @property
    def available(self) -> bool:
        return _HAS_NEO4J

    def connect(self) -> bool:
        """Open the driver and verify connectivity. Returns False on any failure."""
        if not _HAS_NEO4J:
            logger.warning("graph.neo4j.driver_missing", hint="pip install neo4j")
            return False
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
            self._driver.verify_connectivity()
            logger.info("graph.neo4j.connected", uri=self._uri)
            return True
        except Exception as exc:
            logger.warning("graph.neo4j.connect_failed", uri=self._uri, error=str(exc))
            self._driver = None
            return False

    def ensure_schema(self) -> None:
        """Apply constraints + indexes (idempotent)."""
        if self._driver is None:
            return
        with self._driver.session() as session:
            for stmt in SCHEMA_STATEMENTS:
                try:
                    session.run(stmt)
                except Exception as exc:
                    # Not fatal (an index is an optimisation) but not silent: a missing
                    # index is exactly the slow-at-scale failure this exists to prevent.
                    logger.warning("graph.neo4j.schema_stmt_failed", stmt=stmt, error=str(exc))

    def run(self, cypher: str, **params: Any) -> list[dict[str, Any]]:
        """Run a Cypher statement and return records as dicts. [] if not connected."""
        if self._driver is None:
            return []
        with self._driver.session() as session:
            result = session.run(cypher, **params)
            return [dict(record) for record in result]

    def run_write(self, cypher: str, batch: list[dict[str, Any]]) -> None:
        """Run a parametrised write with UNWIND batching for bulk node/edge loads."""
        if self._driver is None or not batch:
            return
        with self._driver.session() as session:
            session.run(cypher, batch=batch)

    def replace_engagement(self, engagement_id: str, nodes: list[dict[str, Any]],
                           edges: list[dict[str, Any]]) -> bool:
        """Replace one engagement's mirror in a single transaction: delete what is
        there, write the new nodes and edges, commit together. A failure part-way
        rolls back, so readers see the previous complete mirror or the new complete
        one, never a half-written graph. Other engagements are untouched. Returns
        False (and logs) when not connected or the transaction failed."""
        if self._driver is None:
            return False
        try:
            with self._driver.session() as session:
                with session.begin_transaction() as tx:
                    tx.run(MIRROR_DELETE, engagement_id=engagement_id)
                    for cypher, rows in ((MIRROR_NODES, nodes), (MIRROR_EDGES, edges)):
                        for i in range(0, len(rows), MIRROR_BATCH_SIZE):
                            tx.run(cypher, batch=rows[i:i + MIRROR_BATCH_SIZE])
                    tx.commit()
            return True
        except Exception as exc:  # noqa: BLE001 — the mirror is advisory
            logger.warning("graph.neo4j.replace_failed", engagement_id=engagement_id, error=str(exc))
            return False

    def close(self) -> None:
        if self._driver is not None:
            try:
                self._driver.close()
            finally:
                self._driver = None
