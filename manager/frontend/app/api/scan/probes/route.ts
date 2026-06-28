import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

// GET /api/scan/probes → proxies to manager GET /agents
export const GET = withBackend(async (_req, { token }) => {
  const probes = await backend<unknown[]>("/agents", { token });
  return NextResponse.json(probes ?? []);
});
