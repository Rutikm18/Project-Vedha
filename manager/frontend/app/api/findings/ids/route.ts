/**
 * Finding ids matching the current filters — BFF proxy. Used to scope a findings
 * export to exactly what the Findings page shows, without paging the whole list.
 * Returns `{ finding_ids: string[] | null }`; null = no finding-level filter, so
 * the caller exports the whole engagement.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { backendFindingFilters } from "../../../../lib/findings-query";

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  // Same sanitised filter mapping the findings list uses (includes engagement_id).
  const filters = backendFindingFilters(url);
  const data = await backend<{ finding_ids: string[] | null }>("/findings/ids", {
    token,
    query: { ...filters },
  });
  return NextResponse.json(data);
});
