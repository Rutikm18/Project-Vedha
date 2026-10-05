import { mockApi, settle } from "./mock-api";
import { expect, test } from "@playwright/test";

const ROUTES = [
  { path: "/", slug: "dashboard" },
  { path: "/engagements", slug: "engagements" },
  { path: "/engagements/e2e", slug: "engagements-e2e" },
  { path: "/scan", slug: "scan" },
  { path: "/campaign", slug: "campaign" },
  { path: "/fleet", slug: "fleet" },
  { path: "/findings", slug: "findings" },
  { path: "/findings?finding=finding-e2e", slug: "findings-detail" },
  { path: "/reports", slug: "reports" },
  { path: "/customers", slug: "customers" },
  { path: "/aibrain", slug: "aibrain" },
  { path: "/settings", slug: "settings" },
  { path: "/portal", slug: "portal" },
  { path: "/portal/findings", slug: "portal-findings" },
  { path: "/portal/scans", slug: "portal-scans" },
  { path: "/portal/fleet", slug: "portal-fleet" },
  { path: "/portal/scope", slug: "portal-scope" },
  { path: "/portal/reports", slug: "portal-reports" },
  { path: "/portal/assistant", slug: "portal-assistant" },
  { path: "/portal/settings", slug: "portal-settings" },
] as const;


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

for (const { path, slug } of ROUTES) {
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

    const layoutViolations = await page.evaluate(() => {
      const violations: string[] = [];
      const visible = (element: Element | null): element is HTMLElement => {
        if (!(element instanceof HTMLElement)) return false;
        const rect = element.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
      };

      const headerLeft = document.querySelector(".vedha-page-header-left");
      const headerTools = document.querySelector(".vedha-page-header-tools");
      if (visible(headerLeft) && visible(headerTools)) {
        const left = headerLeft.getBoundingClientRect();
        const tools = headerTools.getBoundingClientRect();
        const sharesRow = left.top < tools.bottom - 1 && tools.top < left.bottom - 1;
        if (sharesRow && left.right > tools.left + 1) {
          violations.push(`Page header regions overlap by ${Math.ceil(left.right - tools.left)}px`);
        }
      }

      const filterPanel = document.querySelector(".findings-filter-panel");
      if (visible(filterPanel)) {
        const panel = filterPanel.getBoundingClientRect();
        document.querySelectorAll(".findings-filter-panel .findings-filter-group").forEach((group) => {
          if (!visible(group)) return;
          const rect = group.getBoundingClientRect();
          if (rect.left < panel.left - 1 || rect.right > panel.right + 1) {
            violations.push(`Findings filter escapes its panel: ${group.textContent?.trim().slice(0, 40) ?? "unnamed filter"}`);
          }
        });
      }

      return violations;
    });
    expect(layoutViolations, `${path} has overlapping or escaped layout regions`).toEqual([]);

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
