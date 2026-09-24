/** Applicable regional frameworks + incident-reporting clocks — BFF proxy. */
import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { isUuid } from "../../../../../lib/intel-ids";
import { withBackend } from "../../../../../lib/with-backend";

export const GET = withBackend<{ id: string }>(async (_req, { token }, params) => {
  if (!isUuid(params?.id)) return NextResponse.json({ error: "invalid engagement id" }, { status: 400 });
  return NextResponse.json(await backend<unknown>(`/engagements/${params.id}/compliance`, { token }));
});
