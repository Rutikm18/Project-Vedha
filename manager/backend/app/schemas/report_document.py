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
    snapshot_kind: Literal[
        "postgresql_repeatable_read_read_only",
        "sqlite_read_transaction",
        "caller_managed_snapshot",
        "best_effort_read_session",
    ] = "caller_managed_snapshot"
    snapshot_guarantee: Literal[
        "repeatable_read",
        "transactional_snapshot",
        "caller_managed",
        "best_effort",
    ] = "caller_managed"
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
    sha256_basis: str | None = None
    sha256_verified: bool | None = None
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
    assigned_to_user_id: uuid.UUID | None = None
    assigned_to_email: str | None = None
    owner: str | None = None
    owner_source: Literal["finding_assignee", "recorded_action_tracking"] | None = None
    asset_owner: str | None = None
    non_closure_reason: Any = None
    planned_closure_at: str | None = None
    action_reference: str | None = None
    recorded_at: str | None = None


class ReportSlaProjection(BaseModel):
    derived: Literal[True] = True
    historical: Literal[False] = False
    policy_basis: Literal[
        "current_effective_tenant_policy", "approved_deadline_extension"
    ] = "current_effective_tenant_policy"
    deadline_source: Literal["policy", "extension"] = "policy"
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
    integrity_status: Literal["verified", "unverified"] = "unverified"
    integrity_gaps: list[str] = Field(default_factory=list)


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


class ReportRecommendation(BaseModel):
    text: str
    source_type: Literal["finding_evidence", "reviewed_remediation_plan", "knowledge_base_recipe"]
    source_id: str | None = None
    author: str | None = None
    reviewer: str | None = None
    recorded_at: str | None = None
    generated_at: datetime | None = None
    reviewed_at: str | None = None
    review_state: Literal[
        "unreviewed_recorded", "recorded_as_reviewed", "human_reviewed_plan",
        "unreviewed_knowledge_base",
    ]


class ReportRemediation(BaseModel):
    recorded_text: str | None = None
    recorded_text_timestamp: datetime | None = None
    recorded_text_updated_by: str | None = None
    timestamp_gap: str | None = None
    reviewed_plans: list[ReportRemediationPlan] = Field(default_factory=list)
    recommendations: list[ReportRecommendation] = Field(default_factory=list)
    recorded_recommendations: list[str] = Field(default_factory=list)
    # The rule-keyed recipe rendered for this finding (ordered steps, per-OS commands,
    # verification, effort, risk, rollback). Standard knowledge-base content, not a
    # reviewed plan: `source` says so.
    fix_plan: dict[str, Any] | None = None
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
    rollup_usable: bool = False
    validation_gaps: list[str] = Field(default_factory=list)


class ReportDerivedGlobalControlPointer(BaseModel):
    framework: str
    controls: list[str] = Field(default_factory=list)
    rationale: str


class ReportDerivedRegionalObligationPointer(BaseModel):
    framework_id: str
    framework: str
    authority: str
    jurisdictions: list[str] = Field(default_factory=list)
    source_reference: str
    granularity: str
    controls: list[str] = Field(default_factory=list)
    rationale: str
    note: str | None = None


class ReportDerivedFindingComplianceContext(BaseModel):
    source: Literal["derived_context_only"] = "derived_context_only"
    assessment_status: Literal["not_assessed"] = "not_assessed"
    certification_status: Literal["not_a_certification"] = "not_a_certification"
    category: str
    themes: list[str] = Field(default_factory=list)
    used_generic_fallback: bool
    asset_tags: list[str] = Field(default_factory=list)
    global_framework_pointers: list[ReportDerivedGlobalControlPointer] = Field(
        default_factory=list
    )
    regional_obligations: list[ReportDerivedRegionalObligationPointer] = Field(
        default_factory=list
    )


class ReportDerivedRegionalFramework(BaseModel):
    framework_id: str
    name: str
    authority: str
    jurisdictions: list[str] = Field(default_factory=list)
    source_reference: str
    granularity: str
    note: str | None = None
    tag_triggered: bool = False


