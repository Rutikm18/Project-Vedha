# Node Description Batch 55 of 131

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

- "app_dependencies_rationale_27": "Close the global Redis connection pool. Call during app shutdown." | kind=entity | source=manager/backend/app/dependencies.py:L27 | neighbors=[close_redis(), CurrentUser]
- "app_dependencies_rationale_36": "Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl" | kind=entity | source=manager/backend/app/dependencies.py:L36 | neighbors=[get_current_user(), CurrentUser]
- "app_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "app_main_rationale_198": "Identify the Manager API without exposing a second dashboard." | kind=entity | source=manager/backend/app/main.py:L198 | neighbors=[_service_root(), TenantIsolationMiddleware]
- "app_ratelimit_client_ip": "client_ip()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L16 | neighbors=[ratelimit.py, Best-effort client IP. Honors X-Forward…]
- "app_ratelimit_rate_limit": "rate_limit()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L43 | neighbors=[ratelimit.py, FastAPI dependency factory. Keys the wi…]
- "assistant_assistantdrawer_assistantdrawer": "AssistantDrawer()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L12 | neighbors=[AssistantDrawer.tsx, AssistantProvider.tsx]
- "assistant_assistantfab_assistantfab": "AssistantFab()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L6 | neighbors=[AssistantFab.tsx, AssistantProvider.tsx]
- "assistant_assistantprovider_assistantprovider": "AssistantProvider()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L22 | neighbors=[layout.tsx, AssistantProvider.tsx]
- "auth_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/auth/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "auth_jwt_create_device_access_token": "create_device_access_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L40 | neighbors=[jwt.py, create_access_token()]
- "auth_middleware_is_public_enrollment_request": "_is_public_enrollment_request()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L33 | neighbors=[middleware.py, .dispatch()]
- "auth_middleware_tenantisolationmiddleware_authenticate_pat": "._authenticate_pat()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L180 | neighbors=[TenantIsolationMiddleware, .dispatch()]
- "auth_pat_hash_pat_token": "hash_pat_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L36 | neighbors=[pat.py, build_personal_access_token()]
- "auth_pat_new_pat_token": "new_pat_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L32 | neighbors=[pat.py, build_personal_access_token()]
- "auth_pat_pat_display_prefix": "pat_display_prefix()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L40 | neighbors=[pat.py, build_personal_access_token()]
- "auth_pat_validate_pat_scopes": "validate_pat_scopes()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L44 | neighbors=[pat.py, build_personal_access_token()]
- "auth_rbac_rationale_10": "FastAPI dependency that enforces role-based access.      Usage:         @router." | kind=entity | source=manager/backend/app/auth/rbac.py:L10 | neighbors=[require_role(), CurrentUser]
- "auth_rbac_require_role": "require_role()" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L9 | neighbors=[rbac.py, FastAPI dependency that enforces role-b…]
- "auth_router_create_personal_access_token": "create_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L238 | neighbors=[router.py, refresh()]
- "auth_router_login": "login()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L120 | neighbors=[router.py, _authenticate()]
- "auth_router_refresh": "refresh()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L209 | neighbors=[router.py, create_personal_access_token()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-054.json

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
