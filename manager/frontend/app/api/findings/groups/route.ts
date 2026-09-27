/**
 * Grouped findings — BFF proxy to GET /findings/groups. Uses the SAME filter
 * mapping as /api/findings so the grouped view and the list always agree.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";
import { mapFindingGroupPage, type ApiFindingGroupPage } from "../../../../lib/adapters";
import { backendFindingFilters, positiveInt } from "../../../../lib/findings-query";

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const page = positiveInt(url.searchParams.get("page"), 1, 100_000);
  const pageSize = positiveInt(url.searchParams.get("page_size"), 20, 100);
  const data = await backend<ApiFindingGroupPage>("/findings/groups", {
    token,
    query: { ...backendFindingFilters(url), page, page_size: pageSize },
  });
  return NextResponse.json(mapFindingGroupPage(data));
});
