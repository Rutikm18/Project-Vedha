/**
 * Revoke an unused install token — BFF proxy.
 *   DELETE → /probe-enrollment/enroll-tokens/{id}
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { withBackend } from "../../../../../lib/with-backend";

export const DELETE = withBackend<{ id: string }>(async (_req, { token }, params) => {
  const id = encodeURIComponent(params?.id ?? "");
  await backend(`/probe-enrollment/enroll-tokens/${id}`, { token, method: "DELETE" });
  return new NextResponse(null, { status: 204 });
});
