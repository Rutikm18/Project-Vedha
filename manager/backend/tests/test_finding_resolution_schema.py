from __future__ import annotations

from app.models.finding import Finding


def test_finding_has_resolution_lifecycle_columns():
    cols = Finding.__table__.columns
    for name in (
        "resolution_miss_count", "resolved_at", "resolution_method",
        "resolution_run_id", "reopened_count", "detected_db_version",
    ):
        assert name in cols, f"missing column {name}"
    assert cols["resolution_miss_count"].nullable is False
    assert cols["reopened_count"].nullable is False
    assert cols["detected_db_version"].nullable is True
    assert cols["resolved_at"].nullable is True
