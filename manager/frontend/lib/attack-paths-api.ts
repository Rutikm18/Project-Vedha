import { fetchJson } from "./fetcher";
import type { Analysis, PathDetail, PathList, ZoneView } from "./attack-paths";

const base = (engagementId: string) => `/api/engagements/${encodeURIComponent(engagementId)}`;

/** Browser-side calls for the attack-paths page. Each goes through the BFF, which
 *  forwards to FastAPI with the operator's session. */
export const attackPathsApi = {
  /** The stored list. A never-computed engagement is computed once by the backend;
   *  `refresh` forces a recompute (and rewrites the stored paths). */
  list: (engagementId: string, opts: { refresh?: boolean; pageSize?: number } = {}) => {
    const q = new URLSearchParams({ page_size: String(opts.pageSize ?? 50) });
    if (opts.refresh) q.set("refresh", "true");
    return fetchJson<PathList>(`${base(engagementId)}/attack-paths?${q}`);
  },
  detail: (engagementId: string, pathId: string) =>
    fetchJson<PathDetail>(`${base(engagementId)}/attack-paths/${encodeURIComponent(pathId)}`),
  /** Choke points, coverage, freshness and why-empty as of the last computation. Read-only. */
  analysis: (engagementId: string) => fetchJson<Analysis>(`${base(engagementId)}/attack-path-analysis`),
  /** The stored routes grouped into the subnets they cross. Read-only. */
  zones: (engagementId: string) => fetchJson<ZoneView>(`${base(engagementId)}/attack-path-zones`),
};
