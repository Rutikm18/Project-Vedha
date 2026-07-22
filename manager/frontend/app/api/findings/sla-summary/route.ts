/**
 * SLA summary — BFF proxy to FastAPI GET /findings/sla-summary.
 *
 * The backend SLA policy engine is authoritative: it returns each tracked
 * finding's state (breached/at_risk/due_soon/on_track) and hours remaining, so
 * the UI renders those verbatim instead of recomputing deadlines client-side
 * (which would risk drifting from the server's policy).
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

const SEV_TO_UI: Record<string, string> = {
  critical: "CRITICAL", high: "HIGH", medium: "MEDIUM", low: "LOW", info: "INFO",
};

interface ApiSlaItem {
  finding_id: string; title: string; severity: string;
  deadline: string | null; hours_remaining: number | null;
  hours_total: number | null; state: string;
}
interface ApiSlaSummary {
  breached: number; at_risk: number; due_soon: number; on_track: number;
  total_tracked: number; items: ApiSlaItem[];
}

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId = url.searchParams.get("engagement_id") ?? undefined;

  const data = await backend<ApiSlaSummary>("/findings/sla-summary", {
    token,
    query: { engagement_id: engagementId },
  });

  return NextResponse.json({
    summary: {
      breached: data.breached,
      atRisk: data.at_risk,
      dueSoon: data.due_soon,
      onTrack: data.on_track,
      totalTracked: data.total_tracked,
    },
    items: (data.items ?? []).map((it) => ({
      id: it.finding_id,
      title: it.title,
      severity: SEV_TO_UI[it.severity] ?? "INFO",
      deadline: it.deadline,
      hoursRemaining: it.hours_remaining,
      hoursTotal: it.hours_total,
      state: it.state, // breached | at_risk | due_soon | on_track
    })),
  });
});
