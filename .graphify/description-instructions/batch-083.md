# Node Description Batch 84 of 131

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

- "commands_interactive_issinglehost": "isSingleHost()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L189 | neighbors=[interactive.ts]
- "commands_interactive_makerl": "makeRl()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L35 | neighbors=[interactive.ts]
- "commands_interactive_phasestate": "PhaseState" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L809 | neighbors=[interactive.ts]
- "commands_interactive_targetspec": "TargetSpec" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L182 | neighbors=[interactive.ts]
- "commands_interactive_tool": "Tool" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L293 | neighbors=[interactive.ts]
- "commands_login_prompt": "prompt()" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L5 | neighbors=[login.ts]
- "commands_login_promptsilent": "promptSilent()" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L15 | neighbors=[login.ts]
- "commands_report_aireport": "AiReport" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L14 | neighbors=[report.ts]
- "commands_report_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L6 | neighbors=[report.ts]
- "commands_report_errexit": "errExit()" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L40 | neighbors=[report.ts]
- "commands_report_renderreport": "renderReport()" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L45 | neighbors=[report.ts]
- "commands_scan_printaicomment": "printAiComment()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L30 | neighbors=[scan.ts]
- "commands_scan_profile_tools": "PROFILE_TOOLS" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L9 | neighbors=[scan.ts]
- "commands_scan_resolvetargets": "resolveTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L17 | neighbors=[scan.ts]
- "commands_scan_scancommand": "scanCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L37 | neighbors=[scan.ts]
- "commands_status_scanrow": "ScanRow" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L4 | neighbors=[status.ts]
- "commands_status_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L13 | neighbors=[status.ts]
- "commands_tools_c": "C" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L8 | neighbors=[tools.ts]
- "commands_tools_w": "w()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L13 | neighbors=[tools.ts]
- "components_dashboardcharts_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L21 | neighbors=[DashboardCharts.tsx]
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
- "components_sidebar_sidebarprops": "SidebarProps" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L44 | neighbors=[Sidebar.tsx]
- "components_themeprovider_subscribetohydration": "subscribeToHydration()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L24 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_theme": "Theme" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L12 | neighbors=[ThemeProvider.tsx]
- "components_themeprovider_themecontext": "ThemeContext" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L19 | neighbors=[ThemeProvider.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-083.json

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
