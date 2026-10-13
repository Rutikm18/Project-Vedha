import { proxyAttackGraph } from "../../../../../lib/attack-graph-proxy";

export async function GET(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return proxyAttackGraph(req, id, "chokepoints");
}
