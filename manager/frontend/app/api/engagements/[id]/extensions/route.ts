/** Deadline-extension requests for an engagement (?status=) — BFF proxy. */
import { enc, forward } from "../../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ id: string }> };

export async function GET(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/engagements/${enc(id)}/extensions`);
}
