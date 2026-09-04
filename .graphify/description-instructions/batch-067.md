# Node Description Batch 68 of 332

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

- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…, Combined startup gauntlet: HW bind → li…]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_local_run_summarize": "summarize()" | kind=code-symbol | source=probe/agent/local_run.py:L90 | neighbors=[local_run.py, _main(), _clean(), _port_label()]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…]
- "agent_task_runner_taskrunner_archive_result": "._archive_result()" | kind=code-symbol | source=probe/agent/task_runner.py:L507 | neighbors=[Write the outbound payload to the local…, TaskRunner, _result_dir(), ._submit_or_spool()]
- "agent_transport_manager_fingerprint": "manager_fingerprint()" | kind=code-symbol | source=probe/agent/transport.py:L104 | neighbors=[transport.py, Stable identity for the manager a crede…, .activate_enrollment(), Stable identity for the manager a crede…]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L131 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L305 | neighbors=[Transport, .bootstrap(), .register(), .update_state()]
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
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L132 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware]
- "assistant_assistantprovider_useassistant": "useAssistant()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L22 | neighbors=[AssistantDrawer.tsx, AssistantFab.tsx, AssistantProvider.tsx, page.tsx]
- "assistant_factcard_factcard": "FactCard()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L26 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, lifecycleSummary()]
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L65 | neighbors=[TenantIsolationMiddleware, agent_jwt_path_allows(), _is_public_enrollment_request(), ._authenticate_pat()]
- "auth_portal_scope_client_scoped": "client_scoped()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L61 | neighbors=[portal_scope.py, assert_client(), The single choke point every portal SEL…, The single choke point every portal SEL…]
- "auth_portal_scope_require_client": "require_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L72 | neighbors=[portal_scope.py, Role gate for portal routes — 403 unles…, assert_client(), Role gate for portal routes — 403 unles…]
- "auth_portal_scope_scoped_engagement": "scoped_engagement()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L80 | neighbors=[portal_scope.py, Route dependency yielding the client's …, resolve_scope(), Route dependency yielding the client's …]
- "auth_rbac": "rbac.py" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L1 | neighbors=[dependencies.py, require_role(), d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "auth_router_authenticate": "_authenticate()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L58 | neighbors=[router.py, login(), Validates credentials and returns the U…, Validates credentials and returns the U…]
- "commands_interactive_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L104 | neighbors=[interactive.ts, ln(), runInteractive(), wizardScan()]
- "commands_interactive_choosenextphase": "chooseNextPhase()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L927 | neighbors=[interactive.ts, choose(), ln(), runIterativeEngagement()]
- "commands_interactive_pickmodulesbycategory": "pickModulesByCategory()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L300 | neighbors=[interactive.ts, confirm(), ln(), wizardScan()]
- "commands_interactive_runrulebasedvalidation": "runRuleBasedValidation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1355 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardstatus": "wizardStatus()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1938 | neighbors=[interactive.ts, mainMenu(), divider(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 298a9d4 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, a388bb3 script updated, architecture de…, f5ce592 first commit]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-067.json

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
