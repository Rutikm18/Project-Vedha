# Node Description Batch 170 of 330

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

- "workflow_cache_workflowcache_save": ".save()" | kind=code-symbol | source=probe/workflow/cache.py:L122 | neighbors=[WorkflowCache, .to_jsonl_dict()]
- "workflow_cli_build_creds": "_build_creds()" | kind=code-symbol | source=probe/workflow/cli.py:L83 | neighbors=[cli.py, _main()]
- "workflow_cli_build_mode": "_build_mode()" | kind=code-symbol | source=probe/workflow/cli.py:L71 | neighbors=[cli.py, _main()]
- "workflow_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/workflow/cli.py:L43 | neighbors=[cli.py, _main()]
- "workflow_execution_errordetail": "ErrorDetail" | kind=code-symbol | source=probe/workflow/execution.py:L159 | neighbors=[execution.py, classify_scanner_error()]
- "workflow_execution_executiontrace_as_list": ".as_list()" | kind=code-symbol | source=probe/workflow/execution.py:L394 | neighbors=[ExecutionTrace, ._has_active_coverage()]
- "workflow_execution_executiontrace_finalize": ".finalize()" | kind=code-symbol | source=probe/workflow/execution.py:L363 | neighbors=[ExecutionTrace, .skip()]
- "workflow_execution_executiontrace_init": ".__init__()" | kind=code-symbol | source=probe/workflow/execution.py:L246 | neighbors=[ExecutionTrace, ._ensure()]
- "workflow_execution_executiontrace_reused": ".reused()" | kind=code-symbol | source=probe/workflow/execution.py:L349 | neighbors=[ExecutionTrace, .record()]
- "workflow_gates_gate_2_host_discovery": "gate_2_host_discovery()" | kind=code-symbol | source=probe/workflow/gates.py:L105 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_gates_gate_3_port_scan": "gate_3_port_scan()" | kind=code-symbol | source=probe/workflow/gates.py:L112 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_host_health_hosthealthmonitor_finalize": ".finalize()" | kind=code-symbol | source=probe/workflow/host_health.py:L301 | neighbors=[HostHealthMonitor, Emit one fact per offline host, plus an…]
- "workflow_host_health_hosthealthmonitor_init": ".__init__()" | kind=code-symbol | source=probe/workflow/host_health.py:L121 | neighbors=[HostHealthMonitor, _strike_threshold()]
- "workflow_host_health_hosthealthmonitor_note_skipped": ".note_skipped()" | kind=code-symbol | source=probe/workflow/host_health.py:L189 | neighbors=[HostHealthMonitor, ._state()]
- "workflow_host_health_hoststate": "_HostState" | kind=code-symbol | source=probe/workflow/host_health.py:L101 | neighbors=[host_health.py, ._state()]
- "workflow_modes_includes_stage": "includes_stage()" | kind=code-symbol | source=probe/workflow/modes.py:L45 | neighbors=[modes.py, Return whether a bounded plan includes …]
- "workflow_modes_resolve_stage_ceiling": "resolve_stage_ceiling()" | kind=code-symbol | source=probe/workflow/modes.py:L25 | neighbors=[modes.py, Resolve the explicit ceiling while pres…]
- "workflow_modes_service_specific": "service_specific()" | kind=code-symbol | source=probe/workflow/modes.py:L118 | neighbors=[modes.py, EngagementMode]
- "workflow_report_diff_assets": "diff_assets()" | kind=code-symbol | source=probe/workflow/report.py:L42 | neighbors=[report.py, re-scan mode's delta report: what chang…]
- "workflow_router_rationale_72": "True when the port was OBSERVED speaking TLS (a completed handshake, or a     TL" | kind=entity | source=probe/workflow/router.py:L72 | neighbors=[looks_like_tls(), looks_like_ssh()]
- "workflow_workflow_engine_finalize_trace": "_finalize_trace()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L287 | neighbors=[workflow_engine.py, run_engagement()]
- "workflow_workflow_engine_rationale_112": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L112 | neighbors=[_gather_per_host(), _port_candidates()]
- "workflow_workflow_engine_rationale_80": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L80 | neighbors=[_gather_per_host(), _port_candidates()]
- "workflow_workflow_engine_rationale_94": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L94 | neighbors=[_scan_one(), _split_cached()]
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
- "agent_agent_rationale_1016": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1016 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_1020": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1020 | neighbors=[_check_anti_debug()]
- "agent_agent_rationale_1025": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1025 | neighbors=[_load_or_create_signing_identity()]
- "agent_agent_rationale_103": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L103 | neighbors=[_job_intent()]
- "agent_agent_rationale_1049": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1049 | neighbors=[_enroll_device()]
- "agent_agent_rationale_1058": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1058 | neighbors=[_enroll_device()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-169.json

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
