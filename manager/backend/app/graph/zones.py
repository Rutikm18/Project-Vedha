"""
zones.py — the stored routes of one engagement, aggregated into the subnets they cross.

A route drawn host by host is a hairball past a dozen hosts. The attack-graph literature's answer is
to group hosts into protection domains and show the domains; a subnet is the domain this model
already has (the hub nodes). So this reads the routes that are STORED and the subnets the analysis
recorded, and says: which subnets the routes start in, which they end in, which hold a host worth
fixing, and which subnet-to-subnet steps they take, on what basis.

Pure: no database, no computing. It never places a host in a subnet by itself (that would be a
second copy of the graph builder's rule); it reads where the model placed each host from the `via`
list every stored hop carries. What that cannot place is left out and counted, not guessed.

Honesty rules:
  * a link is "at least one stored route took this step", and `routes` counts STORED routes, a
    capped list (at most 5 per entry point per crown jewel): it says how many listed routes use the
    step, not how exposed the step is;
  * a link carries its WEAKEST basis, so one assumed hop makes the link assumed;
  * only subnets that a stored route touches are drawn; the others are counted (`other_zones`);
  * hosts the model could not place in any subnet are counted (`unplaced_assets`), not drawn; a
    route whose entry or crown jewel is unplaced says so (`entry_unplaced`, `jewel_unplaced`)
    instead of being given a subnet.
"""
from __future__ import annotations

from typing import Any

from app.graph.overview import fix_point_ids

# The weakest basis wins when several hops make one link (same ranking the analyzer uses).
BASIS_RANK = {"observed": 4, "same_subnet": 3, "same_host_fqdn": 3, "same_host_name": 2,
              "assumed": 2, "assumed_cross_site": 1, "possible": 1}

# Bases the page words as "assumed or unconfirmed" (see `basisInfo` in lib/attack-paths.ts).
WEAK_BASES = frozenset({"assumed", "assumed_cross_site", "possible", "same_host_name"})

MAX_ZONES = 12


def node_zones(node_count: int, edges: list[dict[str, Any]]) -> list[str | None]:
    """The subnet of each host on one route, as the model placed it, or None when the route does not say.

    A hop's `via` lists the subnets it crossed: two or more = source subnet first, destination last;
    one = the source and destination share it (same subnet) or, for a hop through a gateway, it is the
    destination's subnet and the gateway's own is unknown; none = the hop says nothing about subnets
    (a machine seen on two addresses, or a direct link). A machine with a second address is NOT assumed
    to sit in the same subnet as the first: being in two is the point of it, so it stays unplaced."""
    zones: list[str | None] = [None] * node_count
    for i, e in enumerate(edges):
        if i + 1 >= node_count:
            break
        via = [str(v) for v in (e.get("via") or [])]
        if len(via) >= 2:
            src, dst = via[0], via[-1]
        elif len(via) == 1:
            src, dst = (None, via[0]) if e.get("technique") == "GATEWAY_ROUTE" else (via[0], via[0])
        else:
            src = dst = None
        if zones[i] is None:
            zones[i] = src
        if zones[i + 1] is None:
            zones[i + 1] = dst
    return zones


def _weakest(bases: list[str | None]) -> str:
    return min((b or "observed" for b in bases), key=lambda b: BASIS_RANK.get(b, 0))


