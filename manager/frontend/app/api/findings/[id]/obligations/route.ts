/** Regional compliance obligations for one finding (deterministic) — BFF proxy. */
import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { isUuid } from "../../../../../lib/intel-ids";
import { withBackend } from "../../../../../lib/with-backend";

export const GET = withBackend<{ id: string }>(async (_req, { token }, params) => {
  if (!isUuid(params?.id)) return NextResponse.json({ error: "invalid finding id" }, { status: 400 });
  return NextResponse.json(await backend<unknown>(`/findings/${params.id}/obligations`, { token }));
});
