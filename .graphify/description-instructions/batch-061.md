# Node Description Batch 62 of 104

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "vuln_nuclei_nucleiscanner_map_finding": "._map_finding()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L145 | neighbors=[NucleiScanner, .parse_output()]
- "vuln_nuclei_nucleiscanner_template_selector": ".template_selector()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L194 | neighbors=[NucleiScanner, Given a list of service names on an ass…]
- "vuln_tasks_dedup_hash": "_dedup_hash()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L170 | neighbors=[tasks.py, Deprecated — use app.utils.hash.dedup_h…]
- "vuln_tasks_fire_critical_webhook": "_fire_critical_webhook()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L138 | neighbors=[tasks.py, run_post_scan_enrichment()]
- "websocket_manager_agentconnectionmanager_agent_stale_after": ".agent_stale_after()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L212 | neighbors=[AgentConnectionManager, Return agent_ids whose last heartbeat i…]
- "websocket_manager_agentconnectionmanager_connected_agents": ".connected_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L195 | neighbors=[AgentConnectionManager, Return a snapshot of all connected agen…]
- "websocket_manager_agentconnectionmanager_get_agent_status": ".get_agent_status()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L208 | neighbors=[AgentConnectionManager, Return 'online', 'busy', or 'offline'.]
- "websocket_manager_agentconnectionmanager_is_connected": ".is_connected()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L186 | neighbors=[AgentConnectionManager, Check if a specific agent is connected.]
- "websocket_manager_agentconnectionmanager_is_online": ".is_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L190 | neighbors=[AgentConnectionManager, Check if a specific agent is online (co…]
- "websocket_manager_agentconnectionmanager_online_agents": ".online_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L200 | neighbors=[AgentConnectionManager, Return agent IDs whose status is 'onlin…]
- "websocket_manager_agentconnectionmanager_record_heartbeat": ".record_heartbeat()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L134 | neighbors=[AgentConnectionManager, Record a heartbeat from an agent.]
- "websocket_manager_agentconnectionmanager_register": ".register()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L96 | neighbors=[AgentConnectionManager, Register an agent's WebSocket connectio…]
- "websocket_manager_connectionmanager_get_room_clients": ".get_room_clients()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L73 | neighbors=[ConnectionManager, Get number of connected clients in a ro…]
- "websocket_manager_graphwebsocketmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L232 | neighbors=[GraphWebSocketManager, ConnectionManager]
- "workers_outbox_enqueue": "enqueue()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L65 | neighbors=[outbox.py, Add an outbox event to the caller's ses…]
- "workers_outbox_handle_facts_ready": "_handle_facts_ready()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L82 | neighbors=[outbox.py, Run the deterministic detection pipelin…]
- "workers_outbox_main": "main()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L211 | neighbors=[outbox.py, Event]
- "workers_outbox_mark_done": "_mark_done()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L142 | neighbors=[outbox.py, _process()]
- "workers_outbox_register": "register()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L55 | neighbors=[outbox.py, Decorator: bind an async handler to a t…]
- "workflow_asset_asset_merge_result": ".merge_result()" | kind=code-symbol | source=probe/workflow/asset.py:L84 | neighbors=[Asset, Dispatch a real ScanResult into the rig…]
- "workflow_asset_utcnow": "_utcnow()" | kind=code-symbol | source=probe/workflow/asset.py:L28 | neighbors=[asset.py, .needs_recheck_live()]
- "workflow_cache_cacheentry_from_jsonl_dict": ".from_jsonl_dict()" | kind=code-symbol | source=probe/workflow/cache.py:L71 | neighbors=[CacheEntry, ._load()]
- "workflow_cache_cacheentry_to_jsonl_dict": ".to_jsonl_dict()" | kind=code-symbol | source=probe/workflow/cache.py:L65 | neighbors=[CacheEntry, .save()]
- "workflow_cache_workflowcache_init": ".__init__()" | kind=code-symbol | source=probe/workflow/cache.py:L83 | neighbors=[WorkflowCache, ._load()]
- "workflow_cache_workflowcache_save": ".save()" | kind=code-symbol | source=probe/workflow/cache.py:L101 | neighbors=[WorkflowCache, .to_jsonl_dict()]
- "workflow_cli_build_creds": "_build_creds()" | kind=code-symbol | source=probe/workflow/cli.py:L84 | neighbors=[cli.py, _main()]
- "workflow_cli_build_mode": "_build_mode()" | kind=code-symbol | source=probe/workflow/cli.py:L72 | neighbors=[cli.py, _main()]
- "workflow_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/workflow/cli.py:L44 | neighbors=[cli.py, _main()]
- "workflow_cli_parse_duration": "_parse_duration()" | kind=code-symbol | source=probe/workflow/cli.py:L29 | neighbors=[cli.py, 7d' / '12h' / '30m' -> timedelta. Simpl…]
- "workflow_gates_gate_2_host_discovery": "gate_2_host_discovery()" | kind=code-symbol | source=probe/workflow/gates.py:L52 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_gates_gate_3_port_scan": "gate_3_port_scan()" | kind=code-symbol | source=probe/workflow/gates.py:L59 | neighbors=[gates.py, gate_0_is_passive_profile()]
- "workflow_gates_gate_5_branch_eligible": "gate_5_branch_eligible()" | kind=code-symbol | source=probe/workflow/gates.py:L69 | neighbors=[gates.py, Does `branch` apply to this host?      …]
- "workflow_init": "__init__.py" | kind=code-symbol | source=probe/workflow/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, workflow — conditional, caching, depend…]
- "workflow_modes_service_specific": "service_specific()" | kind=code-symbol | source=probe/workflow/modes.py:L36 | neighbors=[modes.py, EngagementMode]
- "workflow_report_diff_assets": "diff_assets()" | kind=code-symbol | source=probe/workflow/report.py:L42 | neighbors=[report.py, re-scan mode's delta report: what chang…]
- "workflow_router_looks_like_http": "looks_like_http()" | kind=code-symbol | source=probe/workflow/router.py:L37 | neighbors=[router.py, route_branches()]
- "activity_route_apiactivity": "ApiActivity" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L9 | neighbors=[route.ts]
- "activity_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L14 | neighbors=[route.ts]
- "ad_asreproast_asreproastchecker_generate_finding": ".generate_finding()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L106 | neighbors=[ASREPRoastChecker]
- "ad_bloodhound_bloodhoundcollector_close": ".close()" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L267 | neighbors=[BloodHoundCollector]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-061.json

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
