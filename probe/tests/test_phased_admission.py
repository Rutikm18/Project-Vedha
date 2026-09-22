"""
Admission must size a two-phase sweep by the part that has to finish.

`deep` intensity sweeps all 65,535 ports in two phases: a first pass over the
high-signal ports, with every later stage running on it, then the rest as a
tail budgeted per host that truncates to not_scanned by design. Sizing the
refusal by the full breadth refuses any aggressive scan wider than about 16
hosts at 150 pps, though a /24's first pass finishes in about half an hour.
"""
from __future__ import annotations

from agent import engine
from agent import feasibility as fz
from workflow.intensity import INTENSITY_PRESETS, intensity_first_pass, intensity_port_override
from workflow.workflow_engine import _port_candidates

FULL = intensity_port_override("deep")
FIRST = intensity_first_pass("deep")


class TestAdmissionPortCount:
    def test_a_phased_deep_sweep_is_sized_by_its_first_pass(self):
        """Mirrors run_engagement's own split, so admission and execution
        agree on the port set."""
        expected = len(set(_port_candidates("it", None, port_override=FIRST))
                       & set(_port_candidates("it", None, port_override=FULL)))
        n = fz.admission_port_count("it", None, FULL, FIRST, phased=True)
        assert n == expected
        assert n < 65535

    def test_an_unphased_sweep_is_sized_by_everything_it_sweeps(self):
        """A full-port audit stops at the port stage: nothing to bring
        forward, so every port must finish."""
        assert fz.admission_port_count("it", None, FULL, FIRST, phased=False) == 65535

    def test_a_job_without_a_first_pass_is_unchanged(self):
        assert fz.admission_port_count("it", None, None, None, phased=True) \
            == fz.port_count_for("it", None, None)


class TestTheReportedCase:
    def test_an_aggressive_slash_24_is_admitted(self):
        preset = INTENSITY_PRESETS["deep"]
        estimate = fz.estimate(
            hosts=254,
            ports=fz.admission_port_count("it", None, FULL, FIRST, phased=True),
            rate=preset["rate"], ceiling_seconds=7200, retries=preset["retries"])
        assert estimate.verdict != "cannot_finish"


class TestTheGateStillRefuses:
    def test_a_first_pass_that_cannot_finish_is_still_refused(self):
        """One host, but a 1 s ceiling: the ~1,145-port first pass at 150 pps
        needs ~7.6 s. Refused before a packet leaves, and the message states
        the first-pass arithmetic, not 65,535."""
        result = engine.run_scan("network_va", {
            "targets": ["10.77.0.1"],
            "scope_cidrs": ["10.77.0.0/24"],
            "intensity": "deep",
            "max_runtime_seconds": 1,
        })
        assert result["error_code"] == "job_cannot_finish"
        assert "65535" not in result["error"].replace(",", "")
        assert result["facts"] == []
