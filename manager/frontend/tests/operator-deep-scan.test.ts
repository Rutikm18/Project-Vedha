/* The single-asset Deep scan on the operator Scanner: same card and same
 * one-IP rules as the portal, launched through the operator enqueue, and never
 * described as spending the customer's plan (operators are unlimited). */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { buildDeepScanLaunch, buildScanLaunchRequest } from "../lib/scan-launch";
import { deepScanCopy, deepTargetProblem } from "../components/portal/DeepScanCard";
import type { Entitlement, ModeAllowance } from "../lib/entitlements";

const mode = (quota: number | null, used = 0): ModeAllowance => ({
  enabled: quota == null || quota > 0, quota, used,
  left: quota == null ? null : Math.max(quota - used, 0),
  can_scan: quota == null || quota - used > 0, reason: null,
});

const plan: Entitlement = {
  state: "active", can_scan: true, reason: null, plan_type: "poc",
  starts_at: "2026-09-20T00:00:00Z", expires_at: "2026-10-04T00:00:00Z", days_left: 9,
  scan_quota: 10, scans_used: 3, scans_left: 7, license_key: null,
  modes: { stealth: mode(null), normal: mode(10, 3), aggressive: mode(0), deep: mode(2) },
  deep_repeat_policy: "distinct", deep_scanned_targets: ["10.0.0.9/32"],
};

test("operator deep launch: one asset, the deep use case, no portal-only fields", () => {
  const body = buildDeepScanLaunch({ engagementId: "eng-1", ip: "10.0.0.5", probeId: "probe-7", audience: "operator" });
  assert.deepEqual(body, {
    engagement_id: "eng-1", use_case_id: "uc_deep_port_sweep", targets: ["10.0.0.5"],
    intensity: "aggressive", preferred_agent_id: "probe-7",
  });
  // On the wire: exactly the one host as targets AND scope, deep intensity.
  const wire = buildScanLaunchRequest(body);
  assert.deepEqual(wire.params.targets, ["10.0.0.5"]);
  assert.deepEqual(wire.params.scope_cidrs, ["10.0.0.5"]);
  assert.equal(wire.params.intensity, "aggressive");
  assert.equal("scan_mode" in wire.params, false);
});

test("portal deep launch still names the deep mode for the plan check", () => {
  const body = buildDeepScanLaunch({ engagementId: "eng-1", ip: "10.0.0.5", audience: "portal" });
  assert.deepEqual(body.params, { scan_mode: "deep" });
  assert.equal(body.preferred_agent_id, undefined);
});

test("card copy: the customer sees their allowance, the operator sees it is not charged", () => {
  const portal = deepScanCopy(plan);
  assert.equal(portal.badge, "2 left");
  assert.match(portal.footer, /Uses 1 deep scan from your plan/);
  assert.ok(portal.rules.some((r) => /different asset/.test(r)));
  assert.ok(portal.rules.some((r) => /your authorized scope/.test(r)));

  const operator = deepScanCopy(null);
  assert.equal(operator.badge, "Operator · not counted");
  assert.match(operator.footer, /doesn't use the customer's Deep allowance/);
  assert.ok(operator.rules.some((r) => /this engagement's scope/.test(r)));
  assert.equal(operator.rules.some((r) => /different asset|same asset again/.test(r)), false);
});

test("scope wording follows the audience", () => {
  const scope = ["10.0.0.0/24"];
  assert.match(deepTargetProblem("192.0.2.9", scope, [], false) ?? "", /outside your authorized scope/);
  assert.match(deepTargetProblem("192.0.2.9", scope, [], false, "this engagement's scope") ?? "",
    /outside this engagement's scope/);
  // Operators are not bound by the customer's repeat policy.
  assert.equal(deepTargetProblem("10.0.0.9", scope, [], false, "this engagement's scope"), null);
});

test("deep selection belongs to the chosen engagement and uses the shared builder", () => {
  const page = readFileSync(join(process.cwd(), "app/scan/workspace.tsx"), "utf8");
  assert.match(page, /<DeepScanCard key=\{selectedEng\}/);
  assert.match(page, /buildDeepScanLaunch\(/);
  assert.match(page, /assets=\{selectedAssets\?\.rows \?\? \[\]\}/);
  assert.match(page, /excluded=\{selectedEngagement\?\.excludedCidrs/);
  assert.equal((page.match(/<DeepScanCard/g) ?? []).length, 1);
});

test("a full-port scan can never be built for more than one host", () => {
  for (const use_case_id of ["uc_deep_port_sweep", "uc_full_port_audit"]) {
    const base = { engagement_id: "eng-1", use_case_id };
    for (const targets of [undefined, [], ["10.0.0.5", "10.0.0.6"], ["10.0.0.0/24"], ["10.0.0.4-10.0.0.9"], ["10.0.0.5,10.0.0.6"]]) {
      assert.throws(() => buildScanLaunchRequest({ ...base, targets }), /exactly one host/, JSON.stringify(targets));
    }
    assert.doesNotThrow(() => buildScanLaunchRequest({ ...base, targets: ["10.0.0.5"] }));
    assert.doesNotThrow(() => buildScanLaunchRequest({ ...base, targets: ["10.0.0.5/32"] }));
  }
  // other scans are unaffected: a range is still fine for Network VA
  assert.doesNotThrow(() => buildScanLaunchRequest({
    engagement_id: "eng-1", use_case_id: "uc_network_va", targets: ["10.0.0.0/24"] }));
  assert.throws(() => buildDeepScanLaunch({
    engagementId: "eng-1", ip: "10.0.0.5, 10.0.0.6", audience: "operator" }), /exactly one host/);
});

test("the card says one host, shows what it covers, and offers no way to add a second", () => {
  const card = readFileSync(join(process.cwd(), "components/portal/DeepScanCard.tsx"), "utf8");
  assert.match(card, /Deep scan · one host/);
  assert.match(card, /Deep-scan this host/);
  assert.match(card, /65,535/);
  assert.doesNotMatch(card, /<textarea/);              // a single-line field only
  assert.match(deepScanCopy(null).rules[0], /Exactly one host per deep scan/);
  assert.match(deepScanCopy(plan).rules[0], /Exactly one host per deep scan/);
  for (const bad of ["10.0.0.5, 10.0.0.6", "10.0.0.5 10.0.0.6", "10.0.0.0/24", "10.0.0.5;10.0.0.6"]) {
    assert.ok(deepTargetProblem(bad, ["10.0.0.0/24"], [], false), bad);
  }
});
