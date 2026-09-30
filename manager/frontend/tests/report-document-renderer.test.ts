import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { CanonicalReportDocument } from "../components/report/CanonicalReportDocument";
import type {
  ReportDocument,
  ReportFinding,
  ReportFindingEvent,
  ReportRegulatoryProfile,
} from "../lib/report/report-document";

const GENERATED_AT = "2026-09-26T08:30:00Z";
const DESCRIPTION_SECRET = "description-secret-report-value";
const EVIDENCE_SECRET = "evidence-secret-report-value";
const EVENT_SECRET = "event-secret-report-value";
const PROVENANCE_SECRET = "provenance-secret-report-value";
const RETEST_SECRET = "retest-secret-report-value";
const ACTION_SECRET = "action-secret-report-value";
const REGULATORY_SECRET = "regulatory-secret-report-value";
const BEARER = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.dBjftJeZ4CVP";

const regulatoryProfiles: ReportRegulatoryProfile[] = [{
  profile_id: "CERT-IN-CCSAPG-1.0-2025",
  name: "CERT-In Comprehensive Cyber Security Audit Policy Guidelines",
  version: "1.0 / 25.07.2025",
  jurisdiction: "India",
  applicability: "Selected as the customer-recorded audit basis",
  rationale: "Selected from the customer's recorded applicability decision",
  source_url: "https://www.cert-in.org.in/PDF/Comprehensive_Cyber_Security_Audit_Policy_Guidelines.pdf",
  scope: { entities: ["Example Corp"], systems: ["Internet perimeter"], api_key: REGULATORY_SECRET },
  selected_by: "assessor-1",
  selected_at: "2026-09-19T08:00:00Z",
  reviewed_by: "reviewer-1",
  reviewed_at: "2026-09-19T09:00:00Z",
  limitations: "Customer-recorded selection only; empanelment and conditional annexures are not inferred",
  recorded_reference: "REG-PROFILE-001",
}];

const terminalEvent: ReportFindingEvent = {
  id: "33333333-3333-4333-8333-333333333333",
  event_type: "remediated",
  label: "Remediated",
  actor: "operator-1",
  actor_type: "user",
  from_status: "open",
  to_status: "remediated",
  detail: {
    reason: "Authorized retest passed",
    api_key: EVENT_SECRET,
  },
  occurred_at: "2026-09-25T10:00:00Z",
  synthesized: false,
};

