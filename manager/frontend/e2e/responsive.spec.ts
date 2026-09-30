import { expect, test, type Page, type Route } from "@playwright/test";
import { canonicalReport } from "../tests/fixtures/canonical-report";

const ROUTES = [
  "/",
  "/engagements",
  "/engagements/e2e",
  "/scan",
  "/campaign",
  "/fleet",
  "/findings",
  "/reports",
  "/customers",
  "/aibrain",
  "/settings",
  "/portal",
  "/portal/findings",
  "/portal/scans",
  "/portal/fleet",
  "/portal/scope",
  "/portal/reports",
  "/portal/assistant",
  "/portal/settings",
] as const;

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
  title: "Public management interface",
  severity: "CRITICAL",
  status: "OPEN",
  affectedHost: "192.0.2.10",
  discoveredAt: "2026-09-29T08:00:00Z",
  first_seen: "2026-09-29T08:00:00Z",
  description: "An administrative service is reachable from the internet.",
  technicalDetails: "The service answered on TCP 8443.",
  evidence: [{ label: "Scanner", content: "tcp/8443 open", type: "network" }],
  impact: "An attacker can reach a privileged management surface.",
  remediation: ["Restrict access to the management network."],
  mitre: [],
  cwe: [],
  cve: ["CVE-2026-0001"],
  cve_ids: ["CVE-2026-0001"],
  riskScore: 940,
  risk_score: 94,
  cvss: "9.8",
  cvss_score: 9.8,
  cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  activelyExploited: true,
  detectionCoverage: "BLIND",
  aiTriage: {
    priority: "P0",
    reasoning: "Internet-reachable privileged service with active exploitation evidence.",
    recommendation: "Restrict exposure and validate the control immediately.",
    confidence: 0.96,
  },
};

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
  jobs: [],
  job_stats: { total: 0, running: 0, complete: 0, failed: 0, probes: [] },
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
  findings: [],
};

function json(route: Route, body: unknown, status = 200) {
  return route.fulfill({ status, contentType: "application/json", body: JSON.stringify(body) });
}

async function mockApi(route: Route) {
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
  if (path.startsWith("/api/engagements/e2e/")) return json(route, {});

  if (path === "/api/findings/summary") return json(route, {
    total: 3, openTotal: 3, criticalOpen: 1, highOpen: 1, mediumOpen: 1,
    lowOpen: 0, infoOpen: 0, validated: 1, blind: 1, averageRisk: 71.5,
  });
  if (path === "/api/findings/sla-summary") return json(route, {
    summary: { breached: 1, atRisk: 1, dueSoon: 0, onTrack: 1, totalTracked: 3 },
    items: [{ id: finding.id, title: finding.title, severity: "CRITICAL", deadline: "2026-09-29T00:00:00Z", hoursRemaining: -8, hoursTotal: 24, state: "breached" }],
  });
  if (path === "/api/findings") return json(route, {
    items: [finding], total: 1, page: 1, pageSize: 100, pages: 1,
  });
  if (path === "/api/findings/groups") return json(route, {
    items: [], total: 0, page: 1, pageSize: 100, pages: 1,
  });
  if (path === "/api/findings/assets" || path === "/api/findings/scans") return json(route, []);
  if (path === "/api/findings/compare") return json(route, {
    a: null, b: null, new: [], resolved: [], persistent: [], summary: {},
  });
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
  if (path === "/api/scan/campaigns" || path === "/api/scan/jobs" || path === "/api/customers" || path === "/api/users" || path === "/api/auth/pats" || path === "/api/integrations") return json(route, []);
  if (path === "/api/scan/use-cases") return json(route, []);
  if (path === "/api/fleet/enrollment") return json(route, { requests: [], manager_url: "https://manager.vedha.test" });
  if (path === "/api/fleet/jobs") return json(route, []);
  if (path === "/api/ai/status") return json(route, { enabled: false, provider: "ollama", model: "", providers: [] });
  if (path === "/api/settings/status") return json(route, { apiReachable: true, cookieSecure: true, checkedAt: "2026-09-30T10:00:00Z" });
  if (path === "/api/sla-policy") return json(route, { critical_hours: 24, high_hours: 72, medium_hours: 168, low_hours: 336, info_hours: 0, is_custom: false });

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
    risk_score: 94, remediation: "Restrict access to the management network.", first_seen: finding.first_seen,
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
  if (path === "/api/portal/workspace/fleet/jobs") return json(route, []);
  if (path.startsWith("/api/portal/workspace/fleet/agents/") && path.endsWith("/jobs")) return json(route, []);
  if (path === "/api/portal/reports" || path === "/api/portal/scans" || path === "/api/portal/agents" || path === "/api/portal/activity") return json(route, []);
  if (path === "/api/portal/use-cases") return json(route, []);
  if (path.startsWith("/api/portal/")) return json(route, {});

  return json(route, {});
}

async function settle(page: Page) {
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.addStyleTag({ content: `
    *, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; caret-color: transparent !important; }
  ` });
  await page.waitForTimeout(120);
}

test.beforeEach(async ({ context, page }) => {
  await context.addCookies([
    { name: "vedha_token", value: "e2e", domain: "127.0.0.1", path: "/", httpOnly: true, sameSite: "Lax" },
    { name: "vedha_portal_token", value: "e2e", domain: "127.0.0.1", path: "/", httpOnly: true, sameSite: "Lax" },
  ]);
  await page.addInitScript(() => {
    const fixedNow = Date.parse("2026-09-30T10:30:00Z");
    const RealDate = Date;
    class FixedDate extends RealDate {
      constructor(...args: unknown[]) {
        super(args.length ? args[0] as string | number : fixedNow);
      }
      static now() { return fixedNow; }
    }
    Object.defineProperty(window, "Date", { value: FixedDate });
  });
  await page.route("**/api/**", mockApi);
});

for (const path of ROUTES) {
  const slug = path === "/" ? "dashboard" : path.slice(1).replaceAll("/", "-");
  test(`${path} stays responsive`, async ({ page }, testInfo) => {
    const pageErrors: string[] = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));

    // These pages intentionally poll. Waiting for network-idle makes a healthy
    // dashboard look hung, so wait for the document and then let mocked queries
    // settle instead.
    await page.goto(path, { waitUntil: "domcontentloaded" });
    await page.locator("body").waitFor({ state: "visible" });
    await settle(page);

    const overflow = await page.evaluate(() => ({
      viewport: document.documentElement.clientWidth,
      page: document.documentElement.scrollWidth,
    }));
    expect(overflow.page, `${path} should not overflow horizontally`).toBeLessThanOrEqual(overflow.viewport + 1);

    if ((testInfo.project.use.viewport?.width ?? 1440) <= 768) {
      const undersized = await page.locator("button:visible").evaluateAll((buttons) => buttons
        .map((button) => {
          const box = button.getBoundingClientRect();
          return { label: button.getAttribute("aria-label") || button.textContent?.trim().slice(0, 40) || "button", width: box.width, height: box.height };
        })
        .filter((box) => box.height < 40 || box.width < 40));
      expect(undersized, `${path} has undersized touch targets`).toEqual([]);
    }

    expect(pageErrors, `${path} emitted browser errors`).toEqual([]);
    await expect(page).toHaveScreenshot(`${slug}.png`, {
      animations: "disabled",
      caret: "hide",
      scale: "css",
      maxDiffPixelRatio: 0.015,
    });
  });
}
