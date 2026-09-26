/** Per-engagement SLA policy (overrides the tenant policy) — BFF proxy. */
import { enc, forward } from "../../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ id: string }> };

export async function GET(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/engagements/${enc(id)}/sla-policy`);
}
export async function PUT(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/engagements/${enc(id)}/sla-policy`);
}
export async function DELETE(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/engagements/${enc(id)}/sla-policy`);
}
