/**
 * Detection-explain — BFF proxy to FastAPI.
 *   GET → /engagements/{id}/detection-explain[?rule_id=…]
 * Per-rule detection verdicts (finding_exists / evaluated_clean / schema_drift /
 * no_evidence_collected / rule_error) — the machine-readable answer to
 * "the scripts catch it but the manager doesn't". Operator-gated on the backend.
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";

function fail(e: unknown) {
  const status = e instanceof BackendError ? e.status : 500;
  return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
}

export async function GET(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  const ruleId = new URL(req.url).searchParams.get("rule_id");
  const query = ruleId ? { rule_id: ruleId } : undefined;
  try {
    const data = await backend<unknown>(`/engagements/${id}/detection-explain`, { token, query });
    return NextResponse.json(data);
  } catch (e) {
    return fail(e);
  }
}
