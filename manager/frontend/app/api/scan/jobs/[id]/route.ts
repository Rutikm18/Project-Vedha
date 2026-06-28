import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { withBackend } from "../../../../../lib/with-backend";

// GET /api/scan/jobs/[id] → proxies to manager GET /agents/jobs/{job_id}
// Used by the frontend to poll job status after launch.
export const GET = withBackend(async (
  _req: NextRequest,
  { token },
  params?: { id?: string },
) => {
  const jobId = params?.id;
  if (!jobId) {
    return NextResponse.json({ error: "job id required" }, { status: 400 });
  }
  const job = await backend<unknown>(`/agents/jobs/${jobId}`, { token });
  return NextResponse.json(job);
});
