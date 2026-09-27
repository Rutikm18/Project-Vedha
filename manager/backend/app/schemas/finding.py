import uuid
from datetime import datetime
from decimal import Decimal
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.services.risk_rank import compute_risk_rank


class FindingFilter(BaseModel):
    severity: FindingSeverity | None = None
    status: FindingStatus | None = None
    asset_id: uuid.UUID | None = None
    mitre_technique: str | None = None
    engagement_id: uuid.UUID | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class FindingClosureEvidenceArtifact(BaseModel):
    label: str = Field(min_length=1, max_length=200)
    content: Any
    evidence_type: str = Field(min_length=1, max_length=64)
    tool: str | None = Field(default=None, min_length=1, max_length=128)
    source: str | None = Field(default=None, min_length=1, max_length=128)
    command: str | None = Field(default=None, max_length=10_000)
    captured_at: datetime
    captured_by: str = Field(min_length=1, max_length=200)
    source_host: str | None = Field(default=None, min_length=1, max_length=255)
    sha256: str = Field(min_length=64, max_length=64)

    @model_validator(mode="after")
    def validate_provenance(self) -> "FindingClosureEvidenceArtifact":
        if not (self.tool or self.source):
            raise ValueError("closure evidence requires tool or source")
        if self.captured_at.tzinfo is None or self.captured_at.utcoffset() is None:
            raise ValueError("closure evidence captured_at must include a timezone")
        if re.fullmatch(r"[0-9a-fA-F]{64}", self.sha256) is None:
            raise ValueError("closure evidence sha256 must be 64 hexadecimal characters")
        return self


class FindingRetestRecord(BaseModel):
    passed: bool
    requested_at: datetime
    started_at: datetime
    completed_at: datetime
    verified_at: datetime
    tested_by: str = Field(min_length=1, max_length=200)
    verified_by: str = Field(min_length=1, max_length=200)
    scope: dict[str, Any]
    vantage_point: str = Field(min_length=1, max_length=500)
    authentication_context: str = Field(min_length=1, max_length=500)
    method: str = Field(min_length=1, max_length=2_000)
    tool_configuration: dict[str, Any]
    expected_result: str = Field(min_length=1, max_length=5_000)
    actual_result: str = Field(min_length=1, max_length=5_000)
    coverage_comparison: dict[str, Any]
    change_reference: str = Field(min_length=1, max_length=500)
    residual_risk: str = Field(min_length=1, max_length=5_000)
    before_evidence: list[FindingClosureEvidenceArtifact] = Field(min_length=1)
    after_evidence: list[FindingClosureEvidenceArtifact] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_retest(self) -> "FindingRetestRecord":
        times = (
            self.requested_at,
            self.started_at,
            self.completed_at,
            self.verified_at,
        )
        if any(value.tzinfo is None or value.utcoffset() is None for value in times):
            raise ValueError("retest timestamps must include a timezone")
        if any(later < earlier for earlier, later in zip(times, times[1:])):
            raise ValueError("retest timestamps must be chronological")
        if not self.scope:
            raise ValueError("retest scope must not be empty")
        if not self.tool_configuration:
            raise ValueError("retest tool_configuration must not be empty")
        if not self.coverage_comparison:
            raise ValueError("retest coverage_comparison must not be empty")
        return self


class FindingClosurePacket(BaseModel):
    reason: str = Field(min_length=3, max_length=1_000)
    reviewed_by: str = Field(min_length=1, max_length=200)
    retest: FindingRetestRecord


class FindingActionTrackingPatch(BaseModel):
    non_closure_reason: str = Field(min_length=3, max_length=5_000)
    planned_closure_at: datetime
    action_reference: str | None = Field(default=None, min_length=1, max_length=500)

    @field_validator("planned_closure_at")
    @classmethod
    def validate_planned_closure_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("planned_closure_at must include a timezone")
        return value


