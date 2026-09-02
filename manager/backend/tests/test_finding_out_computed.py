"""FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring)."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.finding import FindingAssetContext, FindingOut


def _base(**kw):
    data = dict(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=None, cve_ids=[],
        title="t", description=None, cvss_score=None, cvss_vector=None,
        epss_score=None, risk_score=None, severity=FindingSeverity.high,
        status=FindingStatus.open, exploitable=False, exploit_validated=False,
        mitre_techniques=[], detection_status=DetectionStatus.detected, evidence={},
        remediation=None, verification_state="inferred", verification_confidence=60,
        needs_review=False, resolution_method=None, reopened_count=0, resolved_at=None,
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
    )
    data.update(kw)
    return FindingOut(**data)


def test_risk_rank_is_computed_not_none():
    out = _base()
    assert isinstance(out.risk_rank, int)
    assert 0 <= out.risk_rank <= 1000


def test_confirmed_exploited_outranks_contradicted():
    hot = _base(verification_state="confirmed", exploit_validated=True)
    cold = _base(verification_state="contradicted")
    assert hot.risk_rank > cold.risk_rank


def test_nested_enrichment_kev_is_part_of_the_rank():
    kev = _base(evidence={"enrichment": {"kev": True}})
    ordinary = _base(evidence={"enrichment": {"kev": False}})
    assert kev.risk_rank > ordinary.risk_rank


def test_explicit_risk_rank_is_preserved():
    out = _base(risk_rank=777)
    assert out.risk_rank == 777


def test_lifecycle_fields_round_trip():
    out = _base(resolution_method="auto", reopened_count=2)
    assert out.resolution_method == "auto"
    assert out.reopened_count == 2


def test_detail_asset_context_round_trips_without_changing_list_contract():
    asset = FindingAssetContext(
        id=uuid.uuid4(),
        ip_address="192.0.2.10",
        hostname="edge-01",
        fqdn="edge-01.example.test",
        os="Linux",
        os_version="12",
        asset_type="server",
        criticality="high",
        owner="Platform Engineering",
        environment="production",
    )
    out = _base(asset_id=asset.id, asset_context=asset)
    assert out.asset_context is not None
    assert out.asset_context.fqdn == "edge-01.example.test"
    assert out.asset_context.criticality == "high"
