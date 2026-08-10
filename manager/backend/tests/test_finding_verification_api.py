from __future__ import annotations

from app.schemas.finding import FindingOut


def test_finding_schema_exposes_verification_fields():
    fields = FindingOut.model_fields
    assert "verification_state" in fields
    assert "needs_review" in fields
    assert "verification_confidence" in fields
    assert "verification_rationale" in fields
