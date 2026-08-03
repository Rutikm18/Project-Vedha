# Node Description Batch 127 of 131

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

- "versions_0018_probe_enrollment_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L18 | neighbors=[0018_probe_enrollment.py] | lang=en
- "vuln_enrichment_ttlcache_contains": ".__contains__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L36 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L43 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L31 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_setitem": ".__setitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L51 | neighbors=[TTLCache] | lang=en
- "vuln_nessus_nessusscanner_close": ".close()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L66 | neighbors=[NessusScanner] | lang=en
- "vuln_nessus_nessusscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L40 | neighbors=[NessusScanner] | lang=en
- "vuln_nuclei_nucleiscanerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L92 | neighbors=[NucleiScanError] | lang=en
- "vuln_nuclei_nucleiscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L113 | neighbors=[NucleiScanner] | lang=en
- "vuln_prioritizer_route_demo_assets": "DEMO_ASSETS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L16 | neighbors=[route.ts] | lang=en
- "vuln_prioritizer_route_demo_findings": "DEMO_FINDINGS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L5 | neighbors=[route.ts] | lang=en
- "vuln_prioritizer_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L27 | neighbors=[route.ts] | lang=en
- "websocket_manager_agentconnectionmanager_connected_count": ".connected_count()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L268 | neighbors=[AgentConnectionManager] | lang=en
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
- "websocket_manager_rationale_168": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L168 | neighbors=[.record_features()] | lang=en
- "websocket_manager_rationale_181": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L181 | neighbors=[.push_job()] | lang=en
- "websocket_manager_rationale_183": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L183 | neighbors=[.push_job()] | lang=en
- "websocket_manager_rationale_187": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L187 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_191": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L191 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_196": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L196 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_201": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L201 | neighbors=[.online_agents()] | lang=en
- "websocket_manager_rationale_211": "Push a job to the first online agent in the requested tenant.          Returns t" | kind=entity | source=manager/backend/app/websocket/manager.py:L211 | neighbors=[.push_job_to_first_online()] | lang=en
- "websocket_manager_rationale_213": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L213 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_229": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L229 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_230": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L230 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_231": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L231 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_233": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L233 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_235": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L235 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_237": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L237 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_238": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L238 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_240": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L240 | neighbors=[.connected_agents()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-126.json

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
