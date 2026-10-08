/** Operator self-service two-step sign-in (lib/mfa-account.ts). */
import { bearerFrom } from "../../../../../lib/backend";
import { mfaAccount } from "../../../../../lib/mfa-account";

type Ctx = { params: Promise<{ action: string }> };

export async function GET(req: Request, { params }: Ctx) {
  return mfaAccount(req, "GET", (await params).action, bearerFrom(req));
}

export async function POST(req: Request, { params }: Ctx) {
  return mfaAccount(req, "POST", (await params).action, bearerFrom(req));
}
