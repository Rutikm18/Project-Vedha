/** Clear the customer-portal session — both the access and the path-scoped
 *  refresh cookie. The refresh cookie must be cleared on the same path it was
 *  set with (/api/portal/login) or the browser keeps it. */
import { NextResponse } from "next/server";

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set("vedha_portal_token", "", { httpOnly: true, path: "/", maxAge: 0 });
  res.cookies.set("vedha_portal_refresh", "", {
    httpOnly: true,
    path: "/api/portal/login",
    maxAge: 0,
  });
  return res;
}
