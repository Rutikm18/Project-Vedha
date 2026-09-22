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

  // Name the intent and stop there. The probe owns the envelope
  // (probe/workflow/intensity.py): it resolves the preset, then lets any
  // explicit param above still win and clamps the result. Sending a rate here
  // would discard the preset's tuning while keeping its port breadth.
  params.intensity = body.intensity ?? "normal";

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
