/**
 * Customer-portal login — proxies to FastAPI /auth/login and stores the access
 * token in a SEPARATE httpOnly cookie (vedha_portal_token) so a customer session
 * is fully independent of any operator session. The backend already rate-limits
 * /auth/login, so the portal inherits brute-force protection.
 *
 * Session longevity mirrors the operator side (app/api/auth/login): the short
 * access token (15 min) is paired with a path-scoped refresh cookie (7 days) so
 * a customer is not hard-logged-out mid-task. PUT rotates the pair.
 *
 * Guard: only a role=client token is accepted here — an operator who tries to
 * sign into the portal is rejected (they would see nothing anyway, but fail fast).
 */
import { NextResponse } from "next/server";
import { backend, BackendError, cookieFrom, forwardedFor } from "../../../../lib/backend";
import { isClientToken } from "../../../../lib/token-role";
import {
  clearChallengeCookie, loginErrorCode, MFA_EXPIRED, readLoginBody, runLoginStep, setChallengeCookie,
} from "../../../../lib/mfa-login";

const secureCookie =
  process.env.AUTH_COOKIE_SECURE === "true" ||
  (process.env.AUTH_COOKIE_SECURE !== "false" && process.env.NODE_ENV === "production");

const ACCESS_COOKIE = "vedha_portal_token";
const REFRESH_COOKIE = "vedha_portal_refresh";
// The refresh cookie is only ever sent to this route, never to the data proxy.
const REFRESH_PATH = "/api/portal/login";
// Holds the two-step challenge between the password and code steps (lib/mfa-login).
const MFA_COOKIE = "vedha_portal_mfa";

function setPortalCookies(
  res: NextResponse,
  accessToken: string,
  refreshToken: string,
) {
  res.cookies.set(ACCESS_COOKIE, accessToken, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "strict",
    path: "/",
    maxAge: 15 * 60,
  });
  res.cookies.set(REFRESH_COOKIE, refreshToken, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "strict",
    path: REFRESH_PATH,
    maxAge: 7 * 24 * 60 * 60,
  });
}

export async function POST(req: Request) {
  const body = readLoginBody(await req.json().catch(() => null));
  if (!body) return NextResponse.json({ error: "invalid JSON" }, { status: 400 });
  if (!body.step && (!body.email || !body.password)) {
    return NextResponse.json({ error: "email and password are required" }, { status: 400 });
  }

  try {
    const out = await runLoginStep(req, body, MFA_COOKIE, forwardedFor(req));
    if (out.kind === "challenge") {
      const res = NextResponse.json({ ok: false, mfa: out.mfa });
      setChallengeCookie(res, MFA_COOKIE, REFRESH_PATH, out.token, secureCookie);
      return res;
    }
    if (out.kind === "setup") {
      return NextResponse.json({ ok: false, mfa: "enroll", secret: out.secret, otpauth_uri: out.otpauthUri, account: out.account });
    }
    const d = out.tokens;

    // Read claims without verifying signature (FastAPI already signed it) purely
    // to reject non-client logins at the door; revoke the session just opened.
    if (!isClientToken(d.access_token)) {
      await backend("/auth/logout", { method: "POST", body: { refresh_token: d.refresh_token } })
        .catch(() => {});
      const res = NextResponse.json(
        { error: "This login is not a customer portal account.", code: "not_a_client" },
        { status: 403 },
      );
      if (body.step) clearChallengeCookie(res, MFA_COOKIE, REFRESH_PATH, secureCookie);
      return res;
    }

    const res = NextResponse.json(out.recoveryCodes ? { ok: true, recovery_codes: out.recoveryCodes } : { ok: true });
    setPortalCookies(res, d.access_token, d.refresh_token);
    if (body.step) clearChallengeCookie(res, MFA_COOKIE, REFRESH_PATH, secureCookie);
    return res;
  } catch (e) {
    if (e instanceof BackendError) {
      const code = e.status === 403 ? "not_a_client" : loginErrorCode(e, body.step);
      const payload: { error: string; code: string; retryAfter?: number } = { error: e.message, code };
      if (e.retryAfter !== undefined) payload.retryAfter = e.retryAfter;
      const res = NextResponse.json(payload, { status: code === MFA_EXPIRED ? 401 : e.status });
      if (e.retryAfter !== undefined) res.headers.set("Retry-After", String(e.retryAfter));
      if (code === MFA_EXPIRED) clearChallengeCookie(res, MFA_COOKIE, REFRESH_PATH, secureCookie);
      return res;
    }
    return NextResponse.json({ error: "login failed", code: "backend_unavailable" }, { status: 502 });
  }
}

/**
 * Token refresh — proxies to FastAPI /auth/refresh using the path-scoped
 * vedha_portal_refresh cookie, and rotates BOTH cookies. Mirrors the operator
 * PUT on /api/auth/login. Re-validates role=client so a rotated token can never
 * silently escalate the session out of the portal.
 */
export async function PUT(req: Request) {
  const refreshToken = cookieFrom(req, REFRESH_COOKIE);
  if (!refreshToken) {
    return NextResponse.json({ error: "not authenticated" }, { status: 401 });
  }
  try {
    const d = await backend<{ access_token: string; refresh_token: string }>(
      "/auth/refresh",
      { method: "POST", body: { refresh_token: refreshToken }, headers: forwardedFor(req) },
    );
    if (!isClientToken(d.access_token)) {
      return NextResponse.json({ error: "not a customer portal account" }, { status: 403 });
    }
    const res = NextResponse.json({ ok: true });
    setPortalCookies(res, d.access_token, d.refresh_token);
    return res;
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 401;
    return NextResponse.json({ error: (e as Error).message }, { status });
  }
}

/**
 * Sign-out — revokes the refresh token server-side, then clears both cookies.
 * Must live on REFRESH_PATH: the path-scoped refresh cookie reaches no other
 * route. Revocation is best-effort; the cookies are cleared regardless.
 */
export async function DELETE(req: Request) {
  const refreshToken = cookieFrom(req, REFRESH_COOKIE);
  if (refreshToken) {
    await backend("/auth/logout", { method: "POST", body: { refresh_token: refreshToken } })
      .catch(() => {});
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set(ACCESS_COOKIE, "", {
    httpOnly: true, secure: secureCookie, sameSite: "strict", path: "/", maxAge: 0,
  });
  res.cookies.set(REFRESH_COOKIE, "", {
    httpOnly: true, secure: secureCookie, sameSite: "strict", path: REFRESH_PATH, maxAge: 0,
  });
  return res;
}
