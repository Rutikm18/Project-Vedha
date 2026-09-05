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


def test_skipped_scanner_is_not_reported_as_degraded():
    """A scanner that stood down because the service isn't on the host is NOT
    degraded. Bucketing the two together made a healthy full run report ten
    "degraded" scanners, which reads as a broken pipeline to the operator."""
    scanner_runs = [
        {"id": "port_scan", "status": "completed"},
        {"id": "smb_scan", "status": "failed"},
        {"id": "db_scan", "status": "skipped",
         "skip_reason": "No eligible target or service was observed."},
        {"id": "dns_scan", "status": "skipped",
         "skip_reason": "No eligible target or service was observed."},
    ]
    cov = build_coverage(scanner_runs, [{"scanner": "port_scan", "target": "10.0.0.5"}])

    # Degraded means genuinely degraded — only the failed scanner qualifies.
    assert cov["scanners_degraded"] == ["smb_scan"]
    # Skipped is its own, separately reportable state.
    assert cov["scanners_skipped"] == ["db_scan", "dns_scan"]
    assert cov["scanners_completed"] == ["port_scan"]


def test_skipped_scanner_still_proves_nothing_about_coverage():
    """Splitting the label must NOT loosen auto-resolution. A skipped scanner is
    still not proof we looked, so its facts never mark an asset covered."""
    scanner_runs = [
        {"id": "tls_scan", "status": "completed"},
        {"id": "smb_scan", "status": "skipped"},
    ]
    facts = [
        {"scanner": "tls_scan", "target": "10.0.0.5:443"},
        {"scanner": "smb_scan", "target": "10.0.0.6:445"},   # skipped → NOT covered
    ]
    cov = build_coverage(scanner_runs, facts)
    assert cov["assets"] == ["10.0.0.5"]
