import { NextRequest, NextResponse } from "next/server";
import { startOpenVASScan } from "../../../../lib/openvas-client";
import { withVerifiedLocalScanner } from "../../../../lib/with-backend";
import { isScopeAllowed } from "../../../../lib/permissions-store";
import { validateOpenVASScanRequest } from "../../../../lib/scanner-request-validation";

export const POST = withVerifiedLocalScanner(async (req: NextRequest, { user }) => {
  const body = await req.json().catch(() => null);
  const validated = validateOpenVASScanRequest(body, {
    gvmHost: process.env.OPENVAS_HOST ?? "openvas",
    gvmPort: Number(process.env.OPENVAS_PORT ?? "9390"),
    gvmUser: process.env.OPENVAS_USER ?? "admin",
  });

  if (validated.ok === false) {
    return NextResponse.json(
      { error: validated.error },
      { status: validated.source === "configuration" ? 503 : 400 },
    );
  }
  const {
    targets,
    scanConfig,
    gvmHost,
    gvmPort,
    gvmUser,
    createFindings,
  } = validated.value;

  if (!user.email) {
    return NextResponse.json(
      { error: "Local scanner routes require a user-backed access token." },
      { status: 403 },
    );
  }
  const denied = targets.filter((target) => !isScopeAllowed(user.email!, target));
  if (denied.length > 0) {
    return NextResponse.json(
      { error: `Targets out of your permitted scope: ${denied.join(", ")}` },
      { status: 403 },
    );
  }

  const gvmPassword = process.env.OPENVAS_PASSWORD ?? "";
  if (!gvmPassword) {
    return NextResponse.json({ error: "OPENVAS_PASSWORD environment variable not set." }, { status: 503 });
  }

  const { taskId } = await startOpenVASScan({
    targets,
    gvmHost,
    gvmPort,
    gvmUser,
    gvmPassword,
    scanConfig,
    ownerTenantId: user.tenant_id,
    ownerUserId: user.user_id,
  });

  return NextResponse.json({
    taskId,
    status: "queued",
    progress: 0,
    message: `OpenVAS scan queued. Poll GET /api/scan/openvas/${taskId} for status.`,
    createFindings,
  });
});
