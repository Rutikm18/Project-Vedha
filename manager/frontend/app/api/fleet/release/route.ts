/**
 * Published agent release (version, architectures, signature) — BFF proxy.
 *   GET → /agent/release
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  return NextResponse.json(await backend("/agent/release", { token }));
});
