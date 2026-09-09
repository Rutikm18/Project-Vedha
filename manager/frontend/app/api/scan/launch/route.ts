import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import {
  toAgentJobRequest,
  type ScanLaunchBody,
} from "../../../../lib/scan-launch";
import { withBackend } from "../../../../lib/with-backend";

// Enqueues the same backend command shape used by the customer engagement
// workspace; only authentication and engagement resolution differ by surface.
export const POST = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json() as ScanLaunchBody;
  if (!body?.engagement_id) {
    return NextResponse.json({ error: "engagement_id is required" }, { status: 400 });
  }
  if (!body?.use_case_id) {
    return NextResponse.json({ error: "use_case_id is required" }, { status: 400 });
  }

  const dispatched = toAgentJobRequest(body);
  const result = await backend<Record<string, unknown>>("/agents/jobs", {
    token,
    method: "POST",
    body: dispatched,
  });
  return NextResponse.json({ ...result, dispatched }, { status: 201 });
});
