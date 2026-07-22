/**
 * Recent activity — BFF proxy to FastAPI GET /activity.
 * Merged scan-job + finding events for the tenant, newest first.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";

interface ApiActivity {
  id: string; timestamp: string; kind: string;
  action: string; detail: string; engagement_id: string;
}

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const limit = url.searchParams.get("limit") ?? "20";
  const items = await backend<ApiActivity[]>("/activity", { token, query: { limit } });
  return NextResponse.json(
    (items ?? []).map((it) => ({
      id: it.id,
      timestamp: it.timestamp,
      actor: it.kind,
      action: it.action,
      detail: it.detail,
      engagementId: it.engagement_id,
    })),
  );
});
