import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

interface LaunchBody {
  engagement_id: string;
  use_case_id: string;
  targets?: string[];
  params?: Record<string, unknown>;
}

// POST /api/scan/launch → proxies to manager POST /agents/jobs
// Enqueues a scan job that the probe picks up on its next poll cycle.
export const POST = withBackend(async (req: NextRequest, { token }) => {
  const body = await req.json() as LaunchBody;

  if (!body?.engagement_id) {
    return NextResponse.json({ error: "engagement_id is required" }, { status: 400 });
  }
  if (!body?.use_case_id) {
    return NextResponse.json({ error: "use_case_id is required" }, { status: 400 });
  }

  // Map use_case_id → job_type. All probe-executable jobs are "discovery" type
  // on the manager side; the use_case_id drives what the probe actually runs.
  const JOB_TYPE_MAP: Record<string, string> = {
    uc_discovery_only:       "discovery",
    uc_full_assessment:      "discovery",
    uc_external_web_triage:  "discovery",
    uc_db_exposure:          "discovery",
    uc_windows_estate:       "lateral",
    uc_ot_passive:           "discovery",
    uc_ai_endpoint_sweep:    "discovery",
    uc_rescan_delta:         "discovery",
    uc_iot_device_survey:    "discovery",
    uc_web_app_triage:       "discovery",
    uc_udp_service_exposure: "discovery",
  };

  const job_type = JOB_TYPE_MAP[body.use_case_id] ?? "discovery";

  // Merge caller-supplied targets into params so probe can read them.
  const params: Record<string, unknown> = { ...(body.params ?? {}) };
  if (body.targets?.length) {
    params.targets = body.targets;
    params.scope_cidrs = body.targets;
  }

  const result = await backend<{ job_id: string; status: string; use_case_id: string }>("/agents/jobs", {
    token,
    method: "POST",
    body: {
      engagement_id: body.engagement_id,
      job_type,
      use_case_id: body.use_case_id,
      params,
    },
  });

  return NextResponse.json(result, { status: 201 });
});
