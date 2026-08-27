import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
    # P2 passive verification verdict (normalized, dashboard-facing).
    verification_state: str | None = None
    verification_confidence: int | None = None
    verification_rationale: str | None = None
    needs_review: bool = False
    # P1 resolution lifecycle (auto-resolution / manual reopen surfacing).
    resolution_method: str | None = None
    reopened_count: int = 0
    resolved_at: datetime | None = None
    # P4 unified priority (computed; see services/risk_rank.py).
    risk_rank: int | None = None
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
                kev=bool(ev.get("kev")),
                exploit_validated=bool(self.exploit_validated),
                verification_state=self.verification_state,
                confidence=self.verification_confidence,
                asset_criticality=None,
                internet_facing=None,
                auth_enforced=None,
            )
        return self
