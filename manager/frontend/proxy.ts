import { NextRequest, NextResponse } from "next/server";
import { resolveTenantSubdomain, TENANT_HEADER } from "./lib/tenant";
import { pageAuthSurface } from "./lib/page-auth";

export function proxy(req: NextRequest) {
  const url = req.nextUrl;
  const pathname = url.pathname;

  // ── Auth gate ────────────────────────────────────────────────────────────
  // Check for the session cookie (written by /api/auth/login).
  // We only verify *presence* here — actual JWT validation happens inside
  // withBackend → FastAPI on every BFF call. Edge middleware cannot import
  // jsonwebtoken (Node.js only), so we keep this layer lightweight.
  const authSurface = pageAuthSurface(pathname);
  if (authSurface !== "public") {
    const tokenName = authSurface === "portal" ? "vedha_portal_token" : "vedha_token";
    const loginPath = authSurface === "portal" ? "/portal/login" : "/login";
    const token = req.cookies.get(tokenName)?.value;
    if (!token) {
      const loginUrl = new URL(loginPath, req.url);
      loginUrl.searchParams.set("next", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  // ── Tenant routing ──────────────────────────────────────────────────────
  const queryTenant = url.searchParams.get("tenant");
  const sub = resolveTenantSubdomain({
    host: req.headers.get("host"),
    headerTenant: req.headers.get("x-tenant"),
    queryTenant,
    cookieTenant: req.cookies.get("tenant")?.value,
  });

  const reqHeaders = new Headers(req.headers);
  if (sub) reqHeaders.set(TENANT_HEADER, sub);
  else reqHeaders.delete(TENANT_HEADER);

  const res = NextResponse.next({ request: { headers: reqHeaders } });
  if (queryTenant) {
    res.cookies.set("tenant", queryTenant.toLowerCase(), { sameSite: "lax", path: "/" });
  }
  return res;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
