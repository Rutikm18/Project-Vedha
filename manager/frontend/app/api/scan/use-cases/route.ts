import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

// GET /api/scan/use-cases → proxies to manager GET /agents/use-cases
export const GET = withBackend(async (_req, { token }) => {
  const useCases = await backend<unknown[]>("/agents/use-cases", { token });
  return NextResponse.json(useCases ?? []);
});
