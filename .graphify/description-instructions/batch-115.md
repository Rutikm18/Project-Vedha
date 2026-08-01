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

- "vuln_enrichment_ttlcache_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L43 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L31 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_setitem": ".__setitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L51 | neighbors=[TTLCache] | lang=en
- "vuln_nessus_nessusscanner_close": ".close()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L67 | neighbors=[NessusScanner] | lang=en
- "vuln_nessus_nessusscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L41 | neighbors=[NessusScanner] | lang=en
- "vuln_nuclei_nucleiscanerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L93 | neighbors=[NucleiScanError] | lang=en
- "vuln_nuclei_nucleiscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L114 | neighbors=[NucleiScanner] | lang=en
- "vuln_prioritizer_route_demo_assets": "DEMO_ASSETS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L16 | neighbors=[route.ts] | lang=en
- "vuln_prioritizer_route_demo_findings": "DEMO_FINDINGS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L5 | neighbors=[route.ts] | lang=en
- "vuln_prioritizer_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L27 | neighbors=[route.ts] | lang=en
- "websocket_manager_agentconnectionmanager_connected_count": ".connected_count()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L266 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_agentconnectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L86 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_connectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L28 | neighbors=[ConnectionManager] | lang=en
- "websocket_manager_rationale_1": "WebSocket manager for real-time graph updates, agent push, and live collaboratio" | kind=entity | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[manager.py] | lang=en
- "websocket_manager_rationale_123": "Remove an agent's WebSocket registration." | kind=entity | source=manager/backend/app/websocket/manager.py:L123 | neighbors=[.unregister()] | lang=en
- "websocket_manager_rationale_129": "Remove the current registration, optionally only for one socket.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L129 | neighbors=[.unregister()] | lang=en
- "websocket_manager_rationale_136": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L136 | neighbors=[.record_heartbeat()] | lang=en
- "websocket_manager_rationale_147": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L147 | neighbors=[.push_job()] | lang=en
- "websocket_manager_rationale_153": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L153 | neighbors=[.record_heartbeat()] | lang=en
- "websocket_manager_rationale_165": "Push a job to the first online connected agent.          Returns the agent_id th" | kind=entity | source=manager/backend/app/websocket/manager.py:L165 | neighbors=[.push_job_to_first_online()] | lang=en
- "websocket_manager_rationale_166": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L166 | neighbors=[.record_features()] | lang=en
- "websocket_manager_rationale_181": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L181 | neighbors=[.push_job()] | lang=en
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
