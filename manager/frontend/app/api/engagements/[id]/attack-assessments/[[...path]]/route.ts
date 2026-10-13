import { NextResponse } from "next/server";
import { backendResponse, bearerFrom } from "../../../../../../lib/backend";

type Context = { params: Promise<{ id: string; path?: string[] }> };
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

async function forward(req: Request, context: Context) {
  const headers = { "Cache-Control": "no-store" };
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401, headers });
  const { id, path = [] } = await context.params;
  const validPath = path.length === 0 || (path.length === 1 && UUID.test(path[0])) ||
    (path.length === 3 && UUID.test(path[0]) && path[1] === "findings" && UUID.test(path[2]));
  if (!UUID.test(id) || !validPath) return NextResponse.json({ error: "Unknown assessment route" }, { status: 404, headers });
  if (req.method === "POST" && path.length) return NextResponse.json({ error: "Method not allowed" }, { status: 405, headers });
  const query: Record<string, string> = {};
  const url = new URL(req.url);
  for (const key of ["page", "page_size"]) {
    const value = url.searchParams.get(key);
    if (value) query[key] = value;
  }
  try {
    const response = await backendResponse(`/engagements/${id}/attack-assessments${path.length ? "/" + path.join("/") : ""}`, {
      token, method: req.method, query,
      headers: req.headers.has("idempotency-key") ? { "Idempotency-Key": req.headers.get("idempotency-key")! } : undefined,
    });
    return new Response(await response.text(), {
      status: response.status,
      headers: { ...headers, "Content-Type": response.headers.get("content-type") ?? "application/json" },
    });
  } catch {
    return NextResponse.json({ error: "The assessment service is unavailable. Retry shortly." }, { status: 502, headers });
  }
}

export const GET = forward;
export const POST = forward;
