/**
 * Findings — BFF proxy to the FastAPI backend (single source of truth).
 * Replaces the in-memory `findings-store`. Returns an array of UI-shaped findings.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";
import { toUiFinding } from "../../../lib/adapters";
import { backendFindingFilters, positiveInt } from "../../../lib/findings-query";

const VALID_SORTS = new Set(["risk", "cvss", "epss", "date"]);

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  // One sanitised filter mapping, shared with /api/findings/groups.
  const filters = backendFindingFilters(url);
  const engagementId = filters.engagement_id;
  const agentId = filters.agent_id;
  const severity = filters.severity;
  const paginated = url.searchParams.get("paginated") === "true";

  if (paginated) {
    const page = positiveInt(url.searchParams.get("page"), 1, 100_000);
    const pageSize = positiveInt(url.searchParams.get("page_size"), 20, 100);
    const rawSort = url.searchParams.get("sort") ?? "risk";
    const sort = VALID_SORTS.has(rawSort) ? rawSort : "risk";
    const data = await backend<{
      items?: any[];
      total?: number;
      page?: number;
      page_size?: number;
      pages?: number;
    }>("/findings", {
      token,
      query: { ...filters, sort, page, page_size: pageSize },
    });
    return NextResponse.json({
      items: (data.items ?? []).map(toUiFinding),
      total: data.total ?? 0,
      page: data.page ?? page,
      pageSize: data.page_size ?? pageSize,
      pages: data.pages ?? 1,
    });
  }

  // The backend caps page_size at 100 (422 otherwise), so page through until
  // exhausted instead of over-requesting. The safety cap bounds a pathologically
  // large engagement from fanning out unbounded on this list view.
  const PAGE_SIZE = 100;
  const MAX_PAGES = 20; // ≤ 2000 findings surfaced per list view
  const all: any[] = [];
  for (let page = 1; page <= MAX_PAGES; page++) {
    const data = await backend<{ items?: any[]; pages?: number } | any[]>("/findings", {
      token,
      query: { engagement_id: engagementId, agent_id: agentId, severity, page, page_size: PAGE_SIZE },
    });
    const items = Array.isArray(data) ? data : data.items ?? [];
    all.push(...items);
    const pages = Array.isArray(data) ? 1 : data.pages ?? 1;
    if (page >= pages || items.length < PAGE_SIZE) break;
  }
  return NextResponse.json(all.map(toUiFinding));
});

// Manual finding creation is done through the scan/import path on the backend.
export async function POST() {
  return NextResponse.json(
    { error: "Create findings via a scan or POST /engagements/{id}/scans/import on the backend." },
    { status: 501 },
  );
}
