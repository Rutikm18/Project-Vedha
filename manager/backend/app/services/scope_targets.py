"""
scope_targets.py — the single source of truth for "is this scan target inside the
engagement's authorized scope?"

The engagement's ``scope_cidrs`` is the authoritative allowlist; ``excluded_cidrs``
carves holes out of it. A requested target (a host IP, a CIDR, or an ``a-b``
range) is authorized only if every network it expands to is contained by some
scope CIDR AND overlaps no excluded CIDR.

This logic used to live privately inside ``routers/agents.py`` as the dispatch-time
gate. It is extracted here so the customer portal can apply the SAME check at
request time (fast 422) without duplicating — the two gates cannot drift because
they call one pure function. ``agents.py`` delegates to it; the portal calls it
directly.

``None`` return means "invalid or outside authorization" — callers translate that
to their own rejection (dispatch refusal / HTTP 422). Never reinterpret an empty
or missing scope as unrestricted.
"""
from __future__ import annotations

import ipaddress
from typing import Sequence

IPNetwork = ipaddress.IPv4Network | ipaddress.IPv6Network


def _parse_networks(values: Sequence[str] | None) -> list[IPNetwork] | None:
    if not values:
        return None
    try:
        return [ipaddress.ip_network(str(v).strip(), strict=False) for v in values]
    except (ValueError, TypeError):
        return None


def _expand_requested(values: Sequence[str]) -> list[IPNetwork] | None:
    """Expand raw target tokens (IP / CIDR / ``a-b`` range) into networks.

    Returns ``None`` on any unparseable token (e.g. a hostname), preserving the
    dispatch-gate contract that DNS-requiring targets are never routable.
    """
    networks: list[IPNetwork] = []
    try:
        for raw in values:
            if not isinstance(raw, str) or not raw.strip():
                # A non-string / blank token is not a target we can authorize;
                # signal "no narrowing" to the caller (mirrors the historical
                # dispatch behavior of falling back to the whole scope).
                return None
            value = raw.strip()
            if "-" in value:
                start_raw, end_raw = (p.strip() for p in value.split("-", 1))
                start = ipaddress.ip_address(start_raw)
                end = ipaddress.ip_address(end_raw)
                if start.version != end.version or int(start) > int(end):
                    return None
                networks.extend(ipaddress.summarize_address_range(start, end))
            else:
                networks.append(ipaddress.ip_network(value, strict=False))
    except (ValueError, TypeError):
        return None
    return networks


def validate_targets_in_scope(
    targets: Sequence[str] | str | None,
    scope_cidrs: Sequence[str] | None,
    excluded_cidrs: Sequence[str] | None = None,
) -> list[str] | None:
    """Return the normalized list of authorized target networks, or ``None``.

    * ``scope_cidrs`` empty/None → ``None`` (no scope authorizes no activity;
      never trust caller-supplied targets to create their own boundary).
    * ``targets`` None → the whole scope (no narrowing requested).
    * ``targets`` an explicit empty list → ``None`` (asked for nothing routable).
    * any target outside scope, overlapping an exclusion, or unparseable → ``None``.
    """
    allowed = _parse_networks(scope_cidrs)
    if allowed is None:
        return None

    if targets is None:
        return [str(n) for n in allowed]

    values = [targets] if isinstance(targets, str) else list(targets)
    if not values:
        return None

    requested = _expand_requested(values)
    if requested is None:
        return None

    # Every requested network must sit fully inside an allowed network (same IP
    # version). Overlap alone is insufficient — a partially-overlapping request
    # could reach outside the authorized boundary.
    in_scope = all(
        any(t.version == a.version and t.subnet_of(a) for a in allowed)
        for t in requested
    )
    if not in_scope:
        return None

    excluded = _parse_networks(excluded_cidrs) or []
    if excluded and any(
        t.version == x.version and t.overlaps(x)
        for t in requested for x in excluded
    ):
        return None

    return [str(n) for n in requested]
