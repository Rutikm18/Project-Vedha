# Node Description Batch 68 of 104

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

- "auth_router_me": "me()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L33 | neighbors=[router.py]
- "auth_router_revoke_personal_access_token": "revoke_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L175 | neighbors=[router.py]
- "basehttpmiddleware": "BaseHTTPMiddleware" | kind=code-symbol | neighbors=[TenantIsolationMiddleware]
- "basesettings": "BaseSettings" | kind=code-symbol | neighbors=[Settings]
- "brain_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L12 | neighbors=[route.ts]
- "chokepoints_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/chokepoints/route.ts:L5 | neighbors=[route.ts]
- "cli_auth_session": "Session" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L8 | neighbors=[auth.ts]
- "cli_auth_session_dir": "SESSION_DIR" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L5 | neighbors=[auth.ts]
- "cli_auth_session_file": "SESSION_FILE" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L6 | neighbors=[auth.ts]
- "cli_index_program": "program" | kind=code-symbol | source=manager/frontend/cli/index.ts:L32 | neighbors=[index.ts]
- "cli_llm_exploitplan": "ExploitPlan" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L265 | neighbors=[llm.ts]
- "cli_llm_phase_labels": "PHASE_LABELS" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L211 | neighbors=[llm.ts]
- "cli_llm_phaseid": "PhaseId" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L203 | neighbors=[llm.ts]
- "cli_llm_phaserecommendation": "PhaseRecommendation" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L205 | neighbors=[llm.ts]
- "cli_llm_validationverdict": "ValidationVerdict" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L127 | neighbors=[llm.ts]
- "commands_admin_c": "c" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L5 | neighbors=[admin.ts]
- "commands_ask_convmessage": "ConvMessage" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L8 | neighbors=[ask.ts]
- "commands_ask_runinteractive": "runInteractive()" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L10 | neighbors=[ask.ts]
- "commands_doctor_c": "C" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L22 | neighbors=[doctor.ts]
- "commands_doctor_checkdatadir": "checkDataDir()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L159 | neighbors=[doctor.ts]
- "commands_doctor_checkenvfile": "checkEnvFile()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L116 | neighbors=[doctor.ts]
- "commands_doctor_checkenvkey": "checkEnvKey()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L129 | neighbors=[doctor.ts]
- "commands_doctor_checknode": "checkNode()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L80 | neighbors=[doctor.ts]
- "commands_doctor_checknodemodules": "checkNodeModules()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L148 | neighbors=[doctor.ts]
- "commands_doctor_checkresult": "CheckResult" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L14 | neighbors=[doctor.ts]
- "commands_doctor_checkserver": "checkServer()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L188 | neighbors=[doctor.ts]
- "commands_doctor_checksession": "checkSession()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L170 | neighbors=[doctor.ts]
- "commands_doctor_w": "w()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L33 | neighbors=[doctor.ts]
- "commands_engagement_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L4 | neighbors=[engagement.ts]
- "commands_engagement_errexit": "errExit()" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L31 | neighbors=[engagement.ts]
- "commands_engagement_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L23 | neighbors=[engagement.ts]
- "commands_interactive_a": "A" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L26 | neighbors=[interactive.ts]
- "commands_interactive_engagementrow": "EngagementRow" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1741 | neighbors=[interactive.ts]
- "commands_interactive_issinglehost": "isSingleHost()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L189 | neighbors=[interactive.ts]
- "commands_interactive_makerl": "makeRl()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L35 | neighbors=[interactive.ts]
- "commands_interactive_phasestate": "PhaseState" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L809 | neighbors=[interactive.ts]
- "commands_interactive_targetspec": "TargetSpec" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L182 | neighbors=[interactive.ts]
- "commands_interactive_tool": "Tool" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L293 | neighbors=[interactive.ts]
- "commands_login_prompt": "prompt()" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L5 | neighbors=[login.ts]
- "commands_login_promptsilent": "promptSilent()" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L15 | neighbors=[login.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-067.json

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
