/* The plan strip, the Customers page and the scan launcher all render the
 * customer's plan through lib/entitlements — and the portal's intensity list
 * must match the backend policy that actually refuses aggressive scans. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import {
  type Entitlement, type ModeAllowance, daysText, friendlyError, isRunningLow, isoFromDateInput,
  dateInputValue, launchableModes, modeShort, scansText, usageRatio,
} from "../lib/entitlements";
import { configFromDraft, defaultDraft, draftError, draftFrom } from "../components/customers/PlanPanel";

const mode = (quota: number | null, used = 0, can = true): ModeAllowance => ({
  enabled: quota == null || quota > 0, quota, used,
  left: quota == null ? null : Math.max(quota - used, 0),
  can_scan: can && (quota == null || quota - used > 0), reason: null,
});
import { INTENSITY } from "../lib/scan-intensity";
import { deepTargetProblem } from "../components/portal/DeepScanCard";

const base: Entitlement = {
  state: "active", can_scan: true, reason: null, plan_type: "poc",
  starts_at: "2026-09-20T00:00:00Z", expires_at: "2026-10-04T00:00:00Z", days_left: 9,
  scan_quota: 10, scans_used: 3, scans_left: 7, license_key: null,
  modes: { stealth: mode(null), normal: mode(10, 3), aggressive: mode(0), deep: mode(2) },
  deep_repeat_policy: "distinct", deep_scanned_targets: [],
};

test("scans and days read as sentences", () => {
  assert.equal(scansText(base), "7 of 10 scans left");
  assert.equal(scansText({ ...base, scan_quota: null, scans_left: null, scans_used: 4 }), "4 scans used");
  assert.equal(scansText({ ...base, scan_quota: 1, scans_left: 1, scans_used: 0 }), "1 of 1 scan left");
  assert.equal(daysText(base), "Ends in 9 days");
  assert.equal(daysText({ ...base, days_left: 1 }), "Ends within a day");
  assert.equal(daysText({ ...base, expires_at: null, days_left: null }), "No end date");
  assert.match(daysText({ ...base, state: "expired", days_left: 0 }), /^Ended /);
});

test("usage ratio is null when unlimited and capped at 1", () => {
  assert.equal(usageRatio({ scan_quota: null, scans_used: 9 }), null);
  assert.equal(usageRatio({ scan_quota: 4, scans_used: 1 }), 0.25);
  assert.equal(usageRatio({ scan_quota: 2, scans_used: 5 }), 1);
  assert.equal(usageRatio({ scan_quota: 0, scans_used: 0 }), 1);
});

test("running low warns only on an active plan", () => {
  assert.equal(isRunningLow(base), false);
  assert.equal(isRunningLow({ ...base, days_left: 3 }), true);
  assert.equal(isRunningLow({ ...base, scans_left: 1 }), true);
  // Every open type down to its last scan → low, even with no overall cap.
  assert.equal(isRunningLow({ ...base, scan_quota: null, scans_left: null,
    modes: { stealth: mode(0), normal: mode(4, 3), aggressive: mode(0), deep: mode(1) } }), true);
  assert.equal(isRunningLow({ ...base, state: "expired", can_scan: false, days_left: 0 }), false);
});

test("date inputs round-trip through ISO", () => {
  const iso = isoFromDateInput("2026-10-04");
  assert.ok(iso);
  assert.equal(dateInputValue(iso), "2026-10-04");
  assert.equal(isoFromDateInput(""), null);
});

test("FastAPI 422 arrays become one readable sentence", () => {
  const e = new Error(JSON.stringify([{ msg: "Value error, a POC needs a duration" }]));
  assert.equal(friendlyError(e, "x"), "a POC needs a duration");
  assert.equal(friendlyError(new Error("plain"), "x"), "plain");
});

test("UI scan types map to the backend's scan types and probe presets", () => {
  const policy = readFileSync(
    join(process.cwd(), "../backend/app/services/portal_scan_policy.py"), "utf8");
  assert.match(policy, /MODE_FOR_INTENSITY = \{"light": "stealth", "standard": "normal", "deep": "aggressive"\}/);
  for (const id of ["stealth", "normal", "aggressive"] as const) assert.ok(INTENSITY.some((i) => i.id === id));
});

test("the scanner dial is restricted on the portal", () => {
  const page = readFileSync(join(process.cwd(), "app/scan/workspace.tsx"), "utf8");
  assert.match(page, /allowed=\{isPortal \? portalDial : undefined\}/);
  assert.match(page, /DeepScanCard/);
});

test("per-type status and what the customer can launch", () => {
  assert.equal(modeShort(base.modes.stealth), "∞");
  assert.equal(modeShort(base.modes.normal), "7 left");
  assert.equal(modeShort(base.modes.aggressive), "off");
  assert.deepEqual(launchableModes(base), ["stealth", "normal", "deep"]);
  assert.deepEqual(launchableModes(null), []);
});

test("plan draft round-trips per-type allowances and the deep policy", () => {
  const draft = defaultDraft();
  draft.modes.aggressive = { allowance: "limited", quota: 3 };
  draft.modes.deep = { allowance: "limited", quota: 2 };
  draft.deepPolicy = "repeat";
  const cfg = configFromDraft(draft);
  assert.equal(cfg.stealth_quota, null);          // unlimited
  assert.equal(cfg.normal_quota, 10);
  assert.equal(cfg.aggressive_quota, 3);
  assert.equal(cfg.deep_quota, 2);
  assert.equal(cfg.deep_repeat_policy, "repeat");
  const off = defaultDraft();
  assert.equal(configFromDraft(off).deep_quota, 0);   // off = not included
  const back = draftFrom({ ...base, configured: true, notes: null, updated_at: null,
    modes: { stealth: mode(null), normal: mode(10), aggressive: mode(0), deep: mode(2) } });
  assert.equal(back.modes.stealth.allowance, "unlimited");
  assert.equal(back.modes.aggressive.allowance, "off");
  assert.equal(back.modes.deep.allowance, "limited");
  assert.equal(back.modes.deep.quota, 2);
});

test("a plan needs at least one scan type and sane limits", () => {
  const none = defaultDraft();
  for (const m of ["stealth", "normal", "aggressive", "deep"] as const) none.modes[m].allowance = "off";
  assert.match(draftError(none) ?? "", /at least one scan type/);
  const bad = defaultDraft();
  bad.modes.deep = { allowance: "limited", quota: 0 };
  assert.match(draftError(bad) ?? "", /^Deep:/);
  assert.equal(draftError(defaultDraft()), null);
});

test("deep scan pre-check: one in-scope asset, respecting the repeat policy", () => {
  const scope = ["10.0.0.0/24"];
  assert.equal(deepTargetProblem("10.0.0.5", scope, [], true), null);
  assert.equal(deepTargetProblem("10.0.0.5/32", scope, [], true), null);
  assert.match(deepTargetProblem("", scope, [], true) ?? "", /Enter the one IP/);
  assert.match(deepTargetProblem("10.0.0.5, 10.0.0.6", scope, [], true) ?? "", /exactly one asset/);
  assert.match(deepTargetProblem("10.0.0.0/28", scope, [], true) ?? "", /range/);
  assert.match(deepTargetProblem("10.0.0.300", scope, [], true) ?? "", /isn't an IP/);
  assert.match(deepTargetProblem("192.0.2.9", scope, [], true) ?? "", /outside your authorized scope/);
  assert.match(deepTargetProblem("10.0.0.5", scope, ["10.0.0.5/32"], true) ?? "", /already had a deep scan/);
  assert.equal(deepTargetProblem("10.0.0.5", scope, ["10.0.0.5/32"], false), null);   // repeats allowed
});

test("a plan with every scan type open and uncapped reads as one phrase", async () => {
  const { modeSummary, SCAN_MODES } = await import("../lib/entitlements");
  const open = { enabled: true, quota: null, used: 0, left: null, can_scan: true, reason: null };
  const modes = Object.fromEntries(SCAN_MODES.map((m) => [m, open])) as never;
  assert.deepEqual(modeSummary({ modes }), {
    kind: "unlimited", label: "All scan types, unlimited", names: "Stealth, Normal, Aggressive, Deep",
  });
  const three = { ...(modes as object), deep: { ...open, enabled: false } } as never;
  assert.equal((modeSummary({ modes: three }) as { label: string }).label, "3 scan types, unlimited");
});

test("a capped, used-up or switched-off scan type keeps the per-type chips", async () => {
  const { modeSummary, SCAN_MODES } = await import("../lib/entitlements");
  const open = { enabled: true, quota: null, used: 0, left: null, can_scan: true, reason: null };
  const modes = Object.fromEntries(SCAN_MODES.map((m) => [m, open])) as Record<string, typeof open>;
  const capped = { ...modes, normal: { ...open, quota: 5, used: 2, left: 3 } };
  assert.deepEqual(modeSummary({ modes: capped as never }), { kind: "chips", modes: ["stealth", "normal", "aggressive", "deep"] });
  const spent = { ...modes, deep: { ...open, quota: 1, used: 1, left: 0, can_scan: false, reason: "Deep scans used" } };
  assert.equal(modeSummary({ modes: spent as never }).kind, "chips");
  assert.deepEqual(modeSummary(null), { kind: "chips", modes: [] });
});
