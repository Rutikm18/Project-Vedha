# Node Description Batch 187 of 330

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

- "commands_scan_profile_tools": "PROFILE_TOOLS" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L9 | neighbors=[scan.ts]
- "commands_scan_resolvetargets": "resolveTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L17 | neighbors=[scan.ts]
- "commands_scan_scancommand": "scanCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L37 | neighbors=[scan.ts]
- "commands_status_scanrow": "ScanRow" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L4 | neighbors=[status.ts]
- "commands_status_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L13 | neighbors=[status.ts]
- "commands_tools_c": "C" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L8 | neighbors=[tools.ts]
- "commands_tools_w": "w()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L13 | neighbors=[tools.ts]
- "components_dashboardcharts_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L20 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_bone": "Bone()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L36 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_charttooltip": "ChartTooltip()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L41 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L15 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L21 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L25 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L26 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_kpicard": "KpiCard()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L61 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_scorebar": "ScoreBar()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L156 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_sev": "SEV" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L28 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L141 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L171 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_timelinepoint": "TimelinePoint" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L14 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_top_findings": "TOP_FINDINGS" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L203 | neighbors=[DashboardCharts.tsx]
- "components_engagementstatuscontrol_engagement_states": "ENGAGEMENT_STATES" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L31 | neighbors=[EngagementStatusControl.tsx]
- "components_engagementstatuscontrol_engagementstatuscontrolprops": "EngagementStatusControlProps" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L51 | neighbors=[EngagementStatusControl.tsx]
- "components_pageshell_pageshellprops": "PageShellProps" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L10 | neighbors=[PageShell.tsx]
- "components_refreshbutton_refreshbuttonprops": "RefreshButtonProps" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L21 | neighbors=[RefreshButton.tsx]
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
- "customer_access_page_ca": "ca()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L10 | neighbors=[page.tsx]
- "customer_access_page_clientuser": "ClientUser" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L25 | neighbors=[page.tsx]
- "customer_access_page_customeraccesspage": "CustomerAccessPage()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L27 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-186.json

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
