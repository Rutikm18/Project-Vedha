import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer Fleet renders the manager Fleet workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/fleet/page.tsx"), "utf8");
  assert.match(portal, /FleetWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /portalApi|useQuery|Connected vedha-agents/);
});

test("customer Fleet approval is engagement-bound and code-gated", () => {
  const adapter = readFileSync(join(process.cwd(), "lib/fleet-workspace-api.ts"), "utf8");
  const workspace = readFileSync(join(process.cwd(), "app/fleet/page.tsx"), "utf8");
  assert.match(adapter, /workspace\/fleet\/enrollment\/approve/);
  assert.match(adapter, /user_code/);
  assert.match(workspace, /verification code shown by the vedha-agent installer/);
  assert.match(workspace, /Approve and assign agent/);
});
