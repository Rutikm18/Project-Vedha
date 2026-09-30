import { deflateRawSync } from "node:zlib";
import path from "node:path";
import PDFDocument from "pdfkit";
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

type Cell = string | number;

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
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(input: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of input) crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function u16(value: number): Buffer {
  const out = Buffer.allocUnsafe(2);
  out.writeUInt16LE(value & 0xffff);
  return out;
}

function u32(value: number): Buffer {
  const out = Buffer.allocUnsafe(4);
  out.writeUInt32LE(value >>> 0);
  return out;
}

function zip(entries: Array<{ name: string; data: string | Buffer }>): Buffer {
  const localParts: Buffer[] = [];
  const centralParts: Buffer[] = [];
  let offset = 0;

  for (const entry of entries) {
    const name = Buffer.from(entry.name, "utf8");
    const data = Buffer.isBuffer(entry.data) ? entry.data : Buffer.from(entry.data, "utf8");
    const compressed = deflateRawSync(data, { level: 9 });
    const checksum = crc32(data);
    const localHeader = Buffer.concat([
      u32(0x04034b50), u16(20), u16(0x0800), u16(8), u16(0), u16(0),
      u32(checksum), u32(compressed.length), u32(data.length), u16(name.length), u16(0), name,
    ]);
    localParts.push(localHeader, compressed);

    centralParts.push(Buffer.concat([
      u32(0x02014b50), u16(20), u16(20), u16(0x0800), u16(8), u16(0), u16(0),
      u32(checksum), u32(compressed.length), u32(data.length), u16(name.length),
      u16(0), u16(0), u16(0), u16(0), u32(0), u32(offset), name,
    ]));
    offset += localHeader.length + compressed.length;
  }

  const central = Buffer.concat(centralParts);
  const end = Buffer.concat([
    u32(0x06054b50), u16(0), u16(0), u16(entries.length), u16(entries.length),
    u32(central.length), u32(offset), u16(0),
  ]);
  return Buffer.concat([...localParts, central, end]);
}

function excelCell(value: string | number, style = 0): string {
  if (typeof value === "number" && Number.isFinite(value)) {
    return `<c s="${style}" t="n"><v>${value}</v></c>`;
  }
  return `<c s="${style}" t="inlineStr"><is><t xml:space="preserve">${xml(value)}</t></is></c>`;
}

function worksheetXml(rows: Cell[][]): string {
  const body = rows.map((row, rowIndex) =>
    `<row r="${rowIndex + 1}">${row.map((value) => excelCell(value, rowIndex === 0 ? 1 : 0)).join("")}</row>`
  ).join("");
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><cols><col min="1" max="1" width="24" customWidth="1"/><col min="2" max="64" width="28" customWidth="1"/></cols><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><sheetData>${body}</sheetData></worksheet>`;
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
    "Combined recommendation text", "Remediation gaps",
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
      finding.remediation.gaps.join("; "),
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

  const overviewRows: Cell[][] = [
    ["Field", "Recorded value"],
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
    ["Recorded report metadata", recordedText(report.engagement.recorded_report_metadata)],
    ["Regulatory profiles", recordedText(report.engagement.regulatory_profiles)],
    ["Engagement metadata gaps", report.engagement.metadata_gaps.join("; ")],
    ["Summary", recordedText(report.summary)],
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
    { name: "Findings", rows: [FINDING_HEADERS, ...findingRows(report)] },
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
    { name: "xl/styles.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="10"/><name val="Aptos"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF163B72"/><bgColor indexed="64"/></patternFill></fill><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs></styleSheet>` },
    ...sheets.map((sheet, index) => ({ name: `xl/worksheets/sheet${index + 1}.xml`, data: worksheetXml(sheet.rows) })),
  ]);
}

interface ReportLine { text: string; heading?: boolean }

function labelled(label: string, value: unknown, fallback = "Not recorded"): ReportLine {
  return { text: `${label}: ${recordedText(value) || fallback}` };
}

