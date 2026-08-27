import { NextRequest, NextResponse } from "next/server";
import { listCampaigns, saveCampaign } from "../../../../lib/campaign-store";

/**
 * Network-VA campaign progress — list + ingest.
 *
 * GET  /api/scan/campaigns        → compact summaries, most-recent first.
 * POST /api/scan/campaigns        → ingest one ProgressReporter snapshot
 *                                   (the probe's campaign_progress.json). Creates
 *                                   or overwrites by campaign_id.
 *
 * File-backed (data/campaigns/) to match the app's other dev stores. Production
 * follow-up: the probe reports progress on its job heartbeat and the FastAPI
 * backend persists the snapshot — this route then proxies via withBackend, no
 * change to the page (same snapshot shape).
 */
export async function GET() {
  return NextResponse.json(listCampaigns());
}

export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Request body must be valid JSON." }, { status: 400 });
  }
  try {
    const saved = saveCampaign(body);
    return NextResponse.json({ ok: true, campaign_id: saved.campaign_id }, { status: 201 });
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "invalid snapshot" },
      { status: 400 },
    );
  }
}
