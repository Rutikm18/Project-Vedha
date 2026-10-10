import assert from "node:assert/strict";
import test from "node:test";

import { roleSummary, type ReportAsset } from "../lib/report/report-document";
import { riskScoreColor, SEV_PALETTE } from "../lib/severity";

const asset = (over: Partial<ReportAsset>): ReportAsset => ({
  id: "a", ip_address: "10.0.0.1", hostname: null, fqdn: null, os: null, os_version: null,
  asset_type: "server", criticality: "high", owner: null, environment: null, tags: {}, last_seen: null, ...over,
});

test("role summary says nothing when no classifier recorded a role", () => {
  assert.equal(roleSummary(asset({})), null);
});

test("role summary shows the confidence and that an OS-contradicted claim was overruled", () => {
  const text = roleSummary(asset({
    device_role: "network_device", role_confidence: 0.9, resolved_role: "server", role_trusted: false,
  }));
  assert.match(text ?? "", /^server \(classifier said network_device; the OS fingerprint disagrees\), 90% confidence/);
  assert.match(text ?? "", /too uncertain to drive severity or routing/);
});

test("a trusted role is shown plainly, an unrated one says so", () => {
  assert.equal(roleSummary(asset({ device_role: "printer", role_confidence: 0.85, resolved_role: "printer", role_trusted: true })),
    "printer, 85% confidence");
  assert.match(roleSummary(asset({ device_role: "printer", role_confidence: null })) ?? "", /confidence not recorded/);
});

test("risk colours follow the backend severity bands, so a colour never contradicts the severity", () => {
  assert.equal(riskScoreColor(750), SEV_PALETTE.RED);       // critical floor
  assert.equal(riskScoreColor(749), SEV_PALETTE.ORANGE);    // high ceiling
  assert.equal(riskScoreColor(500), SEV_PALETTE.ORANGE);    // high floor
  assert.equal(riskScoreColor(499), SEV_PALETTE.AMBER);     // medium ceiling
  assert.equal(riskScoreColor(250), SEV_PALETTE.AMBER);     // medium floor
  assert.equal(riskScoreColor(249), SEV_PALETTE.STONE);     // low
});
