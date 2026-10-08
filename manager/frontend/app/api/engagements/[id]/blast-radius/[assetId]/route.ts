import { engagementGet } from "../../../../../../lib/attack-paths-proxy";

/** GET /api/engagements/{id}/blast-radius/{assetId} → hosts reachable if this one is owned. */
export const GET = engagementGet({
  uuids: ["id", "assetId"],
  path: (p) => `/engagements/${p.id}/blast-radius/${p.assetId}`,
});
