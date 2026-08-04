import { NextRequest, NextResponse } from "next/server";
import { backend } from "../../../../lib/backend";
import { withBackend } from "../../../../lib/with-backend";

interface LaunchBody {
  engagement_id: string;
  use_case_id: string;
  targets?: string[];                // per-job scope (blank = engagement scope)
  excluded_cidrs?: string[];         // per-job carve-outs subtracted from scope
  // Scan-intensity preset (nmap-style timing). Resolved to rate/concurrency/timeout here.
  intensity?: "stealth" | "normal" | "aggressive";
  passive_listen_seconds?: number;   // OT passive capture window
  recheck_hours?: number;            // re-scan delta window
  preferred_agent_id?: string;       // operator-pinned probe (blank = any compatible)
  params?: Record<string, unknown>;
}

// Scan-intensity presets — the single offensive-security knob operators reason
// about. Each maps to the rate/concurrency/timeout tuple the probe engine clamps
// and applies. Mirrors nmap timing templates (T2 / T3-default / T4).
const INTENSITY_PRESETS: Record<string, { rate: number; concurrency: number; timeout: number; disc_timeout: number }> = {
  stealth:    { rate: 50,  concurrency: 20,  timeout: 4.0, disc_timeout: 2.0 },
  normal:     { rate: 200, concurrency: 100, timeout: 3.0, disc_timeout: 1.5 },
  aggressive: { rate: 600, concurrency: 300, timeout: 2.0, disc_timeout: 1.0 },
};

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
    uc_snmp_exposure:        "discovery",
  };

  const job_type = JOB_TYPE_MAP[body.use_case_id] ?? "discovery";

  // Merge caller-supplied targets into params so probe can read them.
  const params: Record<string, unknown> = { ...(body.params ?? {}) };
  if (body.targets?.length) {
    params.targets = body.targets;
    params.scope_cidrs = body.targets;
  }

  // ── Excluded scope (per-job carve-outs) ───────────────────────────────────
  // The probe merges these with the engagement's authoritative exclusions and
  // ScopeGuard subtracts them from the allowlist — packets never reach them.
  if (body.excluded_cidrs?.length) {
    params.excluded_cidrs = body.excluded_cidrs;
  }

  // ── Resolve scan intensity → engine tuning numbers ────────────────────────
  const preset = INTENSITY_PRESETS[body.intensity ?? "normal"] ?? INTENSITY_PRESETS.normal;
  params.intensity    = body.intensity ?? "normal";   // provenance
  params.rate         = preset.rate;
  params.concurrency  = preset.concurrency;
  params.timeout      = preset.timeout;
  params.disc_timeout = preset.disc_timeout;

  // ── OT passive listen window (only meaningful for the OT use-case) ────────
  if (typeof body.passive_listen_seconds === "number" && body.passive_listen_seconds > 0) {
    params.passive_listen_seconds = body.passive_listen_seconds;
  }

  // ── Re-scan delta window ──────────────────────────────────────────────────
  if (typeof body.recheck_hours === "number" && body.recheck_hours >= 0) {
    params.recheck_hours = body.recheck_hours;
  }

  // Operator-pinned probe (optional). Empty/undefined = any compatible probe claims it.
  if (body.preferred_agent_id) {
    params.preferred_agent_id = body.preferred_agent_id;
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

  // Echo back the exact non-secret request the probe will execute.
  const dispatched: Record<string, unknown> = {
    engagement_id: body.engagement_id,
    job_type,
    use_case_id: body.use_case_id,
    params,
  };

  return NextResponse.json({ ...result, dispatched }, { status: 201 });
});
