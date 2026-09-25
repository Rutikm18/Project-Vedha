/** Diff two scans — what's new, fixed, and still present. Proxies the backend
 *  /findings/compare and maps both sides to UI-shaped findings. */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { mapCompareResult } from "../../../../lib/adapters";

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const a = url.searchParams.get("a")?.trim().slice(0, 64);
  const b = url.searchParams.get("b")?.trim().slice(0, 64);
  if (!a || !b) {
    return NextResponse.json({ error: "Both scans (a, b) are required." }, { status: 400 });
  }
  const data = await backend<unknown>("/findings/compare", { token, query: { a, b } });
  return NextResponse.json(mapCompareResult(data));
});
