/**
 * Customers — BFF proxy. Lists every provisioned customer login for the tenant
 * (operator "Customers" dashboard). Provisioning / reset / disable reuse the
 * per-engagement customer-access proxy at /api/engagements/[id]/customer-access.
 */
import { NextResponse } from "next/server";
import { backend } from "../../../lib/backend";
import { withBackend } from "../../../lib/with-backend";

export const GET = withBackend(async (_req, { token }) => {
  const customers = await backend<unknown[]>("/customers", { token });
  return NextResponse.json(customers ?? []);
});
