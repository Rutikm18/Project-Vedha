import type { Page, Route } from "@playwright/test";
import { canonicalReport } from "../tests/fixtures/canonical-report";
const engagement = {
  id: "e2e",
  name: "Northwind perimeter review",
  client: "Northwind Systems",
  status: "ACTIVE",
  startDate: "2026-09-01",
  endDate: "2026-09-30",
  scopeCidrs: ["192.0.2.0/24"],
  excludedCidrs: [],
  assessor: "Vedha Security",
  description: "External exposure and remediation validation.",
  assetCount: 12,
  findingCount: 3,
  findingsBySeverity: { CRITICAL: 1, HIGH: 1, MEDIUM: 1, LOW: 0 },
  tags: ["external", "quarterly"],
  progress: 72,
};

const finding = {
  id: "finding-e2e",
  title: "SMBv1 enabled (wormable, deprecated) (port 445)",
  severity: "CRITICAL",
  status: "OPEN",
  affectedHost: "192.0.2.10",
  discoveredAt: "2026-09-29T08:00:00Z",
  first_seen: "2026-09-29T08:00:00Z",
  lastSeen: "2026-09-30T08:00:00Z",
  category: "Network exposure",
  description: "An administrative service is reachable from the internet.",
  technicalDetails: "The service answered on TCP 8443.",
  attackPath: "External network → SMB service → remote code execution",
  evidence: [{ label: "Scanner", content: "tcp/8443 open", type: "network" }],
  impact: "An attacker can reach a privileged management surface.",
  remediation: ["Restrict access to the management network."],
  mitre: [],
  killChain: [],
  compliance: [],
  cwe: [],
  cve: ["CVE-2026-0001"],
  cve_ids: ["CVE-2026-0001"],
  cves: ["CVE-2026-0001"],
  riskScore: 940,
  risk_score: 940,
  priority: "P0",
  cvss: "9.8",
  cvss_score: 9.8,
  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  epssScore: 0.82,
  epssPercentile: 0.97,
  epssRecorded: true,
  kevListed: true,
  kevStatusRecorded: true,
  exploitMaturity: "WEAPONIZED",
  exploitMaturityRecorded: true,
  pocAvailable: true,
  activelyExploited: true,
  detectionCoverage: "BLIND",
  fpProbability: 0.02,
  fpProbabilityRecorded: true,
  aiTriage: {
    reasoning: "Internet-reachable privileged service with active exploitation evidence.",
    recommendation: "Restrict exposure and validate the control immediately.",
    confidence: 0.96,
  },
};

const auditEntry = (n: number, over: Record<string, unknown> = {}) => ({
  id: `00000000-0000-4000-8000-0000000000${String(n).padStart(2, "0")}`,
  timestamp: `2026-10-16T08:${String(60 - n).padStart(2, "0")}:04Z`,
  action: "finding.updated", label: "Finding changed", category: "findings", category_label: "Findings",
  outcome: "success",
  actor: { id: "11111111-1111-4111-8111-111111111111", type: "user", label: "analyst@vedha.test" },
  resource_type: "finding", resource_id: null, engagement_id: null, engagement_name: null,
  ip_address: "203.0.113.7", user_agent: "Mozilla/5.0", request_id: `req-${n}`,
  detail: { status: "confirmed" }, changes: { status: { before: "open", after: "confirmed" } },
  chain_position: n, entry_hash: "ab".repeat(32), ...over,
});

const auditEntries = [
  auditEntry(2, {
    action: "auth.login.failure", label: "Sign-in failed", category: "authentication",
    category_label: "Sign-in and sessions", outcome: "failure",
    actor: { id: "anonymous", type: "anonymous", label: "ghost@example.test" },
    detail: { reason: "user_not_found" }, changes: null, resource_type: null,
  }),
  auditEntry(1),
];

const scans = [
  { jobId: "job-new", reference: "SCN-261016-NEWEST", useCaseId: "uc_network_va", intensity: "normal", scannedAt: "2026-10-16T08:00:00Z", status: "completed", findings: 4 },
  { jobId: "job-old", reference: "SCN-261009-OLDER0", useCaseId: "uc_network_va", intensity: "normal", scannedAt: "2026-10-09T08:00:00Z", status: "completed", findings: 3 },
];

