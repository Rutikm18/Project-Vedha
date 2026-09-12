import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type FleetWorkspaceSurface = "manager" | "portal";

export function createFleetWorkspaceApi(surface: FleetWorkspaceSurface) {
  if (surface === "manager") {
    return {
      enrollment: <T>() => fetchJson<T>("/api/fleet/enrollment"),
      probes: <T>() => fetchJson<T>("/api/scan/probes"),
      agentJobs: <T>(agentId: string) => fetchJson<T>(`/api/fleet/agents/${encodeURIComponent(agentId)}/jobs`),
      jobs: <T>(query: string) => fetchJson<T>(`/api/fleet/jobs?${query}`),
      approve: <T>(requestId: string, probeName: string | null, _userCode?: string) => {
        void _userCode;
        return fetchJson<T>(`/api/fleet/enrollment/${encodeURIComponent(requestId)}/approve`, {
        method: "POST", body: JSON.stringify({ probe_name: probeName }),
        });
      },
    };
  }
  return {
    // Enrollment requests have no engagement identity until an operator binds
    // them, so exposing the tenant queue would violate portal isolation.
    enrollment: async <T>() => ({ requests: [], manager_url: "" }) as T,
    probes: <T>() => portalApi<T>("/agents"),
    agentJobs: <T>(agentId: string) => portalApi<T>(`/workspace/fleet/agents/${encodeURIComponent(agentId)}/jobs`),
    jobs: <T>(query: string) => portalApi<T>(`/workspace/fleet/jobs${query ? `?${query}` : ""}`),
    approve: <T>(_requestId: string, probeName: string | null, userCode?: string) => {
      void _requestId;
      if (!userCode?.trim()) throw new Error("Enter the verification code shown by the vedha-agent installer");
      return portalApi<T>("/workspace/fleet/enrollment/approve", {
        method: "POST",
        body: { user_code: userCode.trim(), probe_name: probeName },
      });
    },
  };
}
