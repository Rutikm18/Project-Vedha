import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { PortalReportTabContent } from "../app/portal/reports/workspace";
import type {
  PortalFinding,
  PortalSummary,
  PortalTrends,
} from "../lib/portal-client";

const summary: PortalSummary = {
  posture: {
    risk_index: 38,
    exploitable_score: 20,
    posture_score: 71,
    grade: "B",
    open_findings: 1,
  },
  open_findings: 1,
  closed_findings: 2,
  severity_counts: { critical: 0, high: 1, medium: 0, low: 0, info: 0 },
  pending_requests: 0,
  running_jobs: 0,
};

const trends: PortalTrends = {
  by_severity: { critical: 0, high: 1, medium: 0, low: 0, info: 0 },
  timeline: [],
};

const findings: PortalFinding[] = [{
  id: "finding-1",
  title: "Recorded TLS weakness",
  description: "The endpoint negotiates a deprecated protocol.",
  severity: "high",
  status: "open",
  cvss_score: 7.5,
  cve_ids: [],
  risk_score: 750,
  remediation: "Disable the deprecated protocol.",
  first_seen: "2026-09-25T10:00:00Z",
}];

describe("portal live report renderer", () => {
  test("mounts every live report section even when one screen tab is active", () => {
    const html = renderToStaticMarkup(createElement(PortalReportTabContent, {
      tab: "executive",
      summary,
      trends,
      findings,
    }));

    assert.match(html, /data-report-section="executive"/);
    assert.match(html, /data-report-section="findings"/);
    assert.match(html, /Recorded TLS weakness/);
    assert.match(html, /data-active="false"/);
  });

  test("does not describe every terminal disposition as verified closure", () => {
    const html = renderToStaticMarkup(createElement(PortalReportTabContent, {
      tab: "executive",
      summary,
      trends,
      findings,
    }));

    assert.doesNotMatch(html, /Verified and closed/);
    assert.match(html, /verification may be absent/i);
  });

  test("on screen only the active report section is displayed; print reveals them all", () => {
    const css = readFileSync(new URL("../app/globals.css", import.meta.url), "utf8");
    const hide = css.search(/\.portal-report-tab-pane\[data-active="false"\]\s*{\s*display:\s*none;/);
    const reveal = css.search(/@media print\s*{\s*\.portal-report-tab-pane\s*{\s*display:\s*block\s*!important;/);
    assert.ok(hide >= 0, "the inactive section must be hidden on screen");
    assert.ok(reveal > hide, "the print rule must come after, and override, the screen rule");
  });

  test("reveals every mounted live report section for print", () => {
    const css = readFileSync(new URL("../app/globals.css", import.meta.url), "utf8");
    assert.match(
      css,
      /@media print\s*{[\s\S]*?\.portal-report-tab-pane\s*{\s*display:\s*block\s*!important;/,
    );
  });

  test("returns the portal shell, wrapper and report main to document flow for print", () => {
    const css = readFileSync(new URL("../app/globals.css", import.meta.url), "utf8");

    assert.match(
      css,
      /@media print\s*{[\s\S]*?\.portal-shell\s*,\s*\.portal-shell-frame\s*,\s*\.portal-page-main\s*{[\s\S]*?height:\s*auto\s*!important;[\s\S]*?overflow:\s*visible\s*!important;/,
    );
    assert.match(
      css,
      /@media print\s*{[\s\S]*?\.portal-shell-frame\s*{[\s\S]*?display:\s*block\s*!important;/,
    );
  });
});
