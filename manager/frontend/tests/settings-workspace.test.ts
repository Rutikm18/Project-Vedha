import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer Settings renders the manager Settings workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/settings/page.tsx"), "utf8");
  assert.match(portal, /SettingsWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /usePortalEngagement|SLA_POLICY|AppearanceSection/);
});

test("portal Settings exposes only engagement-scoped shared sections", () => {
  const source = readFileSync(join(process.cwd(), "app/settings/workspace.tsx"), "utf8");
  assert.match(source, /\["workspace", "probe-fleet", "ai", "audit-log"\]/);
});
