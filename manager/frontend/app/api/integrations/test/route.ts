/**
 * Integration test — BFF proxy. Queues a test notification to all enabled
 * integrations so an operator can confirm delivery. POST → /integrations/test
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const POST = withBackend(async (_req, { token }) => {
  return NextResponse.json(await backend("/integrations/test", { token, method: "POST" }));
});
