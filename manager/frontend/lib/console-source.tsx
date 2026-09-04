"use client";

/**
 * console-source — the seam that lets ONE set of console components serve both
 * the operator dashboard and the customer portal.
 *
 * THE PROBLEM IT SOLVES. The dashboard components (components/dashboard/*) each
 * called `fetchJson("/api/…")` directly, so they were welded to the operator API.
 * Giving the customer the same console meant copying them — and a copy diverges
 * the first time either side is edited. The brief was explicit: a change to the
 * main dashboard must show up in the customer portal automatically.
 *
 * THE SEAM. A component asks for a logical dataset by KEY ("posture", "sla",
 * "exposure", …). This context decides which concrete endpoint that key resolves
 * to, and how the response is fetched. The operator provider points at the
 * operator API; the portal provider points at /api/portal/*, which FastAPI pins
 * to the caller's own engagement. Same component, same rendering, different
 * scope — and only the provider knows the difference.
 *
 * WHY THE SHAPES MATCH. The portal routes DELEGATE to the operator handlers with
 * engagement_id pinned (backend/app/routers/portal.py), so both sides return the
 * same JSON. That is what makes one component able to render either.
 *
 * CAPABILITIES, NOT ROLE CHECKS. Components ask `can("navigateToEngagement")`
 * rather than testing `mode === "portal"`. A customer console has no engagement
 * switcher and no drill-through into operator screens; expressing that as a
 * named capability keeps the reason legible at the call site.
 */

import React, { createContext, useContext, useMemo } from "react";
import { useQuery, type UseQueryResult } from "@tanstack/react-query";
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

/** Logical datasets the console can render. Adding a panel means adding a key
 *  here and an endpoint in BOTH providers — a compile-time reminder that the
 *  customer console needs a scoped equivalent, not a silent operator-only panel. */
export type ConsoleKey =
  | "agents"
  | "sla"
  | "findingsSummary"
  | "posture"
  | "exposure"
  | "activity"
  | "topFindings"
  | "engagements";

export type ConsoleCapability =
  /** Clicking through to an operator-only screen (engagement, campaign). */
  | "navigateToEngagement"
  /** Choosing which engagement the console shows. A customer has exactly one. */
  | "switchEngagement"
  /** Acting on a finding (status changes, assignment). */
  | "mutateFindings";

export interface ConsoleSource {
  mode: "operator" | "portal";
  /** Shown where the console names what it is scoped to. */
  scopeLabel: string;
  /** null endpoint = this dataset does not exist on this side; the panel that
   *  needs it renders its unavailable state instead of erroring. */
  endpoints: Record<ConsoleKey, string | null>;
  capabilities: ReadonlySet<ConsoleCapability>;
}

const OPERATOR_SOURCE: ConsoleSource = {
  mode: "operator",
  scopeLabel: "All engagements",
  endpoints: {
    agents: "/api/agents/register",
    sla: "/api/findings/sla-summary",
    findingsSummary: "/api/findings/summary",
    posture: "/api/analytics/posture",
    exposure: "/api/analytics/exposure",
    activity: "/api/activity?limit=20",
    topFindings: "/api/findings?paginated=true&page=1&page_size=5&sort=risk",
    engagements: "/api/engagements",
  },
  capabilities: new Set<ConsoleCapability>([
    "navigateToEngagement", "switchEngagement", "mutateFindings",
  ]),
};

/** Every path is relative to /api/portal, which FastAPI scopes to the caller's
 *  own engagement. `engagements` is null on purpose: a customer has exactly one
 *  and never picks from a list. */
const PORTAL_SOURCE: ConsoleSource = {
  mode: "portal",
  scopeLabel: "Your engagement",
  endpoints: {
    agents: "/agents",
    sla: "/sla-summary",
    findingsSummary: "/summary",
    posture: "/analytics/posture",
    exposure: "/analytics/exposure",
    activity: "/activity?limit=20",
    topFindings: "/findings",
    engagements: null,
  },
  capabilities: new Set<ConsoleCapability>(),
};

const ConsoleSourceContext = createContext<ConsoleSource>(OPERATOR_SOURCE);

export function ConsoleSourceProvider(
  { source, children }: { source: ConsoleSource; children: React.ReactNode },
) {
  return (
    <ConsoleSourceContext.Provider value={source}>
      {children}
    </ConsoleSourceContext.Provider>
  );
}

/** Operator console. Explicit so a page states which console it is. */
export function OperatorConsoleProvider({ children }: { children: React.ReactNode }) {
  return <ConsoleSourceProvider source={OPERATOR_SOURCE}>{children}</ConsoleSourceProvider>;
}

/** Customer console — same components, engagement-scoped data. */
export function PortalConsoleProvider(
  { scopeLabel, children }: { scopeLabel?: string; children: React.ReactNode },
) {
  const source = useMemo<ConsoleSource>(
    () => (scopeLabel ? { ...PORTAL_SOURCE, scopeLabel } : PORTAL_SOURCE),
    [scopeLabel],
  );
  return <ConsoleSourceProvider source={source}>{children}</ConsoleSourceProvider>;
}

export function useConsoleSource(): ConsoleSource {
  return useContext(ConsoleSourceContext);
}

/** The React Query key `useConsoleQuery` stores a dataset under. Exported so
 *  freshness indicators read the SAME cache entry the panel's data came from —
 *  reading a hand-written key silently returns undefined and the indicator
 *  disappears, which is exactly what happened when these moved behind the seam. */
export function consoleQueryKey(mode: ConsoleSource["mode"], key: ConsoleKey): unknown[] {
  return ["console", mode, key];
}

/** Convenience for components already inside a provider. */
export function useConsoleQueryKey(key: ConsoleKey): unknown[] {
  return consoleQueryKey(useConsoleSource().mode, key);
}

export function useConsoleCapability(cap: ConsoleCapability): boolean {
  return useConsoleSource().capabilities.has(cap);
}

export interface ConsoleQueryOptions {
  refetchInterval?: number;
  enabled?: boolean;
}

/**
 * Fetch a logical dataset for whichever console is mounted.
 *
 * The query key carries the mode, so operator and portal caches never collide
 * if both ever render in one session. `unavailable` is true when this side has
 * no endpoint for the key — distinct from "loading" and from "errored", so a
 * panel can say "not available here" instead of spinning forever.
 */
export function useConsoleQuery<T>(
  key: ConsoleKey,
  opts: ConsoleQueryOptions = {},
): UseQueryResult<T> & { unavailable: boolean } {
  const source = useConsoleSource();
  const endpoint = source.endpoints[key];

  const query = useQuery<T>({
    queryKey: ["console", source.mode, key],
    queryFn: () => {
      if (!endpoint) throw new Error(`"${key}" is not available in the ${source.mode} console`);
      return source.mode === "portal"
        ? portalApi<T>(endpoint)
        : fetchJson<T>(endpoint);
    },
    enabled: (opts.enabled ?? true) && endpoint !== null,
    refetchInterval: opts.refetchInterval,
  });

  return Object.assign(query, { unavailable: endpoint === null });
}
