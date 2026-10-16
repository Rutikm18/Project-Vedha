import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { GET as findingIds } from "../app/api/findings/ids/route";

const originalFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = originalFetch; });

function req(qs: string, cookie = "vedha_token=operator-token"): NextRequest {
  return new NextRequest(`http://localhost/api/findings/ids?${qs}`, {
    headers: cookie ? { cookie } : {},
  });
}

describe("findings export-ids BFF", () => {
  test("forwards engagement + filters to the backend /findings/ids with the operator token", async () => {
    let url = "";
    let auth = "";
    globalThis.fetch = async (input, init) => {
      url = String(input);
      auth = new Headers(init?.headers).get("authorization") ?? "";
      return new Response(JSON.stringify({ finding_ids: ["id-a", "id-b"] }), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const res = await findingIds(req("engagement_id=eng-1&severity=critical&status=open"));

    assert.equal(res.status, 200);
    const u = new URL(url);
    assert.equal(u.pathname, "/findings/ids");
    assert.equal(u.searchParams.get("engagement_id"), "eng-1");
    assert.equal(u.searchParams.get("severity"), "critical");
    assert.equal(auth, "Bearer operator-token");
    assert.deepEqual(await res.json(), { finding_ids: ["id-a", "id-b"] });
  });

  test("passes through a null result (no filter → whole engagement)", async () => {
    globalThis.fetch = async () => new Response(JSON.stringify({ finding_ids: null }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
    const res = await findingIds(req("engagement_id=eng-1"));
    assert.deepEqual(await res.json(), { finding_ids: null });
  });

  test("an unauthenticated request never reaches the backend", async () => {
    let calls = 0;
    globalThis.fetch = async () => { calls += 1; return new Response(); };
    const res = await findingIds(req("engagement_id=eng-1", ""));
    assert.equal(res.status, 401);
    assert.equal(calls, 0);
  });
});
