/** Approve the cached AI refinement for the customer portal — BFF proxy. */
import { enc, forward } from "../../../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ id: string }> };

export async function POST(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/findings/${enc(id)}/remediation/publish`);
}
