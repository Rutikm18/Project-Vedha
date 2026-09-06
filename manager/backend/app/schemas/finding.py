import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.services.finding_content import detection_method as _detection_method
from app.services.finding_content import exploit_maturity as _compute_maturity
from app.services.finding_content import exploitation_signals
from app.services.risk_rank import compute_risk_rank
from app.services.verification_kb import verification_for_finding as _verification_for_finding


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
    # Stored only on the immutable lifecycle event, never on the finding row.
    action_reason: str | None = Field(default=None, max_length=1000)

    @field_validator("action_reason")
    @classmethod
    def normalize_action_reason(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


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
    # Populated on the detail endpoint. List responses intentionally leave this
    # null to keep portfolio reads bounded and avoid an asset N+1 query.
    asset_context: FindingAssetContext | None = None

    # ── Enrichment content (services/finding_content, _compliance, evidence_summary) ──
    # LIGHT fields — computed on EVERY response by the validator below; cheap,
    # evidence-derived, safe to show as list badges.
    exploit_maturity: str | None = None          # WEAPONIZED | POC | THEORETICAL
    actively_exploited: bool = False
    # HEAVY prose — the detail endpoint fills these via finding_enrichment; the LIST
    # deliberately leaves them null so portfolio reads stay bounded (no per-row KB).
    technical_details: str | None = None
    impact: str | None = None
    business_impact: str | None = None
    exploitation: dict | None = None
    evidence_summary: list[dict] | None = None
    compliance: list[dict] | None = None

    # ── Report enrichment (Phase 3) — computed by the validator below; no column.
    # detection_method → report confidence; verification → the retest block (its
    # `expected` is the pass criterion). epss_percentile / kev_added_at /
    # internet_reachable are surfaced from evidence when enrichment recorded them.
    detection_method: str | None = None
    verification: dict | None = None
    epss_percentile: float | None = None
    kev_added_at: str | None = None
    internet_reachable: bool | None = None

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

    @model_validator(mode="after")
    def _populate_enrichment_light(self) -> "FindingOut":
        """Fill the cheap, evidence-derived enrichment badges on every response
        (list + detail) so the maturity / actively-exploited signal is always
        available without the heavier detail-only prose. Detail responses may
        override these via ``model_copy`` after validation — the values agree
        because both read the same signals."""
        signals = exploitation_signals(self)
        if self.exploit_maturity is None:
            self.exploit_maturity = _compute_maturity(signals)
        if not self.actively_exploited:
            self.actively_exploited = bool(signals.get("kev") or signals.get("validated"))
        return self

    @model_validator(mode="after")
    def _populate_report_enrichment(self) -> "FindingOut":
        """Report-facing enrichment, computed on every response (cheap, no DB):
        the detection method (→ confidence) and a deterministic retest block,
        plus EPSS percentile / KEV date / internet exposure surfaced from
        evidence when the enrichment recorded them."""
        if self.detection_method is None:
            self.detection_method = _detection_method(self)
        if self.verification is None:
            self.verification = _verification_for_finding(self)
        ev = self.evidence if isinstance(self.evidence, dict) else {}
        enr = ev.get("enrichment") if isinstance(ev.get("enrichment"), dict) else {}
        if self.epss_percentile is None:
            pct = enr.get("epss_percentile")
            if pct is None:
                pct = ev.get("epss_percentile")
            if pct is not None:
                try:
                    self.epss_percentile = float(pct)
                except (TypeError, ValueError):
                    self.epss_percentile = None
        if self.kev_added_at is None:
            kev_date = (
                enr.get("kev_added") or enr.get("kev_date_added")
                or ev.get("kev_added") or ev.get("kev_date_added")
            )
            self.kev_added_at = str(kev_date) if kev_date else None
        if self.internet_reachable is None:
            reach = enr.get("internet_facing")
            if reach is None:
                reach = ev.get("internet_facing")
            self.internet_reachable = bool(reach) if reach is not None else None
        return self
