"""Phase 3: FindingOut exposes report enrichment (detection_method, verification
retest block, epss_percentile / kev_added_at / internet_reachable) computed at
serialization — no column, no migration."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.finding import FindingOut


def _base(**kw):
    data = dict(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=None, cve_ids=[],
        title="t", description=None, cvss_score=None, cvss_vector=None,
        epss_score=None, risk_score=None, severity=FindingSeverity.high,
        status=FindingStatus.open, exploitable=False, exploit_validated=False,
        mitre_techniques=[], detection_status=DetectionStatus.detected, evidence={},
        remediation=None, verification_state=None, verification_confidence=None,
        needs_review=False, resolution_method=None, reopened_count=0, resolved_at=None,
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
    )
    data.update(kw)
    return FindingOut(**data)


def test_verification_block_always_present_with_pass_criterion():
    out = _base()
    assert out.verification is not None
    assert out.verification["expected"]
    assert out.verification["method"]


def test_weak_tls_gets_a_specific_retest():
    out = _base(title="TLS 1.0 / weak cipher (RC4) supported")
    assert "command" in out.verification
    assert "TLS 1.2" in out.verification["expected"]


def test_detection_method_from_exploit_validated():
    assert _base(exploit_validated=True).detection_method == "exploit"


def test_detection_method_from_verification_state():
    assert _base(verification_state="confirmed").detection_method == "behavioural"


def test_detection_method_none_when_unproven():
    assert _base().detection_method is None


def test_epss_percentile_surfaced_from_evidence():
    assert _base(evidence={"enrichment": {"epss_percentile": 0.97}}).epss_percentile == 0.97
    assert _base(evidence={}).epss_percentile is None


def test_kev_added_at_surfaced_from_evidence():
    assert _base(evidence={"enrichment": {"kev_added": "2024-01-15"}}).kev_added_at == "2024-01-15"


def test_internet_reachable_surfaced_from_evidence():
    assert _base(evidence={"enrichment": {"internet_facing": True}}).internet_reachable is True
    assert _base(evidence={"enrichment": {"internet_facing": False}}).internet_reachable is False
    assert _base(evidence={}).internet_reachable is None


def test_existing_computed_fields_are_unaffected():
    out = _base(exploit_validated=True)
    assert isinstance(out.risk_rank, int)
    assert out.actively_exploited is True
