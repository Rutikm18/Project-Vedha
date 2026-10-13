"""Pure, experimental binding evaluator; no collection, authorization or I/O.

Evaluates one selected local prerequisite bundle. It does not establish global
goal absence, observed compromise, raw evidence truth or production readiness.
"""

from __future__ import annotations

from datetime import datetime
import hashlib
from pathlib import Path
from typing import Annotated, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)


Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
RULE_ID = "LOCAL-DATASTORE-READ"
RULE_VERSION = "binding-contract@1"
RULE_ARTIFACT_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ScopedRecord(ContractModel):
    tenant_id: UUID
    engagement_id: UUID


class Entry(ScopedRecord):
    id: UUID
    kind: Literal["external_actor"] = "external_actor"
    authentication: Literal["unauthenticated"] = "unauthenticated"
    context_ref: Text


class Asset(ScopedRecord):
    id: UUID
    kind: Literal["asset"] = "asset"


class Service(ScopedRecord):
    id: UUID
    kind: Literal["service"] = "service"
    asset_id: UUID
    instance_ref: Text
    protocol: Literal["tcp"]
    port: Annotated[int, Field(strict=True, ge=1, le=65535)]


class ListenerBinding(ScopedRecord):
    subject_id: UUID
    target_id: UUID
    context_ref: Text
    service_instance_ref: Text
    protocol: Literal["tcp"]
    port: Annotated[int, Field(strict=True, ge=1, le=65535)]


class Evidence(ListenerBinding):
    id: UUID
    kind: Literal[
        "entry_service_reachability", "datastore_application_read", "service_metadata"
    ]
    raw_ref: Text
    collector_version: Text
    sha256: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    observed_at: datetime
    valid_until: datetime
    operation_ref: Text | None = None

    @field_validator("observed_at", "valid_until")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("evidence time requires a timezone")
        return value

    @model_validator(mode="after")
    def interval_is_ordered(self) -> Evidence:
        if self.valid_until <= self.observed_at:
            raise ValueError("valid_until must follow observed_at")
        return self


class Finding(ScopedRecord):
    id: UUID
    asset_id: UUID
    service_id: UUID
    lifecycle: Literal["open", "accepted", "remediated", "false_positive"]
    evidence_ids: Annotated[tuple[UUID, ...], Field(min_length=1, max_length=32)]


class Assertion(ListenerBinding):
    id: UUID
    predicate: Literal[
        "service_reachable_from_declared_entry",
        "unauthenticated_datastore_data_read_supported",
    ]
    truth: Literal["supported_true", "supported_false", "unknown", "conflicted"]
    evidence_ids: Annotated[tuple[UUID, ...], Field(min_length=1, max_length=32)]


class LocalRuleInput(ScopedRecord):
    rule_id: Literal["LOCAL-DATASTORE-READ"] = RULE_ID
    rule_version: Literal["binding-contract@1"] = RULE_VERSION
    as_of: datetime
    entry: Entry
    asset: Asset
    service: Service
    finding: Finding
    assertions: Annotated[tuple[Assertion, ...], Field(min_length=2, max_length=2)]
    evidence: Annotated[tuple[Evidence, ...], Field(min_length=1, max_length=32)]

    @field_validator("as_of")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("as_of requires a timezone")
        return value


class LocalProof(ScopedRecord):
    rule_id: Literal["LOCAL-DATASTORE-READ"] = RULE_ID
    rule_version: Literal["binding-contract@1"] = RULE_VERSION
    rule_artifact_sha256: str = RULE_ARTIFACT_SHA256
    as_of: datetime
    actor_id: UUID
    context_ref: Text
    asset_id: UUID
    service_id: UUID
    service_instance_ref: Text
    finding_id: UUID
    capability: Literal["datastore_data_read"] = "datastore_data_read"
    privilege_context: Literal["service_data_read_only"] = "service_data_read_only"
    extent: Literal["observed_operation_only"] = "observed_operation_only"
    realization: Literal["not_observed_chain"] = "not_observed_chain"
    assertion_ids: tuple[UUID, ...]
    evidence_ids: tuple[UUID, ...]
    operation_refs: tuple[str, ...]


