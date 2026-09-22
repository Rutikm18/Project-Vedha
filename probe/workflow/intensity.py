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
        # Light TOUCH, not light latency. This preset is what an operator picks
        # for a monitored, production or fragile segment, so it is the quietest
        # envelope in the table, not the fastest.
        #
        # It previously declared 800 pps / concurrency 200 / timeout 1.0. That
        # envelope never actually ran: the launcher overrode all four values on
        # every job, and nothing else selects `light`. It was also the least
        # accurate setting here — port_scanner.py:474 measured rate 300 /
        # concurrency 200 reporting 69 FALSE `filtered` on a real LAN host, all
        # 69 of which resolved `closed` when re-probed at 40 / 10. These are the
        # numbers the launcher had been forcing, i.e. the ones with field use
        # behind them.
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
    },
    "deep": {
        "port_profile": "full",      # the entire 1–65535 TCP space
        "rate": 150.0,
        "concurrency": 80,
        "timeout": 4.0,
        "disc_timeout": 2.0,
        "retries": 2,
        # The ONLY preset that needs a ceiling: port_profile="full" is all 65,535
        # ports, and against a host that rate-limits its RSTs that measured an
        # 11.9-hour ETA for a single host while other jobs queued behind it.
        # 30 min comfortably exceeds a healthy full sweep (~21 min at the ~51
        # ports/sec measured after the congestion fixes), so this stops the
        # pathological case without touching a scan that is working. Ports not
        # reached are reported not_scanned, never "filtered".
        "max_host_seconds": 1800,
        # PHASE THE SWEEP. Banner, OS and the deep branches all wait on the port
        # stage, so a single 65,535-port pass meant no host was ASSESSED for
        # hours (109s/host of pure sending at best; 280-2,728s measured). This
        # names the high-signal ports to sweep FIRST; the engine unions it with
        # the branch catalogs, assesses that, then takes the rest as a budgeted
        # tail. Same coverage, and an interrupted job loses the tail rather than
        # the assessment.
        "first_pass_profile": "top1000",
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
