"""
reachability.py — derive the engagement's network topology for attack-path
generation from data the manager already holds.

The graph engine (app/graph) can only find multi-host paths if it knows which
hosts can reach which. Nothing supplied that before: GraphBuilder.build_from_db
built the graph with no topology at all, so no lateral movement existed
(FM-01 in manager/docs/ATTACK_PATH_PLAN.md). We have no firewall ACLs, so
reachability is INFERRED — MulVAL's host-access-control model rebuilt from
subnet membership — and every inferred link says so.

Model (hub, not mesh — FM-21):
  * one SEGMENT per subnet. Assets join their segment (O(n) edges). Hosts inside
    one subnet reach each other through the segment hub, instead of an O(n²)
    pairwise mesh that explodes path search.
  * Segment → segment LINKS between subnets, labelled by basis:
      same_subnet  hosts on one subnet (link is implicit in the hub)
      assumed      different subnets of the engagement; no evidence either way
    Confidence, not certainty, rides on every link so the analyzer down-weights
    a guess below an adjacency.
  * GATEWAYS (device_role == network_device) are the explicit pivot between
    subnets. In `segmented` posture subnets connect ONLY through a gateway the
    attacker has compromised; in `flat` posture (the default — the conventional
    internal-pentest assumption) subnets are also linked directly, but as
    `assumed`, never as fact.

Subnet assignment: the most specific engagement scope CIDR that contains the
host. A scope broader than a typical subnet (/24 for IPv4, /64 for IPv6) says
little about real segmentation — a single 10.0.0.0/8 scope would put the whole
company in one subnet — so such hosts are bucketed into their /24 (/64) and the
segment is marked `inferred`. A host outside every scope CIDR is bucketed the
same way and marked `unscoped`; a host with no parseable IP is listed, never
silently dropped.

Pure and deterministic: no DB, no I/O, stable ordering.
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from typing import Any, Iterable

from app.detection.asset_identity import MODE_GLOBAL, MODE_PER_SITE, is_partitionable

POSTURE_FLAT = "flat"
POSTURE_SEGMENTED = "segmented"
POSTURES = (POSTURE_FLAT, POSTURE_SEGMENTED)

BASIS_SAME_SUBNET = "same_subnet"
BASIS_ASSUMED = "assumed"
BASIS_CROSS_SITE = "assumed_cross_site"

# Confidence that a hop of this kind is actually open. Coarse on purpose: these
# ORDER paths (adjacent > routed-and-assumed), they are not measured rates.
CONF_SAME_SUBNET = 0.9
CONF_ASSUMED_LINK = 0.5        # flat posture: subnets of one engagement
CONF_GATEWAY_ROUTE = 0.6       # a compromised gateway routes into its other subnets
CONF_CROSS_SITE = 0.3          # two SITES' private networks: even less likely to be connected

_V4_SUBNET = 24
_V6_SUBNET = 64
_GATEWAY_ROLES = frozenset({"network_device", "network"})


@dataclass
class Segment:
    key: str
    cidr: str
    inferred: bool = False         # bucketed from a broad scope, not a declared subnet
    scoped: bool = True            # inside some engagement scope CIDR
    site: str | None = None        # per-site identity: the site whose private network this is
    members: list[str] = field(default_factory=list)
    gateways: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"key": self.key, "cidr": self.cidr, "inferred": self.inferred,
                "scoped": self.scoped, "site": self.site, "members": list(self.members),
                "gateways": list(self.gateways)}


def _parse_networks(cidrs: Iterable[str] | None) -> list[ipaddress._BaseNetwork]:
    nets = []
    for c in cidrs or []:
        try:
            nets.append(ipaddress.ip_network(str(c).strip(), strict=False))
        except ValueError:
            continue
    # most specific first; ties broken deterministically
    nets.sort(key=lambda n: (-n.prefixlen, n.version, str(n)))
    return nets


def _bucket(ip: ipaddress._BaseAddress) -> ipaddress._BaseNetwork:
    plen = _V4_SUBNET if ip.version == 4 else _V6_SUBNET
    return ipaddress.ip_network(f"{ip}/{plen}", strict=False)


def segment_for(ip_text: str | None, scope: list[ipaddress._BaseNetwork]
                ) -> tuple[ipaddress._BaseNetwork, bool, bool] | None:
    """(network, inferred, scoped) for one host IP, or None if unparseable."""
    if not ip_text:
        return None
    try:
        ip = ipaddress.ip_address(str(ip_text).split("%", 1)[0].strip())
    except ValueError:
        return None
    for net in scope:
        if net.version == ip.version and ip in net:
            sub_floor = _V4_SUBNET if ip.version == 4 else _V6_SUBNET
            if net.prefixlen >= sub_floor:
                return net, False, True
            return _bucket(ip), True, True
    return _bucket(ip), True, False


def _attr(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _segment_site(asset: Any, mode: str) -> str | None:
    """The site that owns this asset's private network, or None when its subnet is
    shared. Only under per-site identity, and only for a non-global address: two
    sites that both use 10.0.0.0/24 have two networks, not one (FM-14); a public
    subnet is one network wherever it is seen."""
    if mode != MODE_PER_SITE:
        return None
    site = _attr(asset, "site_id")
    return str(site) if site is not None and is_partitionable(_attr(asset, "ip_address")) else None


def derive_topology(assets: Iterable[Any], scope_cidrs: Iterable[str] | None = None,
                    posture: str = POSTURE_FLAT, identity_mode: str = MODE_GLOBAL) -> dict[str, Any]:
    """Build the engagement topology consumed by GraphBuilder.add_segment_topology.

    `assets` are objects or dicts with `id`, `ip_address` and optional
    `device_role` / `site_id`. With `identity_mode="per_site"` a private subnet is
    keyed by (CIDR, site), so equal CIDRs at two sites are two segments, linked
    only by a low-confidence `assumed_cross_site` edge in flat posture and never
    routed through a gateway of the other site. Returns
      {"posture", "segments": {key: Segment.to_dict()},
       "links":  [{"src", "dst", "basis", "confidence"}],   # segment -> segment
       "routes": [{"gateway", "segment", "basis", "confidence"}],
       "unplaced": [asset_id]}
    """
    if posture not in POSTURES:
        posture = POSTURE_FLAT
    scope = _parse_networks(scope_cidrs)
    segments: dict[str, Segment] = {}
    unplaced: list[str] = []

    for a in sorted(assets, key=lambda x: str(_attr(x, "id"))):
        aid = str(_attr(a, "id"))
        placed = segment_for(_attr(a, "ip_address"), scope)
        if placed is None:
            unplaced.append(aid)
            continue
        net, inferred, scoped = placed
        site = _segment_site(a, identity_mode)
        key = f"{net}@{site}" if site else str(net)
        seg = segments.get(key)
        if seg is None:
            seg = segments[key] = Segment(key=key, cidr=str(net), inferred=inferred, scoped=scoped, site=site)
        seg.members.append(aid)
        role = str(_attr(a, "device_role") or "").lower()
        if role in _GATEWAY_ROLES:
            seg.gateways.append(aid)

    keys = sorted(segments)
    links: list[dict[str, Any]] = []
    routes: list[dict[str, Any]] = []
    if posture == POSTURE_FLAT:
        # O(S²) in SUBNETS, not hosts — S is tens, so this stays small.
        for src in keys:
            for dst in keys:
                if src == dst:
                    continue
                a_site, b_site = segments[src].site, segments[dst].site
                cross_site = a_site is not None and b_site is not None and a_site != b_site
                links.append({"src": src, "dst": dst,
                              "basis": BASIS_CROSS_SITE if cross_site else BASIS_ASSUMED,
                              "confidence": CONF_CROSS_SITE if cross_site else CONF_ASSUMED_LINK})
    # In both postures a compromised gateway routes into every OTHER subnet. We do
    # not know its routing table, so these are `assumed` too; in segmented
    # posture they are the ONLY way across.
    for key in keys:
        for gw in segments[key].gateways:
            for other in keys:
                # a site's gateway does not route into ANOTHER site's private network
                gw_site, other_site = segments[key].site, segments[other].site
                if other != key and not (gw_site and other_site and gw_site != other_site):
                    routes.append({"gateway": gw, "segment": other, "basis": BASIS_ASSUMED,
                                   "confidence": CONF_GATEWAY_ROUTE})

    return {
        "posture": posture,
        "segments": {k: segments[k].to_dict() for k in keys},
        "links": links,
        "routes": routes,
        "unplaced": unplaced,
    }


def posture_from_roe(rules_of_engagement: dict | None) -> str:
    """Engagement-level posture toggle (rules_of_engagement.attack_path_reachability)."""
    val = (rules_of_engagement or {}).get("attack_path_reachability")
    return val if val in POSTURES else POSTURE_FLAT
