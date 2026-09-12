import { toUiEngagement } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type AIBrainWorkspaceSurface = "manager" | "portal";

interface BrainRequest {
  messages: Array<{ role: "user" | "assistant"; content: string }>;
  engagementId?: string;
  provider?: string;
  model?: string;
}

export function createAIBrainWorkspaceApi(surface: AIBrainWorkspaceSurface) {
  if (surface === "manager") {
    return {
      status: <T>() => fetchJson<T>("/api/ai/status"),
      engagements: <T>() => fetchJson<T>("/api/engagements"),
      send: <T>(body: BrainRequest) => fetchJson<T>("/api/brain", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    };
  }

  return {
    status: <T>() => portalApi<T>("/workspace/ai/status"),
    engagements: async <T>() => {
      const engagement = await portalApi<Record<string, unknown>>("/workspace/engagement");
      return { engagements: [toUiEngagement(engagement)] } as T;
    },
    // Engagement scope is intentionally not forwarded. The portal backend
    // derives it from the authenticated client claim before grounding the LLM.
    send: <T>(body: BrainRequest) => portalApi<T>("/assistant/chat", {
      method: "POST",
      body: {
        messages: body.messages,
        provider: body.provider,
        model: body.model,
      },
    }),
  };
}
