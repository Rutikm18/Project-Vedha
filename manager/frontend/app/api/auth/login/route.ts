/**
 * Email + password login — proxies to the FastAPI backend's /auth/login.
 * The FastAPI access token becomes the single session token the UI stores and
 * sends on every subsequent /api/* call (which the BFF forwards to FastAPI).
 */
import { NextResponse } from "next/server";
import { backend, BackendError, cookieFrom, forwardedFor } from "../../../../lib/backend";
import { isClientToken } from "../../../../lib/token-role";

const PORTAL_ACCOUNT = {
  error: "This is a customer portal account. Sign in at the customer portal instead.",
  code: "portal_account",
} as const;

const secureCookie = process.env.AUTH_COOKIE_SECURE === "true"
  || (process.env.AUTH_COOKIE_SECURE !== "false" && process.env.NODE_ENV === "production");

function setSessionCookies(
  response: NextResponse,
  accessToken: string,
  refreshToken: string,
) {
  response.cookies.set("vedha_token", accessToken, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "strict",
    path: "/",
    maxAge: 15 * 60,
  });
  response.cookies.set("vedha_refresh_token", refreshToken, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "strict",
    path: "/api/auth/login",
    maxAge: 7 * 24 * 60 * 60,
  });
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
      headers: forwardedFor(req),
    });
    // A customer would only meet a console that refuses every call. Turn them
    // away here, and revoke the session just opened so nothing is left behind.
    if (isClientToken(d.access_token)) {
      await backend("/auth/logout", { method: "POST", body: { refresh_token: d.refresh_token } })
        .catch(() => {});
      return NextResponse.json(PORTAL_ACCOUNT, { status: 403 });
    }
    const res = NextResponse.json({ ok: true, email });
    setSessionCookies(res, d.access_token, d.refresh_token);
    return res;
  } catch (e) {
    if (e instanceof BackendError) {
      // Map backend failures to a stable code the UI can branch on without
      // string-matching messages.
      const code = e.status === 401 ? "invalid_credentials"
        : e.status === 429 ? "rate_limited"
        : e.status >= 500 ? "backend_unavailable"
        : "login_failed";
      const payload: { error: string; code: string; retryAfter?: number } = { error: e.message, code };
      if (e.retryAfter !== undefined) payload.retryAfter = e.retryAfter;
      const res = NextResponse.json(payload, { status: e.status });
      // Re-emit Retry-After so standards-aware clients (and the browser) can honor it.
      if (e.retryAfter !== undefined) res.headers.set("Retry-After", String(e.retryAfter));
      return res;
    }
    return NextResponse.json(
      { error: "login failed", code: "backend_unavailable" },
      { status: 502 },
    );
  }
}

/** Token refresh — proxies to FastAPI /auth/refresh. */
export async function PUT(req: Request) {
  const body = await req.json().catch(() => ({})) as { refreshToken?: string };
  const refreshToken = cookieFrom(req, "vedha_refresh_token") ?? body.refreshToken;
  if (!refreshToken) return NextResponse.json({ error: "refreshToken required" }, { status: 400 });
  try {
    const d = await backend<{ access_token: string; refresh_token: string }>(
      "/auth/refresh",
      { method: "POST", body: { refresh_token: refreshToken }, headers: forwardedFor(req) },
    );
    // The refresh door is operator-only too: never turn a customer's token into
    // an operator session.
    if (isClientToken(d.access_token)) {
      return NextResponse.json(PORTAL_ACCOUNT, { status: 403 });
    }
    const response = NextResponse.json({ ok: true });
    setSessionCookies(response, d.access_token, d.refresh_token);
    return response;
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 401;
    return NextResponse.json({ error: (e as Error).message }, { status });
  }
}

/**
 * Sign-out — revokes the refresh token server-side, then clears both cookies.
 * Lives HERE (not /api/auth/logout) because the refresh cookie is path-scoped to
 * this route: it is the only place the browser sends it. Revocation is
 * best-effort; the cookies are cleared regardless.
 */
export async function DELETE(req: Request) {
  const refreshToken = cookieFrom(req, "vedha_refresh_token");
  if (refreshToken) {
    await backend("/auth/logout", { method: "POST", body: { refresh_token: refreshToken } })
      .catch(() => {});
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set("vedha_token", "", {
    httpOnly: true, secure: secureCookie, sameSite: "strict", path: "/", maxAge: 0,
  });
  res.cookies.set("vedha_refresh_token", "", {
    httpOnly: true, secure: secureCookie, sameSite: "strict", path: "/api/auth/login", maxAge: 0,
  });
  return res;
}
