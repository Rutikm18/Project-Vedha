/**
 * SLA policy — BFF proxy.
 *   GET → /sla-policy            (effective per-severity windows for the tenant)
 *   PUT → /sla-policy            (upsert the tenant's custom windows)
 */
import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  return NextResponse.json(await backend("/sla-policy", { token }));
});

export const PUT = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json();
  return NextResponse.json(await backend("/sla-policy", { token, method: "PUT", body }));
});
