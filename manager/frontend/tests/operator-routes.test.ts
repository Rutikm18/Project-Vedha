import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";
import { GET as postureGet } from "../app/api/analytics/posture/route";
import { canMountAssistant, isAssistantRoute } from "../lib/assistant-access";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe("posture analytics BFF", () => {
  test("forwards the engagement scope and preserves the dashboard contract", async () => {
    let requestedUrl = "";
    let authorization = "";
    globalThis.fetch = async (input, init) => {
      requestedUrl = String(input);
      authorization = new Headers(init?.headers).get("authorization") ?? "";
      return new Response(JSON.stringify({
        has_runs: true,
        scores: { patch: 83 },
        scores_prev: { patch: 70 },
        matrix: [{ family: "linux", current: 83, previous: 70 }],
      }), { status: 200, headers: { "content-type": "application/json" } });
    };

    const response = await postureGet(new NextRequest(
      "http://localhost/api/analytics/posture?engagement_id=eng-42",
      { headers: { authorization: "Bearer operator-token" } },
    ));

    assert.equal(response.status, 200);
    assert.match(requestedUrl, /\/analytics\/posture\?engagement_id=eng-42$/);
    assert.equal(authorization, "Bearer operator-token");
    assert.deepEqual(await response.json(), {
      has_runs: true,
      scores: { patch: 83 },
      scores_prev: { patch: 70 },
      matrix: [{ family: "linux", current: 83, previous: 70 }],
    });
  });
});

describe("assistant route access", () => {
  test("is hidden on public authentication and portal routes", () => {
    assert.equal(isAssistantRoute("/login"), false);
    assert.equal(isAssistantRoute("/portal/login"), false);
    assert.equal(isAssistantRoute("/portal/findings"), false);
  });

  test("is available inside authenticated operator routes", () => {
    assert.equal(isAssistantRoute("/"), true);
    assert.equal(isAssistantRoute("/findings"), true);
    assert.equal(isAssistantRoute("/engagements/eng-42"), true);
  });

  test("requires a verified authenticated session before mounting", () => {
    assert.equal(canMountAssistant("/findings", "checking"), false);
    assert.equal(canMountAssistant("/findings", "anonymous"), false);
    assert.equal(canMountAssistant("/login", "authenticated"), false);
    assert.equal(canMountAssistant("/findings", "authenticated"), true);
  });
});
