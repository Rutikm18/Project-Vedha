import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { toUiAgent } from "../../../../lib/adapters";

// GET /api/agents/register → proxies to manager GET /agents
// The dashboard's Agent Monitor polls this every 15s to show connected probes.
// Despite the "register" in the path, this is a LIST endpoint (GET).
// Map through toUiAgent so the client gets the camelCase UI shape (currentJobId)
// and an uppercase status (ONLINE/BUSY/OFFLINE) — the raw backend rows are
// snake_case with a lowercase enum, which the Agent Monitor could not read.
export const GET = withBackend(async (_req, { token }) => {
  const agents = await backend<any[]>("/agents", { token });
  return NextResponse.json((agents ?? []).map(toUiAgent));
});
