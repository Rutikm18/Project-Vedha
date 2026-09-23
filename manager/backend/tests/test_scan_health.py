"""
test_scan_health.py — the probe scan-metrics → coverage/health verdict.

Guards the false-NEGATIVE surface: a firewall-truncated or fd-exhausted scan
must be flagged (should_warn) instead of passing as a clean host, while a genuine
clean scan and a metrics-less scan must NOT warn.
"""
from __future__ import annotations

from app.discovery.scan_health import scan_health_summary


def _summary(**metric):
    return scan_health_summary({"scan_metrics": [metric]})


def test_clean_scan_is_healthy_and_does_not_warn():
    s = _summary(health="ok", complete=True, missing=0, local_resource_errors=0)
    assert s["healthy"] is True
    assert s["degraded"] is False and s["incomplete"] is False
    assert s["should_warn"] is False


def test_local_resource_errors_flag_degraded():
    s = _summary(health="degraded", complete=True, missing=0, local_resource_errors=7)
    assert s["degraded"] is True
    assert s["should_warn"] is True
    assert s["local_resource_errors_total"] == 7
    assert "under-report" in s["reason"]


def test_missing_ports_flag_incomplete():
    s = _summary(health="ok", complete=False, missing=12, local_resource_errors=0)
    assert s["incomplete"] is True
    assert s["should_warn"] is True
    assert s["missing_ports_total"] == 12
    assert s["healthy"] is False


def test_no_metrics_means_nothing_to_attest():
    s = scan_health_summary({"scan_type": "host_discovery"})
    assert s["hosts_measured"] == 0
    assert s["healthy"] is False        # nothing measured
    assert s["should_warn"] is False    # ...but nothing to warn about either
    assert scan_health_summary(None)["should_warn"] is False


def test_aggregates_across_hosts():
    result = {"scan_metrics": [
        {"health": "ok", "complete": True, "missing": 0, "local_resource_errors": 0},
        {"health": "degraded", "complete": True, "missing": 0, "local_resource_errors": 3},
        {"health": "ok", "complete": False, "missing": 5, "local_resource_errors": 0},
    ]}
    s = scan_health_summary(result)
    assert s["hosts_measured"] == 3
    assert s["hosts_degraded"] == 1
    assert s["hosts_incomplete"] == 1
    assert s["missing_ports_total"] == 5
    assert s["should_warn"] is True


# ── F3: two-phase hosts must count once, and budget truncation is honest ──────
#
# A two-phase deep scan emits TWO scan_summary facts per host (first pass +
# tail, disjoint port ranges), and both carry the SAME `target`. Grouping by
# that target is what keeps
# hosts_measured / hosts_degraded / hosts_incomplete from doubling, and what
# lets a tail that legitimately ran out of its time budget be reported as
# `hosts_budget_truncated` — an operator-chosen tradeoff, not degraded
# coverage — instead of raising a false "coverage degraded" finding.

def test_a_two_summary_host_counts_once():
    result = {"scan_metrics": [
        {"target": "10.0.0.5", "health": "ok", "complete": True,
         "missing": 0, "local_resource_errors": 0},
        {"target": "10.0.0.5", "health": "ok", "complete": True,
         "missing": 0, "local_resource_errors": 0},
    ]}
    s = scan_health_summary(result)
    assert s["hosts_measured"] == 1
    assert s["hosts_degraded"] == 0
    assert s["hosts_incomplete"] == 0
    assert s["should_warn"] is False


def test_a_budget_exhausted_tail_is_truncated_not_degraded():
    """The only gap on this host is a tail that ran out of its time budget —
    that must NOT count as incomplete/degraded, and must NOT raise the
    coverage-degraded finding (should_warn stays False)."""
    result = {"scan_metrics": [
        {"target": "10.0.0.5", "health": "ok", "complete": True,
         "missing": 0, "local_resource_errors": 0},
        {"target": "10.0.0.5", "health": "ok", "complete": False,
         "missing": 40000, "local_resource_errors": 0, "budget_exhausted": True},
    ]}
    s = scan_health_summary(result)
    assert s["hosts_measured"] == 1
    assert s["hosts_budget_truncated"] == 1
    assert s["hosts_incomplete"] == 0
    assert s["hosts_degraded"] == 0
    assert s["should_warn"] is False
    assert "time budget" in s["reason"]


def test_a_non_budget_gap_still_counts_incomplete():
    """missing > 0 without budget_exhausted is real, unexplained loss — it
    must still raise incomplete/should_warn, even if the SAME host also has
    a separate, legitimately budget-truncated summary."""
    result = {"scan_metrics": [
        {"target": "10.0.0.5", "health": "ok", "complete": False,
         "missing": 12, "local_resource_errors": 0},
        {"target": "10.0.0.5", "health": "ok", "complete": False,
         "missing": 40000, "local_resource_errors": 0, "budget_exhausted": True},
    ]}
    s = scan_health_summary(result)
    assert s["hosts_measured"] == 1
    assert s["hosts_incomplete"] == 1
    assert s["hosts_budget_truncated"] == 0
    assert s["should_warn"] is True


def test_a_legacy_entry_without_target_falls_back_to_per_entry_counting():
    """Older probes never stamped a target — those entries keep the
    pre-F3 behavior of one-entry-one-host, unaffected by grouping."""
    result = {"scan_metrics": [
        {"health": "ok", "complete": True, "missing": 0, "local_resource_errors": 0},
        {"health": "ok", "complete": True, "missing": 0, "local_resource_errors": 0},
    ]}
    s = scan_health_summary(result)
    assert s["hosts_measured"] == 2
    assert s["hosts_degraded"] == 0
    assert s["hosts_incomplete"] == 0


def test_targeted_and_legacy_entries_both_count_in_the_same_result():
    result = {"scan_metrics": [
        {"target": "10.0.0.5", "health": "ok", "complete": True,
         "missing": 0, "local_resource_errors": 0},
        {"target": "10.0.0.5", "health": "ok", "complete": True,
         "missing": 0, "local_resource_errors": 0},
        {"health": "degraded", "complete": True, "missing": 0,
         "local_resource_errors": 1},
    ]}
    s = scan_health_summary(result)
    assert s["hosts_measured"] == 2          # one grouped host + one legacy entry
    assert s["hosts_degraded"] == 1
