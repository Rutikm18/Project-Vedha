"""
The scope partition must take a dropped host's METRICS with its facts.

`result["scan_metrics"]` is a top-level convenience list the probe pre-computes
from the same facts it ships (`agent/engine.py`: the `data` of every fact whose
status is `scan_summary`, surfaced at the top so the manager need not filter
facts to find them). partition_result_scope() only ever traversed `hosts`,
`facts` and `findings`, so when it dropped an out-of-scope host the metrics row
attesting to that host's coverage stayed behind.

scan_health_summary() then aggregated a host that is not in the result:
`missing` and `local_resource_errors` from evidence nobody kept, and a
hosts-degraded / hosts-incomplete count over a population that no longer
matches. It can push a scan to `degraded` — raising a coverage finding about a
host the operator never authorized — or dilute a real problem. Either way the
verdict cites evidence that was deliberately discarded.

This is NOT a scope leak. The scan_summary fact's `data` blob itself carries
`vantage` and no target (which is exactly why the identity traversal never
saw it), so nothing out-of-scope was ever laundered into the inventory. What
was wrong is the ACCOUNTING, and this codebase's standing rule is that a
number nobody can trace is worse than no number.

Matching is by VALUE, not by recomputation: the manager does not re-derive a
list the probe declared, it only removes the entries whose fact it just
dropped. `scan_metrics` entries are stamped with the host they describe
(`{**data, "target": target}` — see `agent/engine.py::_scan_metrics_from_facts`),
which also means two hosts that happen to report byte-identical `data` are
unambiguous to remove: the target makes each host's own entry the only one
that matches.
"""
from __future__ import annotations

import pytest

from app.discovery.scan_health import scan_health_summary
from app.services.job_result_service import partition_result_scope

SCOPE = ["10.0.0.0/24"]


def _summary(missing: int = 0, health: str = "ok") -> dict:
    """A scan_summary `data` blob. No target — it describes the sweep."""
    return {
        "vantage": "probe-a",
        "complete": missing == 0,
        "missing": missing,
        "health": health,
        "local_resource_errors": 3 if health == "degraded" else 0,
    }


def _metric(target: str, data: dict) -> dict:
    """What `result["scan_metrics"]` actually holds: the fact's `data`,
    stamped with its `target`, exactly as the probe builds it."""
    return {**data, "target": target}


def _result(*, in_scope_summary: dict, out_of_scope_summary: dict) -> dict:
    return {
        "hosts": [{"ip": "10.0.0.5"}, {"ip": "192.168.99.9"}],
        "facts": [
            {"target": "10.0.0.5", "scanner": "port_scan",
             "status": "scan_summary", "data": in_scope_summary},
            {"target": "192.168.99.9", "scanner": "port_scan",
             "status": "scan_summary", "data": out_of_scope_summary},
        ],
        "scan_metrics": [
            _metric("10.0.0.5", in_scope_summary),
            _metric("192.168.99.9", out_of_scope_summary),
        ],
    }


