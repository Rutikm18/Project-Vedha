"""Seal a normalized local input cut; acquisition consistency is the adapter's job."""

import hashlib
import json
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, field_validator

from app.graph.local_rule import ContractModel, LocalRuleInput, ScopedRecord, Text


class EvidenceRevision(ContractModel):
    evidence_id: UUID
    source_ref: Text
    source_revision: Text
    completed_batch_ref: Text
    ingested_at: datetime

    @field_validator("ingested_at")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("ingested_at requires a timezone")
        return value


class InputCut(ScopedRecord):
    effective_as_of: datetime
    known_at_cutoff: datetime
    captured_at: datetime
    capture_protocol: Literal["materialized_repeatable_read"]
    normalization_version: Text
    rule_artifact_sha256: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    revisions: Annotated[
        tuple[EvidenceRevision, ...], Field(min_length=1, max_length=32)
    ]

    @field_validator("effective_as_of", "known_at_cutoff", "captured_at")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("cut time requires a timezone")
        return value


class SealedInput(ContractModel):
    input_hash: str
    cut: InputCut
    normalized_input: LocalRuleInput


def seal_input(value: LocalRuleInput, cut: InputCut) -> SealedInput:
    if (cut.tenant_id, cut.engagement_id) != (value.tenant_id, value.engagement_id):
        raise ValueError("cut_scope_mismatch")
    if cut.effective_as_of != value.as_of:
        raise ValueError("effective_time_mismatch")
    if cut.known_at_cutoff > cut.captured_at:
        raise ValueError("knowledge_cutoff_after_capture")
    revisions = {r.evidence_id: r for r in cut.revisions}
    if len(revisions) != len(cut.revisions):
        raise ValueError("duplicate_evidence_revision")
    if set(revisions) != {e.id for e in value.evidence}:
        raise ValueError("revision_manifest_mismatch")
    source_revisions = {}
    for record in value.evidence:
        revision = revisions[record.id]
        if revision.ingested_at > cut.known_at_cutoff:
            raise ValueError("evidence_not_known_at_cutoff")
        if record.observed_at > cut.effective_as_of:
            raise ValueError("evidence_from_future")
        key = revision.source_ref
        if (
            key in source_revisions
            and source_revisions[key] != revision.source_revision
        ):
            raise ValueError("mixed_source_revisions")
        source_revisions[key] = revision.source_revision
    normalized = value.model_dump(mode="json")
    normalized["as_of"] = value.as_of.astimezone(timezone.utc).isoformat()
    for item, record in zip(normalized["evidence"], value.evidence):
        item["observed_at"] = record.observed_at.astimezone(timezone.utc).isoformat()
        item["valid_until"] = record.valid_until.astimezone(timezone.utc).isoformat()
    for key in ("assertions", "evidence"):
        normalized[key] = sorted(normalized[key], key=lambda r: r["id"])
    for assertion in normalized["assertions"]:
        assertion["evidence_ids"].sort()
    normalized["finding"]["evidence_ids"].sort()
    manifest = cut.model_dump(mode="json")
    manifest["effective_as_of"] = cut.effective_as_of.astimezone(
        timezone.utc
    ).isoformat()
    manifest["known_at_cutoff"] = cut.known_at_cutoff.astimezone(
        timezone.utc
    ).isoformat()
    for item, revision in zip(manifest["revisions"], cut.revisions):
        item["ingested_at"] = revision.ingested_at.astimezone(timezone.utc).isoformat()
    manifest["revisions"] = sorted(
        manifest["revisions"], key=lambda r: r["evidence_id"]
    )
    # Capture wall time is retained for audit but does not change semantic identity.
    manifest.pop("captured_at")
    encoded = json.dumps(
        {"input": normalized, "manifest": manifest},
        sort_keys=True,
        separators=(",", ":"),
    )
    return SealedInput(
        input_hash=hashlib.sha256(encoded.encode()).hexdigest(),
        cut=cut,
        normalized_input=value,
    )
