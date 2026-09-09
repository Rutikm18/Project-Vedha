import { toApiFindingPatch, toUiFinding } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type FindingsWorkspaceSurface = "manager" | "portal";

/** Keep finding-focused AI navigation inside the caller's authenticated surface. */
export function portalFindingAssistantHref(findingId: string): string {
  return `/portal/assistant?finding=${encodeURIComponent(findingId)}`;
}

export function portalFindingAssistantPrompt(findingId: string): string {
  return `Explain finding ${findingId}. Summarize what it means, its impact, why it is prioritized, the recorded evidence, and the next remediation and verification steps.`;
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

/** Route/data adapter; the Findings component tree is identical on both surfaces. */
export function createFindingsWorkspaceApi(surface: FindingsWorkspaceSurface) {
  if (surface === "manager") {
    return {
      list: <T>(query: string) => fetchJson<T>(`/api/findings?${query}`),
      summary: <T>(query: string) => fetchJson<T>(`/api/findings/summary${query ? `?${query}` : ""}`),
      engagements: <T>() => fetchJson<T>("/api/engagements"),
      agents: <T>() => fetchJson<T>("/api/agents/register"),
      engagement: <T>(id: string) => fetchJson<T>(`/api/engagements/${id}`),
      detail: <T>(id: string) => fetchJson<T>(`/api/findings/${id}`),
      update: <T>(id: string, patch: unknown) => fetchJson<T>(`/api/findings/${id}`, {
        method: "PUT",
        body: JSON.stringify(patch),
      }),
      reopen: <T>(id: string, reason: string) => fetchJson<T>(`/api/findings/${id}/reopen`, {
        method: "POST",
        body: JSON.stringify({ reason }),
      }),
      remediation: <T>(id: string, os: string) => fetchJson<T>(`/api/findings/${id}/remediation?os=${os}`),
      events: <T>(id: string) => fetchJson<T>(`/api/findings/${id}/events`),
    };
  }

  return {
    list: async <T>(query: string) => {
      const page = await portalApi<ApiFindingPage>(`/workspace/findings?${query}`);
      return {
        items: (page.items ?? []).map(toUiFinding),
        total: page.total ?? 0,
        page: page.page ?? 1,
        pageSize: page.page_size ?? 20,
        pages: page.pages ?? 1,
      } as T;
    },
    summary: async <T>(query: string) => mapSummary(
      await portalApi<ApiFindingSummary>(`/workspace/findings/summary${query ? `?${query}` : ""}`),
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
    detail: async <T>(id: string) => toUiFinding(
      await portalApi<unknown>(`/workspace/findings/${id}`),
    ) as T,
    update: async <T>(id: string, patch: unknown) => toUiFinding(
      await portalApi<unknown>(`/findings/${id}`, {
        method: "PATCH",
        body: toApiFindingPatch(patch),
        idempotencyKey: crypto.randomUUID(),
      }),
    ) as T,
    reopen: async <T>(id: string, reason: string) => toUiFinding(
      await portalApi<unknown>(`/findings/${id}/reopen`, {
        method: "POST",
        body: { reason },
        idempotencyKey: crypto.randomUUID(),
      }),
    ) as T,
    remediation: <T>(id: string, os: string) => portalApi<T>(`/findings/${id}/remediation?os=${os}`),
    events: <T>(id: string) => portalApi<T>(`/findings/${id}/events`),
  };
}
