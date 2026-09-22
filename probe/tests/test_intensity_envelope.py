"""
The intensity preset is the ONLY source of a scan's probe envelope.

The launcher used to send rate/concurrency/timeout/disc_timeout with every
named intensity, so the preset's own tuning was always discarded while its port
BREADTH survived. Two consequences, in opposite directions:

  * `deep` ran its 65,535 ports at 600 pps / 2.0 s instead of the 150 pps /
    4.0 s that breadth was tuned for.
  * `light` never once ran its declared 800 pps / 1.0 s / retries 0 — the UI
    always forced 50 pps / 20 / 4.0 s over it.

`light`'s declared envelope is also the least accurate in the table, and by a
margin this repo measured rather than assumed: port_scanner.py:474 records rate
300 / concurrency 200 producing 69 FALSE `filtered` on a real LAN host, every
one of which resolved `closed` when re-probed at 40 / 10. 800 / 200 with
timeout 1.0 and no retries sits well past that point. So `light` now carries
the envelope its only caller had always forced, which is both the validated one
and the one its name describes: light TOUCH, not light latency.
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
        """rate 300 / concurrency 200 measured 69 false `filtered`
        (port_scanner.py:474). No preset may ship at or above that point."""
        for name, preset in INTENSITY_PRESETS.items():
            assert preset["rate"] < 300, name
            assert preset["concurrency"] < 200, name

    def test_breadth_and_rate_move_together(self):
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
