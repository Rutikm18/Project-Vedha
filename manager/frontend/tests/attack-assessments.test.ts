import assert from "node:assert/strict";
import test from "node:test";
import { ApiError } from "../lib/fetcher";
import { assessmentRequest, assessmentBase } from "../lib/attack-assessments";
import { GET, POST } from "../app/api/engagements/[id]/attack-assessments/[[...path]]/route";

const engagement = "00000000-0000-4000-8000-000000000001";
const snapshot = "00000000-0000-4000-8000-000000000002";

test("feature denial preserves the operator session and returns its actual status", async () => {
  const original = globalThis.fetch;
  const calls: string[] = [];
  globalThis.fetch = async (input) => {
    calls.push(String(input));
    return Response.json({ error: "Assessment access is restricted" }, { status: 403 });
  };
  try {
    await assert.rejects(assessmentRequest("/assessments"), (error: unknown) => error instanceof ApiError && error.status === 403);
    assert.deepEqual(calls, ["/assessments"]);
  } finally { globalThis.fetch = original; }
});

test("expired session refresh retries exactly once and never erases a later permission denial", async () => {
  const original = globalThis.fetch;
  const calls: string[] = [];
  globalThis.fetch = async (input) => {
    calls.push(String(input));
    if (String(input) === "/api/auth/login") return Response.json({ ok: true });
    return Response.json({ error: "denied" }, { status: calls.length === 1 ? 401 : 403 });
  };
  try {
    await assert.rejects(assessmentRequest("/assessments"), (error: unknown) => error instanceof ApiError && error.status === 403);
    assert.deepEqual(calls, ["/assessments", "/api/auth/login", "/assessments"]);
  } finally { globalThis.fetch = original; }
});

test("BFF requires authentication and rejects route injection before forwarding", async () => {
  const original = globalThis.fetch;
  let forwarded = false;
  globalThis.fetch = async () => { forwarded = true; return Response.json({}); };
  try {
    const anonymous = await GET(new Request("http://test/assessments"), { params: Promise.resolve({ id: engagement }) });
    assert.equal(anonymous.status, 401);
    assert.equal(anonymous.headers.get("cache-control"), "no-store");
    const invalid = await GET(new Request("http://test/assessments", { headers: { authorization: "Bearer synthetic-token" } }), { params: Promise.resolve({ id: engagement, path: ["..", "auth"] }) });
    assert.equal(invalid.status, 404);
    assert.equal(forwarded, false);
  } finally { globalThis.fetch = original; }
});

test("BFF preserves backend denial and forwards only scoped path/pagination", async () => {
  const original = globalThis.fetch;
  let forwarded: { url: string; auth: string | null } | undefined;
  globalThis.fetch = async (input, init) => {
    forwarded = { url: String(input), auth: new Headers(init?.headers).get("authorization") };
    return Response.json({ detail: "scope denied" }, { status: 403 });
  };
  try {
    const response = await GET(new Request("http://test/assessments?page=2&page_size=20&tenant_id=foreign", { headers: { authorization: "Bearer synthetic-token" } }), { params: Promise.resolve({ id: engagement, path: [snapshot] }) });
    assert.equal(response.status, 403);
    assert.equal(response.headers.get("cache-control"), "no-store");
    assert.deepEqual(await response.json(), { detail: "scope denied" });
    assert.ok(forwarded?.url.includes(`/engagements/${engagement}/attack-assessments/${snapshot}`));
    assert.ok(forwarded?.url.includes("page=2"));
    assert.ok(!forwarded?.url.includes("tenant_id"));
    assert.equal(forwarded?.auth, "Bearer synthetic-token");
  } finally { globalThis.fetch = original; }
});

test("BFF cannot POST to detail endpoints or accept arbitrary effect data", async () => {
  const request = new Request("http://test/assessments", { method: "POST", headers: { authorization: "Bearer synthetic-token" } });
  const response = await POST(request, { params: Promise.resolve({ id: engagement, path: [snapshot] }) });
  assert.equal(response.status, 405);
  assert.equal(assessmentBase("../foreign"), "/api/engagements/..%2Fforeign/attack-assessments");
});
