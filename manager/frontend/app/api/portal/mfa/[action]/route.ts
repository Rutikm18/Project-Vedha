/** Customer self-service two-step sign-in (lib/mfa-account.ts), on the portal session. */
import { cookieFrom } from "../../../../../lib/backend";
import { mfaAccount } from "../../../../../lib/mfa-account";

type Ctx = { params: Promise<{ action: string }> };

export async function GET(req: Request, { params }: Ctx) {
  return mfaAccount(req, "GET", (await params).action, cookieFrom(req, "vedha_portal_token"));
}

export async function POST(req: Request, { params }: Ctx) {
  return mfaAccount(req, "POST", (await params).action, cookieFrom(req, "vedha_portal_token"));
}
