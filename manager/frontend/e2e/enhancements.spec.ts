import { expect, test, type Page, type Route } from "@playwright/test";
import { mockApi } from "./mock-api";

const catalog = [{ use_case_id: "uc_network_va", display_name: "Network Vulnerability Assessment", description: "Assess in-scope services", scan_type: "network_va", profile: "it", expected_runtime_hint: "5 minutes", status: "available" }];
const probes = [{ id: "probe-e2e", name: "Test probe", online: true, capabilities: ["network_va"], status: "online", current_job_id: null }];
const respond = (route: Route, body: unknown, status = 200) => route.fulfill({ status, contentType: "application/json", body: JSON.stringify(body) });

test.beforeEach(async ({ context, page }) => {
  await context.addCookies([{ name: "vedha_token", value: "e2e", domain: "127.0.0.1", path: "/", httpOnly: true, sameSite: "Lax" }, { name: "vedha_portal_token", value: "e2e", domain: "127.0.0.1", path: "/", httpOnly: true, sameSite: "Lax" }]);
  await page.route("**/api/**", mockApi);
});

async function expectFocusInside(page: Page, selector: string) {
  await expect.poll(() => page.evaluate((target) => document.querySelector(target)?.contains(document.activeElement), selector)).toBe(true);
}

test("critical attention shortcut applies filters and survives reload", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /1 critical finding/ }).click();
  await page.getByText("More filters", { exact: false }).click();
  await expect(page.getByRole("button", { name: "CRITICAL", exact: true })).toHaveAttribute("aria-pressed", "true");
  await expect(page.getByRole("combobox", { name: "Lifecycle", exact: true })).toHaveValue("OPEN");
  await page.reload();
  await page.getByText("More filters", { exact: false }).click();
  await expect(page.getByRole("combobox", { name: "Lifecycle", exact: true })).toHaveValue("OPEN");
  await expect.poll(() => page.evaluate(() => new URLSearchParams(location.search).get("severity"))).toBe("CRITICAL");
});

test("SLA shortcut reaches the breached queue", async ({ page }) => {
  await page.goto("/");
  const request = page.waitForRequest((request) => new URL(request.url()).pathname === "/api/findings" && new URL(request.url()).searchParams.get("sla_breached") === "true");
  await page.getByRole("button", { name: /8 SLA breaches/ }).click();
  await page.getByText("More filters", { exact: false }).click();
  await request;
  await expect(page.getByRole("button", { name: "SLA breached", exact: true })).toHaveAttribute("aria-pressed", "true");
});

test("queue filter changes remain shareable and history restores state", async ({ page }) => {
  await page.goto("/findings?severity=HIGH&status=confirmed&page=2");
  await page.getByText("More filters", { exact: false }).click();
  await expect(page.getByRole("combobox", { name: "Lifecycle", exact: true })).toHaveValue("CONFIRMED");
  await page.getByLabel("Search findings", { exact: true }).fill("CVE-2026");
  await expect.poll(() => page.evaluate(() => new URLSearchParams(location.search).get("search"))).toBe("CVE-2026");
  await page.reload();
  await page.getByText("More filters", { exact: false }).click();
  await expect(page.getByLabel("Search findings", { exact: true })).toHaveValue("CVE-2026");
  await page.evaluate(() => { history.pushState(history.state, "", "/findings?severity=LOW&status=open"); dispatchEvent(new PopStateEvent("popstate")); });
  await expect(page.getByRole("combobox", { name: "Lifecycle", exact: true })).toHaveValue("OPEN");
  await page.goBack();
  await expect(page.getByRole("combobox", { name: "Lifecycle", exact: true })).toHaveValue("CONFIRMED");
});

test("Findings header controls do not overlap the page title", async ({ page }) => {
  await page.goto("/findings");
  await expect(page.getByLabel("Search findings", { exact: true })).toBeVisible();
  const title = await page.locator(".vedha-page-title-meta").boundingBox();
  const tools = await page.locator(".vedha-page-header-tools").boundingBox();
  expect(title).not.toBeNull();
  expect(tools).not.toBeNull();
  const separated = title!.y + title!.height <= tools!.y || title!.x + title!.width <= tools!.x;
  expect(separated).toBe(true);
});

