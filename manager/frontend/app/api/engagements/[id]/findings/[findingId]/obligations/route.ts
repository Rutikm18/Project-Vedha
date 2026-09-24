/** Regional compliance obligations a finding implicates — BFF proxy. */
import { NextResponse } from "next/server";
import { backend } from "../../../../../../../lib/backend";
import { isUuid } from "../../../../../../../lib/intel-ids";
import { withBackend } from "../../../../../../../lib/with-backend";

export const GET = withBackend<{ id: string; findingId: string }>(async (_req, { token }, params) => {
  if (!isUuid(params?.id) || !isUuid(params?.findingId)) {
    return NextResponse.json({ error: "invalid id" }, { status: 400 });
  }
  return NextResponse.json(await backend<unknown>(
    `/engagements/${params.id}/findings/${params.findingId}/obligations`, { token }));
});
