"""
asset_identity.py — when are two observations of one IP the same asset?
(P1b of manager/docs/ATTACK_PATH_PLAN.md, FM-14.)

Assets were keyed by (engagement, IP). That is wrong in exactly one situation:
two sites of the same organisation that each use the same PRIVATE address range
(two branches both on 10.0.0.0/24). Their 10.0.0.5 are different machines, but
were merged into one asset — findings mixed, and attack paths drawn between
networks that are not connected.

The obvious fix — always key by (site, IP) — breaks the platform's own design.
Several probes are meant to scan the SAME host from different vantages:
exposure fusion compares an external probe with an internal one, and branch
probes routinely scan HQ over VPN. Keyed by site, one host scanned from two
sites becomes two assets.

So identity is a policy, chosen per engagement and applied per IP:

  global    (default; today's behaviour) — the IP alone identifies the asset.
  per_site  a NON-GLOBAL IP (RFC 1918, CGNAT, link-local, ULA …) is identified by
            (site of the probe that observed it, IP). A globally-routable IP is
            unique on the internet and is never split, in either mode.

An observation from a probe with no site stays global even in per_site mode.

The operator chooses per_site; this module supplies the evidence to choose it:
  * overlapping_private_ranges — sites whose authorised private ranges overlap
  * identity_conflicts         — the same private IP reported under DIFFERENT
                                 hostnames by different sites: concrete proof
                                 two machines are being merged

Pure and deterministic: no DB, no I/O.
"""
from __future__ import annotations

import ipaddress
from typing import Any, Iterable

MODE_GLOBAL = "global"
MODE_PER_SITE = "per_site"
MODES = (MODE_GLOBAL, MODE_PER_SITE)

RECOMMEND_KEEP = "keep_global"
RECOMMEND_PER_SITE = "consider_per_site"
RECOMMEND_PER_SITE_STRONG = "switch_to_per_site"


def mode_from_roe(rules_of_engagement: dict | None) -> str:
    """Engagement identity mode (rules_of_engagement.asset_identity); default global."""
    val = (rules_of_engagement or {}).get("asset_identity")
    return val if val in MODES else MODE_GLOBAL


def _ip(value: Any) -> ipaddress._BaseAddress | None:
    if value is None:
        return None
    try:
        return ipaddress.ip_address(str(value).split("%", 1)[0].strip())
    except ValueError:
        return None


def is_partitionable(ip_text: Any) -> bool:
    """True for an IP that is NOT globally unique (private, CGNAT, link-local,
    ULA, …), i.e. one that two separate networks can both use. Hostnames and
    unparseable values are not partitioned."""
    ip = _ip(ip_text)
    return ip is not None and not ip.is_global


def identity_site(ip_text: Any, site_id: Any, mode: str) -> Any:
    """The site that scopes this observation's identity, or None for global.

    None whenever mode is global, the observing probe has no site, or the IP is
    globally routable — so one public host scanned from several sites stays one
    asset, and today's behaviour is unchanged by default."""
    if mode != MODE_PER_SITE or site_id is None:
        return None
    return site_id if is_partitionable(ip_text) else None


# ── evidence for the operator ────────────────────────────────────────────────

def _private_networks(cidrs: Iterable[str] | None) -> list[ipaddress._BaseNetwork]:
    nets = []
    for c in cidrs or []:
        try:
            net = ipaddress.ip_network(str(c).strip(), strict=False)
        except ValueError:
            continue
        # A range is "private" for this purpose if its first address is not
        # globally routable (covers RFC 1918, CGNAT, ULA, link-local).
        if not net.network_address.is_global:
            nets.append(net)
    return nets


def overlapping_private_ranges(site_cidrs: dict[Any, Iterable[str]]) -> list[dict[str, Any]]:
    """Pairs of sites whose authorised PRIVATE ranges overlap.

    Overlap is necessary for an identity collision, not sufficient: two sites
    that share one routing domain (connected over VPN, one address plan) can
    legitimately authorise the same range. So this is a prompt to check, never a
    reason to split automatically."""
    sites = sorted(site_cidrs, key=str)
    nets = {s: _private_networks(site_cidrs[s]) for s in sites}
    out: list[dict[str, Any]] = []
    for i, a in enumerate(sites):
        for b in sites[i + 1:]:
            shared = sorted({
                str(na if na.prefixlen >= nb.prefixlen else nb)
                for na in nets[a] for nb in nets[b]
                if na.version == nb.version and na.overlaps(nb)
            })
            if shared:
                out.append({"site_a": str(a), "site_b": str(b), "overlap": shared})
    return out


_GENERIC_NAMES = frozenset({
    "localhost", "localhost.localdomain", "unknown", "none", "null", "host",
    "router", "gateway", "switch", "printer", "android", "iphone", "ipad",
    "raspberrypi", "ubuntu", "debian", "kali", "openwrt", "dd-wrt",
})


def normalize_name(name: Any) -> str | None:
    """Comparable host name: lower-case, trailing dot dropped, the first DNS
    label for comparison. None for empty, IP-looking or generic names that many
    different machines share (they prove nothing about identity)."""
    if not isinstance(name, str):
        return None
    n = name.strip().rstrip(".").lower()
    if not n or _ip(n) is not None:
        return None
    short = n.split(".", 1)[0]
    if len(short) < 3 or short in _GENERIC_NAMES or n in _GENERIC_NAMES:
        return None
    return short


def identity_conflicts(observations: Iterable[tuple[Any, str, Any]]) -> list[dict[str, Any]]:
    """Concrete evidence of merged machines.

    `observations` are (site_id, ip, host_name) triples. A conflict is a private
    IP for which two different sites reported DIFFERENT normalised names — the
    same IP, two machines. Public IPs and site-less observations are ignored
    (they are never partitioned). Same name from two sites is consistent with
    one host scanned from two vantages, so it is not a conflict."""
    by_ip: dict[str, dict[str, set[str]]] = {}
    for site, ip, name in observations:
        if site is None or not is_partitionable(ip):
            continue
        norm = normalize_name(name)
        if norm is None:
            continue
        by_ip.setdefault(str(_ip(ip)), {}).setdefault(str(site), set()).add(norm)

    out: list[dict[str, Any]] = []
    for ip in sorted(by_ip):
        per_site = by_ip[ip]
        if len(per_site) < 2:
            continue
        all_names = [names for names in per_site.values()]
        # conflict iff some pair of sites share NO name
        sites = sorted(per_site)
        disjoint = any(not (per_site[a] & per_site[b])
                       for i, a in enumerate(sites) for b in sites[i + 1:])
        if disjoint:
            out.append({"ip": ip,
                        "names_by_site": {s: sorted(per_site[s]) for s in sites},
                        "distinct_names": sorted(set().union(*all_names))})
    return out


def recommend(mode: str, overlaps: list, conflicts: list) -> dict[str, str]:
    """Plain recommendation for the operator."""
    if mode == MODE_PER_SITE:
        return {"action": "none", "detail": "per-site identity is already on"}
    if conflicts:
        return {"action": RECOMMEND_PER_SITE_STRONG,
                "detail": f"{len(conflicts)} private IP(s) are reported as different "
                          "machines by different sites; they are being merged. Set "
                          "rules_of_engagement.asset_identity = 'per_site'."}
    if overlaps:
        return {"action": RECOMMEND_PER_SITE,
                "detail": "sites authorise overlapping private ranges. If those sites "
                          "are separate networks, set asset_identity = 'per_site'; if "
                          "they are one routed network, keep 'global'."}
    return {"action": RECOMMEND_KEEP, "detail": "no evidence of overlapping address space"}
