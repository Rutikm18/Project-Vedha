import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

export const POST = withBackend(async (req: NextRequest, { token }, params) => {
  const { engagementId } = params as { engagementId: string };
  const body = await req.json();
  const result = await backend<unknown>(`/engagements/${engagementId}/ai-report/approve`, {
    token, method: "POST", body: JSON.stringify(body),
  });
  return NextResponse.json(result);
});
