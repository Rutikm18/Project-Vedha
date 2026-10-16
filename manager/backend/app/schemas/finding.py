import re
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from itertools import pairwise
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.services.evidence_integrity import (
    CANONICAL_SHA256_BASIS,
    verify_canonical_sha256,
)
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
    sha256_basis: str = Field(default=CANONICAL_SHA256_BASIS)

    @model_validator(mode="after")
    def validate_provenance(self) -> "FindingClosureEvidenceArtifact":
        if not (self.tool or self.source):
            raise ValueError("closure evidence requires tool or source")
        if self.captured_at.tzinfo is None or self.captured_at.utcoffset() is None:
            raise ValueError("closure evidence captured_at must include a timezone")
        if re.fullmatch(r"[0-9a-fA-F]{64}", self.sha256) is None:
            raise ValueError("closure evidence sha256 must be 64 hexadecimal characters")
        if self.sha256_basis != CANONICAL_SHA256_BASIS:
            raise ValueError("closure evidence uses an unsupported sha256 basis")
        if verify_canonical_sha256(
            self.content, self.sha256, self.sha256_basis
        ) is not True:
            raise ValueError(
                "closure evidence sha256 must match the canonical recorded content"
            )
        self.sha256 = self.sha256.lower()
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
        if any(later < earlier for earlier, later in pairwise(times)):
            raise ValueError("retest timestamps must be chronological")
        if self.verified_at > datetime.now(timezone.utc):
            raise ValueError("retest timestamps must not be in the future")
        if not self.scope:
            raise ValueError("retest scope must not be empty")
        if not self.tool_configuration:
            raise ValueError("retest tool_configuration must not be empty")
        if not self.coverage_comparison:
            raise ValueError("retest coverage_comparison must not be empty")
        if any(
            self.coverage_comparison.get(key) in (None, "", [], {})
            for key in ("before", "after")
        ):
            raise ValueError(
                "retest coverage_comparison requires before and after values"
            )

        before_times = [item.captured_at for item in self.before_evidence]
        after_times = [item.captured_at for item in self.after_evidence]
        if any(later < earlier for earlier, later in pairwise(before_times)):
            raise ValueError("before evidence capture times must be chronological")
        if any(later < earlier for earlier, later in pairwise(after_times)):
            raise ValueError("after evidence capture times must be chronological")
        if any(value > self.started_at for value in before_times):
            raise ValueError("before evidence must be captured by retest start")
        if any(
            value < self.started_at or value > self.completed_at
            for value in after_times
        ):
            raise ValueError(
                "after evidence must be captured during the retest execution window"
            )
        if max(before_times) > min(after_times):
            raise ValueError("before evidence must precede after evidence")

        before_sources = {
            value.casefold()
            for item in self.before_evidence
            for value in (item.tool, item.source)
            if value
        }
        after_sources = {
            value.casefold()
            for item in self.after_evidence
            for value in (item.tool, item.source)
            if value
        }
        if before_sources.isdisjoint(after_sources):
            raise ValueError(
                "before and after evidence require a common tool or source"
            )
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


class FindingRiskAcceptance(BaseModel):
    """What accepting a risk requires: who answers for it, until when, and what limits the
    exposure meanwhile. Without all three an "accepted" finding is just a hidden one."""
    risk_owner: str = Field(min_length=1, max_length=200)
    expires_at: datetime
    compensating_controls: str = Field(min_length=3, max_length=2_000)

    @field_validator("risk_owner", "compensating_controls")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("expires_at")
    @classmethod
    def expiry_is_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("expires_at must include a timezone")
        return value


