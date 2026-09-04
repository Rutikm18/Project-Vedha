# Node Description Batch 170 of 332

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

- "websocket_manager_rationale_209": "Push a job to the first online agent in the requested tenant.          Returns t" | kind=entity | source=manager/backend/app/websocket/manager.py:L209 | neighbors=[.push_job_to_first_online(), .get_agent_status()]
- "websocket_manager_rationale_213": "Push a job to the first online agent in the requested tenant.          Returns t" | kind=entity | source=manager/backend/app/websocket/manager.py:L213 | neighbors=[.push_job_to_first_online(), .agent_stale_after()]
- "websocket_manager_rationale_243": "Deliver a job-push to an agent wherever its socket is connected.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L243 | neighbors=[.deliver_job(), .online_agents()]
- "websocket_manager_rationale_245": "Deliver a job-push to an agent wherever its socket is connected.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L245 | neighbors=[.deliver_job(), .online_agents()]
- "websocket_manager_rationale_298": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L298 | neighbors=[.is_online(), .handle_client()]
- "workers_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/workers/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "workers_outbox_main": "main()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L446 | neighbors=[outbox.py, Event]
- "workers_outbox_mark_done": "_mark_done()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L358 | neighbors=[outbox.py, _process()]
- "workers_outbox_rationale_130": "Fan a notification out to the tenant's enabled email/Slack/Jira integrations." | kind=entity | source=manager/backend/app/workers/outbox.py:L130 | neighbors=[_handle_notify(), _claim_batch()]
- "workers_outbox_rationale_204": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L204 | neighbors=[_requeue_stale_stmt(), _reclaim_stale()]
- "workflow_asset_utcnow": "_utcnow()" | kind=code-symbol | source=probe/workflow/asset.py:L27 | neighbors=[asset.py, .needs_recheck_live()]
- "workflow_branches_branchspec_host_level": ".host_level()" | kind=code-symbol | source=probe/workflow/branches.py:L101 | neighbors=[BranchSpec, True when the fact describes the host r…]
- "workflow_branches_db_kwargs": "_db_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L68 | neighbors=[branches.py, Ports with a known database engine get …]
- "workflow_branches_no_kwargs": "_no_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L54 | neighbors=[branches.py, For scanners that take no `ports` argum…]
- "workflow_branches_ports_kwargs": "_ports_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L49 | neighbors=[branches.py, The default: hand the scanner the ports…]
- "workflow_branches_web_kwargs": "_web_kwargs()" | kind=code-symbol | source=probe/workflow/branches.py:L60 | neighbors=[branches.py, Tell the web scanner which of these por…]
- "workflow_cache_cacheentry_from_jsonl_dict": ".from_jsonl_dict()" | kind=code-symbol | source=probe/workflow/cache.py:L92 | neighbors=[CacheEntry, ._load()]
- "workflow_cache_cacheentry_to_jsonl_dict": ".to_jsonl_dict()" | kind=code-symbol | source=probe/workflow/cache.py:L86 | neighbors=[CacheEntry, .save()]
- "workflow_cache_workflowcache_init": ".__init__()" | kind=code-symbol | source=probe/workflow/cache.py:L104 | neighbors=[WorkflowCache, ._load()]
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
