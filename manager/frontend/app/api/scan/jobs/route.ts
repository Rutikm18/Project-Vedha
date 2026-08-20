import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

// GET /api/scan/jobs?engagement_id=... → proxies to manager
// GET /engagements/{engagement_id}/jobs
// Lets the scan page rehydrate queued/running/recent jobs from the DB on load,
// so a launched job survives a page refresh or navigation.
export const GET = withBackend(async (req: NextRequest, { token }) => {
  const engagementId = req.nextUrl.searchParams.get("engagement_id");
  if (!engagementId) {
    return NextResponse.json({ error: "engagement_id is required" }, { status: 400 });
  }
  const jobs = await backend<unknown>(`/engagements/${engagementId}/jobs`, { token });
  return NextResponse.json(jobs);
});
