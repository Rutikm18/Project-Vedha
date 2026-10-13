import { proxyAttackGraph } from "../../../../../../lib/attack-graph-proxy";

export async function GET(req: Request, { params }: { params: Promise<{ id: string; assetId: string }> }) {
  const { id, assetId } = await params;
  return proxyAttackGraph(req, id, "blast-radius", assetId);
}