export function reportLines(report: ReportDocument): ReportLine[] {
  const lines: ReportLine[] = [
    { text: "VEDHA SECURITY ASSESSMENT REPORT", heading: true },
    { text: "DRAFT / NOT APPROVED — HUMAN REVIEW REQUIRED", heading: true },
    { text: report.engagement.name, heading: true },
    labelled("Client", report.engagement.client),
    labelled("Engagement ID", report.engagement.id),
    labelled("Engagement status", report.engagement.status),
    labelled("Schema version", report.document.schema_version),
    labelled("Generated at", report.document.generated_at),
    labelled("Canonical timezone", report.document.timezone),
    labelled("Display timezone", report.document.display_timezone),
    labelled("Snapshot kind", report.document.snapshot_kind),
    labelled("Snapshot guarantee", report.document.snapshot_guarantee),
    labelled("Persisted", report.document.persisted),
    labelled("Assessment window", `${report.engagement.start_time ?? "Not recorded"} — ${report.engagement.end_time ?? "Not recorded"}`),
    labelled("Assessor", report.engagement.assessor),
    labelled("Scope", report.engagement.scope_cidrs.join(", ")),
    labelled("Excluded scope", report.engagement.excluded_cidrs.join(", ")),
    labelled("Engagement description", report.engagement.description),
    { text: "" },
    { text: "DOCUMENT CONTROL, METHODOLOGY, RISK AND LIMITATIONS", heading: true },
    labelled("Recorded report metadata", report.engagement.recorded_report_metadata),
    labelled("Regulatory profiles", report.engagement.regulatory_profiles),
    labelled("Engagement metadata gaps", report.engagement.metadata_gaps),
    { text: "Compliance mappings are recorded references only; this report does not claim certification or regulatory attestation." },
    { text: "" },
    { text: "DERIVED REGIONAL COMPLIANCE CONTEXT — NOT ASSESSED", heading: true },
    { text: "Derived context only. The following profile, frameworks, obligations, and reporting clocks are not assessed control results, a certification, an attestation, or legal advice." },
    labelled("Context source", report.derived_regional_compliance.source),
    labelled("Assessment status", report.derived_regional_compliance.assessment_status),
    labelled("Certification status", report.derived_regional_compliance.certification_status),
    labelled("Profile source", report.derived_regional_compliance.profile_source),
    labelled("Sector and jurisdictions", report.derived_regional_compliance.profile),
    labelled("Asset tags considered", report.derived_regional_compliance.asset_tags),
    labelled("Applicable regional frameworks", report.derived_regional_compliance.frameworks),
    labelled("Contextual reporting clocks", report.derived_regional_compliance.reporting_clocks),
    labelled("Regional compliance disclaimer", report.derived_regional_compliance.disclaimer),
    { text: "A listed reporting deadline is a contextual trigger reference; this report does not assert that an incident or notification trigger occurred." },
    { text: "" },
    { text: "EXECUTIVE SUMMARY", heading: true },
    labelled("Summary", report.summary),
    labelled("Readiness complete", report.readiness.complete),
    labelled("Readiness gap counts", report.readiness.gap_counts),
    labelled("Report readiness gaps", report.readiness.report_gaps),
    { text: "" },
    { text: "TECHNICAL FINDINGS", heading: true },
  ];

  report.findings.forEach((finding, index) => {
    lines.push(
      { text: `${index + 1}. [${finding.severity}] ${finding.title}`, heading: true },
      labelled("Finding ID", finding.id),
      labelled("Status", finding.status),
      labelled("Affected asset", finding.asset),
      labelled("CVSS", { score: finding.cvss_score, vector: finding.cvss_vector }),
      labelled("Risk and exploitability", {
        risk_score: finding.risk_score,
        epss_score: finding.epss_score,
        exploitable: finding.exploitable,
        exploit_validated: finding.exploit_validated,
        detection_status: finding.detection_status,
      }),
      labelled("Taxonomy", {
        cve_ids: finding.cve_ids,
        cwe_ids: finding.cwe_ids,
        mitre_techniques: finding.mitre_techniques,
      }),
      labelled("Description", finding.description),
      labelled("Technical details", finding.technical_details),
      labelled("Technical impact", finding.impact),
      labelled("Business impact", finding.business_impact),
      labelled("Exploitation context", finding.exploitation),
      labelled("Reproduction / validation steps", finding.reproduction_steps),
      labelled("Root cause", finding.root_cause),
      labelled("Preconditions", finding.preconditions),
      labelled("Finding timestamps", {
        first_seen: finding.first_seen,
        last_seen: finding.last_seen,
        created_at: finding.created_at,
        updated_at: finding.updated_at,
      }),
      labelled("Initial detection provenance", finding.initial_detection_provenance),
      labelled("Latest detection provenance", finding.latest_detection_provenance),
      labelled("Verification", finding.verification),
      labelled("Action tracking", finding.action_tracking),
      labelled("Current SLA projection", finding.current_sla),
      { text: "Evidence", heading: true },
    );
    if (finding.evidence.artifacts.length === 0) lines.push({ text: "No evidence artifacts recorded." });
    for (const artifact of finding.evidence.artifacts) {
      lines.push(labelled(`Evidence ${artifact.index} — ${artifact.label}`, {
        type: artifact.evidence_type,
        content: artifact.content,
        tool: artifact.tool,
        source: artifact.source,
        command: artifact.command,
        timestamp: artifact.timestamp,
        captured_at: artifact.captured_at,
        captured_by: artifact.captured_by,
        source_host: artifact.source_host,
        sha256: artifact.sha256,
        sha256_basis: artifact.sha256_basis,
        sha256_verified: artifact.sha256_verified,
        scan_result_id: artifact.scan_result_id,
        scan_job_id: artifact.scan_job_id,
        detection_run_id: artifact.detection_run_id,
        timestamp_basis: artifact.timestamp_basis,
      }));
    }
    lines.push(
      labelled("Evidence gaps", finding.evidence.gaps),
      { text: "Remediation and recommendations", heading: true },
      labelled("Recorded remediation", finding.remediation.recorded_text),
      labelled("Remediation provenance", {
        recorded_at: finding.remediation.recorded_text_timestamp,
        updated_by: finding.remediation.recorded_text_updated_by,
        timestamp_gap: finding.remediation.timestamp_gap,
      }),
      labelled("Reviewed remediation plans", finding.remediation.reviewed_plans),
      labelled("Structured recommendation records", finding.remediation.recommendations),
      labelled("Compatibility recommendation text", finding.remediation.recorded_recommendations),
      labelled("Remediation gaps", finding.remediation.gaps),
      { text: "Closure, retest and lifecycle", heading: true },
      labelled("Closure record", {
        disposition: finding.closure.current_disposition,
        terminal: finding.closure.is_terminal,
        resolved_at: finding.closure.resolved_at,
        resolution_method: finding.closure.resolution_method,
        resolution_run_id: finding.closure.resolution_run_id,
        resolution_miss_count: finding.closure.resolution_miss_count,
        reopened_count: finding.closure.reopened_count,
        reviewed_by: finding.closure.reviewed_by,
        latest_terminal_event: finding.closure.latest_terminal_event,
      }),
      labelled("Recorded closure evidence", finding.closure.recorded_closure_evidence),
      labelled("Auto-resolution coverage", finding.closure.auto_resolution_coverage),
      labelled("Retest record", finding.closure.retest),
      labelled("Lifecycle timeline", finding.lifecycle),
      labelled("Closure completeness gaps", finding.closure.completeness_gaps),
    );
    if (finding.closure.retest) {
      const retest = finding.closure.retest;
      lines.push(
        labelled("Retest result", retest.passed == null ? null : (retest.passed ? "Passed" : "Failed")),
        labelled("Retest timing", {
          requested_at: retest.requested_at,
          started_at: retest.started_at,
          completed_at: retest.completed_at,
          verified_at: retest.verified_at,
        }),
        labelled("Retest actors", { tested_by: retest.tested_by, verified_by: retest.verified_by }),
        labelled("Retest scope", retest.scope),
        labelled("Retest vantage point", retest.vantage_point),
        labelled("Retest authentication context", retest.authentication_context),
        labelled("Retest method", retest.method),
        labelled("Retest tool configuration", retest.tool_configuration),
        labelled("Retest expected result", retest.expected_result),
        labelled("Retest actual result", retest.actual_result),
        labelled("Retest coverage comparison", retest.coverage_comparison),
        labelled("Retest change reference", retest.change_reference),
        labelled("Retest residual risk", retest.residual_risk),
        labelled("Retest evidence integrity", {
          status: retest.integrity_status,
          gaps: retest.integrity_gaps,
        }),
        labelled("Before-remediation evidence", retest.before_evidence),
        labelled("After-remediation evidence", retest.after_evidence),
      );
    }
    lines.push({ text: "Compliance mappings", heading: true });
    if (finding.compliance_mappings.length === 0) lines.push({ text: "No compliance mappings recorded." });
    for (const mapping of finding.compliance_mappings) {
      lines.push(labelled(
        [mapping.framework, mapping.control_id, mapping.control_title].filter(Boolean).join(" · ") || "Recorded mapping",
        mapping,
      ));
    }
    lines.push(
      { text: "Derived compliance context — not assessed", heading: true },
      { text: "Derived context only. These pointers are separate from recorded mappings and are not a certification, attestation, legal conclusion, or recorded control result." },
      labelled("Derived source", finding.derived_compliance_context.source),
      labelled("Derived assessment status", finding.derived_compliance_context.assessment_status),
      labelled("Derived certification status", finding.derived_compliance_context.certification_status),
      labelled("Derived category", finding.derived_compliance_context.category),
      labelled("Derived themes", finding.derived_compliance_context.themes),
      labelled("Asset tags considered", finding.derived_compliance_context.asset_tags),
      labelled("Global framework control pointers", finding.derived_compliance_context.global_framework_pointers),
      labelled("Regional obligation pointers", finding.derived_compliance_context.regional_obligations),
    );
    if (finding.derived_compliance_context.used_generic_fallback) {
      lines.push({
        text: "Generic fallback warning: this finding category used the generic control-pointer set. Confirm the classification and control applicability before customer delivery.",
      });
    }
    lines.push(labelled("Finding readiness gaps", finding.readiness_gaps), { text: "" });
  });

  lines.push(
    { text: "CLOSURE REGISTER", heading: true },
    ...report.findings.map((finding) => labelled(finding.id, {
      title: finding.title,
      disposition: finding.closure.current_disposition,
      terminal: finding.closure.is_terminal,
      resolved_at: finding.closure.resolved_at,
      method: finding.closure.resolution_method,
      retest: finding.closure.retest,
      evidence: finding.closure.recorded_closure_evidence,
      completeness_gaps: finding.closure.completeness_gaps,
    })),
    { text: "" },
    { text: "COMPLIANCE CONTROL ROLLUP", heading: true },
    labelled("Mapping source", report.compliance_rollup.source),
    labelled("Recorded regulatory profiles", report.compliance_rollup.regulatory_profiles),
    labelled("Frameworks and controls", report.compliance_rollup.frameworks),
    labelled("Unmapped finding IDs", report.compliance_rollup.unmapped_finding_ids),
    labelled("Compliance rollup gap", report.compliance_rollup.gap),
    { text: "" },
    { text: "REPORT READINESS", heading: true },
    labelled("Complete", report.readiness.complete),
    labelled("Gap counts", report.readiness.gap_counts),
    labelled("Affected finding IDs", report.readiness.affected_finding_ids),
    labelled("Report gaps", report.readiness.report_gaps),
    { text: "This live document is not persisted, signed, approved, certified, or suitable for customer delivery until reviewed and issued through document control." },
  );
  return lines;
}