const scanRef = (reference: string, scannedAt: string) => ({
  reference, useCaseId: "uc_network_va", intensity: "normal", scannedAt, jobId: null, runId: null,
});

// GET /findings/compare, mapped by the BFF: 1 new, 1 fixed, 1 changed, 1 unchanged.
const compareResult = {
  a: scanRef("SCN-261009-OLDER0", "2026-10-09T08:00:00Z"),
  b: scanRef("SCN-261016-NEWEST", "2026-10-16T08:00:00Z"),
  counts: { new: 1, fixed: 1, stillPresent: 2, changed: 1 },
  summaryA: { total: 3, bySeverity: { CRITICAL: 0, HIGH: 2, MEDIUM: 1, LOW: 0, INFO: 0 }, averageRisk: 540, fromSnapshot: true },
  summaryB: { total: 3, bySeverity: { CRITICAL: 1, HIGH: 1, MEDIUM: 1, LOW: 0, INFO: 0 }, averageRisk: 610, fromSnapshot: true },
  new: [{ ...finding, id: "cmp-new", title: "Redis exposed without authentication" }],
  fixed: [{ ...finding, id: "cmp-fixed", title: "SMBv1 enabled", severity: "HIGH" }],
  stillPresent: [
    { ...finding, id: "cmp-moved", title: "Outdated OpenSSH" },
    { ...finding, id: "cmp-same", title: "TLS 1.0 accepted", severity: "MEDIUM" },
  ],
  changed: [{
    finding: { ...finding, id: "cmp-moved", title: "Outdated OpenSSH" },
    before: { severity: "MEDIUM", riskScore: 400, status: "OPEN" },
    after: { severity: "HIGH", riskScore: 520, status: "OPEN" },
    severityChanged: true, statusChanged: false, riskDelta: 120,
  }],
};

// What GET /findings/{id}/risk-explanation returns for the finding above (critical, KEV, 9.8, EPSS 82%).
const riskExplanation = {
  model_version: "risk-rank-v1", score: 940, max: 1000, severity: "critical",
  dimensions: [
    { key: "impact", label: "Impact", weight: 0.4, value: 0.984, points: 393.6, inputs: [
      { key: "cvss", label: "CVSS base score", raw: 9.8, normalized: 0.98, weight: 0.8, contribution: 0.784, source: "recorded", note: "Recorded CVSS 9.8 out of 10." },
      { key: "severity", label: "Severity", raw: "critical", normalized: 1, weight: 0.2, contribution: 0.2, source: "recorded", note: "Critical maps to 1.0." },
    ] },
    { key: "exploit", label: "Exploitability", weight: 0.25, value: 0.9, points: 225, inputs: [
      { key: "epss", label: "EPSS", raw: 0.82, normalized: 0.82, weight: 0.45, contribution: 0.369, source: "recorded", note: "82% chance of exploitation in 30 days." },
      { key: "kev", label: "Known exploited (KEV)", raw: true, normalized: 1, weight: 0.35, contribution: 0.35, source: "recorded", note: "Listed in CISA KEV." },
      { key: "exploit_validated", label: "Exploit validated", raw: false, normalized: 0, weight: 0.2, contribution: 0, source: "recorded", note: "Not validated." },
    ] },
    { key: "context", label: "Asset context", weight: 0.2, value: 0.5, points: 100, inputs: [
      { key: "asset_criticality", label: "Asset criticality", raw: null, normalized: 0.5, weight: 0.45, contribution: 0.225, source: "default", note: "No asset recorded; neutral 0.5 used." },
      { key: "internet_facing", label: "Internet exposure", raw: null, normalized: 0.5, weight: 0.35, contribution: 0.175, source: "default", note: "Not recorded; neutral 0.5 used." },
      { key: "auth_gap", label: "Authentication gap", raw: null, normalized: 0.5, weight: 0.2, contribution: 0.1, source: "default", note: "Not recorded; neutral 0.5 used." },
    ] },
    { key: "evidence", label: "Evidence strength", weight: 0.15, value: 0.8, points: 120, inputs: [
      { key: "verification", label: "Verification verdict", raw: "confirmed", normalized: 1, weight: 0.6, contribution: 0.6, source: "recorded", note: "Confirmed." },
      { key: "confidence", label: "Confidence", raw: 50, normalized: 0.5, weight: 0.4, contribution: 0.2, source: "recorded", note: "50% confidence." },
    ] },
  ],
  additive_score: 838.6, band: { floor: 750, ceiling: 1000, position: 0.7544 },
  placement: { formula: "floor + position × (ceiling − floor)", result: 940 },
  defaults_used: ["asset_criticality", "internet_facing", "auth_gap"],
  context: { asset: null, internet_exposure_source: "not recorded", service_exposure: null },
  stored_score: 940, stored_in_sync: true,
  priority: {
    priority: "P0", label: "Immediate", rule: "exploited_high_impact",
    reason: "Known to be exploited and critical impact.", inputs: {},
    rules: [
      { id: "exploited_high_impact", priority: "P0", condition: "Known exploited (KEV) or validated, and severity High or Critical", matched: true, decisive: true },
      { id: "critical_past_sla", priority: "P0", condition: "Critical and past its SLA deadline", matched: false, decisive: false },
      { id: "critical", priority: "P1", condition: "Severity Critical", matched: true, decisive: false },
    ],
  },
};

