"""
test_feasibility.py — A2: can this job finish before the runtime ceiling?

A wide sweep that cannot possibly complete currently looks identical, for the
first two hours, to one that can. The operator waits out the whole ceiling and
gets a `partial` result with no explanation of what was arithmetically
impossible from the first second.

The model is deliberately a FLOOR over the port stage only: one probe per
(host, port) at the configured rate, ignoring banner/deep/UDP stages that run
after it. If even the floor does not fit, nothing downstream can save the job —
which is exactly the verdict worth having up front.

Pure arithmetic. Same shape as test_kernel_limits.py / test_doctor.py.
"""
from __future__ import annotations

from agent import feasibility as fz

CEILING = 7200.0          # PROBE_MAX_JOB_SECONDS default (2h)


# ── the floor: probes / rate ────────────────────────────────────────────────

def test_floor_is_probes_over_rate():
    est = fz.estimate(hosts=100, ports=1000, rate=200, ceiling_seconds=CEILING)
    assert est is not None
    assert est.probes == 100_000
    assert abs(est.floor_seconds - 500.0) < 0.01       # 100k / 200


def test_rate_is_shared_across_hosts_not_per_host():
    # The scanner's RateLimiter lives on the scanner INSTANCE, and one instance
    # serves every host in the port stage. Doubling the host count therefore
    # doubles the wall clock — it does not run in parallel at full rate each.
    one = fz.estimate(hosts=1, ports=65535, rate=600, ceiling_seconds=CEILING)
    ten = fz.estimate(hosts=10, ports=65535, rate=600, ceiling_seconds=CEILING)
    assert one is not None and ten is not None
    assert abs(ten.floor_seconds - one.floor_seconds * 10) < 0.01


def test_estimate_declines_to_guess_on_degenerate_input():
    assert fz.estimate(hosts=0, ports=1000, rate=200, ceiling_seconds=CEILING) is None
    assert fz.estimate(hosts=10, ports=0, rate=200, ceiling_seconds=CEILING) is None
    assert fz.estimate(hosts=10, ports=10, rate=0, ceiling_seconds=CEILING) is None
    assert fz.estimate(hosts=10, ports=10, rate=200, ceiling_seconds=0) is None


# ── verdicts ────────────────────────────────────────────────────────────────

def test_normal_intensity_on_a_slash24_fits():
    est = fz.estimate(hosts=254, ports=100, rate=200, ceiling_seconds=CEILING)
    assert est is not None and est.verdict == "fits"


def test_stealth_intensity_fits():
    est = fz.estimate(hosts=254, ports=15, rate=50, ceiling_seconds=CEILING)
    assert est is not None and est.verdict == "fits"


def test_a_job_over_half_the_ceiling_is_tight_not_fine():
    # Retries and the stages after the port sweep both add on top of the floor,
    # so a floor past half the ceiling will not survive contact with reality.
    # 150 x 65,535 at the 2000 pps clamp = 4,915s floor against a 7,200s ceiling.
    est = fz.estimate(hosts=150, ports=65535, rate=2000, ceiling_seconds=CEILING)
    assert est is not None
    assert est.floor_seconds < CEILING          # the floor alone does fit...
    assert est.verdict == "tight"               # ...but only just


def test_the_same_sweep_over_fewer_hosts_genuinely_fits():
    # 100 hosts is 3,277s — comfortably under half the ceiling. The boundary is
    # real, not a blanket pessimism about wide sweeps.
    est = fz.estimate(hosts=100, ports=65535, rate=2000, ceiling_seconds=CEILING)
    assert est is not None and est.verdict == "fits"


def test_the_reported_aggressive_job_cannot_finish():
    # 1000 hosts x 65,535 ports at the UI's "aggressive" 600 pps.
    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=CEILING,
                      retries=2)
    assert est is not None
    assert est.verdict == "cannot_finish"
    assert est.probes == 65_535_000
    assert abs(est.floor_seconds - 109_225.0) < 1        # 30.3 hours
    assert est.floor_seconds > CEILING * 15              # off by more than 15x


# ── the two numbers an operator can act on ──────────────────────────────────

def test_reachable_hosts_says_how_much_of_the_scope_actually_fits():
    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=CEILING)
    assert est is not None
    # 7200s x 600pps / 65535 ports = ~65 hosts, not 1000.
    assert est.reachable_hosts == 65


def test_reachable_hosts_never_exceeds_the_scope():
    est = fz.estimate(hosts=10, ports=100, rate=1000, ceiling_seconds=CEILING)
    assert est is not None and est.reachable_hosts == 10


def test_required_rate_says_what_would_make_it_fit():
    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=CEILING)
    assert est is not None
    # 65.5M probes / 7200s = ~9,102 pps — above the 2000 pps clamp, so the rate
    # knob alone cannot rescue this job. That is the point of reporting it.
    assert abs(est.required_rate - 9102.08) < 1


