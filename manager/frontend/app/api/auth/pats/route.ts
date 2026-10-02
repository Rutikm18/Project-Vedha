import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  const pats = await backend<unknown[]>("/auth/personal-access-tokens", { token });
  return NextResponse.json(pats);
});

export const POST = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json();
  const pat = await backend<unknown>("/auth/personal-access-tokens", {
    token,
    method: "POST",
    body,
  });
  return NextResponse.json(pat);
});
