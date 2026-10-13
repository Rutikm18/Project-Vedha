from types import SimpleNamespace

import pytest

from app.graph.snapshot_comparison import compare_readiness


def snapshot(sequence, records=(), **overrides):
    values = dict(
        id=f"snapshot-{sequence}", tenant_id="tenant", engagement_id="engagement",
        request_sequence=sequence, status="completed", normalization_version="v1",
        rule_pack_version="v1", rule_artifact_sha256="digest",
        result_document={"compute": "complete_for_readiness", "assessments": list(records)},
    )
    values.update(overrides)
    return SimpleNamespace(**values)


def test_removal_and_lifecycle_edit_never_verify_remediation():
    old = snapshot(1, [{"finding_id": "a", "lifecycle": "open"}, {"finding_id": "b"}])
    new = snapshot(2, [{"finding_id": "a", "lifecycle": "remediated"}, {"finding_id": "c"}])
    result = compare_readiness(old, new)
    assert result["comparison_state"] == "inconclusive_for_remediation"
    assert [r["change"] for r in result["changes"]] == ["changed", "absent_from_current", "added"]
    assert all(r["verification_state"] == "not_verified" for r in result["changes"])
    assert result["changes"][0]["changed_fields"] == ["lifecycle"]


def test_model_change_and_truncation_are_explicit():
    result = compare_readiness(snapshot(1), snapshot(2, normalization_version="v2", result_document={"compute": "truncated"}))
    assert "model_changed" in result["reasons"]
    assert "computation_incomplete" in result["reasons"]


@pytest.mark.parametrize("overrides,code", [
    ({"tenant_id": "other"}, "scope_mismatch"),
    ({"engagement_id": "other"}, "scope_mismatch"),
    ({"status": "failed"}, "requires_completed"),
    ({"request_sequence": 1}, "requires_earlier"),
])
def test_invalid_comparisons_are_rejected(overrides, code):
    with pytest.raises(ValueError, match=code):
        compare_readiness(snapshot(1), snapshot(2, **overrides))
