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

test("structured closure packets cross the BFF contract unchanged", () => {
  const closure = {
    reason: "Authorized retest confirms the fix",
    reviewed_by: "reviewer@example.test",
    retest: { passed: true },
  };

  assert.deepEqual(
    toApiFindingPatch({ status: "REMEDIATED", closure }),
    { status: "remediated", closure },
  );
});

test("action tracking crosses the BFF contract with API field naming", () => {
  const actionTracking = {
    non_closure_reason: "Waiting for the approved maintenance window",
    planned_closure_at: "2026-10-05T22:00:00+05:30",
    action_reference: "CHG-2026-1005",
  };

  assert.deepEqual(
    toApiFindingPatch({ actionTracking }),
    { action_tracking: actionTracking },
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
  });
  assert.equal(finding.affectedHost, "edge-01.example.test");
});

test("finding signals preserve distinct recorded meanings", () => {
  const finding = toUiFinding({
    id: "finding-signals",
    severity: "critical",
    status: "open",
    exploit_validated: true,
    exploitable: true,
    evidence: { kev: true },
  });

  assert.equal(finding.exploitValidated, true);
  assert.equal(finding.kevListed, true);
  assert.equal(finding.kevStatusRecorded, true);
  assert.equal(finding.exploitedInWild, false);
  assert.equal(finding.activelyExploited, false);
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

test("finding lifecycle uses authoritative observation fields before row update time", () => {
  const finding = toUiFinding({
    id: "finding-1",
    first_seen: "2026-08-01T01:00:00Z",
    last_seen: "2026-09-01T02:00:00Z",
    updated_at: "2026-09-20T03:00:00Z",
    initial_detection_run_id: "run-initial",
    detection_run_id: "run-detect",
    resolution_run_id: "run-resolve",
    verification_method: "active",
    detected_db_version: "db-sha256",
  });

  assert.equal(finding.firstSeen, "2026-08-01T01:00:00Z");
  assert.equal(finding.discoveredAt, "2026-08-01T01:00:00Z");
  assert.equal(finding.lastSeen, "2026-09-01T02:00:00Z");
  assert.equal(finding.initialDetectionRunId, "run-initial");
  assert.equal(finding.detectionRunId, "run-detect");
  assert.equal(finding.resolutionRunId, "run-resolve");
  assert.equal(finding.verificationMethod, "active");
  assert.equal(finding.detectedDbVersion, "db-sha256");
});
