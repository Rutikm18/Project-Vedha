"""Regression tests for the Manager's canonical 0-1000 finding risk contract."""

from app.detection.prioritization import _posture_risk_on_manager_scale


def test_posture_risk_is_normalized_once_at_the_manager_boundary():
    assert _posture_risk_on_manager_scale({"rule_id": "POSTURE-SMB", "risk_score": 90}) == 900.0
    assert _posture_risk_on_manager_scale({"rule_id": "POSTURE-TLS", "risk_score": 100}) == 1000.0
    assert _posture_risk_on_manager_scale({"rule_id": "POSTURE-INFO", "risk_score": 1}) == 10.0


def test_only_detection_engine_posture_evidence_uses_the_boundary_conversion():
    assert _posture_risk_on_manager_scale({"risk_score": 90}) is None
    assert _posture_risk_on_manager_scale({"rule_id": "POSTURE-SMB"}) is None
    assert _posture_risk_on_manager_scale({"rule_id": "POSTURE-SMB", "risk_score": "invalid"}) is None
