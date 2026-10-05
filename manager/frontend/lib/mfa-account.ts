/**
 * Self-service two-step sign-in for a signed-in user (Settings → Account
 * security), shared by the operator and portal BFF routes. Only these actions
 * pass through; anything else is a 404 rather than an open proxy onto /auth.
 */
import { NextResponse } from "next/server";
import { backend, BackendError, forwardedFor } from "./backend";

const ACTIONS: Record<string, "GET" | "POST"> = {
  status: "GET",
  setup: "POST",
  enable: "POST",
  disable: "POST",
  "recovery-codes": "POST",
};

export async function mfaAccount(req: Request, method: "GET" | "POST", action: string, token: string | null): Promise<Response> {
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  if (ACTIONS[action] !== method) return NextResponse.json({ error: "Not found" }, { status: 404 });
  try {
    let body: unknown;
    if (method === "POST") body = await req.json().catch(() => ({}));
    const data = await backend<unknown>(`/auth/mfa/${action}`, { method, token, body, headers: forwardedFor(req) });
    return NextResponse.json(data ?? {});
  } catch (e) {
    if (e instanceof BackendError) return NextResponse.json({ error: e.message }, { status: e.status });
    return NextResponse.json({ error: "Two-step sign-in service unavailable" }, { status: 502 });
  }
}
