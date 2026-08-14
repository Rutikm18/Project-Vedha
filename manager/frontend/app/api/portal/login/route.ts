/**
 * Customer-portal login — proxies to FastAPI /auth/login and stores the access
 * token in a SEPARATE httpOnly cookie (vedha_portal_token) so a customer session
 * is fully independent of any operator session. The backend already rate-limits
 * /auth/login, so the portal inherits brute-force protection.
 *
 * Guard: only a role=client token is accepted here — an operator who tries to
 * sign into the portal is rejected (they would see nothing anyway, but fail fast).
 */
import { NextResponse } from "next/server";
import jwt from "jsonwebtoken";
import { backend, BackendError } from "../../../../lib/backend";

const secureCookie =
  process.env.AUTH_COOKIE_SECURE === "true" ||
  (process.env.AUTH_COOKIE_SECURE !== "false" && process.env.NODE_ENV === "production");

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
    const claims = jwt.decode(d.access_token) as { role?: string } | null;
    if (!claims || claims.role !== "client") {
      return NextResponse.json(
        { error: "This login is not a customer portal account.", code: "not_a_client" },
        { status: 403 },
      );
    }

    const res = NextResponse.json({ ok: true });
    res.cookies.set("vedha_portal_token", d.access_token, {
      httpOnly: true,
      secure: secureCookie,
      sameSite: "strict",
      path: "/",
      maxAge: 15 * 60,
    });
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