test("assistant contains keyboard focus and returns it on close", async ({ page }, testInfo) => {
  await page.goto("/findings");
  await page.getByRole("button", { name: /Open Ask Vedha assistant/ }).click();
  await expect(page.getByRole("dialog", { name: "Ask Vedha assistant" })).toBeVisible();
  await expectFocusInside(page, ".assistant-drawer");
  for (let index = 0; index < 12; index++) {
    await page.keyboard.press(index % 2 ? "Shift+Tab" : "Tab");
    await expectFocusInside(page, ".assistant-drawer");
  }
  await expect.poll(() => page.locator(".vedha-page-main").evaluate((element) => Boolean(element.closest("[inert]")))).toBe(true);
  await page.screenshot({ path: testInfo.outputPath("assistant.png") });
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.getByRole("button", { name: /Open Ask Vedha assistant/ })).toBeFocused();
  await expect.poll(() => page.locator(".vedha-page-main").evaluate((element) => Boolean(element.closest("[inert]")))).toBe(false);
});

test("mobile navigation has protected focus and an expanded trigger", async ({ page }, testInfo) => {
  test.skip((testInfo.project.use.viewport?.width ?? 1440) >= 768, "Mobile drawer only");
  await page.goto("/findings");
  const trigger = page.locator('[aria-controls="operator-navigation"]');
  await trigger.click();
  await expect(trigger).toHaveAttribute("aria-expanded", "true");
  await expectFocusInside(page, "#operator-navigation");
  await page.keyboard.press("Shift+Tab");
  await expectFocusInside(page, "#operator-navigation");
  await page.keyboard.press("Escape");
  await expect(trigger).toBeFocused();
  await expect(trigger).toHaveAttribute("aria-expanded", "false");
});

test("dashboard failure does not present healthy status", async ({ page }, testInfo) => {
  await page.route("**/api/findings/sla-summary", (route) => respond(route, { error: "SLA service unavailable" }, 503));
  await page.goto("/");
  await expect(page.getByText("SLA status unavailable.", { exact: false })).toBeVisible({ timeout: 15000 });
  await expect(page.getByText("System Nominal")).toHaveCount(0);
  await expect(page.getByLabel("Live", { exact: true })).toHaveCount(0);
  await expect(page.getByRole("img", { name: "S L A status unavailable" })).toContainText("—");
  await page.screenshot({ path: testInfo.outputPath("dashboard-unavailable.png") });
});

test("setup retry preserves typed scope and distinguishes failed probe inventory", async ({ page }, testInfo) => {
  let failed = true;
  await page.route("**/api/scan/use-cases", (route) => respond(route, catalog));
  await page.route("**/api/scan/probes", (route) => respond(route, failed ? { error: "Probe inventory unavailable" } : probes, failed ? 503 : 200));
  await page.goto("/scan");
  await expect(page.getByText("Scan setup is unavailable")).toBeVisible();
  await expect(page.getByText("Probe inventory: Probe inventory unavailable")).toBeVisible();
  await page.locator("#scan-scope").fill("192.0.2.20");
  await expect(page.getByRole("button", { name: "Launch Scan", exact: true })).toBeDisabled();
  await page.screenshot({ path: testInfo.outputPath("scan-unavailable.png") });
  failed = false;
  await page.getByRole("button", { name: "Retry setup" }).click();
  await expect(page.getByText("Scan setup is unavailable")).toHaveCount(0);
  await expect(page.locator("#scan-scope")).toHaveValue("192.0.2.20");
  await expect(page.getByRole("button", { name: "Launch Scan", exact: true })).toBeEnabled();
});

test("job polling failure keeps the job and retries without launching again", async ({ page }) => {
  let failed = true;
  let launches = 0;
  await page.route("**/api/scan/use-cases", (route) => respond(route, catalog));
  await page.route("**/api/scan/probes", (route) => respond(route, probes));
  await page.route("**/api/scan/launch", (route) => { launches++; return respond(route, { job_id: "job-e2e", status: "pending" }); });
  await page.route("**/api/scan/jobs/job-e2e", (route) => respond(route, failed ? { error: "Status unavailable" } : { job_id: "job-e2e", engagement_id: "e2e", status: "running", use_case_id: "uc_network_va", result: null }, failed ? 503 : 200));
  await page.goto("/scan");
  await page.getByRole("button", { name: "Launch Scan", exact: true }).click();
  await expect(page.getByText("Job status may be out of date")).toBeVisible();
  failed = false;
  await page.getByRole("button", { name: "Retry job status" }).click();
  await expect(page.getByText("Job status may be out of date")).toHaveCount(0);
  expect(launches).toBe(1);
});


