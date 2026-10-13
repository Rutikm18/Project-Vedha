/**
 * Liveness for the container health check (manager/docker-compose.yml). It says
 * only that this server answers; it calls nothing and reveals nothing.
 */
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export function GET() {
  return NextResponse.json({ status: "ok" }, { headers: { "Cache-Control": "no-store" } });
}