function finding(id: string, title: string): ReportFinding {
  return {
    id,
    title,
    description: `Recorded description password=${DESCRIPTION_SECRET}`,
    technical_details: "The endpoint completed a deprecated TLS handshake.",
    impact: "Recorded technical impact",
    business_impact: "Recorded customer impact",
    exploitation: "An on-path attacker can attempt protocol downgrade.",
    reproduction_steps: ["Offer TLS 1.0", "Observe a successful handshake"],
    root_cause: "Deprecated protocol remains enabled in server policy.",
    preconditions: ["Network access to the endpoint"],
    severity: "high",
    status: "remediated",
    asset: {
      id: "44444444-4444-4444-8444-444444444444",
      ip_address: "192.0.2.10",
      hostname: "edge-01",
      fqdn: "edge-01.example.test",
      os: "Linux",
      os_version: "12",
      asset_type: "server",
      criticality: "high",
      owner: "Platform",
      environment: "production",
      tags: { zone: "external" },
      last_seen: "2026-09-25T09:00:00Z",
    },
    cve_ids: ["CVE-2026-0001"],
    cwe_ids: ["CWE-326"],
    mitre_techniques: ["T1040"],
    cvss_score: 7.5,
    cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L",
    epss_score: 0.1,
    risk_score: 750,
    exploitable: true,
    exploit_validated: false,
    detection_status: "detected",
    first_seen: "2026-09-20T08:30:00Z",
    last_seen: "2026-09-24T08:30:00Z",
    initial_detection_run_id: "55555555-5555-4555-8555-555555555551",
    detection_run_id: "55555555-5555-4555-8555-555555555552",
    initial_detection_provenance: {
      role: "initial_discovery",
      run_id: "55555555-5555-4555-8555-555555555551",
      scan_result_id: "77777777-7777-4777-8777-777777777771",
      scan_job_id: "88888888-8888-4888-8888-888888888881",
      scan_attempt_id: "99999999-9999-4999-8999-999999999991",
      agent_id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
      scan_type: "vulnerability",
      scan_result_checksum: "sha256:initial-result",
      scan_result_validation_state: "validated",
      scan_result_recorded_at: "2026-09-20T08:29:59Z",
      trigger: "scheduled",
      status: "completed",
      vuln_db_version: "sha256:db-initial",
      vuln_db_fetched_at: "2026-09-20T07:00:00Z",
      started_at: "2026-09-20T08:00:00Z",
      finished_at: "2026-09-20T08:30:00Z",
      facts_count: 12,
      findings_new: 1,
      findings_reaffirmed: 0,
      findings_current: 1,
      recorded_coverage: { targets: 1 },
      recorded_stats: { password: PROVENANCE_SECRET },
    },
    latest_detection_provenance: {
      role: "latest_observation",
      run_id: "55555555-5555-4555-8555-555555555552",
      scan_result_id: "77777777-7777-4777-8777-777777777772",
      scan_job_id: "88888888-8888-4888-8888-888888888882",
      scan_attempt_id: "99999999-9999-4999-8999-999999999992",
      agent_id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa2",
      scan_type: "revalidation",
      scan_result_checksum: "sha256:latest-result",
      scan_result_validation_state: "validated",
      scan_result_recorded_at: "2026-09-24T08:29:59Z",
      trigger: "manual",
      status: "completed",
      vuln_db_version: "sha256:db-latest",
      vuln_db_fetched_at: "2026-09-24T07:00:00Z",
      started_at: "2026-09-24T08:00:00Z",
      finished_at: "2026-09-24T08:30:00Z",
      facts_count: 14,
      findings_new: 0,
      findings_reaffirmed: 1,
      findings_current: 1,
      recorded_coverage: { targets: 1 },
      recorded_stats: { duration_seconds: 1800 },
    },
    detected_db_version: "sha256:db-v1",
    created_at: "2026-09-20T08:30:00Z",
    updated_at: "2026-09-25T10:00:00Z",
    verification: {
      state: "confirmed",
      confidence: 95,
      rationale: "Two observations",
      method: "passive",
      needs_review: false,
    },
    action_tracking: {
      assigned_to_user_id: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa3",
      assigned_to_email: "platform-owner@example.test",
      owner: "Platform",
      owner_source: "finding_assignee",
      asset_owner: "Platform operations",
      non_closure_reason: `A scheduled change window was required before closure; api_key=${ACTION_SECRET}`,
      planned_closure_at: "2026-09-25T10:00:00Z",
      action_reference: "CHG-2026-0042",
      recorded_at: "2026-09-21T10:00:00Z",
    },
    evidence: {
      raw: { password: "must-not-render" },
      artifacts: [{
        index: 1,
        label: "Scanner output",
        content: `password=${EVIDENCE_SECRET}\nTLSv1 accepted`,
        evidence_type: "scanner_output",
        tool: "testssl",
        source: "assessment-run",
        command: `curl -H "Authorization: Bearer ${BEARER}" https://example.test`,
        timestamp: "2026-09-20T10:00:00+05:30",
        captured_at: null,
        captured_by: "operator-1",
        source_host: "probe-01",
        sha256: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        sha256_basis: "canonical_json_content",
        sha256_verified: true,
        scan_result_id: "aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa",
        scan_job_id: "bbbbbbbb-1111-4111-8111-bbbbbbbbbbbb",
        detection_run_id: "cccccccc-1111-4111-8111-cccccccccccc",
        timestamp_basis: "manager_recorded",
      }],
      gaps: [],
    },
    remediation: {
      recorded_text: "Disable TLS 1.0.",
      recorded_text_timestamp: "2026-09-24T07:30:00Z",
      recorded_text_updated_by: "assessor-1",
      timestamp_gap: null,
      reviewed_plans: [{
        id: "66666666-6666-4666-8666-666666666666",
        os: "linux",
        source: "reviewed_plan",
        reviewed: true,
        generated_at: "2026-09-24T08:30:00Z",
        model: "reviewed-model",
        summary: "Disable the weak protocol",
        effort: "low",
        remediation_risk: "medium",
        steps: [{ step: 1, action: "Update server policy" }],
        verification: ["Run the authorized TLS scanner again"],
        long_term_recommendations: ["Baseline cryptographic policy"],
        compensating_controls: "Restrict network access until patched",
        raw: { api_key: "must-not-render" },
      }],
      recommendations: [{
        text: "Continuously monitor protocol configuration",
        source_type: "finding_evidence",
        source_id: "aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa",
        author: "assessor-1",
        reviewer: null,
        recorded_at: "2026-09-24T07:30:00Z",
        generated_at: null,
        reviewed_at: null,
        review_state: "unreviewed_recorded",
      }, {
        text: "Baseline cryptographic policy",
        source_type: "reviewed_remediation_plan",
        source_id: "66666666-6666-4666-8666-666666666666",
        author: null,
        reviewer: "reviewer-1",
        recorded_at: null,
        generated_at: "2026-09-24T08:30:00Z",
        reviewed_at: "2026-09-24T09:00:00Z",
        review_state: "human_reviewed_plan",
      }],
      recorded_recommendations: ["Continuously monitor protocol configuration"],
      gaps: [],
    },
    compliance_mappings: [{
      source_key: "compliance_mappings",
      mapping_id: "MAP-001",
      framework: "ISO/IEC 27001",
      framework_version: "2022",
      release: "2024-01",
      profile: "Customer baseline",
      control_id: "A.8.24",
      control_title: "Use of cryptography",
      relationship: "supports",
      rationale: "Weak protocol affects the recorded control objective",
      applicability: "applicable",
      assessment_status: "fail",
      result: "fail",
      test_ids: ["TEST-7"],
      scope: { zone: "external" },
      context: { service: "TLS" },
      source_url: "https://example.test/mapping/MAP-001",
      mapping_source: "customer_control_register",
      mapping_version: "3",
      mapped_by: "assessor-1",
      mapped_at: "2026-09-20T10:00:00Z",
      reviewed_by: "reviewer-1",
      reviewed_at: "2026-09-21T10:00:00Z",
      limitations: "Sampling only",
      customer_statement: "Control requires remediation",
      assessor: "Vedha Security",
      assessed_at: "2026-09-20T10:00:00Z",
      evidence_references: ["F001/E01"],
      recorded_reference: "ISO-REF-1",
      raw: { api_key: "mapping-raw-must-not-render" },
      rollup_usable: false,
      validation_gaps: ["mapping_review_required"],
    }],
    lifecycle: [terminalEvent],
    closure: {
      current_disposition: "remediated",
      is_terminal: true,
      resolved_at: "2026-09-25T10:00:00Z",
      resolution_method: "manual",
      resolution_run_id: null,
      resolution_miss_count: 0,
      reopened_count: 0,
      reviewed_by: "reviewer-closure-1",
      latest_terminal_event: terminalEvent,
      terminal_and_reopen_history: [terminalEvent],
      recorded_closure_evidence: {
        raw: null,
        artifacts: [{
          index: 1,
          label: "Post-fix scan",
          content: "TLSv1 rejected",
          evidence_type: "retest",
          tool: "testssl",
          source: "manual-retest",
          command: null,
          timestamp: "2026-09-25T09:55:00Z",
          captured_at: null,
          captured_by: "operator-1",
          source_host: "probe-01",
          sha256: "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
          sha256_basis: "canonical_json_content",
          sha256_verified: true,
        }],
        gaps: [],
      },
      retest: {
        passed: true,
        requested_at: "2026-09-25T09:00:00Z",
        started_at: "2026-09-25T09:15:00Z",
        completed_at: "2026-09-25T09:55:00Z",
        verified_at: "2026-09-25T09:58:00Z",
        tested_by: "operator-1",
        verified_by: "reviewer-closure-1",
        scope: { hosts: ["192.0.2.10"], ports: [443] },
        vantage_point: "external probe",
        authentication_context: `api_key=${RETEST_SECRET}`,
        method: "Repeat the original TLS protocol check",
        tool_configuration: { authorization: `Bearer ${BEARER}`, profile: "strict" },
        expected_result: "TLSv1 negotiation is rejected",
        actual_result: "TLSv1 negotiation was rejected",
        coverage_comparison: { before: 1, after: 1, equivalent: true },
        change_reference: "CHG-2026-0042",
        residual_risk: "No weak-protocol exposure observed in the recorded scope",
        before_evidence: {
          raw: { api_key: "before-raw-must-not-render" },
          artifacts: [{
            index: 1,
            label: "Before-fix TLS capture",
            content: `TLSv1 accepted password=${RETEST_SECRET}`,
            evidence_type: "retest_before",
            tool: "testssl",
            source: "manual-retest",
            command: `curl -H "Authorization: Bearer ${BEARER}" https://example.test`,
            timestamp: "2026-09-25T09:20:00Z",
            captured_at: "2026-09-25T09:20:05Z",
            captured_by: "operator-1",
            source_host: "probe-01",
            sha256: "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
            sha256_basis: "canonical_json_content",
            sha256_verified: true,
          }],
          gaps: [],
        },
        after_evidence: {
          raw: { secret: "after-raw-must-not-render" },
          artifacts: [{
            index: 1,
            label: "After-fix TLS capture",
            content: `TLSv1 rejected api_key=${RETEST_SECRET}`,
            evidence_type: "retest_after",
            tool: "testssl",
            source: "manual-retest",
            command: null,
            timestamp: "2026-09-25T09:55:00Z",
            captured_at: "2026-09-25T09:55:05Z",
            captured_by: "operator-1",
            source_host: "probe-01",
            sha256: "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            sha256_basis: "canonical_json_content",
            sha256_verified: false,
          }],
          gaps: [],
        },
        integrity_status: "unverified",
        integrity_gaps: ["after_evidence_hash_mismatch"],
      },
      auto_resolution_coverage: null,
      completeness_gaps: ["closure_review_metadata_absent"],
    },
    current_sla: {
      derived: true,
      historical: false,
      policy_basis: "approved_deadline_extension",
      deadline_source: "extension",
      calculated_at: GENERATED_AT,
      state: "closed",
      deadline: null,
      hours_remaining: null,
      hours_total: 72,
    },
    readiness_gaps: ["closure_review_metadata_absent"],
  };
}

