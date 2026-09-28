"""
portal_scan_policy.py — what a CUSTOMER may run from the portal.

The portal offers two intensities: stealth (probe preset `light`) and normal
(`standard`). Aggressive (`deep`) is operator-only. The block is enforced here,
server-side, on every portal scan path — hiding the option in the UI is not the
control. Three ways to reach an aggressive scan without typing "deep" are closed:

  * a use case whose default intensity is deep → the use case is not offered
  * an unset intensity → always materialized to an allowed preset, so the probe
    never falls back to a use-case default the manager didn't vet
  * raw rate/concurrency/timeout overrides → stripped from portal jobs; the
    probe's named preset is the only envelope a customer gets
"""
from __future__ import annotations

from fastapi import HTTPException, status

PORTAL_ALLOWED_INTENSITIES = frozenset({"light", "standard"})
PORTAL_DEFAULT_INTENSITY = "standard"

# Keys the probe reads to override a preset's envelope
# (probe/agent/engine.py::_tuning_from_params and the kernel-safety escapes).
TUNING_OVERRIDE_KEYS = frozenset({
    "rate", "concurrency", "timeout", "retries", "disc_timeout",
    "max_host_seconds", "allow_degraded_kernel", "allow_infeasible",
})

_AGGRESSIVE_MSG = ("Aggressive scanning is not available from the customer portal. "
                   "Choose Stealth or Normal, or ask your security team to run it.")


def _use_case_default(use_case_id: str | None) -> str | None:
    if not use_case_id:
        return None
    from app.routers.agents import _USE_CASES
    return (_USE_CASES.get(use_case_id) or {}).get("intensity")


def portal_use_case_allowed(use_case_id: str) -> bool:
    """A use case is offered on the portal only if its default is portal-safe
    (or unset, in which case the portal materializes `standard`)."""
    default = _use_case_default(use_case_id)
    return default is None or default in PORTAL_ALLOWED_INTENSITIES


def resolve_portal_intensity(value, *, use_case_id: str | None) -> str:
    """The intensity a portal job runs at — always one of the allowed presets.

    403 for aggressive (a policy refusal, not a malformed request); 422 for a
    value that isn't an intensity at all."""
    from app.routers.agents import _normalize_intensity_name

    if use_case_id and not portal_use_case_allowed(use_case_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"'{use_case_id}' is an aggressive-only scan. {_AGGRESSIVE_MSG}")
    try:
        name = _normalize_intensity_name(value)
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    if name is None:
        name = _use_case_default(use_case_id) or PORTAL_DEFAULT_INTENSITY
    if name not in PORTAL_ALLOWED_INTENSITIES:
        raise HTTPException(status.HTTP_403_FORBIDDEN, _AGGRESSIVE_MSG)
    return name


def strip_tuning_overrides(params: dict) -> dict:
    """A copy of ``params`` without any preset-overriding tuning key."""
    return {k: v for k, v in (params or {}).items() if k not in TUNING_OVERRIDE_KEYS}