class FindingPatch(BaseModel):
    """All fields optional — PATCH semantics."""
    status: FindingStatus | None = None
    owner: str | None = None          # mapped to asset.owner or stored in notes
    assigned_to: uuid.UUID | None = None
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
    closure: FindingClosurePacket | None = None
    action_tracking: FindingActionTrackingPatch | None = None
    # Required when moving a finding to `accepted` (owner + expiry + compensating control).
    risk_acceptance: FindingRiskAcceptance | None = None

    @field_validator("action_reason")
    @classmethod
    def normalize_action_reason(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None

    @model_validator(mode="after")
    def validate_risk_acceptance_scope(self) -> "FindingPatch":
        if self.risk_acceptance is not None and self.status != FindingStatus.accepted:
            raise ValueError("risk_acceptance requires status=accepted")
        return self

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


class FindingAssetOption(BaseModel):
    """One affected asset for the findings IP filter."""
    asset_id: uuid.UUID
    ip_address: str
    hostname: str | None = None
    findings: int


class ScanOption(BaseModel):
    """One scan that produced findings — feeds the findings 'filter by scan'
    control and the compare picker. `findings` counts distinct findings the scan
    touched (new + reaffirmed + resolved), across all its detection runs."""
    job_id: uuid.UUID
    reference: str | None = None
    use_case_id: str | None = None
    intensity: str | None = None
    scanned_at: datetime | None = None
    status: str | None = None
    findings: int


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
    # Who to propose as the accountable owner when a risk on this asset is accepted: the asset's
    # owner, else an owner/team tag. A suggestion the analyst confirms, never applied silently.
    suggested_risk_owner: str | None = None


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


class FindingScanRef(BaseModel):
    """The scan that most recently produced or confirmed this finding — its human
    reference (SCN-YYMMDD-XXXXXX), use-case, intensity, and when it ran. Lets the
    UI label and group findings by scan without exposing run/job UUIDs. Resolved by
    the router from detection_run_id → detection_runs → scan_jobs; every field is
    optional because legacy findings and probe-self-assessed rows have no run link."""
    run_id: uuid.UUID | None = None
    job_id: uuid.UUID | None = None
    reference: str | None = None
    use_case_id: str | None = None
    intensity: str | None = None
    scanned_at: datetime | None = None


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
    content_overrides: dict | None = None
    assigned_to: uuid.UUID | None = None
    due_at: datetime | None = None
    due_at_source: str | None = None
    remediation_updated_at: datetime | None = None
    remediation_updated_by: str | None = None
    last_seen: datetime | None = None
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
    first_seen: datetime | None = None
    # The scan that most recently produced/confirmed this finding (task 3). Resolved
    # by the router from detection_run_id → detection_runs → scan_jobs; left null for
    # legacy/self-assessed findings with no run link. See FindingScanRef.
    scan: FindingScanRef | None = None
    # What the FILTERED scan did to this finding (new | reaffirmed | resolved). Set
    # only on the list when ?scan= is applied; null otherwise. Lets "filter by scan"
    # answer "what did that scan find" rather than merely narrowing the list.
    scan_outcome: str | None = None
    # P4 unified priority (computed; see services/risk_rank.py).
    risk_rank: int | None = None
    # Response priority P0-P5 (services/finding_priority.explain_priority); None for closed
    # findings and on responses that do not resolve SLA state.
    priority: str | None = None
    priority_reason: str | None = None
    # Why CVE / CVSS / EPSS / CWE are legitimately empty (recorded, or derived for configuration
    # findings) — so a list can say "not applicable" instead of "not recorded".
    scoring_not_applicable: dict[str, str] = Field(default_factory=dict)
    # Populated on the detail endpoint. List responses intentionally leave this
    # null to keep portfolio reads bounded and avoid an asset N+1 query.
    asset_context: FindingAssetContext | None = None
    # Affected asset identity on EVERY response (list + detail): the list resolves
    # the whole page in one query, so the UI never has to show an asset UUID.
    asset_ip: str | None = None
    asset_hostname: str | None = None

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

    @field_validator("resolution_miss_count", "reopened_count", mode="before")
    @classmethod
    def _default_lifecycle_counters(cls, value: Any) -> Any:
        # Persisted rows are non-null, but legacy/transient ORM objects may
        # expose SQLAlchemy's pre-flush ``None`` instead of the server default.
        return 0 if value is None else value

    @model_validator(mode="after")
    def _populate_scoring_not_applicable(self) -> "FindingOut":
        if not self.scoring_not_applicable:
            from app.services.report_enrichment import not_applicable_reasons
            self.scoring_not_applicable = not_applicable_reasons(self)
        return self

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


class ScanCompareCounts(BaseModel):
    new: int
    fixed: int
    still_present: int
    # Of still_present: findings whose severity, risk score or status differs between
    # the two scans' snapshots. Needs a snapshot on BOTH sides, so it is 0 when either
    # scan predates snapshots.
    changed: int = 0


class ScanCompareSnapshot(BaseModel):
    """A finding as one scan saw it."""
    severity: str | None = None
    risk_score: float | None = None
    status: str | None = None


class ScanCompareChange(BaseModel):
    """A finding present in both scans whose recorded state differs."""
    finding: FindingOut
    before: ScanCompareSnapshot
    after: ScanCompareSnapshot
    severity_changed: bool = False
    status_changed: bool = False
    risk_delta: float | None = None


class ScanCompareSummary(BaseModel):
    """What one scan saw, for the side-by-side totals. `from_snapshot` is False when
    any finding's severity had to come from today's row (a scan that predates
    snapshots), in which case the figures describe the finding now, not the scan then."""
    total: int
    by_severity: dict[str, int]
    average_risk: float | None = None
    from_snapshot: bool = True


class ScanCompareOut(BaseModel):
    """Diff between two scans (a = baseline, b = target). A finding is 'present' in a
    scan when that scan saw it new or reaffirmed. new = present in b but not a; fixed
    = present in a but not b; still_present = present in both; changed = the part of
    still_present whose severity, risk score or status differs between the scans.
    `counts` are the true totals; the finding lists are capped, most-severe first."""
    a: FindingScanRef | None = None
    b: FindingScanRef | None = None
    counts: ScanCompareCounts
    summary_a: ScanCompareSummary | None = None
    summary_b: ScanCompareSummary | None = None
    new: list[FindingOut]
    fixed: list[FindingOut]
    still_present: list[FindingOut]
    changed: list[ScanCompareChange] = []
