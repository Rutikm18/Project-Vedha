import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../lib/backend";

export async function GET(req: Request) {
  const token = bearerFrom(req);
  if (!token) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  try {
    const status = await backend("/ai/status", { token });
    return NextResponse.json(status, { headers: { "Cache-Control": "no-store" } });
  } catch (error) {
    const code = error instanceof BackendError ? error.status : 502;
    return NextResponse.json({
      error: error instanceof Error ? error.message : "Manager AI status unavailable",
    }, { status: code });
  }
}