class ReportDerivedReportingClock(BaseModel):
    framework_id: str
    framework: str
    authority: str
    deadline_hours: float
    trigger: str
    reference: str


class ReportDerivedRegionalCompliance(BaseModel):
    source: Literal["derived_context_only"] = "derived_context_only"
    assessment_status: Literal["not_assessed"] = "not_assessed"
    certification_status: Literal["not_a_certification"] = "not_a_certification"
    profile_source: Literal[
        "recorded_engagement_profile", "default_generic_profile"
    ]
    profile: dict[str, Any]
    asset_tags: list[str] = Field(default_factory=list)
    frameworks: list[ReportDerivedRegionalFramework] = Field(default_factory=list)
    reporting_clocks: list[ReportDerivedReportingClock] = Field(default_factory=list)
    disclaimer: str


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
    # Why the platform flagged this (rule, evidence basis, the rule's false-positive
    # caveat) — kept apart from the description, which explains the weakness itself.
    detection_rationale: str | None = None
    service_port: int | None = None
    # Why CVE / CVSS / EPSS / CWE are legitimately empty (recorded, or derived for
    # configuration findings): an empty score with a reason is "not applicable", not a gap.
    not_applicable_reasons: dict[str, str] = Field(default_factory=dict)
    # Per narrative field: "recorded" (analyst/AI/evidence) or "knowledge_base" (standard text).
    narrative_sources: dict[str, str] = Field(default_factory=dict)
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
    derived_compliance_context: ReportDerivedFindingComplianceContext
    lifecycle: list[FindingEventOut] = Field(default_factory=list)
    closure: ReportClosureProjection
    current_sla: ReportSlaProjection
    readiness_gaps: list[str] = Field(default_factory=list)


class ReportIssueGroup(BaseModel):
    """One row for the client: every finding about the same service on the same asset,
    nested. The findings stay the audit records; this is how many *issues* they are."""
    key: str
    asset_id: uuid.UUID | None = None
    asset_label: str | None = None
    port: int | None = None
    title: str
    severity: str
    open: bool
    finding_count: int
    finding_ids: list[uuid.UUID]
    signals: list[str] = Field(default_factory=list)


class ReportSummary(BaseModel):
    # Findings roll up to issues (asset + service port); see `issue_groups`.
    issue_count: int = 0
    issue_groups: list[ReportIssueGroup] = Field(default_factory=list)
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


class ReportCoverageRule(BaseModel):
    rule_id: str
    title: str | None = None
    # finding_exists | evaluated_clean | no_evidence_collected | schema_drift | rule_error
    verdict: str
    reasons: list[str] = Field(default_factory=list)


class ReportCoverageSheet(BaseModel):
    """What was checked, so "not detected" can be told from "not checked".

    Taken from the engagement's latest completed detection run (its recorded per-rule
    verdicts) and the scan job that fed it. Nothing here is inferred: a rule with no recorded
    verdict is shown as `no_evidence_collected` (its scanner never produced facts)."""
    run_id: uuid.UUID
    run_finished_at: datetime | None = None
    vuln_db_version: str | None = None
    scan_reference: str | None = None
    scan_use_case: str | None = None
    scan_intensity: str | None = None
    ports_scanned: list[int] | str | None = None
    ports_scanned_note: str | None = None
    rules_total: int
    rules_evaluated_clean: int
    rules_with_finding: int
    rules_not_checked: int
    rules_could_not_assess: int
    rules: list[ReportCoverageRule] = Field(default_factory=list)
    interpretation: str = (
        "evaluated_clean means the check ran and found nothing; no_evidence_collected means the "
        "check did not run (its scanner produced no facts) and says nothing about the asset; "
        "schema_drift and rule_error mean the check could not be assessed."
    )


class ReportDocument(BaseModel):
    document: ReportDocumentControl
    engagement: ReportEngagement
    summary: ReportSummary
    findings: list[ReportFinding]
    # The latest detection run's per-rule outcomes (None when no run has been recorded).
    coverage_sheet: ReportCoverageSheet | None = None
    compliance_rollup: ReportComplianceRollup
    derived_regional_compliance: ReportDerivedRegionalCompliance
    readiness: ReportReadiness
