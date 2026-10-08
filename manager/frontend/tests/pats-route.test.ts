import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import { NextRequest } from "next/server";
import { GET, POST } from "../app/api/auth/pats/route";
import { DELETE } from "../app/api/auth/pats/[id]/route";

const realFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = realFetch; });

function capture(status = 200, reply: unknown = {}) {
  const seen: { url: string; method: string; auth: string | null; body: string | null; contentType: string | null }[] = [];
  globalThis.fetch = (async (input: string | URL | Request, init?: RequestInit) => {
    const h = new Headers(init?.headers);
    seen.push({
      url: String(input), method: init?.method ?? "GET", auth: h.get("authorization"),
      body: typeof init?.body === "string" ? init.body : null, contentType: h.get("content-type"),
    });
    return new Response(JSON.stringify(reply), { status, headers: { "content-type": "application/json" } });
  }) as typeof fetch;
  return seen;
}

const authed = (init: RequestInit = {}) =>
  new NextRequest("http://x/api/auth/pats", { ...init, headers: { authorization: "Bearer tok", "content-type": "application/json" } });

// The backend mounts the auth router under /auth; these routes once called a
// path that does not exist (404) and sent the body JSON-encoded twice (422).
test("list calls the backend's /auth/personal-access-tokens", async () => {
  const seen = capture(200, []);
  const res = await GET(authed());
  assert.equal(res.status, 200);
  assert.match(seen[0].url, /\/auth\/personal-access-tokens$/);
  assert.equal(seen[0].auth, "Bearer tok");
});

test("create forwards the body as one JSON object, not a JSON string", async () => {
  const seen = capture(201, { id: "1", token: "vpat_x" });
  const payload = { name: "ci", scopes: ["api:read"], expires_in_days: 30 };
  await POST(authed({ method: "POST", body: JSON.stringify(payload) }));
  assert.match(seen[0].url, /\/auth\/personal-access-tokens$/);
  assert.equal(seen[0].method, "POST");
  assert.deepEqual(JSON.parse(seen[0].body!), payload);
});

test("revoke calls the backend's /auth/personal-access-tokens/{id}", async () => {
  const seen = capture(200, { ok: true });
  await DELETE(authed({ method: "DELETE" }), { params: Promise.resolve({ id: "abc" }) });
  assert.match(seen[0].url, /\/auth\/personal-access-tokens\/abc$/);
  assert.equal(seen[0].method, "DELETE");
});

test("a backend refusal reaches the caller with its status", async () => {
  capture(403, { detail: "Personal access tokens cannot create more personal access tokens" });
  const res = await POST(authed({ method: "POST", body: JSON.stringify({ name: "x" }) }));
  assert.equal(res.status, 403);
});
