/**
 * Revoke an unused install code — BFF proxy.
 *   DELETE → /probe-enrollment/install-codes/{id}
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { withBackend } from "../../../../../lib/with-backend";

export const DELETE = withBackend<{ id: string }>(async (_req, { token }, params) => {
  const id = encodeURIComponent(params?.id ?? "");
  await backend(`/probe-enrollment/install-codes/${id}`, { token, method: "DELETE" });
  return new NextResponse(null, { status: 204 });
});