const slaItems = Array.from({ length: 8 }, (_, index) => ({
  id: index === 0 ? finding.id : `${finding.id}-${index + 1}`,
  title: index % 2 === 0
    ? "Outdated SSH server (Dropbear 2017.75)"
    : "Weak SSH cryptographic algorithms offered",
  severity: index < 2 ? "HIGH" : "MEDIUM",
  deadline: "2026-09-29T00:00:00Z",
  hoursRemaining: -(8 + index * 24),
  hoursTotal: 72,
  state: "breached",
}));

const step = (n: number, tier: string, title: string, description: string, cmds: string[]) => ({
  step: n, tier, title, description, commands: null, commands_for_os: cmds, pre_checks: [],
  reboot_required: tier === "fix", downtime: tier === "fix" ? "A short service restart" : "None", rollback: "Re-enable the setting.", risk: "low",
});

const remediationBundles = {
  view: "fix", sla_source: "tenant", generated_at: "2026-09-30T10:00:00Z",
  summary: { bundles: 2, open_bundles: 2, done_bundles: 0, open_findings: 3, closed_findings: 0, hosts: 2, act: 1 },
  bundles: [
    {
      fix_key: "smbv1-disable", ref: "FIX-01", recipe_id: "smbv1", product_family: "windows", title: "Disable SMBv1 on Windows file servers",
      remediation_type: "vendor_fix", risk_response: "mitigate", target_state: "SMBv1 disabled and not negotiated", effort: "low", remediation_risk: "low",
      steps_by_os: {
        windows: [
          step(1, "containment", "Block TCP 445 from untrusted networks", "Restrict SMB at the perimeter firewall while the fix lands.", ["netsh advfirewall firewall add rule name=BlockSMB dir=in action=block protocol=TCP localport=445"]),
          step(2, "fix", "Disable the SMBv1 server component", "Turn SMBv1 off on the host.", ["Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force"]),
        ],
        linux: [step(1, "fix", "Set the minimum SMB protocol", "Require SMB2 or newer in smb.conf.", ["server min protocol = SMB2"])],
      },
      verification_check: { scanner: "smb_scan", check: "SMBv1 negotiation attempt", expected: "The host refuses SMBv1", manual_command: "nmap -p445 --script smb-protocols HOST" },
      compensating_controls: "Block TCP 445 at the firewall and restrict it to the management network until the host is fixed.",
      references: [], resolves: ["cmp-f1"], open_finding_ids: ["cmp-f1"], excluded: [], open_count: 2, closed_count: 0,
      due_at: "2026-10-02T10:00:00Z", due_source: "tenant", urgency: "act", progress: { closed: 0, total: 2 }, status: "open", max_severity: "critical", kev: true,
      hosts: [
        { host: "fs-01", ip: "10.10.0.14", os: "Windows Server 2016", os_family: "windows", ports: [445], finding_ids: ["cmp-f1"], status: "open", due_at: "2026-10-02T10:00:00Z", due_source: "tenant", closed_at: null },
        { host: "fs-02", ip: "10.10.0.15", os: "Windows Server 2012 R2", os_family: "windows", ports: [445], finding_ids: ["cmp-f4"], status: "open", due_at: "2026-10-02T10:00:00Z", due_source: "tenant", closed_at: null },
      ],
    },
    {
      fix_key: "tls-legacy", ref: "FIX-02", recipe_id: "tls", product_family: null, title: "Disable TLS 1.0 and 1.1",
      remediation_type: "mitigation", risk_response: "mitigate", target_state: "TLS 1.2 or newer only", effort: "low", remediation_risk: "low",
      steps_by_os: { generic: [step(1, "fix", "Disable legacy protocols", "Remove TLS 1.0 and 1.1 from the listener.", ["ssl_protocols TLSv1.2 TLSv1.3;"])] },
      verification_check: { scanner: "tls", check: "Protocol negotiation", expected: "TLS 1.0 and 1.1 are refused", manual_command: "openssl s_client -tls1 -connect HOST:443" },
      compensating_controls: "Terminate TLS at a gateway that already enforces TLS 1.2.",
      references: [], resolves: ["cmp-f3"], open_finding_ids: ["cmp-f3"], excluded: [], open_count: 1, closed_count: 0,
      due_at: "2026-10-30T10:00:00Z", due_source: "tenant", urgency: "track", progress: { closed: 0, total: 1 }, status: "open", max_severity: "medium", kev: false,
      hosts: [{ host: "web-01", ip: "10.10.0.14", os: "Ubuntu 22.04", os_family: "linux", ports: [443], finding_ids: ["cmp-f3"], status: "open", due_at: "2026-10-30T10:00:00Z", due_source: "tenant", closed_at: null }],
    },
  ],
};

