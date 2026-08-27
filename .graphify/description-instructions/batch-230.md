# Node Description Batch 231 of 236

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

- "websocket_manager_rationale_318": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L318 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_320": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L320 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_333": "Return 'online', 'busy', or 'offline'." | kind=entity | source=manager/backend/app/websocket/manager.py:L333 | neighbors=[.get_agent_status()] | lang=en
- "websocket_manager_rationale_337": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L337 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_34": "Accept connection and add to room." | kind=entity | source=manager/backend/app/websocket/manager.py:L34 | neighbors=[.connect()] | lang=en
- "websocket_manager_rationale_341": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L341 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_343": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L343 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_350": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L350 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_352": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L352 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_354": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L354 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_360": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L360 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_361": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L361 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_362": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L362 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_381": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L381 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_404": "Broadcast graph data update to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L404 | neighbors=[.broadcast_graph_update()] | lang=en
- "websocket_manager_rationale_413": "Broadcast a single node update." | kind=entity | source=manager/backend/app/websocket/manager.py:L413 | neighbors=[.broadcast_node_update()] | lang=pt
- "websocket_manager_rationale_42": "Remove connection from room." | kind=entity | source=manager/backend/app/websocket/manager.py:L42 | neighbors=[.disconnect()] | lang=en
- "websocket_manager_rationale_423": "Broadcast layout change to all subscribers." | kind=entity | source=manager/backend/app/websocket/manager.py:L423 | neighbors=[.broadcast_layout_update()] | lang=en
- "websocket_manager_rationale_50": "Broadcast message to all connections in a room." | kind=entity | source=manager/backend/app/websocket/manager.py:L50 | neighbors=[.broadcast()] | lang=en
- "websocket_manager_rationale_67": "Send message to a specific connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L67 | neighbors=[.send_personal()] | lang=en
- "websocket_manager_rationale_74": "Get number of connected clients in a room." | kind=entity | source=manager/backend/app/websocket/manager.py:L74 | neighbors=[.get_room_clients()] | lang=en
- "websocket_manager_rationale_79": "Tracks WebSocket connections from probes/agents for direct job push.      Each c" | kind=entity | source=manager/backend/app/websocket/manager.py:L79 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_rationale_98": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L98 | neighbors=[.register()] | lang=en
- "websocket_manager_rationale_99": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L99 | neighbors=[.register()] | lang=en
- "workers_outbox_rationale_103": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L103 | neighbors=[_handle_facts_ready()] | lang=en
- "workers_outbox_rationale_104": "Run the deterministic detection pipeline on a submitted facts payload.     Re-re" | kind=entity | source=manager/backend/app/workers/outbox.py:L104 | neighbors=[_handle_facts_ready()] | lang=en
- "workers_outbox_rationale_131": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L131 | neighbors=[_claim_batch()] | lang=en
- "workers_outbox_rationale_139": "Fan a notification out to the tenant's enabled email/Slack/Jira integrations." | kind=entity | source=manager/backend/app/workers/outbox.py:L139 | neighbors=[_handle_notify()] | lang=en
- "workers_outbox_rationale_149": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L149 | neighbors=[_claim_batch()] | lang=en
- "workers_outbox_rationale_158": "Atomically claim up to `batch_size` due events. FOR UPDATE SKIP LOCKED     means" | kind=entity | source=manager/backend/app/workers/outbox.py:L158 | neighbors=[_claim_batch()] | lang=en
- "workers_outbox_rationale_163": "Requeue events a dead worker left in PROCESSING past the lease.      `attempts`" | kind=entity | source=manager/backend/app/workers/outbox.py:L163 | neighbors=[_reclaim_stale()] | lang=en
- "workers_outbox_rationale_164": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L164 | neighbors=[_stale_cutoff()] | lang=en
- "workers_outbox_rationale_169": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L169 | neighbors=[_dead_letter_stale_stmt()] | lang=en
- "workers_outbox_rationale_182": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L182 | neighbors=[_stale_cutoff()] | lang=en
- "workers_outbox_rationale_187": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L187 | neighbors=[_dead_letter_stale_stmt()] | lang=en
- "workers_outbox_rationale_191": "The `locked_at` boundary before which a PROCESSING row is considered dead." | kind=entity | source=manager/backend/app/workers/outbox.py:L191 | neighbors=[_stale_cutoff()] | lang=en
- "workers_outbox_rationale_196": "Stranded events that already exhausted their retry budget → dead-letter.     Bou" | kind=entity | source=manager/backend/app/workers/outbox.py:L196 | neighbors=[_dead_letter_stale_stmt()] | lang=en
- "workers_outbox_rationale_213": "Stranded events with retry budget left → make due now so a live worker     re-cl" | kind=entity | source=manager/backend/app/workers/outbox.py:L213 | neighbors=[_requeue_stale_stmt()] | lang=en
- "workers_outbox_rationale_216": "Reschedule with exponential backoff, or dead-letter once attempts are     exhaus" | kind=entity | source=manager/backend/app/workers/outbox.py:L216 | neighbors=[_mark_retry_or_dead()] | lang=en
- "workers_outbox_rationale_222": "Requeue events a dead worker left in PROCESSING past the lease.      `_claim_bat" | kind=entity | source=manager/backend/app/workers/outbox.py:L222 | neighbors=[_reclaim_stale()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-230.json

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
