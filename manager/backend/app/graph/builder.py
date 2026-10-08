"""
GraphBuilder — turns engagement assets/services/findings into an attack graph.

The canonical graph is an in-memory ``networkx.DiGraph`` (so analysis is
deterministic and fully testable without a database). When a connected
``Neo4jClient`` is supplied, the same graph is mirrored into Neo4j via batched
``UNWIND`` writes for large-scale Cypher shortest-path queries.

Node types        : Asset, Service, Finding, Credential, NetworkSegment
Relationship types: HAS_SERVICE, HAS_FINDING, EXPLOITS, CONNECTS_TO,
                    SAME_SEGMENT, CREDENTIAL_REUSE

Node id convention: ``"{type}:{uuid}"`` e.g. ``asset:<uuid>`` — keeps the graph
namespaced so an asset and a finding can never collide.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Iterable

import networkx as nx
import structlog

from app.graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

# Service.exposure value set by exposure fusion when an EXTERNAL-vantage probe saw
# the port open (app/detection/vantage_fusion.py).
SERVICE_EXPOSURE_EXTERNAL = "external"

# Environments that imply an internet-facing asset (attack source).
_EXPOSED_ENVIRONMENTS: frozenset[str] = frozenset(
    {"dmz", "external", "internet", "public", "perimeter", "edge"}
)

# Cypher cost = attack complexity. Lower = easier to exploit.
_AC_COMPLEXITY = {"L": 1.0, "M": 2.0, "H": 3.0}
_SEVERITY_COMPLEXITY = {
    "critical": 1.0, "high": 1.5, "medium": 2.5, "low": 3.0, "info": 4.0,
}


def asset_node_id(asset_id: Any) -> str:
    return f"asset:{asset_id}"


def service_node_id(service_id: Any) -> str:
    return f"service:{service_id}"


def finding_node_id(finding_id: Any) -> str:
    return f"finding:{finding_id}"


def segment_node_id(key: Any) -> str:
    return f"segment:{key}"


def _enum_value(v: Any, default: str = "") -> str:
    """Normalise a value that may be an Enum, str, or None to a lowercase str."""
    if v is None:
        return default
    return str(getattr(v, "value", v)).lower()


def _to_float(v: Any, default: float = 0.0) -> float:
    if v is None:
        return default
    if isinstance(v, Decimal):
        return float(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def exploit_complexity(finding: Any) -> float:
    """
    Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity
    component when present, otherwise estimated from severity. Lower = easier.
    """
    vector = getattr(finding, "cvss_vector", None) or ""
    for token in str(vector).split("/"):
        if token.startswith("AC:"):
            return _AC_COMPLEXITY.get(token[3:].upper(), 2.0)
    sev = _enum_value(getattr(finding, "severity", None), "medium")
    return _SEVERITY_COMPLEXITY.get(sev, 2.5)


def _attack_complexity(finding: Any) -> str | None:
    """CVSS Attack Complexity token (L/M/H) from the vector, or None."""
    for token in str(getattr(finding, "cvss_vector", None) or "").split("/"):
        if token.startswith("AC:"):
            ac = token[3:].upper()
            return ac if ac in _AC_COMPLEXITY else None
    return None


# Finding statuses that still describe a live weakness. Remediated, accepted and
# false-positive findings must never become attack steps (FM-06).
LIVE_FINDING_STATUSES: frozenset[str] = frozenset({"open", "confirmed"})


def is_live_finding(finding: Any) -> bool:
    status = getattr(finding, "status", None)
    if status is None:
        return True          # in-memory / demo findings carry no status
    return _enum_value(status) in LIVE_FINDING_STATUSES


def is_internet_exposed(asset: Any) -> bool:
    tags = getattr(asset, "tags", None) or {}
    if isinstance(tags, dict) and tags.get("internet_exposed"):
        return True
    return _enum_value(getattr(asset, "environment", None)) in _EXPOSED_ENVIRONMENTS


class GraphBuilder:
    def __init__(self, neo4j: Neo4jClient | None = None):
        # MultiDiGraph: a pair of assets can be linked by several relationship
        # types at once (e.g. SAME_SEGMENT *and* CREDENTIAL_REUSE).
        self.graph = nx.MultiDiGraph()
        self._neo4j = neo4j

    # ── build_asset_graph ─────────────────────────────────────────────────────────

    def build_asset_graph(
        self,
        engagement_id: Any,
        assets: Iterable[Any],
        services: Iterable[Any] = (),
        findings: Iterable[Any] = (),
        credentials: Iterable[dict[str, Any]] | None = None,
        network_topology: dict[str, Any] | None = None,
    ) -> nx.MultiDiGraph:
        """
        Build the full multi-type attack graph. Returns the populated DiGraph
        (also stored on ``self.graph``).
        """
        g = self.graph
        g.clear()
        g.graph["engagement_id"] = str(engagement_id)

        assets = list(assets)
        services = list(services)
        findings = [f for f in findings if is_live_finding(f)]

        # ── Asset nodes ──
        for a in assets:
            g.add_node(
                asset_node_id(a.id),
                type="Asset",
                entity_id=str(a.id),
                label=getattr(a, "hostname", None) or getattr(a, "ip_address", None) or str(a.id),
                ip=getattr(a, "ip_address", None),
                criticality=_enum_value(getattr(a, "criticality", None), "medium"),
                internet_exposed=is_internet_exposed(a),
                exposure_basis="asset_tag" if is_internet_exposed(a) else None,
                device_role=getattr(a, "device_role", None),
                role_detail=getattr(a, "role_detail", None),
                compromised=False,
            )

        # ── Service nodes + HAS_SERVICE ──
        for s in services:
            sid = service_node_id(s.id)
            g.add_node(
                sid,
                type="Service",
                entity_id=str(s.id),
                label=f"{getattr(s, 'service_name', None) or 'svc'}:{getattr(s, 'port', '')}",
                port=getattr(s, "port", None),
            )
            aid = asset_node_id(getattr(s, "asset_id", None))
            if g.has_node(aid):
                g.add_edge(aid, sid, type="HAS_SERVICE")
                # P4a: the fleet-fused, multi-probe exposure verdict (vantage_fusion)
                # is the real "reachable from the internet" signal. It was stamped
                # on Service rows but never read here, so no asset was ever an entry
                # point (FM-02). An externally-exposed service makes its host an
                # internet ENTRY candidate — reachable, not yet owned.
                exposure = str(getattr(s, "exposure", None) or "").lower()
                g.nodes[sid]["exposure"] = exposure or None
                if exposure == SERVICE_EXPOSURE_EXTERNAL:
                    node = g.nodes[aid]
                    node["internet_exposed"] = True
                    node["exposure_basis"] = node.get("exposure_basis") or "service_exposure"
                    ports = set(node.get("exposed_ports") or [])
                    port = getattr(s, "port", None)
                    if isinstance(port, int):
                        ports.add(port)
                    node["exposed_ports"] = sorted(ports)

        # ── Finding nodes + HAS_FINDING ──
        for f in findings:
            fid = finding_node_id(f.id)
            cvss = _to_float(getattr(f, "cvss_score", None))
            g.add_node(
                fid,
                type="Finding",
                entity_id=str(f.id),
                label=getattr(f, "title", None) or str(f.id),
                cvss=cvss,
                severity=_enum_value(getattr(f, "severity", None), "info"),
                exploitable=bool(getattr(f, "exploitable", False)),
                exploit_validated=bool(getattr(f, "exploit_validated", False)),
                mitre=list(getattr(f, "mitre_techniques", None) or []),
                # Inputs to the analyzer's step-likelihood model (EPSS is a measured
                # exploitation probability; AC and confidence refine the estimate).
                epss=_to_float(getattr(f, "epss_score", None)),
                attack_complexity=_attack_complexity(f),
                confidence=getattr(f, "verification_confidence", None),
            )
            aid = asset_node_id(getattr(f, "asset_id", None))
            if getattr(f, "asset_id", None) is not None and g.has_node(aid):
                g.add_edge(aid, fid, type="HAS_FINDING")

        # ── derived edges ──
        self.add_exploit_edges(findings)
        if network_topology:
            self.add_network_edges(assets, network_topology)
        if credentials:
            self._add_credential_edges(credentials)

        logger.info(
            "graph.build.done",
            engagement=str(engagement_id),
            nodes=g.number_of_nodes(),
            edges=g.number_of_edges(),
        )
        return g

    # ── add_exploit_edges ─────────────────────────────────────────────────────────

    def add_exploit_edges(self, findings: Iterable[Any]) -> int:
        """
        For each exploitable finding add an EXPLOITS edge Finding→Asset with
        ``weight = exploit_complexity`` (lower = easier). Returns edges added.
        """
        added = 0
        for f in findings:
            if not (getattr(f, "exploitable", False) or getattr(f, "exploit_validated", False)):
                continue
            aid = asset_node_id(getattr(f, "asset_id", None))
            fid = finding_node_id(f.id)
            if not (self.graph.has_node(aid) and self.graph.has_node(fid)):
                continue
            self.graph.add_edge(
                fid, aid,
                type="EXPLOITS",
                weight=exploit_complexity(f),
                cvss=_to_float(getattr(f, "cvss_score", None)),
                validated=bool(getattr(f, "exploit_validated", False)),
            )
            added += 1
        return added

    # ── add_network_edges ─────────────────────────────────────────────────────────

    def add_network_edges(self, assets: Iterable[Any], network_topology: dict[str, Any]) -> int:
        """
        Add CONNECTS_TO (directed reachability) and SAME_SEGMENT edges from
        segmentation data.

        ``network_topology`` =
          {
            "segments":    {"<segment-name>": ["<asset_id>", ...]},
            "connections": [["<src_asset_id>", "<dst_asset_id>"], ...],
          }
        Assets in the same segment are fully reachable from one another.
        """
        added = 0
        segments = network_topology.get("segments", {}) or {}
        for seg_name, member_ids in segments.items():
            seg_node = f"segment:{seg_name}"
            self.graph.add_node(seg_node, type="NetworkSegment", label=seg_name)
            members = [asset_node_id(m) for m in member_ids if self.graph.has_node(asset_node_id(m))]
            for m in members:
                self.graph.add_edge(m, seg_node, type="IN_SEGMENT")
            # SAME_SEGMENT lateral reachability (both directions).
            for i, a in enumerate(members):
                for b in members[i + 1:]:
                    self.graph.add_edge(a, b, type="SAME_SEGMENT", weight=1.0)
                    self.graph.add_edge(b, a, type="SAME_SEGMENT", weight=1.0)
                    added += 2

        for pair in network_topology.get("connections", []) or []:
            if len(pair) != 2:
                continue
            src, dst = asset_node_id(pair[0]), asset_node_id(pair[1])
            if self.graph.has_node(src) and self.graph.has_node(dst):
                self.graph.add_edge(src, dst, type="CONNECTS_TO", weight=1.0)
                added += 1
        return added

    def add_segment_topology(self, topology: dict[str, Any]) -> int:
        """
        Add subnet HUB nodes from reachability.derive_topology (P1a).

          asset  -IN_SEGMENT->   segment        membership (O(n), not O(n²))
          segment -SEGMENT_LINK-> segment       inter-subnet link (basis, confidence)
          asset  -ROUTES->       segment        a gateway routing into another subnet

        Hosts on one subnet reach each other THROUGH the hub; the analyzer turns
        hub hops into movement only toward hosts the attacker can compromise.
        Returns edges added.
        """
        added = 0
        segments = topology.get("segments") or {}
        for key, seg in segments.items():
            node = segment_node_id(key)
            self.graph.add_node(
                node, type="NetworkSegment", entity_id=key, label=seg.get("cidr", key),
                cidr=seg.get("cidr", key), inferred=bool(seg.get("inferred")),
                scoped=bool(seg.get("scoped", True)),
                gateways=list(seg.get("gateways") or []))
            for member in seg.get("members") or []:
                aid = asset_node_id(member)
                if self.graph.has_node(aid):
                    self.graph.add_edge(aid, node, type="IN_SEGMENT")
                    self.graph.nodes[aid]["segment"] = key
                    added += 1
        for link in topology.get("links") or []:
            src, dst = segment_node_id(link["src"]), segment_node_id(link["dst"])
            if self.graph.has_node(src) and self.graph.has_node(dst):
                self.graph.add_edge(src, dst, type="SEGMENT_LINK", basis=link.get("basis"),
                                    reachability_confidence=link.get("confidence", 1.0))
                added += 1
        for route in topology.get("routes") or []:
            gw, dst = asset_node_id(route["gateway"]), segment_node_id(route["segment"])
            if self.graph.has_node(gw) and self.graph.has_node(dst):
                self.graph.add_edge(gw, dst, type="ROUTES", basis=route.get("basis"),
                                    reachability_confidence=route.get("confidence", 1.0))
                added += 1
        self.graph.graph["reachability_posture"] = topology.get("posture")
        self.graph.graph["unplaced_assets"] = list(topology.get("unplaced") or [])
        return added

    def _add_credential_edges(self, credentials: Iterable[dict[str, Any]]) -> int:
        """
        CREDENTIAL_REUSE edges between assets sharing a credential.
        ``credentials`` items: {"id": ..., "label": ..., "reused_on": [asset_ids]}.
        """
        added = 0
        for cred in credentials:
            cid = f"credential:{cred.get('id')}"
            self.graph.add_node(cid, type="Credential", label=cred.get("label", str(cred.get("id"))))
            hosts = [asset_node_id(h) for h in cred.get("reused_on", []) if self.graph.has_node(asset_node_id(h))]
            for h in hosts:
                self.graph.add_edge(h, cid, type="HAS_CREDENTIAL")
            for i, a in enumerate(hosts):
                for b in hosts[i + 1:]:
                    self.graph.add_edge(a, b, type="CREDENTIAL_REUSE", weight=0.5, credential=cid)
                    self.graph.add_edge(b, a, type="CREDENTIAL_REUSE", weight=0.5, credential=cid)
                    added += 2
        return added

    # ── PostgreSQL loader ───────────────────────────────────────────────────────

    async def build_from_db(self, db: Any, engagement_id: Any) -> nx.MultiDiGraph:
        """Load assets/services/findings for an engagement and build the graph."""
        from sqlalchemy import select

        from app.models.asset import Asset
        from app.models.finding import Finding
        from app.models.service import Service

        assets = list((await db.execute(
            select(Asset).where(Asset.engagement_id == engagement_id)
        )).scalars().all())
        asset_ids = [a.id for a in assets]

        services = []
        from app.models.enums import FindingStatus
        findings = list((await db.execute(
            select(Finding).where(
                Finding.engagement_id == engagement_id,
                Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]),
            )
        )).scalars().all())
        if asset_ids:
            services = list((await db.execute(
                select(Service).where(Service.asset_id.in_(asset_ids))
            )).scalars().all())

        graph = self.build_asset_graph(engagement_id, assets, services, findings)

        # P1a: derive the subnet topology from the engagement scope and assets.
        # Before this, no topology was ever supplied, so no lateral movement
        # existed and every multi-host path was impossible (FM-01).
        from app.detection.reachability import derive_topology, posture_from_roe
        from app.models.engagement import Engagement
        engagement = await db.get(Engagement, engagement_id)
        topology = derive_topology(
            assets,
            getattr(engagement, "scope_cidrs", None) or [],
            posture_from_roe(getattr(engagement, "rules_of_engagement", None)),
        )
        self.add_segment_topology(topology)

        if self._neo4j is not None:
            self.sync_to_neo4j(engagement_id)
        return graph

    # ── Neo4j mirror ──────────────────────────────────────────────────────────────

    def sync_to_neo4j(self, engagement_id: Any) -> dict[str, int]:
        """Mirror the current in-memory graph into Neo4j via batched writes."""
        if self._neo4j is None:
            return {"nodes": 0, "edges": 0}
        self._neo4j.ensure_schema()

        nodes = [
            {"key": n, "engagement_id": str(engagement_id), **{k: v for k, v in data.items()}}
            for n, data in self.graph.nodes(data=True)
        ]
        # Single :GraphNode label keyed by `key`, with the real node type kept as
        # a property — avoids assuming the APOC plugin for dynamic labels.
        self._neo4j.run_write(
            "UNWIND $batch AS n MERGE (x:GraphNode {key: n.key}) SET x += n",
            nodes,
        )
        edges = [
            {"src": u, "dst": v, **{k: val for k, val in data.items()}}
            for u, v, data in self.graph.edges(data=True)
        ]
        self._neo4j.run_write(
            "UNWIND $batch AS e "
            "MATCH (a:GraphNode {key: e.src}) MATCH (b:GraphNode {key: e.dst}) "
            "MERGE (a)-[r:REL {type: e.type}]->(b) SET r += e",
            edges,
        )
        logger.info("graph.neo4j.synced", nodes=len(nodes), edges=len(edges))
        return {"nodes": len(nodes), "edges": len(edges)}
