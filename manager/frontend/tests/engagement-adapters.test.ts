import assert from "node:assert/strict";
import { describe, test } from "node:test";

import {
  toApiEngagementCreate,
  toApiEngagementPatch,
  toApiFindingPatch,
  toUiFinding,
} from "../lib/adapters";

describe("engagement request adapters", () => {
  test("create preserves an empty scope so the backend rejects it truthfully", () => {
    const body = toApiEngagementCreate({ name: "test", scopeCidrs: "  " });
    assert.deepEqual(body.scope_cidrs, []);
  });

  test("create and patch normalize comma/newline-separated scope", () => {
    const create = toApiEngagementCreate({
      name: "test",
      scopeCidrs: "10.0.0.0/24,\n192.168.1.5",
      excludedCidrs: "10.0.0.5\n10.0.0.6",
    });
    assert.deepEqual(create.scope_cidrs, ["10.0.0.0/24", "192.168.1.5"]);
    assert.deepEqual(create.excluded_cidrs, ["10.0.0.5", "10.0.0.6"]);

    const patch = toApiEngagementPatch({ scopeCidrs: "10.0.0.0/24\n10.1.0.0/24" });
    assert.deepEqual(patch.scope_cidrs, ["10.0.0.0/24", "10.1.0.0/24"]);
  });
});

describe("finding status adapters", () => {
  test("maps every backend status to the supported UI workflow", () => {
    const expected = {
      open: "OPEN",
      confirmed: "CONFIRMED",
      remediated: "REMEDIATED",
      accepted: "ACCEPTED",
      fp: "FALSE_POSITIVE",
    };

    for (const [apiStatus, uiStatus] of Object.entries(expected)) {
      assert.equal(toUiFinding({ id: "f-1", status: apiStatus }).status, uiStatus);
    }
  });

  test("keeps risk scoring on the backend's 0-1000 scale", () => {
    assert.equal(toUiFinding({ id: "f-1", risk_score: 825 }).riskScore, 825);
    assert.equal(toUiFinding({ id: "f-2", cvss_score: 7.5 }).riskScore, 750);
  });

  test("maps every UI workflow status back to the backend enum", () => {
    const expected = {
      OPEN: "open",
      CONFIRMED: "confirmed",
      REMEDIATED: "remediated",
      ACCEPTED: "accepted",
      FALSE_POSITIVE: "fp",
    };

    for (const [uiStatus, apiStatus] of Object.entries(expected)) {
      assert.deepEqual(toApiFindingPatch({ status: uiStatus }), { status: apiStatus });
    }
  });
});