# ── the terms that dominate, and why C1/C2 exist ────────────────────────────

def test_retries_multiply_the_send_phase():
    est = fz.estimate(hosts=10, ports=65535, rate=600, ceiling_seconds=CEILING,
                      retries=2)
    assert est is not None
    # retries=2 means up to 3 probes on a silent port.
    assert abs(est.retry_seconds - est.floor_seconds * 3) < 0.01


def test_the_unbounded_reprobe_pass_dominates_everything_else():
    # The cleanup pass re-probes ambiguous ports at 40 pps with 4 attempts each
    # and is NOT bounded by max_host_seconds. On a silent host it is two orders
    # of magnitude more expensive than the sweep it is cleaning up after.
    est = fz.estimate(hosts=1, ports=65535, rate=600, ceiling_seconds=CEILING)
    assert est is not None
    assert est.reprobe_seconds > est.floor_seconds * 50
    # ONE fully-filtered host spends 6,554s — 91% of the entire 2h job ceiling —
    # in a cleanup pass that max_host_seconds does not bound. So two such hosts
    # exhaust the job on their own, before any other host is touched.
    assert est.reprobe_seconds > CEILING * 0.9
    assert est.reprobe_seconds * 2 > CEILING


# ── rendering ───────────────────────────────────────────────────────────────

def test_describe_is_one_line_naming_the_verdict_and_the_numbers():
    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=CEILING)
    line = fz.describe(est)
    assert "\n" not in line
    assert "1000" in line and "65535" in line
    assert "cannot_finish" in line or "cannot finish" in line


def test_as_check_is_advisory_and_carries_remediation_when_it_cannot_finish():
    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=CEILING)
    check = fz.as_check(est)
    assert check.name == "runtime"
    assert check.status == "warn"           # advisory: A2 never blocks
    assert "65" in check.remediation        # tells you what does fit
    assert check.status != "fail"


def test_as_check_passes_for_a_job_that_fits():
    est = fz.estimate(hosts=254, ports=100, rate=200, ceiling_seconds=CEILING)
    check = fz.as_check(est)
    assert check.status == "pass"


def test_as_check_warns_on_tight_without_claiming_failure():
    est = fz.estimate(hosts=150, ports=65535, rate=2000, ceiling_seconds=CEILING)
    check = fz.as_check(est)
    assert check.status == "warn" and "tight" in check.detail.lower()


# ── port-count resolution: the estimate needs the REAL sweep width ──────────

def test_port_count_for_matches_the_engine_s_own_catalog_resolution():
    # Must agree with workflow_engine._port_candidates or the estimate is fiction.
    from workflow.workflow_engine import _port_candidates
    for profile in ("it", "iot"):
        for override in (None, list(range(1, 65536))):
            expected = len(_port_candidates(profile, None, port_override=override))
            assert fz.port_count_for(profile, None, override) == expected


def test_port_count_for_a_full_override_is_the_whole_tcp_space():
    full = list(range(1, 65536))
    assert fz.port_count_for("it", None, full) == 65535


# ── the wiring, not just the arithmetic ─────────────────────────────────────
# engine.run_scan wraps the preflight in `except Exception` so diagnostics can
# never fail a scan. That also means a NameError or a bad import silently
# DISABLES it, which is how this very call site shipped broken once (LOG was
# not defined in engine.py). These tests assert the line actually reaches the
# log, so the preflight cannot rot back into a no-op unnoticed.

def test_run_scan_logs_a_runtime_estimate(caplog):
    import logging

    from agent import engine

    # 10.0.0.1 is unreachable in CI, so no packets land — but the preflight runs
    # before any probe is sent, which is exactly when it is supposed to speak.
    with caplog.at_level(logging.INFO, logger="engine"):
        result = engine.run_scan("full_port_audit", {"targets": ["10.0.0.1"]})

    assert result["ok"] is True
    estimates = [r.getMessage() for r in caplog.records
                 if r.getMessage().startswith("Runtime estimate:")]
    assert estimates, "preflight produced no runtime estimate — is it being swallowed?"
    line = estimates[0]
    assert "65535 port(s)" in line          # the REAL sweep width, not a guess
    assert "1 host(s)" in line


def test_run_scan_preflight_uses_the_resolved_envelope_not_defaults(caplog):
    import logging

    from agent import engine

    # deep intensity clamps rate to the preset's 150 pps unless overridden.
    with caplog.at_level(logging.INFO, logger="engine"):
        engine.run_scan("full_port_audit",
                        {"targets": ["10.0.0.1"], "rate": 600})

    line = next(r.getMessage() for r in caplog.records
                if r.getMessage().startswith("Runtime estimate:"))
    assert "600 pps" in line, line
