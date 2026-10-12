"""Adversarial binding checks for one local effect, without DB or scanners."""

import json
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.graph.local_rule import (
    LocalRuleInput,
    RuleBindingError,
    evaluate_local_data_read,
)


EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "docs/planning/2026-10-13-attack-path-local-rule.example.json"
)


@pytest.fixture
def payload():
    return json.loads(EXAMPLE.read_text())


def derive(payload):
    return evaluate_local_data_read(LocalRuleInput.model_validate(payload))


def test_exact_local_effect_and_bound_provenance(payload):
    proof = derive(payload)
    assert proof.capability == "datastore_data_read"
    assert proof.privilege_context == "service_data_read_only"
    assert proof.extent == "observed_operation_only"
    assert proof.realization == "not_observed_chain"
    assert proof.actor_id == UUID(payload["entry"]["id"])
    assert proof.service_id == UUID(payload["service"]["id"])
    assert proof.asset_id == UUID(payload["asset"]["id"])
    assert set(proof.assertion_ids) == {UUID(a["id"]) for a in payload["assertions"]}
    assert set(proof.evidence_ids) == {UUID(e["id"]) for e in payload["evidence"]}
    assert proof.operation_refs == ("fixture:one-synthetic-application-record-read",)


def test_accepted_risk_still_supports_technical_exposure(payload):
    payload["finding"]["lifecycle"] = "accepted"
    assert derive(payload).capability == "datastore_data_read"


@pytest.mark.parametrize("state", ["remediated", "false_positive"])
def test_withdrawn_finding_cannot_support_effect(payload, state):
    payload["finding"]["lifecycle"] = state
    with pytest.raises(RuleBindingError, match="withdrawn_finding"):
        derive(payload)


@pytest.mark.parametrize("premise", [0, 1])
@pytest.mark.parametrize("state", ["unknown", "supported_false", "conflicted"])
def test_each_and_premise_must_be_supported(payload, premise, state):
    payload["assertions"][premise]["truth"] = state
    with pytest.raises(RuleBindingError, match="premise_not_supported"):
        derive(payload)


@pytest.mark.parametrize("collection", ["assertions", "evidence"])
@pytest.mark.parametrize(
    "field,replacement",
    [
        ("subject_id", "00000000-0000-4000-8000-000000000004"),
        ("target_id", "00000000-0000-4000-8000-000000000004"),
        ("context_ref", "different-principal-session"),
        ("service_instance_ref", "replacement-listener-same-address"),
        ("port", 6380),
    ],
)
def test_mismatched_ground_bindings_rejected(payload, collection, field, replacement):
    payload[collection][1][field] = replacement
    with pytest.raises(RuleBindingError):
        derive(payload)


@pytest.mark.parametrize(
    "record", ["entry", "asset", "service", "finding", "assertion", "evidence"]
)
@pytest.mark.parametrize("field", ["tenant_id", "engagement_id"])
def test_every_record_must_match_declared_scope(payload, record, field):
    if record == "evidence":
        target = payload["evidence"][0]
    elif record == "assertion":
        target = payload["assertions"][0]
    else:
        target = payload[record]
    target[field] = "00000000-0000-4000-8000-000000000099"
    with pytest.raises(RuleBindingError, match="scope_mismatch"):
        derive(payload)


@pytest.mark.parametrize(
    "record,field",
    [("service", "asset_id"), ("finding", "asset_id"), ("finding", "service_id")],
)
def test_service_host_and_finding_binding(payload, record, field):
    payload[record][field] = payload["entry"]["id"]
    with pytest.raises(RuleBindingError):
        derive(payload)


@pytest.mark.parametrize("record", ["entry", "asset", "service"])
def test_entity_kind_cannot_be_relabelled(payload, record):
    payload[record]["kind"] = "principal"
    with pytest.raises(ValidationError):
        derive(payload)


@pytest.mark.parametrize(
    "field,value",
    [
        ("effect", {"capability": "domain_admin"}),
        ("feasibility", "blocked"),
        ("freshness", "stale"),
        ("selected_steps", []),
        ("rule_version", "unreviewed@9"),
    ],
)
def test_caller_cannot_supply_effect_or_summary_verdict(payload, field, value):
    payload[field] = value
    with pytest.raises(ValidationError):
        derive(payload)


