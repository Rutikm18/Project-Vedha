"""Bounded, internal normalized-data engine. HTTP callers cannot submit facts.

Fixed effects are service data-read only. Cross-assessment transfer needs an
explicit credential observation, not a matching IP, subnet, name or CVE.
"""

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator

from app.graph.local_rule import ContractModel

ENGINE_VERSION = "environment-data-read@1"
ENGINE_DIGEST = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


class SystemRef(ContractModel):
    engagement_id: UUID
    asset_id: UUID
    service_id: UUID
    instance_ref: str = Field(min_length=1, max_length=256)
    protocol: Literal["tcp"]
    port: int = Field(strict=True, ge=1, le=65535)


class TransferEvidence(ContractModel):
    id: UUID
    tenant_id: UUID
    environment_id: UUID
    actor_id: UUID
    context_ref: str = Field(min_length=1, max_length=256)
    target: SystemRef
    source: SystemRef | None = None
    identity_ref: str | None = None
    kind: Literal[
        "directed_reachability",
        "unauthenticated_application_read",
        "authenticated_application_read",
        "credential_access",
        "credential_authentication",
    ]
    state: Literal["supported", "unknown", "conflicted"]
    raw_ref: str = Field(min_length=1, max_length=512)
    collector_version: str = Field(min_length=1, max_length=128)
    operation_ref: str | None = Field(default=None, min_length=1, max_length=512)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    observed_at: datetime
    valid_until: datetime
    known_at: datetime

    @field_validator("observed_at", "valid_until", "known_at")
    @classmethod
    def aware(cls, value):
        if value.utcoffset() is None:
            raise ValueError("timezone_required")
        return value


class ReadTransition(ContractModel):
    id: UUID
    rule_id: Literal["unauthenticated_data_read", "credential_backed_data_read"]
    tenant_id: UUID
    environment_id: UUID
    actor_id: UUID
    context_ref: str = Field(min_length=1, max_length=256)
    source: SystemRef | None = None
    target: SystemRef
    identity_ref: str | None = None
    finding_id: UUID
    finding_asset_id: UUID
    finding_service_id: UUID
    finding_lifecycle: Literal["open", "accepted", "remediated", "false_positive"]
    finding_evidence_ids: tuple[UUID, ...] = Field(min_length=1, max_length=16)
    evidence: tuple[TransferEvidence, ...] = Field(max_length=16)


