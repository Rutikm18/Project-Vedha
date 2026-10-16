/** The full working of a finding risk score and P0-P5 priority — authenticated BFF proxy. */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";

function fail(error: unknown) {
  const status = error instanceof BackendError ? error.status : 500;
  return NextResponse.json(
    { error: (error as Error)?.message ?? "backend error" },
    { status },
  );
}

export async function GET(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  try {
    const explanation = await backend<unknown>(`/findings/${id}/risk-explanation`, { token });
    return NextResponse.json(explanation);
  } catch (error) {
    return fail(error);
  }
}