test("advanced filters show applied scope and can be removed independently", async ({ page }) => {
  await page.goto("/findings?severity=HIGH&ip=192.0.2.10&scan=SCN-1");
  await expect(page.getByRole("button", { name: "Remove HIGH filter" })).toBeVisible();
  await page.getByRole("button", { name: "Remove HIGH filter" }).click();
  await expect.poll(() => page.evaluate(() => new URLSearchParams(location.search).has("severity"))).toBe(false);
  await expect.poll(() => page.evaluate(() => new URLSearchParams(location.search).get("ip"))).toBe("192.0.2.10");
  await page.getByText("More filters", { exact: false }).click();
  await expect(page.getByLabel("Asset IP", { exact: true })).toHaveValue("192.0.2.10");
  await page.reload();
  await expect(page.getByRole("button", { name: "Remove IP: 192.0.2.10 filter" })).toBeVisible();
});

test("refresh retains queue work without navigating the document", async ({ page }) => {
  let documents = 0;
  page.on("request", (request) => { if (request.resourceType() === "document") documents++; });
  await page.goto("/findings?search=CVE");
  await page.getByText("More filters", { exact: false }).click();
  await page.getByRole("button", { name: "Compare scans", exact: true }).click();
  await page.getByRole("button", { name: "Refresh data", exact: true }).click();
  await expect(page.getByRole("status").filter({ hasText: "Active data refreshed" })).toBeVisible({ timeout: 15000 });
  await expect(page.getByLabel("Search findings", { exact: true })).toHaveValue("CVE");
  await expect(page.getByRole("region", { name: "Compare two scans" })).toBeVisible();
  expect(documents).toBe(1);
});

test("failed refresh offers recovery and retains the queue scope", async ({ page }) => {
  await page.goto("/findings?search=CVE");
  await expect(page.getByLabel("Search findings", { exact: true })).toHaveValue("CVE");
  await page.route("**/api/findings?**", (route) => respond(route, { error: "Queue unavailable" }, 503));
  await page.getByRole("button", { name: "Refresh data", exact: true }).click();
  await expect(page.getByText("Refresh failed. Retry.", { exact: true })).toBeVisible({ timeout: 20000 });
  await expect(page.getByLabel("Search findings", { exact: true })).toHaveValue("CVE");
  await page.unroute("**/api/findings?**");
  await page.getByRole("button", { name: "Retry refresh", exact: true }).click();
  await expect(page.getByRole("status").filter({ hasText: "Active data refreshed" })).toBeVisible({ timeout: 15000 });
});

test("portal attention handoff stays inside the customer workspace", async ({ page }) => {
  await page.goto("/portal");
  await page.getByRole("button", { name: /1 critical finding/ }).click();
  await expect(page).toHaveURL(/\/portal\/findings\?severity=CRITICAL&status=open/);
  await expect(page.getByRole("button", { name: "Remove CRITICAL filter" })).toBeVisible();
});

test("portal mobile navigation protects focus and restores its trigger", async ({ page }, info) => {
  test.skip((info.project.use.viewport?.width ?? 1440) >= 768, "Mobile drawer only");
  await page.goto("/portal/findings");
  const trigger = page.getByRole("button", { name: "Open sidebar" });
  await trigger.click();
  await expectFocusInside(page, "#operator-navigation");
  await page.keyboard.press("Shift+Tab");
  await expectFocusInside(page, "#operator-navigation");
  await page.keyboard.press("Escape");
  await expect(trigger).toBeFocused();
  await expect(page.locator('#operator-navigation')).toHaveAttribute("inert", "");
});

