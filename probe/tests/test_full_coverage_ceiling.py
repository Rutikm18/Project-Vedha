"""A scan that must cover all 65,535 ports gets a ceiling sized by its work.

The fixed 2 h ceiling made a full sweep stop wherever the clock ran out and
report the rest not_scanned. Now the ceiling follows the sweep (with headroom
for retries, the cleanup pass and re-assessing what the tail opens), never
below the normal ceiling, never above PROBE_MAX_FULL_SCAN_SECONDS, and a job's
own max_runtime_seconds can still only lower it. When even the maximum cannot
cover every port, the job says which rate would.
"""
from __future__ import annotations

import logging

import pytest

from agent import engine


class TestSizing:
    def test_a_small_sweep_keeps_the_normal_ceiling(self):
        # 1 host x 65,535 at 150 pps is ~7 min of sweeping.
        assert engine._full_coverage_ceiling(hosts=1, ports=65535, rate=150,
                                             base=7200) == 7200

    def test_a_large_sweep_gets_what_it_needs(self):
        got = engine._full_coverage_ceiling(hosts=20, ports=65535, rate=150, base=7200)
        sweep = 20 * 65535 / 150
        assert got == pytest.approx((sweep * 1.5 + 1800) / 0.85)
        assert got > 7200

    def test_it_never_exceeds_the_maximum(self):
        got = engine._full_coverage_ceiling(hosts=254, ports=65535, rate=150, base=7200)
        assert got == engine.MAX_FULL_SCAN_SECONDS

    def test_a_job_can_still_only_lower_it(self):
        assert engine._full_coverage_ceiling(hosts=20, ports=65535, rate=150,
                                             base=7200, explicit=3600) == 3600

    @pytest.mark.parametrize("hosts, ports, rate", [(0, 65535, 150), (1, 0, 150),
                                                    (1, 65535, 0)])
    def test_degenerate_input_keeps_the_base(self, hosts, ports, rate):
        assert engine._full_coverage_ceiling(hosts=hosts, ports=ports, rate=rate,
                                             base=7200) == 7200


class TestRateThatWouldCover:
    def test_it_inverts_the_sizing(self):
        ceiling = 86_400.0
        rate = engine._rate_to_cover(hosts=254, ports=65535, ceiling=ceiling)
        assert engine._full_coverage_ceiling(hosts=254, ports=65535, rate=rate,
                                             base=7200) == pytest.approx(ceiling)

    def test_no_rate_fits_a_ceiling_shorter_than_the_after_sweep_stages(self):
        assert engine._rate_to_cover(hosts=1, ports=65535, ceiling=600) is None


def _run(monkeypatch, scan_type, params):
    seen: dict = {}

    async def _fake(targets, scope, *, cache, trace, **kwargs):
        seen.update(kwargs)
        trace.finalize()
        return {}
    monkeypatch.setattr(engine, "run_engagement", _fake)
    result = engine.run_scan(scan_type, params, validated_scope=["10.0.0.0/24"])
    return result, seen


class TestWiring:
    def test_a_full_port_audit_of_many_hosts_gets_a_longer_ceiling(self, monkeypatch):
        targets = [f"10.0.0.{i}" for i in range(1, 21)]
        result, _ = _run(monkeypatch, "full_port_audit", {"targets": targets})
        ceiling = result["run_stats"]["applied_tuning"]["max_runtime_seconds"]
        assert ceiling > engine.MAX_JOB_SECONDS

    def test_a_narrow_scan_keeps_the_fixed_ceiling(self, monkeypatch):
        targets = [f"10.0.0.{i}" for i in range(1, 21)]
        result, _ = _run(monkeypatch, "discovery", {"targets": targets})
        ceiling = result["run_stats"]["applied_tuning"]["max_runtime_seconds"]
        assert ceiling == engine.MAX_JOB_SECONDS

    def test_when_it_cannot_cover_everything_it_names_the_rate(self, monkeypatch, caplog):
        targets = [f"10.0.0.{i}" for i in range(1, 21)]
        with caplog.at_level(logging.WARNING, logger="engine"):
            _run(monkeypatch, "full_port_audit",
                 {"targets": targets, "max_runtime_seconds": 3600})
        msgs = [r.getMessage() for r in caplog.records]
        assert any("not every port can be swept" in m and "pps would" in m for m in msgs)


class TestTheDeepModePath:
    """The UI's "Deep" mode is uc_deep_port_sweep: every port plus the full
    assessment. Its 64,390-port tail is what used to stop at the fixed ceiling."""

    def test_deep_port_sweep_is_sized_by_its_full_range(self, monkeypatch):
        targets = [f"10.0.0.{i}" for i in range(1, 21)]
        result, seen = _run(monkeypatch, "deep_port_sweep",
                            {"targets": targets, "allow_infeasible": True})
        ceiling = result["run_stats"]["applied_tuning"]["max_runtime_seconds"]
        assert ceiling == pytest.approx(engine._full_coverage_ceiling(
            hosts=20, ports=65535, rate=150, base=engine.MAX_JOB_SECONDS))
        assert ceiling > engine.MAX_JOB_SECONDS

    def test_it_still_phases_and_the_tail_ends_inside_the_ceiling(self, monkeypatch):
        import time
        targets = [f"10.0.0.{i}" for i in range(1, 21)]
        before = time.monotonic()
        result, seen = _run(monkeypatch, "deep_port_sweep",
                            {"targets": targets, "allow_infeasible": True})
        ceiling = result["run_stats"]["applied_tuning"]["max_runtime_seconds"]
        assert seen["first_pass_ports"] and len(seen["first_pass_ports"]) < 2000
        assert len(seen["port_override"]) == 65535
        assert before < seen["tail_deadline"] < time.monotonic() + ceiling
