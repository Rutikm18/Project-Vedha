import { toUiEngagement, toUiFinding } from "./adapters";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type ReportsWorkspaceSurface = "manager" | "portal";

async function portalReportGeneration<T>(body: unknown): Promise<T> {
  const send = () => fetch("/api/reports/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Vedha-Surface": "portal" },
    body: JSON.stringify(body),
    credentials: "same-origin",
  });
  let response = await send();
  if (response.status === 401) {
    const refreshed = await fetch("/api/portal/login", { method: "PUT", credentials: "same-origin" });
    if (refreshed.ok) response = await send();
  }
  const value = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(value?.error ?? value?.detail ?? `Request failed (${response.status})`);
  }
  return value as T;
}

interface PortalPage<T> {
  items?: T[];
  total?: number;
  page?: number;
  page_size?: number;
  pages?: number;
}

interface SlaEnvelope {
  summary?: { breached?: number };
  breached?: number;
  items?: Array<{ id?: string; finding_id?: string; deadline?: string | null; state?: string }>;
}

function attachSla<T extends Record<string, unknown>>(items: T[], sla: SlaEnvelope): T[] {
  const deadlines = new Map(
    (sla.items ?? []).map((item) => [String(item.id ?? item.finding_id ?? ""), item]),
  );
  return items.map((item) => {
    const matched = deadlines.get(String(item.id ?? ""));
    return matched ? { ...item, slaDeadline: matched.deadline ?? undefined, slaState: matched.state } : item;
  });
}

/**
 * The reports UI consumes one contract on both surfaces. The portal transport
 * deliberately ignores any browser-supplied engagement id: FastAPI derives the
 * engagement from the authenticated customer session.
 */
export function createReportsWorkspaceApi(surface: ReportsWorkspaceSurface) {
  if (surface === "manager") {
    return {
      engagements: <T>() => fetchJson<T>("/api/engagements"),
      findings: async <T>(engagementId: string) => {
        const encoded = encodeURIComponent(engagementId);
        const [page, sla] = await Promise.all([
          fetchJson<PortalPage<Record<string, unknown>>>(`/api/findings?paginated=true&engagement_id=${encoded}&page=1&page_size=100&sort=risk`),
          fetchJson<SlaEnvelope>(`/api/findings/sla-summary?engagement_id=${encoded}`),
        ]);
        return { ...page, items: attachSla(page.items ?? [], sla) } as T;
      },
      summary: async <T>(engagementId: string) => {
        const encoded = encodeURIComponent(engagementId);
        const [summary, sla] = await Promise.all([
          fetchJson<Record<string, unknown>>(`/api/findings/summary?engagement_id=${encoded}`),
          fetchJson<SlaEnvelope>(`/api/findings/sla-summary?engagement_id=${encoded}`),
        ]);
        return { ...summary, slaBreached: Number(sla.summary?.breached ?? sla.breached ?? 0) } as T;
      },
      activity: <T>(engagementId: string) => fetchJson<T>(
        `/api/activity?engagement_id=${encodeURIComponent(engagementId)}&limit=50`,
      ),
      generate: <T>(body: unknown) => fetchJson<T>("/api/reports/generate", {
        method: "POST",
        headers: { "X-Vedha-Surface": "manager" },
        body: JSON.stringify(body),
      }),
    };
  }

  return {
    engagements: async <T>() => {
      const engagement = await portalApi<Record<string, unknown>>("/workspace/engagement");
      return { engagements: [toUiEngagement(engagement)] } as T;
    },
    findings: async <T>(_engagementId: string) => {
      void _engagementId;
      const [page, sla] = await Promise.all([
        portalApi<PortalPage<Record<string, unknown>>>("/workspace/findings?paginated=true&page=1&page_size=100&sort=risk"),
        portalApi<SlaEnvelope>("/sla-summary"),
      ]);
      const findings = attachSla((page.items ?? []).map(toUiFinding), sla);
      return {
        items: findings,
        total: page.total ?? 0,
        page: page.page ?? 1,
        pageSize: page.page_size ?? 100,
        pages: page.pages ?? 0,
      } as T;
    },
    summary: async <T>(_engagementId: string) => {
      void _engagementId;
      const [value, sla] = await Promise.all([
        portalApi<Record<string, unknown>>("/workspace/findings/summary"),
        portalApi<SlaEnvelope>("/sla-summary"),
      ]);
      return {
        total: Number(value.total ?? 0),
        openTotal: Number(value.open_total ?? 0),
        criticalOpen: Number(value.critical_open ?? 0),
        validated: Number(value.validated ?? 0),
        blind: Number(value.blind ?? 0),
        averageRisk: Number(value.average_risk ?? 0),
        slaBreached: Number(sla.breached ?? sla.summary?.breached ?? 0),
      } as T;
    },
    activity: <T>(_engagementId: string) => {
      void _engagementId;
      return portalApi<T>("/activity?limit=50");
    },
    generate: <T>(body: unknown) => portalReportGeneration<T>(body),
  };
}
