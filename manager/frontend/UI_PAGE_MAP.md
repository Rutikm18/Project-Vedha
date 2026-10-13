# Vedha Manager — UI/UX Page → Code File Map

Every navigable page and the actual files behind it. All paths are relative to
`manager/frontend/`. Next.js App Router: a `page.tsx` is a route; `route.ts` under
`app/api/**` is that page's BFF proxy to the FastAPI backend.

Two apps share this frontend:
- **Manager** (internal operator app) — `app/*`
- **Portal** (customer-facing app) — `app/portal/*`

---

## Shared UI infrastructure (used by every page)

| Concern | File location |
|---|---|
| Root layout / providers | `app/layout.tsx` |
| Global styles + theme tokens (`--sev-*`, `--bg-*`, fonts) | `app/globals.css` |
| Page frame (header + content) | `components/PageShell.tsx` |
| Left navigation | `components/Sidebar.tsx` |
| Theme provider | `components/ThemeProvider.tsx` |
| Toasts | `components/ToastProvider.tsx` |
| React Query provider | `components/QueryProvider.tsx` |
| Loading / empty / error states | `components/states/DataState.tsx` |
| Console UI primitives | `components/console/Primitives.tsx` |
| Data fetch helper (client) | `lib/fetcher.ts` |
| Backend call helper (server/BFF) | `lib/backend.ts`, `lib/with-backend.ts` |
| Severity colors/labels | `lib/severity.ts` |

### AI Assistant (drawer available across pages)
`components/assistant/AssistantProvider.tsx`, `AssistantDrawer.tsx`, `AssistantFab.tsx`,
`AssistantText.tsx`, `AdvisorFlow.tsx`, `FactCard.tsx`, `ModelSwitcher.tsx` · logic:
`lib/assistant.ts`, `lib/ai-engine.ts` · proxy: `app/api/assistant/chat/route.ts`,
`app/api/assistant/explain/route.ts`

---

## Manager pages

### 1. Dashboard (home)
- Page: `app/page.tsx`
- Components: `components/dashboard/DashboardGrid.tsx`, `components/DashboardCharts.tsx`,
  `components/dashboard/LiveOverview.tsx`, `ExposureCards.tsx`, `PostureScorecard.tsx`,
  `PatchComparisonMatrix.tsx`, `SlaStatus.tsx`
- API: `app/api/activity/route.ts`, `app/api/analytics/exposure/route.ts`,
  `app/api/findings/summary/route.ts`, `app/api/findings/sla-summary/route.ts`

### 1a. Dashboard → Attack paths (Beta) section, sidebar entry and `/attack-paths`
- Dashboard section: `components/dashboard/AttackPathsPanel.tsx`, placed in `DashboardGrid.tsx` under the posture/SLA band
  (shown only when the console source has the `viewAttackPaths` capability: operators yes, customer portal no).
  Composition: `components/attack-paths/AttackPathsTiles.tsx` (three tiles of engagement counts), `OverviewList.tsx`
  (ladder of up to five engagements, each row with `JewelMeter.tsx`), `FixFirstCard.tsx` (route chain and share bars
  for the top row when it is exposed or reachable), `AttackPathStyles.tsx` + `overview-styles.ts` (container-query layout)
- Trend: `components/attack-paths/Sparkline.tsx` (2 px line from zero, ringed end dot, the numbers as its accessible name) with
  `trendView` / `sparkline` in `lib/attack-paths.ts`; history comes from `attack_path_snapshots` (migration `0061`)
- Compute: `components/attack-paths/useComputeAttackPaths.ts` (an explicit per-row recompute, run on a click only); the button sits beside the row link
- "Needs attention now" strip: one item built by `attackPathAttention` in `DashboardGrid.tsx`'s `NeedsAttention` (operator console only)
- Sidebar: `components/Sidebar.tsx` (Analysis → "Attack paths", BETA badge, operator menu only)
- Page: `app/attack-paths/page.tsx` (all engagements, the same tiles and rows, Beta badge and notice)
- Data: `lib/console-source.tsx` dataset `attackPaths` (operator endpoint `/api/attack-paths/overview?limit=5`, portal `null`)
  → BFF `app/api/attack-paths/overview/route.ts` → backend `GET /attack-paths/overview`; the card calls
  `app/api/attack-paths/focus/[id]/route.ts` → `GET /attack-paths/focus/{engagement_id}`. Both read-only, tenant-scoped,
  operators only (`routers/attack_paths.py`; rows built by `app/graph/overview.py`)
