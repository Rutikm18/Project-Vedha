# Node Description Batch 51 of 119

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "auth_router_refresh": "refresh()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L70 | neighbors=[router.py, create_personal_access_token()]
- "brain_route_validmessages": "validMessages()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L21 | neighbors=[route.ts, POST()]
- "cli_llm_commentonstage": "commentOnStage()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L22 | neighbors=[llm.ts, client()]
- "cli_llm_explainfindings": "explainFindings()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L54 | neighbors=[llm.ts, client()]
- "cli_llm_planexploit": "planExploit()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L278 | neighbors=[llm.ts, client()]
- "cli_llm_recommendnextphase": "recommendNextPhase()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L222 | neighbors=[llm.ts, client()]
- "cli_llm_suggestattackpath": "suggestAttackPath()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L92 | neighbors=[llm.ts, client()]
- "cli_llm_validatefindings": "validateFindings()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L138 | neighbors=[llm.ts, client()]
- "commands_admin_buildadmincommand": "buildAdminCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L13 | neighbors=[index.ts, admin.ts]
- "commands_ask_buildaskcommand": "buildAskCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L59 | neighbors=[index.ts, ask.ts]
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
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5e2d0ed7a2fe2e171616a98cebb2295cf557314": "c5e2d0e chore: retire probe-go to spike/probe-go branch" | kind=Commit | source=git | neighbors=[1fe16c8 stable but some dead code, need…, feat/probe-usecase-alignment]
- "components_dashboardcharts_dashboardcharts": "DashboardCharts()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L218 | neighbors=[page.tsx, DashboardCharts.tsx]
- "components_queryprovider_queryprovider": "QueryProvider()" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L6 | neighbors=[layout.tsx, QueryProvider.tsx]
- "components_themeprovider_themeprovider": "ThemeProvider()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L30 | neighbors=[layout.tsx, ThemeProvider.tsx]
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L26 | neighbors=[PageShell.tsx, ThemeProvider.tsx]
- "components_toastprovider_toastcontext": "ToastContext" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L26 | neighbors=[ToastProvider.tsx, useToast.ts]
- "components_toastprovider_toastprovider": "ToastProvider()" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L159 | neighbors=[layout.tsx, ToastProvider.tsx]
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L82 | neighbors=[page.tsx, LiveOverview.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-050.json

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
