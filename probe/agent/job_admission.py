"""job_admission.py — the agent's independent, defense-in-depth admission gate.

Wired into TaskRunner AFTER the existing engagement-scope / local-ceiling /
exclusion checks, so it is the last gate before a packet leaves:

1. `drop_denied` — the PERMANENT denylist (loopback, link-local incl.
   169.254.169.254, multicast, reserved, broadcast, Manager address) that a CIDR
   allowlist does not catch. Fail-closed.
2. `verify_signed_job` — GATED signed-job verification: enforced only when a
   pinned job-signing key is configured (`PROBE_JOB_SIGNING_KEY`). Off by default
   in this initial phase (the Manager does not sign jobs yet); forward-compatible
   with the agent↔Manager contract (0c).
"""
from __future__ import annotations

import time

from agent import scope_model as sm


def drop_denied(targets: list[str], manager_ip: str | None = None) -> tuple[list[str], list[str]]:
    kept: list[str] = []
    denied: list[str] = []
    for t in targets:
        (denied if sm.is_denied(t, manager_ip) else kept).append(t)
    return kept, denied


def verify_signed_job(params: dict, pinned_key_b64: str | None, now: float | None = None) -> tuple[bool, str]:
    if not pinned_key_b64:
        return True, "signature check skipped (no pinned key configured)"
    if not isinstance(params, dict) or "sig" not in params:
        return False, "pinned job-signing key configured but the job is unsigned"
    from agent import connect
    return connect.verify_job(params, pinned_key_b64, now if now is not None else time.time())