- View-model and wording: `lib/attack-paths.ts` (`overviewState`, `overviewLine`, `overviewTiles`, `meterCells`,
  `focusLead`, `routeChainView`, `focusBars`). Six row states; "not computed" and "no crown jewel marked" are never "0 reachable"
- Each row links to `/engagements/{id}/attack-paths` (§4a), which also shows an exposed-only engagement as
  "directly exposed" (`ExposedCallout` in `Panels.tsx`)

### 2. Login
- Page: `app/login/page.tsx`
- API: `app/api/auth/login/route.ts`, `auth/me/route.ts`, `auth/logout/route.ts`,
  `auth/pats/route.ts`, `auth/dev-hint/route.ts`
- Store: `lib/security-context.ts`

### 3. Engagements (list)
- Page: `app/engagements/page.tsx`
- API: `app/api/engagements/route.ts`
- Store: `lib/engagements-store.ts`

### 4. Engagement detail
- Page: `app/engagements/[id]/page.tsx`
- API: `app/api/engagements/[id]/route.ts`, `.../assets/route.ts`,
  `.../vuln-prioritizer/route.ts`, `.../import-facts/route.ts`
- Attack-path API (all real proxies to FastAPI via `lib/attack-paths-proxy.ts`, which validates
  UUID params and forwards only listed query keys): `.../attack-paths/route.ts` (+ `[pathId]`),
  `.../attack-path-analysis/route.ts`, `.../chokepoints/route.ts`, `.../attack-graph/route.ts`,
  `.../blast-radius/[assetId]/route.ts`
- AI report: `.../ai-report/{draft,generate,approve,reject}/route.ts`,
  `.../ai-report/status/[jobId]/route.ts`
- Detection validation: `.../detection-validation/{coverage,gaps,results,run,siem-config}/route.ts`
- Attack paths page: see 4a.

### 4a. Engagement → Attack paths (Beta)
- Page: `app/engagements/[id]/attack-paths/page.tsx` → `AttackPathsWorkspace.tsx` (data + layout),
  `Panels.tsx` (coverage, empty-state explanation, fix-first, route table, step detail),
  `PathMap.tsx` (route map), `styles.ts`
- Linked from the engagement toolbar with a Beta badge (operators only, not the customer portal); the page header carries the same badge and a notice that says what beta means here
- API client: `lib/attack-paths-api.ts` · view-model and types: `lib/attack-paths.ts`
  (wording rules, empty-state reasons, fix-first sentence, route-map layout)
- Subnet map ("Where the routes go"): `app/engagements/[id]/attack-paths/ZoneMap.tsx` (boxes + arrows + two tables), data from BFF
  `app/api/engagements/[id]/attack-path-zones/route.ts` → `GET /engagements/{id}/attack-path-zones` (`app/graph/zones.py`); layout and wording
  in `lib/attack-paths.ts` (`layoutZoneMap`, `zoneSummary`)
- Backend: `manager/backend/app/routers/attack_paths.py` (list, detail, analysis, zones, recompute)

### 5. Engagement → Customer access
- Page: `app/engagements/[id]/customer-access/page.tsx`
- API: `app/api/engagements/[id]/customer-access/[...path]/route.ts`

### 6. Scan (launch + Active Job + VA Campaign live view)
- Page: `app/scan/page.tsx`
- Components (VA Campaigns live view): `app/campaign/[id]/CampaignProgress.tsx`,
  `app/campaign/[id]/RawFacts.tsx`
