# Node Description Batch 39 of 134

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

- "vuln_nuclei_nucleiscanner_template_selector": ".template_selector()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L444 | neighbors=[NucleiScanner, Given a list of service names on an ass…, Given a list of service names on an ass…, Given a list of service names on an ass…]
- "vuln_nuclei_rationale_1": "NucleiScanner — async subprocess wrapper around the Nuclei CLI.  Nuclei outputs" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[nuclei.py, FindingSeverity, FindingStatus, ServiceFingerprint]
- "vuln_nuclei_rationale_110": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L110 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_127": "Run Nuclei and stream JSONL findings from stdout.          ``request_timeout_sec" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L127 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_132": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L132 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_195": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L195 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_383": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L383 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_446": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L446 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_80": "Machine-readable state for the most recent scanner invocation." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L80 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiRunReport]
- "vuln_nuclei_rationale_81": "Runs nuclei as an async subprocess.         Returns a list of parsed finding dic" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L81 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_91": "Fatal Nuclei failure, optionally carrying findings emitted before failure." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L91 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanError]
- "vuln_tasks_run_post_scan_enrichment": "run_post_scan_enrichment()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L34 | neighbors=[tasks.py, Triggered by the vuln scan API after a …, _fire_critical_webhook(), Triggered by the vuln scan API after a …]
- "websocket_manager_agentconnectionmanager_agent_stale_after": ".agent_stale_after()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L275 | neighbors=[AgentConnectionManager, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…]
- "websocket_manager_agentconnectionmanager_connected_agents": ".connected_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L239 | neighbors=[AgentConnectionManager, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…]
- "websocket_manager_agentconnectionmanager_get_agent_status": ".get_agent_status()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L271 | neighbors=[AgentConnectionManager, Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Push a job to the first online agent in…]
- "websocket_manager_agentconnectionmanager_is_connected": ".is_connected()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L230 | neighbors=[AgentConnectionManager, Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.]
- "websocket_manager_agentconnectionmanager_is_online": ".is_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L234 | neighbors=[AgentConnectionManager, Check if a specific agent is online (co…, Check if a specific agent is online (co…, Check if a specific agent is online (co…]
- "websocket_manager_agentconnectionmanager_online_agents": ".online_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L244 | neighbors=[AgentConnectionManager, Return agent IDs whose status is 'onlin…, Return agent IDs whose status is 'onlin…, Return agent IDs whose status is 'onlin…]
- "websocket_manager_agentconnectionmanager_online_agents_for_tenant": ".online_agents_for_tenant()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L248 | neighbors=[AgentConnectionManager, .push_job_to_first_online(), Return idle connected agents belonging …, Return idle connected agents belonging …]
- "workers_outbox_enqueue": "enqueue()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L86 | neighbors=[outbox.py, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…, Add an outbox event to the caller's ses…]
- "workers_outbox_handle_facts_ready": "_handle_facts_ready()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L103 | neighbors=[outbox.py, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…, Run the deterministic detection pipelin…]
- "workers_outbox_process": "_process()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L254 | neighbors=[outbox.py, _mark_done(), _mark_retry_or_dead(), run_worker()]
- "workers_outbox_rationale_186": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L186 | neighbors=[_requeue_stale_stmt(), OutboxEvent, ScanResult, run_worker()]
- "workers_outbox_register": "register()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L76 | neighbors=[outbox.py, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…, Decorator: bind an async handler to a t…]
- "workers_reaper_run_reaper": "run_reaper()" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L87 | neighbors=[reaper.py, Poll loop: requeue expired jobs every r…, reap_once(), Poll loop: requeue expired jobs every r…]
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=probe/workflow/asset.py:L70 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…]
- "workflow_asset_parse_ts": "_parse_ts()" | kind=code-symbol | source=probe/workflow/asset.py:L31 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_asset_portfact": "PortFact" | kind=code-symbol | source=probe/workflow/asset.py:L36 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_cache_cacheentry": "CacheEntry" | kind=code-symbol | source=probe/workflow/cache.py:L55 | neighbors=[cache.py, .from_jsonl_dict(), .to_jsonl_dict(), .put()]
- "workflow_cli_main": "_main()" | kind=code-symbol | source=probe/workflow/cli.py:L95 | neighbors=[cli.py, _build_creds(), _build_mode(), build_parser()]
- "workflow_execution_classify_scanner_error": "classify_scanner_error()" | kind=code-symbol | source=probe/workflow/execution.py:L153 | neighbors=[execution.py, ErrorDetail, Map low-level failures into stable, ope…, scanner_failure_result()]
- "workflow_execution_executiontrace_ensure": "._ensure()" | kind=code-symbol | source=probe/workflow/execution.py:L239 | neighbors=[ExecutionTrace, .__init__(), .record(), .skip()]
- "workflow_modes_assessment": "assessment()" | kind=code-symbol | source=probe/workflow/modes.py:L111 | neighbors=[modes.py, EngagementMode, Full funnel, every branch the profile a…, Full funnel, every branch the profile a…]
- "workflow_modes_re_scan": "re_scan()" | kind=code-symbol | source=probe/workflow/modes.py:L126 | neighbors=[modes.py, Loads a prior engagement's cache; only …, EngagementMode, Loads a prior engagement's cache; only …]
- "workflow_modes_triage": "triage()" | kind=code-symbol | source=probe/workflow/modes.py:L104 | neighbors=[modes.py, Discovery + ports + banner only — no de…, EngagementMode, Discovery + ports + banner only — no de…]
- "workflow_router_looks_like_db": "looks_like_db()" | kind=code-symbol | source=probe/workflow/router.py:L62 | neighbors=[router.py, looks_like_http(), True when a service banner carries a da…, route_branches()]
- "workflow_router_looks_like_tls": "looks_like_tls()" | kind=code-symbol | source=probe/workflow/router.py:L50 | neighbors=[router.py, True when this port's banner result is …, route_branches(), True when this port's banner result is …]
- "workflow_workflow_engine_port_candidates": "_port_candidates()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L109 | neighbors=[workflow_engine.py, Return TCP ports worth scanning for thi…, run_engagement(), Return TCP ports worth scanning for thi…]
- "workflow_workflow_engine_scan_one": "_scan_one()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L58 | neighbors=[workflow_engine.py, _gather_per_host(), Run one component without allowing a ta…, run_engagement()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
