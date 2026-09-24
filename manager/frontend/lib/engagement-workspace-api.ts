import { toApiEngagementPatch, toUiEngagement, toUiFinding } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type EngagementWorkspaceSurface = "manager" | "portal";

interface PortalPage<T> {
  items?: T[];
  total?: number;
  page?: number;
  page_size?: number;
  pages?: number;
}

async function portalMultipart<T>(path: string, form: FormData): Promise<T> {
  const send = () => fetch(`/api/portal${path}`, {
    method: "POST",
    body: form,
    credentials: "same-origin",
  });
  let response = await send();
  if (response.status === 401) {
    const refreshed = await fetch("/api/portal/login", { method: "PUT", credentials: "same-origin" });
    if (refreshed.ok) response = await send();
  }
  const value = await response.json().catch(() => null);
  if (!response.ok) throw new Error(value?.error ?? value?.detail ?? `Import failed (${response.status})`);
  return value as T;
}

export function createEngagementWorkspaceApi(surface: EngagementWorkspaceSurface) {
  if (surface === "manager") {
    return {
      detail: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}`),
      findings: <T>(engagementId: string, page: number) => fetchJson<T>(
        `/api/findings?paginated=true&engagement_id=${encodeURIComponent(engagementId)}&page=${page}&page_size=20&sort=risk`,
      ),
      assets: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/assets`),
      progress: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/campaign-progress`),
      update: <T>(engagementId: string, body: unknown) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}`, {
        method: "PUT", body: JSON.stringify(body),
      }),
      importFacts: async <T>(engagementId: string, form: FormData) => {
        const response = await fetch(`/api/engagements/${encodeURIComponent(engagementId)}/import-facts`, {
          method: "POST", body: form, credentials: "same-origin",
        });
        const value = await response.json().catch(() => null);
        if (!response.ok) throw new Error(value?.error ?? value?.detail ?? `Import failed (${response.status})`);
        return value as T;
      },
      // Asset intelligence + regulatory profile. Operators can edit; the portal is read-only.
      canEditIntel: true,
      compliance: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/compliance`),
      profile: <T>(engagementId: string) => fetchJson<T>(`/api/engagements/${encodeURIComponent(engagementId)}/profile`),
      setProfile: <T>(engagementId: string, body: { sector: string; jurisdictions: string[] }) => fetchJson<T>(
        `/api/engagements/${encodeURIComponent(engagementId)}/profile`, { method: "PUT", body: JSON.stringify(body) },
      ),
      setAssetTags: <T>(engagementId: string, assetId: string, tags: Array<{ key: string; value: string }>) => fetchJson<T>(
        `/api/engagements/${encodeURIComponent(engagementId)}/assets/${encodeURIComponent(assetId)}/tags`,
        { method: "PUT", body: JSON.stringify({ tags }) },
      ),
      retag: <T>(engagementId: string) => fetchJson<T>(
        `/api/engagements/${encodeURIComponent(engagementId)}/assets/retag`, { method: "POST" },
      ),
    };
  }

  return {
    detail: async <T>(_engagementId: string) => {
      void _engagementId;
      const [detail, activity] = await Promise.all([
        portalApi<Record<string, unknown>>("/workspace/engagement"),
        portalApi<Array<Record<string, unknown>>>("/activity?limit=50"),
      ]);
      return {
        engagement: toUiEngagement(detail),
        activity: activity.map((item) => ({
          id: item.id,
          timestamp: item.timestamp,
          actor: item.kind,
          action: item.action,
          detail: item.detail,
        })),
      } as T;
    },
    findings: async <T>(_engagementId: string, pageNumber: number) => {
      const page = await portalApi<PortalPage<Record<string, unknown>>>(
        `/workspace/findings?paginated=true&page=${pageNumber}&page_size=20&sort=risk`,
      );
      return {
        items: (page.items ?? []).map(toUiFinding),
        total: page.total ?? 0,
        page: page.page ?? pageNumber,
        pageSize: page.page_size ?? 20,
        pages: page.pages ?? 0,
      } as T;
    },
    assets: <T>() => portalApi<T>("/workspace/engagement/assets"),
    progress: <T>() => portalApi<T>("/workspace/scan/campaign-progress"),
    update: async <T>(_engagementId: string, body: unknown) => {
      const updated = await portalApi<Record<string, unknown>>("/workspace/engagement", {
        method: "PATCH", body: toApiEngagementPatch(body), idempotencyKey: crypto.randomUUID(),
      });
      return { engagement: toUiEngagement(updated) } as T;
    },
    importFacts: <T>(_engagementId: string, form: FormData) =>
      portalMultipart<T>("/workspace/engagement/import-facts", form),
    canEditIntel: false,
    compliance: <T>() => portalApi<T>("/workspace/compliance"),
    profile: async <T>(): Promise<T> => { throw new Error("The regulatory profile is managed by your assessor."); },
    setProfile: async <T>(): Promise<T> => { throw new Error("The regulatory profile is managed by your assessor."); },
    setAssetTags: async <T>(): Promise<T> => { throw new Error("Asset tags are managed by your assessor."); },
    retag: async <T>(): Promise<T> => { throw new Error("Asset tags are managed by your assessor."); },
  };
}
