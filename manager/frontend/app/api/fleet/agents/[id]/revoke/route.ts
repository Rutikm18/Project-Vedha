/**
 * Revoke an agent for good — BFF proxy (operator only: admin / manager).
 *   POST → /agents/{id}/revoke   { reason?: string }
 * Nothing is deleted on the manager; the agent is just never accepted again.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

export const POST = withBackend<{ id: string }>(async (req, { token }, params) => {
  const id = encodeURIComponent(params?.id ?? "");
  const body = await req.json().catch(() => ({}));
  const reason = typeof body?.reason === "string" ? body.reason.slice(0, 500) : null;
  const result = await backend(`/agents/${id}/revoke`, { token, method: "POST", body: { reason } });
  return NextResponse.json(result);
});
