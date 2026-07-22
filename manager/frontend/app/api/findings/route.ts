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

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId =
    url.searchParams.get("engagement_id") ??
    url.searchParams.get("engagementId") ??
    undefined;
  const rawSeverity = url.searchParams.get("severity");
  // Sanitize: only forward valid enum values; skip garbage to avoid 422
  const severity = rawSeverity && VALID_SEVERITIES.has(rawSeverity.toUpperCase())
    ? rawSeverity.toUpperCase()
    : undefined;

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
