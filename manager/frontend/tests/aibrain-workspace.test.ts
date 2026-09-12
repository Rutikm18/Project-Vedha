import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer Assistant renders the exact manager AI Brain workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/assistant/page.tsx"), "utf8");
  assert.match(portal, /AIBrainWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /portalApi|useQuery|STARTERS/);
});

test("portal AI transport does not forward browser engagement scope", () => {
  const adapter = readFileSync(join(process.cwd(), "lib/aibrain-workspace-api.ts"), "utf8");
  const portalSend = adapter.slice(adapter.indexOf("Engagement scope is intentionally"));
  assert.match(portalSend, /messages: body\.messages/);
  assert.doesNotMatch(portalSend, /engagementId: body\.engagementId/);
});
