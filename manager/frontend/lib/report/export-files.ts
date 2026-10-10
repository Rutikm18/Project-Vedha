import { renderReportPdf } from "./export-pdf";
import { zip } from "./zip";
import { buildReportDocx } from "./export-docx";
import {
  SEVERITY_LABEL,
  findingRef,
  humanize,
  keyMetrics,
  orderFindings,
  overallRating,
  readableText,
  severityKey,
  severityRows,
} from "./presentation";
import type { ReportDocument } from "./report-document";
import { redact } from "./finding-model";

export type ReportExportFormat = "csv" | "xlsx" | "pdf" | "docx";

export interface ReportExportFile {
  bytes: Buffer;
  contentType: string;
  filename: string;
}

function maskText(value: string): string {
  const placeholders: string[] = [];
  const protectedText = value.replace(/\[REDACTED:[^\]]+\]/g, (placeholder) => {
    const token = `__VEDHA_MASK_${placeholders.length}__`;
    placeholders.push(placeholder);
    return token;
  });
  return redact(protectedText).text.replace(
    /__VEDHA_MASK_(\d+)__/g,
    (_match, index: string) => placeholders[Number(index)] ?? "[REDACTED]",
  );
}

function exportSafe(value: unknown): unknown {
  if (typeof value === "string") return maskText(value);
  if (Array.isArray(value)) return value.map(exportSafe);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .filter(([key]) => key.toLowerCase() !== "raw")
        .map(([key, item]) => [key, exportSafe(item)]),
    );
  }
  return value;
}

function recordedText(value: unknown): string {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return maskText(value);
  try {
    return JSON.stringify(exportSafe(value));
  } catch {
    return String(value);
  }
}

type Cell = string | number | { v: string | number; s: number };

/** Workbook cell styles (indices into styles.xml cellXfs). */
const XS = { body: 0, header: 1, label: 2, critical: 3, high: 4, medium: 5, low: 6, info: 7, title: 8, ok: 9, risk: 10 } as const;

function sevStyle(value: unknown): number {
  const key = severityKey(String(value ?? ""));
  return String(value ?? "").trim() ? XS[key] : XS.body;
}

const CONTENT_TYPES: Record<ReportExportFormat, string> = {
  csv: "text/csv; charset=utf-8",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  pdf: "application/pdf",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
};

const EXTENSIONS: Record<ReportExportFormat, string> = {
  csv: "csv",
  xlsx: "xlsx",
  pdf: "pdf",
  docx: "docx",
};

function plain(value: unknown): string {
  return maskText(String(value ?? "").replace(/\u0000/g, "").trim());
}