test("report readiness and metadata remain available in print", async ({ page }) => {
  await page.goto("/reports");
  await expect(page.getByRole("region", { name: "Report handoff readiness" })).toBeVisible();
  const metadata = page.locator(".cr-generation-details");
  await expect(metadata).not.toHaveAttribute("open", "");
  await metadata.locator("summary").click();
  await expect(metadata.getByText("Schema version", { exact: true })).toBeVisible();
  await metadata.locator("summary").click();
  await page.emulateMedia({ media: "print" });
  await expect(metadata.getByText("Schema version", { exact: true })).toBeVisible();
  await expect(page.getByRole("region", { name: "Report handoff readiness" })).toBeHidden();
});

for (const path of ["/findings", "/scan", "/reports"]) {
  test(`${path} supports dark theme, reduced motion and enlarged text`, async ({ page }, info) => {
    await page.addInitScript(() => localStorage.setItem("vedha-theme", "dark"));
    await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
    await page.goto(path);
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    await expect(page.getByRole("heading", { level: 1 }).first()).toBeVisible();
    await page.screenshot({ path: info.outputPath(`${path.slice(1)}-dark.png`), fullPage: false });
    await page.addStyleTag({ content: "html { zoom: 2; }" });
    await expect(page.getByRole("heading", { level: 1 }).first()).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    expect(overflow).toBe(false);
    const animated = await page.locator(".vedha-sidebar").evaluate((element) => getComputedStyle(element).transitionDuration);
    expect(animated).toBe("0s");
  });
}


test.describe("touch affordances", () => {
  test.use({ hasTouch: true });
  test("visible task controls meet the product's 44px target", async ({ page }) => {
    await page.goto("/findings");
    await page.getByText("More filters", { exact: false }).click();
    const undersized = await page.evaluate(() => {
      const inViewport = (element: Element) => {
        const box = element.getBoundingClientRect();
        return box.width > 0 && box.height > 0 && box.top < innerHeight && box.bottom > 0
          && box.left < innerWidth && box.right > 0 && getComputedStyle(element).visibility !== "hidden"
          && !element.closest("[inert]");
      };
      return Array.from(document.querySelectorAll("button, input, select, summary, nav a"))
        .filter(inViewport).flatMap((element) => {
          const box = element.getBoundingClientRect();
          return box.height < 43.5 || box.width < 43.5 ? [`${element.getAttribute("aria-label") ?? element.textContent?.trim()}: ${box.width}×${box.height}`] : [];
        });
    });
    expect(undersized).toEqual([]);
  });
});


test("saved report failure recovers into a keyboard-safe viewer", async ({ page }) => {
  let failed = true;
  await page.route("**/api/portal/reports", (route) => respond(route, [{ id: "doc-e2e", output_type: "executive_summary", model: "reviewed", generated_at: "2026-09-30T10:30:00Z" }]));
  await page.route("**/api/portal/reports/doc-e2e", (route) => respond(route, failed ? { error: "Report unavailable" } : { id: "doc-e2e", output_type: "executive_summary", model: "reviewed", content: "Recorded assessment report" }, failed ? 503 : 200));
  await page.goto("/portal/reports");
  await page.getByRole("tab", { name: "Documents", exact: true }).click();
  await page.getByRole("button", { name: "View executive summary", exact: true }).click();
  await expect(page.getByText("Could not open the report:", { exact: false })).toBeVisible();
  failed = false;
  const retry = page.getByRole("button", { name: "Retry document", exact: true });
  await retry.click();
  await expect(page.getByRole("dialog", { name: "executive summary report" })).toBeVisible();
  await page.keyboard.press("Tab");
  await expectFocusInside(page, '[role="dialog"]');
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(retry).toHaveCount(0);
  await expect(page.getByRole("button", { name: "View executive summary", exact: true })).toBeFocused();
});


test("phone triage keeps queue search in the initial viewport", async ({ page }, info) => {
  test.skip((info.project.use.viewport?.width ?? 1440) >= 768, "Phone hierarchy only");
  await page.goto("/findings");
  await expect(page.getByLabel("Search findings", { exact: true })).toBeVisible();
  const search = await page.getByLabel("Search findings", { exact: true }).boundingBox();
  expect(search).not.toBeNull();
  expect(search!.y + search!.height).toBeLessThan(info.project.use.viewport!.height);
  // A short list needs no fix-first cards: they would only repeat the rows right below,
  // so there is no urgent toggle to open and the finding itself is the next thing on screen.
  await expect(page.getByRole("button", { name: /urgent finding/ })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /^SMBv1 enabled/ })).toBeVisible();
});

