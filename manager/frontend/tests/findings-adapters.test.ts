import assert from "node:assert/strict";
import test from "node:test";

import { toApiFindingPatch, toUiFinding } from "../lib/adapters";

test("finding action reasons cross the BFF contract without changing status semantics", () => {
  assert.deepEqual(
    toApiFindingPatch({
      status: "ACCEPTED",
      actionReason: "Business owner approved the exception until the next review.",
    }),
    {
      status: "accepted",
      action_reason: "Business owner approved the exception until the next review.",
    },
  );
});

test("finding detail maps bounded asset context for the overview", () => {
  const finding = toUiFinding({
    id: "finding-1",
    title: "Exposed service",
    severity: "high",
    status: "open",
    created_at: "2026-09-01T00:00:00Z",
    asset_context: {
      id: "asset-1",
      ip_address: "192.0.2.10",
      hostname: "edge-01",
      fqdn: "edge-01.example.test",
      os: "Linux",
      os_version: "12",
      asset_type: "server",
      criticality: "high",
      owner: "Platform Engineering",
      environment: "production",
    },
  });

  assert.deepEqual(finding.assetContext, {
    id: "asset-1",
    ipAddress: "192.0.2.10",
    hostname: "edge-01",
    fqdn: "edge-01.example.test",
    os: "Linux",
    osVersion: "12",
    assetType: "server",
    criticality: "high",
    owner: "Platform Engineering",
    environment: "production",
    suggestedRiskOwner: null,
  });
});

test("finding detail keeps structured backend evidence as one reviewable artifact", () => {
  const finding = toUiFinding({
    id: "finding-1",
    evidence: {
      engine: "nuclei",
      template_id: "CVE-2021-44228",
      matched_at: "https://example.test",
      timestamp: "2026-09-06T12:30:00Z",
    },
  });

  assert.equal(finding.evidence.length, 1);
  assert.equal(finding.evidence[0].label, "nuclei evidence");
  assert.equal(finding.evidence[0].type, "json");
  assert.equal(finding.evidence[0].tool, "nuclei");
  assert.equal(JSON.parse(finding.evidence[0].content).template_id, "CVE-2021-44228");
});

test("finding detail preserves provenance on legacy evidence arrays", () => {
  const finding = toUiFinding({
    id: "finding-1",
    evidence: [{
      label: "Probe output",
      content: "443/tcp open",
      tool: "nmap",
      timestamp: "2026-09-06T12:30:00Z",
      source_host: "probe-01",
    }],
  });

  assert.deepEqual(finding.evidence[0], {
    label: "Probe output",
    content: "443/tcp open",
    type: undefined,
    tool: "nmap",
    source: undefined,
    command: undefined,
    timestamp: "2026-09-06T12:30:00Z",
    capturedAt: undefined,
    capturedBy: undefined,
    sourceHost: "probe-01",
    sha256: undefined,
  });
});

test("risk acceptance terms reach the API as risk_acceptance", () => {
  const body = toApiFindingPatch({
    status: "ACCEPTED",
    actionReason: "Business exception",
    riskAcceptance: { riskOwner: "CISO", expiresAt: "2027-01-01T00:00:00.000Z", compensatingControls: "ACL to jump host" },
  });
  assert.deepEqual(body, {
    status: "accepted",
    action_reason: "Business exception",
    risk_acceptance: { risk_owner: "CISO", expires_at: "2027-01-01T00:00:00.000Z", compensating_controls: "ACL to jump host" },
  });
});

test("the suggested risk owner reaches the UI model", () => {
  const finding = toUiFinding({
    id: "finding-2", engagement_id: "e", title: "t", severity: "high", status: "open",
    asset_context: { id: "a", asset_type: "server", criticality: "high", suggested_risk_owner: "Platform SRE" },
  });
  assert.equal(finding.assetContext?.suggestedRiskOwner, "Platform SRE");
});

test("a scanner finding with no SOC validation reads 'not tested', never covered", () => {
  // testing-round gap 13: every scanner finding used to arrive as `detected`, so
  // engagements read 100% detection coverage and no blind spots.
  const base = { id: "f", title: "t", severity: "high", status: "open",
                 created_at: "2026-09-01T00:00:00Z" };
  assert.equal(toUiFinding({ ...base, detection_status: "unknown" }).detectionCoverage, "NOT_TESTED");
  assert.equal(toUiFinding({ ...base }).detectionCoverage, "NOT_TESTED");
  assert.equal(toUiFinding({ ...base, detection_status: "detected" }).detectionCoverage, "COVERED");
  assert.equal(toUiFinding({ ...base, detection_status: "missed" }).detectionCoverage, "BLIND");
});
