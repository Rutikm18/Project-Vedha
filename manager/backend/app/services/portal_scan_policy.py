"""
portal_scan_policy.py — what a CUSTOMER may run from the portal, and as which
scan type (the allowance it spends).

Four scan types, each with its own allowance in the customer's plan
(services/entitlements.py decides whether the plan includes it):

  stealth    → probe preset `light`
  normal     → probe preset `standard`
  aggressive → probe preset `deep` over the chosen scope
  deep       → uc_deep_port_sweep (every TCP port + the full assessment) on
               EXACTLY ONE asset

Rules enforced here, server-side, on every portal scan path:
  * an unset intensity is materialized (the use case's default, else normal),
    so the probe never falls back to a default the manager didn't account for
  * the full-port capabilities are reachable ONLY as a deep scan on one asset —
    never over a range, and never without spending a deep allowance
  * raw rate/concurrency/timeout overrides are stripped: a customer gets the
    named preset's envelope and nothing else
"""
from __future__ import annotations

import ipaddress

from fastapi import HTTPException, status

from app.services.scope_targets import validate_targets_in_scope

MODE_FOR_INTENSITY = {"light": "stealth", "standard": "normal", "deep": "aggressive"}
INTENSITY_FOR_MODE = {"stealth": "light", "normal": "standard", "aggressive": "deep", "deep": "deep"}
PORTAL_DEFAULT_INTENSITY = "standard"

# The every-port capability a deep scan runs, and the full-port use cases that
# may only be reached that way.
DEEP_SCAN_USE_CASE = "uc_deep_port_sweep"
FULL_PORT_USE_CASES = frozenset({"uc_full_port_audit", "uc_deep_port_sweep"})

# Keys the probe reads to override a preset's envelope
# (probe/agent/engine.py::_tuning_from_params and the kernel-safety escapes).
TUNING_OVERRIDE_KEYS = frozenset({
    "rate", "concurrency", "timeout", "retries", "disc_timeout",
    "max_host_seconds", "allow_degraded_kernel", "allow_infeasible",
})


def _use_case_default(use_case_id: str | None) -> str | None:
    if not use_case_id:
        return None
    from app.routers.agents import _USE_CASES
    return (_USE_CASES.get(use_case_id) or {}).get("intensity")


def portal_use_case_allowed(use_case_id: str) -> bool:
    """Offered in the portal's regular catalogue. The full-port use cases are
    not — they're reached through the Deep scan (one asset) instead."""
    return use_case_id not in FULL_PORT_USE_CASES


def resolve_portal_mode(value, *, use_case_id: str | None) -> tuple[str, str]:
    """(scan type, probe intensity) for a regular (non-deep) portal scan.

    403 for a full-port use case outside a deep scan; 422 for a value that
    isn't an intensity at all. Whether the plan includes the resulting scan
    type is decided when the allowance is spent."""
    from app.routers.agents import _normalize_intensity_name

    if use_case_id in FULL_PORT_USE_CASES:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Full-port scans run as a Deep scan on one asset. Choose Deep scan and pick "
            "the asset.")
    try:
        name = _normalize_intensity_name(value)
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    if name is None:
        name = _use_case_default(use_case_id) or PORTAL_DEFAULT_INTENSITY
    return MODE_FOR_INTENSITY[name], name


def validate_deep_target(targets, scope_cidrs, excluded_cidrs) -> str:
    """The single asset a deep scan may cover, normalized to a host prefix.

    Exactly one entry; a single IP (or a /32 · /128 — never a range); inside the
    engagement scope and outside its exclusions. 422 with a sentence otherwise."""
    items = [t for t in (targets or []) if str(t).strip()]
    if len(items) != 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "A deep scan covers exactly one asset — enter a single IP address.")
    raw = str(items[0]).strip()
    try:
        net = ipaddress.ip_network(raw, strict=False)
    except ValueError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            f"'{raw}' isn't an IP address.")
    if net.num_addresses != 1:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"'{raw}' is a range. A deep scan covers exactly one asset — enter a single IP.")
    normalized = validate_targets_in_scope([str(net)], scope_cidrs, excluded_cidrs)
    if not normalized:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"{net.network_address} is outside your authorized scope (or excluded).")
    return normalized[0]


def strip_tuning_overrides(params: dict) -> dict:
    """A copy of ``params`` without any preset-overriding tuning key."""
    return {k: v for k, v in (params or {}).items() if k not in TUNING_OVERRIDE_KEYS}
