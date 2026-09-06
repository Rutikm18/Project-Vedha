from __future__ import annotations

from types import SimpleNamespace

from app.services.finding_content import detection_method
from app.services.verification_kb import verification_for_finding


def F(**kw):
    base = dict(title="", description="", cve_ids=[], exploit_validated=False, verification_state=None)
    base.update(kw)
    return SimpleNamespace(**base)


def test_generic_fallback_always_has_a_pass_criterion():
    v = verification_for_finding(F(title="Some unclassifiable finding"))
    assert v["method"]
    assert v["expected"]


def test_weak_tls_gets_a_specific_retest_with_command():
    v = verification_for_finding(F(title="Weak TLS cipher suite (RC4) offered"))
    assert "command" in v
    assert "TLS 1.2" in v["expected"]


def test_missing_patch_routes_by_cve_when_no_keyword():
    v = verification_for_finding(F(title="Acme Widget flaw", cve_ids=["CVE-2024-9999"]))
    assert "fixed release" in v["expected"]


def test_anon_ftp_retest_attempts_the_login():
    v = verification_for_finding(F(title="Anonymous FTP login permitted"))
    assert "anonymous" in v["command"].lower()


def test_detection_method_from_validation_signals():
    assert detection_method(F(exploit_validated=True)) == "exploit"
    assert detection_method(F(verification_state="confirmed")) == "behavioural"
    assert detection_method(F(verification_state="corroborated")) == "inference"
    assert detection_method(F()) is None


def test_detection_coverage_is_not_consulted():
    # detection_status is blue-team coverage, not proof of how it was established.
    f = F(detection_status="detected")
    assert detection_method(f) is None
