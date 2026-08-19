# Node Description Batch 49 of 227

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

- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=probe/agent/cli.py:L528 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=probe/agent/cli.py:L391 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=probe/agent/cli.py:L94 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()]
- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=probe/agent/cli.py:L88 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()]
- "agent_engine_scan_method_for": "_scan_method_for()" | kind=code-symbol | source=probe/agent/engine.py:L147 | neighbors=[engine.py, _applied_tuning(), syn' for wide sweeps (deep intensity / …, run_scan()]
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…]
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…, Combined startup gauntlet: HW bind → li…]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L27 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job(), Structured result from running one scan…]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L46 | neighbors=[Args:             http_get:       Callb…, TaskRunner, Args:             http_get:       Callb…, Args:             http_get:       Callb…]
- "agent_transport_devicealreadyenrollederror": "DeviceAlreadyEnrolledError" | kind=code-symbol | source=probe/agent/transport.py:L35 | neighbors=[transport.py, TransportError, The probe's device signing key is alrea…, .create_enrollment_request()]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L55 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_refresh_device_access": ".refresh_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L379 | neighbors=[Transport, .ensure_device_access(), .load_state(), .update_state()]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L221 | neighbors=[Transport, .bootstrap(), .register(), .update_state()]
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=probe/agent/use_cases.py:L195 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code()]
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=probe/agent/use_cases.py:L217 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve()]
- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=probe/agent/use_cases.py:L206 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int()]
- "ai_agent_agentdecisionengine_overview": "._overview()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L264 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), ._count(), _val()]
- "ai_agent_agentdecisionengine_persist": "._persist()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L347 | neighbors=[AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), .run()]
- "ai_hallucination": "hallucination.py" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[HallucinationGuard, HallucinationGuard — post-generation va…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_enum": "_enum()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L334 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding(), _remediation_plan_prompt()]
- "ai_llm_report_llmreportgenerator_complete": "._complete()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L112 | neighbors=[LLMReportGenerator, LLMUnavailableError, ._generate_and_store(), .generate_remediation_plan()]
- "ai_llm_report_llmreportgenerator_generate_remediation_steps": ".generate_remediation_steps()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L224 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]
- "ai_llm_report_llmreportgenerator_generate_technical_finding": ".generate_technical_finding()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L199 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]
- "ai_llm_report_parse_json_response": "_parse_json_response()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L381 | neighbors=[llm_report.py, .generate_remediation_plan(), Fault-tolerant JSON extraction from an …, Fault-tolerant JSON extraction from an …]
- "ai_llm_report_rationale_1": "LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses" | kind=entity | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[llm_report.py, HallucinationGuard, ReviewStatus, LLMOutput]
- "ai_llm_report_rationale_47": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/llm_report.py:L47 | neighbors=[LLMUnavailableError, HallucinationGuard, ReviewStatus, LLMOutput]
- "ai_llm_report_safe_commands": "_safe_commands()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L408 | neighbors=[llm_report.py, _normalize_ai_plan(), Extract a step's command(s) and drop an…, Extract a step's command(s) and drop an…]
- "ai_verification_graph": "verification_graph.py" | kind=code-symbol | source=manager/backend/app/ai/verification_graph.py:L1 | neighbors=[graph_available(), run_verification(), verification_graph.py — optional LangGr…, c02c465 feat(verification): optional La…]
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L120 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware]
- "assistant_assistantprovider_useassistant": "useAssistant()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L16 | neighbors=[AssistantDrawer.tsx, AssistantFab.tsx, AssistantProvider.tsx, page.tsx]
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L65 | neighbors=[TenantIsolationMiddleware, agent_jwt_path_allows(), _is_public_enrollment_request(), ._authenticate_pat()]
- "auth_portal_scope_client_scoped": "client_scoped()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L61 | neighbors=[portal_scope.py, assert_client(), The single choke point every portal SEL…, The single choke point every portal SEL…]
- "auth_portal_scope_require_client": "require_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L72 | neighbors=[portal_scope.py, Role gate for portal routes — 403 unles…, assert_client(), Role gate for portal routes — 403 unles…]
- "auth_portal_scope_scoped_engagement": "scoped_engagement()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L80 | neighbors=[portal_scope.py, Route dependency yielding the client's …, resolve_scope(), Route dependency yielding the client's …]
- "auth_rbac": "rbac.py" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L1 | neighbors=[dependencies.py, require_role(), d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
