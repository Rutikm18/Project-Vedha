/**
 * Set, extend or clear an agent's access expiry — BFF proxy (operator only).
 *   PATCH → /agents/{id}/access-expiry   { access_expires_at: ISO string | null }
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../../../lib/backend";
import { withBackend } from "../../../../../../lib/with-backend";

export const PATCH = withBackend<{ id: string }>(async (req, { token }, params) => {
  const id = encodeURIComponent(params?.id ?? "");
  const body = await req.json();
  const result = await backend(`/agents/${id}/access-expiry`, {
    token,
    method: "PATCH",
    body: { access_expires_at: body?.access_expires_at ?? null },
  });
  return NextResponse.json(result);
});
