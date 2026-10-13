"""
coverage.py — how much of the network the attack paths are actually built on
(P5 of manager/docs/ATTACK_PATH_PLAN.md: FM-13 coverage gaps, FM-32 staleness).

A path can only run through hosts that were found. A host the scan missed has no
node, so "no path through that subnet" may simply mean "nobody looked there". These
reports make that visible next to the paths, from what the graph itself knows —
they never claim a subnet was FULLY scanned, because no scanned-address accounting
reaches the graph; "observed" is the strongest word used.

Pure: takes the graph the builder produced, returns plain dicts.
"""
from __future__ import annotations

import ipaddress
from typing import Any

import networkx as nx


def _networks(cidrs) -> list[ipaddress._BaseNetwork]:
    out = []
    for c in cidrs or []:
        try:
            out.append(ipaddress.ip_network(str(c).strip(), strict=False))
        except ValueError:
            continue
    return out


def coverage_report(graph: nx.MultiDiGraph) -> dict[str, Any]:
    """Per-subnet host counts and recency, and scope that has no observed host."""
    members: dict[str, list[dict[str, Any]]] = {}
    for u, v, d in graph.edges(data=True):
        if d.get("type") == "IN_SEGMENT" and graph.nodes[u].get("type") == "Asset":
            members.setdefault(v, []).append(graph.nodes[u])

    segments: list[dict[str, Any]] = []
    for node, data in sorted(graph.nodes(data=True), key=lambda kv: str(kv[0])):
        if data.get("type") != "NetworkSegment":
            continue
        hosts = members.get(node, [])
        seen = sorted(h["last_seen"] for h in hosts if h.get("last_seen"))
        segments.append({
            "segment": data.get("entity_id"), "cidr": data.get("cidr"), "site": data.get("site"),
            "hosts": len(hosts), "stale_hosts": sum(1 for h in hosts if h.get("stale")),
            "last_seen": seen[-1] if seen else None,
            "inferred": bool(data.get("inferred")), "in_scope": bool(data.get("scoped", True)),
        })

    seg_nets = []
    for s in segments:
        parsed = _networks([s["cidr"]])
        if parsed:
            seg_nets.append(parsed[0])
    gaps = []
    for scope in _networks(graph.graph.get("scope_cidrs")):
        if not any(scope.version == s.version and scope.overlaps(s) for s in seg_nets):
            gaps.append({"cidr": str(scope), "addresses": scope.num_addresses})

    outside = [s["cidr"] for s in segments if not s["in_scope"]]
    placed = sum(s["hosts"] for s in segments)
    unplaced = len(graph.graph.get("unplaced_assets") or [])
    partial = bool(gaps or outside or unplaced)
    return {
        "basis": "hosts observed per subnet; the scanned address space itself is not tracked",
        "confidence": "partial" if partial else "observed",
        "segments": segments,
        "scope_without_observed_hosts": gaps,
        "observed_outside_scope": outside,
        "assets_placed": placed,
        "assets_without_a_subnet": unplaced,
        "inferred_subnets": sum(1 for s in segments if s["inferred"]),
    }


def freshness_report(graph: nx.MultiDiGraph) -> dict[str, Any]:
    """How old the evidence under the paths is (assets are flagged stale by the builder)."""
    assets = [d for _, d in graph.nodes(data=True) if d.get("type") == "Asset"]
    seen = sorted(a["last_seen"] for a in assets if a.get("last_seen"))
    stale = sum(1 for a in assets if a.get("stale"))
    return {
        "window_days": graph.graph.get("freshness_days"),
        "assets": len(assets),
        "stale_assets": stale,
        "stale_fraction": round(stale / len(assets), 3) if assets else 0.0,
        "assets_without_timestamp": sum(1 for a in assets if not a.get("last_seen")),
        "oldest_seen": seen[0] if seen else None,
        "newest_seen": seen[-1] if seen else None,
    }