class TestTheMetricsFollowTheFacts:
    def test_a_dropped_host_loses_its_metrics_row(self):
        clean, dirty = _summary(), _summary(missing=400, health="degraded")
        filtered, rejected = partition_result_scope(
            _result(in_scope_summary=clean, out_of_scope_summary=dirty), SCOPE)

        assert len(rejected) == 2            # the host row and the fact row
        assert filtered["scan_metrics"] == [_metric("10.0.0.5", clean)]

    def test_the_authorized_host_keeps_its_metrics(self):
        clean, dirty = _summary(missing=7), _summary(missing=400)
        filtered, _ = partition_result_scope(
            _result(in_scope_summary=clean, out_of_scope_summary=dirty), SCOPE)

        assert filtered["scan_metrics"] == [_metric("10.0.0.5", clean)]
        assert [f["target"] for f in filtered["facts"]] == ["10.0.0.5"]

    def test_the_health_verdict_stops_citing_discarded_evidence(self):
        """The bug in one number: a degraded verdict sourced entirely from a
        host whose evidence was dropped."""
        clean, dirty = _summary(), _summary(missing=400, health="degraded")
        filtered, _ = partition_result_scope(
            _result(in_scope_summary=clean, out_of_scope_summary=dirty), SCOPE)

        verdict = scan_health_summary(filtered)
        assert verdict["degraded"] is False
        assert verdict["hosts_measured"] == 1
        assert verdict["missing_ports_total"] == 0
        assert verdict["local_resource_errors_total"] == 0

    def test_identical_summaries_drop_exactly_one(self):
        """Two hosts can report byte-identical coverage `data`. The target
        stamp disambiguates them, so dropping one host removes exactly that
        host's entry — never the survivor's, and never both."""
        same = _summary(missing=5)
        filtered, _ = partition_result_scope(
            _result(in_scope_summary=dict(same), out_of_scope_summary=dict(same)),
            SCOPE)

        assert filtered["scan_metrics"] == [_metric("10.0.0.5", same)]

    def test_a_summary_without_data_is_matched_as_the_probe_emitted_it(self):
        """The probe surfaces `{**f.get("data", {}), "target": f.get("target")}`,
        so a summary fact with no `data` key appears in scan_metrics as just
        `{"target": ...}`. The partition must remove that same entry."""
        result = {
            "hosts": [{"ip": "10.0.0.5"}, {"ip": "192.168.99.9"}],
            "facts": [
                {"target": "10.0.0.5", "scanner": "port_scan",
                 "status": "scan_summary", "data": _summary()},
                {"target": "192.168.99.9", "scanner": "port_scan",
                 "status": "scan_summary"},
            ],
            "scan_metrics": [_metric("10.0.0.5", _summary()),
                              {"target": "192.168.99.9"}],
        }
        filtered, _ = partition_result_scope(result, SCOPE)
        assert filtered["scan_metrics"] == [_metric("10.0.0.5", _summary())]


class TestNothingElseMoves:
    def test_an_all_authorized_result_is_untouched(self):
        result = {
            "hosts": [{"ip": "10.0.0.5"}],
            "facts": [{"target": "10.0.0.5", "scanner": "port_scan",
                       "status": "scan_summary", "data": _summary()}],
            "scan_metrics": [_summary()],
        }
        filtered, rejected = partition_result_scope(result, SCOPE)
        assert rejected == []
        assert filtered is result

    def test_a_result_with_no_metrics_still_partitions(self):
        result = {
            "hosts": [{"ip": "10.0.0.5"}, {"ip": "192.168.99.9"}],
            "facts": [],
        }
        filtered, rejected = partition_result_scope(result, SCOPE)
        assert len(rejected) == 1
        assert "scan_metrics" not in filtered

    def test_a_dropped_non_summary_fact_takes_no_metrics_with_it(self):
        """Only scan_summary facts have a metrics row. An ordinary dropped
        fact must not shorten the list."""
        kept = _summary()
        result = {
            "hosts": [],
            "facts": [
                {"target": "10.0.0.5", "scanner": "port_scan",
                 "status": "scan_summary", "data": kept},
                {"target": "192.168.99.9", "scanner": "port_scan",
                 "status": "open", "data": {"port": 80}},
            ],
            "scan_metrics": [kept],
        }
        filtered, rejected = partition_result_scope(result, SCOPE)
        assert len(rejected) == 1
        assert filtered["scan_metrics"] == [kept]

    @pytest.mark.parametrize("metrics", ["not-a-list", None, 42])
    def test_a_malformed_metrics_field_is_left_alone(self, metrics):
        """Never crash ingest over a convenience field."""
        result = {
            "hosts": [{"ip": "192.168.99.9"}, {"ip": "10.0.0.5"}],
            "facts": [],
            "scan_metrics": metrics,
        }
        filtered, _ = partition_result_scope(result, SCOPE)
        assert filtered["scan_metrics"] == metrics
