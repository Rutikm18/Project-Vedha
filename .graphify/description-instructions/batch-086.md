# Node Description Batch 87 of 134

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

- "components_dashboardcharts_scorebar": "ScoreBar()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L194 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_sev": "SEV" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L29 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L179 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L209 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_timelinepoint": "TimelinePoint" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L15 | neighbors=[DashboardCharts.tsx]
- "components_dashboardcharts_top_findings": "TOP_FINDINGS" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L203 | neighbors=[DashboardCharts.tsx]
- "components_pageshell_pageshellprops": "PageShellProps" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L9 | neighbors=[PageShell.tsx]
- "components_sidebar_nav_sections": "NAV_SECTIONS" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L18 | neighbors=[Sidebar.tsx]
- "components_sidebar_navitem": "NavItem" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L11 | neighbors=[Sidebar.tsx]
- "components_sidebar_sidebarprops": "SidebarProps" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L44 | neighbors=[Sidebar.tsx]
- "components_themeprovider_subscribetohydration": "subscribeToHydration()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L24 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_theme": "Theme" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L12 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontext": "ThemeContext" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L19 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontextvalue": "ThemeContextValue" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L14 | neighbors=[ThemeProvider.tsx]
- "components_toastprovider_toast": "Toast" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L8 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toast_styles": "TOAST_STYLES" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L35 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastcontextvalue": "ToastContextValue" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L17 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toastitem": "ToastItem()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L69 | neighbors=[ToastProvider.tsx]
- "components_toastprovider_toasttype": "ToastType" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L6 | neighbors=[ToastProvider.tsx]
- "dashboard_liveoverview_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L33 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_finding": "Finding" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L23 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L35 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isactiveengagement": "isActiveEngagement()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L42 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_isopen": "isOpen()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L34 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L43 | neighbors=[LiveOverview.tsx]
- "dashboard_liveoverview_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L22 | neighbors=[LiveOverview.tsx]
- "dashboard_patchcomparisonmatrix_cell": "cell" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L24 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_head": "head" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L33 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_netchip": "NetChip()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L49 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_netlabel": "netLabel()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L19 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_patchcomparisonmatrix_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L14 | neighbors=[PatchComparisonMatrix.tsx]
- "dashboard_posturescorecard_delta": "Delta()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L45 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_dial": "Dial()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L56 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_grade": "GRADE" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L47 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_grade_color": "GRADE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L39 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_posture": "Posture" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L30 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_readout": "Readout()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L82 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_scores": "Scores" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L24 | neighbors=[PostureScorecard.tsx]
- "dashboard_posturescorecard_statcard": "StatCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L55 | neighbors=[PostureScorecard.tsx]
- "dashboard_slastatus_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L17 | neighbors=[SlaStatus.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-086.json

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
