import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type FleetWorkspaceSurface = "manager" | "portal";

/** What Fleet → Add agent needs to know before it can hand out a command. */
export interface AgentInstallInfo {
  available: boolean;
  version?: string;
  arches?: string[];
  signed?: boolean;
  signing_key_id?: string;
  reason?: string;
  manager_url: string;
  manager_url_configured: boolean;
  /** Portal only: whether this engagement can take an agent right now. */
  can_add_agent?: boolean;
  blocker?: string | null;
  /** The Windows side of the release; absent on managers that predate it. */
  windows?: AgentWindowsInfo;
}

export interface AgentWindowsInfo {
  available: boolean;
  /** Why Windows is withheld — operators only; empty for customers. */
  reason?: string;
  p256_signed?: boolean;
  p256_key_id?: string | null;
  /** SHA-1 thumbprint the release pins for vedha-agent.exe; null when it is not Authenticode-signed. */
  authenticode_thumbprint?: string | null;
}

export interface InstallCommands {
  one_line: string;
  download: string;
  run: string;
  /** Windows PowerShell form — run from an elevated prompt. Absent for a non-https manager or values that cannot be embedded safely. */
  windows_powershell?: string;
  /** cmd.exe form (self-elevating). Absent whenever the PowerShell form is. */
  windows_cmd?: string;
}

/** An install token as Fleet lists it. `token` and `commands` exist only in the
 *  create response — the raw token is never returned again. */
export interface InstallToken {
  id: string;
  name: string;
  token_prefix: string;
  engagement_id: string | null;
  state: "active" | "used" | "expired" | "revoked";
  usable: boolean;
  created_at: string | null;
  expires_at: string;
  last_used_at: string | null;
  token?: string;
  commands?: InstallCommands;
}

export interface FleetEngagementOption {
  id: string;
  name: string;
  status: string;
  scopeCidrs: string[];
}

export interface AgentExpiryResult {
  id: string;
  access_expires_at: string | null;
  access_expired: boolean;
}

// Install-command lifetimes offered in Fleet (minutes); must match the backend's
// INSTALL_TOKEN_LIFETIMES.
export const INSTALL_LIFETIMES: { minutes: number; label: string }[] = [
  { minutes: 60, label: "1 hour" },
  { minutes: 24 * 60, label: "24 hours" },
  { minutes: 7 * 24 * 60, label: "7 days" },
];

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
      installInfo: () => fetchJson<AgentInstallInfo>("/api/fleet/release"),
      engagements: async (): Promise<FleetEngagementOption[]> => {
        const data = await fetchJson<{ engagements?: FleetEngagementOption[] }>("/api/engagements");
        return data?.engagements ?? [];
      },
      installTokens: (engagementId?: string) => fetchJson<InstallToken[]>(
        `/api/fleet/enroll-tokens${engagementId ? `?engagement_id=${encodeURIComponent(engagementId)}` : ""}`,
      ),
      createInstallToken: (engagementId: string | null, name: string, lifetimeMinutes: number) => {
        if (!engagementId) throw new Error("Choose the engagement this agent will scan for");
        return fetchJson<InstallToken>("/api/fleet/enroll-tokens", {
          method: "POST",
          body: JSON.stringify({ engagement_id: engagementId, name, expires_in_minutes: lifetimeMinutes }),
        });
      },
      revokeInstallToken: (id: string) => fetchJson<null>(
        `/api/fleet/enroll-tokens/${encodeURIComponent(id)}`, { method: "DELETE" },
      ),
      // Set/extend/clear an agent's access expiry (operator only). null clears it.
      setAgentExpiry: (agentId: string, accessExpiresAt: string | null) => fetchJson<AgentExpiryResult>(
        `/api/fleet/agents/${encodeURIComponent(agentId)}/access-expiry`,
        { method: "PATCH", body: JSON.stringify({ access_expires_at: accessExpiresAt }) },
      ),
      canSetExpiry: true,
    };
  }
  return {
    // Enrollment requests have no engagement identity until an operator binds
    // them, so exposing the tenant queue would violate portal isolation.
    enrollment: async <T>() => ({ requests: [] }) as T,
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
    installInfo: () => portalApi<AgentInstallInfo>("/workspace/fleet/install"),
    // The engagement is the session's — the customer never picks one.
    engagements: async (): Promise<FleetEngagementOption[]> => [],
    installTokens: (_engagementId?: string) => {
      void _engagementId;
      return portalApi<InstallToken[]>("/workspace/fleet/enroll-tokens");
    },
    createInstallToken: (_engagementId: string | null, name: string, lifetimeMinutes: number) => {
      void _engagementId;
      return portalApi<InstallToken>("/workspace/fleet/enroll-tokens", {
        method: "POST", body: { name, lifetime_minutes: lifetimeMinutes },
      });
    },
    revokeInstallToken: (id: string) => portalApi<null>(
      `/workspace/fleet/enroll-tokens/${encodeURIComponent(id)}`, { method: "DELETE" },
    ),
    // Customers can't change expiry — only the operator sets it.
    setAgentExpiry: (_agentId: string, _accessExpiresAt: string | null): Promise<AgentExpiryResult> => {
      void _agentId; void _accessExpiresAt;
      return Promise.reject(new Error("Agent access expiry is managed by your Vedha operator"));
    },
    canSetExpiry: false,
  };
}
