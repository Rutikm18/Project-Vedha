import { toUiEngagement } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";
import { buildScanLaunchRequest, type ScanLaunchBody } from "./scan-launch";
import { newId } from "./uuid";

export type ScannerWorkspaceSurface = "manager" | "portal";

export function createScannerWorkspaceApi(surface: ScannerWorkspaceSurface) {
  if (surface === "manager") {
    return {
      useCases: <T>() => fetchJson<T>("/api/scan/use-cases"),
      probes: <T>() => fetchJson<T>("/api/scan/probes"),
      engagements: <T>() => fetchJson<T>("/api/engagements"),
      assets: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/assets`),
      jobs: <T>(engagementId: string) => fetchJson<T>(`/api/scan/jobs?engagement_id=${encodeURIComponent(engagementId)}`),
      job: <T>(jobId: string) => fetchJson<T>(`/api/scan/jobs/${encodeURIComponent(jobId)}`),
      launch: <T>(body: ScanLaunchBody) => fetchJson<T>("/api/scan/launch", {
        method: "POST", body: JSON.stringify(body),
      }),
      campaignProgress: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/campaign-progress`),
      rawFacts: <T>(engagementId: string, query: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/raw-facts${query}`),
      cancelJob: <T>(jobId: string) => fetchJson<T>(`/api/fleet/jobs/${encodeURIComponent(jobId)}/cancel`, { method: "POST" }),
    };
  }

  return {
    useCases: <T>() => portalApi<T>("/workspace/scan/use-cases"),
    probes: <T>() => portalApi<T>("/agents"),
    engagements: async <T>() => {
      const detail = await portalApi<unknown>("/workspace/engagement");
      return { engagements: [toUiEngagement(detail)] } as T;
    },
    assets: <T>(engagementId: string) => {
      if (!engagementId) throw new Error("Select an engagement before loading IPs.");
      return portalApi<T>("/workspace/engagement/assets");
    },
    jobs: <T>() => portalApi<T>("/workspace/scan/jobs"),
    job: <T>(jobId: string) => portalApi<T>(`/workspace/scan/jobs/${encodeURIComponent(jobId)}`),
    launch: async <T>(body: ScanLaunchBody) => {
      const request = buildScanLaunchRequest(body);
      const result = await portalApi<Record<string, unknown>>("/workspace/scan/jobs", {
        method: "POST", body: request, idempotencyKey: newId(),
      });
      return { ...result, dispatched: request } as T;
    },
    campaignProgress: <T>() => portalApi<T>("/workspace/scan/campaign-progress"),
    rawFacts: <T>(_engagementId: string, query: string) => portalApi<T>(`/workspace/scan/raw-facts${query}`),
    cancelJob: <T>(jobId: string) => portalApi<T>(`/workspace/scan/jobs/${encodeURIComponent(jobId)}/cancel`, {
      method: "POST", idempotencyKey: newId(),
    }),
  };
}
