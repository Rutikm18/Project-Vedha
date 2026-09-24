/** Affected assets (with finding counts) — options for the findings IP filter. */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { mapAsset, type ApiFindingAsset } from "../../../../lib/adapters";

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId = url.searchParams.get("engagement_id") ?? undefined;
  const assets = await backend<ApiFindingAsset[]>("/findings/assets", {
    token,
    query: { engagement_id: engagementId },
  });
  return NextResponse.json(assets.map(mapAsset));
});
