from __future__ import annotations

from app.models.finding import Finding


def test_finding_has_verification_columns():
    cols = Finding.__table__.columns
    for name in (
        "verification_state", "verification_confidence",
        "verification_rationale", "needs_review", "verification_method",
    ):
        assert name in cols, f"missing column {name}"
    assert cols["needs_review"].nullable is False
    assert cols["verification_state"].nullable is True
