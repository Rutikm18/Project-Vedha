import { NextResponse } from "next/server";
import { getCampaign } from "../../../../../lib/campaign-store";

// GET /api/scan/campaigns/[id] → full ProgressReporter snapshot for one campaign.
// Polled by the live campaign page; 404 until the first snapshot is ingested.
export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const snap = getCampaign(id);
  if (!snap) {
    return NextResponse.json({ error: "campaign not found" }, { status: 404 });
  }
  return NextResponse.json(snap);
}
