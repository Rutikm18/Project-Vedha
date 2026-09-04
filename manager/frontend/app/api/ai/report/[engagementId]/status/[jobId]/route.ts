import { NextResponse } from "next/server";
import { backend } from "../../../../../../../lib/backend";
import { withBackend } from "../../../../../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }, params) => {
  const { engagementId, jobId } = params as { engagementId: string; jobId: string };
  const result = await backend<unknown>(`/engagements/${engagementId}/ai-report/status/${jobId}`, { token });
  return NextResponse.json(result);
});
