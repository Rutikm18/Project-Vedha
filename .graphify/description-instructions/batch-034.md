# Node Description Batch 35 of 76

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

- "commands_interactive_parsemanualhosts": "parseManualHosts()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1451 | neighbors=[interactive.ts, wizardScan()]
- "commands_interactive_phaselabel": "phaseLabel()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L880 | neighbors=[interactive.ts, runIterativeEngagement()]
- "commands_interactive_w": "w()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L31 | neighbors=[interactive.ts, wizardAsk()]
- "commands_login_buildlogincommand": "buildLoginCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L46 | neighbors=[index.ts, login.ts]
- "commands_logout_buildlogoutcommand": "buildLogoutCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L4 | neighbors=[index.ts, logout.ts]
- "commands_report_buildreportcommand": "buildReportCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L85 | neighbors=[index.ts, report.ts]
- "commands_scan_buildscancommand": "buildScanCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L143 | neighbors=[index.ts, scan.ts]
- "commands_status_buildstatuscommand": "buildStatusCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L21 | neighbors=[index.ts, status.ts]
- "commands_tools_buildtoolscommand": "buildToolsCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L29 | neighbors=[index.ts, tools.ts]
- "commands_tools_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L14 | neighbors=[tools.ts, showSpinner()]
- "commands_tools_showspinner": "showSpinner()" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L16 | neighbors=[tools.ts, ln()]
- "commands_whoami_buildwhoamicommand": "buildWhoamiCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L4 | neighbors=[index.ts, whoami.ts]
- "components_dashboardcharts_dashboardcharts": "DashboardCharts()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L216 | neighbors=[page.tsx, DashboardCharts.tsx]
- "components_queryprovider_queryprovider": "QueryProvider()" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L6 | neighbors=[layout.tsx, QueryProvider.tsx]
- "components_themeprovider_themeprovider": "ThemeProvider()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L21 | neighbors=[layout.tsx, ThemeProvider.tsx]
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L17 | neighbors=[PageShell.tsx, ThemeProvider.tsx]
- "components_toastprovider_toastcontext": "ToastContext" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L26 | neighbors=[ToastProvider.tsx, useToast.ts]
- "components_toastprovider_toastprovider": "ToastProvider()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L159 | neighbors=[layout.tsx, ToastProvider.tsx]
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L83 | neighbors=[page.tsx, LiveOverview.tsx]
- "dashboard_protocolrow_riskcolor": "riskColor()" | kind=code-symbol | source=manager/frontend/components/dashboard/ProtocolRow.tsx:L6 | neighbors=[ProtocolRow.tsx, ProtocolRow()]
- "dashboard_slarow_getsla": "getSla()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L6 | neighbors=[SlaRow.tsx, SlaRow()]
- "dashboard_slasummarycell_slasummarycell": "SlaSummaryCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaSummaryCell.tsx:L11 | neighbors=[SlaSummaryCell.tsx, page.tsx]
- "dashboard_zonerow_zonerow": "ZoneRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/ZoneRow.tsx:L6 | neighbors=[ZoneRow.tsx, page.tsx]
- "data_mock_dashboard_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L11 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_attack_paths": "ATTACK_PATHS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L41 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_pathstatus": "PathStatus" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L10 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L31 | neighbors=[ProtocolRow.tsx, mock-dashboard.ts]
- "data_mock_dashboard_protocols": "PROTOCOLS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L57 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_sla_findings": "SLA_FINDINGS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L49 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_slafinding": "SlaFinding" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L22 | neighbors=[SlaRow.tsx, mock-dashboard.ts]
- "data_mock_dashboard_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L36 | neighbors=[ZoneRow.tsx, mock-dashboard.ts]
- "data_mock_dashboard_zones": "ZONES" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L64 | neighbors=[mock-dashboard.ts, page.tsx]
- "detection_correlator_detectioncorrelator_generate_gap_report": ".generate_gap_report()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L192 | neighbors=[DetectionCorrelator, DetectionGap]
- "detection_correlator_host_matches": "_host_matches()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L68 | neighbors=[correlator.py, ._host_for()]
- "detection_edr_crowdstrikefalcon_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L98 | neighbors=[CrowdStrikeFalcon, ._request()]
- "detection_edr_microsoftdefender_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L147 | neighbors=[MicrosoftDefender, ._request()]
- "detection_edr_sentinelone_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L193 | neighbors=[SentinelOne, ._request()]
- "detection_engine_ai_normalizer_aiclient_propose_cpe": ".propose_cpe()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L89 | neighbors=[AIClient, Returns a list of {"vendor", "product",…]
- "detection_engine_ai_normalizer_anthropicaiclient_propose_cpe": ".propose_cpe()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L108 | neighbors=[AnthropicAIClient, .get()]
- "detection_engine_ai_normalizer_fakeaiclient_propose_cpe": ".propose_cpe()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L134 | neighbors=[FakeAIClient, .get()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-034.json

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
