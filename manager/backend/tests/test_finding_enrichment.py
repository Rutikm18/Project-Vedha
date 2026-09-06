"""Enrichment exposure: FindingOut light fields (list) + detail_enrichment (detail).

Pins the list-light / detail-heavy split — every response carries the cheap
maturity/active badges, but the heavy prose + compliance only appear when the
detail path assembles them — and that overrides win over the KB.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.schemas.finding import FindingOut
from app.services.finding_enrichment import detail_enrichment


def _out(**kw) -> FindingOut:
    data = dict(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=None, cve_ids=[],
        title="t", description=None, cvss_score=None, cvss_vector=None,
        epss_score=None, risk_score=None, severity=FindingSeverity.high,
        status=FindingStatus.open, exploitable=False, exploit_validated=False,
        mitre_techniques=[], detection_status=DetectionStatus.detected, evidence={},
        remediation=None, created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    data.update(kw)
    return FindingOut(**data)


def _finding(**kw):
    base = dict(
        title="", description="", remediation="", cve_ids=[], evidence={},
        cvss_score=None, epss_score=None, exploit_validated=False,
        severity=FindingSeverity.high, content_overrides=None,
    )
    base.update(kw)
    return SimpleNamespace(**base)


# ── list-light: every FindingOut carries the cheap badges ──────────────────────

def test_findingout_computes_maturity_and_active_from_evidence():
    out = _out(evidence={"kev": True})
    assert out.exploit_maturity == "WEAPONIZED"
    assert out.actively_exploited is True


def test_findingout_defaults_to_theoretical_when_no_signal():
    out = _out(evidence={})
    assert out.exploit_maturity == "THEORETICAL"
    assert out.actively_exploited is False


def test_findingout_list_leaves_heavy_prose_null():
    out = _out(evidence={"kev": True})
    # Heavy fields are detail-only — never populated by list serialization.
    assert out.technical_details is None
    assert out.business_impact is None
    assert out.impact is None
    assert out.compliance is None
    assert out.evidence_summary is None


# ── detail-heavy: detail_enrichment fills everything ───────────────────────────

def test_detail_enrichment_populates_all_sections():
    fields = detail_enrichment(_finding(title="RDP exposed on 3389",
                                        evidence={"kev": True, "port": 3389}))
    assert fields["technical_details"].strip()
    assert fields["business_impact"].strip()
    assert fields["impact"].strip()
    assert fields["exploitation"]["note"].strip()
    assert fields["exploit_maturity"] == "WEAPONIZED"
    assert fields["actively_exploited"] is True
    assert len(fields["compliance"]) == 5
    assert any(f["label"] == "Port" for f in fields["evidence_summary"])


def test_detail_enrichment_scales_business_impact_by_criticality():
    low = detail_enrichment(_finding(title="RDP exposed"), asset_criticality="low")
    crit = detail_enrichment(_finding(title="RDP exposed"), asset_criticality="critical")
    assert len(crit["business_impact"]) > len(low["business_impact"])


def test_detail_enrichment_honours_content_overrides():
    fields = detail_enrichment(_finding(
        title="RDP exposed",
        content_overrides={"business_impact": "Board-level custom impact statement."},
    ))
    assert fields["business_impact"] == "Board-level custom impact statement."
    # Non-overridden prose still comes from the KB.
    assert fields["technical_details"].strip()


def test_detail_enrichment_survives_missing_evidence():
    fields = detail_enrichment(_finding(title="weird thing", evidence=None))
    assert fields["evidence_summary"] == []
    assert len(fields["compliance"]) == 5
