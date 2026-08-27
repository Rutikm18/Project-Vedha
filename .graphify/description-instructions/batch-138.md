# Node Description Batch 139 of 236

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "components_dashboardcharts_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L209 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_timelinepoint": "TimelinePoint" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L15 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_top_findings": "TOP_FINDINGS" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L203 | neighbors=[DashboardCharts.tsx]
- "components_pageshell_pageshellprops": "PageShellProps" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L9 | neighbors=[PageShell.tsx]
- "components_sidebar_nav_sections": "NAV_SECTIONS" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L21 | neighbors=[Sidebar.tsx]
- "components_sidebar_navitem": "NavItem" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L14 | neighbors=[Sidebar.tsx]
- "components_sidebar_sidebarprops": "SidebarProps" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L49 | neighbors=[Sidebar.tsx]
- "components_themeprovider_subscribetohydration": "subscribeToHydration()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L24 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_theme": "Theme" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L12 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontext": "ThemeContext" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L19 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontextvalue": "ThemeContextValue" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L14 | neighbors=[ThemeProvider.tsx]
- "components_toastprovider_toast": "Toast" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L8 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toast_styles": "TOAST_STYLES" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L35 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastcontextvalue": "ToastContextValue" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L17 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastitem": "ToastItem()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L69 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toasttype": "ToastType" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L6 | neighbors=[ToastProvider.tsx]
- "customer_access_page_ca": "ca()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L9 | neighbors=[page.tsx]
- "customer_access_page_clientuser": "ClientUser" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L24 | neighbors=[page.tsx]
- "customer_access_page_customeraccesspage": "CustomerAccessPage()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L26 | neighbors=[page.tsx]
- "customer_access_page_scanreq": "ScanReq" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L20 | neighbors=[page.tsx]
- "customers_page_clientuserresp": "ClientUserResp" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L20 | neighbors=[page.tsx]
- "customers_page_customer": "Customer" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L10 | neighbors=[page.tsx]
- "customers_page_customerspage": "CustomersPage()" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L36 | neighbors=[page.tsx]
- "customers_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L19 | neighbors=[page.tsx]
- "customers_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/customers/page.tsx:L25 | neighbors=[page.tsx]
- "customers_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/customers/route.ts:L10 | neighbors=[route.ts]
- "dashboard_dashboardgrid_agent": "Agent" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L36 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agent_status": "AGENT_STATUS" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L38 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agentmonitor": "AgentMonitor()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L73 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agentrow": "AgentRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L44 | neighbors=[DashboardGrid.tsx]
- "dashboard_dashboardgrid_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L35 | neighbors=[DashboardGrid.tsx]
- "dashboard_exposurecards_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L26 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_healthband": "healthBand()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L50 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_meterrow": "MeterRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L59 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_riskband": "riskBand()" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L42 | neighbors=[ExposureCards.tsx]
- "dashboard_exposurecards_scalenote": "scaleNote" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L150 | neighbors=[ExposureCards.tsx]
- "dashboard_liveoverview_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L33 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L35 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isactiveengagement": "isActiveEngagement()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L42 | neighbors=[LiveOverview.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-138.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
