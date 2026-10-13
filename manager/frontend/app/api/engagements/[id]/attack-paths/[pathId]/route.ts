import { proxyAttackGraph } from "../../../../../../lib/attack-graph-proxy";

export async function GET(req: Request, { params }: { params: Promise<{ id: string; pathId: string }> }) {
  const { id, pathId } = await params;
  return proxyAttackGraph(req, id, "attack-paths", pathId);
}
