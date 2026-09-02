"""Regression tests for posture findings entering the Manager risk contract."""

from app.detection.prioritization import _posture_risk_on_manager_scale


def test_upstream_posture_score_cannot_force_the_manager_ceiling():
    base = {
        "rule_id": "POSTURE-SMB",
        "severity": "critical",
        "state": "confirmed",
        "confidence": 90,
    }
    assert _posture_risk_on_manager_scale({**base, "risk_score": 100}) < 1000.0
    assert _posture_risk_on_manager_scale({**base, "risk_score": 1}) == \
        _posture_risk_on_manager_scale({**base, "risk_score": 100})


def test_posture_severity_and_evidence_drive_manager_risk():
    critical = _posture_risk_on_manager_scale({
        "rule_id": "POSTURE-SMB", "severity": "critical",
        "state": "confirmed", "confidence": 95,
    })
    medium = _posture_risk_on_manager_scale({
        "rule_id": "POSTURE-TLS", "severity": "medium",
        "state": "inferred", "confidence": 50,
    })
    assert critical is not None and medium is not None and critical > medium


def test_only_detection_engine_posture_evidence_uses_the_boundary_conversion():
    assert _posture_risk_on_manager_scale({"risk_score": 90}) is None
    assert _posture_risk_on_manager_scale({"rule_id": "POSTURE-SMB"}) is None
