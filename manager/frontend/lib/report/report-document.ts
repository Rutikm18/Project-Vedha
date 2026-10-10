/**
 * Canonical customer-report read model returned by Manager.
 *
 * Field names intentionally mirror the FastAPI schema. This is a read-only
 * evidence contract, not a UI enrichment layer: absent values stay absent and
 * projections remain labelled as projections by the backend.
 */

export interface ReportDocumentControl {
  schema_version: "1.0";
  generated_at: string;
  timezone: "UTC";
  display_timezone: string;
  snapshot_kind:
    | "postgresql_repeatable_read_read_only"
    | "sqlite_read_transaction"
    | "caller_managed_snapshot"
    | "best_effort_read_session";
  snapshot_guarantee: "repeatable_read" | "transactional_snapshot" | "caller_managed" | "best_effort";
  persisted: false;
}

export interface ReportRegulatoryProfile {
  profile_id: string | null;
  name: string | null;
  version: string | null;
  jurisdiction: string | null;
  applicability: string | null;
  rationale: string | null;
  source_url: string | null;
  scope: unknown;
  selected_by: string | null;
  selected_at: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
  limitations: unknown;
  recorded_reference: string | null;
}

export interface ReportEngagement {
  id: string;
  name: string;
  status: string;
  scope_cidrs: string[];
  excluded_cidrs: string[];
  start_time: string | null;
  end_time: string | null;
  created_at: string;
  updated_at: string;
  client: string | null;
  assessor: string | null;
  description: string | null;
  tags: string[];
  recorded_report_metadata: Record<string, string>;
  regulatory_profiles: ReportRegulatoryProfile[];
  metadata_gaps: string[];
}

export interface ReportAsset {
  id: string;
  ip_address: string | null;
  hostname: string | null;
  fqdn: string | null;
  os: string | null;
  os_version: string | null;
  asset_type: string;
  criticality: string;
  owner: string | null;
  environment: string | null;
  tags: Record<string, unknown>;
  last_seen: string | null;
}

export interface ReportEvidenceArtifact {
  index: number;
  label: string;
  content: unknown;
  evidence_type: string | null;
  tool: string | null;
  source: string | null;
  command: string | null;
  timestamp: string | null;
  captured_at: string | null;
  captured_by: string | null;
  source_host: string | null;
  sha256: string | null;
  sha256_basis?: string | null;
  sha256_verified?: boolean | null;
  scan_result_id?: string | null;
  scan_job_id?: string | null;
  detection_run_id?: string | null;
  timestamp_basis?: string | null;
}

export interface ReportEvidence {
  raw: unknown;
  artifacts: ReportEvidenceArtifact[];
  gaps: string[];
}

export interface ReportVerification {
  state: string | null;
  confidence: number | null;
  rationale: string | null;
  method: string | null;
  needs_review: boolean;
}

export interface ReportActionTracking {
  assigned_to_user_id: string | null;
  assigned_to_email: string | null;
  owner: string | null;
  owner_source: "finding_assignee" | "recorded_action_tracking" | null;
  asset_owner: string | null;
  non_closure_reason: unknown;
  planned_closure_at: string | null;
  action_reference: string | null;
  recorded_at: string | null;
}

export interface ReportSlaProjection {
  derived: true;
  historical: false;
  policy_basis: "current_effective_tenant_policy" | "approved_deadline_extension";
  deadline_source: "policy" | "extension";
  calculated_at: string;
  state: string;
  deadline: string | null;
  hours_remaining: number | null;
  hours_total: number | null;
}

export interface ReportDetectionRunProvenance {
  role: "initial_discovery" | "latest_observation";
  run_id: string;
  scan_result_id: string | null;
  scan_job_id: string | null;
  scan_attempt_id: string | null;
  agent_id: string | null;
  scan_type: string | null;
  scan_result_checksum: string | null;
  scan_result_validation_state: string | null;
  scan_result_recorded_at: string | null;
  trigger: string;
  status: string;
  vuln_db_version: string | null;
  vuln_db_fetched_at: string | null;
  started_at: string;
  finished_at: string | null;
  facts_count: number;
  findings_new: number;
  findings_reaffirmed: number;
  findings_current: number;
  recorded_coverage: unknown;
  recorded_stats: Record<string, unknown>;
}

