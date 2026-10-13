import { engagementGet, QUERY } from "../../../../../lib/attack-paths-proxy";

/** GET /api/engagements/{id}/attack-graph → D3-compatible graph JSON. */
export const GET = engagementGet({
  uuids: ["id"],
  path: (p) => `/engagements/${p.id}/attack-graph`,
  query: { target_asset_id: QUERY.uuid },
});
