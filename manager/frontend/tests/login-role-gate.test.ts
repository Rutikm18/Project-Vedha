import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import jwt from "jsonwebtoken";
import { POST, PUT } from "../app/api/auth/login/route";
import { isClientToken, tokenRole } from "../lib/token-role";

const realFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = realFetch; });

const token = (role: string) => jwt.sign({ role, sub: "u1" }, "test-secret");

/** Backend stub: /auth/login and /auth/refresh answer with a token of `role`; records every call. */
function backendAs(role: string) {
  const calls: { path: string; body: unknown }[] = [];
  globalThis.fetch = (async (input: string | URL | Request, init?: RequestInit) => {
    const path = new URL(String(input)).pathname;
    calls.push({ path, body: typeof init?.body === "string" ? JSON.parse(init.body) : null });
    if (path === "/auth/login" || path === "/auth/refresh") {
      return new Response(JSON.stringify({ access_token: token(role), refresh_token: "refresh-1" }), {
        status: 200, headers: { "content-type": "application/json" },
      });
    }
    return new Response("{}", { status: 200, headers: { "content-type": "application/json" } });
  }) as typeof fetch;
  return calls;
}

const loginReq = () => new Request("http://x/api/auth/login", {
  method: "POST", headers: { "content-type": "application/json" },
  body: JSON.stringify({ email: "c@cust.io", password: "pw" }),
});

test("tokenRole / isClientToken read the role claim", () => {
  assert.equal(tokenRole(token("client")), "client");
  assert.equal(isClientToken(token("client")), true);
  assert.equal(isClientToken(token("admin")), false);
  assert.equal(tokenRole("not-a-jwt"), null);
  assert.equal(isClientToken("not-a-jwt"), false);
});

test("a customer account is turned away from the operator login with a clear code", async () => {
  backendAs("client");
  const res = await POST(loginReq());
  assert.equal(res.status, 403);
  const body = await res.json() as { code: string; error: string };
  assert.equal(body.code, "portal_account");
  assert.match(body.error, /customer portal/i);
});

test("the turned-away customer gets no operator cookies and the session is revoked", async () => {
  const calls = backendAs("client");
  const res = await POST(loginReq());
  assert.equal(res.headers.getSetCookie().length, 0);
  const logout = calls.find((c) => c.path === "/auth/logout");
  assert.ok(logout, "refresh token must be revoked");
  assert.deepEqual(logout.body, { refresh_token: "refresh-1" });
});

test("an operator still signs in and gets the session cookies", async () => {
  backendAs("admin");
  const res = await POST(loginReq());
  assert.equal(res.status, 200);
  const cookies = res.headers.getSetCookie().join("\n");
  assert.match(cookies, /vedha_token=/);
  assert.match(cookies, /vedha_refresh_token=/);
});

test("refresh will not turn a customer token into an operator session", async () => {
  backendAs("client");
  const res = await PUT(new Request("http://x/api/auth/login", {
    method: "PUT", headers: { "content-type": "application/json", cookie: "vedha_refresh_token=r1" },
  }));
  assert.equal(res.status, 403);
  assert.equal(res.headers.getSetCookie().length, 0);
});

test("refresh still works for an operator", async () => {
  backendAs("manager");
  const res = await PUT(new Request("http://x/api/auth/login", {
    method: "PUT", headers: { "content-type": "application/json", cookie: "vedha_refresh_token=r1" },
  }));
  assert.equal(res.status, 200);
  assert.match(res.headers.getSetCookie().join("\n"), /vedha_token=/);
});
