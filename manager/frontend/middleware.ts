import { NextRequest, NextResponse } from "next/server";
import { resolveTenantSubdomain, TENANT_HEADER } from "./lib/tenant";

// Routes that don't need an auth token
const PUBLIC_PATHS = new Set(["/login"]);
// API routes carry their own Authorization header — don't block them at the middleware layer.
// Only page routes need the cookie check so the browser can be redirected to /login.
const PUBLIC_PREFIXES = [
  "/_next/",
  "/favicon",
  "/api/",
];

function isPublic(pathname: string): boolean {
  if (PUBLIC_PATHS.has(pathname)) return true;
  return PUBLIC_PREFIXES.some((p) => pathname.startsWith(p));
}

export function middleware(req: NextRequest) {
  const url = req.nextUrl;
  const pathname = url.pathname;

  // ── Auth gate ────────────────────────────────────────────────────────────
  // Check for the session cookie (written by /api/auth/login).
  // We only verify *presence* here — actual JWT validation happens inside
  // withBackend → FastAPI on every BFF call. Edge middleware cannot import
  // jsonwebtoken (Node.js only), so we keep this layer lightweight.
  if (!isPublic(pathname)) {
    const token = req.cookies.get("vedha_token")?.value;
    if (!token) {
      const loginUrl = new URL("/login", req.url);
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
