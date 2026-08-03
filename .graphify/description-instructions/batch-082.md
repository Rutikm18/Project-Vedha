# Node Description Batch 83 of 131

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

- "auth_startup_rationale_148": "Verify the bcrypt library can round-trip a hash — catches misconfigured passlib." | kind=entity | source=manager/backend/app/auth/startup.py:L148 | neighbors=[_check_bcrypt()]
- "auth_startup_rationale_160": "Verify the seeded admin account exists and is active." | kind=entity | source=manager/backend/app/auth/startup.py:L160 | neighbors=[_check_admin_account()]
- "auth_startup_rationale_198": "Verify the default tenant is active." | kind=entity | source=manager/backend/app/auth/startup.py:L198 | neighbors=[_check_tenant()]
- "auth_startup_rationale_283": "Run all startup checks concurrently.     Called from FastAPI lifespan before the" | kind=entity | source=manager/backend/app/auth/startup.py:L283 | neighbors=[run_startup_diagnostics()]
- "auth_startup_rationale_93": "Raised when one or more fatal checks fail — aborts app startup." | kind=entity | source=manager/backend/app/auth/startup.py:L93 | neighbors=[StartupAbortError]
- "basehttpmiddleware": "BaseHTTPMiddleware" | kind=code-symbol | neighbors=[TenantIsolationMiddleware]
- "basesettings": "BaseSettings" | kind=code-symbol | neighbors=[Settings]
- "brain_route_aimessage": "AiMessage" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L6 | neighbors=[route.ts]
- "brain_route_evidencetext": "evidenceText()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L40 | neighbors=[route.ts]
- "brain_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L11 | neighbors=[route.ts]
- "chat_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L11 | neighbors=[route.ts]
- "chat_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L20 | neighbors=[route.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-082.json

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
