import { engagementGet } from "../../../../../lib/attack-paths-proxy";

/**
 * GET /api/engagements/{id}/attack-path-analysis → the stored engagement-level analysis:
 * choke points, coverage, freshness, and why a list is empty. Never computes on read.
 */
export const GET = engagementGet({
  uuids: ["id"],
  path: (p) => `/engagements/${p.id}/attack-path-analysis`,
});
