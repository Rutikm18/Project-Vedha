"""
PathAnalyzer — attack-path discovery, scoring, chokepoint and blast-radius
analysis over the GraphBuilder graph.

The analyzer works on an attacker *movement projection* of the full multi-type
graph: a directed edge Asset_A → Asset_B means an attacker who controls A can
reach B AND gain control of it. Three properties make the result trustworthy
(each fixes a failure mode in manager/docs/ATTACK_PATH_PLAN.md §9):

  * MONOTONIC CONTROL (FM-05). An attacker can only act from a host they control.
    A movement edge exists only when it *grants control* of the destination: the
    destination carries an exploitable step, or the hop is credential reuse
    (valid credentials grant access without an exploit). Merely reaching a host
    the attacker cannot compromise is not a foothold, so no path continues from it.
    This is the monotonic-privilege model of MulVAL / Ou et al. (CCS'06).

  * LIKELIHOOD, NOT CVSS SUM (FM-17/18/19). Each step has a success likelihood in
    (0, 1]: exploit evidence (validated > EPSS > attack complexity > severity),
    scaled by the finding's verification confidence and the hop's reachability
    confidence. A path's likelihood is the PRODUCT of its steps, so longer chains
    are less likely, never more. CVSS measures severity, not probability (FIRST);
    it only enters as a fallback estimate when nothing better is known, and a
    misconfiguration with no CVSS still gets a non-zero floor.

  * BOUNDED SEARCH (FM-21/23). Paths are enumerated most-likely-first with Yen's
    k-shortest-paths (``nx.shortest_simple_paths``) over cost = -ln(likelihood),
    and the generator is stopped after k. ``all_simple_paths`` enumerated every
    simple path before truncating, which explodes combinatorially on a flat
    subnet (≈1M paths at 11 hosts).

Equivalent Neo4j Cypher (used only when a Neo4jClient is connected) is
engagement-scoped (FM-27): every query is filtered by ``$engagement_id``.
"""
from __future__ import annotations

import itertools
import math
from typing import Any

import networkx as nx
import structlog

logger = structlog.get_logger()

# ── Cypher query examples (server-side equivalents) ───────────────────────────
# Every query is scoped to ONE engagement. An unscoped MATCH on a shared Neo4j
# would return other tenants' assets (FM-27).

CYPHER_SHORTEST_PATH = """
// Most direct attack path from an internet-exposed asset to a target, one engagement.
MATCH (src:GraphNode {type: 'Asset', internet_exposed: true, engagement_id: $engagement_id})
MATCH (tgt:GraphNode {type: 'Asset', entity_id: $target_id, engagement_id: $engagement_id})
MATCH p = shortestPath((src)-[:REL*..10]->(tgt))
WHERE all(r IN relationships(p) WHERE r.type IN ['CONNECTS_TO', 'SAME_SEGMENT', 'CREDENTIAL_REUSE'])
  AND all(n IN nodes(p) WHERE n.engagement_id = $engagement_id)
RETURN p, reduce(c = 0.0, r IN relationships(p) | c + coalesce(r.weight, 1.0)) AS cost
ORDER BY cost ASC
"""

CYPHER_BLAST_RADIUS = """
// All assets reachable from a compromised asset within 10 hops, one engagement.
MATCH (src:GraphNode {type: 'Asset', entity_id: $asset_id, engagement_id: $engagement_id})
MATCH p = (src)-[:REL*..10]->(reached:GraphNode {type: 'Asset', engagement_id: $engagement_id})
WHERE all(r IN relationships(p) WHERE r.type IN ['CONNECTS_TO', 'SAME_SEGMENT', 'CREDENTIAL_REUSE'])
RETURN DISTINCT reached.entity_id AS asset_id
"""

