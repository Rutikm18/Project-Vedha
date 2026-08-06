# Node Description Batch 57 of 134

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

- "commands_doctor_builddoctorcommand": "buildDoctorCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L216 | neighbors=[index.ts, doctor.ts]
- "commands_doctor_checktool": "checkTool()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L92 | neighbors=[doctor.ts, which()]
- "commands_doctor_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L33 | neighbors=[doctor.ts, render()]
- "commands_doctor_symbol": "symbol()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L35 | neighbors=[doctor.ts, render()]
- "commands_doctor_which": "which()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L73 | neighbors=[doctor.ts, checkTool()]
- "commands_engagement_buildengagementcommand": "buildEngagementCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L36 | neighbors=[index.ts, engagement.ts]
- "commands_findings_buildfindingscommand": "buildFindingsCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L6 | neighbors=[index.ts, findings.ts]
- "commands_interactive_asksecret": "askSecret()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L51 | neighbors=[interactive.ts, ensureAuthenticated()]
- "commands_interactive_buildinteractivecommand": "buildInteractiveCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2091 | neighbors=[index.ts, interactive.ts]
- "commands_interactive_detectlocalsubnet": "detectLocalSubnet()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L194 | neighbors=[interactive.ts, pickTargets()]
- "commands_interactive_parsemanualhosts": "parseManualHosts()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1448 | neighbors=[interactive.ts, wizardScan()]
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
- "components_dashboardcharts_dashboardcharts": "DashboardCharts()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L218 | neighbors=[page.tsx, DashboardCharts.tsx]
- "components_queryprovider_queryprovider": "QueryProvider()" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L6 | neighbors=[layout.tsx, QueryProvider.tsx]
- "components_themeprovider_themeprovider": "ThemeProvider()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L30 | neighbors=[layout.tsx, ThemeProvider.tsx]
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L26 | neighbors=[PageShell.tsx, ThemeProvider.tsx]
- "components_toastprovider_toastcontext": "ToastContext" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L26 | neighbors=[ToastProvider.tsx, useToast.ts]
- "components_toastprovider_toastprovider": "ToastProvider()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L159 | neighbors=[layout.tsx, ToastProvider.tsx]
- "dashboard_liveoverview_verdict": "verdict()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L47 | neighbors=[LiveOverview.tsx, LiveOverview()]
- "dashboard_patchcomparisonmatrix_n": "n()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L45 | neighbors=[PatchComparisonMatrix.tsx, PatchComparisonMatrix()]
- "dashboard_posturescorecard_matrixrow": "MatrixRow" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L27 | neighbors=[PatchComparisonMatrix.tsx, PostureScorecard.tsx]
- "dashboard_slastatus_deadlinetitle": "deadlineTitle()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L68 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "dashboard_slastatus_elapsedpct": "elapsedPct()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L62 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "dashboard_slastatus_pct": "pct()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L54 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "dashboard_slastatus_slastatus": "SlaStatus()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L169 | neighbors=[SlaStatus.tsx, page.tsx]
- "dashboard_slastatus_timelabel": "timeLabel()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L52 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "detection_correlator_detectioncorrelator_generate_gap_report": ".generate_gap_report()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L192 | neighbors=[DetectionCorrelator, DetectionGap]
- "detection_correlator_host_matches": "_host_matches()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L68 | neighbors=[correlator.py, ._host_for()]
- "detection_edr_crowdstrikefalcon_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L98 | neighbors=[CrowdStrikeFalcon, ._request()]
- "detection_edr_microsoftdefender_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L147 | neighbors=[MicrosoftDefender, ._request()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-056.json

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
