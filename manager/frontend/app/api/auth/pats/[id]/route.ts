import { NextResponse } from "next/server";
import { backend } from "../../../../../lib/backend";
import { withBackend } from "../../../../../lib/with-backend";

export const DELETE = withBackend(async (_req, { token }, params) => {
  const { id } = params as { id: string };
  await backend<unknown>(`/personal-access-tokens/${id}`, {
    token,
    method: "DELETE",
  });
  return NextResponse.json({ ok: true });
});
