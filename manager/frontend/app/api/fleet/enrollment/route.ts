import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  const requests = await backend<unknown[]>("/probe-enrollment/requests", { token });
  return NextResponse.json({
    requests,
    manager_url: (process.env.MANAGER_PUBLIC_URL ?? "").replace(/\/$/, ""),
  });
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