const campaignJobs = [
  { id: "job-run-1111", use_case_id: "uc_network_va", job_type: "network_va", status: "running", phase: "scanning",
    agent_name: "mumbai-dc-probe", result_summary: {}, reference: "SCN-261016-AB12CD",
    created_at: "2026-09-30T09:40:00Z", started_at: "2026-09-30T09:41:00Z", completed_at: null },
  { id: "job-pend-2222", use_case_id: "uc_network_va", job_type: "network_va", status: "pending", phase: "queued",
    agent_name: null, result_summary: {}, reference: "SCN-261016-EF34GH",
    created_at: "2026-09-30T09:45:00Z", started_at: null, completed_at: null },
  { id: "job-done-3333", use_case_id: "uc_network_va", job_type: "network_va", status: "completed", phase: "complete",
    agent_name: "pune-branch-probe", reference: "SCN-261015-IJ56KL",
    result_summary: { scanner_count: 6, fact_count: 412, open_ports: 37, profile: "normal", scanners: ["nmap", "tls", "smb_scan"] },
    created_at: "2026-09-29T08:00:00Z", started_at: "2026-09-29T08:01:00Z", completed_at: "2026-09-29T08:52:00Z" },
  { id: "job-fail-4444", use_case_id: "uc_network_va", job_type: "network_va", status: "failed", phase: "scanning",
    agent_name: "mumbai-dc-probe", result_summary: {}, reference: "SCN-261014-MN78OP",
    created_at: "2026-09-28T08:00:00Z", started_at: "2026-09-28T08:01:00Z", completed_at: "2026-09-28T08:03:00Z" },
];

const fleetJobs = campaignJobs.map((j) => ({
  job_id: j.id, reference: j.reference, agent_id: j.agent_name ? `agent-${j.agent_name}` : null, agent_name: j.agent_name,
  engagement_id: "e2e", engagement_name: "Northwind perimeter review", job_type: j.job_type, status: j.status,
  use_case_id: j.use_case_id, created_at: j.created_at, started_at: j.started_at, completed_at: j.completed_at,
}));

const campaignRuns = [
  { campaign_id: "camp-20260930-a1b2", targets: ["10.10.0.0/24", "10.20.0.0/24"], status: "running", percent: 46,
    current_stage: "Service fingerprinting", started_at: "2026-09-30T09:41:00Z", updated_at: "2026-09-30T10:29:00Z", stage_count: 7 },
  { campaign_id: "camp-20260929-c3d4", targets: ["192.168.1.0/24"], status: "completed", percent: 100,
    current_stage: null, started_at: "2026-09-29T08:01:00Z", updated_at: "2026-09-29T08:52:00Z", stage_count: 7 },
];

