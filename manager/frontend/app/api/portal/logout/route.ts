/** Clear the customer-portal session cookie. */
import { NextResponse } from "next/server";

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set("vedha_portal_token", "", { httpOnly: true, path: "/", maxAge: 0 });
  return res;
}
