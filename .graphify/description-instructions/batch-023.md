# Node Description Batch 24 of 104

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

- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=probe/agent/cli.py:L86 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()] | lang=en
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L476 | neighbors=[cli.py, cmd_scan_run(), CliError, .request()] | lang=en
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L151 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run()] | lang=en
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L86 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp()] | lang=en
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…] | lang=en
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…] | lang=en
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L38 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license()] | lang=en
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L44 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()] | lang=en
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=probe/agent/task_runner.py:L79 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._submit_or_spool()] | lang=en
- "agent_transport_post": ".post()" | kind=code-symbol | source=probe-go/agent/transport.go:L133 | neighbors=[transport.py, .Login(), .Register(), .SubmitResult()] | lang=en
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L132 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError] | lang=en
- "ai_agent_agentdecisionengine_overview": "._overview()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L264 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), ._count(), _val()] | lang=en
- "ai_agent_agentdecisionengine_persist": "._persist()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L336 | neighbors=[AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), .run()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_remediation_steps": ".generate_remediation_steps()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L222 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_technical_finding": ".generate_technical_finding()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L197 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()] | lang=en
- "ai_llm_report_rationale_1": "LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses" | kind=entity | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[HallucinationGuard, llm_report.py, ReviewStatus, LLMOutput] | lang=en
- "ai_llm_report_rationale_47": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/llm_report.py:L47 | neighbors=[HallucinationGuard, LLMUnavailableError, ReviewStatus, LLMOutput] | lang=en
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L92 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware] | lang=en
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graph-store.ts, graphStore, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graph-store.ts, graphStore, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "attack_paths_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L1 | neighbors=[GET(), graph-store.ts, graphStore, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, TenantIsolationMiddleware, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "chokepoints_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/chokepoints/route.ts:L1 | neighbors=[GET(), graph-store.ts, graphStore, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "commands_interactive_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L104 | neighbors=[interactive.ts, ln(), runInteractive(), wizardScan()] | lang=en
- "commands_interactive_choosenextphase": "chooseNextPhase()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L927 | neighbors=[interactive.ts, choose(), ln(), runIterativeEngagement()] | lang=en
- "commands_interactive_pickmodulesbycategory": "pickModulesByCategory()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L300 | neighbors=[interactive.ts, confirm(), ln(), wizardScan()] | lang=en
- "commands_interactive_runrulebasedvalidation": "runRuleBasedValidation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1358 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardstatus": "wizardStatus()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1941 | neighbors=[interactive.ts, mainMenu(), divider(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 298a9d4 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, a388bb3 script updated, architecture de…, f5ce592 first commit] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, agents/greeting-introduction, main, bd7383f scanner fine ..now integrations] | lang=fr
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L47 | neighbors=[page.tsx, PageShell.tsx, Sidebar.tsx, page.tsx] | lang=en
- "dashboard_protocolrow_protocolrow": "ProtocolRow()" | kind=code-symbol | source=manager/frontend/components/dashboard/ProtocolRow.tsx:L10 | neighbors=[Exposure.tsx, ProtocolRow.tsx, riskColor(), page.tsx] | lang=en
- "dashboard_slasummarycell": "SlaSummaryCell.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaSummaryCell.tsx:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, SlaSummaryCell(), SlaSummaryMetric, page.tsx] | lang=en
- "detection_correlator_aware": "_aware()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L209 | neighbors=[correlator.py, ._in_window(), ._min_latency(), Normalise naive datetimes to UTC so com…] | lang=en
- "detection_edr_edrqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L78 | neighbors=[.query_detections(), EDRQueryEngine, .query_detections(), .query_detections()] | lang=en
- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()] | lang=en
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L82 | neighbors=[engine_bridge.py, create_findings_from_facts(), _ensure_importable(), facts (ScanResult dicts) -> detection_e…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-023.json

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
