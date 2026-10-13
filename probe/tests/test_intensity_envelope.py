"""
The intensity preset is the ONLY source of a scan's probe envelope.

The launcher sends nothing but the intensity name, so each preset's rate,
concurrency and timeouts are what actually reach the scanner. Breadth and rate
move in opposite directions: a wide sweep at a quick-sweep rate reports closed
ports as `filtered`, as the reprobe comment in PortScanner.__init__ records.
"""
from __future__ import annotations

import pytest

from agent.engine import _tuning_from_params
from workflow.intensity import INTENSITY_PRESETS, resolve_intensity

# The envelope each preset must resolve to with no operator override.
# rate, concurrency, timeout, disc_timeout
EXPECTED = {
    "light":    (50.0, 20, 4.0, 2.0),
    "standard": (200.0, 100, 3.0, 1.5),
    "deep":     (150.0, 80, 4.0, 2.0),
}


class TestPresetEnvelope:
    @pytest.mark.parametrize("name", sorted(EXPECTED))
    def test_preset_declares_the_expected_envelope(self, name):
        rate, conc, timeout, disc = EXPECTED[name]
        preset = INTENSITY_PRESETS[name]
        assert (preset["rate"], preset["concurrency"],
                preset["timeout"], preset["disc_timeout"]) == (rate, conc, timeout, disc)

    @pytest.mark.parametrize("name", sorted(EXPECTED))
    def test_envelope_reaches_the_tuning_dict(self, name):
        """A preset value that never reaches run_engagement is decoration."""
        rate, conc, timeout, disc = EXPECTED[name]
        t = _tuning_from_params({}, resolve_intensity(name))
        assert (t["rate"], t["concurrency"], t["timeout"], t["disc_timeout"]) \
            == (rate, conc, timeout, disc)

    def test_light_is_quieter_than_standard(self):
        """`light` is the one an operator picks for a monitored or fragile
        segment. It must not out-shout the balanced default."""
        assert INTENSITY_PRESETS["light"]["rate"] < INTENSITY_PRESETS["standard"]["rate"]
        assert (INTENSITY_PRESETS["light"]["concurrency"]
                < INTENSITY_PRESETS["standard"]["concurrency"])

    def test_no_preset_exceeds_the_measured_false_filtered_threshold(self):
        """rate 300 / concurrency 200 measured 69 false `filtered` (the reprobe
        comment in PortScanner.__init__). No preset may ship at or above it."""
        for name, preset in INTENSITY_PRESETS.items():
            assert preset["rate"] < 300, name
            assert preset["concurrency"] < 200, name

    def test_wider_sweeps_probe_more_gently(self):
        """The wider the sweep, the gentler the probe has to be: a 65,535-port
        pass at a quick-sweep rate is what made `deep` a lower-ACCURACY mode."""
        assert INTENSITY_PRESETS["deep"]["rate"] < INTENSITY_PRESETS["standard"]["rate"]
        assert INTENSITY_PRESETS["deep"]["timeout"] > INTENSITY_PRESETS["standard"]["timeout"]


class TestOperatorOverrideStillWins:
    """Presets supply DEFAULTS. Someone who genuinely wants a different
    envelope may still ask for one — they just have to ask."""

    def test_explicit_rate_beats_the_preset(self):
        t = _tuning_from_params({"rate": 40}, resolve_intensity("deep"))
        assert t["rate"] == 40

    def test_explicit_override_is_still_clamped(self):
        t = _tuning_from_params({"rate": 1e9}, resolve_intensity("light"))
        assert t["rate"] == 2000


def test_udp_breadth_scales_with_intensity():
    """Aggressive probes UDP wide (every catalogued service); standard/stealth
    sample only the common few."""
    from workflow.intensity import intensity_udp_ports
    from scanner.udp_scanner import UDP_PROBES
    assert intensity_udp_ports("deep") == sorted(UDP_PROBES)          # wide
    narrow = intensity_udp_ports("standard")
    assert set(narrow) == {53, 123, 137, 161, 500, 623, 1900, 5060, 5353, 11211}   # every service the manager has a rule for
    assert intensity_udp_ports("light") == narrow
    assert len(intensity_udp_ports("deep")) > len(narrow)