- API: `app/api/scan/launch/route.ts`, `scan/use-cases/route.ts`, `scan/probes/route.ts`,
  `scan/jobs/route.ts` (+ `[id]`), `scan/campaigns/route.ts` (+ `[id]`)
- Campaign progress / evidence / explain:
  `app/api/engagements/[id]/campaign-progress/route.ts`,
  `app/api/engagements/[id]/raw-facts/route.ts`,
  `app/api/engagements/[id]/detection-explain/route.ts`
- Stores: `lib/scan-pipeline.ts`, `lib/scan-events.ts`, `lib/job-store.ts`,
  `lib/campaign-store.ts`, `lib/scanner-request-validation.ts`, `lib/target-parser.ts`

### 7. Campaign (standalone)
- Pages: `app/campaign/page.tsx`, `app/campaign/[id]/page.tsx`
- Components: `app/campaign/[id]/CampaignProgress.tsx`, `app/campaign/[id]/RawFacts.tsx`
- Store: `lib/campaign-store.ts`

### 8. Fleet (probes + all running jobs)
- Page: `app/fleet/page.tsx`
- Component: `app/fleet/FleetJobs.tsx`
- API: `app/api/fleet/jobs/route.ts`, `fleet/agents/[id]/jobs/route.ts`,
  `fleet/enrollment/route.ts` (+ `[id]/approve`), `app/api/agents/register/route.ts`
- Store: `lib/agents-store.ts`

### 9. Findings
- Page: `app/findings/page.tsx`
- API: `app/api/findings/route.ts` (+ `[id]`, `[id]/reopen`), `findings/summary/route.ts`,
  `findings/sla-summary/route.ts`
- Store: `lib/findings-store.ts`, `lib/detection-store.ts`, `lib/finding-id.ts`

### 10. Reports
- Page: `app/reports/page.tsx`
- API: engagement AI-report routes (see §4)

### 11. Customers (clients)
- Page: `app/customers/page.tsx`
- API: `app/api/customers/route.ts`, `customers/[id]/reveal/route.ts`
- Store: `lib/clients-store.ts`, `lib/cases-store.ts`

### 12. AI Brain
- Page: `app/aibrain/page.tsx`
- Components: `components/assistant/FactCard.tsx`, `AssistantText.tsx`
- API: `app/api/brain/route.ts`, `app/api/ai/status/route.ts`
- Logic: `lib/assistant.ts`, `lib/ai-engine.ts`, `lib/ai/` under `lib/engine/`

### 13. Settings
- Page: `app/settings/page.tsx`
- API: `app/api/settings/status/route.ts`, `app/api/sla-policy/route.ts`,
  `app/api/integrations/route.ts` (+ `[kind]`, `test`)

---

## Portal pages (customer-facing)

Shared portal frame: `components/portal/PortalShell.tsx` · layout: `app/portal/layout.tsx`
· logic: `lib/portal-client.ts` · auth proxy: `app/api/portal/login/route.ts`,
`portal/logout/route.ts` · generic proxy: `app/api/portal/[...path]/route.ts`

| Page | Route file |
|---|---|
| Portal login | `app/portal/login/page.tsx` |
| Portal home | `app/portal/page.tsx` |
| Portal findings | `app/portal/findings/page.tsx` |
| Portal scans | `app/portal/scans/page.tsx` |
| Portal reports | `app/portal/reports/page.tsx` |
| Portal settings | `app/portal/settings/page.tsx` |

---

## Parser/adapter libs (turn raw tool output → UI models)

`lib/nmap-parser.ts`, `naabu-parser.ts`, `nuclei-parser.ts`, `httpx-parser.ts`,
`netexec-parser.ts`, `testssl-parser.ts`, `whatweb-parser.ts`, `openvas-client.ts`,
`adapters.ts`, `exploit-store.ts`, `tenant.ts` / `tenant-server.ts`, `errors.ts`.

> Note: styling is CSS-variable/theme driven from `app/globals.css` (there is no
> per-page stylesheet); components are styled inline against those tokens.
