import { engagementGet } from "../../../../../lib/attack-paths-proxy";

/**
 * GET /api/engagements/{id}/attack-path-zones → the stored routes aggregated into the subnets they
 * cross: where routes start and end, which subnet holds a host to fix, and which step between subnets
 * rests on an assumed link. Never computes on read.
 */
export const GET = engagementGet({
  uuids: ["id"],
  path: (p) => `/engagements/${p.id}/attack-path-zones`,
});
