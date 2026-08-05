from __future__ import annotations

from datetime import datetime, timezone

from app.services.posture import (
    FindingView, Scores, aggregate, compute_scores, grade_for,
)


def _fv(**kw) -> FindingView:
    base = dict(
        id="f", severity="high", risk_score=None, epss_score=None,
        exploitable=False, exploit_validated=False, asset_criticality=None,
        first_seen=None, last_seen=None,
    )
    base.update(kw)
    return FindingView(**base)


def test_aggregate_is_bounded_and_empty_is_zero():
    assert aggregate([]) == 0.0
    assert 0.0 <= aggregate([0.5, 0.5, 0.9]) <= 100.0
    # noisy-OR: two independent 0.5 → 1-(0.5*0.5)=0.75 → 75.0
    assert aggregate([0.5, 0.5]) == 75.0
    # values clamp to [0,1]
    assert aggregate([5.0]) == 100.0


def test_aggregate_is_monotonic():
    before = aggregate([0.4, 0.4])
    after = aggregate([0.4, 0.4, 0.3])
    assert after >= before


def test_grade_bands():
    assert grade_for(95) == "A"
    assert grade_for(90) == "A"
    assert grade_for(80) == "B"
    assert grade_for(60) == "C"
    assert grade_for(40) == "D"
    assert grade_for(10) == "F"


def test_compute_scores_empty_is_perfect():
    s = compute_scores([])
    assert s == Scores(risk_index=0.0, exploitable_score=0.0, posture_score=100, grade="A")


def test_compute_scores_uses_risk_epss_exploit_and_asset_criticality():
    findings = [
        _fv(risk_score=800, epss_score=0.9, exploit_validated=True, asset_criticality="critical"),
        _fv(risk_score=200, epss_score=0.1, exploitable=True, asset_criticality="low"),
    ]
    s = compute_scores(findings)
    # risk_index = 100*(1-(1-0.8)(1-0.2)) = 100*(1-0.16) = 84.0
    assert s.risk_index == 84.0
    # finding 1 exploit prob = max(0.9,0.6? no,1.0)*1.0 = 1.0 → aggregate saturates to 100
    assert s.exploitable_score == 100.0
    # blend = 0.6*84 + 0.4*100 = 90.4 → posture = round(100-90.4)=10 → grade F
    assert s.posture_score == 10
    assert s.grade == "F"
