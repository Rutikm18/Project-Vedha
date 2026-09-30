import { NextResponse } from "next/server";

import { backend } from "../../../../../lib/backend";
import type { ReportDocument } from "../../../../../lib/report/report-document";
import { withBackend } from "../../../../../lib/with-backend";

/**
 * Authenticated, read-only BFF for the canonical Manager report document.
 * Manager remains responsible for tenant scoping and report-reader RBAC.
 */
export const GET = withBackend(async (_request, { token }, params) => {
  const { id } = params as { id: string };
  const document = await backend<ReportDocument>(
    `/engagements/${encodeURIComponent(id)}/report-document`,
    { token },
  );

  return NextResponse.json(document, {
    headers: { "Cache-Control": "private, no-store" },
  });
});
