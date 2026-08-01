import { NextResponse } from "next/server";
import { backend, bearerFrom } from "../../../../lib/backend";

const required = {
  email: ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "SMTP_FROM"],
  slack: ["SLACK_WEBHOOK_URL"],
  jira: ["JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"],
} as const;

function readiness(keys: readonly string[]) {
  const missing = keys.filter((key) => !process.env[key]?.trim());
  return { configured: missing.length === 0, missing };
}

export async function GET(req: Request) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  let apiReachable = false;
  try {
    await backend("/health", { token });
    apiReachable = true;
  } catch {
    apiReachable = false;
  }

  const production = process.env.NODE_ENV === "production";
  const cookieSecure = process.env.AUTH_COOKIE_SECURE === "true"
    || (process.env.AUTH_COOKIE_SECURE !== "false" && production);

  return NextResponse.json({
    checkedAt: new Date().toISOString(),
    environment: production ? "production" : "development",
    apiReachable,
    cookieSecure,
    integrations: {
      email: readiness(required.email),
      slack: readiness(required.slack),
      jira: readiness(required.jira),
    },
  }, { headers: { "Cache-Control": "no-store" } });
}
