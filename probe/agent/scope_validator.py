"""
scope_validator.py — defense-in-depth scope re-validation for the probe.

The probe independently validates that every target it scans falls within the
engagement's authorized scope. This is a belt-and-suspenders guard: even if a
job's params were tampered with (buggy or compromised manager), the probe
fetches the authoritative scope from the manager and enforces it before any
packet leaves the host.

Responsibilities:
  1. Fetch the engagement's authoritative scope+exclusions from the manager.
  2. Check that provided targets fall within the scope CIDRs.
  3. Drop any targets that fall inside excluded CIDRs (carve-outs).

Each function is pure logic except fetch_engagement_scope() which requires
a transport dependency.
"""
from __future__ import annotations

import ipaddress
import logging
from typing import Any, Callable

LOG = logging.getLogger("scope_validator")


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

    Returns (allowed, rejected). Hostname targets that cannot be resolved to
    an IP are passed through (the engine's ScopeGuard handles them at the
    packet level).
    """
    networks = []
    for cidr in scope_cidrs:
        try:
            networks.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            LOG.warning("invalid scope CIDR in validation: %r", cidr)

    allowed, rejected = [], []
    for t in targets:
        host = t.split(":")[0] if ":" in t else t
        try:
            addr = ipaddress.ip_address(host)
            in_scope = any(addr in net for net in networks)
        except ValueError:
            # hostname or CIDR — pass through, ScopeGuard handles at packet level
            in_scope = True
        (allowed if in_scope else rejected).append(t)
    return allowed, rejected


def targets_in_excludes(
    targets: list[str],
    excluded_cidrs: list[str],
) -> tuple[list[str], list[str]]:
    """Remove targets that fall inside any excluded CIDR.

    Returns (kept, dropped). A literal IP target that lands in an exclusion
    is dropped here before any packet — the engine's ScopeGuard enforces the
    same rule again at the packet level. Hostnames that can't be resolved are
    kept (ScopeGuard handles them).
    """
    if not excluded_cidrs:
        return targets, []

    nets = []
    for cidr in excluded_cidrs:
        try:
            nets.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            pass

    kept, dropped = [], []
    for t in targets:
        host = t.split(":")[0] if ":" in t else t
        try:
            addr = ipaddress.ip_address(host)
            excluded = any(addr in net for net in nets)
        except ValueError:
            excluded = False  # CIDR/hostname targets handled by ScopeGuard
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
