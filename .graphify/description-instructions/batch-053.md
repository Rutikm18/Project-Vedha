# Node Description Batch 54 of 131

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

- "agent_engine_env_number": "_env_number()" | kind=code-symbol | source=probe/agent/engine.py:L45 | neighbors=[engine.py, Read a bounded numeric safety setting w…]
- "agent_engine_facts_from_cache": "_facts_from_cache()" | kind=code-symbol | source=probe/agent/engine.py:L252 | neighbors=[engine.py, run_scan()]
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L45 | neighbors=[license.py, verify_license()]
- "agent_result_spool_resultspool_at_capacity": ".at_capacity()" | kind=code-symbol | source=probe/agent/result_spool.py:L235 | neighbors=[Whether new jobs must pause until pendi…, ResultSpool]
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…]
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…]
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…]
- "agent_scope_validator_rationale_58": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L58 | neighbors=[fetch_engagement_scope(), validate_targets_in_scope()]
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L15 | neighbors=[agent.py, tools.ts]
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L313 | neighbors=[agent.py, tools.ts]
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L24 | neighbors=[agent.py, tools.ts]
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L98 | neighbors=[agent.py, tools.ts]
- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L26 | neighbors=[agent.py, tools.ts]
- "agent_transport_rationale_354": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L354 | neighbors=[.fetch_scope(), .is_ws_connected()]
- "agent_transport_transport_clear_state": ".clear_state()" | kind=code-symbol | source=probe/agent/transport.py:L207 | neighbors=[Transport, .update_state()]
- "agent_transport_transport_close": ".close()" | kind=code-symbol | source=probe/agent/transport.py:L667 | neighbors=[_sync_directory(), Transport]
- "agent_transport_transport_init": ".__init__()" | kind=code-symbol | source=probe/agent/transport.py:L85 | neighbors=[Transport, .load_state()]
- "agent_validation_metric": "_metric()" | kind=code-symbol | source=probe/agent/validation.py:L173 | neighbors=[validation.py, score_inventory()]
- "agent_validation_not_scored": "_not_scored()" | kind=code-symbol | source=probe/agent/validation.py:L197 | neighbors=[validation.py, score_inventory()]
- "agent_validation_resolve_use_cases": "resolve_use_cases()" | kind=code-symbol | source=probe/agent/validation.py:L38 | neighbors=[validation.py, Resolve suites plus explicit use-cases,…]
- "agent_validation_target_address_count": "target_address_count()" | kind=code-symbol | source=probe/agent/validation.py:L93 | neighbors=[validation.py, Return the conservative number of addre…]
- "agent_validation_validate_targets": "validate_targets()" | kind=code-symbol | source=probe/agent/validation.py:L55 | neighbors=[validation.py, Require every IP/CIDR target to be full…]
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
- "app_config_get_settings": "get_settings()" | kind=code-symbol | source=manager/backend/app/config.py:L121 | neighbors=[config.py, Settings]
- "app_dependencies_close_redis": "close_redis()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L26 | neighbors=[dependencies.py, Close the global Redis connection pool.…]
- "app_dependencies_get_current_user": "get_current_user()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L35 | neighbors=[dependencies.py, Reads user claims injected by TenantIso…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-053.json

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
