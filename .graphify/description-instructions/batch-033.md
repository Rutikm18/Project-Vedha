# Node Description Batch 34 of 76

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

- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L27 | neighbors=[agent.py, tools.ts]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L119 | neighbors=[use_cases.py, Return (scan_type, profile) for a job. …]
- "ai_llm_report_collect_cves_scores": "_collect_cves_scores()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L332 | neighbors=[llm_report.py, .generate_executive_summary()]
- "ai_llm_report_llmreportgenerator_generate_detection_rule_explanation": ".generate_detection_rule_explanation()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L243 | neighbors=[LLMReportGenerator, ._generate_and_store()]
- "ai_llm_report_uuid": "_uuid()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L314 | neighbors=[llm_report.py, ._generate_and_store()]
- "ai_prioritizer_to_float": "_to_float()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L61 | neighbors=[prioritizer.py, extract_features()]
- "ai_prioritizer_vulnprioritizer_train": ".train()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L110 | neighbors=[Fit an XGBoost regressor on historical …, VulnPrioritizer]
- "app_config_get_settings": "get_settings()" | kind=code-symbol | source=manager/backend/app/config.py:L86 | neighbors=[config.py, Settings]
- "app_database_get_read_db": "get_read_db()" | kind=code-symbol | source=manager/backend/app/database.py:L56 | neighbors=[database.py, Read-only session (no commit) routed to…]
- "app_dependencies_close_redis": "close_redis()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L26 | neighbors=[dependencies.py, Close the global Redis connection pool.…]
- "app_dependencies_get_current_user": "get_current_user()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L35 | neighbors=[dependencies.py, Reads user claims injected by TenantIso…]
- "app_dependencies_rationale_27": "Close the global Redis connection pool. Call during app shutdown." | kind=entity | source=manager/backend/app/dependencies.py:L27 | neighbors=[close_redis(), CurrentUser]
- "app_dependencies_rationale_36": "Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl" | kind=entity | source=manager/backend/app/dependencies.py:L36 | neighbors=[get_current_user(), CurrentUser]
- "app_ratelimit_client_ip": "client_ip()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L16 | neighbors=[ratelimit.py, Best-effort client IP. Honors X-Forward…]
- "app_ratelimit_rate_limit": "rate_limit()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L43 | neighbors=[ratelimit.py, FastAPI dependency factory. Keys the wi…]
- "auth_jwt_create_access_token": "create_access_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L20 | neighbors=[jwt.py, _now()]
- "auth_middleware_tenantisolationmiddleware_authenticate_pat": "._authenticate_pat()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L94 | neighbors=[TenantIsolationMiddleware, .dispatch()]
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L27 | neighbors=[TenantIsolationMiddleware, ._authenticate_pat()]
- "auth_rbac_rationale_10": "FastAPI dependency that enforces role-based access.      Usage:         @router." | kind=entity | source=manager/backend/app/auth/rbac.py:L10 | neighbors=[require_role(), CurrentUser]
- "auth_rbac_require_role": "require_role()" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L9 | neighbors=[rbac.py, FastAPI dependency that enforces role-b…]
- "auth_router_create_personal_access_token": "create_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L99 | neighbors=[router.py, refresh()]
- "auth_router_refresh": "refresh()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L70 | neighbors=[router.py, create_personal_access_token()]
- "cli_llm_commentonstage": "commentOnStage()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L22 | neighbors=[llm.ts, client()]
- "cli_llm_explainfindings": "explainFindings()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L54 | neighbors=[llm.ts, client()]
- "cli_llm_planexploit": "planExploit()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L278 | neighbors=[llm.ts, client()]
- "cli_llm_recommendnextphase": "recommendNextPhase()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L222 | neighbors=[llm.ts, client()]
- "cli_llm_suggestattackpath": "suggestAttackPath()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L92 | neighbors=[llm.ts, client()]
- "cli_llm_validatefindings": "validateFindings()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L138 | neighbors=[llm.ts, client()]
- "commands_admin_buildadmincommand": "buildAdminCommand()" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L13 | neighbors=[index.ts, admin.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-033.json

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
