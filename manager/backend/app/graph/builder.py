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

import json
from datetime import datetime
from decimal import Decimal
from typing import Any, Iterable

import networkx as nx
import structlog

from app.detection.asset_identity import DEFAULT_FRESHNESS_DAYS, is_stale
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


def _iso(value: Any) -> str | None:
    return value.isoformat() if isinstance(value, datetime) else None


def _neo4j_scalar(v: Any) -> Any:
    if isinstance(v, bool) or v is None or isinstance(v, (int, float, str)):
        return v
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.isoformat()
    return str(getattr(v, "value", v))


def _neo4j_props(data: dict[str, Any]) -> dict[str, Any]:
    """Node/edge attributes as Neo4j property values. Neo4j stores only primitives
    and homogeneous lists of primitives; a nested dict or a mixed list would make
    the whole write fail, so those become JSON text and null attributes are dropped
    (an absent property already reads as null)."""
    out: dict[str, Any] = {}
    for k, v in data.items():
        if v is None:
            continue
        if isinstance(v, dict):
            out[str(k)] = json.dumps(v, sort_keys=True, default=str)
        elif isinstance(v, (list, tuple, set, frozenset)):
            items = [_neo4j_scalar(i) for i in (sorted(v, key=str) if isinstance(v, (set, frozenset)) else v)
                     if i is not None]
            if any(isinstance(i, (dict, list, tuple, set)) for i in v):
                out[str(k)] = json.dumps(list(v), default=str)
            elif len({type(i) for i in items}) <= 1:
                out[str(k)] = items
            else:
                out[str(k)] = json.dumps(items, default=str)
        else:
            out[str(k)] = _neo4j_scalar(v)
    return out


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


def freshness_days_from_roe(rules_of_engagement: dict | None) -> int | None:
    """Engagement freshness window in days (rules_of_engagement.attack_path_freshness_days);
    default 30, 0 disables staleness handling."""
    val = (rules_of_engagement or {}).get("attack_path_freshness_days")
    if isinstance(val, bool) or not isinstance(val, int) or val < 0:
        return DEFAULT_FRESHNESS_DAYS
    return val or None


def _finding_evidence(finding: Any) -> dict[str, Any]:
    ev = getattr(finding, "evidence", None)
    return ev if isinstance(ev, dict) else {}


def _finding_capability(finding: Any) -> tuple[str | None, str | None]:
    """(capability, source) this finding is classified as (P2), from its rule_id /
    category / ATT&CK technique. Only a curated-rule source may grant control."""
    from app.detection.capability_map import classify

    ev = _finding_evidence(finding)
    return classify(
        ev.get("rule_id"),
        ev.get("category"),
        getattr(finding, "mitre_techniques", None) or ev.get("mitre"),
        ev,
    )


def _finding_state(finding: Any) -> str | None:
    """The finding's own state for step likelihood: the posture state when present
    (confirmed/suspected/potential), else the verification verdict."""
    ev = _finding_evidence(finding)
    return ev.get("state") or getattr(finding, "verification_state", None)


def _finding_confidence(finding: Any) -> Any:
    """Verification confidence, or the posture rule's own confidence when the
    finding was never verification-stamped (posture findings carry 0–100)."""
    vc = getattr(finding, "verification_confidence", None)
    if vc is not None:
        return vc
    return _finding_evidence(finding).get("confidence")


def _finding_kev(finding: Any) -> bool:
    """True when the finding is linked to a CISA KEV-listed CVE (exploitability.py
    records this on posture evidence; the CVE track sets evidence.kev)."""
    ev = _finding_evidence(finding)
    if ev.get("kev"):
        return True
    return any(r.get("kev_listed") for r in (ev.get("kev_refs") or []) if isinstance(r, dict))


