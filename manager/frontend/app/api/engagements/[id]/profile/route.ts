/**
 * Engagement regulatory profile (sector + jurisdictions) — BFF proxy.
 *   GET → /engagements/{id}/profile      PUT → same (admin/manager; audited)
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { isUuid } from "../../../../../lib/intel-ids";
import { withBackend } from "../../../../../lib/with-backend";

type P = { id: string };

export const GET = withBackend<P>(async (_req, { token }, params) => {
  if (!isUuid(params?.id)) return NextResponse.json({ error: "invalid engagement id" }, { status: 400 });
  return NextResponse.json(await backend<unknown>(`/engagements/${params.id}/profile`, { token }));
});

export const PUT = withBackend<P>(async (req, { token }, params) => {
  if (!isUuid(params?.id)) return NextResponse.json({ error: "invalid engagement id" }, { status: 400 });
  const body = await req.json();
  return NextResponse.json(await backend<unknown>(`/engagements/${params.id}/profile`, {
    token, method: "PUT", body: { sector: body?.sector, jurisdictions: body?.jurisdictions ?? [] },
  }));
});
