import { NextResponse } from "next/server";

// POST /api/auth/logout — clears the session cookie
export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set("vedha_token", "", {
    httpOnly: true,
    sameSite: "strict",
    path: "/",
    maxAge: 0,
  });
  res.cookies.set("vedha_refresh_token", "", {
    httpOnly: true,
    sameSite: "strict",
    path: "/api/auth/login",
    maxAge: 0,
  });
  return res;
}