export interface ReportAutoResolutionCoverage {
  evidence_type: "recorded_detection_run_coverage";
  interpretation: "coverage_evidence_not_patch_attestation";
  run_id: string;
  scan_result_id: string | null;
  trigger: string;
  status: string;
  vuln_db_version: string | null;
  vuln_db_fetched_at: string | null;
  started_at: string;
  finished_at: string | null;
  facts_count: number;
  findings_new: number;
  findings_reaffirmed: number;
  findings_current: number;
  recorded_coverage: unknown;
  recorded_stats: Record<string, unknown>;
}

export interface ReportRetestRecord {
  passed: boolean | null;
  requested_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  verified_at: string | null;
  tested_by: string | null;
  verified_by: string | null;
  scope: unknown;
  vantage_point: string | null;
  authentication_context: string | null;
  method: string | null;
  tool_configuration: unknown;
  expected_result: unknown;
  actual_result: unknown;
  coverage_comparison: unknown;
  change_reference: string | null;
  residual_risk: unknown;
  before_evidence: ReportEvidence;
  after_evidence: ReportEvidence;
  integrity_status: "verified" | "unverified";
  integrity_gaps: string[];
}

export interface ReportFindingEvent {
  id: string | null;
  event_type: string;
  label: string;
  actor: string | null;
  actor_type: string;
  from_status: string | null;
  to_status: string | null;
  detail: Record<string, unknown> | null;
  occurred_at: string;
  synthesized: boolean;
}

export interface ReportClosureProjection {
  current_disposition: string;
  is_terminal: boolean;
  resolved_at: string | null;
  resolution_method: string | null;
  resolution_run_id: string | null;
  resolution_miss_count: number;
  reopened_count: number;
  reviewed_by: string | null;
  latest_terminal_event: ReportFindingEvent | null;
  terminal_and_reopen_history: ReportFindingEvent[];
  recorded_closure_evidence: ReportEvidence;
  retest: ReportRetestRecord | null;
  auto_resolution_coverage: ReportAutoResolutionCoverage | null;
  completeness_gaps: string[];
}

export interface ReportRemediationPlan {
  id: string;
  os: string;
  source: string;
  reviewed: true;
  generated_at: string;
  model: string | null;
  summary: string | null;
  effort: string | null;
  remediation_risk: string | null;
  steps: Array<Record<string, unknown>>;
  verification: string[];
  long_term_recommendations: string[];
  compensating_controls: string | null;
  raw: Record<string, unknown>;
}

export interface ReportRecommendation {
  text: string;
  source_type: "finding_evidence" | "reviewed_remediation_plan" | "knowledge_base_recipe";
  source_id: string | null;
  author: string | null;
  reviewer: string | null;
  recorded_at: string | null;
  generated_at: string | null;
  reviewed_at: string | null;
  review_state:
    | "unreviewed_recorded" | "recorded_as_reviewed" | "human_reviewed_plan" | "unreviewed_knowledge_base";
}

export interface ReportRemediation {
  recorded_text: string | null;
  recorded_text_timestamp: string | null;
  recorded_text_updated_by: string | null;
  timestamp_gap: string | null;
  reviewed_plans: ReportRemediationPlan[];
  recommendations: ReportRecommendation[];
  recorded_recommendations: string[];
  /** The rule-keyed recipe rendered for this finding (standard knowledge-base content, not a reviewed plan). */
  fix_plan?: ReportFixPlan | null;
  gaps: string[];
}

export interface ReportFixPlanStep {
  step: number;
  tier?: string;
  title: string;
  description?: string;
  commands_for_os?: string[];
  downtime?: string;
  rollback?: string;
  risk?: string;
}

