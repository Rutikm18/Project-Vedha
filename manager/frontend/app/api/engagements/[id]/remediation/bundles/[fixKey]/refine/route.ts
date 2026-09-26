/** Refine a fix bundle with AI — BFF proxy. */
import { enc, forward } from "../../../../../../../../lib/operator-proxy";

export const maxDuration = 120;
type Ctx = { params: Promise<{ id: string; fixKey: string }> };

export async function POST(req: Request, { params }: Ctx) {
  const { id, fixKey } = await params;
  return forward(req, `/engagements/${enc(id)}/remediation/bundles/${enc(fixKey)}/refine`);
}
