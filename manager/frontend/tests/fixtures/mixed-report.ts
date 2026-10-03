/**
 * A mixed report built from the canonical fixture: open and closed findings of
 * every severity, SLA states, and a sparse finding with nothing recorded.
 */
import type { ReportDocument, ReportFinding } from "../../lib/report/report-document";
import { canonicalReport } from "./canonical-report";

function variant(
  base: ReportFinding,
  patch: Partial<ReportFinding> & { id: string; title: string },
  sla?: Partial<ReportFinding["current_sla"]>,
): ReportFinding {
  const copy = structuredClone(base);
  return {
    ...copy,
    exploitable: false,
    exploit_validated: false,
    ...patch,
    current_sla: { ...copy.current_sla, ...sla },
  };
}

const base = canonicalReport.findings[0]!;

const sparse: ReportFinding = {
  ...structuredClone(base),
  id: "f0000000-0000-4000-8000-000000000006",
  title: "Sparse informational finding",
  severity: "info",
  status: "open",
  description: null,
  technical_details: null,
  impact: null,
  business_impact: null,
  exploitation: null,
  reproduction_steps: null,
  root_cause: null,
  preconditions: null,
  asset: null,
  cve_ids: [],
  cwe_ids: [],
  mitre_techniques: [],
  cvss_score: null,
  cvss_vector: null,
  epss_score: null,
  risk_score: null,
  exploitable: false,
  exploit_validated: false,
  first_seen: null,
  last_seen: null,
  action_tracking: { ...base.action_tracking, owner: null, assigned_to_email: null, assigned_to_user_id: null, owner_source: null },
  evidence: { raw: null, artifacts: [], gaps: ["evidence_absent"] },
  remediation: { ...structuredClone(base.remediation), recorded_text: null, reviewed_plans: [], recommendations: [], recorded_recommendations: [] },
  current_sla: { ...base.current_sla, state: "untracked", deadline: null, hours_total: null, hours_remaining: null },
  readiness_gaps: ["evidence_absent"],
};

export const mixedReport: ReportDocument = (() => {
  const report = structuredClone(canonicalReport);
  report.findings = [
    variant(base, { id: "f0000000-0000-4000-8000-000000000001", title: "Medium open finding", severity: "medium", status: "open", risk_score: 40 },
      { state: "on_track", deadline: "2026-10-20T00:00:00Z", hours_total: 720 }),
    variant(base, { id: "f0000000-0000-4000-8000-000000000002", title: "Critical open finding", severity: "critical", status: "confirmed", exploitable: true, risk_score: 95, cvss_score: 9.8 },
      { state: "breached", deadline: "2026-09-22T00:00:00Z", hours_total: 72 }),
    variant(base, { id: "f0000000-0000-4000-8000-000000000003", title: "High closed finding", severity: "high", status: "remediated" }),
    variant(base, { id: "f0000000-0000-4000-8000-000000000004", title: "High open finding", severity: "high", status: "open", risk_score: 70 },
      { state: "at_risk", deadline: "2026-09-27T00:00:00Z", hours_total: 168 }),
    variant(base, { id: "f0000000-0000-4000-8000-000000000005", title: "Second critical open finding", severity: "critical", status: "open", risk_score: 90 },
      { state: "on_track", deadline: "2026-09-29T00:00:00Z", hours_total: 72 }),
    sparse,
  ];
  report.readiness = {
    complete: false,
    gap_counts: { evidence_absent: 1, closure_review_metadata_absent: 2 },
    affected_finding_ids: {
      evidence_absent: ["f0000000-0000-4000-8000-000000000006"],
      closure_review_metadata_absent: ["f0000000-0000-4000-8000-000000000003", "f0000000-0000-4000-8000-000000000001"],
    },
    report_gaps: ["report_methodology_absent"],
  };
  return report;
})();
