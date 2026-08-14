#!/usr/bin/env python3
"""
unauth_access.py — proof of UNAUTHENTICATED access to auth-less-by-default data
stores, from the banner the collector already captured.

Offensive value: "port 6379 open" is informational; "Redis answered with no auth"
is a P1 foothold — full read/write of the data, and RCE via `CONFIG SET dir` +
`SAVE` (webshell / cron / authorized_keys). This module turns the observed
response into that verdict.

Safety: this is INTERPRETATION ONLY of bytes already collected by service_banner's
existing read-only probes (null / HTTP GET / generic). No credentials are ever
sent — these services have NO authentication by default, so a normal read reveals
whether auth is enforced. Not an authentication attempt, not a write, not
brute force. `classify_unauth_access` returns:
    True  — a read succeeded with no auth (proven unauthenticated access)
    False — the service demanded auth (protected)
    None  — the banner doesn't say (no finding raised — never guess)
"""
from __future__ import annotations

# Services whose UNAUTH exposure is directly RCE-capable (not just data access).
RCE_CAPABLE = {"redis"}

# service -> (unauth markers, protected markers). Lowercased substring match.
_MARKERS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "redis": (("redis_version", "# server", "+pong", "run_id", "redis_git", "uptime_in_seconds"),
              ("noauth", "-denied", "authentication required", "operation not permitted")),
    "memcached": (("stat pid", "stat version", "version ", "stat uptime"),
                  ("client error", "authentication")),
    "mongodb": (("ismaster", "maxwireversion", "topologyversion", "hellook", "\"ok\" : 1"),
                ("unauthorized", "requires authentication", "authentication failed")),
    "elasticsearch": (("you know, for search", "cluster_name", "lucene_version", "\"cluster_uuid\""),
                      ("missing authentication", "security_exception", "unauthorized")),
    "couchdb": (("\"couchdb\":\"welcome\"", "\"couchdb\": \"welcome\"", "welcome"),
                ("unauthorized", "you are not a server admin")),
}


def _as_text(banner) -> str:
    if banner is None:
        return ""
    if isinstance(banner, bytes):
        banner = banner.decode("latin-1", errors="replace")
    return str(banner).lower()


def classify_unauth_access(service: str | None, banner) -> bool | None:
    """Decide whether `banner` proves unauthenticated access for `service`.

    True = unauthenticated read succeeded; False = auth enforced; None = unknown.
    Protected markers win over unauth markers (a NOAUTH error is decisive)."""
    svc = (service or "").lower()
    markers = _MARKERS.get(svc)
    if not markers:
        return None
    text = _as_text(banner)
    if not text:
        return None
    unauth_markers, protected_markers = markers
    if any(m in text for m in protected_markers):
        return False
    if any(m in text for m in unauth_markers):
        return True
    return None


def is_rce_capable(service: str | None) -> bool:
    return (service or "").lower() in RCE_CAPABLE
