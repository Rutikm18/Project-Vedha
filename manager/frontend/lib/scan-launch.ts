export interface ScanLaunchBody {
  engagement_id: string;
  use_case_id: string;
  targets?: string[];
  excluded_cidrs?: string[];
  intensity?: "stealth" | "normal" | "aggressive";
  passive_listen_seconds?: number;
  recheck_hours?: number;
  preferred_agent_id?: string;
  params?: Record<string, unknown>;
}

const INTENSITY_PRESETS: Record<string, { rate: number; concurrency: number; timeout: number; disc_timeout: number }> = {
  stealth: { rate: 50, concurrency: 20, timeout: 4.0, disc_timeout: 2.0 },
  normal: { rate: 200, concurrency: 100, timeout: 3.0, disc_timeout: 1.5 },
  aggressive: { rate: 600, concurrency: 300, timeout: 2.0, disc_timeout: 1.0 },
};

const JOB_TYPE_MAP: Record<string, string> = {
  uc_discovery_only: "discovery",
  uc_device_inventory: "discovery",
  uc_full_assessment: "discovery",
  uc_external_web_triage: "discovery",
  uc_db_exposure: "discovery",
  uc_windows_estate: "lateral",
  uc_ot_passive: "discovery",
  uc_ai_endpoint_sweep: "discovery",
  uc_rescan_delta: "discovery",
  uc_network_va: "discovery",
  uc_iot_device_survey: "discovery",
  uc_web_app_triage: "discovery",
  uc_udp_service_exposure: "discovery",
  uc_snmp_exposure: "discovery",
  uc_full_port_audit: "discovery",
  uc_exposure_matrix: "discovery",
};

/** Convert the UI launcher contract into the manager's canonical enqueue
 * contract. Both operator and portal transports call this exact function. */
export function buildScanLaunchRequest(body: ScanLaunchBody) {
  const job_type = JOB_TYPE_MAP[body.use_case_id] ?? "discovery";
  const params: Record<string, unknown> = { ...(body.params ?? {}) };
  if (body.targets?.length) {
    params.targets = body.targets;
    params.scope_cidrs = body.targets;
  }
  if (body.excluded_cidrs?.length) params.excluded_cidrs = body.excluded_cidrs;

  const preset = INTENSITY_PRESETS[body.intensity ?? "normal"] ?? INTENSITY_PRESETS.normal;
  params.intensity = body.intensity ?? "normal";
  params.rate = preset.rate;
  params.concurrency = preset.concurrency;
  params.timeout = preset.timeout;
  params.disc_timeout = preset.disc_timeout;

  if (typeof body.passive_listen_seconds === "number" && body.passive_listen_seconds > 0) {
    params.passive_listen_seconds = body.passive_listen_seconds;
  }
  if (typeof body.recheck_hours === "number" && body.recheck_hours >= 0) {
    params.recheck_hours = body.recheck_hours;
  }
  if (body.preferred_agent_id) params.preferred_agent_id = body.preferred_agent_id;

  return {
    engagement_id: body.engagement_id,
    job_type,
    use_case_id: body.use_case_id,
    params,
  };
}