def route_links(zones: list[str | None], edges: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    """(from subnet, to subnet, weakest basis) for each step between two different subnets on a route.
    Hosts the route does not place are skipped, and the step spans them, taking the weakest basis of
    every hop it covers."""
    out: list[tuple[str, str, str]] = []
    prev_i: int | None = None
    for i, z in enumerate(zones):
        if z is None:
            continue
        if prev_i is not None and zones[prev_i] != z:
            out.append((str(zones[prev_i]), z, _weakest([e.get("basis") for e in edges[prev_i:i]])))
        prev_i = i
    return out


def _label(key: str, cidr: str | None, site: str | None, site_names: dict[str, str]) -> str:
    base = cidr or key.split("@", 1)[0]
    name = site_names.get(str(site)) if site else None
    return f"{base} @ {name}" if name else base


def build_zones(
    *,
    analysis: dict[str, Any] | None,
    routes: list[dict[str, Any]],
    site_names: dict[str, str] | None = None,
    computed_at: Any = None,
    engagement_id: Any = None,
) -> dict[str, Any]:
    """The zone view of one engagement. `routes` are STORED routes: {nodes: [asset id], edges: [hop dicts]}.
    `analysis is None` = never computed (nothing is drawn, and nothing is said about it)."""
    site_names = site_names or {}
    out: dict[str, Any] = {
        "engagement_id": str(engagement_id) if engagement_id is not None else None,
        "computed": analysis is not None,
        "computed_at": computed_at.isoformat() if computed_at is not None else None,
        "routes_considered": len(routes) if analysis is not None else None,
        "zones": [], "links": [], "other_zones": 0, "unplaced_assets": None,
        "zones_hidden": 0, "links_hidden": 0, "routes_unplaced": 0,
        # Routes whose first or last host the model did not place in a subnet: they still count in the
        # zones they do cross, but no entry or crown-jewel subnet is claimed for them.
        "entry_unplaced": 0, "jewel_unplaced": 0,
    }
    if analysis is None:
        return out

    coverage = analysis.get("coverage") or {}
    segments = {str(s.get("segment")): s for s in coverage.get("segments") or [] if isinstance(s, dict)}
    out["unplaced_assets"] = coverage.get("assets_without_a_subnet")
    on_fix_list = fix_point_ids(analysis.get("choke"))

    zone: dict[str, dict[str, Any]] = {}
    link: dict[tuple[str, str], dict[str, Any]] = {}

    def z(key: str) -> dict[str, Any]:
        if key not in zone:
            seg = segments.get(key, {})
            zone[key] = {
                "key": key, "label": _label(key, seg.get("cidr"), seg.get("site"), site_names),
                "hosts": seg.get("hosts"), "stale_hosts": seg.get("stale_hosts"),
                "inferred": bool(seg.get("inferred")), "in_scope": seg.get("in_scope", True),
                "entry": False, "jewel": False, "fix": False, "routes": 0,
            }
        return zone[key]

    for r in routes:
        nodes = [str(n).removeprefix("asset:") for n in r.get("nodes") or []]
        edges = [e for e in r.get("edges") or [] if isinstance(e, dict)]
        if not nodes:
            continue
        zs = node_zones(len(nodes), edges)
        known = [x for x in zs if x is not None]
        if not known:
            out["routes_unplaced"] += 1
            continue
        if zs[0] is not None:
            z(zs[0])["entry"] = True
        else:
            out["entry_unplaced"] += 1
        if zs[-1] is not None:
            z(zs[-1])["jewel"] = True
        else:
            out["jewel_unplaced"] += 1
        for aid, x in zip(nodes, zs):
            if x is not None and aid in on_fix_list:
                z(x)["fix"] = True
        for x in dict.fromkeys(known):                      # each zone once per route
            z(x)["routes"] += 1
        seen: set[tuple[str, str]] = set()
        for a, b, basis in route_links(zs, edges):
            k = (a, b)
            cur = link.setdefault(k, {"from": a, "to": b, "routes": 0, "basis": basis})
            if BASIS_RANK.get(basis, 0) < BASIS_RANK.get(cur["basis"], 0):
                cur["basis"] = basis
            if k not in seen:
                cur["routes"] += 1
                seen.add(k)
            z(a), z(b)

    # Draw at most MAX_ZONES: the ones that carry a role first, then the busiest.
    ordered = sorted(zone.values(), key=lambda d: (-(d["entry"] + d["jewel"] + d["fix"]), -d["routes"], d["label"]))
    kept = {d["key"] for d in ordered[:MAX_ZONES]}
    out["zones_hidden"] = max(len(ordered) - MAX_ZONES, 0)
    out["zones"] = sorted((d for d in ordered[:MAX_ZONES]), key=lambda d: d["label"])
    links = [d for d in link.values() if d["from"] in kept and d["to"] in kept]
    out["links_hidden"] = len(link) - len(links)
    for d in links:
        d["weak"] = d["basis"] in WEAK_BASES
    out["links"] = sorted(links, key=lambda d: (d["from"], d["to"]))
    out["other_zones"] = sum(1 for k, s in segments.items() if k not in zone and (s.get("hosts") or 0) > 0)
    return out