export interface ReportFixPlan {
  source: string;
  recipe_id?: string;
  title?: string;
  summary?: string;
  effort?: string;
  remediation_risk?: string;
  steps: ReportFixPlanStep[];
  verification_check?: { check?: string; expected?: string; manual_command?: string };
  long_term_recommendations?: string[];
  compensating_controls?: string;
}

export interface ReportComplianceMapping {
  source_key: string;
  mapping_id: string | null;
  framework: string | null;
  framework_version: string | null;
  release: string | null;
  profile: string | null;
  control_id: string | null;
  control_title: string | null;
  relationship: string | null;
  rationale: string | null;
  applicability: string | null;
  assessment_status: string | null;
  result: string | null;
  test_ids: string[] | null;
  scope: unknown | null;
  context: unknown | null;
  source_url: string | null;
  mapping_source: string | null;
  mapping_version: string | null;
  mapped_by: string | null;
  mapped_at: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
  limitations: unknown | null;
  customer_statement: unknown | null;
  assessor: string | null;
  assessed_at: string | null;
  evidence_references: string[];
  recorded_reference: string | null;
  raw: unknown;
  rollup_usable: boolean;
  validation_gaps: string[];
}

export interface ReportDerivedGlobalControlPointer {
  framework: string;
  controls: string[];
  rationale: string;
}

export interface ReportDerivedRegionalObligationPointer {
  framework_id: string;
  framework: string;
  authority: string;
  jurisdictions: string[];
  source_reference: string;
  granularity: string;
  controls: string[];
  rationale: string;
  note: string | null;
}

export interface ReportDerivedFindingComplianceContext {
  source: "derived_context_only";
  assessment_status: "not_assessed";
  certification_status: "not_a_certification";
  category: string;
  themes: string[];
  used_generic_fallback: boolean;
  asset_tags: string[];
  global_framework_pointers: ReportDerivedGlobalControlPointer[];
  regional_obligations: ReportDerivedRegionalObligationPointer[];
}

export interface ReportDerivedRegionalFramework {
  framework_id: string;
  name: string;
  authority: string;
  jurisdictions: string[];
  source_reference: string;
  granularity: string;
  note: string | null;
  tag_triggered: boolean;
}

export interface ReportDerivedReportingClock {
  framework_id: string;
  framework: string;
  authority: string;
  deadline_hours: number;
  trigger: string;
  reference: string;
}

export interface ReportDerivedRegionalCompliance {
  source: "derived_context_only";
  assessment_status: "not_assessed";
  certification_status: "not_a_certification";
  profile_source: "recorded_engagement_profile" | "default_generic_profile";
  profile: {
    sector?: string;
    jurisdictions?: string[];
    [key: string]: unknown;
  };
  asset_tags: string[];
  frameworks: ReportDerivedRegionalFramework[];
  reporting_clocks: ReportDerivedReportingClock[];
  disclaimer: string;
}

export interface ReportFinding {
  id: string;
  title: string;
  description: string | null;
  technical_details: unknown;
  impact: unknown;
  business_impact: unknown;
  exploitation: unknown;
  reproduction_steps: unknown;
  root_cause: unknown;
  preconditions: unknown;
  /** Why the platform flagged this (rule, evidence basis, false-positive caveat). */
  detection_rationale?: string | null;
  service_port?: number | null;
  /** Why CVE / CVSS / EPSS / CWE are legitimately empty (recorded, or derived for configuration findings). */
  not_applicable_reasons?: Record<string, string>;
  /** Per narrative field: "recorded" or "knowledge_base" (standard text). */
  narrative_sources?: Record<string, string>;
  severity: string;
  status: string;
  asset: ReportAsset | null;
  cve_ids: string[];
  cwe_ids: string[];
  mitre_techniques: string[];
  cvss_score: number | string | null;
  cvss_vector: string | null;
  epss_score: number | string | null;
  risk_score: number | string | null;
  exploitable: boolean;
  exploit_validated: boolean;
  detection_status: string;
  first_seen: string | null;
  last_seen: string | null;
  initial_detection_run_id: string | null;
  detection_run_id: string | null;
  initial_detection_provenance: ReportDetectionRunProvenance | null;
  latest_detection_provenance: ReportDetectionRunProvenance | null;
  detected_db_version: string | null;
  created_at: string;
  updated_at: string;
  verification: ReportVerification;
  action_tracking: ReportActionTracking;
  evidence: ReportEvidence;
  remediation: ReportRemediation;
  compliance_mappings: ReportComplianceMapping[];
  derived_compliance_context: ReportDerivedFindingComplianceContext;
  lifecycle: ReportFindingEvent[];
  closure: ReportClosureProjection;
  current_sla: ReportSlaProjection;
  readiness_gaps: string[];
}

