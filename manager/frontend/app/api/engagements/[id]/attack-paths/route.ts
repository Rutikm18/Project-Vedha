import { engagementGet, QUERY } from "../../../../../lib/attack-paths-proxy";

/**
 * GET /api/engagements/{id}/attack-paths → FastAPI /engagements/{id}/attack-paths
 * The stored list. `refresh=true` makes the backend recompute and store first.
 */
export const GET = engagementGet({
  uuids: ["id"],
  path: (p) => `/engagements/${p.id}/attack-paths`,
  query: {
    refresh: QUERY.boolean,
    target_asset_id: QUERY.uuid,
    page: QUERY.positiveInt(10_000),
    page_size: QUERY.positiveInt(100),
  },
});
