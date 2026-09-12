import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { buildScanLaunchRequest, type ScanLaunchBody } from "../../../../lib/scan-launch";

// POST /api/scan/launch → proxies to manager POST /agents/jobs
// Enqueues a scan job that the probe picks up on its next poll cycle.
export const POST = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json() as ScanLaunchBody;

  if (!body?.engagement_id) {
    return NextResponse.json({ error: "engagement_id is required" }, { status: 400 });
  }
  if (!body?.use_case_id) {
    return NextResponse.json({ error: "use_case_id is required" }, { status: 400 });
  }

  const request = buildScanLaunchRequest(body);

  const result = await backend<{ job_id: string; status: string; use_case_id: string }>("/agents/jobs", {
    token,
    method: "POST",
    body: request,
  });

  // Echo back the exact non-secret request the probe will execute.
  return NextResponse.json({ ...result, dispatched: request }, { status: 201 });
});
