"""
Deep intensity carries a per-host time ceiling.

`deep` sets port_profile="full" — all 65,535 ports. Against a host that
rate-limits its RSTs that measured an 11.9-hour ETA for ONE host, with other jobs
queued behind it. An operator choosing "deep" is asking for thorough, not
unbounded, and nothing in the preset said where thorough ends.

light/standard stay unbounded on purpose: they are already bounded by port
BREADTH (quick = ~15 ports, standard = the profile catalog), so a time ceiling
would add a second, redundant limit that could only ever cut a scan short for no
reason.
"""
from __future__ import annotations

from workflow.intensity import INTENSITY_PRESETS


class TestBudgets:
    def test_deep_has_a_finite_host_budget(self):
        assert INTENSITY_PRESETS["deep"]["max_host_seconds"] == 1800

    def test_light_is_unbounded(self):
        """Already bounded by breadth — ~15 ports."""
        assert INTENSITY_PRESETS["light"]["max_host_seconds"] is None

    def test_standard_is_unbounded(self):
        """Already bounded by the profile's own port catalog."""
        assert INTENSITY_PRESETS["standard"]["max_host_seconds"] is None

    def test_every_preset_declares_the_key(self):
        """Absent-vs-None must not be ambiguous at the call site."""
        for name, preset in INTENSITY_PRESETS.items():
            assert "max_host_seconds" in preset, name

    def test_deep_budget_exceeds_a_healthy_full_sweep(self):
        """A full 65,535-port sweep runs ~21 min at healthy throughput (~51
        ports/sec measured). The ceiling must not cut off a scan that is
        working — it exists to stop the pathological case, not the normal one."""
        assert INTENSITY_PRESETS["deep"]["max_host_seconds"] > 21 * 60


# ── the budget must survive the params -> run_engagement translation ─────────
from agent.engine import _tuning_from_params                # noqa: E402
from workflow.intensity import resolve_intensity            # noqa: E402


class TestTuningTranslation:
    """A preset value that never reaches run_engagement is decoration. These
    assert the whole path: preset -> tuning dict -> engine kwarg."""

    def test_deep_preset_reaches_the_tuning_dict(self):
        t = _tuning_from_params({}, resolve_intensity("deep"))
        assert t["max_host_seconds"] == 1800

    def test_standard_stays_unbounded(self):
        t = _tuning_from_params({}, resolve_intensity("standard"))
        assert t["max_host_seconds"] is None

    def test_operator_override_is_honoured(self):
        t = _tuning_from_params({"max_host_seconds": 600}, resolve_intensity("deep"))
        assert t["max_host_seconds"] == 600

    def test_override_is_clamped_to_a_safe_envelope(self):
        """Same clamping discipline as every other tuning knob — an operator
        cannot set a 1-second budget that guarantees an empty scan."""
        assert _tuning_from_params({"max_host_seconds": 1},
                                   resolve_intensity("deep"))["max_host_seconds"] == 60
        assert _tuning_from_params({"max_host_seconds": 999999},
                                   resolve_intensity("deep"))["max_host_seconds"] == 14400

    def test_override_can_bound_an_otherwise_unbounded_preset(self):
        """An operator running standard against a huge estate may still want a
        ceiling, even though the preset does not ship one."""
        t = _tuning_from_params({"max_host_seconds": 300}, resolve_intensity("standard"))
        assert t["max_host_seconds"] == 300

    def test_run_engagement_accepts_the_kwarg(self):
        """Guards the seam: a tuning key run_engagement does not accept would be
        a TypeError at scan time, not at import time."""
        import inspect
        from workflow.workflow_engine import run_engagement
        assert "max_host_seconds" in inspect.signature(run_engagement).parameters
