/**
 * Findings filter mapping — browser query string → FastAPI query, shared by the
 * list BFF route and the grouped-view BFF route so the two can never disagree.
 *
 * Everything is sanitised: only valid enum values are forwarded (garbage would
 * 422 on the backend), the IP filter is IP-shaped only, free text is bounded.
 */

// Only these values are valid FastAPI enums on the backend.
const VALID_SEVERITIES = new Set(["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]);
const STATUS_TO_API: Record<string, string> = {
  OPEN: "open",
  CONFIRMED: "confirmed",
  REMEDIATED: "remediated",
  ACCEPTED: "accepted",
  FALSE_POSITIVE: "fp",
};
const VALID_VERIFICATION = new Set(["confirmed", "corroborated", "inferred", "contradicted"]);
// Exact IP or an IP prefix ("192.168.1."). Same charset the backend accepts.
const IP_FILTER = /^[0-9A-Fa-f:.]{1,45}$/;

export type BackendFindingFilters = Record<string, string | number | boolean | undefined>;

export function positiveInt(value: string | null, fallback: number, max: number): number {
  const parsed = Number(value);
  return Number.isInteger(parsed) && parsed > 0 ? Math.min(parsed, max) : fallback;
}

export function backendFindingFilters(url: URL): BackendFindingFilters {
  const p = url.searchParams;
  const rawSeverity = p.get("severity");
  const rawStatus = p.get("status");
  const ip = p.get("asset_ip")?.trim();
  const verification = p.get("verification_state");
  return {
    engagement_id: p.get("engagement_id") ?? p.get("engagementId") ?? undefined,
    agent_id: p.get("agent_id") ?? p.get("agentId") ?? undefined,
    severity: rawSeverity && VALID_SEVERITIES.has(rawSeverity.toUpperCase())
      ? rawSeverity.toLowerCase()
      : undefined,
    status: rawStatus ? STATUS_TO_API[rawStatus.toUpperCase()] : undefined,
    // "still an active exposure" (open|confirmed) — the same tracked set the
    // summary/SLA/analytics endpoints count. Sent only when asked for.
    active_only: p.get("active_only") === "true" ? true : undefined,
    search: p.get("search")?.trim().slice(0, 200) || undefined,
    asset_ip: ip && IP_FILTER.test(ip) ? ip : undefined,
    // Filter to findings a single scan touched (SCN ref, job id, or run id).
    scan: p.get("scan")?.trim().slice(0, 64) || undefined,
    // The findings page sends the backend's own names; `blind` / `validated` are
    // the older aliases. Reading only the aliases silently dropped both filters.
    detection_status: p.get("detection_status") === "missed" || p.get("blind") === "true"
      ? "missed" : undefined,
    exploit_validated: p.get("exploit_validated") === "true" || p.get("validated") === "true"
      ? true : undefined,
    needs_review: p.get("needs_review") === "true" ? true : undefined,
    verification_state: verification && VALID_VERIFICATION.has(verification) ? verification : undefined,
    sla_breached: p.get("sla_breached") === "true" ? true : undefined,
  };
}

const VALID_SORTS = new Set(["risk", "cvss", "epss", "date"]);

/**
 * The findings page's query string (UI enum names such as HIGH / FALSE_POSITIVE)
 * → a query string the FastAPI backend accepts. The portal talks to the backend
 * through a pass-through proxy, so without this its severity/status filters
 * reached FastAPI verbatim and failed enum validation (422).
 */
export function backendQueryString(query: string): string {
  const url = new URL(`http://local/?${query}`);
  const out = new URLSearchParams();
  for (const [k, v] of Object.entries(backendFindingFilters(url))) {
    if (v !== undefined && v !== "") out.set(k, String(v));
  }
  const p = url.searchParams;
  if (p.has("page")) out.set("page", String(positiveInt(p.get("page"), 1, 100_000)));
  if (p.has("page_size")) out.set("page_size", String(positiveInt(p.get("page_size"), 20, 100)));
  const sort = p.get("sort");
  if (sort && VALID_SORTS.has(sort)) out.set("sort", sort);
  return out.toString();
}

/** Browser queue state is shareable; API parameters remain a separate contract. */
export function findingChoice<T extends string>(value: string | null, choices: readonly T[], fallback: T): T {
  const normalized = value?.toUpperCase();
  return choices.find((choice) => choice.toUpperCase() === normalized) ?? fallback;
}

export function findingPage(value: string | null): number {
  const page = Number(value);
  return Number.isSafeInteger(page) && page > 0 ? page : 1;
}

export function findingFlag(value: string | null): boolean {
  return value === "true" || value === "1";
}

export function writeFindingParam(key: string, value: string | null) {
  const url = new URL(window.location.href);
  if (value === null || value === "") url.searchParams.delete(key);
  else url.searchParams.set(key, value);
  // Preserve Next's history metadata and publish to the existing external store.
  window.history.replaceState(window.history.state, "", `${url.pathname}${url.search}${url.hash}`);
  window.dispatchEvent(new PopStateEvent("popstate"));
}
