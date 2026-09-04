# Node Description Batch 68 of 330

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "agent_task_runner_taskrunner_archive_result": "._archive_result()" | kind=code-symbol | source=probe/agent/task_runner.py:L507 | neighbors=[Write the outbound payload to the local…, TaskRunner, _result_dir(), ._submit_or_spool()] | lang=en
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L119 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()] | lang=en
- "agent_transport_transport_activate_enrollment": ".activate_enrollment()" | kind=code-symbol | source=probe/agent/transport.py:L423 | neighbors=[Transport, manager_fingerprint(), .load_state(), .update_state()] | lang=en
- "agent_transport_transport_heartbeat_ex": ".heartbeat_ex()" | kind=code-symbol | source=probe/agent/transport.py:L582 | neighbors=[Send a heartbeat and report WHY it fail…, Transport, .heartbeat(), .ensure_device_access()] | lang=en
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L293 | neighbors=[Transport, .bootstrap(), .register(), .update_state()] | lang=en
- "ai_agent_agentdecisionengine_overview": "._overview()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L264 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), ._count(), _val()] | lang=en
- "ai_agent_agentdecisionengine_persist": "._persist()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L347 | neighbors=[AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), .run()] | lang=en
- "ai_hallucination": "hallucination.py" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[HallucinationGuard, HallucinationGuard — post-generation va…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "ai_llm_report_enum": "_enum()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L334 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding(), _remediation_plan_prompt()] | lang=en
- "ai_llm_report_llmreportgenerator_complete": "._complete()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L112 | neighbors=[LLMReportGenerator, LLMUnavailableError, ._generate_and_store(), .generate_remediation_plan()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_remediation_steps": ".generate_remediation_steps()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L224 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_technical_finding": ".generate_technical_finding()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L199 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()] | lang=en
- "ai_llm_report_parse_json_response": "_parse_json_response()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L381 | neighbors=[llm_report.py, .generate_remediation_plan(), Fault-tolerant JSON extraction from an …, Fault-tolerant JSON extraction from an …] | lang=en
- "ai_llm_report_rationale_1": "LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses" | kind=entity | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[llm_report.py, HallucinationGuard, ReviewStatus, LLMOutput] | lang=en
- "ai_llm_report_rationale_47": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/llm_report.py:L47 | neighbors=[LLMUnavailableError, HallucinationGuard, ReviewStatus, LLMOutput] | lang=en
- "ai_llm_report_safe_commands": "_safe_commands()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L408 | neighbors=[llm_report.py, _normalize_ai_plan(), Extract a step's command(s) and drop an…, Extract a step's command(s) and drop an…] | lang=en
- "ai_verification_graph": "verification_graph.py" | kind=code-symbol | source=manager/backend/app/ai/verification_graph.py:L1 | neighbors=[graph_available(), run_verification(), verification_graph.py — optional LangGr…, c02c465 feat(verification): optional La…] | lang=en
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L132 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware] | lang=en
- "assistant_assistantprovider_useassistant": "useAssistant()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L22 | neighbors=[AssistantDrawer.tsx, AssistantFab.tsx, AssistantProvider.tsx, page.tsx] | lang=en
- "assistant_factcard_factcard": "FactCard()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L26 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, lifecycleSummary()] | lang=en
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L65 | neighbors=[TenantIsolationMiddleware, agent_jwt_path_allows(), _is_public_enrollment_request(), ._authenticate_pat()] | lang=en
- "auth_portal_scope_client_scoped": "client_scoped()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L61 | neighbors=[portal_scope.py, assert_client(), The single choke point every portal SEL…, The single choke point every portal SEL…] | lang=en
- "auth_portal_scope_require_client": "require_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L72 | neighbors=[portal_scope.py, Role gate for portal routes — 403 unles…, assert_client(), Role gate for portal routes — 403 unles…] | lang=en
- "auth_portal_scope_scoped_engagement": "scoped_engagement()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L80 | neighbors=[portal_scope.py, Route dependency yielding the client's …, resolve_scope(), Route dependency yielding the client's …] | lang=en
- "auth_rbac": "rbac.py" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L1 | neighbors=[dependencies.py, require_role(), d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_router_authenticate": "_authenticate()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L58 | neighbors=[router.py, login(), Validates credentials and returns the U…, Validates credentials and returns the U…] | lang=en
- "commands_interactive_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L104 | neighbors=[interactive.ts, ln(), runInteractive(), wizardScan()] | lang=en
- "commands_interactive_choosenextphase": "chooseNextPhase()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L927 | neighbors=[interactive.ts, choose(), ln(), runIterativeEngagement()] | lang=en
- "commands_interactive_pickmodulesbycategory": "pickModulesByCategory()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L300 | neighbors=[interactive.ts, confirm(), ln(), wizardScan()] | lang=en
- "commands_interactive_runrulebasedvalidation": "runRuleBasedValidation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1355 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardstatus": "wizardStatus()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1938 | neighbors=[interactive.ts, mainMenu(), divider(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 298a9d4 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, a388bb3 script updated, architecture de…, f5ce592 first commit] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, agents/greeting-introduction, main, bd7383f scanner fine ..now integrations] | lang=fr
- "components_queryprovider": "QueryProvider.tsx" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, QueryProvider(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "components_refreshbutton_refreshbutton": "RefreshButton()" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L30 | neighbors=[PageShell.tsx, RefreshButton.tsx, page.tsx, PortalShell.tsx] | lang=en
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L54 | neighbors=[PageShell.tsx, Sidebar.tsx, page.tsx, page.tsx] | lang=en
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L26 | neighbors=[PageShell.tsx, ThemeProvider.tsx, PortalShell.tsx, page.tsx] | lang=en
- "console_primitives_meter": "Meter()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L90 | neighbors=[Primitives.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx] | lang=en

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
