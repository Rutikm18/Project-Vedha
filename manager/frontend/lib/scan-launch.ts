import { parseScanIp } from "./scan-target";

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
  uc_deep_port_sweep: "discovery",
};

/** The capability a Deep scan runs: every TCP port plus the full assessment. */
export const DEEP_SCAN_UC = "uc_deep_port_sweep";

/** Every-port capabilities. They cover exactly ONE host — the manager enforces the
 *  same rule (422) — so the client refuses to even build a request for several. */
export const FULL_PORT_USE_CASES: readonly string[] = ["uc_full_port_audit", "uc_deep_port_sweep"];

export const ONE_HOST_MESSAGE = "A deep scan covers exactly one host — enter a single IP address.";

/** True when `value` is one IP (a /32 or /128 suffix is allowed), not a list or range. */
export function isSingleHost(value: unknown): boolean {
  return parseScanIp(value) !== null;
}

/** The launcher body for a single-asset Deep scan, from either Scanner.
 *  Portal: the manager pins the use case, preset and target and charges the
 *  customer's plan, so the body only names the deep intent (`scan_mode`).
 *  Operator: a plain enqueue of the deep use case on that one host — "aggressive"
 *  is the manager's alias for the deep preset — and nothing is charged. */
export function buildDeepScanLaunch(opts: {
  engagementId: string;
  ip: string;
  probeId?: string;
  audience: "portal" | "operator";
}): ScanLaunchBody {
  if (!isSingleHost(opts.ip)) throw new Error(ONE_HOST_MESSAGE);
  const body: ScanLaunchBody = {
    engagement_id: opts.engagementId, use_case_id: DEEP_SCAN_UC, targets: [opts.ip],
    intensity: "aggressive",
  };
  if (opts.probeId) body.preferred_agent_id = opts.probeId;
  if (opts.audience === "portal") body.params = { scan_mode: "deep" };
  return body;
}

/** Convert the UI launcher contract into the manager's canonical enqueue
 * contract. Both operator and portal transports call this exact function. */
export function buildScanLaunchRequest(body: ScanLaunchBody) {
  if (FULL_PORT_USE_CASES.includes(body.use_case_id)
      && !(Array.isArray(body.targets) && body.targets.length === 1 && isSingleHost(body.targets[0]))) {
    throw new Error(ONE_HOST_MESSAGE);
  }
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
