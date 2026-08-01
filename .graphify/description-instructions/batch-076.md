# Node Description Batch 77 of 119

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

- "components_dashboardcharts_bone": "Bone()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L37 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_charttooltip": "ChartTooltip()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L42 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L16 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L22 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L26 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L27 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_kpicard": "KpiCard()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L63 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_scorebar": "ScoreBar()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L194 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_sev": "SEV" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L29 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L179 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L209 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_timelinepoint": "TimelinePoint" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L15 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_top_findings": "TOP_FINDINGS" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L203 | neighbors=[DashboardCharts.tsx]
- "components_pageshell_pageshellprops": "PageShellProps" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L9 | neighbors=[PageShell.tsx]
- "components_sidebar_nav_sections": "NAV_SECTIONS" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L18 | neighbors=[Sidebar.tsx]
- "components_sidebar_navitem": "NavItem" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L11 | neighbors=[Sidebar.tsx]
- "components_sidebar_sidebarprops": "SidebarProps" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L43 | neighbors=[Sidebar.tsx]
- "components_themeprovider_subscribetohydration": "subscribeToHydration()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L24 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_theme": "Theme" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L12 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontext": "ThemeContext" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L19 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontextvalue": "ThemeContextValue" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L14 | neighbors=[ThemeProvider.tsx]
- "components_toastprovider_toast": "Toast" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L8 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toast_styles": "TOAST_STYLES" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L35 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastcontextvalue": "ToastContextValue" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L17 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastitem": "ToastItem()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L69 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toasttype": "ToastType" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L6 | neighbors=[ToastProvider.tsx]
- "dashboard_exposure_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/components/dashboard/Exposure.tsx:L19 | neighbors=[Exposure.tsx]
- "dashboard_liveoverview_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L24 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isactiveengagement": "isActiveEngagement()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L39 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isopen": "isOpen()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L34 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L43 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L22 | neighbors=[LiveOverview.tsx]
- "dashboard_slarow_sev_bg": "SEV_BG" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L19 | neighbors=[SlaRow.tsx]
- "dashboard_slarow_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L25 | neighbors=[SlaRow.tsx]
- "dashboard_slastatus_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L17 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_sev_style": "SEV_STYLE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L37 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slaitem": "SlaItem" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L20 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slastate": "SlaState" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L18 | neighbors=[SlaStatus.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-076.json

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
