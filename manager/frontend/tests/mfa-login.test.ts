import { test, afterEach } from "node:test";
import assert from "node:assert/strict";
import jwt from "jsonwebtoken";
import { POST } from "../app/api/auth/login/route";
import { POST as PORTAL_POST } from "../app/api/portal/login/route";
import { groupKey, recoveryCodesText } from "../components/auth/MfaStep";
import { GET as MFA_GET, POST as MFA_POST } from "../app/api/auth/mfa/[action]/route";
import { POST as PORTAL_MFA_POST } from "../app/api/portal/mfa/[action]/route";
import { POST as USER_ACTION } from "../app/api/users/[id]/[action]/route";
import { NextRequest } from "next/server";
import { recoveryCodesNote } from "../components/settings/AccountSecuritySection";

const realFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = realFetch; });

const token = (role: string) => jwt.sign({ role, sub: "u1" }, "test-secret");
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

/** Backend stub answering each path with `answers[path]`; records every call. */
function backend(answers: Record<string, () => Response>) {
  const calls: { path: string; body: Record<string, unknown> | null }[] = [];
  globalThis.fetch = (async (input: string | URL | Request, init?: RequestInit) => {
    const path = new URL(String(input)).pathname;
    calls.push({ path, body: typeof init?.body === "string" ? JSON.parse(init.body) : null });
    return (answers[path] ?? (() => json({})))();
  }) as typeof fetch;
  return calls;
}

const req = (url: string, body: unknown, cookie?: string) => new Request(url, {
  method: "POST",
  headers: { "content-type": "application/json", ...(cookie ? { cookie } : {}) },
  body: JSON.stringify(body),
});

const cookiesOf = (res: Response) => res.headers.getSetCookie().join("\n");

test("a correct password on an MFA account opens no session, only a scoped challenge cookie", async () => {
  backend({ "/auth/login": () => json({ mfa_required: true, mfa_token: "challenge-1" }) });
  const res = await POST(req("http://x/api/auth/login", { email: "a@b.io", password: "pw" }));
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: false, mfa: "verify" });
  const cookies = cookiesOf(res);
  assert.doesNotMatch(cookies, /vedha_token=/);
  // The challenge never reaches page script: httpOnly, and only sent back to this route.
  assert.match(cookies, /vedha_mfa=challenge-1/);
  assert.match(cookies, /HttpOnly/i);
  assert.match(cookies, /Path=\/api\/auth\/login/);
  assert.match(cookies, /Max-Age=300/);
});

test("the code step sends the cookie's challenge to the backend and finishes sign-in", async () => {
  const calls = backend({
    "/auth/mfa/verify": () => json({ access_token: token("manager"), refresh_token: "r1" }),
  });
  const res = await POST(req("http://x/api/auth/login", { step: "verify", code: "123456" }, "vedha_mfa=challenge-1"));
  assert.equal(res.status, 200);
  assert.deepEqual(calls[0], { path: "/auth/mfa/verify", body: { mfa_token: "challenge-1", code: "123456" } });
  const cookies = cookiesOf(res);
  assert.match(cookies, /vedha_token=/);
  assert.match(cookies, /vedha_mfa=;/); // challenge cleared
});

test("a wrong code is reported as invalid_code, not as bad credentials", async () => {
  backend({ "/auth/mfa/verify": () => json({ detail: "Invalid or expired code" }, 401) });
  const res = await POST(req("http://x/api/auth/login", { step: "verify", code: "000000" }, "vedha_mfa=c"));
  assert.equal(res.status, 401);
  assert.equal((await res.json() as { code: string }).code, "invalid_code");
});

test("a code step without a challenge asks the user to start again and calls nothing", async () => {
  const calls = backend({});
  const res = await POST(req("http://x/api/auth/login", { step: "verify", code: "123456" }));
  assert.equal(res.status, 401);
  assert.equal((await res.json() as { code: string }).code, "mfa_expired");
  assert.equal(calls.length, 0);
});

test("an unknown step is refused", async () => {
  backend({});
  const res = await POST(req("http://x/api/auth/login", { step: "become_admin" }));
  assert.equal(res.status, 400);
});

test("required enrolment: setup returns the key, enable returns recovery codes with the session", async () => {
  backend({
    "/auth/login": () => json({ mfa_enrollment_required: true, mfa_token: "enrol-1" }),
    "/auth/mfa/enroll/setup": () => json({ secret: "JBSWY3DPEHPK3PXP", otpauth_uri: "otpauth://totp/x", account: "a@b.io" }),
    "/auth/mfa/enroll/enable": () => json({ access_token: token("admin"), refresh_token: "r1", recovery_codes: ["AAAAA-BBBBB"] }),
  });
  const first = await POST(req("http://x/api/auth/login", { email: "a@b.io", password: "pw" }));
  assert.deepEqual(await first.json(), { ok: false, mfa: "enroll" });

  const setup = await POST(req("http://x/api/auth/login", { step: "enroll_setup" }, "vedha_mfa=enrol-1"));
  const body = await setup.json() as { secret: string; otpauth_uri: string };
  assert.equal(body.secret, "JBSWY3DPEHPK3PXP");
  assert.doesNotMatch(cookiesOf(setup), /vedha_token=/);

  const done = await POST(req("http://x/api/auth/login", { step: "enroll_enable", code: "123456" }, "vedha_mfa=enrol-1"));
  assert.deepEqual(await done.json(), { ok: true, recovery_codes: ["AAAAA-BBBBB"] });
  assert.match(cookiesOf(done), /vedha_token=/);
});

