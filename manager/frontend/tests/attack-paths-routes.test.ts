import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";
import { GET as listGet } from "../app/api/engagements/[id]/attack-paths/route";
import { GET as detailGet } from "../app/api/engagements/[id]/attack-paths/[pathId]/route";
import { GET as chokeGet } from "../app/api/engagements/[id]/chokepoints/route";
import { GET as analysisGet } from "../app/api/engagements/[id]/attack-path-analysis/route";
import { GET as graphGet } from "../app/api/engagements/[id]/attack-graph/route";
import { GET as blastGet } from "../app/api/engagements/[id]/blast-radius/[assetId]/route";

const ENG = "11111111-1111-4111-8111-111111111111";
const PATH = "22222222-2222-4222-8222-222222222222";
const ASSET = "33333333-3333-4333-8333-333333333333";

const originalFetch = globalThis.fetch;
let calls: { url: string; authorization: string }[] = [];

function stubBackend(body: unknown = { ok: true }, status = 200) {
  calls = [];
  globalThis.fetch = async (input, init) => {
    calls.push({ url: String(input), authorization: new Headers(init?.headers).get("authorization") ?? "" });
    return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });
  };
}

afterEach(() => {
  globalThis.fetch = originalFetch;
  calls = [];
});

const req = (url: string, token: string | null = "operator-token") =>
  new NextRequest(url, token ? { headers: { authorization: `Bearer ${token}` } } : {});
const ctx = (params: Record<string, string>) => ({ params: Promise.resolve(params) });

describe("attack-path BFF forwards to the real backend", () => {
  test("list: same path, operator token, allowed query only", async () => {
    stubBackend({ total: 0, items: [] });
    const res = await listGet(
      req(`http://localhost/api/engagements/${ENG}/attack-paths?refresh=true&page_size=50&page=2&evil=1`),
      ctx({ id: ENG }),
    );
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { total: 0, items: [] });
    assert.equal(calls.length, 1);
    const url = new URL(calls[0].url);
    assert.equal(url.pathname, `/engagements/${ENG}/attack-paths`);
    assert.equal(url.searchParams.get("refresh"), "true");
    assert.equal(url.searchParams.get("page_size"), "50");
    assert.equal(url.searchParams.get("page"), "2");
    assert.equal(url.searchParams.get("evil"), null, "unlisted query keys never reach FastAPI");
    assert.equal(calls[0].authorization, "Bearer operator-token");
  });

  test("each route maps to its backend endpoint", async () => {
    const cases: [string, () => Promise<Response>, string][] = [
      ["detail", () => detailGet(req("http://localhost/x"), ctx({ id: ENG, pathId: PATH })), `/engagements/${ENG}/attack-paths/${PATH}`],
      ["chokepoints", () => chokeGet(req("http://localhost/x"), ctx({ id: ENG })), `/engagements/${ENG}/chokepoints`],
      ["analysis", () => analysisGet(req("http://localhost/x"), ctx({ id: ENG })), `/engagements/${ENG}/attack-path-analysis`],
      ["graph", () => graphGet(req("http://localhost/x"), ctx({ id: ENG })), `/engagements/${ENG}/attack-graph`],
      ["blast", () => blastGet(req("http://localhost/x"), ctx({ id: ENG, assetId: ASSET })), `/engagements/${ENG}/blast-radius/${ASSET}`],
    ];
    for (const [name, call, path] of cases) {
      stubBackend();
      const res = await call();
      assert.equal(res.status, 200, name);
      assert.equal(new URL(calls[0].url).pathname, path, name);
    }
  });
});

describe("attack-path BFF refuses what it should not forward", () => {
  test("a path parameter that is not a UUID is rejected before any backend call", async () => {
    stubBackend();
    for (const bad of ["../../admin", "..%2F..%2Fadmin", "abc", `${ENG}/extra`, ""]) {
      const res = await chokeGet(req("http://localhost/x"), ctx({ id: bad }));
      assert.equal(res.status, 400, bad);
    }
    const res = await detailGet(req("http://localhost/x"), ctx({ id: ENG, pathId: "../../etc" }));
    assert.equal(res.status, 400);
    assert.equal(calls.length, 0, "nothing was sent to the backend");
  });

  test("a malformed query value is rejected, not coerced", async () => {
    stubBackend();
    for (const q of ["refresh=maybe", "page=0", "page=-1", "page_size=101", "page_size=abc", "target_asset_id=nope"]) {
      const res = await listGet(req(`http://localhost/x?${q}`), ctx({ id: ENG }));
      assert.equal(res.status, 400, q);
    }
    assert.equal(calls.length, 0);
  });

  test("no token means no backend call", async () => {
    stubBackend();
    const res = await analysisGet(req("http://localhost/x", null), ctx({ id: ENG }));
    assert.equal(res.status, 401);
    assert.equal(calls.length, 0);
  });
});

describe("attack-path BFF keeps the backend's verdict", () => {
  test("a 404 from FastAPI stays a 404 with its message", async () => {
    stubBackend({ detail: "Attack path not found" }, 404);
    const res = await detailGet(req("http://localhost/x"), ctx({ id: ENG, pathId: PATH }));
    assert.equal(res.status, 404);
    assert.deepEqual(await res.json(), { error: "Attack path not found" });
  });

  test("a 403 is not turned into a success or an empty list", async () => {
    stubBackend({ detail: "Forbidden" }, 403);
    const res = await listGet(req("http://localhost/x"), ctx({ id: ENG }));
    assert.equal(res.status, 403);
    assert.deepEqual(await res.json(), { error: "Forbidden" });
  });

  test("a backend outage is an error, never an empty result", async () => {
    globalThis.fetch = async () => { throw new TypeError("fetch failed"); };
    const res = await analysisGet(req("http://localhost/x"), ctx({ id: ENG }));
    assert.ok(res.status >= 500, "an unreachable backend must not look like 'no paths'");
    const body = await res.json();
    assert.ok(body.error);
  });
});
