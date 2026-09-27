"""Stable response contract for the canonical engagement report read model.

The contract deliberately distinguishes recorded facts from derived projections.
Missing evidence, compliance mappings, and closure metadata are represented as
explicit gaps; the API never fills them with generated prose or current time.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.finding import FindingEventOut


class ReportDocumentControl(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    generated_at: datetime
    timezone: Literal["UTC"] = "UTC"
    display_timezone: str = "UTC"
    snapshot_kind: Literal["live_read_model"] = "live_read_model"
    persisted: Literal[False] = False


class ReportRegulatoryProfile(BaseModel):
    profile_id: str | None = None
    name: str | None = None
    version: str | None = None
    jurisdiction: str | None = None
    applicability: str | None = None
    rationale: str | None = None
    source_url: str | None = None
    scope: Any = None
    selected_by: str | None = None
    selected_at: str | None = None
    reviewed_by: str | None = None
    reviewed_at: str | None = None
    limitations: Any = None
    recorded_reference: str | None = None


class ReportEngagement(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    scope_cidrs: list[str] = Field(default_factory=list)
    excluded_cidrs: list[str] = Field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    created_at: datetime
    updated_at: datetime
    client: str | None = None
    assessor: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    recorded_report_metadata: dict[str, str] = Field(default_factory=dict)
    regulatory_profiles: list[ReportRegulatoryProfile] = Field(default_factory=list)
    metadata_gaps: list[str] = Field(default_factory=list)


class ReportAsset(BaseModel):
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
    tags: dict[str, Any] = Field(default_factory=dict)
    last_seen: datetime | None = None


class ReportEvidenceArtifact(BaseModel):
    index: int = Field(ge=1)
    label: str
    content: Any = None
    evidence_type: str | None = None
    tool: str | None = None
    source: str | None = None
    command: str | None = None
    timestamp: str | None = None
    captured_at: str | None = None
    captured_by: str | None = None
    source_host: str | None = None
    sha256: str | None = None
    scan_result_id: str | None = None
    scan_job_id: str | None = None
    detection_run_id: str | None = None
    timestamp_basis: str | None = None


class ReportEvidence(BaseModel):
    raw: Any = None
    artifacts: list[ReportEvidenceArtifact] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)


class ReportVerification(BaseModel):
    state: str | None = None
    confidence: int | None = None
    rationale: str | None = None
    method: str | None = None
    needs_review: bool


class ReportActionTracking(BaseModel):
    owner: str | None = None
    non_closure_reason: Any = None
    planned_closure_at: str | None = None
    action_reference: str | None = None
    recorded_at: str | None = None


class ReportSlaProjection(BaseModel):
    derived: Literal[True] = True
    historical: Literal[False] = False
    policy_basis: Literal["current_effective_tenant_policy"] = (
        "current_effective_tenant_policy"
    )
    calculated_at: datetime
    state: str
    deadline: datetime | None = None
    hours_remaining: float | None = None
    hours_total: int | None = None


class ReportDetectionRunProvenance(BaseModel):
    role: Literal["initial_discovery", "latest_observation"]
    run_id: uuid.UUID
    scan_result_id: uuid.UUID | None = None
    scan_job_id: uuid.UUID | None = None
    scan_attempt_id: uuid.UUID | None = None
    agent_id: uuid.UUID | None = None
    scan_type: str | None = None
    scan_result_checksum: str | None = None
    scan_result_validation_state: str | None = None
    scan_result_recorded_at: datetime | None = None
    trigger: str
    status: str
    vuln_db_version: str | None = None
    vuln_db_fetched_at: str | None = None
    started_at: datetime
    finished_at: datetime | None = None
    facts_count: int
    findings_new: int
    findings_reaffirmed: int
    findings_current: int
    recorded_coverage: Any = None
    recorded_stats: dict[str, Any] = Field(default_factory=dict)


class ReportAutoResolutionCoverage(BaseModel):
    evidence_type: Literal["recorded_detection_run_coverage"] = (
        "recorded_detection_run_coverage"
    )
    interpretation: Literal["coverage_evidence_not_patch_attestation"] = (
        "coverage_evidence_not_patch_attestation"
    )
    run_id: uuid.UUID
    scan_result_id: uuid.UUID | None = None
    trigger: str
    status: str
    vuln_db_version: str | None = None
    vuln_db_fetched_at: str | None = None
    started_at: datetime
    finished_at: datetime | None = None
    facts_count: int
    findings_new: int
    findings_reaffirmed: int
    findings_current: int
    recorded_coverage: Any = None
    recorded_stats: dict[str, Any] = Field(default_factory=dict)


class ReportRetestRecord(BaseModel):
    passed: bool | None = None
    requested_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    verified_at: str | None = None
    tested_by: str | None = None
    verified_by: str | None = None
    scope: Any = None
    vantage_point: str | None = None
    authentication_context: str | None = None
    method: str | None = None
    tool_configuration: Any = None
    expected_result: Any = None
    actual_result: Any = None
    coverage_comparison: Any = None
    change_reference: str | None = None
    residual_risk: Any = None
    before_evidence: ReportEvidence
    after_evidence: ReportEvidence


class ReportClosureProjection(BaseModel):
    current_disposition: str
    is_terminal: bool
    resolved_at: datetime | None = None
    resolution_method: str | None = None
    resolution_run_id: uuid.UUID | None = None
    resolution_miss_count: int
    reopened_count: int
    reviewed_by: str | None = None
    latest_terminal_event: FindingEventOut | None = None
    terminal_and_reopen_history: list[FindingEventOut] = Field(default_factory=list)
    recorded_closure_evidence: ReportEvidence
    retest: ReportRetestRecord | None = None
    auto_resolution_coverage: ReportAutoResolutionCoverage | None = None
    completeness_gaps: list[str] = Field(default_factory=list)


class ReportRemediationPlan(BaseModel):
    id: uuid.UUID
    os: str
    source: str
    reviewed: Literal[True] = True
    generated_at: datetime
    model: str | None = None
    summary: str | None = None
    effort: str | None = None
    remediation_risk: str | None = None
    steps: list[dict[str, Any]] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list)
    long_term_recommendations: list[str] = Field(default_factory=list)
    compensating_controls: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class ReportRemediation(BaseModel):
    recorded_text: str | None = None
    recorded_text_timestamp: datetime | None = None
    recorded_text_updated_by: str | None = None
    timestamp_gap: str | None = None
    reviewed_plans: list[ReportRemediationPlan] = Field(default_factory=list)
    recorded_recommendations: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)


class ReportComplianceMapping(BaseModel):
    source_key: str
    mapping_id: str | None = None
    framework: str | None = None
    framework_version: str | None = None
    release: str | None = None
    profile: str | None = None
    control_id: str | None = None
    control_title: str | None = None
    relationship: str | None = None
    rationale: str | None = None
    applicability: str | None = None
    assessment_status: str | None = None
    result: str | None = None
    test_ids: list[str] | None = None
    scope: Any = None
    context: Any = None
    source_url: str | None = None
    mapping_source: str | None = None
    mapping_version: str | None = None
    mapped_by: str | None = None
    mapped_at: str | None = None
    reviewed_by: str | None = None
    reviewed_at: str | None = None
    limitations: Any = None
    customer_statement: Any = None
    assessor: str | None = None
    assessed_at: str | None = None
    evidence_references: list[str] = Field(default_factory=list)
    recorded_reference: str | None = None
    raw: Any = None


class ReportFinding(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    technical_details: Any = None
    impact: Any = None
    business_impact: Any = None
    exploitation: Any = None
    reproduction_steps: Any = None
    root_cause: Any = None
    preconditions: Any = None
    severity: str
    status: str
    asset: ReportAsset | None = None
    cve_ids: list[str] = Field(default_factory=list)
    cwe_ids: list[str] = Field(default_factory=list)
    mitre_techniques: list[str] = Field(default_factory=list)
    cvss_score: Decimal | None = None
    cvss_vector: str | None = None
    epss_score: Decimal | None = None
    risk_score: Decimal | None = None
    exploitable: bool
    exploit_validated: bool
    detection_status: str
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    initial_detection_run_id: uuid.UUID | None = None
    detection_run_id: uuid.UUID | None = None
    initial_detection_provenance: ReportDetectionRunProvenance | None = None
    latest_detection_provenance: ReportDetectionRunProvenance | None = None
    detected_db_version: str | None = None
    created_at: datetime
    updated_at: datetime
    verification: ReportVerification
    action_tracking: ReportActionTracking
    evidence: ReportEvidence
    remediation: ReportRemediation
    compliance_mappings: list[ReportComplianceMapping] = Field(default_factory=list)
    lifecycle: list[FindingEventOut] = Field(default_factory=list)
    closure: ReportClosureProjection
    current_sla: ReportSlaProjection
    readiness_gaps: list[str] = Field(default_factory=list)


class ReportSummary(BaseModel):
    total_findings: int
    by_severity: dict[str, int]
    by_status: dict[str, int]
    by_severity_status: dict[str, dict[str, int]]
    open_by_severity: dict[str, int]
    terminal_by_severity: dict[str, int]
    open_or_confirmed: int
    terminal: int
    auto_resolved: int
    manual_remediated: int
    findings_with_reopen_history: int


class ReportComplianceControlRollup(BaseModel):
    control_id: str | None = None
    control_title: str | None = None
    finding_ids: list[uuid.UUID]
    recorded_results: list[str] = Field(default_factory=list)


class ReportComplianceFrameworkRollup(BaseModel):
    framework: str | None = None
    framework_version: str | None = None
    mapping_count: int
    finding_count: int
    controls: list[ReportComplianceControlRollup] = Field(default_factory=list)


class ReportComplianceRollup(BaseModel):
    source: Literal["recorded_finding_mappings_only"] = "recorded_finding_mappings_only"
    mapping_count: int
    regulatory_profiles: list[ReportRegulatoryProfile] = Field(default_factory=list)
    frameworks: list[ReportComplianceFrameworkRollup] = Field(default_factory=list)
    unmapped_finding_ids: list[uuid.UUID] = Field(default_factory=list)
    gap: str | None = None


class ReportReadiness(BaseModel):
    complete: bool
    gap_counts: dict[str, int] = Field(default_factory=dict)
    affected_finding_ids: dict[str, list[uuid.UUID]] = Field(default_factory=dict)
    report_gaps: list[str] = Field(default_factory=list)


class ReportDocument(BaseModel):
    document: ReportDocumentControl
    engagement: ReportEngagement
    summary: ReportSummary
    findings: list[ReportFinding]
    compliance_rollup: ReportComplianceRollup
    readiness: ReportReadiness
