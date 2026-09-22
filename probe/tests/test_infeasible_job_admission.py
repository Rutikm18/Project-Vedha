"""
H1 — refuse a job that cannot finish, with the remedy attached.

THE FAILURE THIS REPLACES
-------------------------
A job whose port stage cannot complete inside the runtime ceiling looked,
for the entire ceiling, exactly like one that could. The operator waited two
hours and got `partial` / `degraded`, with nothing saying what had been
arithmetically impossible from the first second:

    1022 hosts x 65,535 ports = 66,976,770 probes at 600 pps
      -> floor 31.0 h against a 2.0 h ceiling

A2 made that visible in the log. This makes it a decision.

WHY REFUSE RATHER THAN QUIETLY SCAN LESS
----------------------------------------
Silently downgrading the sweep to whatever fits would return a "successful"
job that covered 1.7% of what was asked — the same class of deception this
whole workstream has been removing (a `filtered` port that was never probed,
a scan_result that dropped 90% of its evidence). A refusal that names the two
configurations which WOULD work is actionable in one step and lies about
nothing.

DELIBERATELY NARROW
-------------------
It fires only when the FLOOR — one probe per port, ignoring retries, the
cleanup pass and every stage after the port sweep — already exceeds the
ceiling. A job that merely looks tight still runs, because it might finish and
a partial result from it is genuinely useful. And `allow_infeasible` exists for
the operator who wants the partial anyway.
"""
from __future__ import annotations

import pytest

from agent import engine


def _job(**over):
    """An envelope whose port stage cannot fit its ceiling.

    ONE host, not the /22 from the field report: the arithmetic is identical
    (floor > ceiling) and the shape of the refusal is what is under test, but a
    red run terminates in a second instead of attempting a real 1022-host
    sweep. `max_runtime_seconds` is the ceiling the floor is measured against.
    """
    params = {
        "targets": ["10.77.0.1"],
        "scope_cidrs": ["10.77.0.0/22"],
        "intensity": "deep",               # port_profile=full -> 65,535 ports
        "rate": 600,                       # 65,535 / 600 = 109 s floor
        "concurrency": 300,
        "max_runtime_seconds": 30,         # ...against a 30 s ceiling
    }
    params.update(over)
    return params


class TestAnImpossibleJobIsRefused:
    def test_the_reported_case_is_refused_immediately(self):
        result = engine.run_scan("full_port_audit", _job())
        assert result["ok"] is False
        assert result["error_code"] == "job_cannot_finish"

    def test_the_refusal_is_instant_not_a_two_hour_wait(self):
        import time

        started = time.monotonic()
        engine.run_scan("full_port_audit", _job())
        assert time.monotonic() - started < 10

    def test_the_refusal_states_the_arithmetic(self):
        result = engine.run_scan("full_port_audit", _job())
        error = result["error"]
        assert "65535" in error.replace(",", "")
        assert "600" in error
        # The verdict has to carry the projected duration, or "cannot finish"
        # is an assertion the operator has no way to check.
        assert "h" in error and "ceiling" in error.lower()

    def test_the_remedy_names_both_configurations_that_would_work(self):
        """Actionable in one step: narrow the scope, or narrow the ports."""
        result = engine.run_scan("full_port_audit", _job())
        remediation = result["issues"][0]["remediation"]
        assert "port" in remediation.lower()
        assert "host" in remediation.lower()

    def test_nothing_was_scanned(self):
        result = engine.run_scan("full_port_audit", _job())
        assert result["facts"] == []
        assert result["outcome"] == "failed"

    def test_the_refusal_is_not_retryable(self):
        """Retrying an unchanged envelope produces the same verdict; the
        manager must not burn the job's attempts on it."""
        result = engine.run_scan("full_port_audit", _job())
        assert result["issues"][0]["retryable"] is False


class TestFeasibleJobsAreUntouched:
    def test_a_single_host_full_port_audit_still_runs(self):
        result = engine.run_scan("full_port_audit", {"targets": ["10.0.0.1"]})
        assert result["ok"] is True

    def test_an_ordinary_discovery_job_still_runs(self):
        result = engine.run_scan("discovery", {"targets": ["10.0.0.1"]})
        assert result["ok"] is True

    def test_a_merely_tight_job_is_allowed_to_try(self):
        """`tight` means the floor fits but the margin is thin. It might
        finish, and a partial from it is useful — only the impossible case is
        worth refusing."""
        from agent import feasibility as fz

        est = fz.estimate(hosts=150, ports=65535, rate=2000,
                          ceiling_seconds=7200.0)
        assert est.verdict == "tight"
        assert engine._refuse_if_infeasible(est, {}) is None


class TestTheOperatorCanOverride:
    def test_allow_infeasible_lets_the_job_proceed(self):
        """Someone who wants two hours of partial coverage may have it — but
        they have to ask."""
        from agent import feasibility as fz

        est = fz.estimate(hosts=1000, ports=65535, rate=600,
                          ceiling_seconds=7200.0)
        assert est.verdict == "cannot_finish"
        assert engine._refuse_if_infeasible(
            est, {"allow_infeasible": True}) is None

    def test_without_the_override_it_is_refused(self):
        from agent import feasibility as fz

        est = fz.estimate(hosts=1000, ports=65535, rate=600,
                          ceiling_seconds=7200.0)
        assert engine._refuse_if_infeasible(est, {}) is not None

    def test_no_estimate_is_never_a_refusal(self):
        """A job whose breadth could not be projected must not be blocked by
        the absence of a number."""
        assert engine._refuse_if_infeasible(None, {}) is None


@pytest.mark.parametrize("flag", [True, "true", 1])
def test_the_override_accepts_the_usual_truthy_spellings(flag):
    from agent import feasibility as fz

    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=7200.0)
    assert engine._refuse_if_infeasible(est, {"allow_infeasible": flag}) is None
