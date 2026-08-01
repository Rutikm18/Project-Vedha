# Node Description Batch 68 of 119

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

- "workflow_execution_errordetail": "ErrorDetail" | kind=code-symbol | source=probe/workflow/execution.py:L147 | neighbors=[execution.py, classify_scanner_error()]
- "workflow_execution_executiontrace_as_list": ".as_list()" | kind=code-symbol | source=probe/workflow/execution.py:L364 | neighbors=[ExecutionTrace, ._has_active_coverage()]
- "workflow_execution_executiontrace_finalize": ".finalize()" | kind=code-symbol | source=probe/workflow/execution.py:L333 | neighbors=[ExecutionTrace, .skip()]
- "workflow_execution_executiontrace_init": ".__init__()" | kind=code-symbol | source=probe/workflow/execution.py:L234 | neighbors=[ExecutionTrace, ._ensure()]
- "workflow_execution_executiontrace_reused": ".reused()" | kind=code-symbol | source=probe/workflow/execution.py:L319 | neighbors=[ExecutionTrace, .record()]
- "workflow_execution_planned_components": "planned_components()" | kind=code-symbol | source=probe/workflow/execution.py:L96 | neighbors=[execution.py, Resolve the exact collector plan for on…]
- "workflow_gates_gate_2_host_discovery": "gate_2_host_discovery()" | kind=code-symbol | source=probe/workflow/gates.py:L54 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_gates_gate_3_port_scan": "gate_3_port_scan()" | kind=code-symbol | source=probe/workflow/gates.py:L61 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_modes_includes_stage": "includes_stage()" | kind=code-symbol | source=probe/workflow/modes.py:L45 | neighbors=[modes.py, Return whether a bounded plan includes …]
- "workflow_modes_resolve_stage_ceiling": "resolve_stage_ceiling()" | kind=code-symbol | source=probe/workflow/modes.py:L25 | neighbors=[modes.py, Resolve the explicit ceiling while pres…]
- "workflow_modes_service_specific": "service_specific()" | kind=code-symbol | source=probe/workflow/modes.py:L118 | neighbors=[modes.py, EngagementMode]
- "workflow_report_diff_assets": "diff_assets()" | kind=code-symbol | source=probe/workflow/report.py:L42 | neighbors=[report.py, re-scan mode's delta report: what chang…]
- "workflow_workflow_engine_finalize_trace": "_finalize_trace()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L219 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_record": "_record()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L193 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_record_reused": "_record_reused()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L210 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_store_results": "_store_results()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L178 | neighbors=[workflow_engine.py, run_engagement()]
- "activity_route_apiactivity": "ApiActivity" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L9 | neighbors=[route.ts]
- "activity_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L14 | neighbors=[route.ts]
- "ad_asreproast_asreproastchecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L106 | neighbors=[ASREPRoastChecker]
- "ad_bloodhound_bloodhoundcollector_close": ".close()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L267 | neighbors=[BloodHoundCollector]
- "ad_bloodhound_bloodhoundcollector_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L46 | neighbors=[BloodHoundCollector]
- "ad_ldap_enum_ldapenumerator_connection": ".connection()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L185 | neighbors=[LDAPEnumerator]
- "ad_ldap_enum_ldapenumerator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L120 | neighbors=[LDAPEnumerator]
- "ad_orchestrator_adassessmentrunner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L42 | neighbors=[ADAssessmentRunner]
- "agent_agent_agentdeps": "AgentDeps" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L39 | neighbors=[agent.py]
- "agent_agent_agentopts": "AgentOpts" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L26 | neighbors=[agent.py]
- "agent_agent_rationale_258": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L258 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_263": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L263 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_293": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L293 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_302": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L302 | neighbors=[_run_polled_job_with_heartbeats()]
- "agent_agent_rationale_327": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L327 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_336": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L336 | neighbors=[_run_ws_push_loop()]
- "agent_agent_rationale_382": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L382 | neighbors=[_ws_run_job()]
- "agent_agent_rationale_387": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L387 | neighbors=[_ws_run_job()]
- "agent_agent_rationale_43": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L43 | neighbors=[_load_env()]
- "agent_agent_rationale_437": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L437 | neighbors=[_ws_http_poll_fallback()]
- "agent_agent_rationale_442": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L442 | neighbors=[_ws_http_poll_fallback()]
- "agent_agent_rationale_45": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L45 | neighbors=[_bounded_env_int()]
- "agent_agent_rationale_46": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L46 | neighbors=[_bounded_env_int()]
- "agent_agent_rationale_463": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L463 | neighbors=[_ws_stage_job_offer()]

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
