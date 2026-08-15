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
import jwt from "jsonwebtoken";
import { backend, BackendError, cookieFrom } from "../../../../lib/backend";

const secureCookie =
  process.env.AUTH_COOKIE_SECURE === "true" ||
  (process.env.AUTH_COOKIE_SECURE !== "false" && process.env.NODE_ENV === "production");

const ACCESS_COOKIE = "vedha_portal_token";
const REFRESH_COOKIE = "vedha_portal_refresh";
// The refresh cookie is only ever sent to this route, never to the data proxy.
const REFRESH_PATH = "/api/portal/login";

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

/** True only if the token's role claim is exactly "client". */
function isClientToken(accessToken: string): boolean {
  const claims = jwt.decode(accessToken) as { role?: string } | null;
  return !!claims && claims.role === "client";
}

export async function POST(req: Request) {
  let body: { email?: string; password?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "invalid JSON" }, { status: 400 });
  }
  const { email, password } = body;
  if (!email || !password) {
    return NextResponse.json({ error: "email and password are required" }, { status: 400 });
  }

  try {
    const d = await backend<{ access_token: string; refresh_token: string }>("/auth/login", {
      method: "POST",
      body: { email, password },
    });

    // Read claims without verifying signature (FastAPI already signed it) purely
    // to reject non-client logins at the door.
    if (!isClientToken(d.access_token)) {
      return NextResponse.json(
        { error: "This login is not a customer portal account.", code: "not_a_client" },
        { status: 403 },
      );
    }

    const res = NextResponse.json({ ok: true });
    setPortalCookies(res, d.access_token, d.refresh_token);
    return res;
  } catch (e) {
    if (e instanceof BackendError) {
      const code =
        e.status === 401 ? "invalid_credentials"
        : e.status === 429 ? "rate_limited"
        : e.status === 403 ? "not_a_client"
        : e.status >= 500 ? "backend_unavailable"
        : "login_failed";
      return NextResponse.json({ error: e.message, code }, { status: e.status });
    }
    return NextResponse.json({ error: "login failed" }, { status: 500 });
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
      { method: "POST", query: { refresh_token: refreshToken } },
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
