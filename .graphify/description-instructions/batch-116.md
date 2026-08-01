# Node Description Batch 117 of 119

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

- "websocket_manager_rationale_291": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L291 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_298": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L298 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_299": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L299 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_318": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L318 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_34": "Accept connection and add to room." | kind=entity | source=manager/backend/app/websocket/manager.py:L34 | neighbors=[.connect()] | lang=en
- "websocket_manager_rationale_341": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L341 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_350": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L350 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_360": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L360 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_42": "Remove connection from room." | kind=entity | source=manager/backend/app/websocket/manager.py:L42 | neighbors=[.disconnect()] | lang=en
- "websocket_manager_rationale_50": "Broadcast message to all connections in a room." | kind=entity | source=manager/backend/app/websocket/manager.py:L50 | neighbors=[.broadcast()] | lang=en
- "websocket_manager_rationale_67": "Send message to a specific connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L67 | neighbors=[.send_personal()] | lang=en
- "websocket_manager_rationale_74": "Get number of connected clients in a room." | kind=entity | source=manager/backend/app/websocket/manager.py:L74 | neighbors=[.get_room_clients()] | lang=en
- "websocket_manager_rationale_79": "Tracks WebSocket connections from probes/agents for direct job push.      Each c" | kind=entity | source=manager/backend/app/websocket/manager.py:L79 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_rationale_98": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L98 | neighbors=[.register()] | lang=en
- "websocket_manager_rationale_99": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L99 | neighbors=[.register()] | lang=en
- "workflow_asset_asset_merge_db_scan": "._merge_db_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L140 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_mcp_ai_scan": "._merge_mcp_ai_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L144 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_passive_collect": "._merge_passive_collect()" | kind=code-symbol | source=probe/workflow/asset.py:L156 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_service_banner": "._merge_service_banner()" | kind=code-symbol | source=probe/workflow/asset.py:L118 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_smb_scan": "._merge_smb_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L130 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_snmp_scan": "._merge_snmp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L136 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_ssh_inventory": "._merge_ssh_inventory()" | kind=code-symbol | source=probe/workflow/asset.py:L162 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_tls_scan": "._merge_tls_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L122 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_web_scan": "._merge_web_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L126 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_windows_inventory": "._merge_windows_inventory()" | kind=code-symbol | source=probe/workflow/asset.py:L166 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_open_ports_for_deep_scan": ".open_ports_for_deep_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L81 | neighbors=[Asset] | lang=en
- "workflow_asset_rationale_1": "asset.py — per-host fact model the workflow engine reasons about.  This is an OR" | kind=entity | source=probe/workflow/asset.py:L1 | neighbors=[asset.py] | lang=en
- "workflow_asset_rationale_72": "Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep" | kind=entity | source=probe/workflow/asset.py:L72 | neighbors=[.needs_recheck_live()] | lang=en
- "workflow_asset_rationale_85": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L85 | neighbors=[.merge_result()] | lang=en
- "workflow_cache_rationale_1": "cache.py — (host, port, scanner) -> CacheEntry, so deterministic facts are colle" | kind=entity | source=probe/workflow/cache.py:L1 | neighbors=[cache.py] | lang=en
- "workflow_cache_rationale_122": "True if there's no cached entry, OR the entry is uncertain         (always worth" | kind=entity | source=probe/workflow/cache.py:L122 | neighbors=[.should_recheck()] | lang=en
- "workflow_cache_rationale_79": "In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c" | kind=entity | source=probe/workflow/cache.py:L79 | neighbors=[WorkflowCache] | lang=en
- "workflow_cache_workflowcache_all_entries_for_host": ".all_entries_for_host()" | kind=code-symbol | source=probe/workflow/cache.py:L139 | neighbors=[WorkflowCache] | lang=en
- "workflow_cli_rationale_1": "cli.py — entrypoint for the conditional workflow engine. Flag conventions follow" | kind=entity | source=probe/workflow/cli.py:L1 | neighbors=[cli.py] | lang=en
- "workflow_cli_rationale_30": "7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar" | kind=entity | source=probe/workflow/cli.py:L30 | neighbors=[_parse_duration()] | lang=en
- "workflow_execution_executiontrace_degraded": ".degraded()" | kind=code-symbol | source=probe/workflow/execution.py:L346 | neighbors=[ExecutionTrace] | lang=en
- "workflow_execution_executiontrace_issues": ".issues()" | kind=code-symbol | source=probe/workflow/execution.py:L338 | neighbors=[ExecutionTrace] | lang=en
- "workflow_execution_rationale_1": "Execution telemetry and failure normalization for the probe workflow." | kind=entity | source=probe/workflow/execution.py:L1 | neighbors=[execution.py] | lang=en
- "workflow_execution_rationale_105": "Resolve the exact collector plan for one workflow invocation." | kind=entity | source=probe/workflow/execution.py:L105 | neighbors=[planned_components()] | lang=en
- "workflow_execution_rationale_154": "Map low-level failures into stable, operator-actionable categories." | kind=entity | source=probe/workflow/execution.py:L154 | neighbors=[classify_scanner_error()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-116.json

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
