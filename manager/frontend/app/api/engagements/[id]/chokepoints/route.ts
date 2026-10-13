import { engagementGet } from "../../../../../lib/attack-paths-proxy";

/** GET /api/engagements/{id}/chokepoints → hosts to fix first and the smallest cutting set. */
export const GET = engagementGet({
  uuids: ["id"],
  path: (p) => `/engagements/${p.id}/chokepoints`,
});
