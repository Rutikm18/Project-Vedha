/** Approve or reject a deadline-extension request — BFF proxy. */
import { NextResponse } from "next/server";
import { enc, forward } from "../../../../../lib/operator-proxy";

type Ctx = { params: Promise<{ id: string; action: string }> };

export async function POST(req: Request, { params }: Ctx) {
  const { id, action } = await params;
  if (action !== "approve" && action !== "reject") {
    return NextResponse.json({ error: "Unknown action" }, { status: 404 });
  }
  return forward(req, `/extensions/${enc(id)}/${action}`);
}
