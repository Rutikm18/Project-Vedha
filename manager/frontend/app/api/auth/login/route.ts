/**
 * Email + password login — proxies to the FastAPI backend's /auth/login.
 * The FastAPI access token becomes the single session token the UI stores and
 * sends on every subsequent /api/* call (which the BFF forwards to FastAPI).
 */
import { NextResponse } from "next/server";
import { backend, BackendError } from "../../../../lib/backend";

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
    const res = NextResponse.json({ token: d.access_token, refreshToken: d.refresh_token, email });
    // Set cookie so Edge middleware can gate routes without JS
    res.cookies.set("vedha_token", d.access_token, {
      httpOnly: false,   // must be readable by JS so fetchJson can also use it
      sameSite: "lax",
      path: "/",
      maxAge: 7 * 24 * 3600,
    });
    return res;
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 500;
    return NextResponse.json({ error: (e as Error).message || "login failed" }, { status });
  }
}

/** Token refresh — proxies to FastAPI /auth/refresh. */
export async function PUT(req: Request) {
  const { refreshToken } = await req.json().catch(() => ({}));
  if (!refreshToken) return NextResponse.json({ error: "refreshToken required" }, { status: 400 });
  try {
    const d = await backend<{ access_token: string; refresh_token: string }>(
      "/auth/refresh",
      { method: "POST", query: { refresh_token: refreshToken } },
    );
    return NextResponse.json({ token: d.access_token, refreshToken: d.refresh_token });
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 401;
    return NextResponse.json({ error: (e as Error).message }, { status });
  }
}