CYPHER_CHOKEPOINTS = """
// Assets that appear on the most shortest paths to critical targets, one engagement.
MATCH (tgt:GraphNode {type: 'Asset', criticality: 'critical', engagement_id: $engagement_id})
MATCH (src:GraphNode {type: 'Asset', internet_exposed: true, engagement_id: $engagement_id})
MATCH p = shortestPath((src)-[:REL*..10]->(tgt))
WHERE all(r IN relationships(p) WHERE r.type IN ['CONNECTS_TO', 'SAME_SEGMENT', 'CREDENTIAL_REUSE'])
UNWIND nodes(p) AS hop
WITH hop, count(DISTINCT p) AS path_count
WHERE hop.type = 'Asset'
RETURN hop.entity_id AS asset_id, path_count ORDER BY path_count DESC
"""

# Relationship types an attacker can traverse for lateral movement.
_MOVEMENT_RELS = frozenset({"CONNECTS_TO", "SAME_SEGMENT", "CREDENTIAL_REUSE", "SAME_HOST"})

# When several movement relationships link the same asset pair, the most
# reliable one labels the projected edge. SAME_HOST (one machine, two addresses)
# is identity, not a hop; credential reuse is the next most reliable.
_REL_PRIORITY = {"SAME_HOST": 4, "CREDENTIAL_REUSE": 3, "CONNECTS_TO": 2, "SAME_SEGMENT": 1}

# ── step likelihood model ─────────────────────────────────────────────────────
# Exploit evidence, strongest first. Values are deliberately coarse: they ORDER
# steps sensibly; they are not a calibrated probability of compromise.
P_VALIDATED = 0.95            # exploit actually validated in this engagement
P_CREDENTIAL_REUSE = 0.85     # valid credentials grant access without an exploit
_P_ATTACK_COMPLEXITY = {"L": 0.75, "M": 0.5, "H": 0.3}
_P_SEVERITY = {"critical": 0.65, "high": 0.5, "medium": 0.35, "low": 0.2, "info": 0.1}
P_FLOOR = 0.1                 # a known weakness is never "impossible" (FM-19)
P_UNKNOWN_HOP = 0.5           # a hop counted in `hops` but not described by an edge

# A step that lands on an asset not seen within the freshness window (FM-16/32): the
# weakness may have been fixed or the address re-leased, so it is likelier wrong.
P_STALE_FACTOR = 0.5

# Subnet hubs (P1a). Reaching a member through its subnet's hub costs the
# member's exploit likelihood scaled by the same-subnet adjacency confidence.
CONF_SAME_SUBNET = 0.9
_HUB_RELS = frozenset({"IN_SEGMENT", "SEGMENT_LINK", "ROUTES"})

# Business impact of reaching the target, by criticality.
_IMPACT = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4, "info": 0.2}


def step_likelihood(finding: dict[str, Any]) -> float:
    """Success likelihood (0, 1] of exploiting one finding node.

    Evidence order: validated exploit > EPSS (a measured exploitation
    probability) > CVSS attack complexity > severity. CVSS score itself is never
    read as a probability. Scaled by verification confidence when present.
    """
    if finding.get("exploit_validated"):
        p = P_VALIDATED
    else:
        candidates = []
        epss = _safe_float(finding.get("epss"))
        if epss > 0:
            # EPSS is a 30-day in-the-wild probability; a reachable exploitable
            # step is at least as likely as its complexity estimate suggests.
            candidates.append(epss)
        ac = finding.get("attack_complexity")
        if ac in _P_ATTACK_COMPLEXITY:
            candidates.append(_P_ATTACK_COMPLEXITY[ac])
        else:
            candidates.append(_P_SEVERITY.get(str(finding.get("severity") or "medium"), 0.35))
        p = max(candidates)
    conf = finding.get("confidence")
    if conf is not None:
        c = _safe_float(conf)
        if 0 < c <= 100:
            p *= c / 100.0
    return _clamp_p(p)


def _clamp_p(p: float) -> float:
    return max(P_FLOOR, min(1.0, p))


def _cost(p: float) -> float:
    """Edge cost for shortest-path search: most likely path == cheapest path."""
    return -math.log(max(p, 1e-9))


