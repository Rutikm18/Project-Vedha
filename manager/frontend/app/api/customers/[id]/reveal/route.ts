/**
 * Customer login password reveal — BFF proxy.
 *   GET → /customers/{id}/reveal   (operator-only; the backend audits every reveal)
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";

export async function GET(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  try {
    const data = await backend<{ id: string; email: string; password: string | null }>(
      `/customers/${id}/reveal`, { token });
    return NextResponse.json(data);
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 500;
    return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
  }
}
