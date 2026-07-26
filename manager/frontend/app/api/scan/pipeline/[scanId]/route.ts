import { NextRequest, NextResponse } from "next/server";
import { getPipeline } from "../../../../../lib/scan-pipeline";
import { withVerifiedLocalScanner } from "../../../../../lib/with-backend";

export const GET = withVerifiedLocalScanner<{ scanId: string }>(async (
  _req: NextRequest,
  { user },
  params,
) => {
  const { scanId } = params!;
  const state = getPipeline(scanId);

  if (!state || state.ownerTenantId !== user.tenant_id) {
    return NextResponse.json({ error: "Pipeline scan not found." }, { status: 404 });
  }

  return NextResponse.json({
    scanId: state.scanId,
    status: state.status,
    profile: state.profile,
    targets: state.targets,
    stages: state.stages,
    overallProgress: state.overallProgress,
    startedAt: state.startedAt,
    completedAt: state.completedAt,
    totalFindings: state.totalFindings,
    findingIds: state.findingIds,
    context: state.context,
  });
});