const PDF_FONT_NAME = "VedhaUnicode";
const PDF_FONT_PATH = path.join(process.cwd(), "public", "fonts", "unifont-17.0.05.otf");

/**
 * Generate the delivery PDF with an embedded, broad-coverage Unicode font.
 * PDFKit subsets the font and writes a Type0/CID font plus a ToUnicode CMap,
 * so both the visible glyphs and copied/extracted text preserve their code
 * points. The font lives in public/ because that directory is copied into the
 * production standalone image as well as local/server builds.
 */
function buildPdf(report: ReportDocument): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    const document = new PDFDocument({
      autoFirstPage: false,
      bufferPages: true,
      compress: true,
      margin: 48,
      pdfVersion: "1.4",
      size: "A4",
      info: {
        Title: `${plain(report.engagement.name)} security assessment report`,
        Author: "Vedha VAPT Platform",
        Subject: "Security assessment findings, evidence, remediation, closure and compliance",
        CreationDate: new Date(report.document.generated_at),
      },
    });
    const chunks: Buffer[] = [];
    document.on("data", (chunk: Buffer | Uint8Array) => chunks.push(Buffer.from(chunk)));
    document.once("error", reject);
    document.once("end", () => resolve(Buffer.concat(chunks)));
    document.registerFont(PDF_FONT_NAME, PDF_FONT_PATH);

    const pageWidth = 595.28;
    const contentWidth = pageWidth - 96;
    const contentBottom = 755;

    const addPage = () => {
      document.addPage({ size: "A4", margin: 48 });
      document.font(PDF_FONT_NAME).fillColor("#0f172a").fontSize(9);
    };

    addPage();
    for (const line of reportLines(report)) {
      const text = line.text || " ";
      const fontSize = line.heading ? 11 : 9;
      const lineGap = line.heading ? 2 : 1;
      document.font(PDF_FONT_NAME).fontSize(fontSize);
      const height = document.heightOfString(text, { width: contentWidth, lineGap });
      if (document.y + height > contentBottom) addPage();
      document
        .fillColor(line.heading ? "#163b72" : "#0f172a")
        .fontSize(fontSize)
        .text(text, 48, document.y, {
          width: contentWidth,
          lineGap,
        });
      document.y += line.heading ? 3 : 2;
    }

    const pageRange = document.bufferedPageRange();
    for (let index = pageRange.start; index < pageRange.start + pageRange.count; index += 1) {
      document.switchToPage(index);
      document
        .font(PDF_FONT_NAME)
        .fontSize(8)
        .fillColor("#475569")
        .text(
          `Page ${index - pageRange.start + 1} of ${pageRange.count} — Vedha VAPT Platform`,
          48,
          780,
          { width: contentWidth, lineBreak: false, align: "left" },
        );
    }
    document.end();
  });
}

function wordParagraph(text: string, heading = false): string {
  const style = heading
    ? `<w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="163B72"/><w:sz w:val="26"/></w:rPr><w:t xml:space="preserve">${xml(text)}</w:t></w:r>`
    : `<w:pPr><w:spacing w:after="100" w:line="276" w:lineRule="auto"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">${xml(text)}</w:t></w:r>`;
  return `<w:p>${style}</w:p>`;
}

function buildDocx(report: ReportDocument): Buffer {
  const body = reportLines(report).map((line) => wordParagraph(line.text, line.heading)).join("");
  return zip([
    { name: "[Content_Types].xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>` },
    { name: "_rels/.rels", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>` },
    { name: "docProps/core.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${xml(report.engagement.name)} security report</dc:title><dc:creator>Vedha VAPT Platform</dc:creator>${ooxmlCreated(report)}</cp:coreProperties>` },
    { name: "docProps/app.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Vedha VAPT Platform</Application></Properties>` },
    { name: "word/document.xml", data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>${body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>` },
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
        ? await buildPdf(report)
        : buildDocx(report);
  return {
    bytes,
    contentType: CONTENT_TYPES[format],
    filename: exportFilename(format, report),
  };
}
