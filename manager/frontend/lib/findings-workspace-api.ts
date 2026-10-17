import {
  mapAsset, mapCompareResult, mapFindingGroupPage, mapScanOption, toApiFindingPatch, toUiFinding,
  type ApiFindingAsset, type ApiFindingGroupPage, type ApiScanOption,
} from "./adapters";
export type { FindingAssetOption, ScanOption } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";
import { backendQueryString } from "./findings-query";
import { newId } from "./uuid";

export type FindingsWorkspaceSurface = "manager" | "portal";

export function portalFindingAssistantHref(findingId: string): string {
  return `/portal/assistant?finding=${encodeURIComponent(findingId)}`;
}

interface ApiFindingPage {
  items?: unknown[];
  total?: number;
  page?: number;
  page_size?: number;
  pages?: number;
}

interface ApiFindingSummary {
  total?: number;
  open_total?: number;
  critical_open?: number;
  high_open?: number;
  medium_open?: number;
  low_open?: number;
  info_open?: number;
  validated?: number;
  blind?: number;
  average_risk?: number;
}

function mapSummary(summary: ApiFindingSummary) {
  return {
    total: summary.total ?? 0,
    openTotal: summary.open_total ?? 0,
    criticalOpen: summary.critical_open ?? 0,
    highOpen: summary.high_open ?? 0,
    mediumOpen: summary.medium_open ?? 0,
    lowOpen: summary.low_open ?? 0,
    infoOpen: summary.info_open ?? 0,
    validated: summary.validated ?? 0,
    blind: summary.blind ?? 0,
    averageRisk: summary.average_risk ?? 0,
  };
}

/** One UI tree, two transports. Portal data remains engagement-scoped server-side. */
export function createFindingsWorkspaceApi(surface: FindingsWorkspaceSurface) {
  if (surface === "manager") {
    return {
      list: <T>(query: string) => fetchJson<T>(`/api/findings?${query}`),
      findingIds: <T>(query: string) => fetchJson<T>(`/api/findings/ids?${query}`),
      groups: <T>(query: string) => fetchJson<T>(`/api/findings/groups?${query}`),
      summary: <T>(query: string) => fetchJson<T>(`/api/findings/summary${query ? `?${query}` : ""}`),
      assets: <T>(query: string) => fetchJson<T>(`/api/findings/assets${query ? `?${query}` : ""}`),
      scans: <T>(query: string) => fetchJson<T>(`/api/findings/scans${query ? `?${query}` : ""}`),
      compare: <T>(query: string) => fetchJson<T>(`/api/findings/compare?${query}`),
      engagements: <T>() => fetchJson<T>("/api/engagements"),
      agents: <T>() => fetchJson<T>("/api/agents/register"),
      engagement: <T>(id: string) => fetchJson<T>(`/api/engagements/${id}`),
      detail: <T>(id: string) => fetchJson<T>(`/api/findings/${id}`),
      update: <T>(id: string, patch: unknown) => fetchJson<T>(`/api/findings/${id}`, {
        method: "PUT", body: JSON.stringify(patch),
      }),
      reopen: <T>(id: string, reason: string) => fetchJson<T>(`/api/findings/${id}/reopen`, {
        method: "POST", body: JSON.stringify({ reason }),
      }),
      remediation: <T>(id: string, os: string) => fetchJson<T>(`/api/findings/${id}/remediation?os=${os}`),
      events: <T>(id: string) => fetchJson<T>(`/api/findings/${id}/events`),
      riskExplanation: <T>(id: string) => fetchJson<T>(`/api/findings/${id}/risk-explanation`),
      obligations: <T>(id: string) => fetchJson<T>(`/api/findings/${id}/obligations`),
      complianceBrief: <T>(id: string) => fetchJson<T>(`/api/findings/${id}/compliance-brief`, { method: "POST" }),
    };
  }

  return {
    list: async <T>(query: string) => {
      const page = await portalApi<ApiFindingPage>(`/workspace/findings?${backendQueryString(query)}`);
      return {
        items: (page.items ?? []).map(toUiFinding),
        total: page.total ?? 0,
        page: page.page ?? 1,
        pageSize: page.page_size ?? 20,
        pages: page.pages ?? 1,
      } as T;
    },
    // Findings export is operator-only for now; the portal stub returns "whole
    // engagement" so the shared workspace type is satisfied without a portal route.
    findingIds: async <T>() => ({ finding_ids: null } as T),
    groups: async <T>(query: string) => mapFindingGroupPage(
      await portalApi<ApiFindingGroupPage>(`/workspace/findings/groups?${backendQueryString(query)}`),
    ) as T,
    summary: async <T>(query: string) => mapSummary(
      await portalApi<ApiFindingSummary>(`/workspace/findings/summary${query ? `?${query}` : ""}`),
    ) as T,
    assets: async <T>() => (
      (await portalApi<ApiFindingAsset[]>("/workspace/findings/assets")).map(mapAsset)
    ) as T,
    scans: async <T>() => (
      (await portalApi<ApiScanOption[]>("/workspace/findings/scans")).map(mapScanOption)
    ) as T,
    compare: async <T>(query: string) => mapCompareResult(
      await portalApi<unknown>(`/workspace/findings/compare?${query}`),
    ) as T,
    engagements: async <T>() => {
      const engagement = await portalApi<{ id: string; name: string }>("/engagement");
      return { engagements: [engagement] } as T;
    },
    agents: <T>() => portalApi<T>("/agents"),
    engagement: async <T>() => {
      const engagement = await portalApi<{ id: string; name: string }>("/engagement");
      return { engagement } as T;
    },
    detail: async <T>(id: string) => toUiFinding(await portalApi<unknown>(`/workspace/findings/${id}`)) as T,
    update: async <T>(id: string, patch: unknown) => toUiFinding(await portalApi<unknown>(`/findings/${id}`, {
      method: "PATCH", body: toApiFindingPatch(patch), idempotencyKey: newId(),
    })) as T,
    reopen: async <T>(id: string, reason: string) => toUiFinding(await portalApi<unknown>(`/findings/${id}/reopen`, {
      method: "POST", body: { reason }, idempotencyKey: newId(),
    })) as T,
    remediation: <T>(id: string, os: string) => portalApi<T>(`/findings/${id}/remediation?os=${os}`),
    events: <T>(id: string) => portalApi<T>(`/findings/${id}/events`),
    riskExplanation: <T>(id: string) => portalApi<T>(`/workspace/findings/${id}/risk-explanation`),
    obligations: <T>(id: string) => portalApi<T>(`/workspace/findings/${id}/obligations`),
    complianceBrief: <T>(id: string) => portalApi<T>(`/workspace/findings/${id}/compliance-brief`, {
      method: "POST", idempotencyKey: newId(),
    }),
  };
}
