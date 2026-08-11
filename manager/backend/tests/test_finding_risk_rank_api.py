from __future__ import annotations

from app.schemas.finding import FindingOut


def test_finding_schema_exposes_risk_rank():
    assert "risk_rank" in FindingOut.model_fields
