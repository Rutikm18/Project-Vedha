/** Refine the plan with AI (gateway-routed on the backend) — BFF proxy. */
import { enc, forward } from "../../../../../../lib/operator-proxy";

export const maxDuration = 120;
type Ctx = { params: Promise<{ id: string }> };

export async function POST(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/findings/${enc(id)}/remediation/refine`);
}
