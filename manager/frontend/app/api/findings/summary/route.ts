import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

interface ApiSummary {
  total: number;
  open_total: number;
  critical_open: number;
  high_open: number;
  medium_open: number;
  low_open: number;
  info_open: number;
  validated: number;
  blind: number;
  average_risk: number;
}

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId =
    url.searchParams.get("engagement_id")
    ?? url.searchParams.get("engagementId")
    ?? undefined;
  const summary = await backend<ApiSummary>("/findings/summary", {
    token,
    query: { engagement_id: engagementId },
  });
  return NextResponse.json({
    total: summary.total,
    openTotal: summary.open_total,
    criticalOpen: summary.critical_open,
    highOpen: summary.high_open,
    mediumOpen: summary.medium_open,
    lowOpen: summary.low_open,
    infoOpen: summary.info_open,
    validated: summary.validated,
    blind: summary.blind,
    averageRisk: summary.average_risk,
  });
});
