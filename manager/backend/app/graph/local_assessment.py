"""Bounded local alternatives and typed, read-only counterfactual evaluation."""

import hashlib
import json
from datetime import timezone
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field

from app.graph.assessment_state import GoalAssessment, summarize_goal
from app.graph.local_rule import (
    ContractModel,
    LocalProof,
    LocalRuleInput,
    RuleBindingError,
    ScopedRecord,
    evaluate_local_data_read,
)


class RouteOutcome(ContractModel):
    finding_id: UUID
    status: Literal[
        "supported", "blocked", "missing_prerequisites", "conflicted", "stale"
    ]
    reason_code: str
    proof: LocalProof | None = None
    signature: str | None = None


class LocalAssessment(ContractModel):
    goal: GoalAssessment
    routes: tuple[RouteOutcome, ...]
    display_limited: bool


class RequireAuthentication(ScopedRecord):
    kind: Literal["require_datastore_authentication"] = (
        "require_datastore_authentication"
    )
    service_id: UUID
    service_instance_ref: str


class ActionComparison(ContractModel):
    realization: Literal["simulated_only"] = "simulated_only"
    before: LocalAssessment
    after: LocalAssessment
    action: RequireAuthentication
    verification_required: tuple[str, ...] = (
        "Confirm authentication is required on the same datastore listener.",
        "Recollect reachability and access evidence under the original entry scenario.",
        "Recompute with comparable collection coverage and rule versions.",
    )


def proof_signature(proof: LocalProof) -> str:
    data = proof.model_copy(update={"as_of": proof.as_of.astimezone(timezone.utc)})
    return hashlib.sha256(data.model_dump_json().encode()).hexdigest()


def _input_signature(value: LocalRuleInput) -> str:
    data = value.model_dump(mode="json")
    data["as_of"] = value.as_of.astimezone(timezone.utc).isoformat()
    for item, evidence in zip(data["evidence"], value.evidence):
        item["observed_at"] = evidence.observed_at.astimezone(timezone.utc).isoformat()
        item["valid_until"] = evidence.valid_until.astimezone(timezone.utc).isoformat()
    for key in ("assertions", "evidence"):
        data[key].sort(key=lambda r: r["id"])
    for assertion in data["assertions"]:
        assertion["evidence_ids"].sort()
    data["finding"]["evidence_ids"].sort()
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def evaluate_local_alternatives(
    inputs: tuple[LocalRuleInput, ...],
    *,
    coverage: Literal["complete", "partial"] = "partial",
    max_applications: Annotated[int, Field(gt=0)] = 1000,
    display_limit: int = 20,
    _action: RequireAuthentication | None = None,
) -> LocalAssessment:
    """All inputs must describe one actor/scenario/asset goal at one as-of.

    Limits apply before evaluating a bundle. Local rules have fixed finite
    prerequisites, no recursive capability creation and no route-tree expansion.
    """
    if not 1 <= max_applications <= 10000 or not 1 <= display_limit <= 1000:
        raise ValueError("invalid assessment budget")
    if coverage not in ("complete", "partial"):
        raise ValueError("invalid collection coverage")
    if len(inputs) > 10000:
        raise ValueError("input_bundle_limit_exceeded")
    if inputs:
        first = inputs[0]
        key = (
            first.tenant_id,
            first.engagement_id,
            first.entry,
            first.asset,
            first.as_of,
        )
        if any(
            (x.tenant_id, x.engagement_id, x.entry, x.asset, x.as_of) != key
            for x in inputs
        ):
            raise ValueError("incompatible_goal_or_scenario")
    routes = []
    signatures = set()
    seen_inputs = set()
    canonical_by_identity = {}

    def canonical_input(value):
        # The retained immutable input tuple keeps identities stable for this
        # evaluation. Avoid serializing the same object on every duplicate.
        identity = id(value)
        if identity not in canonical_by_identity:
            canonical_by_identity[identity] = _input_signature(value)
        return canonical_by_identity[identity]

    processed = 0
    for value in inputs:
        # Normalize order before deduplicating bundles; duplicates cannot consume
        # the frontier budget or inflate exposure counts.
        canonical = canonical_input(value)
        if canonical in seen_inputs:
            continue
        if processed == max_applications:
            break
        seen_inputs.add(canonical)
        processed += 1
        try:
            proof = evaluate_local_data_read(value)
            if _action is not None and (
                value.tenant_id,
                value.engagement_id,
                value.service.id,
                value.service.instance_ref,
            ) == (
                _action.tenant_id,
                _action.engagement_id,
                _action.service_id,
                _action.service_instance_ref,
            ):
                routes.append(
                    RouteOutcome(
                        finding_id=value.finding.id,
                        status="blocked",
                        reason_code="simulated_authentication_required",
                    )
                )
                continue
            signature = proof_signature(proof)
            if signature in signatures:
                continue
            signatures.add(signature)
            routes.append(
                RouteOutcome(
                    finding_id=value.finding.id,
                    status="supported",
                    reason_code="supported_derivation_exists",
                    proof=proof,
                    signature=signature,
                )
            )
        except RuleBindingError as exc:
            if exc.code == "premise_not_supported":
                truths = {a.truth for a in value.assertions}
                # Positive-read evidence cannot also prove an authoritative
                # negative access fact. Negative evidence gets its own later
                # contract; only a typed simulation below may mark a route blocked.
                status = (
                    "conflicted" if "conflicted" in truths else "missing_prerequisites"
                )
            elif exc.code == "evidence_not_current":
                status = "stale"
            else:
                status = "missing_prerequisites"
            routes.append(
                RouteOutcome(
                    finding_id=value.finding.id, status=status, reason_code=exc.code
                )
            )
    # A consumed budget with remaining unique inputs is explicitly truncated.
    remaining = any(canonical_input(x) not in seen_inputs for x in inputs)
    goal = summarize_goal(
        tuple(r.status for r in routes),
        compute="truncated" if remaining else "complete",
        coverage=coverage,
    )
    routes.sort(
        key=lambda r: (
            r.status != "supported",
            str(r.finding_id),
            r.signature or r.reason_code,
        )
    )
    return LocalAssessment(
        goal=goal,
        routes=tuple(routes[:display_limit]),
        display_limited=len(routes) > display_limit,
    )


def compare_authentication_action(
    inputs: tuple[LocalRuleInput, ...],
    action: RequireAuthentication,
    *,
    coverage: Literal["complete", "partial"] = "partial",
    max_applications: int = 1000,
) -> ActionComparison:
    if not inputs:
        raise ValueError("action_requires_a_bound_assessment")
    if any(
        (x.tenant_id, x.engagement_id) != (action.tenant_id, action.engagement_id)
        for x in inputs
    ):
        raise ValueError("action_scope_mismatch")
    if not any(
        (x.service.id, x.service.instance_ref)
        == (action.service_id, action.service_instance_ref)
        for x in inputs
    ):
        raise ValueError("action_listener_not_in_assessment")
    return ActionComparison(
        before=evaluate_local_alternatives(
            inputs, coverage=coverage, max_applications=max_applications
        ),
        after=evaluate_local_alternatives(
            inputs, coverage=coverage, max_applications=max_applications, _action=action
        ),
        action=action,
    )
