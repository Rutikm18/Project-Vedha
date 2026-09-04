import { NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }, params) => {
  const { engagementId } = params as { engagementId: string };
  const result = await backend<unknown>(`/engagements/${engagementId}/ai-report/draft`, { token });
  return NextResponse.json(result);
});
