import { NextResponse } from "next/server";
import { backendResponse, bearerFrom } from "../../../../../../lib/backend";
import { isUuid } from "../../../../../../lib/attack-paths-proxy";

export async function POST(req: Request, context: { params: Promise<{ id: string }> }) {
  const headers = { "Cache-Control": "no-store" };
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401, headers });
  const { id } = await context.params;
  const target = new URL(req.url).searchParams.get("target_asset_id");
  if (!isUuid(id) || (target && !isUuid(target))) return NextResponse.json({ error: "Invalid graph scope" }, { status: 400, headers });
  try {
    const response = await backendResponse(`/engagements/${id}/attack-paths/refresh`, {
      token, method: "POST", query: target ? { target_asset_id: target } : undefined,
    });
    return new Response(await response.text(), { status: response.status, headers: { ...headers, "Content-Type": "application/json" } });
  } catch {
    return NextResponse.json({ error: "The graph service is unavailable. Retry shortly." }, { status: 502, headers });
  }
}
