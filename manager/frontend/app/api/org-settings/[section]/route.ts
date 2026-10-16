/**
 * Organisation policy settings — BFF proxy.
 *   GET → /org-settings/{section}   (defaults until an admin edits it)
 *   PUT → /org-settings/{section}   (strictly validated by the backend)
 * Only the known sections are proxied, so the path cannot be steered
 * anywhere else on the backend.
 */
import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

const SECTIONS = new Set(["auth", "scan", "customer-defaults", "audit"]);

function section(params: { section: string } | undefined): string | null {
  const s = params?.section ?? "";
  return SECTIONS.has(s) ? s : null;
}

export const GET = withBackend(async (_req, { token }, params) => {
  const s = section(params as { section: string });
  if (!s) return NextResponse.json({ error: "Unknown settings section" }, { status: 404 });
  return NextResponse.json(await backend(`/org-settings/${s}`, { token }));
});

export const PUT = withBackend(async (req: NextRequest, { token }, params) => {
  const s = section(params as { section: string });
  if (!s) return NextResponse.json({ error: "Unknown settings section" }, { status: 404 });
  const body = await req.json();
  return NextResponse.json(await backend(`/org-settings/${s}`, { token, method: "PUT", body }));
});
