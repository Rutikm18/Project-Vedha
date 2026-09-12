import { toUiEngagement } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type CampaignWorkspaceSurface = "manager" | "portal";

export function createCampaignWorkspaceApi(surface: CampaignWorkspaceSurface) {
  if (surface === "manager") {
    return {
      campaigns: <T>() => fetchJson<T>("/api/scan/campaigns"),
      engagements: <T>() => fetchJson<T>("/api/engagements"),
    };
  }
  return {
    // Legacy probe snapshots are local files without an engagement foreign key,
    // so they cannot be safely attributed to this customer. The shared page's
    // canonical job/pipeline sections remain live; snapshots stay empty until
    // the producer stores engagement identity.
    campaigns: async <T>() => [] as T,
    engagements: async <T>() => {
      const detail = await portalApi<Record<string, unknown>>("/workspace/engagement");
      return { engagements: [toUiEngagement(detail)] } as T;
    },
  };
}