const report: ReportDocument = {
  document: {
    schema_version: "1.0",
    generated_at: GENERATED_AT,
    timezone: "UTC",
    display_timezone: "Asia/Kolkata",
    snapshot_kind: "postgresql_repeatable_read_read_only",
    snapshot_guarantee: "repeatable_read",
    persisted: false,
  },
  engagement: {
    id: "11111111-1111-4111-8111-111111111111",
    name: "Customer perimeter assessment",
    status: "completed",
    scope_cidrs: ["192.0.2.0/24"],
    excluded_cidrs: ["192.0.2.254/32"],
    start_time: "2026-09-19T08:30:00Z",
    end_time: "2026-09-25T08:30:00Z",
    created_at: "2026-09-18T08:30:00Z",
    updated_at: "2026-09-26T07:30:00Z",
    client: "Example Corp",
    assessor: "Vedha Security",
    description: "External perimeter assessment",
    tags: ["external"],
    recorded_report_metadata: {
      version: "1.0",
      document_status: "Draft",
      classification: "Confidential",
      prepared_by: "assessor-1",
      prepared_at: "2026-09-26T07:00:00Z",
      reviewed_by: "reviewer-1",
      reviewed_at: "2026-09-26T07:30:00Z",
      approved_by: "approver-1",
      approved_at: "2026-09-26T08:00:00Z",
      issue_date: "2026-09-26T08:15:00Z",
      reporting_period: "2026-09-19 through 2026-09-25",
      methodology: "Recorded methodology",
      risk_rating_method: "CVSS plus recorded business context",
      tools_used: "testssl, Nmap",
      testing_narrative: "External testing from the recorded assessment probe",
      segmentation_results: "Segmentation boundary tested as recorded",
      environment_cleanup: "Temporary test artifacts removed",
      evidence_retention_policy: "Retain approved evidence for 12 months",
      distribution: "Named customer security contacts only",
      report_timezone: "Asia/Kolkata",
      limitations: "Recorded limitations",
    },
    regulatory_profiles: regulatoryProfiles,
    metadata_gaps: [],
  },
  summary: {
    total_findings: 2,
    by_severity: { critical: 0, high: 2, medium: 0, low: 0, info: 0 },
    by_status: { open: 0, confirmed: 0, remediated: 2, accepted: 0, fp: 0 },
    by_severity_status: {
      critical: { open: 0, confirmed: 0, remediated: 0, accepted: 0, fp: 0 },
      high: { open: 0, confirmed: 0, remediated: 2, accepted: 0, fp: 0 },
      medium: { open: 0, confirmed: 0, remediated: 0, accepted: 0, fp: 0 },
      low: { open: 0, confirmed: 0, remediated: 0, accepted: 0, fp: 0 },
      info: { open: 0, confirmed: 0, remediated: 0, accepted: 0, fp: 0 },
    },
    open_by_severity: { critical: 0, high: 0, medium: 0, low: 0, info: 0 },
    terminal_by_severity: { critical: 0, high: 2, medium: 0, low: 0, info: 0 },
    open_or_confirmed: 0,
    terminal: 2,
    auto_resolved: 0,
    manual_remediated: 2,
    findings_with_reopen_history: 0,
  },
  findings: [
    finding("22222222-2222-4222-8222-222222222221", "First complete finding"),
    finding("22222222-2222-4222-8222-222222222222", "Second complete finding"),
  ],
  compliance_rollup: {
    source: "recorded_finding_mappings_only",
    mapping_count: 2,
    regulatory_profiles: regulatoryProfiles,
    frameworks: [{
      framework: "ISO/IEC 27001",
      framework_version: "2022",
      mapping_count: 2,
      finding_count: 2,
      controls: [{
        control_id: "A.8.24",
        control_title: "Use of cryptography",
        finding_ids: [
          "22222222-2222-4222-8222-222222222221",
          "22222222-2222-4222-8222-222222222222",
        ],
        recorded_results: ["fail"],
      }],
    }],
    unmapped_finding_ids: [],
    gap: null,
  },
  readiness: {
    complete: false,
    gap_counts: { closure_review_metadata_absent: 2 },
    affected_finding_ids: {
      closure_review_metadata_absent: [
        "22222222-2222-4222-8222-222222222221",
        "22222222-2222-4222-8222-222222222222",
      ],
    },
    report_gaps: [],
  },
};

