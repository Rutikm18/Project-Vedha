import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer Reports renders the manager Reports workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/reports/page.tsx"), "utf8");
  assert.match(portal, /ReportsWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /portalApi|useQuery|Executive Summary/);
});

test("portal report transport never sends a browser-selected engagement id", () => {
  const adapter = readFileSync(join(process.cwd(), "lib/reports-workspace-api.ts"), "utf8");
  assert.match(adapter, /_engagementId/);
  assert.match(adapter, /\/workspace\/findings\?paginated=true/);
  assert.doesNotMatch(adapter, /workspace\/findings[^\n]*engagement_id/);
});
