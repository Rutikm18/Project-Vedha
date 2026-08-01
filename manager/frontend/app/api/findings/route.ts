/**
 * Findings — BFF proxy to the FastAPI backend (single source of truth).
 * Replaces the in-memory `findings-store`. Returns an array of UI-shaped findings.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";
import { toUiFinding } from "../../../lib/adapters";

// Only these values are valid FastAPI enums on the backend.
const VALID_SEVERITIES = new Set(["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]);
const STATUS_TO_API: Record<string, string> = {
  OPEN: "open",
  CONFIRMED: "confirmed",
  REMEDIATED: "remediated",
  ACCEPTED: "accepted",
  FALSE_POSITIVE: "fp",
};
const VALID_SORTS = new Set(["risk", "cvss", "epss", "date"]);

function positiveInt(value: string | null, fallback: number, max: number): number {
  const parsed = Number(value);
  return Number.isInteger(parsed) && parsed > 0 ? Math.min(parsed, max) : fallback;
}

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId =
    url.searchParams.get("engagement_id") ??
    url.searchParams.get("engagementId") ??
    undefined;
  const rawSeverity = url.searchParams.get("severity");
  // Sanitize: only forward valid enum values; skip garbage to avoid 422
  const severity = rawSeverity && VALID_SEVERITIES.has(rawSeverity.toUpperCase())
    ? rawSeverity.toLowerCase()
    : undefined;
  const rawStatus = url.searchParams.get("status");
  const status = rawStatus ? STATUS_TO_API[rawStatus.toUpperCase()] : undefined;
  const paginated = url.searchParams.get("paginated") === "true";

  if (paginated) {
    const page = positiveInt(url.searchParams.get("page"), 1, 100_000);
    const pageSize = positiveInt(url.searchParams.get("page_size"), 20, 100);
    const search = url.searchParams.get("search")?.trim().slice(0, 200) || undefined;
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
      query: {
        engagement_id: engagementId,
        severity,
        status,
        search,
        detection_status: url.searchParams.get("blind") === "true" ? "missed" : undefined,
        exploit_validated: url.searchParams.get("validated") === "true" ? true : undefined,
        sla_breached: url.searchParams.get("sla_breached") === "true" ? true : undefined,
        sort,
        page,
        page_size: pageSize,
      },
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
      query: { engagement_id: engagementId, severity, page, page_size: PAGE_SIZE },
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
