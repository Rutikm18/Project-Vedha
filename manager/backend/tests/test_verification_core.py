from __future__ import annotations

from app.detection.verification import VERIFICATION_STATES, compute_verdict


def test_authoritative_is_confirmed():
    v = compute_verdict({"source_confidence": "authoritative", "state": "confirmed",
                         "confidence": 95})
    assert v.state == "confirmed"
    assert v.confidence == 95
    assert v.needs_review is False


def test_high_confidence_inferred_is_corroborated():
    v = compute_verdict({"source_confidence": "inferred", "state": "suspected",
                         "confidence": 80, "checks": {}})
    assert v.state == "corroborated"


def test_low_confidence_inferred_is_inferred():
    v = compute_verdict({"source_confidence": "inferred", "state": "potential",
                         "confidence": 35, "checks": {}})
    assert v.state == "inferred"


def test_kev_suspected_finding_needs_review():
    v = compute_verdict({"source_confidence": "inferred", "state": "suspected",
                         "confidence": 55, "kev": True, "priority": "high"})
    assert v.needs_review is True
    assert v.state in VERIFICATION_STATES


def test_missing_confidence_defaults_to_inferred_not_crash():
    v = compute_verdict({"source_confidence": "inferred", "state": "suspected"})
    assert v.state in VERIFICATION_STATES
    assert isinstance(v.confidence, int)