const campaignProgress = {
  engagement_id: "e2e",
  engagement: { name: engagement.name, status: engagement.status },
  overall_status: "complete",
  is_complete: true,
  reasons: [],
  coverage: {
    rules_total: 4, rules_assessed: 4, rules_blind: 0,
    rules_unassessed: 0, blind_rule_ids: [], has_gaps: false,
  },
  evidence: { submissions: 1, covered: 1, fully_covered: true },
  queue: { pending: false, overdue: false, dead: false },
  jobs: campaignJobs,
  job_stats: { total: 4, running: 1, complete: 1, failed: 1, probes: ["mumbai-dc-probe", "pune-branch-probe"] },
  detection: {
    status: "complete", facts_count: 1, findings_new: 1, findings_current: 1,
    by_severity: { critical: 1, high: 0, medium: 0, low: 0, info: 0 },
  },
  summary: {
    total_findings: 1, by_severity: { critical: 1, high: 0, medium: 0, low: 0, info: 0 },
    max_risk_score: 940, exploitable: 1, actionable: 1, top_techniques: [],
  },
  phases: [
    { name: "scanning", status: "done", count: 1 },
    { name: "detection", status: "done", count: 1 },
    { name: "remediation", status: "done", count: 1 },
  ],
  percent: 100,
  findings: [
    { id: "cmp-f1", title: "SMBv1 enabled (wormable, deprecated)", severity: "critical", risk_score: 911, confidence: 90,
      corroborated_by: ["smb_scan", "nmap"], cve_ids: ["CVE-2017-0144"], mitre_techniques: ["T1210"], state: "confirmed",
      remediation: "1. Disable SMBv1 on the host. 2. Restart the Server service. 3. Re-run the scan to confirm it no longer negotiates SMBv1." },
    { id: "cmp-f2", title: "VNC accepts connections with no authentication (port 5900)", severity: "high", risk_score: 742, confidence: 70,
      cve_ids: null, mitre_techniques: null, state: "open", remediation: null },
    { id: "cmp-f3", title: "TLS 1.0 accepted on 10.10.0.14:443", severity: "medium", risk_score: 388, confidence: 85,
      cve_ids: null, mitre_techniques: ["T1040"], state: "open",
      remediation: "Disable TLS 1.0 and 1.1. Keep TLS 1.2 and 1.3 only." },
  ],
};

function json(route: Route, body: unknown, status = 200) {
  return route.fulfill({ status, contentType: "application/json", body: JSON.stringify(body) });
}

