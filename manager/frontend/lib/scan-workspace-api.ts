import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";
import {
  toAgentJobRequest,
  type ScanLaunchBody,
} from "./scan-launch";

export { toAgentJobRequest } from "./scan-launch";
export type { ScanLaunchBody } from "./scan-launch";

export type ScannerSurface = "manager" | "portal";

export function createScannerApi(surface: ScannerSurface) {
  if (surface === "manager") {
    return {
      useCases: <T>() => fetchJson<T>("/api/scan/use-cases"),
      probes: <T>() => fetchJson<T>("/api/scan/probes"),
      engagements: <T>() => fetchJson<T>("/api/engagements"),
      job: <T>(id: string) => fetchJson<T>(`/api/scan/jobs/${id}`),
      jobs: <T>(engagementId: string) => fetchJson<T>(
        `/api/scan/jobs?engagement_id=${encodeURIComponent(engagementId)}`,
      ),
      launch: <T>(body: ScanLaunchBody) => fetchJson<T>("/api/scan/launch", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    };
  }

  return {
    useCases: <T>() => portalApi<T>("/workspace/use-cases"),
    probes: <T>() => portalApi<T>("/workspace/probes"),
    engagements: async <T>() => {
      const engagement = await portalApi<{
        id: string;
        name: string;
        status: string;
        scope_cidrs?: string[];
        excluded_cidrs?: string[];
      }>("/engagement");
      return {
        engagements: [{
          id: engagement.id,
          name: engagement.name,
          status: engagement.status,
          scopeCidrs: engagement.scope_cidrs ?? [],
          excludedCidrs: engagement.excluded_cidrs ?? [],
        }],
      } as T;
    },
    job: <T>(id: string) => portalApi<T>(`/workspace/jobs/${id}`),
    jobs: <T>() => portalApi<T>("/workspace/jobs"),
    launch: async <T>(body: ScanLaunchBody) => {
      const dispatched = toAgentJobRequest(body);
      const result = await portalApi<Record<string, unknown>>("/workspace/jobs", {
        method: "POST",
        body: dispatched,
        idempotencyKey: crypto.randomUUID(),
      });
      return { ...result, dispatched } as T;
    },
  };
}
