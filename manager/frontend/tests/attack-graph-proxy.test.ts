import assert from "node:assert/strict";
import test from "node:test";
import { proxyAttackGraph } from "../lib/attack-graph-proxy";

const id = "00000000-0000-4000-8000-000000000001";

test("legacy graph proxy cannot expose a static graph without authentication", async () => {
  const response = await proxyAttackGraph(new Request("http://test/graph"), id, "attack-graph");
  assert.equal(response.status, 401);
  assert.equal(response.headers.get("cache-control"), "no-store");
});

test("legacy graph requests use the real engagement and force readonly pagination", async () => {
  const original = globalThis.fetch;
  let url = "";
  globalThis.fetch = async (input) => { url = String(input); return Response.json({ detail: "unknown engagement" }, { status: 404 }); };
  try {
    const response = await proxyAttackGraph(new Request("http://test/graph?pageSize=30&refresh=true&tenant_id=foreign", { headers: { authorization: "Bearer synthetic-token" } }), id, "attack-paths");
    assert.equal(response.status, 404);
    assert.ok(url.includes(`/engagements/${id}/attack-paths`));
    assert.ok(url.includes("page_size=30"));
    assert.ok(url.includes("refresh=false"));
    assert.ok(!url.includes("tenant_id"));
  } finally { globalThis.fetch = original; }
});
