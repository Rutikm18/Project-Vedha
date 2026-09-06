import { test } from "node:test";
import assert from "node:assert/strict";

import { toRawFinding, deriveDetectionMethod, toReportAssets } from "../lib/report/adapt";

// A minimal UI-Finding-shaped object (as toUiFinding would produce).
const uiBase = {
  id: "VDH-1", title: "t", severity: "CRITICAL", status: "OPEN",
  affectedHost: "web-01", discoveredAt: "2026-08-20T09:00:00Z",
  description: "d", technicalDetails: "td", impact: "i",
  evidence: [{ label: "l", content: "c" }], remediation: ["fix it"],
  mitre: [], riskScore: 900, cvss: "9.8", cvssVector: "",
  activelyExploited: false, detectionCoverage: "BLIND",
  epssScore: 0, epssPercentile: 0, epssRecorded: false,
  exploitValidated: false, verificationState: null,
  assetContext: null,
};
const U = (o: Record<string, unknown>) => ({ ...uiBase, ...o });

test("detectionMethod: validated exploit ⇒ exploit", () => {
  assert.equal(deriveDetectionMethod(U({ exploitValidated: true })), "exploit");
});
test("detectionMethod: confirmed verification ⇒ behavioural", () => {
  assert.equal(deriveDetectionMethod(U({ verificationState: "confirmed" })), "behavioural");
});
test("detectionMethod: corroborated verification ⇒ inference", () => {
  assert.equal(deriveDetectionMethod(U({ verificationState: "corroborated" })), "inference");
});
test("detectionMethod: detectionCoverage is ignored (blue-team signal, not validation)", () => {
  // BLIND is detection coverage, not how the finding was proven — must stay Unverified.
  assert.equal(deriveDetectionMethod(U({ detectionCoverage: "BLIND" })), undefined);
});
test("detectionMethod: nothing recorded ⇒ undefined (honest 'Unverified')", () => {
  assert.equal(deriveDetectionMethod(U({})), undefined);
});

test("assets: empty when no asset context", () => {
  assert.deepEqual(toReportAssets(U({})), []);
});
test("assets: one row derived from asset context", () => {
  const rows = toReportAssets(U({
    assetContext: { hostname: "web-01", ipAddress: "10.0.0.5", environment: "internal", owner: "ops" },
  }));
  assert.equal(rows.length, 1);
  assert.equal(rows[0].host, "web-01");
  assert.equal(rows[0].ip, "10.0.0.5");
  assert.equal(rows[0].internetReachable, false);
});

test("epss: mapped only when recorded", () => {
  assert.equal(toRawFinding(U({ epssScore: 0.7, epssRecorded: true })).epss, 0.7);
  assert.equal(toRawFinding(U({ epssScore: 0, epssRecorded: false })).epss, undefined);
});
test("internetReachable: dmz environment ⇒ true", () => {
  assert.equal(
    toRawFinding(U({ assetContext: { hostname: "h", environment: "DMZ" } })).internetReachable,
    true,
  );
});
test("toRawFinding: preserves required fields for assess()", () => {
  const r = toRawFinding(U({ exploitValidated: true }));
  assert.equal(r.id, "VDH-1");
  assert.equal(r.exploitValidated, true);
  assert.equal(r.detectionMethod, "exploit");
});

test("toRawFinding: prefers backend detectionMethod over derivation", () => {
  // No local signals → derivation is undefined; the backend value must win.
  assert.equal(toRawFinding(U({ detectionMethod: "version" })).detectionMethod, "version");
});

test("toRawFinding: passes through backend verification block and KEV date", () => {
  const r = toRawFinding(U({ verification: { expected: "no longer offered" }, kevDateAdded: "2024-01-15" }));
  assert.equal(r.verification?.expected, "no longer offered");
  assert.equal(r.kevAddedAt, "2024-01-15");
});

test("toRawFinding: prefers backend internetReachable", () => {
  assert.equal(toRawFinding(U({ internetReachable: true })).internetReachable, true);
});
