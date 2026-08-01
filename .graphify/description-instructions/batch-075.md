# Node Description Batch 76 of 119

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

- "cli_llm_phaserecommendation": "PhaseRecommendation" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L205 | neighbors=[llm.ts]
- "cli_llm_validationverdict": "ValidationVerdict" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L127 | neighbors=[llm.ts]
- "commands_admin_c": "c" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L5 | neighbors=[admin.ts]
- "commands_ask_convmessage": "ConvMessage" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L8 | neighbors=[ask.ts]
- "commands_ask_runinteractive": "runInteractive()" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L10 | neighbors=[ask.ts]
- "commands_doctor_c": "C" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L22 | neighbors=[doctor.ts]
- "commands_doctor_checkdatadir": "checkDataDir()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L158 | neighbors=[doctor.ts]
- "commands_doctor_checkenvfile": "checkEnvFile()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L115 | neighbors=[doctor.ts]
- "commands_doctor_checkenvkey": "checkEnvKey()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L128 | neighbors=[doctor.ts]
- "commands_doctor_checknode": "checkNode()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L79 | neighbors=[doctor.ts]
- "commands_doctor_checknodemodules": "checkNodeModules()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L147 | neighbors=[doctor.ts]
- "commands_doctor_checkresult": "CheckResult" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L14 | neighbors=[doctor.ts]
- "commands_doctor_checkserver": "checkServer()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L187 | neighbors=[doctor.ts]
- "commands_doctor_checksession": "checkSession()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L169 | neighbors=[doctor.ts]
- "commands_doctor_w": "w()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L33 | neighbors=[doctor.ts]
- "commands_engagement_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L4 | neighbors=[engagement.ts]
- "commands_engagement_errexit": "errExit()" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L31 | neighbors=[engagement.ts]
- "commands_engagement_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L23 | neighbors=[engagement.ts]
- "commands_interactive_a": "A" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L26 | neighbors=[interactive.ts]
- "commands_interactive_engagementrow": "EngagementRow" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1738 | neighbors=[interactive.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-075.json

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