describe("canonical report renderer", () => {
  test("mounts every canonical finding and preserves the exact generation timestamp", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.equal((html.match(/class="cr-finding"/g) ?? []).length, report.findings.length);
    assert.match(html, new RegExp(GENERATED_AT));
    assert.match(html, new RegExp(`<code>${GENERATED_AT}</code> UTC`));
    assert.match(html, /LIVE, NON-PERSISTED OPERATOR DRAFT/);
    assert.match(html, /postgresql_repeatable_read_read_only/);
    assert.match(html, /guarantee: repeatable_read/);
    assert.match(html, /First complete finding/);
    assert.match(html, /Second complete finding/);
    for (const item of report.findings) {
      assert.match(html, new RegExp(`id="finding-${item.id}"`));
    }
  });

  test("renders configured-timezone dates while retaining canonical UTC ISO values", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Asia\/Kolkata/);
    assert.match(html, /14:00:00/);
    assert.match(html, /2026-09-26T08:30:00\.000Z/);
    assert.match(html, new RegExp(`<code>${GENERATED_AT}</code> UTC`));
  });

  test("renders standard document control and assessment-method metadata", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Document status/);
    assert.match(html, /Draft/);
    assert.match(html, /assessor-1/);
    assert.match(html, /reviewer-1/);
    assert.match(html, /approver-1/);
    assert.match(html, /CVSS plus recorded business context/);
    assert.match(html, /testssl, Nmap/);
    assert.match(html, /External testing from the recorded assessment probe/);
    assert.match(html, /Segmentation boundary tested as recorded/);
    assert.match(html, /Temporary test artifacts removed/);
    assert.match(html, /Retain approved evidence for 12 months/);
    assert.match(html, /Named customer security contacts only/);
  });

  test("renders the complete recorded finding narrative without collapsing impact fields", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Technical details/);
    assert.match(html, /deprecated TLS handshake/);
    assert.match(html, /Technical impact/);
    assert.match(html, /Recorded technical impact/);
    assert.match(html, /Business impact/);
    assert.match(html, /Recorded customer impact/);
    assert.match(html, /Exploitation and attack context/);
    assert.match(html, /protocol downgrade/);
    assert.match(html, /Reproduction or validation steps/);
    assert.match(html, /successful handshake/);
    assert.match(html, /Root cause/);
    assert.match(html, /Deprecated protocol remains enabled/);
    assert.match(html, /Preconditions/);
    assert.match(html, /Network access to the endpoint/);
  });

  test("renders severity disposition aggregates and the full severity-by-status cross-tab", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Open and terminal findings by recorded severity/);
    assert.match(html, /Recorded severity × status cross-tab/);
    assert.match(html, /Remediated/);
    assert.match(html, /Accepted/);
    assert.match(html, /Fp/);
    assert.match(html, /terminal[\s\S]*not presented as a regulatory closure conclusion/i);
  });

  test("renders action tracking and remediation edit provenance for each finding", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Action tracking and planned closure/);
    assert.match(html, /Platform/);
    assert.match(html, /Assigned user ID/);
    assert.match(html, /aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa3/);
    assert.match(html, /platform-owner@example\.test/);
    assert.match(html, /Finding Assignee/);
    assert.match(html, /Platform operations/);
    assert.match(html, /CHG-2026-0042/);
    assert.match(html, /A scheduled change window was required before closure/);
    assert.match(html, /Text updated at/);
    assert.match(html, /2026-09-24T07:30:00Z/);
    assert.match(html, /Text updated by/);
    assert.match(html, /assessor-1/);
    assert.match(html, /Approved Deadline Extension/);
    assert.match(html, /Deadline source/);
    assert.match(html, /Extension/);
    assert.doesNotMatch(html, new RegExp(ACTION_SECRET));
  });

  test("renders structured recommendation provenance separately from compatibility text", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Structured recommendation records/);
    assert.match(html, /Recommendation 1/);
    assert.match(html, /Finding Evidence/);
    assert.match(html, /Unreviewed Recorded/);
    assert.match(html, /Human Reviewed Plan/);
    assert.match(html, /Compatibility recommendation text/);
  });

  test("renders scanner observation identifiers and the timestamp basis on evidence", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Scan result ID/);
    assert.match(html, /aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa/);
    assert.match(html, /Scan job ID/);
    assert.match(html, /bbbbbbbb-1111-4111-8111-bbbbbbbbbbbb/);
    assert.match(html, /Detection run ID/);
    assert.match(html, /cccccccc-1111-4111-8111-cccccccccccc/);
    assert.match(html, /Timestamp basis/);
    assert.match(html, /manager_recorded/);
    assert.match(html, /SHA-256 basis/);
    assert.match(html, /canonical_json_content/);
    assert.match(html, /SHA-256 verified/);
  });

  test("renders detailed closure evidence, terminal history, and completeness gaps", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Post-fix scan/);
    assert.match(html, /TLSv1 rejected/);
    assert.match(html, /manual-retest/);
    assert.match(html, /bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/);
    assert.match(html, /Authorized retest passed/);
    assert.match(html, /closure_review_metadata_absent/);
    assert.match(html, /Closure review metadata absent/);
    assert.match(html, /2026-09-25T10:00:00Z/);
  });

  test("renders the full structured retest record with before-and-after evidence", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Structured retest verification/);
    assert.match(html, /Retest Passed/);
    assert.match(html, /reviewer-closure-1/);
    assert.match(html, /2026-09-25T09:00:00Z/);
    assert.match(html, /2026-09-25T09:15:00Z/);
    assert.match(html, /2026-09-25T09:55:00Z/);
    assert.match(html, /2026-09-25T09:58:00Z/);
    assert.match(html, /external probe/);
    assert.match(html, /Repeat the original TLS protocol check/);
    assert.match(html, /TLSv1 negotiation is rejected/);
    assert.match(html, /TLSv1 negotiation was rejected/);
    assert.match(html, /CHG-2026-0042/);
    assert.match(html, /Before remediation evidence/);
    assert.match(html, /Before-fix TLS capture/);
    assert.match(html, /After remediation evidence/);
    assert.match(html, /After-fix TLS capture/);
    assert.match(html, /cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc/);
    assert.match(html, /dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd/);
    assert.match(html, /Evidence integrity/);
    assert.match(html, /Unverified/);
    assert.match(html, /after_evidence_hash_mismatch/);
  });

  test("distinguishes initial discovery from latest observation scan provenance", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Initial discovery scan/);
    assert.match(html, /Latest observation scan/);
    assert.match(html, /SCN \/ scan job ID/);
    assert.match(html, /77777777-7777-4777-8777-777777777771/);
    assert.match(html, /88888888-8888-4888-8888-888888888882/);
    assert.match(html, /99999999-9999-4999-8999-999999999992/);
    assert.match(html, /aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa2/);
    assert.match(html, /revalidation/);
    assert.match(html, /sha256:initial-result/);
    assert.match(html, /sha256:latest-result/);
    assert.match(html, /validated/);
    assert.match(html, /sha256:db-initial/);
    assert.match(html, /sha256:db-latest/);
    assert.doesNotMatch(html, /Latest discovery/i);
  });

  test("states when initial discovery scan provenance is unavailable", () => {
    const incompleteReport = structuredClone(report);
    incompleteReport.findings[0]!.initial_detection_provenance = null;

    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report: incompleteReport }));

    assert.match(html, /No initial discovery scan provenance is recorded\./);
    assert.match(html, /Latest observation scan/);
  });

  test("renders every extended compliance field without treating mappings as a verdict", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /MAP-001/);
    assert.match(html, /2024-01/);
    assert.match(html, /Customer baseline/);
    assert.match(html, /A\.8\.24/);
    assert.match(html, /Use of cryptography/);
    assert.match(html, /supports/);
    assert.match(html, /Weak protocol affects the recorded control objective/);
    assert.match(html, /applicable/);
    assert.match(html, /fail/);
    assert.match(html, /TEST-7/);
    assert.match(html, /&quot;zone&quot;: &quot;external&quot;/);
    assert.match(html, /&quot;service&quot;: &quot;TLS&quot;/);
    assert.match(html, /https:\/\/example\.test\/mapping\/MAP-001/);
    assert.match(html, /href="https:\/\/example\.test\/mapping\/MAP-001"/);
    assert.match(html, /customer_control_register/);
    assert.match(html, /assessor-1/);
    assert.match(html, /reviewer-1/);
    assert.match(html, /Sampling only/);
    assert.match(html, /Control requires remediation/);
    assert.match(html, /Vedha Security/);
    assert.match(html, /F001\/E01/);
    assert.match(html, /ISO-REF-1/);
    assert.match(html, /Eligible for control rollup/);
    assert.match(html, /mapping_review_required/);
    assert.match(html, /ISO\/IEC 27001/);
    assert.match(html, /not a certification, audit opinion, or compliance verdict/i);
    assert.doesNotMatch(html, /mapping-raw-must-not-render/);
  });

  test("renders complete regulatory profile applicability without implying compliance", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /CERT-In Comprehensive Cyber Security Audit Policy Guidelines/);
    assert.match(html, /CERT-IN-CCSAPG-1\.0-2025/);
    assert.match(html, /Selected as the customer-recorded audit basis/);
    assert.match(html, /customer&#x27;s recorded applicability decision/);
    assert.match(html, /India/);
    assert.match(html, /REG-PROFILE-001/);
    assert.match(html, /Customer-recorded selection only; empanelment and conditional annexures are not inferred/);
    assert.match(html, /href="https:\/\/www\.cert-in\.org\.in\/PDF\/Comprehensive_Cyber_Security_Audit_Policy_Guidelines\.pdf"/);
    assert.match(html, /does not by itself establish compliance/i);
    assert.match(html, /no conditional annexure or obligation is inferred/i);
    assert.doesNotMatch(html, new RegExp(REGULATORY_SECRET));
  });

  test("renders a document-level closure register for every finding", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /Retest and closure register/);
    assert.match(html, /Closure and retest status for every finding/);
    for (const item of report.findings) {
      assert.equal((html.match(new RegExp(`href="#finding-${item.id}"`, "g")) ?? []).length, 1);
    }
    assert.match(html, /Before \/ after artifacts/);
    assert.match(html, /Reopened:/);
  });

  test("does not turn a non-http compliance source into an active link", () => {
    const unsafeReport = structuredClone(report);
    unsafeReport.findings[0]!.compliance_mappings[0]!.source_url = "javascript:alert(1)";
    unsafeReport.compliance_rollup.regulatory_profiles[0]!.source_url = "javascript:regulatory(1)";

    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report: unsafeReport }));

    assert.match(html, /javascript:alert\(1\)/);
    assert.match(html, /javascript:regulatory\(1\)/);
    assert.doesNotMatch(html, /href="javascript:/);
  });

  test("redacts evidence, commands, and lifecycle details and omits raw payloads", () => {
    const html = renderToStaticMarkup(createElement(CanonicalReportDocument, { report }));

    assert.match(html, /\[REDACTED: credential\]/);
    assert.doesNotMatch(html, new RegExp(DESCRIPTION_SECRET));
    assert.doesNotMatch(html, new RegExp(EVIDENCE_SECRET));
    assert.doesNotMatch(html, new RegExp(EVENT_SECRET));
    assert.doesNotMatch(html, new RegExp(PROVENANCE_SECRET));
    assert.doesNotMatch(html, new RegExp(RETEST_SECRET));
    assert.doesNotMatch(html, new RegExp(BEARER.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
    assert.doesNotMatch(html, /must-not-render/);
    assert.doesNotMatch(html, /mapping-raw-must-not-render/);
    assert.doesNotMatch(html, /before-raw-must-not-render/);
    assert.doesNotMatch(html, /after-raw-must-not-render/);
  });
});