export interface ReportIssueGroup {
  key: string;
  asset_id: string | null;
  asset_label: string | null;
  port: number | null;
  title: string;
  severity: string;
  open: boolean;
  finding_count: number;
  finding_ids: string[];
  signals: string[];
}

export interface ReportSummary {
  /** Findings roll up to issues (one per asset + service port). */
  issue_count?: number;
  issue_groups?: ReportIssueGroup[];
  total_findings: number;
  by_severity: Record<string, number>;
  by_status: Record<string, number>;
  by_severity_status: Record<string, Record<string, number>>;
  open_by_severity: Record<string, number>;
  terminal_by_severity: Record<string, number>;
  open_or_confirmed: number;
  terminal: number;
  auto_resolved: number;
  manual_remediated: number;
  findings_with_reopen_history: number;
}

export interface ReportComplianceControlRollup {
  control_id: string | null;
  control_title: string | null;
  finding_ids: string[];
  recorded_results: string[];
}

export interface ReportComplianceFrameworkRollup {
  framework: string | null;
  framework_version: string | null;
  mapping_count: number;
  finding_count: number;
  controls: ReportComplianceControlRollup[];
}

export interface ReportComplianceRollup {
  source: "recorded_finding_mappings_only";
  mapping_count: number;
  regulatory_profiles: ReportRegulatoryProfile[];
  frameworks: ReportComplianceFrameworkRollup[];
  unmapped_finding_ids: string[];
  gap: string | null;
}

export interface ReportReadiness {
  complete: boolean;
  gap_counts: Record<string, number>;
  affected_finding_ids: Record<string, string[]>;
  report_gaps: string[];
}

export interface ReportDocument {
  document: ReportDocumentControl;
  engagement: ReportEngagement;
  summary: ReportSummary;
  findings: ReportFinding[];
  compliance_rollup: ReportComplianceRollup;
  derived_regional_compliance: ReportDerivedRegionalCompliance;
  readiness: ReportReadiness;
}

/** Render arbitrary recorded JSON without interpreting its meaning. */
export function recordedValue(value: unknown): string | null {
  if (value === null || value === undefined || value === "") return null;
  if (typeof value === "string") return value;
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

/** Human-readable label for a backend gap code; the code remains available. */
export function gapLabel(code: string): string {
  const text = code.replace(/_/g, " ").trim();
  return text ? `${text.charAt(0).toUpperCase()}${text.slice(1)}` : "Unspecified gap";
}

/** Executive narrative composed only from canonical counters. */
export function executiveSummaryText(summary: ReportSummary): string {
  return [
    `The live record contains ${summary.total_findings} finding${summary.total_findings === 1 ? "" : "s"}.`,
    `${summary.open_or_confirmed} are open or confirmed and ${summary.terminal} have a terminal disposition.`,
    `${summary.auto_resolved} are recorded as auto-resolved and ${summary.manual_remediated} as manually remediated.`,
    `${summary.findings_with_reopen_history} have recorded reopen history.`,
  ].join(" ");
}
