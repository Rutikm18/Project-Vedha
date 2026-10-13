import { NextResponse } from "next/server";
import { backendResponse, bearerFrom } from "../../../../../lib/backend";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
type Context = { params: Promise<{ path?: string[] }> };
async function forward(req: Request, context: Context) {
  const headers = { "Cache-Control": "no-store" };
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401, headers });
  const { path = [] } = await context.params;
  if (!(path.length === 0 || (path.length === 1 && (path[0] === "options" || UUID.test(path[0]))))) return NextResponse.json({ error: "Unknown environment assessment route" }, { status: 404, headers });
  if (req.method === "POST" && path.length) return NextResponse.json({ error: "Method not allowed" }, { status: 405, headers });
  const query: Record<string, string> = {};
  const url = new URL(req.url);
  for (const key of ["page", "page_size", "engagement_ids"]) { const value = url.searchParams.get(key); if (value) query[key] = value; }
  let body: unknown;
  if (req.method === "POST") {
    try { body = await req.json(); }
    catch { return NextResponse.json({ error: "Invalid JSON body" }, { status: 400, headers }); }
  }
  try {
    const response = await backendResponse(`/attack-paths/environment-assessments${path.length ? "/" + path.join("/") : ""}`, {
      token, method: req.method, query, body,
      headers: req.headers.has("idempotency-key") ? { "Idempotency-Key": req.headers.get("idempotency-key")! } : undefined,
    });
    return new Response(await response.text(), { status: response.status, headers: { ...headers, "Content-Type": "application/json" } });
  } catch {
    return NextResponse.json({ error: "The environment assessment service is unavailable. Retry shortly." }, { status: 502, headers });
  }
}
export const GET = forward;
export const POST = forward;
