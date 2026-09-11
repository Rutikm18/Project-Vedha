"""Phase 2 — doctor: real pass/warn/fail checks with remediation. Pure logic."""
from __future__ import annotations

from agent import doctor as doc


def test_python_version_pass_and_fail():
    assert doc.check_python((3, 12)).status == "pass"
    assert doc.check_python((3, 8)).status == "pass"
    bad = doc.check_python((3, 7))
    assert bad.status == "fail" and "3.8" in bad.remediation


def test_clock_offset_pass_warn_fail():
    assert doc.check_clock(5).status == "pass"
    assert doc.check_clock(200).status == "warn"
    far = doc.check_clock(4000)
    assert far.status == "fail" and "ntp" in far.remediation.lower()


def test_disk_space_check():
    assert doc.check_disk(2 * 1024**3).status == "pass"
    low = doc.check_disk(10 * 1024**2)
    assert low.status == "fail"


def test_connectivity_classification():
    assert doc.classify_connectivity(True, True, True, True).status == "pass"
    dns = doc.classify_connectivity(False, False, False, False)
    assert dns.status == "fail" and "dns" in dns.detail.lower()
    tcp = doc.classify_connectivity(True, False, False, False)
    assert tcp.status == "fail" and "tcp" in tcp.detail.lower()
    tls = doc.classify_connectivity(True, True, False, False)
    assert tls.status == "fail" and "tls" in tls.detail.lower()
    cert = doc.classify_connectivity(True, True, True, False)
    assert cert.status == "fail" and "cert" in cert.detail.lower()


def test_privilege_is_a_note_not_a_failure():
    assert doc.check_privilege(False).status in ("pass", "warn")
    assert doc.check_privilege(True).status == "pass"


def test_exit_code_nonzero_only_on_fail():
    checks = [doc.Check("a", "pass", ""), doc.Check("b", "warn", "")]
    assert doc.exit_code(checks) == 0
    checks.append(doc.Check("c", "fail", ""))
    assert doc.exit_code(checks) != 0


def test_format_report_marks_each_status():
    body = doc.format_report([doc.Check("x", "pass", "ok"), doc.Check("y", "fail", "bad", "fix it")])
    assert "x" in body and "y" in body and "fix it" in body
