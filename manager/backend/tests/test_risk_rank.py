from __future__ import annotations

from app.services.risk_rank import compute_risk_rank


def _rank(**kw):
    base = dict(severity="high", cvss_score=7.5, epss_score=0.1, kev=False,
                exploit_validated=False, verification_state="inferred",
                confidence=60, asset_criticality="medium",
                internet_facing=False, auth_enforced=False)
    base.update(kw)
    return compute_risk_rank(**base)


def test_bounds():
    assert 0 <= _rank() <= 1000
    assert _rank(severity="critical", cvss_score=10.0, epss_score=0.99, kev=True,
                 exploit_validated=True, verification_state="confirmed",
                 confidence=100, asset_criticality="critical",
                 internet_facing=True, auth_enforced=False) <= 1000


def test_confirmed_exploitable_outranks_contradicted():
    hot = _rank(verification_state="confirmed", exploit_validated=True)
    cold = _rank(verification_state="contradicted")
    assert hot > cold


def test_contradicted_sinks_below_inferred():
    assert _rank(verification_state="contradicted") < _rank(verification_state="inferred")


def test_kev_raises_rank():
    assert _rank(kev=True) > _rank(kev=False)


def test_internet_facing_raises_and_auth_lowers():
    assert _rank(internet_facing=True) > _rank(internet_facing=False)
    assert _rank(auth_enforced=True) < _rank(auth_enforced=False)


def test_low_confidence_lowers_rank():
    assert _rank(confidence=20) < _rank(confidence=95)


def test_missing_optionals_do_not_crash():
    r = compute_risk_rank(severity="low", cvss_score=None, epss_score=None, kev=False,
                          exploit_validated=False, verification_state=None,
                          confidence=None, asset_criticality=None,
                          internet_facing=None, auth_enforced=None)
    assert 0 <= r <= 1000
