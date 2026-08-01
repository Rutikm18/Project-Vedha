# Node Description Batch 116 of 119

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

- "websocket_manager_rationale_187": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L187 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_191": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L191 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_196": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L196 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_201": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L201 | neighbors=[.online_agents()] | lang=en
- "websocket_manager_rationale_213": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L213 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_229": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L229 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_230": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L230 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_233": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L233 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_237": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L237 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_238": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L238 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_243": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L243 | neighbors=[.online_agents()] | lang=en
- "websocket_manager_rationale_251": "Return idle connected agents belonging to exactly one tenant." | kind=entity | source=manager/backend/app/websocket/manager.py:L251 | neighbors=[.online_agents_for_tenant()] | lang=en
- "websocket_manager_rationale_257": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L257 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_26": "Manages WebSocket connections with room-based broadcasting." | kind=entity | source=manager/backend/app/websocket/manager.py:L26 | neighbors=[ConnectionManager] | lang=en
- "websocket_manager_rationale_270": "Return 'online', 'busy', or 'offline'." | kind=entity | source=manager/backend/app/websocket/manager.py:L270 | neighbors=[.get_agent_status()] | lang=en
- "websocket_manager_rationale_274": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L274 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_280": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L280 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_289": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L289 | neighbors=[.broadcast_node_update()] | lang=pt
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
- "workflow_asset_asset_merge_db_scan": "._merge_db_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L139 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_mcp_ai_scan": "._merge_mcp_ai_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L143 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_passive_collect": "._merge_passive_collect()" | kind=code-symbol | source=probe/workflow/asset.py:L155 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_service_banner": "._merge_service_banner()" | kind=code-symbol | source=probe/workflow/asset.py:L117 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_smb_scan": "._merge_smb_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L129 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_snmp_scan": "._merge_snmp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L135 | neighbors=[Asset] | lang=en
- "workflow_asset_asset_merge_ssh_inventory": "._merge_ssh_inventory()" | kind=code-symbol | source=probe/workflow/asset.py:L161 | neighbors=[Asset] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-115.json

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