def test_metadata_response_does_not_establish_application_read(payload):
    payload["evidence"][1]["kind"] = "service_metadata"
    with pytest.raises(RuleBindingError, match="evidence_kind_mismatch"):
        derive(payload)


def test_data_read_requires_explicit_operation_reference(payload):
    payload["evidence"][1]["operation_ref"] = None
    with pytest.raises(RuleBindingError, match="read_operation_missing"):
        derive(payload)


@pytest.mark.parametrize(
    "field,value",
    [
        ("observed_at", "2026-10-13T09:20:00Z"),
        ("valid_until", "2026-10-13T09:05:00Z"),
    ],
)
def test_future_or_expired_evidence_cannot_support_current_effect(
    payload, field, value
):
    payload["evidence"][0][field] = value
    with pytest.raises(RuleBindingError, match="evidence_not_current"):
        derive(payload)


def test_inverted_interval_is_invalid_before_rule_evaluation(payload):
    payload["evidence"][0]["valid_until"] = "2026-10-13T08:59:00Z"
    with pytest.raises(ValidationError, match="valid_until must follow observed_at"):
        derive(payload)


@pytest.mark.parametrize("record", ["input", "evidence"])
def test_naive_time_rejected(payload, record):
    target = payload if record == "input" else payload["evidence"][0]
    target["as_of" if record == "input" else "observed_at"] = "2026-10-13T09:00:00"
    with pytest.raises(ValidationError, match="timezone"):
        derive(payload)


def test_finding_must_cite_the_actual_read_evidence(payload):
    payload["finding"]["evidence_ids"] = [payload["evidence"][0]["id"]]
    with pytest.raises(RuleBindingError, match="finding_read_evidence_mismatch"):
        derive(payload)


@pytest.mark.parametrize("record", ["finding", "assertion"])
def test_dangling_evidence_reference(payload, record):
    target = payload["finding"] if record == "finding" else payload["assertions"][0]
    target["evidence_ids"] = ["00000000-0000-4000-8000-000000000099"]
    with pytest.raises(RuleBindingError, match="evidence_missing"):
        derive(payload)


@pytest.mark.parametrize("collection", ["assertions", "evidence"])
def test_duplicate_record_identity_rejected(payload, collection):
    payload[collection][1]["id"] = payload[collection][0]["id"]
    with pytest.raises(RuleBindingError, match="duplicate_record_id"):
        derive(payload)


def test_duplicate_predicate_cannot_replace_missing_and_condition(payload):
    payload["assertions"][1]["predicate"] = payload["assertions"][0]["predicate"]
    with pytest.raises(RuleBindingError, match="missing_required_predicate"):
        derive(payload)


def test_duplicated_reference_cannot_inflate_support(payload):
    payload["assertions"][0]["evidence_ids"] *= 2
    with pytest.raises(RuleBindingError, match="duplicate_evidence_reference"):
        derive(payload)


def test_order_does_not_change_proof(payload):
    original = derive(payload)
    payload["assertions"].reverse()
    payload["evidence"].reverse()
    assert derive(payload) == original


def test_wrong_listener_consistently_relabelled_in_assertions_still_rejected(payload):
    for assertion in payload["assertions"]:
        assertion["port"] = 6380
    with pytest.raises(RuleBindingError, match="listener_mismatch"):
        derive(payload)


def test_authenticated_entry_cannot_use_unauthenticated_rule(payload):
    payload["entry"]["authentication"] = "authenticated"
    with pytest.raises(ValidationError):
        derive(payload)


def test_missing_and_premise_is_structurally_invalid(payload):
    payload["assertions"].pop()
    with pytest.raises(ValidationError):
        derive(payload)


@pytest.mark.parametrize(
    "field,value", [("port", True), ("port", 65536), ("protocol", "udp")]
)
def test_listener_types_are_not_coerced_into_support(payload, field, value):
    payload["service"][field] = value
    with pytest.raises(ValidationError):
        derive(payload)


def test_serialized_input_round_trip_preserves_effect(payload):
    value = LocalRuleInput.model_validate(payload)
    decoded = LocalRuleInput.model_validate_json(value.model_dump_json())
    assert evaluate_local_data_read(value) == evaluate_local_data_read(decoded)
