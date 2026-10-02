import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { LoginError, loginWithPassword, revokeSessionToken, setCookieValue } from "../cli/auth";

const realFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = realFetch; });

interface Call { url: string; method: string; headers: Record<string, string>; body?: string }

/** Stub fetch with a route table keyed by "METHOD /path"; records every call. */
function stub(routes: Record<string, () => Response>): Call[] {
  const calls: Call[] = [];
  globalThis.fetch = (async (input: string | URL | Request, init?: RequestInit) => {
    const url = String(input);
    const method = (init?.method ?? "GET").toUpperCase();
    calls.push({ url, method, headers: (init?.headers ?? {}) as Record<string, string>, body: init?.body as string | undefined });
    const key = `${method} ${new URL(url).pathname}`;
    const make = routes[key];
    if (!make) throw new Error(`unexpected request ${key}`);
    return make();
  }) as typeof fetch;
  return calls;
}

function loginOk(): Response {
  const h = new Headers({ "content-type": "application/json" });
  h.append("set-cookie", "vedha_token=ACCESS.jwt.value; Path=/; Max-Age=900; HttpOnly; SameSite=strict");
  h.append("set-cookie", "vedha_refresh_token=REFRESH.jwt.value; Path=/api/auth/login; Max-Age=604800; HttpOnly");
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers: h });
}
const json = (b: unknown, status = 200) => new Response(JSON.stringify(b), { status, headers: { "content-type": "application/json" } });

test("setCookieValue reads a named cookie and ignores attributes", () => {
  const lines = ["a=1; Path=/", "vedha_token=abc%2Edef; HttpOnly"];
  assert.equal(setCookieValue(lines, "vedha_token"), "abc.def");
  assert.equal(setCookieValue(lines, "missing"), null);
});

test("login exchanges the browser session for a revocable CLI token", async () => {
  const calls = stub({
    "POST /api/auth/login": loginOk,
    "POST /api/auth/pats": () => json({ id: "pat-1", token: "vpat_secret" }, 201),
    "DELETE /api/auth/login": () => json({ ok: true }),
    "GET /api/auth/me": () => json({ email: "ops@corp.io", role: "admin" }),
  });
  const s = await loginWithPassword("http://srv", "ops@corp.io", "pw");
  assert.equal(s.token, "vpat_secret");
  assert.equal(s.patId, "pat-1");
  assert.equal(s.role, "admin");
  assert.equal(s.email, "ops@corp.io");

  const pat = calls.find((c) => c.url.endsWith("/api/auth/pats"))!;
  assert.equal(pat.headers.Authorization, "Bearer ACCESS.jwt.value");
  const body = JSON.parse(pat.body!);
  assert.deepEqual(body.scopes, ["api:read", "api:write"]);
  assert.equal(body.expires_in_days, 30);
  assert.match(body.name, /^vedha-cli \(/);

  // The browser refresh token is revoked, and the identity call uses the PAT.
  const revoke = calls.find((c) => c.method === "DELETE")!;
  assert.match(revoke.headers.Cookie, /vedha_refresh_token=REFRESH\.jwt\.value/);
  const me = calls.find((c) => c.url.endsWith("/api/auth/me"))!;
  assert.equal(me.headers.Authorization, "Bearer vpat_secret");
});

test("wrong password is a clear error and mints nothing", async () => {
  const calls = stub({
    "POST /api/auth/login": () => json({ error: "nope", code: "invalid_credentials" }, 401),
  });
  await assert.rejects(loginWithPassword("http://srv", "a@b.co", "bad"), (e: unknown) => {
    assert.ok(e instanceof LoginError);
    assert.equal(e.message, "Invalid email or password.");
    assert.equal(e.unreachable, false);
    return true;
  });
  assert.equal(calls.length, 1);
});

test("rate limited login says to wait", async () => {
  stub({ "POST /api/auth/login": () => json({ error: "x", code: "rate_limited" }, 429) });
  await assert.rejects(loginWithPassword("http://srv", "a@b.co", "pw"), /Too many attempts/);
});

test("an unreachable server is flagged so the CLI can hint at starting it", async () => {
  globalThis.fetch = (async () => { throw new Error("ECONNREFUSED"); }) as typeof fetch;
  await assert.rejects(loginWithPassword("http://srv", "a@b.co", "pw"), (e: unknown) => {
    assert.ok(e instanceof LoginError && e.unreachable);
    return true;
  });
});

test("if the token is refused the refresh token is still revoked and nothing is stored", async () => {
  const calls = stub({
    "POST /api/auth/login": loginOk,
    "POST /api/auth/pats": () => json({ error: "forbidden" }, 403),
    "DELETE /api/auth/login": () => json({ ok: true }),
  });
  await assert.rejects(loginWithPassword("http://srv", "a@b.co", "pw"), /would not issue a CLI token/);
  assert.ok(calls.some((c) => c.method === "DELETE"));
});

test("logout revokes the token on the server", async () => {
  const calls = stub({ "DELETE /api/auth/pats/pat-1": () => json({ ok: true }) });
  await revokeSessionToken({ email: "a@b.co", token: "vpat_secret", role: "operator", savedAt: "", patId: "pat-1" });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].headers.Authorization, "Bearer vpat_secret");
});

test("logout revokes against the server it was given, not a default", async () => {
  const calls = stub({ "DELETE /api/auth/pats/pat-9": () => json({ ok: true }) });
  await revokeSessionToken({ email: "a@b.co", token: "t", role: "operator", savedAt: "", patId: "pat-9" }, "http://other:3100");
  assert.equal(calls[0].url, "http://other:3100/api/auth/pats/pat-9");
});

test("logout of an older session with no token id makes no request", async () => {
  const calls = stub({});
  await revokeSessionToken({ email: "a@b.co", token: "t", role: "operator", savedAt: "" });
  assert.equal(calls.length, 0);
});

test("the legacy OTP endpoints and stores are gone", () => {
  const root = path.resolve(__dirname, "..");
  for (const f of ["app/api/auth/request", "app/api/auth/verify", "lib/auth-store.ts", "lib/auth-middleware.ts", "lib/permissions-store.ts"]) {
    assert.equal(fs.existsSync(path.join(root, f)), false, `${f} should be removed`);
  }
});
