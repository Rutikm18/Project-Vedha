/**
 * Attack-path BFF routes — one place that turns `/api/engagements/{id}/…` into the
 * FastAPI call, so every route validates, forwards and fails the same way.
 *
 * Path parameters are interpolated into a backend URL, so each must be a UUID: an
 * id such as `../../admin` would otherwise rewrite the request path. Only the query
 * keys a route lists are forwarded; nothing else the browser sent reaches FastAPI.
 */
import { NextResponse, type NextRequest } from "next/server";
import { backend } from "./backend";
import { withBackend } from "./with-backend";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function isUuid(value: unknown): value is string {
  return typeof value === "string" && UUID.test(value);
}

type Params = Record<string, string | undefined>;

export interface ProxySpec {
  /** Backend path for these (validated) params, e.g. `/engagements/${id}/chokepoints`. */
  path: (p: Params) => string;
  /** Route params that must be UUIDs. */
  uuids: string[];
  /** Query keys forwarded to the backend, with the check each value must pass. */
  query?: Record<string, (value: string) => boolean>;
}

const isBoolean = (v: string) => v === "true" || v === "false";
const isPositiveInt = (max: number) => (v: string) => /^\d{1,4}$/.test(v) && Number(v) >= 1 && Number(v) <= max;

export const QUERY = { boolean: isBoolean, uuid: isUuid, positiveInt: isPositiveInt } as const;

export function engagementGet(spec: ProxySpec) {
  return withBackend<Params>(async (req: NextRequest, { token }, params) => {
    const p = params ?? {};
    for (const key of spec.uuids) {
      if (!isUuid(p[key])) {
        return NextResponse.json({ error: `Invalid ${key}` }, { status: 400 });
      }
    }
    const query: Record<string, string> = {};
    for (const [key, valid] of Object.entries(spec.query ?? {})) {
      const value = req.nextUrl.searchParams.get(key);
      if (value === null) continue;
      if (!valid(value)) {
        return NextResponse.json({ error: `Invalid ${key}` }, { status: 400 });
      }
      query[key] = key === "refresh" ? "false" : value;
    }
    const data = await backend<unknown>(spec.path(p), { token, query });
    return NextResponse.json(data, { headers: { "Cache-Control": "no-store" } });
  });
}
