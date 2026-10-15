import { NextResponse } from "next/server";

import { backend } from "../../../../../lib/backend";
import type { ReportDocument } from "../../../../../lib/report/report-document";
import { withBackend } from "../../../../../lib/with-backend";

/**
 * Authenticated, read-only BFF for the canonical Manager report document.
 * Manager remains responsible for tenant scoping and report-reader RBAC.
 */
export const GET = withBackend(async (request, { token }, params) => {
  const { id } = params as { id: string };
  // Optional finding-selection scope: forward the comma-separated ids verbatim.
  // Manager parses and tenant-checks them; an absent param means the whole engagement.
  const findingIds = new URL(request.url).searchParams.get("finding_ids");
  const scope = findingIds ? `?finding_ids=${encodeURIComponent(findingIds)}` : "";
  const document = await backend<ReportDocument>(
    `/engagements/${encodeURIComponent(id)}/report-document${scope}`,
    { token },
  );

  return NextResponse.json(document, {
    headers: { "Cache-Control": "private, no-store" },
  });
});