function xml(value: unknown): string {
  return plain(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function remediationText(finding: ReportDocument["findings"][number]): string {
  return [
    finding.remediation.recorded_text,
    ...finding.remediation.reviewed_plans.map((plan) => plan.summary),
    ...finding.remediation.reviewed_plans.flatMap((plan) => plan.steps.map(recordedText)),
  ].filter(Boolean).join(" | ");
}

function fixPlanText(finding: ReportDocument["findings"][number]): string {
  const plan = finding.remediation.fix_plan;
  if (!plan) return "";
  const lines = [plan.title || plan.summary || ""];
  for (const step of plan.steps) lines.push(`${step.step}. ${step.tier ? `[${step.tier}] ` : ""}${step.title}`);
  const check = plan.verification_check;
  if (check?.check) lines.push(`Verify: ${check.check}${check.expected ? ` — expected: ${check.expected}` : ""}`);
  return lines.filter(Boolean).join("\n");
}

function standardTextFields(finding: ReportDocument["findings"][number]): string {
  return Object.entries(finding.narrative_sources ?? {})
    .filter(([, source]) => source === "knowledge_base")
    .map(([field]) => field)
    .join("; ");
}

function recommendationText(finding: ReportDocument["findings"][number]): string {
  return [
    ...finding.remediation.recommendations.map((recommendation) => recommendation.text),
    ...finding.remediation.recorded_recommendations,
    ...finding.remediation.reviewed_plans.flatMap((plan) => plan.long_term_recommendations),
    ...finding.remediation.reviewed_plans.map((plan) => plan.compensating_controls),
  ].filter(Boolean).join(" | ");
}

const FINDING_HEADERS = [
  "Document generated at", "Document status", "Snapshot kind", "Snapshot guarantee",
  "Finding ID", "Title", "Severity", "Status",
  "Affected asset", "CVSS", "CVSS vector", "Risk score", "CVEs", "CWEs", "MITRE techniques",
  "First seen", "Last seen", "Created at", "Updated at", "Initial detection run",
  "Latest detection run", "Description", "Technical details", "Technical impact", "Business impact",
  "Exploitation context", "Reproduction / validation", "Root cause", "Preconditions", "Remediation",
  "Structured recommendation records", "Compatibility recommendations", "Evidence count", "Evidence hashes",
  "Evidence hash bases", "Evidence hashes verified", "Evidence gaps", "Assigned user ID", "Assigned user email", "Action owner",
  "Owner source", "Asset owner", "Planned closure", "Action reference", "SLA state", "SLA deadline",
  "SLA policy basis", "SLA deadline source", "Disposition", "Resolved at",
  "Resolution method", "Reviewed by", "Closure evidence count", "Closure evidence hashes",
  "Retest passed", "Retest completed", "Retest verified", "Retest before-evidence count",
  "Retest before-evidence hashes", "Retest after-evidence count", "Retest after-evidence hashes",
  "Retest integrity status", "Retest integrity gaps", "Closure gaps", "Compliance mappings",
  "Compliance mappings rollup usable", "Compliance validation gaps",
  "Derived compliance source", "Derived assessment status", "Derived certification status",
  "Derived finding category", "Derived themes", "Derived generic fallback", "Derived asset tags",
  "Derived global control pointers", "Derived regional obligations",
  "Regional profile source", "Regional sector", "Regional jurisdictions",
  "Applicable regional frameworks", "Regional reporting clocks", "Regional context disclaimer",
  "Readiness gaps",
  "Detection rationale", "Fix plan (ordered steps)", "Standard-text fields", "Score not-applicable reasons",
];

function findingRows(report: ReportDocument): Cell[][] {
  return report.findings.map((finding) => [
    report.document.generated_at,
    report.document.persisted ? "PERSISTED" : "DRAFT / NOT APPROVED",
    report.document.snapshot_kind,
    report.document.snapshot_guarantee,
    finding.id,
    finding.title,
    finding.severity,
    finding.status,
    finding.asset?.fqdn || finding.asset?.hostname || finding.asset?.ip_address || "Not recorded",
    finding.cvss_score ?? "",
    finding.cvss_vector ?? "",
    finding.risk_score ?? "",
    finding.cve_ids.join("; "),
    finding.cwe_ids.join("; "),
    finding.mitre_techniques.join("; "),
    finding.first_seen ?? "",
    finding.last_seen ?? "",
    finding.created_at,
    finding.updated_at,
    finding.initial_detection_run_id ?? "",
    finding.detection_run_id ?? "",
    finding.description ?? "",
    recordedText(finding.technical_details),
    recordedText(finding.impact),
    recordedText(finding.business_impact),
    recordedText(finding.exploitation),
    recordedText(finding.reproduction_steps),
    recordedText(finding.root_cause),
    recordedText(finding.preconditions),
    remediationText(finding),
    recordedText(finding.remediation.recommendations),
    finding.remediation.recorded_recommendations.join(" | "),
    finding.evidence.artifacts.length,
    finding.evidence.artifacts.map((artifact) => artifact.sha256).filter(Boolean).join("; "),
    finding.evidence.artifacts.map((artifact) => artifact.sha256_basis).filter(Boolean).join("; "),
    finding.evidence.artifacts.map((artifact) => artifact.sha256_verified == null ? "not recorded" : String(artifact.sha256_verified)).join("; "),
    finding.evidence.gaps.join("; "),
    finding.action_tracking.assigned_to_user_id ?? "",
    finding.action_tracking.assigned_to_email ?? "",
    finding.action_tracking.owner ?? "",
    finding.action_tracking.owner_source ?? "",
    finding.action_tracking.asset_owner ?? "",
    finding.action_tracking.planned_closure_at ?? "",
    finding.action_tracking.action_reference ?? "",
    finding.current_sla.state,
    finding.current_sla.deadline ?? "",
    finding.current_sla.policy_basis,
    finding.current_sla.deadline_source,
    finding.closure.current_disposition,
    finding.closure.resolved_at ?? "",
    finding.closure.resolution_method ?? "",
    finding.closure.reviewed_by ?? "",
    finding.closure.recorded_closure_evidence.artifacts.length,
    finding.closure.recorded_closure_evidence.artifacts.map((artifact) => artifact.sha256).filter(Boolean).join("; "),
    finding.closure.retest?.passed == null ? "" : String(finding.closure.retest.passed),
    finding.closure.retest?.completed_at ?? "",
    finding.closure.retest?.verified_at ?? "",
    finding.closure.retest?.before_evidence.artifacts.length ?? 0,
    finding.closure.retest?.before_evidence.artifacts.map((artifact) => artifact.sha256).filter(Boolean).join("; ") ?? "",
    finding.closure.retest?.after_evidence.artifacts.length ?? 0,
    finding.closure.retest?.after_evidence.artifacts.map((artifact) => artifact.sha256).filter(Boolean).join("; ") ?? "",
    finding.closure.retest?.integrity_status ?? "",
    finding.closure.retest?.integrity_gaps.join("; ") ?? "",
    finding.closure.completeness_gaps.join("; "),
    finding.compliance_mappings.map((mapping) => [mapping.framework, mapping.control_id].filter(Boolean).join(":"))
      .filter(Boolean).join("; "),
    finding.compliance_mappings.every((mapping) => mapping.rollup_usable) ? "true" : "false",
    finding.compliance_mappings.flatMap((mapping) => mapping.validation_gaps).join("; "),
    finding.derived_compliance_context.source,
    finding.derived_compliance_context.assessment_status,
    finding.derived_compliance_context.certification_status,
    finding.derived_compliance_context.category,
    finding.derived_compliance_context.themes.join("; "),
    String(finding.derived_compliance_context.used_generic_fallback),
    finding.derived_compliance_context.asset_tags.join("; "),
    recordedText(finding.derived_compliance_context.global_framework_pointers),
    recordedText(finding.derived_compliance_context.regional_obligations),
    report.derived_regional_compliance.profile_source,
    typeof report.derived_regional_compliance.profile.sector === "string"
      ? report.derived_regional_compliance.profile.sector
      : "",
    Array.isArray(report.derived_regional_compliance.profile.jurisdictions)
      ? report.derived_regional_compliance.profile.jurisdictions.join("; ")
      : "",
    recordedText(report.derived_regional_compliance.frameworks),
    recordedText(report.derived_regional_compliance.reporting_clocks),
    report.derived_regional_compliance.disclaimer,
    finding.readiness_gaps.join("; "),
    finding.detection_rationale ?? "",
    fixPlanText(finding),
    standardTextFields(finding),
    Object.entries(finding.not_applicable_reasons ?? {}).map(([key, reason]) => `${key.toUpperCase()}: ${reason}`).join(" | "),
  ]);
}

export function exportFilename(format: ReportExportFormat, report: ReportDocument): string {
  const subject = plain(report.engagement.name || report.engagement.client || "assessment")
    .normalize("NFKD")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase()
    .slice(0, 80) || "assessment";
  return `vedha-${subject}-report.${EXTENSIONS[format]}`;
}

function csvCell(value: string | number): string {
  let normalized = plain(value).replace(/\r\n?/g, "\n");
  // Excel and similar tools execute formulas even when a CSV cell is quoted.
  // Prefix attacker-controlled formula leaders so exports remain data, not code.
  if (typeof value === "string" && /^[\t\r ]*[=+\-@]/.test(normalized)) {
    normalized = `'${normalized}`;
  }
  return `"${normalized.replace(/"/g, '""')}"`;
}

function buildCsv(report: ReportDocument): Buffer {
  const rows = [FINDING_HEADERS, ...findingRows(report)];
  return Buffer.from(`\uFEFF${rows.map((row) => row.map(csvCell).join(",")).join("\r\n")}\r\n`, "utf8");
}

/* Minimal ZIP writer for the OOXML exports. It intentionally uses fixed DOS
 * timestamps so a report generated from the same data is byte-for-byte stable,
 * which makes regression tests and incident evidence easier to compare. */
function colName(index: number): string {
  let n = index + 1;
  let name = "";
  while (n > 0) {
    const r = (n - 1) % 26;
    name = String.fromCharCode(65 + r) + name;
    n = Math.floor((n - 1) / 26);
  }
  return name;
}

function excelCell(cell: Cell, ref: string, style = 0): string {
  const value = typeof cell === "object" ? cell.v : cell;
  const s = typeof cell === "object" ? cell.s : style;
  if (typeof value === "number" && Number.isFinite(value)) {
    return `<c r="${ref}" s="${s}" t="n"><v>${value}</v></c>`;
  }
  return `<c r="${ref}" s="${s}" t="inlineStr"><is><t xml:space="preserve">${xml(value)}</t></is></c>`;
}

/**
 * A worksheet with a frozen, filterable header row, column widths fitted to
 * the content, and severity cells coloured by severity.
 */
function worksheetXml(rows: Cell[][], opts: { header?: boolean; labelColumn?: boolean } = {}): string {
  const header = opts.header !== false;
  const width = Math.max(1, ...rows.map((r) => r.length));
  const sevCol = header ? (rows[0] ?? []).findIndex((c) => String(typeof c === "object" ? c.v : c).toLowerCase() === "severity") : -1;
  const widths = Array.from({ length: width }, (_, col) => {
    let max = 8;
    for (const row of rows.slice(0, 400)) {
      const cell = row[col];
      const text = String(typeof cell === "object" ? cell?.v ?? "" : cell ?? "");
      const longest = Math.max(...text.split("\n").map((line) => line.length));
      max = Math.max(max, Math.min(longest, 70));
    }
    return Math.min(Math.max(max * 1.05 + 2, 10), 72);
  });
  const body = rows.map((row, r) => {
    const cells = row.map((value, c) => {
      const style = header && r === 0
        ? XS.header
        : c === sevCol ? sevStyle(typeof value === "object" ? value.v : value)
        : opts.labelColumn && c === 0 ? XS.label : XS.body;
      return excelCell(value, `${colName(c)}${r + 1}`, style);
    }).join("");
    return `<row r="${r + 1}">${cells}</row>`;
  }).join("");
  const cols = widths.map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w.toFixed(1)}" customWidth="1"/>`).join("");
  const pane = header ? `<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A2" sqref="A2"/>` : "";
  const filter = header && rows.length > 1 && !opts.labelColumn ? `<autoFilter ref="A1:${colName(width - 1)}${rows.length}"/>` : "";
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0">${pane}</sheetView></sheetViews><sheetFormatPr defaultRowHeight="15"/><cols>${cols}</cols><sheetData>${body}</sheetData>${filter}</worksheet>`;
}

function ooxmlCreated(report: ReportDocument): string {
  const timestamp = Date.parse(report.document.generated_at);
  if (!Number.isFinite(timestamp)) return "";
  return `<dcterms:created xsi:type="dcterms:W3CDTF">${xml(new Date(timestamp).toISOString())}</dcterms:created>`;
}

function buildXlsx(report: ReportDocument): Buffer {
  const evidenceRows: Cell[][] = [[
    "Finding ID", "Evidence set", "Artifact index", "Label", "Type", "Content", "Tool", "Source", "Command",
    "Timestamp", "Captured at", "Captured by", "Source host", "SHA-256", "SHA-256 basis",
    "SHA-256 verified", "Scan result ID",
    "Scan job ID", "Detection run ID", "Timestamp basis",
  ]];
  const remediationRows: Cell[][] = [[
    "Finding ID", "Recorded remediation", "Recorded at", "Updated by", "Timestamp gap",
    "Reviewed plans", "Structured recommendation records", "Compatibility recommendations",
    "Combined recommendation text", "Remediation gaps", "Fix plan (ordered steps)",
  ]];
  const closureRows: Cell[][] = [[
    "Finding ID", "Disposition", "Terminal", "Resolved at", "Resolution method", "Resolution run",
    "Miss count", "Reopened count", "Reviewed by", "Closure evidence", "Auto-resolution coverage",
    "Retest passed", "Retest requested", "Retest started", "Retest completed", "Retest verified",
    "Tested by", "Verified by", "Retest scope", "Vantage point", "Authentication context",
    "Method", "Tool configuration", "Expected result", "Actual result", "Coverage comparison",
    "Change reference", "Residual risk", "Before evidence", "After evidence", "Lifecycle", "Closure gaps",
    "Retest integrity status", "Retest integrity gaps",
  ]];
  const complianceRows: Cell[][] = [[
    "Finding ID", "Framework", "Framework version", "Release", "Profile", "Control ID",
    "Control title", "Relationship", "Rationale", "Applicability", "Assessment status", "Result",
    "Test IDs", "Scope", "Context", "Source URL", "Mapping source", "Mapping version", "Mapped by",
    "Mapped at", "Reviewed by", "Reviewed at", "Limitations", "Customer statement", "Assessor",
    "Assessed at", "Evidence references", "Recorded reference", "Rollup usable", "Validation gaps",
  ]];
  const derivedContextRows: Cell[][] = [[
    "Finding ID", "Source", "Assessment status", "Certification status", "Category", "Themes",
    "Generic fallback", "Asset tags", "Global framework pointers", "Regional obligations",
  ]];
  const gapRows: Cell[][] = [["Level", "Finding ID", "Category", "Gap"]];

  function appendEvidenceRows(
    findingId: string,
    evidenceSet: string,
    evidence: ReportDocument["findings"][number]["evidence"],
  ) {
    for (const artifact of evidence.artifacts) {
      evidenceRows.push([
        findingId, evidenceSet, artifact.index, artifact.label, artifact.evidence_type ?? "",
        recordedText(artifact.content), artifact.tool ?? "", artifact.source ?? "", artifact.command ?? "",
        artifact.timestamp ?? "", artifact.captured_at ?? "", artifact.captured_by ?? "",
        artifact.source_host ?? "", artifact.sha256 ?? "", artifact.sha256_basis ?? "",
        artifact.sha256_verified == null ? "" : String(artifact.sha256_verified), artifact.scan_result_id ?? "",
        artifact.scan_job_id ?? "", artifact.detection_run_id ?? "", artifact.timestamp_basis ?? "",
      ]);
    }
  }

  for (const finding of report.findings) {
    appendEvidenceRows(finding.id, "finding", finding.evidence);
    appendEvidenceRows(finding.id, "closure", finding.closure.recorded_closure_evidence);
    if (finding.closure.retest) {
      appendEvidenceRows(finding.id, "retest_before", finding.closure.retest.before_evidence);
      appendEvidenceRows(finding.id, "retest_after", finding.closure.retest.after_evidence);
    }
    remediationRows.push([
      finding.id, finding.remediation.recorded_text ?? "",
      finding.remediation.recorded_text_timestamp ?? "", finding.remediation.recorded_text_updated_by ?? "",
      finding.remediation.timestamp_gap ?? "", recordedText(finding.remediation.reviewed_plans),
      recordedText(finding.remediation.recommendations),
      finding.remediation.recorded_recommendations.join(" | "), recommendationText(finding),
      finding.remediation.gaps.join("; "), fixPlanText(finding),
    ]);
    const retest = finding.closure.retest;
    closureRows.push([
      finding.id, finding.closure.current_disposition, String(finding.closure.is_terminal),
      finding.closure.resolved_at ?? "", finding.closure.resolution_method ?? "",
      finding.closure.resolution_run_id ?? "", finding.closure.resolution_miss_count,
      finding.closure.reopened_count, finding.closure.reviewed_by ?? "",
      recordedText(finding.closure.recorded_closure_evidence),
      recordedText(finding.closure.auto_resolution_coverage),
      retest?.passed == null ? "" : String(retest.passed), retest?.requested_at ?? "",
      retest?.started_at ?? "", retest?.completed_at ?? "", retest?.verified_at ?? "",
      retest?.tested_by ?? "", retest?.verified_by ?? "", recordedText(retest?.scope),
      retest?.vantage_point ?? "", retest?.authentication_context ?? "", retest?.method ?? "",
      recordedText(retest?.tool_configuration), recordedText(retest?.expected_result),
      recordedText(retest?.actual_result), recordedText(retest?.coverage_comparison),
      retest?.change_reference ?? "", recordedText(retest?.residual_risk),
      recordedText(retest?.before_evidence), recordedText(retest?.after_evidence),
      recordedText(finding.lifecycle), finding.closure.completeness_gaps.join("; "),
      retest?.integrity_status ?? "", retest?.integrity_gaps.join("; ") ?? "",
    ]);
    for (const mapping of finding.compliance_mappings) {
      complianceRows.push([
        finding.id, mapping.framework ?? "", mapping.framework_version ?? "", mapping.release ?? "",
        mapping.profile ?? "", mapping.control_id ?? "", mapping.control_title ?? "",
        mapping.relationship ?? "", mapping.rationale ?? "", mapping.applicability ?? "",
        mapping.assessment_status ?? "", mapping.result ?? "", (mapping.test_ids ?? []).join("; "),
        recordedText(mapping.scope), recordedText(mapping.context), mapping.source_url ?? "",
        mapping.mapping_source ?? "", mapping.mapping_version ?? "", mapping.mapped_by ?? "",
        mapping.mapped_at ?? "", mapping.reviewed_by ?? "", mapping.reviewed_at ?? "",
        recordedText(mapping.limitations), recordedText(mapping.customer_statement),
        mapping.assessor ?? "", mapping.assessed_at ?? "", mapping.evidence_references.join("; "),
        mapping.recorded_reference ?? "", String(mapping.rollup_usable), mapping.validation_gaps.join("; "),
      ]);
    }
    derivedContextRows.push([
      finding.id,
      finding.derived_compliance_context.source,
      finding.derived_compliance_context.assessment_status,
      finding.derived_compliance_context.certification_status,
      finding.derived_compliance_context.category,
      finding.derived_compliance_context.themes.join("; "),
      String(finding.derived_compliance_context.used_generic_fallback),
      finding.derived_compliance_context.asset_tags.join("; "),
      recordedText(finding.derived_compliance_context.global_framework_pointers),
      recordedText(finding.derived_compliance_context.regional_obligations),
    ]);
    for (const gap of finding.readiness_gaps) gapRows.push(["Finding", finding.id, "readiness", gap]);
    for (const gap of finding.evidence.gaps) gapRows.push(["Finding", finding.id, "evidence", gap]);
    for (const gap of finding.remediation.gaps) gapRows.push(["Finding", finding.id, "remediation", gap]);
    for (const gap of finding.closure.completeness_gaps) gapRows.push(["Finding", finding.id, "closure", gap]);
    for (const gap of finding.closure.retest?.integrity_gaps ?? []) gapRows.push(["Finding", finding.id, "retest integrity", gap]);
    for (const mapping of finding.compliance_mappings) {
      for (const gap of mapping.validation_gaps) gapRows.push(["Finding", finding.id, "compliance validation", gap]);
    }
  }
  for (const gap of report.readiness.report_gaps) gapRows.push(["Report", "", "readiness", gap]);

  const rollupRows: Cell[][] = [[
    "Framework", "Framework version", "Mapping count", "Finding count", "Control ID",
    "Control title", "Finding IDs", "Recorded results",
  ]];
  for (const framework of report.compliance_rollup.frameworks) {
    for (const control of framework.controls) {
      rollupRows.push([
        framework.framework ?? "", framework.framework_version ?? "", framework.mapping_count,
        framework.finding_count, control.control_id ?? "", control.control_title ?? "",
        control.finding_ids.join("; "), control.recorded_results.join("; "),
      ]);
    }
  }

  const ordered = { ...report, findings: orderFindings(report.findings) };
  const rating = overallRating(report);
  const metrics = keyMetrics(report);
  const ratingStyle = rating.level === "none" ? XS.ok : rating.level === "critical" || rating.level === "high" ? XS.risk : XS.label;
  const overviewRows: Cell[][] = [
    ["Field", "Recorded value"],
    ["Overall risk", { v: rating.label, s: ratingStyle }],
    ["Rating basis", `${rating.basis} Rule: highest severity among open findings.`],
    ["Findings", `${metrics.total} total · ${metrics.open} open · ${metrics.closed} closed`],
    ...severityRows(report).map((row) => [{ v: `${SEVERITY_LABEL[row.severity]} findings`, s: XS.label }, `${row.open} open of ${row.total}`] as Cell[]),
    ["Open past SLA deadline", String(metrics.slaBreached)],
    ["Assets with open findings", String(metrics.assetsAffected)],
    ...Object.entries(report.engagement.recorded_report_metadata)
      .filter(([, value]) => value !== null && value !== undefined && String(value).trim())
      .map(([key, value]) => [`Report ${humanize(key).toLowerCase()}`, maskText(String(value))] as Cell[]),
    ["Export status", report.document.persisted ? "PERSISTED" : "DRAFT / NOT APPROVED"],
    ["Schema version", report.document.schema_version],
    ["Generated at", report.document.generated_at],
    ["Canonical timezone", report.document.timezone],
    ["Display timezone", report.document.display_timezone],
    ["Snapshot kind", report.document.snapshot_kind],
    ["Snapshot guarantee", report.document.snapshot_guarantee],
    ["Persisted", String(report.document.persisted)],
    ["Engagement ID", report.engagement.id],
    ["Engagement", report.engagement.name],
    ["Client", report.engagement.client ?? "Not recorded"],
    ["Status", report.engagement.status],
    ["Assessment window", `${report.engagement.start_time ?? "Not recorded"} — ${report.engagement.end_time ?? "Not recorded"}`],
    ["Assessor", report.engagement.assessor ?? "Not recorded"],
    ["Scope", report.engagement.scope_cidrs.join(", ")],
    ["Excluded scope", report.engagement.excluded_cidrs.join(", ")],
    ["Description", report.engagement.description ?? ""],
    ["Regulatory profiles", recordedText(report.engagement.regulatory_profiles)],
    ["Engagement metadata gaps", report.engagement.metadata_gaps.join("; ")],
    ["Summary", readableText(report.summary, "; ") ?? ""],
    ["Readiness complete", String(report.readiness.complete)],
    ["Readiness gap counts", recordedText(report.readiness.gap_counts)],
    ["Compliance rollup source", report.compliance_rollup.source],
    ["Compliance rollup gap", report.compliance_rollup.gap ?? ""],
    ["Unmapped finding IDs", report.compliance_rollup.unmapped_finding_ids.join("; ")],
    ["Derived regional context source", report.derived_regional_compliance.source],
    ["Derived regional assessment status", report.derived_regional_compliance.assessment_status],
    ["Derived regional certification status", report.derived_regional_compliance.certification_status],
    ["Derived regional profile source", report.derived_regional_compliance.profile_source],
    ["Derived regional profile", recordedText(report.derived_regional_compliance.profile)],
    ["Derived regional asset tags", report.derived_regional_compliance.asset_tags.join("; ")],
    ["Derived regional disclaimer", report.derived_regional_compliance.disclaimer],
  ];

  const regionalContextRows: Cell[][] = [[
    "Context type", "Context source", "Assessment status", "Certification status",
    "Framework ID", "Framework", "Authority", "Jurisdictions", "Source reference",
    "Granularity", "Tag-triggered", "Deadline hours", "Trigger", "Reporting reference",
    "Profile source", "Sector", "Profile jurisdictions", "Note", "Disclaimer",
  ], [
    "Profile",
    report.derived_regional_compliance.source,
    report.derived_regional_compliance.assessment_status,
    report.derived_regional_compliance.certification_status,
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    report.derived_regional_compliance.profile_source,
    typeof report.derived_regional_compliance.profile.sector === "string"
      ? report.derived_regional_compliance.profile.sector
      : "",
    Array.isArray(report.derived_regional_compliance.profile.jurisdictions)
      ? report.derived_regional_compliance.profile.jurisdictions.join("; ")
      : "",
    "",
    report.derived_regional_compliance.disclaimer,
  ]];
  for (const framework of report.derived_regional_compliance.frameworks) {
    regionalContextRows.push([
      "Applicable framework",
      report.derived_regional_compliance.source,
      report.derived_regional_compliance.assessment_status,
      report.derived_regional_compliance.certification_status,
      framework.framework_id, framework.name, framework.authority,
      framework.jurisdictions.join("; "), framework.source_reference, framework.granularity,
      String(framework.tag_triggered), "", "", "", "", "", "", framework.note ?? "", "",
    ]);
  }
  for (const clock of report.derived_regional_compliance.reporting_clocks) {
    regionalContextRows.push([
      "Reporting clock",
      report.derived_regional_compliance.source,
      report.derived_regional_compliance.assessment_status,
      report.derived_regional_compliance.certification_status,
      clock.framework_id, clock.framework, clock.authority, "", "", "", "",
      clock.deadline_hours, clock.trigger, clock.reference, "", "", "", "", "",
    ]);
  }

  const sheets: Array<{ name: string; rows: Cell[][] }> = [
    { name: "Overview", rows: overviewRows },
    // The workbook leads with what a reader filters on; the four per-document
    // columns (identical on every row) move to the end. The CSV keeps its order.
    { name: "Findings", rows: [["Ref", ...FINDING_HEADERS.slice(4), ...FINDING_HEADERS.slice(0, 4)], ...findingRows(ordered).map((row, i) => [findingRef(i), ...row.slice(4), ...row.slice(0, 4)])] },
    { name: "Evidence", rows: evidenceRows },
    { name: "Remediation", rows: remediationRows },
    { name: "Closure", rows: closureRows },
    { name: "Compliance", rows: complianceRows },
    { name: "Control Rollup", rows: rollupRows },
    { name: "Gaps", rows: gapRows },
    { name: "Derived Context", rows: derivedContextRows },
    { name: "Regional Context", rows: regionalContextRows },
  ];
  const overrides = sheets.map((_, index) =>
    `<Override PartName="/xl/worksheets/sheet${index + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`
  ).join("");
  const workbookSheets = sheets.map((sheet, index) =>
    `<sheet name="${xml(sheet.name)}" sheetId="${index + 1}" r:id="rId${index + 1}"/>`
  ).join("");
  const workbookRels = sheets.map((_, index) =>
    `<Relationship Id="rId${index + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${index + 1}.xml"/>`
  ).join("");

  return zip([
    { name: "[Content_Types].xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>${overrides}<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>` },
    { name: "_rels/.rels", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>` },
    { name: "docProps/core.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${xml(report.engagement.name)} security report</dc:title><dc:creator>Vedha VAPT Platform</dc:creator>${ooxmlCreated(report)}</cp:coreProperties>` },
    { name: "docProps/app.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Vedha VAPT Platform</Application></Properties>` },
    { name: "xl/workbook.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>${workbookSheets}</sheets></workbook>` },
    { name: "xl/_rels/workbook.xml.rels", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${workbookRels}<Relationship Id="rId${sheets.length + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>` },
    { name: "xl/styles.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="6"><font><sz val="10"/><color rgb="FF0F172A"/><name val="Aptos"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FF12284B"/><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FF12284B"/><sz val="13"/><name val="Aptos"/></font><font><b/><color rgb="FF0F766E"/><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FFB91C1C"/><sz val="10"/><name val="Aptos"/></font></fonts><fills count="8"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF12284B"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFB91C1C"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFC2410C"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFA16207"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FF57534E"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FF475569"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="2"><border/><border><bottom style="thin"><color rgb="FFD9DEE7"/></bottom></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="11"><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf><xf numFmtId="0" fontId="2" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="6" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="7" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf><xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="0" fontId="4" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="5" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs></styleSheet>` },
    ...sheets.map((sheet, index) => ({ name: `xl/worksheets/sheet${index + 1}.xml`, data: worksheetXml(sheet.rows, { labelColumn: sheet.name === "Overview" }) })),
  ]);
}

export async function buildReportExport(
  format: ReportExportFormat,
  report: ReportDocument,
): Promise<ReportExportFile> {
  const bytes = format === "csv"
    ? buildCsv(report)
    : format === "xlsx"
      ? buildXlsx(report)
      : format === "pdf"
        ? (await renderReportPdf(report)).bytes
        : buildReportDocx(report);
  return {
    bytes,
    contentType: CONTENT_TYPES[format],
    filename: exportFilename(format, report),
  };
}
