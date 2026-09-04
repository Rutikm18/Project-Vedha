import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

// POST /api/fleet/jobs/[jobId]/cancel → manager POST /agents/jobs/{job_id}/cancel
//
// One endpoint for both "stop this running scan" and "remove this queued job",
// because from the operator's side they are the same intent. The manager decides
// which case applies: a queued job is simply marked cancelled, while a running
// one also has its lease fence superseded — that is what makes the probe abandon
// the scan and pick up the next queued job.
//
// A 409 from the backend is meaningful rather than noise: it means the job
// already finished or was already cancelled, so the UI should refresh instead of
// implying it stopped something. withBackend already maps BackendError status
// through, so that reaches the caller intact.
export const POST = withBackend(async (
  _req: NextRequest,
  { token },
  params?: { jobId?: string },
) => {
  const jobId = params?.jobId;
  if (!jobId) {
    return NextResponse.json({ error: "job id required" }, { status: 400 });
  }
  const result = await backend<unknown>(
    `/agents/jobs/${encodeURIComponent(jobId)}/cancel`,
    { token, method: "POST" },
  );
  return NextResponse.json(result ?? {});
});
