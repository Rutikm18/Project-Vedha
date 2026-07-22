import { NextResponse } from "next/server";

// POST /api/auth/logout — clears the session cookie
export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set("vedha_token", "", { path: "/", maxAge: 0 });
  return res;
}
