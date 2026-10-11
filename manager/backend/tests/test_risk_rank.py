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


def test_distinct_high_risks_do_not_collapse_at_the_ceiling():
    common = dict(
        severity="critical",
        kev=True,
        exploit_validated=True,
        verification_state="confirmed",
        confidence=100,
        asset_criticality="critical",
        internet_facing=True,
        auth_enforced=False,
    )
    maximum = compute_risk_rank(cvss_score=10.0, epss_score=1.0, **common)
    elevated = compute_risk_rank(cvss_score=9.0, epss_score=0.3, **common)

    assert elevated < maximum
    assert maximum == 1000


def test_severity_remains_an_impact_signal_without_cvss():
    critical = _rank(severity="critical", cvss_score=None)
    medium = _rank(severity="medium", cvss_score=None)

    assert critical > medium


_SEVERITIES = ("info", "low", "medium", "high", "critical")


def test_severity_is_a_hard_band_best_case_lower_never_beats_worst_case_higher():
    """M3: a Medium with every amplifier maxed must not outrank a Critical with none."""
    best = dict(cvss_score=None, epss_score=1.0, kev=True, exploit_validated=True,
                verification_state="confirmed", confidence=100, asset_criticality="critical",
                internet_facing=True, auth_enforced=False)
    worst = dict(cvss_score=None, epss_score=0.0, kev=False, exploit_validated=False,
                 verification_state="contradicted", confidence=0, asset_criticality="low",
                 internet_facing=False, auth_enforced=True)
    for lower, higher in zip(_SEVERITIES, _SEVERITIES[1:]):
        assert compute_risk_rank(severity=lower, **best) < compute_risk_rank(severity=higher, **worst)


def test_band_ordering_holds_with_cvss_present():
    medium_hot = _rank(severity="medium", cvss_score=10.0, epss_score=1.0, kev=True,
                       verification_state="confirmed", internet_facing=True)
    critical_cold = _rank(severity="critical", cvss_score=0.0, epss_score=0.0,
                          verification_state="contradicted", internet_facing=False,
                          auth_enforced=True, asset_criticality="low", confidence=0)
    assert medium_hot < critical_cold


def test_within_a_band_context_still_orders():
    assert _rank(severity="high", internet_facing=True) > _rank(severity="high", internet_facing=False)


def test_unknown_severity_is_treated_as_info():
    assert _rank(severity="bogus", cvss_score=None) <= 99
