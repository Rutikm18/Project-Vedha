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
  });
});
