import assert from "node:assert/strict";
import { inflateRawSync, inflateSync } from "node:zlib";
import { describe, it } from "node:test";

import {
  buildReportExport,
  exportFilename,
} from "../lib/report/export-files";
import { renderReportPdf } from "../lib/report/export-pdf";
import { canonicalReport } from "./fixtures/canonical-report";

function zipEntry(bytes: Buffer, wanted: string): Buffer {
  let offset = 0;
  while (offset + 30 <= bytes.length && bytes.readUInt32LE(offset) === 0x04034b50) {
    const method = bytes.readUInt16LE(offset + 8);
    const compressedSize = bytes.readUInt32LE(offset + 18);
    const nameLength = bytes.readUInt16LE(offset + 26);
    const extraLength = bytes.readUInt16LE(offset + 28);
    const name = bytes.subarray(offset + 30, offset + 30 + nameLength).toString("utf8");
    const start = offset + 30 + nameLength + extraLength;
    const compressed = bytes.subarray(start, start + compressedSize);
    if (name === wanted) return method === 8 ? inflateRawSync(compressed) : compressed;
    offset = start + compressedSize;
  }
  throw new Error(`ZIP entry not found: ${wanted}`);
}

function decodedPdfStreams(bytes: Buffer): string {
  const source = bytes.toString("latin1");
  const streams: string[] = [];
  const pattern = /<<(?:[^>]|>(?!>))*?\/Length\s+(\d+)(?:[^>]|>(?!>))*?\/Filter\s*\/FlateDecode(?:[^>]|>(?!>))*?>>\s*stream\r?\n/g;
  let match: RegExpExecArray | null;
  while ((match = pattern.exec(source)) !== null) {
    const length = Number(match[1]);
    const start = pattern.lastIndex;
    streams.push(inflateSync(bytes.subarray(start, start + length)).toString("latin1"));
    pattern.lastIndex = start + length;
  }
  return streams.join("\n");
}

