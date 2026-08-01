/**
 * Email + password login — proxies to the FastAPI backend's /auth/login.
 * The FastAPI access token becomes the single session token the UI stores and
 * sends on every subsequent /api/* call (which the BFF forwards to FastAPI).
 */
import { NextResponse } from "next/server";
import { backend, BackendError, cookieFrom } from "../../../../lib/backend";

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
    });
    const res = NextResponse.json({ ok: true, email });
    setSessionCookies(res, d.access_token, d.refresh_token);
    return res;
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 500;
    return NextResponse.json({ error: (e as Error).message || "login failed" }, { status });
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
      { method: "POST", query: { refresh_token: refreshToken } },
    );
    const response = NextResponse.json({ ok: true });
    setSessionCookies(response, d.access_token, d.refresh_token);
    return response;
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 401;
    return NextResponse.json({ error: (e as Error).message }, { status });
  }
}
