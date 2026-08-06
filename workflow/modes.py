"""
modes.py — engagement mode configurations. Each mode is a thin config that
tunes run_engagement()'s behavior; gates.py/cache.py never special-case a
mode by name.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

VALID_SERVICES = {"tls", "web", "smb", "db", "mcp_ai", "udp", "snmp"}

STAGE_HOST_DISCOVERY = "host_discovery"
STAGE_PORT_SCAN = "port_scan"
STAGE_SERVICE_BANNER = "service_banner"
STAGE_DEEP_SCAN = "deep_scan"
STAGE_ORDER = (
    STAGE_HOST_DISCOVERY,
    STAGE_PORT_SCAN,
    STAGE_SERVICE_BANNER,
    STAGE_DEEP_SCAN,
)


def resolve_stage_ceiling(
    stage_ceiling: str | None,
    *,
    stop_after_banner: bool = False,
) -> str:
    """Resolve the explicit ceiling while preserving the legacy triage knob."""
    ceiling = (
        stage_ceiling
        if stage_ceiling is not None
        else STAGE_SERVICE_BANNER
        if stop_after_banner
        else STAGE_DEEP_SCAN
    )
    if ceiling not in STAGE_ORDER:
        raise ValueError(
            f"unknown stage ceiling {ceiling!r}; valid: {', '.join(STAGE_ORDER)}"
        )
    return ceiling


def includes_stage(stage_ceiling: str, stage: str) -> bool:
    """Return whether a bounded plan includes `stage`."""
    return STAGE_ORDER.index(stage) <= STAGE_ORDER.index(stage_ceiling)


@dataclass
class EngagementMode:
    name: str
    stop_after_banner: bool
    service_filter: set[str] | None
    force_recheck_after: timedelta | None
    requires_prior_engagement: bool = False
    stage_ceiling: str = STAGE_DEEP_SCAN


def discovery() -> EngagementMode:
    """Host discovery plus the profile's TCP port catalog."""
    return EngagementMode(
        "discovery",
        stop_after_banner=True,
        service_filter=None,
        force_recheck_after=None,
        stage_ceiling=STAGE_PORT_SCAN,
    )


def host_discovery() -> EngagementMode:
    """Liveness checks only."""
    return EngagementMode(
        "host-discovery",
        stop_after_banner=True,
        service_filter=None,
        force_recheck_after=None,
        stage_ceiling=STAGE_HOST_DISCOVERY,
    )


def port_scan() -> EngagementMode:
    """Liveness checks plus the profile's TCP port catalog."""
    return EngagementMode(
        "port-scan",
        stop_after_banner=True,
        service_filter=None,
        force_recheck_after=None,
        stage_ceiling=STAGE_PORT_SCAN,
    )


def service_fingerprint() -> EngagementMode:
    """Liveness, TCP ports, and service banners without deep branches."""
    return EngagementMode(
        "service-fingerprint",
        stop_after_banner=True,
        service_filter=None,
        force_recheck_after=None,
        stage_ceiling=STAGE_SERVICE_BANNER,
    )


def triage() -> EngagementMode:
    """Discovery + ports + banner only — no deep dives, no credentials."""
    return EngagementMode("triage", stop_after_banner=True,
                          service_filter=None, force_recheck_after=None,
                          stage_ceiling=STAGE_SERVICE_BANNER)


def assessment() -> EngagementMode:
    """Full funnel, every branch the profile allows."""
    return EngagementMode("assessment", stop_after_banner=False,
                          service_filter=None, force_recheck_after=None,
                          stage_ceiling=STAGE_DEEP_SCAN)


def service_specific(services: set[str]) -> EngagementMode:
    if not services <= VALID_SERVICES:
        raise ValueError(f"unknown service(s): {services - VALID_SERVICES}; valid: {VALID_SERVICES}")
    return EngagementMode("service-specific", stop_after_banner=False,
                          service_filter=services, force_recheck_after=None,
                          stage_ceiling=STAGE_DEEP_SCAN)


def re_scan(recheck_older_than: timedelta) -> EngagementMode:
    """Loads a prior engagement's cache; only facts older than
    recheck_older_than get re-probed (deterministic ones included — a
    service really could have changed since last time), everything fresher
    is reused as-is."""
    return EngagementMode("re-scan", stop_after_banner=False,
                          service_filter=None, force_recheck_after=recheck_older_than,
                          requires_prior_engagement=True,
                          stage_ceiling=STAGE_DEEP_SCAN)


MODE_FACTORY = {
    "triage": lambda **kw: triage(),
    "assessment": lambda **kw: assessment(),
    "service-specific": lambda **kw: service_specific(kw["services"]),
    "re-scan": lambda **kw: re_scan(kw["recheck_older_than"]),
}
