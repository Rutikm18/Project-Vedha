import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

const reportsPage = readFileSync(join(process.cwd(), "app/reports/workspace.tsx"), "utf8");

test("manager reports render the complete canonical document", () => {
  assert.match(reportsPage, /CanonicalReportDocument/);
  assert.match(reportsPage, /CanonicalReportsWorkspace/);
  assert.match(reportsPage, /report-document/);
  assert.match(reportsPage, /ReportExportMenu/);
});

test("the operator-only canonical request cannot run on the portal surface", () => {
  assert.match(reportsPage, /surface === "portal"/);
  assert.match(reportsPage, /<PortalReportsWorkspace/);

  const portalPage = readFileSync(join(process.cwd(), "app/portal/reports/page.tsx"), "utf8");
  assert.match(portalPage, /surface="portal"/);
});
