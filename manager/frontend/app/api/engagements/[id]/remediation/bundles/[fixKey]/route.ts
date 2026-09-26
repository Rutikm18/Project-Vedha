/** One fix bundle with its per-host checklist — BFF proxy. */
import { enc, forward } from "../../../../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ id: string; fixKey: string }> };

export async function GET(req: Request, { params }: Ctx) {
  const { id, fixKey } = await params;
  return forward(req, `/engagements/${enc(id)}/remediation/bundles/${enc(fixKey)}`);
}
