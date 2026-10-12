import json
from pathlib import Path
from uuid import UUID

import pytest

from app.graph.local_assessment import (
    RequireAuthentication,
    compare_authentication_action,
    evaluate_local_alternatives,
)
from app.graph.local_rule import LocalRuleInput


@pytest.fixture
def payload():
    p = (
        Path(__file__).resolve().parents[3]
        / "docs/planning/2026-10-13-attack-path-local-rule.example.json"
    )
    return json.loads(p.read_text())


def alternate(payload):
    data = json.loads(json.dumps(payload))
    # Same goal/entry, independent listener and supporting records.
    for field in ("service", "finding"):
        data[field]["id"] = str(UUID(int=UUID(data[field]["id"]).int + 100))
    data["service"]["instance_ref"] = "synthetic:second-listener"
    data["service"]["port"] = 6380
    data["finding"]["service_id"] = data["service"]["id"]
    for record in data["assertions"] + data["evidence"]:
        record["id"] = str(UUID(int=UUID(record["id"]).int + 100))
        record["target_id"] = data["service"]["id"]
        record["service_instance_ref"] = data["service"]["instance_ref"]
        record["port"] = 6380
    for record in data["assertions"] + [data["finding"]]:
        record["evidence_ids"] = [
            str(UUID(int=UUID(i).int + 100)) for i in record["evidence_ids"]
        ]
    return LocalRuleInput.model_validate(data)


def action(value):
    return RequireAuthentication(
        tenant_id=value.tenant_id,
        engagement_id=value.engagement_id,
        service_id=value.service.id,
        service_instance_ref=value.service.instance_ref,
    )


def test_duplicate_inputs_do_not_consume_budget_or_inflate_exposure(payload):
    value = LocalRuleInput.model_validate(payload)
    result = evaluate_local_alternatives((value, value, value), max_applications=1)
    assert result.goal.supported_proofs == 1
    assert result.goal.compute == "complete"


def test_display_limit_does_not_change_complete_goal_result(payload):
    values = (LocalRuleInput.model_validate(payload), alternate(payload))
    result = evaluate_local_alternatives(values, display_limit=1)
    assert result.goal.supported_proofs == 2
    assert result.goal.compute == "complete"
    assert len(result.routes) == 1
    assert result.display_limited


def test_compute_limit_keeps_valid_support_and_marks_truncation(payload):
    values = (LocalRuleInput.model_validate(payload), alternate(payload))
    result = evaluate_local_alternatives(values, max_applications=1)
    assert result.goal.state == "supported"
    assert result.goal.compute == "truncated"


def test_wrong_scenario_cannot_compose(payload):
    value = LocalRuleInput.model_validate(payload)
    payload["entry"]["context_ref"] = "assumed-internal-administrator"
    with pytest.raises(ValueError, match="incompatible_goal_or_scenario"):
        evaluate_local_alternatives((value, LocalRuleInput.model_validate(payload)))


def test_intervention_preserves_independent_surviving_listener(payload):
    value = LocalRuleInput.model_validate(payload)
    result = compare_authentication_action(
        (value, alternate(payload)), action(value), coverage="complete"
    )
    assert result.before.goal.supported_proofs == 2
    assert result.after.goal.supported_proofs == 1
    assert result.after.goal.state == "supported"
    assert result.realization == "simulated_only"
    assert result.verification_required
    assert result.after.routes[1].reason_code == "simulated_authentication_required"
    assert value.assertions[1].truth == "supported_true"


def test_intervention_complete_local_model_is_still_only_a_model_claim(payload):
    value = LocalRuleInput.model_validate(payload)
    result = compare_authentication_action((value,), action(value), coverage="complete")
    assert result.after.goal.state == "not_derived_in_declared_model"
    assert result.after.routes[0].status == "blocked"


def test_missing_coverage_after_action_is_indeterminate(payload):
    value = LocalRuleInput.model_validate(payload)
    assert (
        compare_authentication_action((value,), action(value)).after.goal.state
        == "indeterminate"
    )


def test_false_read_assertion_is_not_authoritative_negative_proof(payload):
    payload["assertions"][1]["truth"] = "supported_false"
    result = evaluate_local_alternatives(
        (LocalRuleInput.model_validate(payload),), coverage="complete"
    )
    assert result.goal.state == "indeterminate"
    assert result.routes[0].status == "missing_prerequisites"


def test_simulation_cannot_repair_an_invalid_input_into_safe_claim(payload):
    payload["assertions"][1]["target_id"] = payload["asset"]["id"]
    value = LocalRuleInput.model_validate(payload)
    result = compare_authentication_action((value,), action(value), coverage="complete")
    assert result.after.goal.state == "indeterminate"


def test_foreign_or_unbound_action_rejected(payload):
    value = LocalRuleInput.model_validate(payload)
    foreign = action(value).model_copy(update={"tenant_id": UUID(int=999)})
    with pytest.raises(ValueError, match="action_scope_mismatch"):
        compare_authentication_action((value,), foreign)
    other = action(value).model_copy(update={"service_instance_ref": "old-listener"})
    with pytest.raises(ValueError, match="action_listener_not_in_assessment"):
        compare_authentication_action((value,), other)


@pytest.mark.parametrize("budget", [0, -1, 10001])
def test_invalid_budgets_rejected(payload, budget):
    with pytest.raises(ValueError, match="invalid assessment budget"):
        evaluate_local_alternatives(
            (LocalRuleInput.model_validate(payload),), max_applications=budget
        )


def test_many_repeated_bundles_exceed_input_bound(payload):
    value = LocalRuleInput.model_validate(payload)
    with pytest.raises(ValueError, match="input_bundle_limit_exceeded"):
        evaluate_local_alternatives((value,) * 10001)
