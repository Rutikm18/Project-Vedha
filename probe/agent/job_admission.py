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

import ipaddress
import time

from agent import scope_model as sm


def manager_ip_from_env() -> str | None:
    """Resolve the Manager's IP from PLATFORM_URL so the fleet can never scan its
    own control plane. Best-effort — None when unset/unresolvable."""
    import os
    import socket
    from urllib.parse import urlparse
    host = urlparse(os.environ.get("PLATFORM_URL", "")).hostname
    if not host:
        return None
    try:
        return socket.gethostbyname(host)
    except OSError:
        return None


def drop_denied(targets: list[str], manager_ip: str | None = None) -> tuple[list[str], list[str]]:
    """Split targets against the permanent denylist.

    A reserved range (loopback/link-local/multicast/reserved/IPv6/unparseable)
    is dropped whole — nothing in it is legitimately scannable. But a real CIDR
    that merely CONTAINS the manager's own address is NOT dropped wholesale: the
    manager address is carved out and the rest of the range is kept, so scanning
    a /24 that happens to include the control plane still reaches the other
    hosts instead of failing with "all targets denied". `denied` lists the
    manager address for the carve so the drop stays visible to the operator."""
    kept: list[str] = []
    denied: list[str] = []
    mgr = None
    if manager_ip:
        try:
            mgr = ipaddress.ip_address(manager_ip)
        except ValueError:
            mgr = None
    for t in targets:
        if sm.is_reserved_range(t):
            denied.append(t)
            continue
        net = None
        if mgr is not None:
            try:
                net = ipaddress.ip_network(t, strict=False)
            except ValueError:
                net = None
        if net is not None and mgr.version == net.version and mgr in net:
            if net.num_addresses == 1:
                denied.append(t)                       # the target IS the manager
            else:
                mgr_net = ipaddress.ip_network((mgr, net.max_prefixlen))
                kept.extend(str(s) for s in net.address_exclude(mgr_net))
                denied.append(str(mgr))                # carved out, kept visible
        else:
            kept.append(t)
    return kept, denied


def verify_signed_job(params: dict, pinned_key_b64: str | None, now: float | None = None) -> tuple[bool, str]:
    if not pinned_key_b64:
        return True, "signature check skipped (no pinned key configured)"
    if not isinstance(params, dict) or "sig" not in params:
        return False, "pinned job-signing key configured but the job is unsigned"
    from agent import connect
    return connect.verify_job(params, pinned_key_b64, now if now is not None else time.time())
