"""
intensity.py — the third, orthogonal scan knob.

Two knobs already compose in the engine:
  * mode    (workflow/modes.py) — HOW FAR the funnel runs: host_discovery →
            port_scan → service_banner → deep_scan (the stage ceiling).
  * profile (it / iot / ot)      — WHICH ports and deep branches are in play.

`intensity` is the missing third axis: HOW HARD each stage probes. It is a small,
named preset that bundles port breadth with the rate / concurrency / timeout /
retries envelope, so an operator declares intent ("light", "standard", "deep")
instead of hand-tuning four numbers per job. The three knobs are independent and
compose — a `deep` intensity `discovery` mode still stops after the port stage.

Design rules:
  * `standard` is a NO-OP baseline: its numbers equal the engine's historical
    defaults and its port_profile is None (defer to the profile catalog), so
    every pre-existing use-case behaves exactly as before intensity existed.
  * Presets supply DEFAULTS only. An explicit operator value in the job params
    still wins (and is still clamped to the safe envelope by agent/engine.py) —
    intensity never raises a ceiling the operator did not ask for.
  * Port breadth is expressed as a named port profile resolved through the
    scanner's own resolve_profile(), so "the whole TCP space" has one definition.
"""
from __future__ import annotations

from scanner.port_scanner import resolve_profile

DEFAULT_INTENSITY = "standard"

# Each preset: the port-coverage profile (None = use the it/iot/ot catalog) plus
# the probe envelope. `retries` is PortScanner's extra-attempts-on-silence knob
# (0 = single probe); more retries trade speed for fewer false negatives.
INTENSITY_PRESETS: dict[str, dict] = {
    "light": {
        "port_profile": "quick",     # ~15 highest-signal TCP ports
        # Light TOUCH, not light latency: the preset an operator picks for a
        # monitored, production or fragile segment, so the quietest envelope in
        # the table. It stays well below the point where the reprobe comment in
        # PortScanner.__init__ records a fast sweep (300 pps / concurrency 200)
        # reporting closed ports as `filtered`.
        "rate": 50.0,
        "concurrency": 20,
        "timeout": 4.0,
        "disc_timeout": 2.0,
        # A patient 4.0s timeout at 50 pps already gives a slow responder room
        # to answer, and the reprobe cleanup pass (rate 40 / concurrency 10) is
        # the real second look. Retrying here would only add packets to the one
        # preset whose whole purpose is to emit as few as possible.
        "retries": 0,
        # Already bounded by BREADTH (~15 ports); a time ceiling here could only
        # ever cut short a scan that was going to finish anyway.
        "max_host_seconds": None,
        # Nothing to bring forward: the whole sweep IS the fast set.
        "first_pass_profile": None,
        # Stealth samples only the common UDP services, like standard.
        "udp_profile": "narrow",
    },
    "standard": {
        "port_profile": None,        # defer to the profile's own catalog
        "rate": 200.0,
        "concurrency": 100,
        "timeout": 3.0,
        "disc_timeout": 1.5,
        "retries": 1,
        "max_host_seconds": None,      # bounded by the profile's port catalog
        "first_pass_profile": None,    # the catalog is already the high-signal set
        # Standard samples the common UDP services (DNS/SNMP/NetBIOS/NTP/memcached).
        "udp_profile": "narrow",
    },
    "deep": {
        # Aggressive breadth: the curated ~2,500-port enterprise set (top1000 +
        # the high-value ports companies actually expose), NOT the whole 65,535
        # space. That keeps a /24 inside the job's time ceiling (~70 min at this
        # rate) while probing far wider than standard. Full 65,535-port coverage
        # is the deep_port_sweep use-case, which caps the host count instead.
        "port_profile": "enterprise",
        "rate": 150.0,
        "concurrency": 80,
        "timeout": 4.0,
        "disc_timeout": 2.0,
        "retries": 2,
        # Bounded by breadth now — the enterprise set is small enough that a
        # single sweep finishes without a per-host clock or a phased tail.
        "max_host_seconds": None,
        "first_pass_profile": None,
        # Aggressive probes UDP wide (all catalogued services), where standard
        # samples only the common few. See workflow/gates.py.
        "udp_profile": "wide",
    },
}

VALID_INTENSITIES = frozenset(INTENSITY_PRESETS)


def resolve_intensity(name: str | None) -> dict:
    """Return a COPY of the preset for `name` (falling back to the default).

    Raises ValueError for an unknown, non-empty intensity so a typo in a job is
    rejected loudly rather than silently downgraded.
    """
    key = name or DEFAULT_INTENSITY
    preset = INTENSITY_PRESETS.get(key)
    if preset is None:
        raise ValueError(
            f"unknown intensity {name!r}; valid: {', '.join(sorted(VALID_INTENSITIES))}"
        )
    return dict(preset)


def intensity_first_pass(
    name: str | None,
    *,
    force_profile: str | None = None,
) -> list[int] | None:
    """Ports to sweep BEFORE the rest, or None to sweep once.

    None for every breadth-bounded preset (their whole sweep is already the fast
    set) and for a scan_type that pins its own coverage — a full-port audit stops
    at the port stage, so there is no assessment to bring forward and phasing
    would only add a second scanner setup.
    """
    if force_profile:
        return None
    profile_name = resolve_intensity(name).get("first_pass_profile")
    if profile_name is None:
        return None
    return resolve_profile(profile_name)


#: The UDP services standard/stealth sample: every one the manager has a rule for (DNS, NTP,
#: NetBIOS, SNMP, IKE, IPMI, SSDP, SIP, mDNS, memcached). The wide set is every service the UDP
#: scanner has a probe for (adds TFTP and IKE NAT-T).
_UDP_NARROW = (53, 123, 137, 161, 500, 623, 1900, 5060, 5353, 11211)


def intensity_udp_ports(name: str | None) -> list[int] | None:
    """UDP ports this intensity probes, or None to leave the engine default.

    `wide` (aggressive) probes every catalogued UDP service; `narrow`
    (standard/stealth) samples the common few. Returns None only when a preset
    omits the knob, so the engine keeps its existing UDP behaviour.
    """
    from scanner.udp_scanner import UDP_PROBES
    profile = resolve_intensity(name).get("udp_profile")
    if profile == "wide":
        return sorted(UDP_PROBES)
    if profile == "narrow":
        return sorted(set(_UDP_NARROW) & set(UDP_PROBES))
    return None


def intensity_port_override(
    name: str | None,
    *,
    force_profile: str | None = None,
) -> list[int] | None:
    """Concrete TCP port list for this intensity, or None to defer to the
    profile catalog.

    `force_profile` lets a scan_type pin its own coverage regardless of intensity
    (e.g. full_port_audit is always the whole space). When neither the forced
    profile nor the intensity names a coverage profile, returns None so the
    engine keeps using the it/iot catalog — preserving pre-intensity behavior.
    """
    profile_name = force_profile or resolve_intensity(name)["port_profile"]
    if profile_name is None:
        return None
    return resolve_profile(profile_name)
