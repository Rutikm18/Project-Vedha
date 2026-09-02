/** Structured, OS-aware remediation plan — authenticated BFF proxy. */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";

const SUPPORTED_OS = new Set(["generic", "linux", "windows", "macos"]);

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
  const requestedOs = new URL(req.url).searchParams.get("os")?.toLowerCase() ?? "generic";
  const os = SUPPORTED_OS.has(requestedOs) ? requestedOs : "generic";
  try {
    const plan = await backend<unknown>(`/findings/${id}/remediation`, {
      token,
      query: { os },
    });
    return NextResponse.json(plan);
  } catch (error) {
    return fail(error);
  }
}