export async function mockApi(route: Route) {
  const url = new URL(route.request().url());
  const path = url.pathname;

  if (path === "/api/auth/me") return json(route, { email: "analyst@vedha.test", role: "admin", tenantId: "e2e" });
  if (path === "/api/engagements") return json(route, { engagements: [engagement], timeline: [], stats: { totalAssets: 12 } });
  if (path === "/api/engagements/e2e") return json(route, { engagement, activity: [] });
  if (path === "/api/engagements/e2e/assets") return json(route, []);
  if (path === "/api/engagements/e2e/report-document") return json(route, {
    ...canonicalReport,
    engagement: {
      ...canonicalReport.engagement,
      id: engagement.id,
      name: engagement.name,
      client: engagement.client,
      status: engagement.status,
      scope_cidrs: engagement.scopeCidrs,
    },
  });
  if (path === "/api/engagements/e2e/campaign-progress") return json(route, campaignProgress);
  if (path === "/api/engagements/e2e/remediation/bundles") return json(route, remediationBundles);
  if (path === "/api/engagements/e2e/extensions") return json(route, { items: [] });
  if (path.startsWith("/api/engagements/e2e/")) return json(route, {});

  if (path === "/api/findings/summary") return json(route, {
    total: 3, openTotal: 3, criticalOpen: 1, highOpen: 1, mediumOpen: 1,
    lowOpen: 0, infoOpen: 0, validated: 1, blind: 1, averageRisk: 71.5,
  });
  if (path === "/api/findings/sla-summary") return json(route, {
    summary: { breached: 8, atRisk: 1, dueSoon: 0, onTrack: 1, totalTracked: 10 },
    items: slaItems,
  });
  if (path === "/api/findings") return json(route, {
    items: [finding], total: 1, page: 1, pageSize: 100, pages: 1,
  });
  if (path === "/api/findings/groups") return json(route, {
    items: [], total: 0, page: 1, pageSize: 100, pages: 1,
  });
  if (path === "/api/portal/audit-log") return json(route, {
    items: [
      { id: "00000000-0000-4000-8000-000000000101", timestamp: "2026-10-16T08:10:00Z", label: "Scan requested", category: "scanning",
        category_label: "Scanning and probes", outcome: "success", who: "You", who_is_vedha: false, ip_address: "203.0.113.7" },
      { id: "00000000-0000-4000-8000-000000000102", timestamp: "2026-10-16T07:55:00Z", label: "Finding changed", category: "findings",
        category_label: "Findings", outcome: "success", who: "Vedha analyst", who_is_vedha: true, ip_address: null },
    ],
    next_cursor: null,
  });
  if (path === "/api/audit-logs/integrity") return json(route, {
    ok: true, entries_checked: 1284, oldest: "2026-01-02T00:00:00Z", newest: "2026-10-16T08:00:00Z",
    first_problem: null, retention_days: 365, minimum_retention_days: 180, checked_at: "2026-10-16T08:30:00Z",
  });
  if (path === "/api/audit-logs/facets") return json(route, {
    categories: [
      { key: "authentication", label: "Sign-in and sessions", count: 1 }, { key: "findings", label: "Findings", count: 1 },
      { key: "other", label: "Other", count: 0 },
    ],
    outcomes: [{ key: "success", count: 1 }, { key: "failure", count: 1 }, { key: "denied", count: 0 }],
  });
  if (path === "/api/audit-logs") return json(route, { items: auditEntries, next_cursor: null });
  if (path === "/api/findings/assets") return json(route, []);
  if (path === "/api/findings/scans") return json(route, scans);
  if (path === "/api/findings/compare") return json(route, compareResult);
  if (/^\/api\/findings\/[^/]+\/risk-explanation$/.test(path)) return json(route, riskExplanation);
  if (path.startsWith("/api/findings/")) return json(route, finding);

  if (path === "/api/analytics/posture") return json(route, {
    has_runs: true,
    scores: { risk_index: 47.5, exploitable_score: 16.6, posture_score: 65, grade: "C" },
    scores_prev: { risk_index: 39.9, exploitable_score: 0, posture_score: 76, grade: "B" },
    matrix: [{ severity: "CRITICAL", prev_open: 0, new: 1, resolved: 0, now_open: 1, net: 1 }],
    new_count: 1, resolved_count: 2, persisting_count: 2,
  });
  if (path === "/api/analytics/exposure") return json(route, {
    protocols: [{ name: "HTTPS", value: 78 }, { name: "SSH", value: 52 }],
    zones: [{ name: "Internet edge", score: 58 }, { name: "Corporate", score: 82 }],
  });
  if (path === "/api/activity") return json(route, []);
  if (path === "/api/agents/register" || path === "/api/agents" || path === "/api/scan/probes") return json(route, []);
  if (path === "/api/scan/campaigns") return json(route, campaignRuns);
  if (path === "/api/fleet/jobs") return json(route, fleetJobs);
  if (path === "/api/scan/jobs" || path === "/api/customers" || path === "/api/users" || path === "/api/auth/pats" || path === "/api/integrations") return json(route, []);
  if (path === "/api/scan/use-cases") return json(route, []);
  if (path === "/api/fleet/enrollment") return json(route, { requests: [], manager_url: "https://manager.vedha.test" });
  if (path === "/api/ai/status") return json(route, { enabled: false, provider: "ollama", model: "", providers: [] });
  if (path === "/api/settings/status") return json(route, { apiReachable: true, cookieSecure: true, checkedAt: "2026-09-30T10:00:00Z" });
  if (path === "/api/sla-policy") return json(route, { critical_hours: 24, high_hours: 72, medium_hours: 168, low_hours: 336, info_hours: 0, is_custom: false });

  if (path === "/api/fleet/enroll-tokens" || path === "/api/portal/workspace/fleet/enroll-tokens") return json(route, []);
  if (path === "/api/fleet/release" || path === "/api/portal/workspace/fleet/install") return json(route, { available: false, manager_url: "https://manager.vedha.test", can_add_agent: false });
  if (path === "/api/portal/findings/locked") return json(route, { counts: {}, total: 0, locked_severities: [] });
  if (path === "/api/portal/workspace/findings/assets" || path === "/api/portal/workspace/findings/scans") return json(route, []);
  if (path === "/api/portal/workspace/findings/summary") return json(route, { total: 1, open_total: 1, critical_open: 1, high_open: 0, medium_open: 0, low_open: 0, info_open: 0, validated: 1, blind: 1, average_risk: 940 });
  if (path === "/api/portal/workspace/findings/groups") return json(route, { items: [], total: 0, page: 1, page_size: 20, pages: 1 });
  if (path === "/api/portal/workspace/findings") return json(route, { items: [], total: 0, page: 1, page_size: 20, pages: 1 });
  if (path === "/api/portal/engagement") return json(route, {
    id: "e2e", name: engagement.name, status: "active", scope_cidr_count: 1,
    scope_cidrs: engagement.scopeCidrs, has_assigned_agent: true,
  });
  if (path === "/api/portal/summary") return json(route, {
    posture: { risk_index: 47.5, exploitable_score: 16.6, posture_score: 65, grade: "C", open_findings: 3 },
    open_findings: 3, closed_findings: 2,
    severity_counts: { critical: 1, high: 1, medium: 1, low: 0, info: 0 },
    criticalOpen: 1, highOpen: 1, mediumOpen: 1, lowOpen: 0, infoOpen: 0, openTotal: 3,
    pending_requests: 0, running_jobs: 0,
  });
  if (path === "/api/portal/sla-summary") return json(route, {
    summary: { breached: 1, atRisk: 1, dueSoon: 0, onTrack: 1, totalTracked: 3 }, items: [],
  });
  if (path === "/api/portal/analytics/posture") return json(route, {
    has_runs: true,
    scores: { risk_index: 47.5, exploitable_score: 16.6, posture_score: 65, grade: "C" },
    scores_prev: null, matrix: [], new_count: 1, resolved_count: 2, persisting_count: 2,
  });
  if (path === "/api/portal/analytics/exposure") return json(route, { protocols: [], zones: [] });
  if (path === "/api/portal/findings") return json(route, [{
    id: finding.id, title: finding.title, description: finding.description,
    severity: "critical", status: "open", cvss_score: 9.8, cve_ids: finding.cve_ids,
    risk_score: 940, remediation: "Restrict access to the management network.", first_seen: finding.first_seen,
  }]);
  if (path === "/api/portal/trends") return json(route, { by_severity: { critical: 1, high: 1, medium: 1 }, timeline: [] });
  if (path === "/api/portal/entitlement") return json(route, {
    state: "active", can_scan: true, reason: null, plan_type: "licensed",
    starts_at: "2026-09-01T00:00:00Z", expires_at: null, days_left: null,
    scan_quota: null, scans_used: 1, scans_left: null, license_key: null,
    deep_repeat_policy: "distinct", deep_scanned_targets: [],
    modes: Object.fromEntries(["stealth", "normal", "aggressive", "deep"].map((mode) => [mode, {
      enabled: true, quota: null, used: 0, left: null, can_scan: true, reason: null,
    }])),
  });
  if (path === "/api/portal/workspace/engagement") return json(route, {
    id: engagement.id, name: engagement.name, status: "active",
    scope_cidrs: engagement.scopeCidrs, excluded_cidrs: engagement.excludedCidrs,
    rules_of_engagement: { client: engagement.client, assessor: engagement.assessor },
    finding_summary: { total: engagement.findingCount, critical: 1, high: 1, medium: 1, low: 0 },
  });
  if (path === "/api/portal/workspace/scan/use-cases") return json(route, []);
  if (path === "/api/portal/workspace/scan/jobs") return json(route, []);
  if (path === "/api/portal/workspace/scan/campaign-progress") return json(route, campaignProgress);
  if (path === "/api/portal/remediation/bundles") return json(route, remediationBundles);
  if (path === "/api/portal/extensions") return json(route, { items: [] });
  if (path === "/api/portal/workspace/fleet/jobs") return json(route, []);
  if (path.startsWith("/api/portal/workspace/fleet/agents/") && path.endsWith("/jobs")) return json(route, []);
  if (path === "/api/portal/reports" || path === "/api/portal/scans" || path === "/api/portal/agents" || path === "/api/portal/activity") return json(route, []);
  if (path === "/api/portal/use-cases") return json(route, []);
  if (path.startsWith("/api/portal/")) return json(route, {});

  return json(route, {});
}

export async function settle(page: Page) {
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.addStyleTag({ content: `
    *, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; caret-color: transparent !important; }
  ` });
  await page.waitForTimeout(120);
}
