import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  const requests = await backend<unknown[]>("/probe-enrollment/requests", { token });
  // The install command (with its manager URL and token) now comes from the
  // backend's /probe-enrollment/enroll-tokens, so both Fleet surfaces agree.
  return NextResponse.json({ requests });
});

export const POST = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json();
  const result = await backend("/probe-enrollment/approve", {
    token,
    method: "POST",
    body,
  });
  return NextResponse.json(result);
});
