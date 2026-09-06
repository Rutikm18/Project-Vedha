import { test } from "node:test";
import assert from "node:assert/strict";

import { deriveDetectionMethod, toRawFinding, toReportAssets } from "../lib/report/adapt";

const base = {
  id: "VDH-1",
  title: "Example",
  severity: "CRITICAL",
  status: "OPEN",
  affectedHost: "asset-uuid",
  discoveredAt: "2026-08-20T09:00:00Z",
  description: "Recorded description",
  technicalDetails: "",
  evidence: [{ label: "response", content: "open port 443/tcp" }],
  impact: "Recorded impact",
  remediation: ["Apply the vendor fix."],
  mitre: [],
  riskScore: 810,
  cvss: "9.8",
  cvssVector: "",
  activelyExploited: false,
  exploitedInWild: false,
  exploitValidated: false,
  kevListed: false,
  detectionCoverage: "COVERED",
  verificationState: null,
  epssRecorded: false,
  epssScore: 0,
  assetContext: null,
};

const finding = (overrides: Record<string, unknown> = {}) => ({ ...base, ...overrides });

test("validated exploitation produces confirmed exploit confidence input", () => {
  assert.equal(deriveDetectionMethod(finding({ exploitValidated: true })), "exploit");
});

test("confirmed and corroborated verification map to recorded methods", () => {
  assert.equal(deriveDetectionMethod(finding({ verificationState: "confirmed" })), "behavioural");
  assert.equal(deriveDetectionMethod(finding({ verificationState: "corroborated" })), "configuration");
});

test("coverage alone does not invent a detection method", () => {
  assert.equal(deriveDetectionMethod(finding({ detectionCoverage: "COVERED" })), undefined);
});

test("asset context is mapped without guessing internet exposure", () => {
  const assets = toReportAssets(finding({
    assetContext: {
      hostname: "web-01",
      ipAddress: "10.0.0.5",
      environment: "DMZ",
      os: "Linux",
      owner: "platform",
    },
  }));
  assert.deepEqual(assets, [{
    host: "web-01",
    ip: "10.0.0.5",
    version: "Linux",
    environment: "DMZ",
    owner: "platform",
    internetReachable: undefined,
  }]);
});

test("EPSS is emitted only when the API says it was recorded", () => {
  assert.equal(toRawFinding(finding({ epssRecorded: true, epssScore: 0.72 })).epss, 0.72);
  assert.equal(toRawFinding(finding({ epssRecorded: false, epssScore: 0 })).epss, undefined);
});

test("wild exploitation, KEV, and local validation stay distinct", () => {
  assert.equal(toRawFinding(finding({ exploitValidated: true })).activelyExploited, false);
  assert.equal(toRawFinding(finding({ kevListed: true })).activelyExploited, true);
  assert.equal(toRawFinding(finding({ exploitedInWild: true })).activelyExploited, true);
});

test("the Manager SLA deadline is passed through and never synthesized", () => {
  assert.equal(toRawFinding(finding()).dueAt, undefined);
  assert.equal(
    toRawFinding(finding(), "2026-09-10T00:00:00Z").dueAt,
    "2026-09-10T00:00:00Z",
  );
});

test("evidence provenance survives the adapter", () => {
  const raw = toRawFinding(finding({
    evidence: [{
      label: "scanner output",
      content: "port 22 open",
      tool: "nmap",
      timestamp: "2026-09-06T12:00:00Z",
      sha256: "abc123",
    }],
  }));
  assert.equal(raw.evidence[0].tool, "nmap");
  assert.equal(raw.evidence[0].capturedAt, "2026-09-06T12:00:00Z");
  assert.equal(raw.evidence[0].sha256, "abc123");
});
