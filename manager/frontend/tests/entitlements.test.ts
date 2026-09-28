/* The plan strip, the Customers page and the scan launcher all render the
 * customer's plan through lib/entitlements — and the portal's intensity list
 * must match the backend policy that actually refuses aggressive scans. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import {
  type Entitlement, daysText, friendlyError, isRunningLow, isoFromDateInput, dateInputValue,
  scansText, usageRatio,
} from "../lib/entitlements";
import { INTENSITY, PORTAL_INTENSITIES } from "../lib/scan-intensity";

const base: Entitlement = {
  state: "active", can_scan: true, reason: null, plan_type: "poc",
  starts_at: "2026-09-20T00:00:00Z", expires_at: "2026-10-04T00:00:00Z", days_left: 9,
  scan_quota: 10, scans_used: 3, scans_left: 7, license_key: null,
};

test("scans and days read as sentences", () => {
  assert.equal(scansText(base), "7 of 10 scans left");
  assert.equal(scansText({ ...base, scan_quota: null, scans_left: null, scans_used: 4 }), "Unlimited scans · 4 used");
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

test("portal intensities are stealth + normal, matching the backend policy", () => {
  assert.deepEqual([...PORTAL_INTENSITIES], ["stealth", "normal"]);
  for (const id of PORTAL_INTENSITIES) assert.ok(INTENSITY.some((i) => i.id === id));
  const policy = readFileSync(
    join(process.cwd(), "../backend/app/services/portal_scan_policy.py"), "utf8");
  assert.match(policy, /PORTAL_ALLOWED_INTENSITIES = frozenset\(\{"light", "standard"\}\)/);
});

test("the scanner dial is restricted on the portal", () => {
  const page = readFileSync(join(process.cwd(), "app/scan/page.tsx"), "utf8");
  assert.match(page, /allowed=\{isPortal \? PORTAL_INTENSITIES : undefined\}/);
});
