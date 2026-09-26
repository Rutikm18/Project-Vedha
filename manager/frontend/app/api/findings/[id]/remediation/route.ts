/** Contextual remediation plan (asset-grounded KB or cached AI refinement) — BFF proxy.
 *  `os` is optional: the backend defaults to the OS the scan detected. */
import { enc, forward } from "../../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ id: string }> };

export async function GET(req: Request, { params }: Ctx) {
  const { id } = await params;
  return forward(req, `/findings/${enc(id)}/remediation`);
}
