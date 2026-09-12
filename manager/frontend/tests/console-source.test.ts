import assert from "node:assert/strict";
import test from "node:test";

import { consolePathFor, normalizePortalDataset } from "../lib/console-source";

test("shared console links remain inside the active surface", () => {
  assert.equal(consolePathFor("operator", "findings"), "/findings");
  assert.equal(consolePathFor("portal", "findings"), "/portal/findings");
  assert.equal(
    consolePathFor("portal", "finding", "finding/id"),
    "/portal/findings?finding=finding%2Fid",
  );
  assert.equal(consolePathFor("portal", "scans"), "/portal/scans");
});

test("portal dashboard normalizes the customer summary without inventing a clean state", () => {
  assert.deepEqual(normalizePortalDataset("findingsSummary", {
    open_findings: 22,
    closed_findings: 4,
    severity_counts: { critical: 1, high: 8, medium: 10, low: 3 },
  }), {
    total: 26,
    openTotal: 22,
    criticalOpen: 1,
    highOpen: 8,
    mediumOpen: 10,
    lowOpen: 3,
    infoOpen: 0,
    validated: 0,
    blind: 0,
    averageRisk: 0,
  });
});