def _finding_exploitability(finding: Any) -> str | None:
    """The exploitability tier exploitability.py stamped on a posture finding
    (actively_exploited / likely / elevated / unknown), when present."""
    return _finding_evidence(finding).get("exploitability")


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
        freshness_days: int | None = DEFAULT_FRESHNESS_DAYS,
        now: datetime | None = None,
    ) -> nx.MultiDiGraph:
        """
        Build the full multi-type attack graph. Returns the populated DiGraph
        (also stored on ``self.graph``). Assets last seen more than
        ``freshness_days`` ago are flagged ``stale`` (FM-16/32); the analyzer
        down-weights and labels steps that land on them.
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
                site=str(a.site_id) if getattr(a, "site_id", None) is not None else None,
                last_seen=_iso(getattr(a, "last_seen", None)),
                stale=is_stale(getattr(a, "last_seen", None), now, freshness_days),
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
            cap, cap_source = _finding_capability(f)
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
                confidence=_finding_confidence(f),
                # P2: what the weakness lets an attacker DO, independent of the
                # `exploitable` flag (which only the AD modules ever set). The
                # analyzer turns a control-granting capability into a compromise
                # step just as it does for an exploitable finding (FM-03/12/19).
                capability=cap,
                capability_source=cap_source,
                state=_finding_state(f),
                kev=_finding_kev(f),
                exploitability=_finding_exploitability(f),
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
                scoped=bool(seg.get("scoped", True)), site=seg.get("site"),
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

    def add_machine_links(self, groups: Iterable[dict[str, Any]]) -> int:
        """SAME_HOST edges between the assets of one multi-homed machine
        (asset_identity.link_machines). Owning one address is owning the machine,
        so each edge grants control of its far side; the link's own confidence
        (a name match is evidence, not proof) rides on the edge. Returns edges
        added (two per pair, one each way)."""
        added = 0
        for group in groups:
            members = [asset_node_id(m) for m in group.get("members") or []
                       if self.graph.has_node(asset_node_id(m))]
            for i, a in enumerate(members):
                for b in members[i + 1:]:
                    for u, v in ((a, b), (b, a)):
                        self.graph.add_edge(
                            u, v, type="SAME_HOST", basis=group.get("basis"),
                            reachability_confidence=group.get("confidence", 0.7),
                            machine=group.get("name"))
                        added += 1
        return added

    def _add_credential_edges(self, credentials: Iterable[dict[str, Any]]) -> int:
        """
        CREDENTIAL_REUSE edges between assets sharing a credential.
        ``credentials`` items: {"id", "label", "reused_on": [asset_ids], "basis"?}.
        ``basis`` (P3, e.g. "possible" for a shared default credential) rides on the
        edge so the analyzer and the UI can say how sure the reuse is.
        """
        added = 0
        for cred in credentials:
            cid = f"credential:{cred.get('id')}"
            basis = cred.get("basis", "observed")
            self.graph.add_node(cid, type="Credential", label=cred.get("label", str(cred.get("id"))),
                                basis=basis)
            hosts = [asset_node_id(h) for h in cred.get("reused_on", []) if self.graph.has_node(asset_node_id(h))]
            for h in hosts:
                self.graph.add_edge(h, cid, type="HAS_CREDENTIAL")
            for i, a in enumerate(hosts):
                for b in hosts[i + 1:]:
                    self.graph.add_edge(a, b, type="CREDENTIAL_REUSE", weight=0.5, credential=cid, basis=basis)
                    self.graph.add_edge(b, a, type="CREDENTIAL_REUSE", weight=0.5, credential=cid, basis=basis)
                    added += 2
        return added

    def add_relay_edges(self, relay_edges: Iterable[dict[str, Any]]) -> int:
        """NTLM-relay movement edges src→dst from credentials.derive_credential_edges
        (P3). A relay grants CONTROL of the target (an attacker on the source relays
        coerced authentication to it), so it is a one-directional movement edge the
        analyzer treats like credential reuse. ``basis``/``confidence`` carry the
        preconditions it rests on. Returns edges added."""
        added = 0
        for e in relay_edges:
            src, dst = asset_node_id(e.get("src")), asset_node_id(e.get("dst"))
            if not (self.graph.has_node(src) and self.graph.has_node(dst)) or src == dst:
                continue
            self.graph.add_edge(
                src, dst, type="RELAY", basis=e.get("basis", "assumed"),
                reachability_confidence=e.get("confidence", 0.4),
                technique=e.get("technique"), preconditions=e.get("preconditions"))
            added += 1
        return added

    # ── assembly: the engagement graph from plain objects (no DB) ───────────────

    def assemble(
        self,
        engagement_id: Any,
        assets: Iterable[Any],
        services: Iterable[Any] = (),
        findings: Iterable[Any] = (),
        *,
        scope_cidrs: Iterable[str] = (),
        rules_of_engagement: dict | None = None,
        now: datetime | None = None,
    ) -> nx.MultiDiGraph:
        """Everything build_from_db does after loading rows, from plain objects: assets,
        services and findings, then subnet topology (per-site aware), same-machine
        links and the freshness window. The validation harness (app/graph/validation.py)
        calls this too, so it measures the code that really runs."""
        from app.detection.asset_identity import link_machines, mode_from_roe
        from app.detection.reachability import derive_topology, posture_from_roe

        assets = list(assets)
        scope = list(scope_cidrs or [])
        identity_mode = mode_from_roe(rules_of_engagement)
        freshness_days = freshness_days_from_roe(rules_of_engagement)

        graph = self.build_asset_graph(engagement_id, assets, services, findings,
                                       freshness_days=freshness_days, now=now)
        graph.graph["freshness_days"] = freshness_days
        graph.graph["scope_cidrs"] = scope

        # P1a: derive the subnet topology from the engagement scope and assets.
        # Before this, no topology was ever supplied, so no lateral movement
        # existed and every multi-host path was impossible (FM-01). P1b-4: under
        # per-site identity a private subnet belongs to its site.
        self.add_segment_topology(derive_topology(
            assets, scope, posture_from_roe(rules_of_engagement), identity_mode=identity_mode))
        # P1b-4: one machine seen at several addresses (the dual-homed pivot).
        self.add_machine_links(link_machines(assets, identity_mode, now=now, freshness_days=freshness_days))

        # P3: credential-reuse and NTLM-relay edges, derived from facts with their
        # preconditions checked and labelled. Before this, GraphBuilder was never
        # given a `credentials` structure, so no reuse/relay movement existed (FM-08/09).
        from app.detection.credentials import derive_credential_edges

        cred = derive_credential_edges(assets, [f for f in findings if is_live_finding(f)], services)
        self.add_relay_edges(cred["relay_edges"])
        # H2: shared default credentials are INFORMATION for the report, not graph edges.
        # A read-only community grants no control, a vendor default is already each host's
        # own foothold finding, and the default is public (nothing is captured on one host to
        # reuse on another) — emitting CREDENTIAL_REUSE edges was the FM-08 fallacy and
        # exploded the graph O(k²) on an estate of identical devices.
        graph.graph["shared_default_credentials"] = cred["shared_default_credentials"]
        return graph

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

        from app.models.engagement import Engagement
        engagement = await db.get(Engagement, engagement_id)
        graph = self.assemble(
            engagement_id, assets, services, findings,
            scope_cidrs=getattr(engagement, "scope_cidrs", None) or [],
            rules_of_engagement=getattr(engagement, "rules_of_engagement", None),
        )

        if self._neo4j is not None:
            self.sync_to_neo4j(engagement_id)
        return graph

    # ── Neo4j mirror ──────────────────────────────────────────────────────────────

    def sync_to_neo4j(self, engagement_id: Any) -> dict[str, int]:
        """Replace this engagement's mirror in Neo4j with the current in-memory graph.

        Per-engagement and atomic (see Neo4jClient.replace_engagement): nodes and
        edges for the engagement are deleted and rewritten in one transaction, so a
        fixed weakness leaves the mirror, other tenants are untouched, and parallel
        relationships stay distinct. Best-effort — a Neo4j outage must never stop
        the in-memory analysis; on failure the result carries `error`."""
        if self._neo4j is None:
            return {"nodes": 0, "edges": 0}
        eid = str(engagement_id)
        self._neo4j.ensure_schema()
        nodes = [
            {**_neo4j_props(data), "key": str(n), "engagement_id": eid}
            for n, data in self.graph.nodes(data=True)
        ]
        # `ekey` is the multigraph key: two edges of one type between the same hosts
        # (two credentials, two weaknesses) are two relationships, not one.
        edges = [
            {**_neo4j_props(data), "src": str(u), "dst": str(v), "ekey": str(k), "engagement_id": eid}
            for u, v, k, data in self.graph.edges(keys=True, data=True)
        ]
        if not self._neo4j.replace_engagement(eid, nodes, edges):
            return {"nodes": 0, "edges": 0, "error": "neo4j mirror not updated"}
        logger.info("graph.neo4j.synced", nodes=len(nodes), edges=len(edges))
        return {"nodes": len(nodes), "edges": len(edges)}
