/**
 * Integrations — BFF proxy. Lists the tenant's configured integrations
 * (secrets masked to has_secret). GET → /integrations
 */
import { NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  return NextResponse.json(await backend("/integrations", { token }));
});
