# Node Description Batch 45 of 104

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

- "commands_ask_buildaskcommand": "buildAskCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L59 | neighbors=[index.ts, ask.ts]
- "commands_doctor_builddoctorcommand": "buildDoctorCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L217 | neighbors=[index.ts, doctor.ts]
- "commands_doctor_checktool": "checkTool()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L93 | neighbors=[doctor.ts, which()]
- "commands_doctor_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L34 | neighbors=[doctor.ts, render()]
- "commands_doctor_symbol": "symbol()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L36 | neighbors=[doctor.ts, render()]
- "commands_doctor_which": "which()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L74 | neighbors=[doctor.ts, checkTool()]
- "commands_engagement_buildengagementcommand": "buildEngagementCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L36 | neighbors=[index.ts, engagement.ts]
- "commands_findings_buildfindingscommand": "buildFindingsCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L6 | neighbors=[index.ts, findings.ts]
- "commands_interactive_asksecret": "askSecret()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L51 | neighbors=[interactive.ts, ensureAuthenticated()]
- "commands_interactive_buildinteractivecommand": "buildInteractiveCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2094 | neighbors=[index.ts, interactive.ts]
- "commands_interactive_detectlocalsubnet": "detectLocalSubnet()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L194 | neighbors=[interactive.ts, pickTargets()]
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
- "config_config_env": "env()" | kind=code-symbol | source=probe-go/config/config.go:L86 | neighbors=[config.go, Load()]
- "config_config_envbool": "envBool()" | kind=code-symbol | source=probe-go/config/config.go:L102 | neighbors=[config.go, Load()]
- "config_config_envduration": "envDuration()" | kind=code-symbol | source=probe-go/config/config.go:L110 | neighbors=[config.go, Load()]
- "config_config_envint": "envInt()" | kind=code-symbol | source=probe-go/config/config.go:L93 | neighbors=[config.go, Load()]
- "config_config_hostname": "hostname()" | kind=code-symbol | source=probe-go/config/config.go:L119 | neighbors=[config.go, Load()]
- "config_config_loadfile": "loadFile()" | kind=code-symbol | source=probe-go/config/config.go:L64 | neighbors=[config.go, Load()]
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L83 | neighbors=[page.tsx, LiveOverview.tsx]
- "dashboard_protocolrow_riskcolor": "riskColor()" | kind=code-symbol | source=manager/frontend/components/dashboard/ProtocolRow.tsx:L6 | neighbors=[ProtocolRow.tsx, ProtocolRow()]
- "dashboard_slarow_getsla": "getSla()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L6 | neighbors=[SlaRow.tsx, SlaRow()]
- "dashboard_slastatus_pct": "pct()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L54 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "dashboard_slastatus_slastatus": "SlaStatus()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L115 | neighbors=[page.tsx, SlaStatus.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-044.json

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
