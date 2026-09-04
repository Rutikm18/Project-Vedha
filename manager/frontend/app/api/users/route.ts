import { NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  const users = await backend<unknown[]>("/users", { token });
  return NextResponse.json(users);
});
