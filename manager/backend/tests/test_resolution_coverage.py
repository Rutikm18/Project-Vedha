from __future__ import annotations

from app.detection.resolution import build_coverage, host_of


def test_host_of_strips_single_port():
    assert host_of("10.0.0.5:443") == "10.0.0.5"
    assert host_of("10.0.0.5") == "10.0.0.5"
    assert host_of("") == ""


def test_coverage_counts_only_completed_scanner_observations():
    scanner_runs = [
        {"id": "tls_scan", "status": "completed"},
        {"id": "smb_scan", "status": "degraded"},
    ]
    facts = [
        {"scanner": "tls_scan", "target": "10.0.0.5:443"},   # completed → covered
        {"scanner": "smb_scan", "target": "10.0.0.6:445"},   # degraded → NOT covered
    ]
    cov = build_coverage(scanner_runs, facts)
    assert cov["assets"] == ["10.0.0.5"]
    assert cov["scanners_completed"] == ["tls_scan"]
    assert cov["scanners_degraded"] == ["smb_scan"]


def test_coverage_empty_when_no_scanner_runs():
    # Older probe with no scanner_runs → nothing counts as covered (fail-closed).
    cov = build_coverage(None, [{"scanner": "tls_scan", "target": "10.0.0.5"}])
    assert cov["assets"] == []
