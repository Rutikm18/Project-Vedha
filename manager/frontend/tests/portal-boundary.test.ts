import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { pageAuthSurface } from "../lib/page-auth";
import { canReplayPortalRequest } from "../lib/portal-request";
import { adaptPortalConsoleData } from "../lib/console-source";
import { toAgentJobRequest } from "../lib/scan-workspace-api";
import {
  portalFindingAssistantHref,
  portalFindingAssistantPrompt,
} from "../lib/findings-workspace-api";

describe("page authentication surfaces", () => {
  test("keeps both login pages and BFF routes public at the proxy layer", () => {
    assert.equal(pageAuthSurface("/login"), "public");
    assert.equal(pageAuthSurface("/portal/login"), "public");
    assert.equal(pageAuthSurface("/api/portal/findings"), "public");
  });

  test("separates customer pages from operator pages", () => {
    assert.equal(pageAuthSurface("/portal"), "portal");
    assert.equal(pageAuthSurface("/portal/findings/abc"), "portal");
    assert.equal(pageAuthSurface("/findings"), "operator");
    assert.equal(pageAuthSurface("/engagements/abc"), "operator");
  });
});

describe("portal request replay safety", () => {
  test("replays reads after session rotation", () => {
    assert.equal(canReplayPortalRequest("GET"), true);
    assert.equal(canReplayPortalRequest("HEAD"), true);
  });

  test("requires an idempotency key before replaying a mutation", () => {
    assert.equal(canReplayPortalRequest("POST"), false);
    assert.equal(canReplayPortalRequest("PATCH", "finding-action-123"), true);
    assert.equal(canReplayPortalRequest("DELETE", "  "), false);
  });
});

describe("portal finding feature parity", () => {
  test("keeps finding explanation inside the portal authentication surface", () => {
    assert.equal(
      portalFindingAssistantHref("finding/a b"),
      "/portal/assistant?finding=finding%2Fa%20b",
    );
    assert.match(portalFindingAssistantPrompt("finding-123"), /finding-123/);
  });
});

describe("portal dashboard contract parity", () => {
  test("maps backend summary fields to the manager console contract", () => {
    assert.deepEqual(
      adaptPortalConsoleData("findingsSummary", {
        total: 8,
        open_total: 5,
        critical_open: 2,
        high_open: 1,
        medium_open: 1,
        low_open: 1,
        info_open: 0,
        validated: 3,
        blind: 1,
        average_risk: 640,
      }),
      {
        total: 8,
        openTotal: 5,
        criticalOpen: 2,
        highOpen: 1,
        mediumOpen: 1,
        lowOpen: 1,
        infoOpen: 0,
        validated: 3,
        blind: 1,
        averageRisk: 640,
      },
    );
  });

  test("maps paginated backend findings through the shared UI adapter", () => {
    const result = adaptPortalConsoleData("topFindings", {
      items: [{ id: "f-1", title: "RCE", severity: "critical", cvss_score: 9.8 }],
      total: 1,
      page: 1,
      page_size: 5,
      pages: 1,
    }) as { items: Array<{ id: string; severity: string }>; pageSize: number };
    assert.equal(result.items[0].severity, "CRITICAL");
    assert.equal(result.pageSize, 5);
  });
});

describe("scanner command parity", () => {
  test("builds one backend command shape for manager and customer transports", () => {
    assert.deepEqual(
      toAgentJobRequest({
        engagement_id: "e-1",
        use_case_id: "uc_network_va",
        targets: ["10.0.0.0/24"],
        excluded_cidrs: ["10.0.0.10/32"],
        intensity: "stealth",
        preferred_agent_id: "a-1",
      }),
      {
        engagement_id: "e-1",
        job_type: "discovery",
        use_case_id: "uc_network_va",
        params: {
          targets: ["10.0.0.0/24"],
          scope_cidrs: ["10.0.0.0/24"],
          excluded_cidrs: ["10.0.0.10/32"],
          intensity: "stealth",
          rate: 50,
          concurrency: 20,
          timeout: 4,
          disc_timeout: 2,
          preferred_agent_id: "a-1",
        },
      },
    );
  });
});
