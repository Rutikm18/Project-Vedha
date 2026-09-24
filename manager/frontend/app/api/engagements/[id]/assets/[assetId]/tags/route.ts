/** Replace an asset's manual tags (operator; audited) — BFF proxy. */
import { NextResponse } from "next/server";
import { backend } from "../../../../../../../lib/backend";
import { isUuid } from "../../../../../../../lib/intel-ids";
import { withBackend } from "../../../../../../../lib/with-backend";

export const PUT = withBackend<{ id: string; assetId: string }>(async (req, { token }, params) => {
  if (!isUuid(params?.id) || !isUuid(params?.assetId)) {
    return NextResponse.json({ error: "invalid id" }, { status: 400 });
  }
  const body = await req.json();
  const tags = Array.isArray(body?.tags) ? body.tags : [];
  return NextResponse.json(await backend<unknown>(
    `/engagements/${params.id}/assets/${params.assetId}/tags`, { token, method: "PUT", body: { tags } }));
});
