/** Scans that produced findings — options for the findings "filter by scan"
 *  control and the two-scan compare picker. */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { mapScanOption, type ApiScanOption } from "../../../../lib/adapters";

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId =
    url.searchParams.get("engagement_id") ??
    url.searchParams.get("engagementId") ??
    undefined;
  const scans = await backend<ApiScanOption[]>("/findings/scans", {
    token,
    query: { engagement_id: engagementId },
  });
  return NextResponse.json(scans.map(mapScanOption));
});
