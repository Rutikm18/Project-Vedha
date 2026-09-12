import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { buildScanLaunchRequest } from "../lib/scan-launch";

test("manager and portal use the exact shared scanner workspace", () => {
  const portal = readFileSync(join(process.cwd(), "app/portal/scans/page.tsx"), "utf8");
  assert.match(portal, /ScannerWorkspace/);
  assert.match(portal, /surface="portal"/);
  assert.doesNotMatch(portal, /scan-requests|Request scan/);
});

test("both scanner transports share one canonical launch builder", () => {
  assert.deepEqual(buildScanLaunchRequest({
    engagement_id: "eng-1",
    use_case_id: "uc_network_va",
    intensity: "normal",
    targets: ["10.0.0.1"],
    preferred_agent_id: "agent-1",
  }), {
    engagement_id: "eng-1",
    job_type: "discovery",
    use_case_id: "uc_network_va",
    params: {
      targets: ["10.0.0.1"],
      scope_cidrs: ["10.0.0.1"],
      intensity: "normal",
      rate: 200,
      concurrency: 100,
      timeout: 3,
      disc_timeout: 1.5,
      preferred_agent_id: "agent-1",
    },
  });
});
