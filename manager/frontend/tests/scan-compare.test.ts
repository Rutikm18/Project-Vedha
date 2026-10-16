import { test } from "node:test";
import assert from "node:assert/strict";
import { mapCompareResult } from "../lib/adapters";
import {
  baselineIsNewer, compareExportHref, compareHeadline, defaultTab, formatDelta, netChange,
  snapshotLine, tabCounts, truncatedBy, unchangedFindings,
  type CompareChange, type CompareResult, type CompareScanRef, type CompareSummary,
} from "../lib/scan-compare";

const ref = (reference: string, scannedAt: string | null = null): CompareScanRef => ({
  reference, scannedAt, useCaseId: null, intensity: null, jobId: null, runId: null,
});
const summary = (total: number): CompareSummary => ({ total, bySeverity: {}, averageRisk: null, fromSnapshot: true });

test("unchanged is what is still present minus what changed", () => {
  const counts = tabCounts({ counts: { new: 2, fixed: 1, stillPresent: 5, changed: 2 } });
  assert.deepEqual(counts, { new: 2, fixed: 1, changed: 2, unchanged: 3 });
  assert.equal(tabCounts({ counts: { new: 0, fixed: 0, stillPresent: 1, changed: 4 } }).unchanged, 0);
});

test("the default tab is the worst news first", () => {
  assert.equal(defaultTab({ new: 1, fixed: 5, changed: 3, unchanged: 9 }), "new");
  assert.equal(defaultTab({ new: 0, fixed: 5, changed: 3, unchanged: 9 }), "changed");
  assert.equal(defaultTab({ new: 0, fixed: 5, changed: 0, unchanged: 9 }), "fixed");
  assert.equal(defaultTab({ new: 0, fixed: 0, changed: 0, unchanged: 9 }), "unchanged");
});

test("unchangedFindings drops the findings that moved", () => {
  const f = (id: string) => ({ id });
  const result = {
    stillPresent: [f("a"), f("b"), f("c")],
    changed: [{ finding: f("b") } as CompareChange<{ id: string }>],
  } as CompareResult<{ id: string }>;
  assert.deepEqual(unchangedFindings(result).map((x) => x.id), ["a", "c"]);
});

test("deltas carry a sign, and no score reads as a dash", () => {
  assert.equal(formatDelta(120), "+120");
  assert.equal(formatDelta(-40.04), "−40");
  assert.equal(formatDelta(0), "±0");
  assert.equal(formatDelta(null), "—");
});

test("the headline names both scans and is honest when nothing moved", () => {
  const a = ref("SCN-A");
  const b = ref("SCN-B");
  assert.equal(compareHeadline({ new: 3, fixed: 0, changed: 1, unchanged: 4 }, a, b), "3 new, 1 changed between SCN-A and SCN-B.");
  assert.match(compareHeadline({ new: 0, fixed: 0, changed: 0, unchanged: 4 }, a, b), /^Nothing moved between SCN-A and SCN-B/);
});

test("net change needs both scan summaries", () => {
  assert.equal(netChange(summary(10), summary(7)), -3);
  assert.equal(netChange(null, summary(7)), null);
});

test("a baseline that ran after the target is flagged", () => {
  assert.equal(baselineIsNewer(ref("A", "2026-10-02T00:00:00Z"), ref("B", "2026-10-01T00:00:00Z")), true);
  assert.equal(baselineIsNewer(ref("A", "2026-10-01T00:00:00Z"), ref("B", "2026-10-02T00:00:00Z")), false);
  assert.equal(baselineIsNewer(ref("A"), ref("B", "2026-10-02T00:00:00Z")), false);
});

test("a capped list reports how many rows the export has that the screen does not", () => {
  assert.equal(truncatedBy(620, 500), 120);
  assert.equal(truncatedBy(3, 3), 0);
});

test("export links go to the surface's own route and keep the engagement pin for operators only", () => {
  assert.equal(
    compareExportHref("manager", "SCN-A", "SCN-B", "csv", "eng-1"),
    "/api/findings/compare/export?a=SCN-A&b=SCN-B&format=csv&engagement_id=eng-1",
  );
  assert.equal(
    compareExportHref("portal", "SCN-A", "SCN-B", "json", "eng-1"),
    "/api/portal/workspace/findings/compare/export?a=SCN-A&b=SCN-B&format=json",
  );
});

test("what moved is written out, skipping what did not", () => {
  const change = {
    severityChanged: true, statusChanged: false, riskDelta: 120,
    before: { severity: "MEDIUM", riskScore: 400, status: "OPEN" },
    after: { severity: "HIGH", riskScore: 520, status: "OPEN" },
  } as CompareChange<unknown>;
  assert.deepEqual(snapshotLine(change), ["Severity medium → high", "Risk 400 → 520 (+120)"]);
  const statusOnly = { ...change, severityChanged: false, statusChanged: true, riskDelta: 0,
    after: { severity: "MEDIUM", riskScore: 400, status: "FALSE_POSITIVE" } } as CompareChange<unknown>;
  assert.deepEqual(snapshotLine(statusOnly), ["Status open → false positive"]);
});

test("the adapter maps the server's compare shape, including changed and summaries", () => {
  const finding = { id: "f1", title: "x", severity: "high", status: "open" };
  const mapped = mapCompareResult({
    a: { reference: "SCN-A" }, b: { reference: "SCN-B" },
    counts: { new: 1, fixed: 0, still_present: 1, changed: 1 },
    summary_a: { total: 1, by_severity: { critical: 0, high: 1 }, average_risk: 600, from_snapshot: true },
    summary_b: { total: 2, by_severity: { high: 2 }, average_risk: null, from_snapshot: false },
    new: [finding], fixed: [], still_present: [finding],
    changed: [{
      finding, severity_changed: true, status_changed: false, risk_delta: 40,
      before: { severity: "medium", risk_score: 400, status: "open" },
      after: { severity: "high", risk_score: 440, status: "fp" },
    }],
  });
  assert.equal(mapped.counts.changed, 1);
  assert.deepEqual(mapped.summaryA?.bySeverity, { CRITICAL: 0, HIGH: 1 });
  assert.equal(mapped.summaryB?.fromSnapshot, false);
  assert.equal(mapped.changed[0].finding.id, "f1");
  assert.deepEqual(mapped.changed[0].after, { severity: "HIGH", riskScore: 440, status: "FALSE_POSITIVE" });
  assert.equal(mapped.changed[0].riskDelta, 40);
});

test("a compare from an older server still maps (no changed, no summaries)", () => {
  const mapped = mapCompareResult({ counts: { new: 0, fixed: 0, still_present: 0 }, new: [], fixed: [], still_present: [] });
  assert.equal(mapped.counts.changed, 0);
  assert.deepEqual(mapped.changed, []);
  assert.equal(mapped.summaryA, null);
});
