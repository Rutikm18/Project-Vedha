"""
scope_validator.py — defense-in-depth scope re-validation for the probe.

The probe independently validates that every target it scans falls within the
engagement's authorized scope. This is a belt-and-suspenders guard: even if a
job's params were tampered with (buggy or compromised manager), the probe
fetches the authoritative scope from the manager and enforces it before any
packet leaves the host.

Responsibilities:
  1. Fetch the engagement's authoritative scope+exclusions from the manager.
  2. Check that provided targets fall fully within the scope CIDRs.
  3. Drop any targets that fall inside excluded CIDRs (carve-outs).

Each function is pure logic except fetch_engagement_scope() which requires
a transport dependency.
"""
from __future__ import annotations

import ipaddress
import logging
from typing import Any, Callable

LOG = logging.getLogger("scope_validator")


def _networks_for_target(value: str) -> list[ipaddress._BaseNetwork] | None:
    """Parse one IP, CIDR, or inclusive IP range into covering networks.

    ``None`` means the value is not an IP-based target (for example, a
    hostname). Manager engagements are IP/CIDR-only, so callers can reject
    that case instead of relying on DNS that may resolve differently at the
    Manager and Probe.
    """
    value = value.strip()
    if not value:
        return None
    if "-" in value and "/" not in value:
        try:
            start_raw, end_raw = (part.strip() for part in value.split("-", 1))
            start = ipaddress.ip_address(start_raw)
            end = ipaddress.ip_address(end_raw)
        except ValueError:
            return None
        if start.version != end.version or int(start) > int(end):
            return None
        return list(ipaddress.summarize_address_range(start, end))
    try:
        return [ipaddress.ip_network(value, strict=False)]
    except ValueError:
        return None


def fetch_engagement_scope(
    engagement_id: str,
    http_get: Callable[[str], dict[str, Any] | None],
) -> tuple[list[str] | None, list[str]]:
    """Fetch the engagement's authoritative scope from the manager.

    Args:
        engagement_id: UUID of the engagement.
        http_get: A callable(path) -> dict-or-None that performs an authenticated
                  GET request. The path will be something like
                  f"/engagements/{engagement_id}/scope".

    Returns:
        (scope_cidrs, excluded_cidrs). scope_cidrs is None if the fetch fails
        (caller falls back to job-params scope); excluded_cidrs is always a
        list (possibly empty).
    """
    try:
        body = http_get(f"/engagements/{engagement_id}/scope")
        if body is not None:
            return (body.get("scope_cidrs") or None, body.get("excluded_cidrs") or [])
        LOG.warning("scope fetch returned None — falling back to job params")
    except Exception as exc:
        LOG.warning("scope fetch failed (%s) — falling back to job params", exc)
    return None, []


def validate_targets_in_scope(
    targets: list[str],
    scope_cidrs: list[str],
) -> tuple[list[str], list[str]]:
    """Check targets against the authoritative scope CIDRs.

    Returns (allowed, rejected). IP ranges and CIDRs must be fully contained,
    not merely overlap. A hostname is allowed only when the authoritative
    scope explicitly contains that exact hostname; it is never DNS-resolved
    here because doing so would create a Manager/Probe TOCTOU boundary.
    """
    networks: list[ipaddress._BaseNetwork] = []
    hostnames: set[str] = set()
    for cidr in scope_cidrs:
        try:
            networks.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            value = str(cidr).strip().lower()
            if value:
                hostnames.add(value)
                LOG.warning("non-IP scope entry in validation: %r", cidr)

    allowed, rejected = [], []
    for t in targets:
        target_networks = _networks_for_target(t)
        if target_networks is None:
            in_scope = t.strip().lower() in hostnames
        else:
            in_scope = all(
                any(
                    target.version == scope.version and target.subnet_of(scope)
                    for scope in networks
                )
                for target in target_networks
            )
        (allowed if in_scope else rejected).append(t)
    return allowed, rejected


def targets_in_excludes(
    targets: list[str],
    excluded_cidrs: list[str],
) -> tuple[list[str], list[str]]:
    """Remove targets that fall inside any excluded CIDR.

    Returns (kept, dropped). A target is dropped here only when its complete
    IP/CIDR/range is covered by an exclusion. Partially-overlapping ranges are
    kept so the engine can subtract excluded addresses individually.
    """
    if not excluded_cidrs:
        return targets, []

    nets: list[ipaddress._BaseNetwork] = []
    for cidr in excluded_cidrs:
        try:
            nets.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            pass

    kept, dropped = [], []
    for t in targets:
        target_networks = _networks_for_target(t)
        excluded = bool(target_networks) and all(
            any(
                target.version == net.version and target.subnet_of(net)
                for net in nets
            )
            for target in target_networks
        )
        (dropped if excluded else kept).append(t)
    return kept, dropped


def merge_exclusions(
    engagement_excludes: list[str],
    job_excludes: list[str] | None,
) -> list[str]:
    """Merge engagement-level exclusions with per-job exclusions.

    Returns a deduplicated, order-preserving list.
    """
    combined: list[str] = []
    seen: set[str] = set()
    for e in [*engagement_excludes, *(job_excludes or [])]:
        e = e.strip()
        if e and e not in seen:
            seen.add(e)
            combined.append(e)
    return combined
