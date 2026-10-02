/**
 * Notification rules — BFF proxy.
 *   GET → /notification-rules   (every event with the tenant's choice, or the default)
 *   PUT → /notification-rules   (store the choices; the backend validates them)
 */
import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  return NextResponse.json(await backend("/notification-rules", { token }));
});

export const PUT = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json();
  return NextResponse.json(await backend("/notification-rules", { token, method: "PUT", body }));
});
