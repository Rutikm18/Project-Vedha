/**
 * Posture analytics — BFF proxy to FastAPI GET /analytics/posture.
 * Both the posture scorecard and patch-comparison matrix consume this shared
 * payload, so preserving the backend contract keeps the two cards consistent.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId = url.searchParams.get("engagement_id") ?? undefined;
  const data = await backend<Record<string, unknown>>("/analytics/posture", {
    token,
    query: { engagement_id: engagementId },
  });
  return NextResponse.json(data ?? { has_runs: false });
});
