"""
fragile.py — the fragile-asset guard.

Some systems fall over under ordinary scanning: HSMs, ATMs, SWIFT gateways and
ICS/OT controllers. In a bank, knocking one over is how a scanning vendor gets
removed. Any host the tagger (or an operator) marks as fragile is therefore
limited to GENTLE scans — passive discovery, or light-intensity discovery and
inventory. For anything heavier, fragile hosts are added to the job's exclusion
list, which the probe itself enforces (task_runner merges ``_excluded_cidrs``).
An admin/manager may override with a written reason; the override is audited.

Operator control, via manual tags:
  scan_policy:fragile    mark any host fragile
  scan_policy:standard   clear a heuristic fragile verdict for this host

Pure logic — the routers load the rows and apply the plan.
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from app.intel.tagging import tag_strings

FRAGILE_TAGS: tuple[str, ...] = (
    "sector_fn:hsm", "sector_fn:atm", "sector_fn:swift", "role:ics", "scan_policy:fragile",
)
OPT_OUT_TAG = "scan_policy:standard"

# Scan types that never send more than discovery traffic. passive_discovery is
# gentle at any intensity (it listens); the others only at the light preset.
_ALWAYS_GENTLE = {"passive_discovery"}
_GENTLE_WHEN_LIGHT = {"discovery", "device_inventory"}


def fragile_reasons(tags: Iterable[str]) -> list[str]:
    tagset = set(tags)
    if OPT_OUT_TAG in tagset:
        return []
    return [t for t in FRAGILE_TAGS if t in tagset]


@dataclass(frozen=True)
class FragileHost:
    ip: str
    reasons: list[str]


def fragile_hosts(rows: Iterable[tuple[str | None, dict | None]]) -> list[FragileHost]:
    """(ip, Asset.tags) rows → the fragile hosts among them."""
    out: list[FragileHost] = []
    for ip, tags in rows:
        if not ip:
            continue
        reasons = fragile_reasons(tag_strings(tags))
        if reasons:
            out.append(FragileHost(ip, reasons))
    return out


def is_gentle(scan_type: str | None, intensity: str | None) -> bool:
    """True when the job is gentle enough for fragile hosts. Unknown scan types
    and unknown intensity fail closed (treated as intrusive)."""
    if scan_type in _ALWAYS_GENTLE:
        return True
    return scan_type in _GENTLE_WHEN_LIGHT and intensity == "light"


@dataclass
class FragilePlan:
    cidrs: list[str] = field(default_factory=list)      # to append to _excluded_cidrs
    hosts: list[dict] = field(default_factory=list)     # [{ip, reasons}] for the response / audit
    fully_blocked: bool = False                         # every targeted address is fragile


def _networks(values: Sequence[str]):
    nets = []
    for v in values:
        try:
            nets.append(ipaddress.ip_network(str(v).strip(), strict=False))
        except ValueError:
            continue
    return nets


def fragile_exclusions(hosts: Iterable[FragileHost], job_scope: Sequence[str]) -> FragilePlan:
    """Exclusions for the fragile hosts that fall inside this job's scope."""
    scope = _networks(job_scope)
    plan = FragilePlan()
    for host in hosts:
        try:
            addr = ipaddress.ip_address(host.ip)
        except ValueError:
            continue
        if any(addr.version == net.version and addr in net for net in scope):
            plan.cidrs.append(f"{addr}/{addr.max_prefixlen}")
            plan.hosts.append({"ip": host.ip, "reasons": host.reasons})
    if plan.cidrs and scope:
        excluded = _networks(plan.cidrs)
        total = sum(net.num_addresses for net in scope)
        covered = sum(1 for net in excluded)
        plan.fully_blocked = covered >= total
    return plan
