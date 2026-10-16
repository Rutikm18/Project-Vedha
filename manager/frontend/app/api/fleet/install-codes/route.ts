/**
 * Zero-knowledge install codes (Fleet → Add Windows Agent) — BFF proxy.
 *   GET  → /probe-enrollment/install-codes[?engagement_id=]
 *   POST → /probe-enrollment/install-codes   { name, engagement_id, expires_in_minutes }
 * POST returns the opaque vac_ code ONCE together with the one-line command the
 * operator pastes to the client; GET lists prefixes and state only. No manager
 * URL, key or token is ever shown to the client — only the code and the command.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (req, { token }) => {
  const engagementId = req.nextUrl.searchParams.get("engagement_id") ?? undefined;
  const rows = await backend<unknown[]>("/probe-enrollment/install-codes", {
    token,
    query: { engagement_id: engagementId || undefined },
  });
  return NextResponse.json(rows ?? []);
});

export const POST = withBackend(async (req, { token }) => {
  const body = await req.json();
  const created = await backend("/probe-enrollment/install-codes", {
    token,
    method: "POST",
    body: {
      name: typeof body?.name === "string" && body.name.trim() ? body.name.trim() : "vedha-agent",
      engagement_id: body?.engagement_id,
      // The backend validates this against the allowed preset set.
      expires_in_minutes: typeof body?.expires_in_minutes === "number" ? body.expires_in_minutes : 24 * 60,
    },
  });
  return NextResponse.json(created, { status: 201 });
});
