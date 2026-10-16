import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type SettingsWorkspaceSurface = "manager" | "portal";

export function createSettingsWorkspaceApi(surface: SettingsWorkspaceSurface) {
  if (surface === "manager") {
    return {
      status: <T>() => fetchJson<T>("/api/settings/status"),
      probes: <T>() => fetchJson<T>("/api/agents"),
      aiStatus: <T>() => fetchJson<T>("/api/ai/status"),
    };
  }
  return {
    status: async <T>() => {
      // A successful scoped read proves API reachability and session binding
      // without exposing operator-only deployment configuration.
      await portalApi("/workspace/engagement");
      return { checkedAt: new Date().toISOString(), apiReachable: true } as T;
    },
    probes: async <T>() => {
      const rows = await portalApi<Array<Record<string, unknown>>>("/agents");
      return rows.map((row) => ({
        id: row.id,
        name: row.name,
        hostname: row.name,
        status: row.status,
        last_seen_at: row.last_heartbeat,
        platform: row.location,
        capabilities: row.capabilities,
      })) as T;
    },
    aiStatus: <T>() => portalApi<T>("/workspace/ai/status"),
  };
}