test("a finding shows the full working of its risk score and priority", async ({ page }) => {
  await page.goto("/findings");
  await page.locator(".finding-card-open").first().click();
  await page.getByRole("link", { name: "How is this calculated?" }).click();
  const calc = page.locator("#risk-calculation");
  await expect(calc.getByText("393.6 + 225.0 + 100.0 + 120.0 = 838.6")).toBeVisible();
  await expect(calc.getByText("750 + 0.7544 × (1000 − 750) = 940")).toBeVisible();
  await expect(calc.getByText(/3 inputs were not recorded/)).toBeVisible();
  await expect(calc.getByText("Decided this")).toBeVisible();
});

test("comparing two scans starts empty, then separates new, fixed, changed and unchanged", async ({ page }) => {
  await page.goto("/findings");
  await page.getByText("More filters", { exact: false }).click();
  await page.getByRole("button", { name: "Compare scans", exact: true }).click();
  const panel = page.getByRole("region", { name: "Compare two scans" });
  // Nothing is pre-selected: the operator chooses both scans.
  await expect(panel.getByLabel("Baseline (earlier scan)")).toHaveValue("");
  await expect(panel.getByLabel("Target (later scan)")).toHaveValue("");
  await panel.getByLabel("Baseline (earlier scan)").selectOption("SCN-261009-OLDER0");
  await panel.getByLabel("Target (later scan)").selectOption("SCN-261016-NEWEST");
  await expect(panel.getByText("1 new, 1 fixed, 1 changed between SCN-261009-OLDER0 and SCN-261016-NEWEST.")).toBeVisible();
  // Opens on the worst news; the other buckets are one click away.
  await expect(panel.getByRole("tab", { name: /New/ })).toHaveAttribute("aria-selected", "true");
  await expect(panel.getByText("Redis exposed without authentication")).toBeVisible();
  await panel.getByRole("tab", { name: /Changed/ }).click();
  await expect(panel.getByText("Severity medium → high")).toBeVisible();
  await expect(panel.getByText("Risk 400 → 520 (+120)")).toBeVisible();
  await panel.getByRole("tab", { name: /Unchanged/ }).click();
  await expect(panel.getByText("TLS 1.0 accepted")).toBeVisible();
  await expect(panel.getByText("Outdated OpenSSH")).toHaveCount(0);
  // Exports are real links to the server's uncapped file.
  await expect(panel.getByRole("link", { name: "CSV" })).toHaveAttribute("href", /\/api\/findings\/compare\/export\?a=SCN-261009-OLDER0&b=SCN-261016-NEWEST&format=csv/);
  // The same scan cannot be both sides.
  await expect(panel.getByLabel("Target (later scan)").locator("option", { hasText: "SCN-261009-OLDER0" })).toHaveJSProperty("disabled", true);
});

test("the audit log shows the integrity check, filters by outcome and opens an entry in full", async ({ page }) => {
  await page.goto("/settings?section=audit-log");
  await expect(page.getByText("Tamper check passed: 1,284 entries verified in order.")).toBeVisible();
  await expect(page.getByText("Entries are kept for 365 days")).toBeVisible();
  await expect(page.getByText("Sign-in failed", { exact: true })).toBeVisible();
  const request = page.waitForRequest((r) => r.url().includes("/api/audit-logs?") && r.url().includes("outcome=failure"));
  await page.getByRole("button", { name: /^Failed/ }).click();
  await request;
  await page.getByRole("button", { name: /Sign-in failed/ }).first().click();
  await expect(page.getByText("ghost@example.test").first()).toBeVisible();
  await expect(page.getByText("user_not_found")).toBeVisible();
  await expect(page.getByRole("link", { name: /CSV/ })).toHaveAttribute("href", /\/api\/audit-logs\/export\?.*outcome=failure/);
});

test("a customer sees their own activity record without operator addresses", async ({ page }) => {
  await page.goto("/portal/settings?section=audit-log");
  await expect(page.getByText("Scan requested")).toBeVisible();
  await expect(page.getByText("Vedha analyst")).toBeVisible();
  await expect(page.getByText("Tamper check")).toHaveCount(0);
  await expect(page.getByRole("link", { name: /CSV/ })).toHaveCount(0);
});
