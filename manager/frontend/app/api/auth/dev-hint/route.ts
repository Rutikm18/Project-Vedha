import { NextResponse } from "next/server";

// TESTING-ONLY credential hint for the login page autofill.
//
// Returns the seeded admin email + password so a testing deployment can
// pre-fill the login form. This is a deliberate convenience for the no-TLS
// testing path (make aws-up-ui) and is protected by TWO independent guards:
//
//   1. DEV_LOGIN_HINT must be explicitly "1"/"true" (default off).
//   2. APP_ENV must NOT be "production" — a hard block so this can never leak
//      even if the flag is somehow left on in a real deploy.
//
// deploy/aws/install.sh (production) never sets DEV_LOGIN_HINT and always writes
// APP_ENV=production, so both guards fail closed there.
export const dynamic = "force-dynamic";

export async function GET() {
  const enabled =
    process.env.DEV_LOGIN_HINT === "1" || process.env.DEV_LOGIN_HINT === "true";
  const isProduction = process.env.APP_ENV === "production";

  if (isProduction || !enabled) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }

  const email = process.env.SEED_ADMIN_EMAIL || "";
  const password = process.env.SEED_ADMIN_PASSWORD || "";
  if (!email || !password) {
    return NextResponse.json({ error: "hint unavailable" }, { status: 404 });
  }

  return NextResponse.json({ email, password, testing: true });
}
