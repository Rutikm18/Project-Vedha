import { engagementGet, QUERY } from "../../../../lib/attack-paths-proxy";

/**
 * GET /api/attack-paths/overview → FastAPI /attack-paths/overview
 * Stored attack-path results for every engagement of the caller's tenant (beta).
 * Read-only: the backend never computes on this call. No path parameters; `limit`
 * is the only query key forwarded.
 */
export const GET = engagementGet({
  uuids: [],
  path: () => "/attack-paths/overview",
  query: { limit: QUERY.positiveInt(200) },
});
