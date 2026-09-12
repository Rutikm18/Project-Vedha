import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer VA Campaigns renders the manager campaign workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/campaign/page.tsx"), "utf8");
  assert.match(portal, /CampaignWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /useEffect|FleetJobs|CampaignProgress/);
});
