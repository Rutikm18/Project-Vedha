import json
from pathlib import Path

import pytest

from app.graph.input_manifest import InputCut, seal_input
from app.graph.local_rule import LocalRuleInput


@pytest.fixture
def input_and_cut():
    p = (
        Path(__file__).resolve().parents[3]
        / "docs/planning/2026-10-13-attack-path-local-rule.example.json"
    )
    value = LocalRuleInput.model_validate_json(p.read_text())
    cut = {
        "tenant_id": str(value.tenant_id),
        "engagement_id": str(value.engagement_id),
        "effective_as_of": "2026-10-13T09:05:00Z",
        "known_at_cutoff": "2026-10-13T09:10:00Z",
        "captured_at": "2026-10-13T09:11:00Z",
        "capture_protocol": "materialized_repeatable_read",
        "normalization_version": "test@1",
        "rule_artifact_sha256": "c" * 64,
        "revisions": [
            {
                "evidence_id": str(e.id),
                "source_ref": "synthetic-import",
                "source_revision": "r1",
                "completed_batch_ref": "batch-1",
                "ingested_at": "2026-10-13T09:01:00Z",
            }
            for e in value.evidence
        ],
    }
    return value, cut


def test_replay_and_order_preserve_identity(input_and_cut):
    value, cut = input_and_cut
    original = seal_input(value, InputCut.model_validate(cut))
    data = value.model_dump(mode="json")
    data["assertions"].reverse()
    data["evidence"].reverse()
    cut["revisions"].reverse()
    cut["captured_at"] = "2026-10-13T09:12:00Z"
    assert (
        seal_input(
            LocalRuleInput.model_validate(data), InputCut.model_validate(cut)
        ).input_hash
        == original.input_hash
    )
    assert (
        seal_input(
            LocalRuleInput.model_validate_json(json.dumps(data)), original.cut
        ).input_hash
        == original.input_hash
    )


@pytest.mark.parametrize(
    "field", ["rule_artifact_sha256", "normalization_version", "known_at_cutoff"]
)
def test_semantic_versions_and_knowledge_cutoff_change_identity(input_and_cut, field):
    value, cut = input_and_cut
    original = seal_input(value, InputCut.model_validate(cut))
    cut[field] = {
        "rule_artifact_sha256": "d" * 64,
        "normalization_version": "test@2",
        "known_at_cutoff": "2026-10-13T09:09:00Z",
    }[field]
    assert (
        seal_input(value, InputCut.model_validate(cut)).input_hash
        != original.input_hash
    )


def test_equivalent_timezone_representation_has_same_identity(input_and_cut):
    value, cut = input_and_cut
    original = seal_input(value, InputCut.model_validate(cut))
    data = value.model_dump(mode="json")
    data["as_of"] = "2026-10-13T10:05:00+01:00"
    data["evidence"][0]["observed_at"] = "2026-10-13T10:00:00+01:00"
    cut["known_at_cutoff"] = "2026-10-13T10:10:00+01:00"
    assert (
        seal_input(
            LocalRuleInput.model_validate(data), InputCut.model_validate(cut)
        ).input_hash
        == original.input_hash
    )


@pytest.mark.parametrize(
    "mutation,reason",
    [
        ("late", "evidence_not_known_at_cutoff"),
        ("mixed", "mixed_source_revisions"),
        ("missing", "revision_manifest_mismatch"),
        ("duplicate", "duplicate_evidence_revision"),
        ("wrong_scope", "cut_scope_mismatch"),
        ("future_cutoff", "knowledge_cutoff_after_capture"),
        ("wrong_as_of", "effective_time_mismatch"),
    ],
)
def test_inconsistent_cut_rejected(input_and_cut, mutation, reason):
    value, cut = input_and_cut
    if mutation == "late":
        cut["revisions"][0]["ingested_at"] = "2026-10-13T09:20:00Z"
    elif mutation == "mixed":
        cut["revisions"][1]["source_revision"] = "r2"
    elif mutation == "missing":
        cut["revisions"].pop()
    elif mutation == "duplicate":
        cut["revisions"][1] = dict(cut["revisions"][0])
    elif mutation == "wrong_scope":
        cut["tenant_id"] = "00000000-0000-4000-8000-000000000099"
    elif mutation == "future_cutoff":
        cut["known_at_cutoff"] = "2026-10-13T09:30:00Z"
    elif mutation == "wrong_as_of":
        cut["effective_as_of"] = "2026-10-13T09:04:00Z"
    with pytest.raises(ValueError, match=reason):
        seal_input(value, InputCut.model_validate(cut))
