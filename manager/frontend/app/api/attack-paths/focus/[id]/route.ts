import { engagementGet } from "../../../../../lib/attack-paths-proxy";

/**
 * GET /api/attack-paths/focus/{id} → FastAPI /attack-paths/focus/{id}
 * The dashboard's "fix first" card for one engagement: its highest-risk stored route, the
 * smallest fix set and the hosts whose fix removes the most modelled risk (beta).
 * Read-only: unlike the path-list endpoint the backend never recomputes or writes on this call.
 * `id` must be a UUID; no query keys are forwarded.
 */
export const GET = engagementGet({
  uuids: ["id"],
  path: (p) => `/attack-paths/focus/${p.id}`,
});
