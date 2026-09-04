# Node Description Batch 325 of 332

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "websocket_manager_rationale_28": "Manages WebSocket connections with room-based broadcasting." | kind=entity | source=manager/backend/app/websocket/manager.py:L28 | neighbors=[ConnectionManager] | lang=en
- "websocket_manager_rationale_280": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L280 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_289": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L289 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_291": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L291 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_292": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L292 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_293": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L293 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_294": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L294 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_296": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L296 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_299": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L299 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_300": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L300 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_301": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L301 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_303": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L303 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_306": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L306 | neighbors=[.online_agents()] | lang=en
- "websocket_manager_rationale_308": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L308 | neighbors=[.online_agents()] | lang=en
- "websocket_manager_rationale_314": "Return idle connected agents belonging to exactly one tenant." | kind=entity | source=manager/backend/app/websocket/manager.py:L314 | neighbors=[.online_agents_for_tenant()] | lang=en
- "websocket_manager_rationale_316": "Return idle connected agents belonging to exactly one tenant." | kind=entity | source=manager/backend/app/websocket/manager.py:L316 | neighbors=[.online_agents_for_tenant()] | lang=en
- "websocket_manager_rationale_318": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L318 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_320": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L320 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_333": "Return 'online', 'busy', or 'offline'." | kind=entity | source=manager/backend/app/websocket/manager.py:L333 | neighbors=[.get_agent_status()] | lang=en
- "websocket_manager_rationale_335": "Return 'online', 'busy', or 'offline'." | kind=entity | source=manager/backend/app/websocket/manager.py:L335 | neighbors=[.get_agent_status()] | lang=en
- "websocket_manager_rationale_337": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L337 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_339": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L339 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_34": "Accept connection and add to room." | kind=entity | source=manager/backend/app/websocket/manager.py:L34 | neighbors=[.connect()] | lang=en
- "websocket_manager_rationale_341": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L341 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_343": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L343 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_350": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L350 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_352": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L352 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_354": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L354 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_356": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L356 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_36": "Accept connection and add to room." | kind=entity | source=manager/backend/app/websocket/manager.py:L36 | neighbors=[.connect()] | lang=en
- "websocket_manager_rationale_360": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L360 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_361": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L361 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_362": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L362 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_363": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L363 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_381": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L381 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_383": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L383 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_404": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L404 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_406": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L406 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_413": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L413 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_415": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L415 | neighbors=[.broadcast_node_update()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-324.json

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
