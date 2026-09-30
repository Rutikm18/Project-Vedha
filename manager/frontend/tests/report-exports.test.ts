import assert from "node:assert/strict";
import { inflateRawSync, inflateSync } from "node:zlib";
import { describe, it } from "node:test";

import {
  buildReportExport,
  exportFilename,
  reportLines,
} from "../lib/report/export-files";
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

  it("creates a readable PDF carrying all canonical reporting sections", async () => {
    const file = await buildReportExport("pdf", canonicalReport);
    const text = file.bytes.toString("latin1");
    const sourceText = reportLines(canonicalReport).map((line) => line.text).join("\n");

    assert.equal(file.contentType, "application/pdf");
    assert.equal(file.bytes.subarray(0, 8).toString("ascii"), "%PDF-1.4");
    for (const marker of [
      "DRAFT / NOT APPROVED",
      "DOCUMENT CONTROL, METHODOLOGY, RISK AND LIMITATIONS",
      "External perimeter assessment",
      "TLSv1 accepted",
      "Disable TLS 1.0",
      "TLSv1 negotiation was rejected",
      "Structured recommendation records",
      "human_reviewed_plan",
      "Retest evidence integrity",
      "after_evidence_hash_mismatch",
      "mapping_review_required",
      "DERIVED REGIONAL COMPLIANCE CONTEXT — NOT ASSESSED",
      "recorded_engagement_profile",
      "RBI Cyber Security Framework in Banks",
      "RBI circular 2 Jun 2016 — report within 2–6 hours",
      "Derived compliance context — not assessed",
      "PCI DSS 4.0",
      "ISO/IEC 27001:2022",
      "NIST SP 800-53 Rev.5",
      "SOC 2 (TSC)",
      "HIPAA Security Rule",
      "Generic fallback warning",
      "COMPLIANCE CONTROL ROLLUP",
      "REPORT READINESS",
    ]) assert.match(sourceText, new RegExp(marker.replace(/[.*+?^{}()|[\]\\]/g, "\\$&")));
    assert.match(text, /\/Subtype\s*\/Type0/);
    assert.match(text, /\/FontFile3\s+\d+\s+0\s+R/);
    assert.match(text, /\/ToUnicode\s+\d+\s+0\s+R/);
    const pageCount = Number(text.match(/\/Type\s*\/Pages[\s\S]*?\/Count\s+(\d+)/)?.[1]);
    assert.ok(pageCount > 0 && pageCount <= 10, `unexpected PDF page count: ${pageCount}`);
    assert.doesNotMatch(sourceText, /evidence-secret-report-value/);
    assert.doesNotMatch(sourceText, /mapping-raw-must-not-render/);
    assert.match(text, /%%EOF\s*$/);
  });

  it("preserves Unicode report text in the PDF instead of replacing it with question marks", async () => {
    const unicodeReport = structuredClone(canonicalReport);
    unicodeReport.engagement.name = "München 東京";

    const file = await buildReportExport("pdf", unicodeReport);
    const bytes = file.bytes.toString("latin1");
    const streams = decodedPdfStreams(file.bytes);

    assert.match(bytes, /\/ToUnicode\s+\d+\s+0\s+R/);
    assert.match(streams, /<00fc>/i);
    assert.match(streams, /<6771>/i);
    assert.match(streams, /<4eac>/i);
    assert.doesNotMatch(bytes, /M\?nchen \?\?/);
  });

  it("creates a Word document with canonical control, evidence, closure and compliance detail", async () => {
    const file = await buildReportExport("docx", canonicalReport);
    const document = zipEntry(file.bytes, "word/document.xml").toString("utf8");
    const core = zipEntry(file.bytes, "docProps/core.xml").toString("utf8");

    for (const marker of [
      "DRAFT / NOT APPROVED",
      "External perimeter assessment",
      "TLSv1 accepted",
      "Disable TLS 1.0",
      "Retest actual result",
      "Structured recommendation records",
      "human_reviewed_plan",
      "Retest evidence integrity",
      "after_evidence_hash_mismatch",
      "mapping_review_required",
      "Weak protocol affects the recorded control objective",
      "DERIVED REGIONAL COMPLIANCE CONTEXT — NOT ASSESSED",
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
    ]) assert.match(document, new RegExp(marker.replace(/[.*+?^{}()|[\]\\]/g, "\\$&")));
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
