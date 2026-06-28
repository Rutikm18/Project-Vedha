/**
 * Import a probe scan file → detection + attack graph — BFF proxy to FastAPI.
 *   POST (multipart/form-data, field `file`) → /engagements/{id}/scans/import-facts
 *
 * Unlike the JSON `backend()` helper, this forwards the raw multipart body so the
 * uploaded .json/.jsonl file streams through to FastAPI unchanged.
 */
import { NextResponse } from "next/server";
import { bearerFrom } from "../../../../../lib/backend";

const BASE = (process.env.BACKEND_INTERNAL_URL ?? "http://localhost:18080").replace(/\/$/, "");

export async function POST(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;

  const form = await req.formData();
  const file = form.get("file");
  if (!(file instanceof File)) {
    return NextResponse.json({ error: "No file uploaded (field 'file')." }, { status: 400 });
  }

  const upstream = new FormData();
  upstream.append("file", file, file.name);

  const res = await fetch(`${BASE}/engagements/${id}/scans/import-facts`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: upstream,
    cache: "no-store",
  });

  const text = await res.text();
  let data: unknown = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text };
  }
  return NextResponse.json(data, { status: res.status });
}
