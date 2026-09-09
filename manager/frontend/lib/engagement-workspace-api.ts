import { toApiEngagementPatch, toUiEngagement } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type EngagementWorkspaceSurface = "manager" | "portal";

interface ActivityRecord {
  id: string;
  timestamp: string;
  kind: string;
  action: string;
  detail: string;
}

/**
 * Keeps the engagement UI transport-agnostic. Both surfaces render the same
 * component tree; the portal adapter removes caller-controlled engagement IDs.
 */
export function createEngagementWorkspaceApi(surface: EngagementWorkspaceSurface) {
  if (surface === "manager") {
    return {
      detail: <T>(id: string) => fetchJson<T>(`/api/engagements/${id}`),
      progress: <T>(id: string) => fetchJson<T>(`/api/engagements/${id}/campaign-progress`),
      findings: <T>(id: string, page: number) => fetchJson<T>(
        `/api/findings?paginated=true&engagement_id=${encodeURIComponent(id)}&page=${page}&page_size=20&sort=risk`,
      ),
      assets: <T>(id: string) => fetchJson<T>(`/api/engagements/${id}/assets`),
      update: <T>(id: string, body: unknown) => fetchJson<T>(`/api/engagements/${id}`, {
        method: "PUT",
        body: JSON.stringify(body),
      }),
      importFacts: async <T>(id: string, form: FormData) => {
        const response = await fetch(`/api/engagements/${id}/import-facts`, {
          method: "POST",
          body: form,
          credentials: "same-origin",
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(data.error || data.detail || `Import failed (${response.status})`);
        }
        return data as T;
      },
    };
  }

  return {
    detail: async <T>() => {
      const [detail, activity] = await Promise.all([
        portalApi<unknown>("/workspace/engagement"),
        portalApi<ActivityRecord[]>("/activity?limit=50"),
      ]);
      return {
        engagement: toUiEngagement(detail),
        activity: (activity ?? []).map((item) => ({
          id: item.id,
          timestamp: item.timestamp,
          actor: item.kind,
          action: item.action,
          detail: item.detail,
        })),
      } as T;
    },
    progress: <T>() => portalApi<T>("/workspace/engagement/campaign-progress"),
    findings: async <T>(_id: string, page: number) => {
      const query = new URLSearchParams({
        paginated: "true",
        page: String(page),
        page_size: "20",
        sort: "risk",
      });
      const raw = await portalApi<{
        items?: unknown[];
        total?: number;
        page?: number;
        page_size?: number;
        pages?: number;
      }>(`/workspace/findings?${query}`);
      const { toUiFinding } = await import("./adapters");
      return {
        items: (raw.items ?? []).map(toUiFinding),
        total: raw.total ?? 0,
        page: raw.page ?? page,
        pageSize: raw.page_size ?? 20,
        pages: raw.pages ?? 1,
      } as T;
    },
    assets: <T>() => portalApi<T>("/workspace/engagement/assets"),
    update: async <T>(_id: string, body: unknown) => ({
      engagement: toUiEngagement(await portalApi<unknown>("/workspace/engagement", {
        method: "PATCH",
        body: toApiEngagementPatch(body),
        idempotencyKey: crypto.randomUUID(),
      })),
    }) as T,
    importFacts: <T>(_id: string, form: FormData) => portalApi<T>(
      "/workspace/engagement/import-facts",
      {
        method: "POST",
        body: form,
        idempotencyKey: crypto.randomUUID(),
      },
    ),
  };
}
