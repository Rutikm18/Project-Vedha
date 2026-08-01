# Node Description Batch 50 of 119

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

- "ai_agent_agentdecisionengine_count": "._count()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L329 | neighbors=[AgentDecisionEngine, ._overview()]
- "ai_agent_agentdecisionengine_create": "._create()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L235 | neighbors=[AgentDecisionEngine, .run()]
- "ai_agent_agentdecisionengine_list_assets": "._list_assets()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L296 | neighbors=[AgentDecisionEngine, ._exec_read_tool()]
- "ai_agent_agentdecisionengine_list_attack_paths": "._list_attack_paths()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L317 | neighbors=[AgentDecisionEngine, ._exec_read_tool()]
- "ai_agent_maybe_decimal": "_maybe_decimal()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L395 | neighbors=[agent.py, ._persist()]
- "ai_agent_maybe_uuid": "_maybe_uuid()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L386 | neighbors=[agent.py, ._persist()]
- "ai_agent_tool_result": "_tool_result()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L377 | neighbors=[agent.py, .run()]
- "ai_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/ai/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_collect_cves_scores": "_collect_cves_scores()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L332 | neighbors=[llm_report.py, .generate_executive_summary()]
- "ai_llm_report_llmreportgenerator_generate_detection_rule_explanation": ".generate_detection_rule_explanation()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L243 | neighbors=[LLMReportGenerator, ._generate_and_store()]
- "ai_llm_report_uuid": "_uuid()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L314 | neighbors=[llm_report.py, ._generate_and_store()]
- "ai_prioritizer_to_float": "_to_float()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L61 | neighbors=[prioritizer.py, extract_features()]
- "ai_prioritizer_vulnprioritizer_train": ".train()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L110 | neighbors=[Fit an XGBoost regressor on historical …, VulnPrioritizer]
- "aibrain_page_aibrainpage": "AIBrainPage()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L79 | neighbors=[page.tsx, providerLabel()]
- "aibrain_page_providerlabel": "providerLabel()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L73 | neighbors=[page.tsx, AIBrainPage()]
- "app_config_get_settings": "get_settings()" | kind=code-symbol | source=manager/backend/app/config.py:L102 | neighbors=[config.py, Settings]
- "app_database_get_read_db": "get_read_db()" | kind=code-symbol | source=manager/backend/app/database.py:L56 | neighbors=[database.py, Read-only session (no commit) routed to…]
- "app_dependencies_close_redis": "close_redis()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L26 | neighbors=[dependencies.py, Close the global Redis connection pool.…]
- "app_dependencies_get_current_user": "get_current_user()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L35 | neighbors=[dependencies.py, Reads user claims injected by TenantIso…]
- "app_dependencies_rationale_27": "Close the global Redis connection pool. Call during app shutdown." | kind=entity | source=manager/backend/app/dependencies.py:L27 | neighbors=[close_redis(), CurrentUser]
- "app_dependencies_rationale_36": "Reads user claims injected by TenantIsolationMiddleware.     Raises 401 if middl" | kind=entity | source=manager/backend/app/dependencies.py:L36 | neighbors=[get_current_user(), CurrentUser]
- "app_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "app_main_rationale_198": "Identify the Manager API without exposing a second dashboard." | kind=entity | source=manager/backend/app/main.py:L198 | neighbors=[_service_root(), TenantIsolationMiddleware]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L197 | neighbors=[main.py, Identify the Manager API without exposi…]
- "app_ratelimit_client_ip": "client_ip()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L16 | neighbors=[ratelimit.py, Best-effort client IP. Honors X-Forward…]
- "app_ratelimit_rate_limit": "rate_limit()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L43 | neighbors=[ratelimit.py, FastAPI dependency factory. Keys the wi…]
- "assistant_assistantdrawer_assistantdrawer": "AssistantDrawer()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L12 | neighbors=[AssistantDrawer.tsx, AssistantProvider.tsx]
- "assistant_assistantfab_assistantfab": "AssistantFab()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L6 | neighbors=[AssistantFab.tsx, AssistantProvider.tsx]
- "assistant_assistantprovider_assistantprovider": "AssistantProvider()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L22 | neighbors=[layout.tsx, AssistantProvider.tsx]
- "auth_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/auth/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "auth_jwt_create_access_token": "create_access_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L20 | neighbors=[jwt.py, _now()]
- "auth_middleware_tenantisolationmiddleware_authenticate_pat": "._authenticate_pat()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L93 | neighbors=[TenantIsolationMiddleware, .dispatch()]
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L26 | neighbors=[TenantIsolationMiddleware, ._authenticate_pat()]
- "auth_pat_hash_pat_token": "hash_pat_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L36 | neighbors=[pat.py, build_personal_access_token()]
- "auth_pat_new_pat_token": "new_pat_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L32 | neighbors=[pat.py, build_personal_access_token()]
- "auth_pat_pat_display_prefix": "pat_display_prefix()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L40 | neighbors=[pat.py, build_personal_access_token()]
- "auth_pat_validate_pat_scopes": "validate_pat_scopes()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L44 | neighbors=[pat.py, build_personal_access_token()]
- "auth_rbac_rationale_10": "FastAPI dependency that enforces role-based access.      Usage:         @router." | kind=entity | source=manager/backend/app/auth/rbac.py:L10 | neighbors=[require_role(), CurrentUser]
- "auth_rbac_require_role": "require_role()" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L9 | neighbors=[rbac.py, FastAPI dependency that enforces role-b…]
- "auth_router_create_personal_access_token": "create_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L99 | neighbors=[router.py, refresh()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-049.json

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
