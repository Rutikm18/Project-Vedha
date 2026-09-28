import assert from "node:assert/strict";
import { describe, test } from "node:test";

import {
  DEFAULT_REPORT_FILTERS, REPORT_STATUS, describeReportFilters, isReportFiltered, reportFilterQuery, reportStatus,
} from "../lib/report/filters";
import { createRemediationApi } from "../lib/remediation";

describe("report status vocabulary", () => {
  test("every backend status reads as open / closed / accepted for a client", () => {
    assert.equal(reportStatus("open").label, "Open");
    assert.equal(reportStatus("confirmed").label, "Open · confirmed");
    assert.equal(reportStatus("remediated").label, "Closed · fixed");
    assert.equal(reportStatus("accepted").label, "Risk accepted");
    assert.equal(reportStatus("fp").label, "Closed · false positive");
    assert.equal(reportStatus("FALSE_POSITIVE").key, "FALSE_POSITIVE");
  });

  test("accepted risk is NOT counted as closed — it is still an exposure", () => {
    assert.equal(REPORT_STATUS.ACCEPTED.closed, false);
    assert.equal(REPORT_STATUS.REMEDIATED.closed, true);
  });
});

describe("report filters", () => {
  test("defaults are unfiltered and produce no query", () => {
    assert.equal(isReportFiltered(DEFAULT_REPORT_FILTERS), false);
    assert.equal(reportFilterQuery(DEFAULT_REPORT_FILTERS), "");
    assert.equal(isReportFiltered({ ...DEFAULT_REPORT_FILTERS, search: "   " }), false);
  });

  test("query uses the Findings page's parameter names and casing", () => {
    const q = new URLSearchParams(reportFilterQuery({
      search: " smb ", severity: "HIGH", status: "ACCEPTED", ip: "10.0.0.", scan: "SCN-260928-ABC123",
      exploited: true, slaBreached: true,
    }));
    assert.deepEqual(Object.fromEntries(q), {
      search: "smb", severity: "HIGH", status: "ACCEPTED", asset_ip: "10.0.0.", scan: "SCN-260928-ABC123",
      exploit_validated: "true", sla_breached: "true",
    });
  });

  test("a filtered report describes itself in plain words", () => {
    const notes = describeReportFilters(
      { ...DEFAULT_REPORT_FILTERS, status: "ACCEPTED", severity: "CRITICAL", ip: "10.0.0.5", scan: "job-1" },
      v => (v === "job-1" ? "SCN-1" : v),
    );
    assert.deepEqual(notes, ["Status: Risk accepted", "Severity: Critical", "Host: 10.0.0.5", "Scan: SCN-1"]);
  });
});

describe("filtered Excel/CSV export URLs", () => {
  const filters = reportFilterQuery({ ...DEFAULT_REPORT_FILTERS, status: "FALSE_POSITIVE", severity: "HIGH", ip: "10.0.0." });

  test("operator: filters go out in the backend's casing", () => {
    const url = new URL(createRemediationApi("manager").exportUrl("e1", "csv", "findings", filters), "http://x");
    assert.equal(url.pathname, "/api/engagements/e1/remediation/export");
    assert.equal(url.searchParams.get("status"), "fp");
    assert.equal(url.searchParams.get("severity"), "high");
    assert.equal(url.searchParams.get("asset_ip"), "10.0.0.");
    assert.equal(url.searchParams.get("format"), "csv");
    assert.equal(url.searchParams.get("sheet"), "findings");
  });

  test("portal: same filters, engagement pinned server-side", () => {
    const url = new URL(createRemediationApi("portal").exportUrl("ignored", "xlsx", undefined, filters), "http://x");
    assert.equal(url.pathname, "/api/portal/remediation/export");
    assert.equal(url.searchParams.get("status"), "fp");
    assert.equal(url.searchParams.get("format"), "xlsx");
    assert.equal(url.searchParams.has("sheet"), false);
  });

  test("unfiltered export URL is unchanged", () => {
    assert.equal(createRemediationApi("portal").exportUrl("x", "xlsx"), "/api/portal/remediation/export?format=xlsx");
  });
});
