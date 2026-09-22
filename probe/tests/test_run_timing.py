"""
test_run_timing.py — A3: make "where did the two hours go?" answerable.

ExecutionTrace already accumulates per-component `duration_s`, and run_stats
already carries `fact_count`. What was missing is the part that turns those into
a diagnosis without a profiler:

  * total elapsed wall time as a NUMBER (started_at/finished_at are ISO strings,
    and nobody diffs timestamps by hand at 3am);
  * the per-stage durations rolled up slowest-first, so the dominant stage is
    the first thing you read;
  * the A2 prediction recorded NEXT TO the actual, so the estimate is
    falsifiable instead of decorative.

Pure functions plus one wiring test. Payload size is deliberately NOT here —
see test_payload_size_logged_at_serialization below for why it lives in the
transport instead.
"""
from __future__ import annotations

from agent import feasibility as fz
from workflow.execution import stage_timings


# ── stage rollup ────────────────────────────────────────────────────────────

def test_stage_timings_orders_slowest_first():
    runs = [
        {"id": "host_discovery", "duration_s": 12.0},
        {"id": "port_scan", "duration_s": 980.5},
        {"id": "service_banner", "duration_s": 140.25},
    ]
    assert stage_timings(runs) == [
        {"component": "port_scan", "seconds": 980.5},
        {"component": "service_banner", "seconds": 140.25},
        {"component": "host_discovery", "seconds": 12.0},
    ]


def test_stage_timings_omits_stages_that_never_ran():
    # A planned-but-skipped component has duration 0.0 and would be pure noise
    # in a rollup whose whole job is to point at the expensive stage.
    runs = [
        {"id": "port_scan", "duration_s": 5.0},
        {"id": "udp_scan", "duration_s": 0.0},
        {"id": "smb_scan", "duration_s": 0.0},
    ]
    assert stage_timings(runs) == [{"component": "port_scan", "seconds": 5.0}]


def test_stage_timings_tolerates_missing_and_malformed_fields():
    # as_list() drops None values, so a key can genuinely be absent.
    runs = [{"id": "a"}, {"duration_s": 3.0}, {"id": "b", "duration_s": "x"},
            {"id": "c", "duration_s": 1.5}]
    assert stage_timings(runs) == [{"component": "c", "seconds": 1.5}]


def test_stage_timings_on_empty_input():
    assert stage_timings([]) == []
    assert stage_timings(None) == []


# ── the estimate, shaped for the result ─────────────────────────────────────

def test_as_run_stats_carries_the_numbers_worth_comparing_against():
    est = fz.estimate(hosts=1000, ports=65535, rate=600, ceiling_seconds=7200.0)
    block = fz.as_run_stats(est)
    assert block is not None
    assert block["verdict"] == "cannot_finish"
    assert block["probes"] == 65_535_000
    assert block["reachable_hosts"] == 65
    assert abs(block["floor_seconds"] - 109_225.0) < 1
    assert abs(block["required_rate"] - 9102.08) < 1


def test_as_run_stats_is_none_when_there_was_nothing_to_predict():
    assert fz.as_run_stats(None) is None


def test_as_run_stats_is_json_serializable():
    import json
    est = fz.estimate(hosts=10, ports=100, rate=50, ceiling_seconds=7200.0)
    json.dumps(fz.as_run_stats(est))          # must not raise


# ── wiring: the numbers reach the job result ────────────────────────────────

def test_run_stats_reports_elapsed_stages_and_the_prediction():
    from agent import engine

    # 10.0.0.1 is unreachable in CI — the run is fast and empty, but the timing
    # block is built on every path, which is the contract under test.
    result = engine.run_scan("full_port_audit", {"targets": ["10.0.0.1"]})
    timing = result["run_stats"]["timing"]

    assert isinstance(timing["elapsed_seconds"], float)
    assert timing["elapsed_seconds"] >= 0.0
    assert isinstance(timing["stages"], list)

    # The A2 estimate rides along so predicted and actual sit side by side.
    assert timing["estimate"]["verdict"] in ("fits", "tight", "cannot_finish")
    assert timing["estimate"]["ports"] == 65535


def test_elapsed_seconds_is_present_even_when_the_scan_finds_nothing():
    from agent import engine
    result = engine.run_scan("discovery", {"targets": ["10.0.0.1"]})
    assert "elapsed_seconds" in result["run_stats"]["timing"]


def test_fact_count_still_present_alongside_the_new_timing_block():
    # A3 is additive: nothing that already worked may move or disappear.
    from agent import engine
    stats = engine.run_scan("discovery", {"targets": ["10.0.0.1"]})["run_stats"]
    for key in ("host_count", "open_ports", "fact_count", "error_count",
                "result_count", "scanners_run", "applied_tuning",
                "scope_enforced"):
        assert key in stats, key


# ── payload size is measured where it is already serialized ─────────────────

def test_payload_size_logged_at_serialization(monkeypatch, caplog):
    """Why transport and not run_stats.

    run_stats is built BEFORE submission, so reporting payload size there means
    an extra json.dumps of the whole result purely to measure it — on the one
    path already carrying four copies of a multi-hundred-MB payload. The
    transport already serializes exactly once, so measuring there is free AND
    reports the true wire size, gzip included.
    """
    import logging

    from agent.transport import Transport

    tr = Transport.__new__(Transport)          # no network, no enrollment
    tr._agent_id = "a1"
    tr._compress_over = 0                      # 0 disables gzip

    class _Resp:
        status_code = 200

    class _Client:
        def post(self, *a, **kw):
            return _Resp()

    tr._client = _Client()
    # auth_header is a read-only property on Transport.
    monkeypatch.setattr(Transport, "auth_header", property(lambda self: {}))
    monkeypatch.setattr(Transport, "ensure_device_access", lambda self: True)

    with caplog.at_level(logging.INFO, logger="transport"):
        assert tr.submit_result("job-1", {"job_id": "job-1", "facts": [1, 2, 3]})

    sized = [r.getMessage() for r in caplog.records if "payload" in r.getMessage()]
    assert sized, "submit_result reported no payload size"
    assert "bytes" in sized[0]
