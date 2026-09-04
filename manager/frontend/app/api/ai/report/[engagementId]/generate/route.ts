import { NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

export const POST = withBackend(async (_req, { token }, params) => {
  const { engagementId } = params as { engagementId: string };
  const result = await backend<unknown>(`/engagements/${engagementId}/ai-report/generate`, {
    token, method: "POST",
  });
  return NextResponse.json(result);
});
