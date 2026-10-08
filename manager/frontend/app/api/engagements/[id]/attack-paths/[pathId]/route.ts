import { engagementGet } from "../../../../../../lib/attack-paths-proxy";

/** GET /api/engagements/{id}/attack-paths/{pathId} → one path, hop by hop. */
export const GET = engagementGet({
  uuids: ["id", "pathId"],
  path: (p) => `/engagements/${p.id}/attack-paths/${p.pathId}`,
});
