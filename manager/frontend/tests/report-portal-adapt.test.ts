import { test } from "node:test";
import assert from "node:assert/strict";

import { portalToRawFinding } from "../lib/report/adapt";
import { assess } from "../lib/report/finding-model";

const pf = (o: Record<string, unknown> = {}) => ({
  id: "P1", title: "t", description: "d", severity: "high", status: "open",
  cvss_score: 7.5, cve_ids: ["CVE-2024-1"], risk_score: 700,
  remediation: "patch", first_seen: "2026-08-01T00:00:00Z", ...o,
});

test("portal: no internal fields ever leak", () => {
  const r = portalToRawFinding(pf() as any);
  assert.equal(r.evidence.length, 0);          // never carries evidence
  assert.equal(r.exploitValidated, undefined); // not set
  assert.equal(r.activelyExploited, false);
  assert.equal(r.technicalDetails, "");
});

test("portal: keeps client-facing fields", () => {
  const r = portalToRawFinding(pf() as any);
  assert.equal(r.cvss, "7.5");
  assert.deepEqual(r.cve, ["CVE-2024-1"]);
  assert.deepEqual(r.remediation, ["patch"]);
  assert.equal(r.discoveredAt, "2026-08-01T00:00:00Z");
});

test("portal: null-ish fields degrade safely", () => {
  const r = portalToRawFinding(pf({
    description: null, cvss_score: null, cve_ids: null, risk_score: null,
    remediation: null, first_seen: null, severity: "low",
  }) as any);
  assert.equal(r.cvss, "");
  assert.equal(r.remediation.length, 0);
  assert.equal(r.description, "");
  assert.equal(r.discoveredAt, "");
});

test("portal: assess() runs clean and prioritises by severity alone", () => {
  const a = assess(portalToRawFinding(pf({ severity: "critical", cvss_score: 9.8 }) as any));
  assert.equal(a.severity, "CRITICAL");
  assert.equal(a.priority.code, "P1"); // critical, no exploitation signal
  assert.equal(a.readiness.gaps.length > 0, true); // gaps exist internally…
});
