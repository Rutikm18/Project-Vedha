/**
 * Admin actions on an operator account: deactivate, activate, and clearing a
 * lost authenticator (mfa-reset). The backend enforces the admin role and the
 * tenant boundary; this route only maps the action to its backend path.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { withBackend } from "../../../../../lib/with-backend";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function backendPath(id: string, action: string): string | null {
  if (!UUID.test(id)) return null;
  if (action === "deactivate" || action === "activate") return `/users/${id}/${action}`;
  if (action === "mfa-reset") return `/auth/mfa/reset/${id}`;
  return null;
}

export const POST = withBackend<{ id: string; action: string }>(async (_req, { token }, params) => {
  const path = params ? backendPath(params.id, params.action) : null;
  if (!path) return NextResponse.json({ error: "Not found" }, { status: 404 });
  return NextResponse.json(await backend<unknown>(path, { method: "POST", token }));
});
