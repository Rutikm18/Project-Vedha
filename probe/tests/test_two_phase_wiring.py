"""
The two-phase order has to reach a real job, not just run_engagement's kwargs.

`deep` resolves all 65,535 ports, and the assessment stages used to wait for the
whole sweep. Phasing is only worth anything if the intensity preset actually
names a first pass and agent/engine.py hands it over — the same seam that made
the 30-minute host ceiling a no-op for a year.
"""
from __future__ import annotations

import inspect

from workflow.intensity import (
    INTENSITY_PRESETS,
    intensity_first_pass,
    intensity_port_override,
)
from workflow.workflow_engine import run_engagement


class TestPresets:
    def test_deep_names_a_first_pass(self):
        assert INTENSITY_PRESETS["deep"]["first_pass_profile"] is not None

    def test_breadth_bounded_presets_do_not_phase(self):
        """light (~15 ports) and standard (the catalog) are already small; a
        second setup would buy nothing."""
        assert INTENSITY_PRESETS["light"]["first_pass_profile"] is None
        assert INTENSITY_PRESETS["standard"]["first_pass_profile"] is None

    def test_every_preset_declares_the_key(self):
        for name, preset in INTENSITY_PRESETS.items():
            assert "first_pass_profile" in preset, name


class TestFirstPassResolution:
    def test_deep_first_pass_is_a_small_high_signal_set(self):
        first = intensity_first_pass("deep")
        full = intensity_port_override("deep")

        assert first is not None
        assert 0 < len(first) < len(full) / 10, (
            "a first pass that is not much smaller than the full range does not "
            "bring the assessment forward")
        assert {22, 80, 443, 445, 3389} <= set(first)

    def test_the_first_pass_is_inside_the_requested_coverage(self):
        assert set(intensity_first_pass("deep")) <= set(intensity_port_override("deep"))

    def test_standard_and_light_have_no_first_pass(self):
        assert intensity_first_pass("standard") is None
        assert intensity_first_pass("light") is None

    def test_a_pinned_coverage_profile_is_not_phased(self):
        """full_port_audit stops at the port stage — there is no assessment to
        bring forward, so it sweeps once."""
        assert intensity_first_pass("deep", force_profile="full") is None


class TestEngineSeam:
    def test_run_engagement_accepts_the_kwarg(self):
        assert "first_pass_ports" in inspect.signature(run_engagement).parameters

    def test_run_scan_hands_the_first_pass_to_the_engine(self):
        """The seam itself: a preset value the engine never receives is decoration."""
        src = inspect.getsource(__import__("agent.engine", fromlist=["run_scan"]).run_scan)
        assert "first_pass_ports=" in src

    def test_applied_tuning_reports_the_first_pass_size(self):
        """An operator reading run_stats must be able to see the scan was phased."""
        from agent.engine import _applied_tuning
        applied = _applied_tuning({}, 7200.0, intensity="deep",
                                  port_override=list(range(1, 65536)),
                                  first_pass_ports=[22, 80])
        assert applied["tcp_first_pass_ports"] == 2
