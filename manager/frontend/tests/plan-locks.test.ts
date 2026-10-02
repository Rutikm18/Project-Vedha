/* Portal plan locks in the UI: the operator sets locked severities and features
 * in the customer's Plan panel; the portal shows locked findings as teaser rows
 * and locked features as a lock panel. The server enforces both — these tests
 * pin the configuration round trip and that every surface honours the locks. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { configFromDraft, defaultDraft, draftFrom } from "../components/customers/PlanPanel";
import {
  type EntitlementAdmin, LOCK_FEATURES, LOCKABLE_SEVERITIES, isFeatureLocked, teaserRows,
} from "../lib/entitlements";

const read = (path: string) => readFileSync(join(process.cwd(), path), "utf8");

test("a new POC draft locks Critical and High and no features", () => {
  const d = defaultDraft();
  assert.deepEqual(d.lockedSeverities, ["critical", "high"]);
  assert.deepEqual(d.lockedFeatures, []);
  const cfg = configFromDraft(d);
  assert.deepEqual(cfg.locked_severities, ["critical", "high"]);
  assert.deepEqual(cfg.locked_features, []);
});

test("an existing customer's locks load into the draft and save back unchanged", () => {
  const e = {
    configured: true, plan_type: "licensed", starts_at: "2026-10-01T00:00:00Z", expires_at: null,
    scan_quota: null, deep_repeat_policy: "distinct", notes: null,
    modes: { stealth: { quota: null }, normal: { quota: null }, aggressive: { quota: 0 }, deep: { quota: 0 } },
    locked_severities: [], locked_features: ["reports", "ai_assistant"],
  } as unknown as EntitlementAdmin;
  const d = draftFrom(e);
  assert.deepEqual(d.lockedSeverities, []);                    // never re-locks an existing customer
  assert.deepEqual(d.lockedFeatures, ["reports", "ai_assistant"]);
  assert.deepEqual(configFromDraft(d).locked_features, ["ai_assistant", "reports"]);  // stable order
});

test("lock vocabularies match the backend", () => {
  assert.deepEqual(LOCKABLE_SEVERITIES, ["critical", "high", "medium", "low", "info"]);
  assert.deepEqual(LOCK_FEATURES.map((f) => f.id), ["ai_assistant", "reports", "remediation", "compliance"]);
  for (const f of LOCK_FEATURES) assert.match(f.lockedMessage, /licensed plan/);
});

test("feature lock check tolerates a missing or older plan payload", () => {
  assert.equal(isFeatureLocked(null, "reports"), false);
  assert.equal(isFeatureLocked({ locked_features: ["reports"] }, "reports"), true);
  assert.equal(isFeatureLocked({}, "reports"), false);
});

test("teaser rows: one per locked severity with findings, in severity order", () => {
  assert.deepEqual(teaserRows({ locked_severities: ["critical", "high"], counts: { high: 1, critical: 3 }, total: 4 }),
    [{ severity: "critical", count: 3 }, { severity: "high", count: 1 }]);
  assert.deepEqual(teaserRows({ locked_severities: ["critical"], counts: {}, total: 0 }), []);
  assert.deepEqual(teaserRows(null), []);
});

test("every portal surface honours the locks", () => {
  assert.match(read("app/findings/page.tsx"), /<LockedFindingsTeaser/);
  assert.match(read("app/aibrain/page.tsx"), /isFeatureLocked\([^)]*"ai_assistant"\)/);
  const reports = read("app/portal/reports/workspace.tsx");
  assert.match(reports, /isFeatureLocked\([^)]*"reports"\)/);
  assert.match(reports, /written_reports_withheld/);       // free-text reports withheld while severities are locked
  assert.match(reports, /<LockedFindingsTeaser/);
  assert.match(read("components/remediation/RemediationWorkspace.tsx"), /isFeatureLocked\([^)]*"remediation"\)/);
  assert.match(read("components/customers/PlanPanel.tsx"), /LOCK_FEATURES\.map/);
});
