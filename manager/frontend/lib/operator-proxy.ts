/**
 * Operator BFF forwarding — the operator-console twin of the portal catch-all
 * (app/api/portal/[...path]/route.ts). Forwards the query string, the raw body
 * and the operator bearer token to FastAPI, and streams the response back with
 * content-type / content-disposition intact (so XLSX/CSV downloads work).
 */
import { NextResponse } from "next/server";
import { backendResponse, bearerFrom } from "./backend";

const REQUEST_HEADERS = ["accept", "content-type", "idempotency-key", "x-correlation-id"] as const;
const RESPONSE_HEADERS = ["content-type", "content-disposition", "retry-after", "x-correlation-id"] as const;

function pick(source: Headers, names: readonly string[]): Headers {
  const out = new Headers();
  for (const name of names) {
    const value = source.get(name);
    if (value) out.set(name, value);
  }
  return out;
}

/** Forward `req` to `backendPath` (already URL-encoded) with the same method. */
export async function forward(req: Request, backendPath: string): Promise<Response> {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const method = req.method.toUpperCase();
  const query = new URL(req.url).search;
  const hasBody = method !== "GET" && method !== "HEAD" && req.body !== null;
  try {
    const upstream = await backendResponse(`${backendPath}${query}`, {
      method,
      token,
      headers: pick(req.headers, REQUEST_HEADERS),
      rawBody: hasBody ? req.body : undefined,
    });
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: pick(upstream.headers, RESPONSE_HEADERS),
    });
  } catch {
    return NextResponse.json({ error: "The backend is temporarily unavailable" }, { status: 502 });
  }
}

export const enc = encodeURIComponent;
