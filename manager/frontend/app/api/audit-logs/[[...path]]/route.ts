/** The audit trail — BFF proxy to /audit-logs[/facets|/integrity|/export|/{id}].
 *  Only those four sub-paths and a UUID are proxied, so the path cannot be steered
 *  elsewhere on the backend. The backend enforces who may read it (administrators). */
import { NextResponse } from "next/server";
import { enc, forward } from "../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ path?: string[] }> };

const NAMED = new Set(["facets", "integrity", "export"]);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function GET(req: Request, { params }: Ctx) {
  const { path = [] } = await params;
  if (path.length === 0) return forward(req, "/audit-logs");
  if (path.length === 1 && (NAMED.has(path[0]) || UUID.test(path[0]))) {
    return forward(req, `/audit-logs/${enc(path[0])}`);
  }
  return NextResponse.json({ error: "Not found" }, { status: 404 });
}