describe("canonical report exports", () => {
  it("creates a documented flat findings tracker with closure, compliance and readiness fields", async () => {
    const file = await buildReportExport("csv", canonicalReport);
    const text = file.bytes.toString("utf8");

    assert.equal(file.contentType, "text/csv; charset=utf-8");
    assert.ok(text.startsWith("\uFEFF\"Document generated at\",\"Document status\",\"Snapshot kind\",\"Snapshot guarantee\","));
    assert.match(text, /DRAFT \/ NOT APPROVED/);
    assert.match(text, /repeatable_read/);
    assert.match(text, /current_effective_tenant_policy/);
    assert.match(text, /finding_assignee/);
    assert.match(text, /unreviewed_recorded/);
    assert.match(text, /after_evidence_hash_mismatch/);
    assert.match(text, /mapping_review_required/);
    assert.match(text, /Closure evidence count/);
    assert.match(text, /bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/);
    assert.match(text, /ISO\/IEC 27001:A\.8\.24/);
    assert.match(text, /Derived compliance source/);
    assert.match(text, /derived_context_only/);
    assert.match(text, /not_assessed/);
    assert.match(text, /not_a_certification/);
    assert.match(text, /weak_tls/);
    assert.match(text, /PCI DSS 4\.0/);
    assert.match(text, /NIST SP 800-53 Rev\.5/);
    assert.match(text, /SOC 2 \(TSC\)/);
    assert.match(text, /HIPAA Security Rule/);
    assert.match(text, /RBI Cyber Security Framework in Banks/);
    assert.match(text, /generic/);
    assert.match(text, /true/);
    assert.match(text, /closure_review_metadata_absent/);
    assert.doesNotMatch(text, /evidence-secret-report-value/);
    assert.doesNotMatch(text, /TLSv1 accepted/);
  });

  it("neutralizes spreadsheet formulas in the CSV tracker", async () => {
    const hostile = structuredClone(canonicalReport);
    hostile.findings[0]!.title = "=WEBSERVICE(\"https://example.invalid\")";

    const text = (await buildReportExport("csv", hostile)).bytes.toString("utf8");

    assert.match(text, /\"'=WEBSERVICE\(\"\"https:\/\/example\.invalid\"\"\)\"/);
  });

  it("adds a Coverage sheet that separates evaluated-clean from not-checked rules", async () => {
    const report = {
      ...canonicalReport,
      coverage_sheet: {
        run_id: "run-1", run_finished_at: "2026-09-26T08:00:00Z", vuln_db_version: "db-1",
        scan_reference: "SCAN-1", scan_use_case: "internal_vuln", scan_intensity: "normal",
        ports_scanned: [22, 443], ports_scanned_note: null,
        rules_total: 2, rules_evaluated_clean: 1, rules_with_finding: 0, rules_not_checked: 1, rules_could_not_assess: 0,
        rules: [
          { rule_id: "POSTURE-A", title: "A", verdict: "evaluated_clean", reasons: [] },
          { rule_id: "POSTURE-B", title: "B", verdict: "no_evidence_collected", reasons: [] },
        ],
        interpretation: "evaluated_clean means the check ran.",
      },
    } as typeof canonicalReport;
    const file = await buildReportExport("xlsx", report);
    const workbook = zipEntry(file.bytes, "xl/workbook.xml").toString("utf8");
    assert.match(workbook, /name="Coverage"/);
    const sheet = zipEntry(file.bytes, "xl/worksheets/sheet11.xml").toString("utf8");
    assert.match(sheet, /no_evidence_collected/);
    assert.match(sheet, /ports scanned: 22, 443/);
    assert.doesNotMatch(
      zipEntry((await buildReportExport("xlsx", canonicalReport)).bytes, "xl/workbook.xml").toString("utf8"),
      /name="Coverage"/);
  });

  it("creates a multi-sheet workbook with canonical metadata and detailed registers", async () => {
    const file = await buildReportExport("xlsx", canonicalReport);
    const workbook = zipEntry(file.bytes, "xl/workbook.xml").toString("utf8");
    const core = zipEntry(file.bytes, "docProps/core.xml").toString("utf8");

    for (const sheet of [
      "Overview", "Findings", "Evidence", "Remediation",
      "Closure", "Compliance", "Control Rollup", "Gaps",
      "Derived Context", "Regional Context",
    ]) {
      assert.match(workbook, new RegExp(`name="${sheet}"`));
    }
    assert.match(core, /2026-09-26T08:30:00\.000Z/);
    const overview = zipEntry(file.bytes, "xl/worksheets/sheet1.xml").toString("utf8");
    const evidence = zipEntry(file.bytes, "xl/worksheets/sheet3.xml").toString("utf8");
    const remediation = zipEntry(file.bytes, "xl/worksheets/sheet4.xml").toString("utf8");
    const closure = zipEntry(file.bytes, "xl/worksheets/sheet5.xml").toString("utf8");
    const compliance = zipEntry(file.bytes, "xl/worksheets/sheet6.xml").toString("utf8");
    const derivedContext = zipEntry(file.bytes, "xl/worksheets/sheet9.xml").toString("utf8");
    const regionalContext = zipEntry(file.bytes, "xl/worksheets/sheet10.xml").toString("utf8");
    assert.match(overview, /Snapshot guarantee/);
    assert.match(overview, /repeatable_read/);
    assert.match(overview, /Derived regional profile source/);
    assert.match(overview, /recorded_engagement_profile/);
    assert.match(overview, /not_assessed/);
    assert.match(overview, /not_a_certification/);
    assert.match(evidence, /TLSv1 accepted/);
    assert.match(evidence, /retest_before/);
    assert.match(evidence, /Before-fix TLS capture/);
    assert.match(evidence, /retest_after/);
    assert.match(evidence, /After-fix TLS capture/);
    assert.match(evidence, /SHA-256 basis/);
    assert.match(evidence, /canonical_json_content/);
    assert.match(remediation, /Disable TLS 1\.0/);
    assert.match(remediation, /human_reviewed_plan/);
    assert.match(closure, /TLSv1 negotiation was rejected/);
    assert.match(closure, /after_evidence_hash_mismatch/);
    assert.match(compliance, /Weak protocol affects/);
    assert.match(compliance, /mapping_review_required/);
    assert.match(zipEntry(file.bytes, "xl/worksheets/sheet8.xml").toString("utf8"), /closure_review_metadata_absent/);
    assert.match(derivedContext, /Global framework pointers/);
    assert.match(derivedContext, /PCI DSS 4\.0/);
    assert.match(derivedContext, /NIST SP 800-53 Rev\.5/);
    assert.match(derivedContext, /SOC 2 \(TSC\)/);
    assert.match(derivedContext, /HIPAA Security Rule/);
    assert.match(derivedContext, /Generic fallback/);
    assert.match(derivedContext, />true</);
    assert.match(regionalContext, /RBI Cyber Security Framework in Banks/);
    assert.match(regionalContext, /CERT-In Directions 2022/);
    assert.match(regionalContext, /Digital Personal Data Protection Act and Rules/);
    assert.match(regionalContext, /RBI circular 2 Jun 2016 — report within 2–6 hours/);
    assert.match(regionalContext, /DPDP Rules 2025 — breach intimation/);
    assert.match(regionalContext, /not legal advice or a compliance attestation/);
    assert.doesNotMatch(file.bytes.toString("latin1"), /evidence-secret-report-value/);
  });

  it("creates a designed PDF report carrying every canonical section, masked", async () => {
    const file = await buildReportExport("pdf", canonicalReport);
    const bytes = file.bytes.toString("latin1");
    const { text: trace } = await renderReportPdf(canonicalReport);
    const text = trace.join("\n");

    assert.equal(file.contentType, "application/pdf");
    assert.equal(file.bytes.subarray(0, 8).toString("ascii"), "%PDF-1.4");
    for (const marker of [
      "Vulnerability Assessment Report",
      "DRAFT / NOT APPROVED — HUMAN REVIEW REQUIRED",
      "Document control",
      "Contents",
      "1  Executive summary",
      "OVERALL RISK",
      "2  Scope and methodology",
      "External perimeter assessment",
      "CVSS plus recorded business context",
      "3  Findings overview",
      "4  Detailed findings",
      "TLSv1 accepted",
      "Disable TLS 1.0",
      "TLSv1 negotiation was rejected",
      "Recommendations:",
      "Retest evidence integrity",
      "after_evidence_hash_mismatch",
      "5  Remediation roadmap",
      "6  Retest and closure register",
      "7  Compliance context",
      "mapping_review_required",
      "Derived regional compliance context — not assessed",
      "Recorded engagement profile",
      "RBI Cyber Security Framework in Banks",
      "RBI circular 2 Jun 2016 — report within 2–6 hours",
      "Derived compliance context — not assessed",
      "PCI DSS 4.0",
      "ISO/IEC 27001:2022",
      "NIST SP 800-53 Rev.5",
      "SOC 2 (TSC)",
      "HIPAA Security Rule",
      "Generic fallback warning",
      "Appendix A — Risk rating",
      "Appendix D — Record readiness",
      "closure_review_metadata_absent",
      "repeatable_read",
    ]) assert.ok(text.includes(marker), `PDF is missing: ${marker}`);
    // Recorded values read as prose and tables, never as JSON dumps.
    assert.doesNotMatch(text, /\{"[a-z_]+":/);
    assert.doesNotMatch(text, /evidence-secret-report-value/);
    assert.doesNotMatch(text, /description-secret-report-value/);
    assert.doesNotMatch(text, /must-not-render/);
    assert.match(bytes, /\/Subtype\s*\/Type0/);
    assert.match(bytes, /\/FontFile2\s+\d+\s+0\s+R/);
    assert.match(bytes, /\/ToUnicode\s+\d+\s+0\s+R/);
    assert.match(bytes, /\/Outlines\s+\d+\s+0\s+R/);
    const pageCount = Number(bytes.match(/\/Type\s*\/Pages[\s\S]*?\/Count\s+(\d+)/)?.[1]);
    assert.ok(pageCount > 8 && pageCount <= 30, `unexpected PDF page count: ${pageCount}`);
    assert.match(bytes, /%%EOF\s*$/);
  });

  it("reports an issue found on many assets once, with its affected assets", async () => {
    const many = structuredClone(canonicalReport);
    const base = many.findings[0]!;
    many.findings = Array.from({ length: 40 }, (_, i) => ({
      ...structuredClone(base),
      id: `aaaaaaaa-0000-4000-8000-${String(i).padStart(12, "0")}`,
      title: "SMB signing not required",
      status: "open",
      asset: { ...base.asset!, id: `asset-${i}`, ip_address: `192.0.2.${i + 1}`, hostname: null, fqdn: null },
    }));
    const { text } = await renderReportPdf(many);
    const joined = text.join("\n");
    assert.ok(joined.includes("F001–F040"), "the issue is referenced as one range");
    assert.ok(joined.includes("40 affected assets"), "the asset count is stated");
    assert.ok(joined.includes("192.0.2.40"), "every affected asset is listed");
    assert.equal(text.filter((t) => t === "SMB signing not required").length <= 6, true, "the issue title is not repeated per asset");
  });

  it("preserves Unicode report text in the PDF instead of replacing it with question marks", async () => {
    const unicodeReport = structuredClone(canonicalReport);
    unicodeReport.engagement.name = "München 東京";

    const file = await buildReportExport("pdf", unicodeReport);
    const bytes = file.bytes.toString("latin1");
    const streams = decodedPdfStreams(file.bytes);

    assert.match(bytes, /\/ToUnicode\s+\d+\s+0\s+R/);
    // Plex draws the Latin text; the bundled Unifont draws what Plex lacks.
    assert.match(bytes, /\/FontFile3\s+\d+\s+0\s+R/);
    assert.match(streams, /<00fc>/i);
    assert.match(streams, /<6771>/i);
    assert.match(streams, /<4eac>/i);
    assert.doesNotMatch(bytes, /M\?nchen \?\?/);
  });

  it("creates a styled Word document with contents, header, footer and every canonical section", async () => {
    const file = await buildReportExport("docx", canonicalReport);
    const document = zipEntry(file.bytes, "word/document.xml").toString("utf8");
    const styles = zipEntry(file.bytes, "word/styles.xml").toString("utf8");
    const footer = zipEntry(file.bytes, "word/footer1.xml").toString("utf8");
    const header = zipEntry(file.bytes, "word/header1.xml").toString("utf8");
    const core = zipEntry(file.bytes, "docProps/core.xml").toString("utf8");

    for (const marker of [
      "DRAFT / NOT APPROVED",
      "External perimeter assessment",
      "TLSv1 accepted",
      "Disable TLS 1.0",
      "Retest actual result",
      "Recommendations:",
      "Retest evidence integrity",
      "after_evidence_hash_mismatch",
      "mapping_review_required",
      "Weak protocol affects the recorded control objective",
      "Derived regional compliance context — not assessed",
      "RBI Cyber Security Framework in Banks",
      "CERT-In Directions 2022",
      "DPDP Rules 2025 — breach intimation",
      "Derived compliance context — not assessed",
      "PCI DSS 4.0",
      "ISO/IEC 27001:2022",
      "NIST SP 800-53 Rev.5",
      "SOC 2 (TSC)",
      "HIPAA Security Rule",
      "Generic fallback warning",
      "closure_review_metadata_absent",
    ]) assert.ok(document.includes(marker), `Word document is missing: ${marker}`);
    for (const style of ["Heading1", "Heading2", "Heading3", "VedhaTable", "Code", "NoteCaution", "TOC1"]) {
      assert.match(styles, new RegExp(`w:styleId="${style}"`));
    }
    assert.match(document, /<w:pStyle w:val="Heading1"\/>/);
    assert.match(document, /TOC \\o/);
    assert.match(document, /<w:tblHeader\/>/);
    assert.match(footer, /NUMPAGES/);
    assert.match(header, /CONFIDENTIAL/);
    assert.doesNotMatch(document, /\{&quot;[a-z_]+&quot;:/);
    assert.match(core, /2026-09-26T08:30:00\.000Z/);
    assert.doesNotMatch(document, /evidence-secret-report-value/);
    assert.doesNotMatch(document, /must-not-render/);
  });

  it("uses a filesystem-safe, engagement-specific filename", () => {
    const renamed = structuredClone(canonicalReport);
    renamed.engagement.name = "Q3 / perimeter: review";
    assert.equal(exportFilename("docx", renamed), "vedha-q3-perimeter-review-report.docx");
  });
});
