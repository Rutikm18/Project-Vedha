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
        "rate": 800.0,
        "concurrency": 200,
        "timeout": 1.0,
        "disc_timeout": 1.0,
        "retries": 0,
    },
    "standard": {
        "port_profile": None,        # defer to the profile's own catalog
        "rate": 200.0,
        "concurrency": 100,
        "timeout": 3.0,
        "disc_timeout": 1.5,
        "retries": 1,
    },
    "deep": {
        "port_profile": "full",      # the entire 1–65535 TCP space
        "rate": 150.0,
        "concurrency": 80,
        "timeout": 4.0,
        "disc_timeout": 2.0,
        "retries": 2,
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
