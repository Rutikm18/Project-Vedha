import { NextRequest, NextResponse } from "next/server";
import { getTask } from "../../../../../lib/openvas-client";
import { withVerifiedLocalScanner } from "../../../../../lib/with-backend";

export const GET = withVerifiedLocalScanner<{ taskId: string }>((
  _req: NextRequest,
  { user },
  params,
) => {
  const taskId = params?.taskId;
  if (!taskId) {
    return NextResponse.json({ error: "Task id is required." }, { status: 400 });
  }
  const task = getTask(taskId);

  if (!task || task.ownerTenantId !== user.tenant_id) {
    return NextResponse.json({ error: "Task not found." }, { status: 404 });
  }

  return NextResponse.json({
    taskId: task.taskId,
    status: task.status,
    progress: task.progress,
    findings: task.findings,
    findingCount: task.findings.length,
    error: task.error,
    stats: {
      critical: task.findings.filter((f) => f.severity === "CRITICAL").length,
      high:     task.findings.filter((f) => f.severity === "HIGH").length,
      medium:   task.findings.filter((f) => f.severity === "MEDIUM").length,
      low:      task.findings.filter((f) => f.severity === "LOW").length,
    },
  });
});