class RuleBindingError(ValueError):
    """A selected bundle cannot establish the local rule's fixed effect."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def evaluate_local_data_read(value: LocalRuleInput) -> LocalProof:
    """Return a fixed local effect or reject this selected bundle with a code.

    The caller must supply normalized, independently justified assertions and
    authorized evidence. An error is not a goal-wide 'blocked' verdict.
    """
    records = (
        value.entry,
        value.asset,
        value.service,
        value.finding,
        *value.assertions,
        *value.evidence,
    )
    if any(
        (r.tenant_id, r.engagement_id) != (value.tenant_id, value.engagement_id)
        for r in records
    ):
        raise RuleBindingError("scope_mismatch")
    if len({r.id for r in records}) != len(records):
        raise RuleBindingError("duplicate_record_id")
    if value.service.asset_id != value.asset.id:
        raise RuleBindingError("service_asset_mismatch")
    if (value.finding.asset_id, value.finding.service_id) != (
        value.asset.id,
        value.service.id,
    ):
        raise RuleBindingError("finding_binding_mismatch")
    if value.finding.lifecycle not in ("open", "accepted"):
        raise RuleBindingError("withdrawn_finding")

    by_predicate = {a.predicate: a for a in value.assertions}
    kinds = {
        "service_reachable_from_declared_entry": "entry_service_reachability",
        "unauthenticated_datastore_data_read_supported": "datastore_application_read",
    }
    if set(by_predicate) != set(kinds):
        raise RuleBindingError("missing_required_predicate")
    evidence = {e.id: e for e in value.evidence}
    if len(set(value.finding.evidence_ids)) != len(value.finding.evidence_ids):
        raise RuleBindingError("duplicate_evidence_reference")
    if any(i not in evidence for i in value.finding.evidence_ids):
        raise RuleBindingError("finding_evidence_missing")

    used_evidence: set[UUID] = set()
    operation_refs: set[str] = set()
    for predicate, kind in kinds.items():
        assertion = by_predicate[predicate]
        if (assertion.subject_id, assertion.target_id) != (
            value.entry.id,
            value.service.id,
        ):
            raise RuleBindingError("assertion_entity_mismatch")
        if assertion.context_ref != value.entry.context_ref:
            raise RuleBindingError("scenario_mismatch")
        if (assertion.service_instance_ref, assertion.protocol, assertion.port) != (
            value.service.instance_ref,
            value.service.protocol,
            value.service.port,
        ):
            raise RuleBindingError("listener_mismatch")
        if assertion.truth != "supported_true":
            raise RuleBindingError("premise_not_supported")
        if len(set(assertion.evidence_ids)) != len(assertion.evidence_ids):
            raise RuleBindingError("duplicate_evidence_reference")
        for evidence_id in assertion.evidence_ids:
            record = evidence.get(evidence_id)
            if record is None:
                raise RuleBindingError("assertion_evidence_missing")
            if record.kind != kind:
                raise RuleBindingError("evidence_kind_mismatch")
            if (
                record.subject_id,
                record.target_id,
                record.context_ref,
                record.service_instance_ref,
                record.protocol,
                record.port,
            ) != (
                assertion.subject_id,
                assertion.target_id,
                assertion.context_ref,
                assertion.service_instance_ref,
                assertion.protocol,
                assertion.port,
            ):
                raise RuleBindingError("evidence_binding_mismatch")
            if not record.observed_at <= value.as_of < record.valid_until:
                raise RuleBindingError("evidence_not_current")
            if kind == "datastore_application_read":
                if evidence_id not in value.finding.evidence_ids:
                    raise RuleBindingError("finding_read_evidence_mismatch")
                if record.operation_ref is None:
                    raise RuleBindingError("read_operation_missing")
                operation_refs.add(record.operation_ref)
            used_evidence.add(evidence_id)

    return LocalProof(
        tenant_id=value.tenant_id,
        engagement_id=value.engagement_id,
        as_of=value.as_of,
        actor_id=value.entry.id,
        context_ref=value.entry.context_ref,
        asset_id=value.asset.id,
        service_id=value.service.id,
        service_instance_ref=value.service.instance_ref,
        finding_id=value.finding.id,
        assertion_ids=tuple(sorted((a.id for a in value.assertions), key=str)),
        evidence_ids=tuple(sorted(used_evidence, key=str)),
        operation_refs=tuple(sorted(operation_refs)),
    )