test("a customer finishing MFA at the operator door is still turned away and revoked", async () => {
  const calls = backend({
    "/auth/mfa/verify": () => json({ access_token: token("client"), refresh_token: "r9" }),
  });
  const res = await POST(req("http://x/api/auth/login", { step: "verify", code: "123456" }, "vedha_mfa=c"));
  assert.equal(res.status, 403);
  assert.doesNotMatch(cookiesOf(res), /vedha_token=ey/);
  assert.ok(calls.some((c) => c.path === "/auth/logout" && c.body?.refresh_token === "r9"));
});

test("the portal keeps its own challenge cookie on its own path", async () => {
  backend({
    "/auth/login": () => json({ mfa_required: true, mfa_token: "pc-1" }),
    "/auth/mfa/verify": () => json({ access_token: token("client"), refresh_token: "r1" }),
  });
  const first = await PORTAL_POST(req("http://x/api/portal/login", { email: "c@d.io", password: "pw" }));
  const cookies = cookiesOf(first);
  assert.match(cookies, /vedha_portal_mfa=pc-1/);
  assert.match(cookies, /Path=\/api\/portal\/login/);
  // The operator challenge cookie means nothing to the portal route.
  const wrongCookie = await PORTAL_POST(req("http://x/api/portal/login", { step: "verify", code: "1" }, "vedha_mfa=pc-1"));
  assert.equal((await wrongCookie.json() as { code: string }).code, "mfa_expired");
  const done = await PORTAL_POST(req("http://x/api/portal/login", { step: "verify", code: "123456" }, "vedha_portal_mfa=pc-1"));
  assert.equal(done.status, 200);
  assert.match(cookiesOf(done), /vedha_portal_token=/);
});

test("manual-entry keys are grouped in fours", () => {
  assert.equal(groupKey("JBSWY3DPEHPK3PXP"), "JBSW Y3DP EHPK 3PXP");
});

// ── signed-in routes ─────────────────────────────────────────────────────────

const ctx = (action: string) => ({ params: Promise.resolve({ action }) });

test("self-service MFA routes pass only known actions, with the caller's own session", async () => {
  const calls = backend({ "/auth/mfa/status": () => json({ enabled: false }) });
  const res = await MFA_GET(new Request("http://x/api/auth/mfa/status", { headers: { cookie: "vedha_token=op" } }), ctx("status"));
  assert.equal(res.status, 200);
  assert.equal(calls[0].path, "/auth/mfa/status");

  const unknown = await MFA_POST(req("http://x/api/auth/mfa/reset", {}, "vedha_token=op"), ctx("reset"));
  assert.equal(unknown.status, 404);
  const wrongMethod = await MFA_GET(new Request("http://x/api/auth/mfa/disable", { headers: { cookie: "vedha_token=op" } }), ctx("disable"));
  assert.equal(wrongMethod.status, 404);
  const anonymous = await MFA_GET(new Request("http://x/api/auth/mfa/status"), ctx("status"));
  assert.equal(anonymous.status, 401);
  assert.equal(calls.length, 1);
});

test("the portal MFA route uses the portal session, not an operator one", async () => {
  const seen: string[] = [];
  globalThis.fetch = (async (_input: string | URL | Request, init?: RequestInit) => {
    seen.push(new Headers(init?.headers).get("authorization") ?? "");
    return json({ secret: "S", otpauth_uri: "otpauth://totp/x", account: "c@d.io" });
  }) as typeof fetch;
  const res = await PORTAL_MFA_POST(req("http://x/api/portal/mfa/setup", {}, "vedha_token=op; vedha_portal_token=cust"), ctx("setup"));
  assert.equal(res.status, 200);
  assert.deepEqual(seen, ["Bearer cust"]);
});

test("user actions map to their backend paths and reject anything else", async () => {
  const calls = backend({});
  const id = "6f1c2a4e-7b1d-4c8e-9a51-2f3e4d5c6b7a";
  const run = (action: string, userId = id) => USER_ACTION(
    new NextRequest(`http://x/api/users/${userId}/${action}`, { method: "POST", headers: { cookie: "vedha_token=admin" } }),
    { params: Promise.resolve({ id: userId, action }) },
  );
  assert.equal((await run("mfa-reset")).status, 200);
  assert.equal((await run("deactivate")).status, 200);
  assert.equal((await run("promote")).status, 404);
  assert.equal((await run("deactivate", "../../auth/x")).status, 404);
  assert.deepEqual(calls.map((c) => c.path), [`/auth/mfa/reset/${id}`, `/users/${id}/deactivate`]);
});

test("recovery-code wording flags a low count", () => {
  assert.deepEqual(recoveryCodesNote(10), { text: "10 recovery codes left", low: false });
  assert.equal(recoveryCodesNote(1).text, "Only 1 recovery code left — create new ones");
  assert.equal(recoveryCodesNote(0).low, true);
  const text = recoveryCodesText(["AAAAA-BBBBB"], "a@b.io", new Date("2026-10-03T10:00:00Z"));
  assert.match(text, /Account: a@b\.io\nCreated: 2026-10-03/);
  assert.doesNotMatch(recoveryCodesText(["X"], undefined), /Account:/);
});
