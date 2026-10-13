import { backendResponse, bearerFrom } from "./backend";

type GraphResource = "attack-paths" | "attack-graph" | "chokepoints" | "blast-radius";
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** Legacy graph resources use real authorized backend data, never a demo store. */
export async function proxyAttackGraph(req: Request, engagementId: string, resource: GraphResource, objectId?: string): Promise<Response> {
  const headers = { "Cache-Control": "no-store", "Content-Type": "application/json" };
  const token = bearerFrom(req);
  if (!token) return Response.json({ error: "Not authenticated" }, { status: 401, headers });
  if (!UUID.test(engagementId) || (objectId && !UUID.test(objectId)) || (resource === "blast-radius" && !objectId)) {
    return Response.json({ error: "Unknown graph resource" }, { status: 404, headers });
  }
  const url = new URL(req.url);
  const query: Record<string, string | boolean> = {};
  for (const key of ["page", "target_asset_id"]) {
    const value = url.searchParams.get(key);
    if (value) query[key] = value;
  }
  const pageSize = url.searchParams.get("page_size") ?? url.searchParams.get("pageSize");
  if (pageSize) query.page_size = pageSize;
  if (resource === "attack-paths" && !objectId) query.refresh = false;
  try {
    const response = await backendResponse(`/engagements/${engagementId}/${resource}${objectId ? "/" + objectId : ""}`, { token, query });
    return new Response(await response.text(), { status: response.status, headers });
  } catch {
    return Response.json({ error: "The graph service is unavailable. Retry shortly." }, { status: 502, headers });
  }
}
