import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

// GET /api/fleet/jobs?agent_id=&engagement_id=&running=&status=&limit=
//   → manager GET /agents/jobs
// The tenant-wide job feed for the Fleet page: every probe's jobs with probe +
// engagement names resolved, filterable by probe, engagement, status, running.
export const GET = withBackend(async (req: NextRequest, { token }) => {
  const sp = req.nextUrl.searchParams;
  const query: Record<string, string> = {};
  for (const k of ["agent_id", "engagement_id", "status", "running", "limit"]) {
    const v = sp.get(k);
    if (v) query[k] = v;
  }
  const jobs = await backend<unknown[]>("/agents/jobs", { token, query });
  return NextResponse.json(jobs ?? []);
});
