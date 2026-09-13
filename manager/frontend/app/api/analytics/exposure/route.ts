/**
 * Exposure analytics — BFF proxy to FastAPI GET /analytics/exposure.
 * Returns protocol-risk + zone-health arrays already in the UI's shape
 * ({name,value} / {name,score}), consumed by ExposureCards (MeterRow).
 */
import { NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

interface Exposure {
  protocols: {
    name: string;
    /** Worst severity attributable to this service; null = nothing found on it. */
    severity: string | null;
    /** Severity weight 0-100 — meter length only, never the band label. */
    value: number;
    findings: number;
    assets: number;
  }[];
  zones: { name: string; score: number; assets: number; affected: number }[];
  /** Open findings that name no port, so they cannot be charged to a protocol. */
  unattributed_findings: number;
}

export const GET = withBackend(async (req, { token }) => {
  const url = new URL(req.url);
  const engagementId = url.searchParams.get("engagement_id") ?? undefined;
  const data = await backend<Exposure>("/analytics/exposure", {
    token,
    query: { engagement_id: engagementId },
  });
  return NextResponse.json({
    protocols: data.protocols ?? [],
    zones: data.zones ?? [],
    unattributedFindings: data.unattributed_findings ?? 0,
  });
});
