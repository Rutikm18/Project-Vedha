"""
test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invariant.

"Prove no ports were silently skipped." Count-based completeness can be fooled by
a skip+duplicate pair (attempted still == requested); the SET of ports actually
recorded cannot. Verifies missing/duplicate detection and the strengthened
`complete` property. Pure — no network.
"""
from __future__ import annotations

from main_scripts.port_scanner import ScanMetrics
from main_scripts.scanner_base import ScanResult


def _metrics(requested):
    return ScanMetrics(target="t", vantage="v",
                       ports_requested=len(requested), requested_ports=set(requested))


def _rec(m, port, status="closed"):
    m.record(ScanResult("port_scan", "t", port=port, proto="tcp", status=status))


def test_full_scan_is_complete():
    m = _metrics([1, 2, 3])
    _rec(m, 1, "open"); _rec(m, 2, "closed"); _rec(m, 3, "filtered")
    assert m.complete is True
    assert m.missing_ports == [] and m.duplicate_ports == []
    assert m.classified == 3


def test_missing_port_is_detected():
    m = _metrics([1, 2, 3])
    _rec(m, 1, "open"); _rec(m, 2, "closed")            # 3 never scanned
    assert m.missing_ports == [3]
    assert m.complete is False


def test_duplicate_port_is_detected():
    m = _metrics([1, 2])
    _rec(m, 1, "open"); _rec(m, 1, "closed"); _rec(m, 2, "closed")
    assert m.duplicate_ports == [1]
    assert m.complete is False


def test_skip_plus_duplicate_is_not_falsely_complete():
    # The core fix: counts alone would call this complete (attempted == requested).
    m = _metrics([1, 2, 3])
    _rec(m, 1, "open"); _rec(m, 2, "closed"); _rec(m, 2, "filtered")   # skip 3, dup 2
    assert m.ports_attempted == m.ports_requested == 3     # count-based would say "done"
    assert m.missing_ports == [3] and m.duplicate_ports == [2]
    assert m.complete is False                             # set-based catches it


def test_summary_exposes_missing_and_duplicates():
    m = _metrics([1, 2, 3])
    _rec(m, 1, "open"); _rec(m, 2, "closed"); _rec(m, 2, "filtered")
    d = m.summary()
    assert d["missing"] == 1 and d["missing_ports"] == [3]
    assert d["duplicates"] == 1 and d["duplicate_ports"] == [2]
    assert d["complete"] is False


def test_fallback_count_based_when_no_requested_set():
    # Directly-constructed metrics without a requested set keep the old count invariant.
    m = ScanMetrics(target="t", vantage="v", ports_requested=2)
    _rec(m, 80, "open"); _rec(m, 443, "closed")
    assert m.requested_ports == set()
    assert m.complete is True                              # count-based fallback
