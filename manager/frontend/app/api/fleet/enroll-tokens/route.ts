/**
 * Install tokens (Fleet → Add agent) — BFF proxy.
 *   GET  → /probe-enrollment/enroll-tokens[?engagement_id=]
 *   POST → /probe-enrollment/enroll-tokens   { name, engagement_id, expires_in_minutes }
 * The raw token is returned once by POST (with the ready-made install commands)
 * and never again; GET lists prefixes and state only.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (req, { token }) => {
  const engagementId = req.nextUrl.searchParams.get("engagement_id") ?? undefined;
  const rows = await backend<unknown[]>("/probe-enrollment/enroll-tokens", {
    token,
    query: { engagement_id: engagementId || undefined },
  });
  return NextResponse.json(rows ?? []);
});

export const POST = withBackend(async (req, { token }) => {
  const body = await req.json();
  const created = await backend("/probe-enrollment/enroll-tokens", {
    token,
    method: "POST",
    body: {
      name: typeof body?.name === "string" && body.name.trim() ? body.name.trim() : "vedha-agent",
      engagement_id: body?.engagement_id,
      expires_in_minutes: 24 * 60,
    },
  });
  return NextResponse.json(created, { status: 201 });
});