class PathAnalyzer:
    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph
        self._movement: nx.DiGraph | None = None

    # ── attacker movement projection ──────────────────────────────────────────────

    def _exploit_info(self, asset_node: str) -> dict[str, Any]:
        """Most likely exploitable step on an asset: {finding, cvss, likelihood}.
        Empty when the asset has no exploitable finding (it cannot be compromised
        by exploitation)."""
        best: dict[str, Any] | None = None
        for _, fid, edata in self.graph.out_edges(asset_node, data=True):
            if edata.get("type") != "HAS_FINDING":
                continue
            fdata = self.graph.nodes[fid]
            if not (fdata.get("exploitable") or fdata.get("exploit_validated")):
                continue
            p = step_likelihood(fdata)
            cand = {"finding": fdata.get("entity_id"), "cvss": fdata.get("cvss", 0.0),
                    "likelihood": p, "validated": bool(fdata.get("exploit_validated"))}
            if best is None or cand["likelihood"] > best["likelihood"]:
                best = cand
        return best or {}

    def movement_graph(self) -> nx.DiGraph:
        """
        Build (and cache) the Asset→Asset CONTROL projection. An edge u→v exists
        only when moving from u grants control of v (monotonic, FM-05):
          * v carries an exploitable finding  → exploit step, likelihood of it
          * the hop is CREDENTIAL_REUSE       → access with valid credentials
        A hop to a host the attacker cannot compromise is dropped: reaching it is
        not owning it, and no path may continue from it.
        """
        if self._movement is not None:
            return self._movement

        mv = nx.DiGraph()
        for n, data in self.graph.nodes(data=True):
            if data.get("type") == "Asset":
                mv.add_node(n, **data)

        # Collapse parallel movement edges (MultiDiGraph) per asset pair, keeping
        # the highest-priority relationship and the best reachability confidence.
        best: dict[tuple[str, str], dict[str, Any]] = {}
        for u, v, edata in self.graph.edges(data=True):
            rel = edata.get("type")
            if rel not in _MOVEMENT_RELS or not (mv.has_node(u) and mv.has_node(v)) or u == v:
                continue
            reach = _clamp_reach(edata.get("reachability_confidence", 1.0))
            basis = edata.get("basis", "observed")
            cur = best.get((u, v))
            if cur is None or _REL_PRIORITY.get(rel, 0) > _REL_PRIORITY.get(cur["rel"], 0):
                best[(u, v)] = {"rel": rel, "reach": max(reach, cur["reach"]) if cur else reach,
                                "basis": basis if cur is None else _better_basis(basis, cur["basis"])}
            else:
                cur["reach"] = max(cur["reach"], reach)
                cur["basis"] = _better_basis(basis, cur["basis"])

        self._add_hub_edges(mv)

        for (u, v), info in best.items():
            dest_exploit = self._exploit_info(v)
            if info["rel"] == "SAME_HOST":
                # Same machine: owning one address IS owning the other. The only
                # doubt is whether the two addresses really are one machine, which
                # the link's reachability confidence already carries.
                step_p = 1.0
                grants = True
            elif info["rel"] == "CREDENTIAL_REUSE":
                step_p = max(P_CREDENTIAL_REUSE, dest_exploit.get("likelihood", 0.0))
                grants = True
            elif dest_exploit:
                step_p = dest_exploit["likelihood"]
                grants = True
            else:
                grants = False
            if not grants:
                continue                               # reachable, but not owned
            stale = bool(mv.nodes[v].get("stale"))
            p = _clamp_p(step_p * info["reach"] * (P_STALE_FACTOR if stale else 1.0))
            mv.add_edge(
                u, v,
                weight=_cost(p),
                likelihood=round(p, 4),
                rel=info["rel"],
                basis=info["basis"],
                stale=stale,
                dest_compromisable=bool(dest_exploit),
                dest_cvss=dest_exploit.get("cvss", 0.0),
                dest_finding=dest_exploit.get("finding"),
            )
        self._movement = mv
        return mv

    def _add_hub_edges(self, mv: nx.DiGraph) -> None:
        """Project subnet hubs (NetworkSegment nodes) into the movement graph.

          asset  → hub     joining your own subnet costs nothing (p = 1)
          hub    → asset   ONLY when the member can be compromised (monotonic
                           control): p = exploit likelihood × same-subnet confidence
          hub    → hub     inter-subnet link, p = its reachability confidence
          gateway→ hub     a (controlled) gateway routes into another subnet

        Edges stay O(members + links): a /24 of 200 hosts adds ~400 edges here,
        where the old pairwise SAME_SEGMENT mesh needed 39,800."""
        g = self.graph
        hubs = [n for n, d in g.nodes(data=True) if d.get("type") == "NetworkSegment"]
        for h in hubs:
            mv.add_node(h, **g.nodes[h])
        for u, v, d in g.edges(data=True):
            rel = d.get("type")
            if rel not in _HUB_RELS or not (mv.has_node(u) and mv.has_node(v)):
                continue
            if rel == "IN_SEGMENT" and _is_asset(mv, u):
                _hub_edge(mv, u, v, 1.0, "IN_SEGMENT", "same_subnet")
                exploit = self._exploit_info(u)
                if exploit:      # member is compromisable → reachable FROM its hub
                    stale = bool(mv.nodes[u].get("stale"))
                    p = _clamp_p(exploit["likelihood"] * CONF_SAME_SUBNET * (P_STALE_FACTOR if stale else 1.0))
                    _hub_edge(mv, v, u, p, "SEGMENT_MEMBER", "same_subnet", stale=stale,
                              dest_compromisable=True, dest_cvss=exploit.get("cvss", 0.0),
                              dest_finding=exploit.get("finding"))
            elif rel == "SEGMENT_LINK":
                _hub_edge(mv, u, v, _clamp_reach(d.get("reachability_confidence", 1.0)),
                          "SEGMENT_LINK", d.get("basis") or "assumed")
            elif rel == "ROUTES" and _is_asset(mv, u):
                _hub_edge(mv, u, v, _clamp_reach(d.get("reachability_confidence", 1.0)),
                          "ROUTES", d.get("basis") or "assumed")

    def _source_assets(self, source_type: str) -> list[str]:
        mv = self.movement_graph()
        assets = [(n, d) for n, d in mv.nodes(data=True) if d.get("type") == "Asset"]
        if source_type == "internet_exposed":
            # Exposure is reachability, not compromise (P4a). An internet-exposed
            # host is an entry point only if the attacker can actually gain control
            # of it — the same monotonic-control rule every other hop obeys (FM-05).
            # Otherwise every exposed host would start a path as if already owned.
            return [n for n, d in assets if d.get("internet_exposed") and self._exploit_info(n)]
        if source_type == "any":
            return [n for n, _ in assets]
        # treat source_type as an explicit asset entity_id
        return [n for n, d in assets if d.get("entity_id") == source_type]

    # ── find_paths_to_target ──────────────────────────────────────────────────────

    def find_paths_to_target(
        self,
        target_asset_id: Any,
        source_type: str = "internet_exposed",
        max_hops: int = 10,
        max_paths_per_source: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Return scored attack paths from every source asset to the target, most
        likely first. Each path: {source, target, hops, nodes, edges, likelihood,
        risk_score}. Enumeration is Yen's k-shortest over -ln(likelihood) and stops
        after ``max_paths_per_source`` per source — it never enumerates every path.
        """
        mv = self.movement_graph()
        target_node = f"asset:{target_asset_id}"
        if not mv.has_node(target_node):
            return []

        # Bound how many candidates Yen may yield while skipping over-long paths, so
        # a dense graph cannot turn the skip loop into an unbounded scan.
        scan_cap = max(max_paths_per_source * 20, 50)
        paths: list[dict[str, Any]] = []
        for src in self._source_assets(source_type):
            if src == target_node:
                continue
            try:
                gen = nx.shortest_simple_paths(mv, src, target_node, weight="weight")
                kept = 0
                seen_seq: set[tuple] = set()
                for node_path in itertools.islice(gen, scan_cap):
                    asset_seq = tuple(n for n in node_path if _is_asset(mv, n))
                    if len(asset_seq) - 1 > max_hops or asset_seq in seen_seq:
                        continue      # too long, or same hosts via another subnet route
                    seen_seq.add(asset_seq)
                    paths.append(self._materialise_path(mv, node_path))
                    kept += 1
                    if kept >= max_paths_per_source:
                        break
            except (nx.NodeNotFound, nx.NetworkXNoPath):
                continue

        paths.sort(key=lambda p: (-p["risk_score"], p["hops"], p["nodes"]))
        logger.info("graph.paths.found", target=str(target_asset_id), count=len(paths))
        return paths

    def _materialise_path(self, mv: nx.DiGraph, node_path: list[str]) -> dict[str, Any]:
        """Turn a raw node path (assets AND subnet hubs) into an asset-level path.
        Each hop between two hosts records the subnets it crossed (`via`), its
        combined likelihood, and its WEAKEST reachability basis — so a hop that
        relied on an assumed inter-subnet link is labelled `assumed`."""
        asset_idx = [i for i, n in enumerate(node_path) if _is_asset(mv, n)]
        edges = []
        for i, j in zip(asset_idx, asset_idx[1:]):
            seg = node_path[i:j + 1]
            parts = [mv.edges[a, b] for a, b in zip(seg, seg[1:])]
            via = [mv.nodes[n].get("entity_id") for n in seg[1:-1]]
            p = 1.0
            for ed in parts:
                p *= ed.get("likelihood", 1.0)
            last = parts[-1]
            first_rel = parts[0].get("rel")
            if first_rel == "SAME_HOST" and not via:
                technique = "SAME_HOST"
            elif not via:
                technique = first_rel
            elif first_rel == "ROUTES":
                technique = "GATEWAY_ROUTE"
            else:
                technique = "SAME_SUBNET" if len(via) == 1 else "CROSS_SUBNET"
            basis = min((ed.get("basis", "observed") for ed in parts),
                        key=lambda b: _BASIS_RANK.get(b, 0))
            edges.append({
                "source": mv.nodes[node_path[i]].get("entity_id"),
                "target": mv.nodes[node_path[j]].get("entity_id"),
                "technique": technique,
                "via": via,
                "weight": round(sum(ed.get("weight", 0.0) for ed in parts), 4),
                "likelihood": round(_clamp_p(p), 4),
                "basis": basis,
                "stale": bool(last.get("stale")),
                "exploited": last.get("dest_compromisable", False),
                "finding": last.get("dest_finding"),
                "cvss": last.get("dest_cvss", 0.0),
            })
        tgt = mv.nodes[node_path[-1]]
        path = {
            "source": mv.nodes[node_path[0]].get("entity_id"),
            "target": tgt.get("entity_id"),
            "hops": len(asset_idx) - 1,
            "nodes": [mv.nodes[node_path[i]].get("entity_id") for i in asset_idx],
            "segments": sorted({v for e in edges for v in e["via"]}),
            "edges": edges,
            "target_criticality": tgt.get("criticality", "medium"),
        }
        stale_steps = sum(1 for e in edges if e["stale"])
        path["stale_steps"] = stale_steps
        path["freshness"] = ("stale" if stale_steps == len(edges) and edges
                             else "partly_stale" if stale_steps else "fresh")
        path["likelihood"] = self.path_likelihood(path)
        path["risk_score"] = self.score_path(path)
        return path

    # ── likelihood + score ────────────────────────────────────────────────────────

    def path_likelihood(self, path: dict[str, Any]) -> float:
        """Product of per-step likelihoods (steps are a chain: all must succeed).

        An edge without an explicit `likelihood` (a legacy/hand-built path dict) is
        estimated from its CVSS as a weak fallback, and credential reuse from its
        technique. Hops counted in `hops` but absent from `edges` each contribute
        P_UNKNOWN_HOP, so a longer path can never be more likely than a shorter one.
        """
        edges = path.get("edges", []) or []
        p = 1.0
        for e in edges:
            step = e.get("likelihood")
            if step is None:
                if e.get("technique") == "CREDENTIAL_REUSE":
                    step = P_CREDENTIAL_REUSE
                else:
                    cvss = _safe_float(e.get("cvss"))
                    step = 0.3 + 0.06 * cvss if cvss > 0 else P_FLOOR * 3
            p *= _clamp_p(_safe_float(step))
        extra = max(0, int(path.get("hops", len(edges)) or 0) - len(edges))
        p *= P_UNKNOWN_HOP ** extra
        return round(p, 6)

    def score_path(self, path: dict[str, Any]) -> float:
        """
        Risk score 0–100 = path likelihood × business impact of the target.

        Replaces the old additive score (2×CVSS per hop − 1.5 per hop), under which a
        4-hop CVSS-7 chain scored 50 and a 1-hop CVSS-9.8 scored 18.1 (FM-17), and a
        misconfiguration-only path scored 0 (FM-19).
        """
        likelihood = path.get("likelihood")
        if likelihood is None:
            likelihood = self.path_likelihood(path)
        impact = _IMPACT.get(str(path.get("target_criticality") or "critical"), 0.6)
        return round(max(0.0, min(100.0, 100.0 * likelihood * impact)), 2)

    # ── identify_chokepoints ──────────────────────────────────────────────────────

    def identify_chokepoints(
        self, paths: list[dict[str, Any]], threshold: float = 0.5
    ) -> list[dict[str, Any]]:
        """
        Assets that appear in more than ``threshold`` (default 50%) of all paths —
        cutting these breaks the most attack routes. Excludes each path's own
        source and target endpoints so genuine intermediary chokepoints surface.
        """
        if not paths:
            return []
        total = len(paths)
        counts: dict[str, int] = {}
        for p in paths:
            interior = p["nodes"][1:-1] if len(p["nodes"]) > 2 else []
            for asset_id in set(interior):
                counts[asset_id] = counts.get(asset_id, 0) + 1

        chokepoints = [
            {
                "asset_id": aid,
                "path_count": cnt,
                "path_fraction": round(cnt / total, 3),
                "remediation_priority": _priority(cnt / total),
            }
            for aid, cnt in counts.items()
            if cnt / total > threshold
        ]
        chokepoints.sort(key=lambda c: (-c["path_count"], str(c["asset_id"])))
        return chokepoints

    # ── find_blast_radius ──────────────────────────────────────────────────────────

    def find_blast_radius(self, compromised_asset_id: Any, max_hops: int = 10) -> dict[str, Any]:
        """
        Assets the attacker can gain CONTROL of if ``compromised_asset_id`` is owned
        (control projection, so hosts merely reachable but not compromisable are
        not counted). Returns {origin, reachable, count, by_distance}.
        """
        mv = self.movement_graph()
        origin = f"asset:{compromised_asset_id}"
        if not mv.has_node(origin):
            return {"origin": str(compromised_asset_id), "reachable": [], "count": 0, "by_distance": {}}

        # Distance in HOSTS: entering an asset costs 1, entering a subnet hub 0.
        lengths = nx.single_source_dijkstra_path_length(
            mv, origin, cutoff=max_hops,
            weight=lambda _u, v, _d: 1 if _is_asset(mv, v) else 0)
        by_distance: dict[int, list[str]] = {}
        reachable: list[str] = []
        for node, dist in sorted(lengths.items(), key=lambda kv: (kv[1], kv[0])):
            if node == origin or not _is_asset(mv, node):
                continue
            dist = int(dist)
            entity = mv.nodes[node].get("entity_id")
            reachable.append(entity)
            by_distance.setdefault(dist, []).append(entity)

        return {
            "origin": str(compromised_asset_id),
            "reachable": reachable,
            "count": len(reachable),
            "by_distance": {str(k): v for k, v in sorted(by_distance.items())},
        }

    # ── explain an empty / thin result (FM-30) ────────────────────────────────────

    def diagnose(self, target_asset_ids: list[str] | None = None,
                 source_type: str = "internet_exposed") -> dict[str, Any]:
        """Why are there (no) attack paths? Counts every precondition a path needs
        and names each one that is missing, so an empty result can never be read as
        'the network is safe' when it really means 'the model had nothing to work
        with'. Mirrors the posture engine's evaluated-vs-blind distinction."""
        g = self.graph
        mv = self.movement_graph()
        assets = sum(1 for _, d in g.nodes(data=True) if d.get("type") == "Asset")
        findings = [d for _, d in g.nodes(data=True) if d.get("type") == "Finding"]
        exploitable = sum(1 for d in findings if d.get("exploitable") or d.get("exploit_validated"))
        movement_rels = sum(1 for _, _, d in g.edges(data=True)
                            if d.get("type") in _MOVEMENT_RELS | _HUB_RELS)
        sources = len(self._source_assets(source_type))
        exposed = sum(1 for _, d in g.nodes(data=True)
                      if d.get("type") == "Asset" and d.get("internet_exposed"))
        targets = [t for t in (target_asset_ids or []) if mv.has_node(f"asset:{t}")]

        reasons: list[dict[str, str]] = []
        if assets == 0:
            reasons.append({"code": "no_assets", "detail": "the engagement has no assets yet"})
        if sources == 0:
            if source_type == "internet_exposed" and exposed:
                reasons.append({"code": "entry_points_not_compromisable",
                                "detail": f"{exposed} asset(s) are internet-exposed, but none "
                                          "carries an exploitable finding, so none is a foothold"})
            else:
                reasons.append({"code": "no_entry_points",
                                "detail": "no asset is internet-exposed (no service seen open "
                                          "from an external vantage), so no path has a starting point"})
        if not targets:
            reasons.append({"code": "no_targets",
                            "detail": "no crown-jewel target: none is marked critical and none "
                                      "was auto-selected (domain controller, hypervisor, data store)"})
        if movement_rels == 0:
            reasons.append({"code": "no_reachability",
                            "detail": "no network reachability or credential edges between assets"})
        if exploitable == 0:
            reasons.append({"code": "no_exploitable_steps",
                            "detail": "no finding is marked exploitable, so no host can be compromised"})
        control_edges = sum(1 for _, v in mv.edges() if _is_asset(mv, v))
        if exploitable and control_edges == 0 and movement_rels:
            reasons.append({"code": "no_control_edges",
                            "detail": "hosts are reachable but none reachable host can be compromised"})
        return {
            "assets": assets,
            "findings": len(findings),
            "exploitable_findings": exploitable,
            "entry_points": sources,
            "internet_exposed_assets": exposed,
            "targets": len(targets),
            "reachability_edges": movement_rels,
            "control_edges": control_edges,
            "segments": sum(1 for _, d in g.nodes(data=True) if d.get("type") == "NetworkSegment"),
            "reachability_posture": g.graph.get("reachability_posture"),
            "unplaced_assets": len(g.graph.get("unplaced_assets") or []),
            "reasons": reasons,
        }


_BASIS_RANK = {"observed": 4, "same_subnet": 3, "same_host_fqdn": 3, "same_host_name": 2,
               "assumed": 2, "assumed_cross_site": 1, "possible": 1}


def _is_asset(mv: nx.DiGraph, n: str) -> bool:
    return mv.nodes[n].get("type") == "Asset"


def _hub_edge(mv: nx.DiGraph, u: str, v: str, p: float, rel: str, basis: str, **extra: Any) -> None:
    p = 1.0 if p >= 1.0 else _clamp_p(p)
    mv.add_edge(u, v, weight=_cost(p), likelihood=round(p, 4), rel=rel, basis=basis, **extra)


def _better_basis(a: str, b: str) -> str:
    return a if _BASIS_RANK.get(a, 0) >= _BASIS_RANK.get(b, 0) else b


def _clamp_reach(v: Any) -> float:
    f = _safe_float(v)
    return 1.0 if f <= 0 else min(1.0, f)


def _safe_float(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _priority(fraction: float) -> str:
    if fraction >= 0.8:
        return "critical"
    if fraction >= 0.65:
        return "high"
    return "medium"
