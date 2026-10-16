/**
 * Per-scan-findings adapters: the scan block on a finding, the scan-option list,
 * and the compare result all cross the snake_case → camelCase boundary here, and
 * every consumer (operator BFF + portal transport) shares these mappers.
 */
import assert from "node:assert/strict";
import test from "node:test";

import { toUiFinding, mapScanOption, mapScanRef, mapCompareResult } from "../lib/adapters";

test("toUiFinding surfaces the scan block (snake → camel)", () => {
  const ui = toUiFinding({
    id: "f", title: "t", severity: "high", status: "open",
    scan: {
      reference: "SCN-260301-ABC123", use_case_id: "uc_network_sweep",
      intensity: "aggressive", scanned_at: "2026-03-01T12:00:00Z",
      job_id: "job-1", run_id: "run-1",
    },
  });
  assert.deepEqual(ui.scan, {
    reference: "SCN-260301-ABC123", useCaseId: "uc_network_sweep",
    intensity: "aggressive", scannedAt: "2026-03-01T12:00:00Z",
    jobId: "job-1", runId: "run-1",
  });
});

test("a finding with no scan link maps to scan: null", () => {
  const ui = toUiFinding({ id: "f", title: "t", severity: "low", status: "open" });
  assert.equal(ui.scan, null);
  assert.equal(ui.scanOutcome, null);
});

test("toUiFinding surfaces the filtered scan's outcome", () => {
  const ui = toUiFinding({ id: "f", title: "t", severity: "high", status: "open", scan_outcome: "new" });
  assert.equal(ui.scanOutcome, "new");
});

test("mapScanOption carries the finding count and identity", () => {
  const opt = mapScanOption({
    job_id: "job-1", reference: "SCN-260301-ABC123", use_case_id: "uc_deep_port_sweep",
    intensity: "aggressive", scanned_at: "2026-03-01T12:00:00Z", status: "completed", findings: 7,
  });
  assert.equal(opt.jobId, "job-1");
  assert.equal(opt.reference, "SCN-260301-ABC123");
  assert.equal(opt.findings, 7);
  assert.equal(opt.status, "completed");
});

test("mapScanRef tolerates a null side", () => {
  assert.equal(mapScanRef(null), null);
  assert.equal(mapScanRef({ reference: "SCN-1", use_case_id: null }).reference, "SCN-1");
});

test("mapCompareResult buckets and counts both sides", () => {
  const out = mapCompareResult({
    a: { reference: "SCN-A", scanned_at: "2026-03-01T00:00:00Z" },
    b: { reference: "SCN-B", scanned_at: "2026-03-02T00:00:00Z" },
    counts: { new: 2, fixed: 1, still_present: 3 },
    new: [{ id: "n1", title: "n1", severity: "high", status: "open" },
          { id: "n2", title: "n2", severity: "low", status: "open" }],
    fixed: [{ id: "x1", title: "x1", severity: "medium", status: "remediated" }],
    still_present: [{ id: "s1" }, { id: "s2" }, { id: "s3" }],
  });
  assert.equal(out.a?.reference, "SCN-A");
  assert.equal(out.b?.reference, "SCN-B");
  assert.deepEqual(out.counts, { new: 2, fixed: 1, stillPresent: 3, changed: 0 });
  assert.equal(out.new.length, 2);
  assert.equal(out.fixed.length, 1);
  assert.equal(out.stillPresent.length, 3);
  // Items are UI-shaped findings, not raw rows.
  assert.equal(out.new[0].id, "n1");
  assert.equal(out.new[0].scan, null);
});