def derive_environment_paths(
    transitions: tuple[ReadTransition, ...],
    *,
    tenant_id: UUID,
    environment_id: UUID,
    engagement_ids: frozenset[UUID],
    as_of: datetime,
    known_at: datetime,
    max_applications: int = 1000,
    max_depth: int = 8,
) -> dict:
    """One actor/context/environment cut; effects never supplied by callers.

    Proofs retain source dependencies. One canonical source proof is selected per
    transition: supported existence is sound; exhaustive alternatives are not
    claimed. Missing inputs and limits never mean no organizational exposure.
    """
    if as_of.utcoffset() is None or known_at.utcoffset() is None:
        raise ValueError("timezone_required")
    if (
        not 1 <= len(engagement_ids) <= 20
        or len(transitions) > 1000
        or not 1 <= max_applications <= 1000
        or not 1 <= max_depth <= 32
    ):
        raise ValueError("environment_budget_exceeded")
    ids = [t.id for t in transitions]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate_transition")
    scenarios = {(t.actor_id, t.context_ref) for t in transitions}
    if len(scenarios) > 1:
        raise ValueError("incompatible_actor_context")
    eligible = []
    outcomes = {}
    evidence_identities = {}
    for t in transitions:
        if (
            t.tenant_id != tenant_id
            or t.environment_id != environment_id
            or t.target.engagement_id not in engagement_ids
            or (t.source and t.source.engagement_id not in engagement_ids)
        ):
            raise ValueError("transition_scope_mismatch")
        reason = None
        read_kind = (
            "unauthenticated_application_read"
            if t.rule_id == "unauthenticated_data_read"
            else "authenticated_application_read"
        )
        required = {"directed_reachability", read_kind}
        if t.rule_id == "unauthenticated_data_read":
            if t.source is not None or t.identity_ref is not None:
                reason = "invalid_entry_rule_binding"
        else:
            required |= {"credential_access", "credential_authentication"}
            if t.source is None or not t.identity_ref or t.source == t.target:
                reason = "explicit_credential_bridge_required"
        if t.finding_lifecycle not in {"open", "accepted"}:
            reason = "finding_withdrawn"
        if (t.finding_asset_id, t.finding_service_id) != (
            t.target.asset_id,
            t.target.service_id,
        ):
            reason = "finding_listener_mismatch"
        if (
            len({e.id for e in t.evidence}) != len(t.evidence)
            or {e.kind for e in t.evidence} != required
            or len(t.evidence) != len(required)
        ):
            reason = "required_evidence_bundle_missing"
        if reason is None and (
            len(set(t.finding_evidence_ids)) != len(t.finding_evidence_ids)
            or any(i not in {e.id for e in t.evidence} for i in t.finding_evidence_ids)
            or not any(
                e.kind == read_kind and e.id in t.finding_evidence_ids
                for e in t.evidence
            )
        ):
            reason = "finding_read_observation_not_cited"
        for e in t.evidence:
            if e.id in evidence_identities and evidence_identities[e.id] != e:
                raise ValueError("evidence_identity_conflict")
            evidence_identities[e.id] = e
            if (
                e.tenant_id,
                e.environment_id,
                e.actor_id,
                e.context_ref,
                e.target,
                e.source,
                e.identity_ref,
            ) != (
                t.tenant_id,
                t.environment_id,
                t.actor_id,
                t.context_ref,
                t.target,
                t.source,
                t.identity_ref,
            ):
                reason = "evidence_binding_mismatch"
            elif e.state != "supported":
                reason = "evidence_" + e.state
            elif (
                e.kind
                in {
                    "unauthenticated_application_read",
                    "authenticated_application_read",
                    "credential_access",
                    "credential_authentication",
                }
                and not e.operation_ref
            ):
                reason = "operation_reference_missing"
            elif (
                not e.observed_at <= as_of < e.valid_until
                or not e.observed_at <= e.known_at <= known_at
            ):
                reason = "evidence_not_current_at_cut"
        if reason:
            outcomes[t.id] = {
                "transition_id": str(t.id),
                "state": "missing_prerequisites",
                "reason": reason,
            }
        else:
            eligible.append(t)
    eligible.sort(key=lambda t: str(t.id))
    proofs = {}
    capabilities = {}
    applications = 0
    while eligible and applications < max_applications:
        changed = False
        for t in tuple(eligible):
            source_proof = capabilities.get(t.source) if t.source else None
            if t.source and source_proof is None:
                continue
            if applications == max_applications:
                break
            applications += 1
            # Reject cycles in the selected derivation, even if an earlier
            # unrelated root supplied support for the same service.
            ancestry = source_proof["systems"] if source_proof else []
            if len(ancestry) >= max_depth:
                outcomes[t.id] = {
                    "transition_id": str(t.id),
                    "state": "missing_prerequisites",
                    "reason": "depth_limit",
                }
                eligible.remove(t)
                continue
            target = t.target.model_dump(mode="json")
            if target in ancestry:
                outcomes[t.id] = {
                    "transition_id": str(t.id),
                    "state": "missing_prerequisites",
                    "reason": "cyclic_derivation",
                }
                eligible.remove(t)
                continue
            proof = {
                "transition_id": str(t.id),
                "finding_id": str(t.finding_id),
                "capability": "service_data_read_only",
                "target": target,
                "source_proof_id": source_proof["transition_id"]
                if source_proof
                else None,
                "evidence_ids": sorted(str(e.id) for e in t.evidence),
                "systems": ancestry + [target],
                "realization": "not_observed_chain",
            }
            proofs[t.id] = proof
            capabilities.setdefault(t.target, proof)
            eligible.remove(t)
            changed = True
        if not changed:
            break
    for t in eligible:
        outcomes[t.id] = {
            "transition_id": str(t.id),
            "state": "missing_prerequisites",
            "reason": "compute_limit"
            if applications == max_applications
            else "source_capability_missing",
        }
    return {
        "engine_version": ENGINE_VERSION,
        "supported_proofs": list(proofs.values()),
        "unresolved": [outcomes[k] for k in sorted(outcomes, key=str)],
        "compute": "truncated"
        if (applications == max_applications and eligible)
        or any(o["reason"] == "depth_limit" for o in outcomes.values())
        else "complete_for_supplied_transitions",
        "coverage": "partial",
        "alternatives": "canonical_source_proof_only",
        "realization": "not_observed_chain",
    }
