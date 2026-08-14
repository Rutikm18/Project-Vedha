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