class FindingPatch(BaseModel):
    """All fields optional — PATCH semantics."""
    status: FindingStatus | None = None
    owner: str | None = None          # mapped to asset.owner or stored in notes
    notes: str | None = None          # appended to remediation field
    exploitable: bool | None = None
    exploit_validated: bool | None = None
    detection_status: DetectionStatus | None = None
    remediation: str | None = None
    cvss_score: Decimal | None = Field(default=None, ge=0, le=10)
    epss_score: Decimal | None = Field(default=None, ge=0, le=1)
    risk_score: Decimal | None = Field(default=None, ge=0, le=1000)
    # Stored only on the immutable lifecycle event, never on the finding row.
    action_reason: str | None = Field(default=None, max_length=1000)
    # A structured, immutable closure packet. It is accepted only with a
    # transition to remediated and is stored on that lifecycle event.
    closure: FindingClosurePacket | None = None
    action_tracking: FindingActionTrackingPatch | None = None

    @field_validator("action_reason")
    @classmethod
    def normalize_action_reason(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None

    @model_validator(mode="after")
    def validate_closure_packet(self) -> "FindingPatch":
        if self.closure is None:
            return self
        if self.status != FindingStatus.remediated:
            raise ValueError("closure packet requires status=remediated")
        if not self.closure.retest.passed:
            raise ValueError("a remediated closure packet requires a passed retest")
        if self.action_reason and self.action_reason != self.closure.reason:
            raise ValueError("action_reason and closure.reason must match")
        return self


class FindingReopen(BaseModel):
    reason: str | None = Field(default=None, max_length=1000)

    @field_validator("reason")
    @classmethod
    def normalize_reason(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class FindingAssetContext(BaseModel):
    id: uuid.UUID
    ip_address: str | None = None
    hostname: str | None = None
    fqdn: str | None = None
    os: str | None = None
    os_version: str | None = None
    asset_type: str
    criticality: str
    owner: str | None = None
    environment: str | None = None


class FindingEventOut(BaseModel):
    """One entry in a finding's lifecycle timeline. `id` is null for synthesized
    events (derived from the finding's columns rather than stored)."""
    id: uuid.UUID | None = None
    event_type: str
    label: str
    actor: str | None = None
    actor_type: str = "system"
    from_status: str | None = None
    to_status: str | None = None
    detail: dict | None = None
    occurred_at: datetime
    synthesized: bool = False


class FindingTimeline(BaseModel):
    finding_id: uuid.UUID
    events: list[FindingEventOut]


class SlaItem(BaseModel):
    finding_id: uuid.UUID
    title: str
    severity: FindingSeverity
    deadline: datetime | None
    hours_remaining: float | None
    hours_total: int | None
    state: str  # breached | at_risk | due_soon | on_track


class SlaSummary(BaseModel):
    breached: int
    at_risk: int
    due_soon: int
    on_track: int
    total_tracked: int
    # The most urgent tracked findings (breached first, then soonest deadline).
    items: list[SlaItem]


class FindingSummary(BaseModel):
    total: int
    open_total: int
    critical_open: int
    high_open: int
    medium_open: int
    low_open: int
    info_open: int
    validated: int
    blind: int
    average_risk: int


class FindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    engagement_id: uuid.UUID
    asset_id: uuid.UUID | None
    cve_ids: list[str] | None
    title: str
    description: str | None
    cvss_score: Decimal | None
    cvss_vector: str | None
    epss_score: Decimal | None
    risk_score: Decimal | None
    severity: FindingSeverity
    status: FindingStatus
    exploitable: bool
    exploit_validated: bool
    mitre_techniques: list[str] | None
    detection_status: DetectionStatus
    evidence: dict | None
    remediation: str | None
    remediation_updated_at: datetime | None = None
    remediation_updated_by: str | None = None
    # Recorded observation provenance. These are distinct from created/updated:
    # updating an analyst note must never look like a new scan observation in a
    # customer report.
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    # Initial is immutable discovery provenance; detection_run_id is latest touch.
    initial_detection_run_id: uuid.UUID | None = None
    detection_run_id: uuid.UUID | None = None
    detected_db_version: str | None = None
    # P2 passive verification verdict (normalized, dashboard-facing).
    verification_state: str | None = None
    verification_confidence: int | None = None
    verification_rationale: str | None = None
    verification_method: str | None = None
    needs_review: bool = False
    # P1 resolution lifecycle (auto-resolution / manual reopen surfacing).
    resolution_method: str | None = None
    resolution_run_id: uuid.UUID | None = None
    resolution_miss_count: int = 0
    reopened_count: int = 0
    resolved_at: datetime | None = None
    # P4 unified priority (computed; see services/risk_rank.py).
    risk_rank: int | None = None
    # Populated on the detail endpoint. List responses intentionally leave this
    # null to keep portfolio reads bounded and avoid an asset N+1 query.
    asset_context: FindingAssetContext | None = None
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def _populate_risk_rank(self) -> "FindingOut":
        """Compute the explainable 0-1000 unified rank at serialization time so
        every findings response carries it (list + detail), without an N+1 asset
        fetch. Asset-context factors (criticality/exposure) are left neutral here;
        the router may pre-set ``risk_rank`` with asset context to override."""
        if self.risk_rank is None:
            ev = self.evidence if isinstance(self.evidence, dict) else {}
            sev = getattr(self.severity, "value", self.severity)
            self.risk_rank = compute_risk_rank(
                severity=str(sev),
                cvss_score=float(self.cvss_score) if self.cvss_score is not None else None,
                epss_score=float(self.epss_score) if self.epss_score is not None else None,
                kev=bool(ev.get("kev") or (ev.get("enrichment") or {}).get("kev")),
                exploit_validated=bool(self.exploit_validated),
                verification_state=self.verification_state,
                confidence=self.verification_confidence,
                asset_criticality=None,
                internet_facing=None,
                auth_enforced=None,
            )
        return self
