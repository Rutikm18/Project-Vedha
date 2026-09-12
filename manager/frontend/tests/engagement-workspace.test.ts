import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer Scope renders the exact manager engagement workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/scope/page.tsx"), "utf8");
  assert.match(portal, /EngagementWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /portalApi|useQuery|read-only/i);
});

test("portal engagement transport never accepts browser engagement identity", () => {
  const adapter = readFileSync(join(process.cwd(), "lib/engagement-workspace-api.ts"), "utf8");
  const portal = adapter.slice(adapter.indexOf("return {", adapter.indexOf("if (surface")) + 1);
  assert.match(portal, /_engagementId/);
  assert.match(portal, /\/workspace\/engagement/);
  assert.doesNotMatch(portal, /workspace\/engagements?\?engagement_id/);
});
