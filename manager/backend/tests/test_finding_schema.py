from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.finding import FindingPatch, FindingSummary


def test_finding_patch_accepts_documented_maximum_risk_score():
    patch = FindingPatch(risk_score=Decimal("1000"))

    assert patch.risk_score == Decimal("1000")


def test_finding_patch_rejects_risk_score_above_scale():
    with pytest.raises(ValidationError):
        FindingPatch(risk_score=Decimal("1000.01"))


def test_finding_summary_exposes_full_open_severity_breakdown():
    summary = FindingSummary(
        total=12,
        open_total=8,
        critical_open=1,
        high_open=2,
        medium_open=3,
        low_open=1,
        info_open=1,
        validated=4,
        blind=2,
        average_risk=475,
    )

    assert (
        summary.critical_open
        + summary.high_open
        + summary.medium_open
        + summary.low_open
        + summary.info_open
    ) == summary.open_total
