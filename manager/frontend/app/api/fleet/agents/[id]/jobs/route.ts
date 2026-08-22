import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

// GET /api/fleet/agents/[id]/jobs → manager GET /agents/{id}/job-history
// Per-probe job list (running + recent history) for the Fleet page.
export const GET = withBackend(async (
  _req: NextRequest,
  { token },
  params?: { id?: string },
) => {
  const agentId = params?.id;
  if (!agentId) {
    return NextResponse.json({ error: "agent id required" }, { status: 400 });
  }
  const jobs = await backend<unknown[]>(`/agents/${agentId}/job-history?limit=25`, { token });
  return NextResponse.json(jobs ?? []);
});
