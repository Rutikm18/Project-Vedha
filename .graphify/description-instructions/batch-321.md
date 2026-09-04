# Node Description Batch 322 of 330

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

- "versions_0037_scan_job_cancelled_status_rationale_1": "scan jobs gain a terminal `cancelled` status  An operator could start work but n" | kind=entity | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L1 | neighbors=[0037_scan_job_cancelled_status.py]
- "versions_0037_scan_job_cancelled_status_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L34 | neighbors=[0037_scan_job_cancelled_status.py]
- "vuln_enrichment_ttlcache_contains": ".__contains__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L36 | neighbors=[TTLCache]
- "vuln_enrichment_ttlcache_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L43 | neighbors=[TTLCache]
- "vuln_enrichment_ttlcache_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L31 | neighbors=[TTLCache]
- "vuln_enrichment_ttlcache_setitem": ".__setitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L51 | neighbors=[TTLCache]
- "vuln_nessus_nessusscanner_close": ".close()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L66 | neighbors=[NessusScanner]
- "vuln_nessus_nessusscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L40 | neighbors=[NessusScanner]
- "vuln_nuclei_nucleiscanerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L92 | neighbors=[NucleiScanError]
- "vuln_nuclei_nucleiscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L113 | neighbors=[NucleiScanner]
- "vuln_prioritizer_route_demo_assets": "DEMO_ASSETS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L16 | neighbors=[route.ts]
- "vuln_prioritizer_route_demo_findings": "DEMO_FINDINGS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L5 | neighbors=[route.ts]
- "vuln_prioritizer_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L27 | neighbors=[route.ts]
- "websocket_manager_agentconnectionmanager_connected_count": ".connected_count()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L331 | neighbors=[AgentConnectionManager]
- "websocket_manager_agentconnectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L88 | neighbors=[AgentConnectionManager]
- "websocket_manager_connectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L30 | neighbors=[ConnectionManager]
- "websocket_manager_rationale_1": "WebSocket manager for real-time graph updates, agent push, and live collaboratio" | kind=entity | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[manager.py]
- "websocket_manager_rationale_101": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L101 | neighbors=[.register()]
- "websocket_manager_rationale_123": "Remove an agent's WebSocket registration." | kind=entity | source=manager/backend/app/websocket/manager.py:L123 | neighbors=[.unregister()]
- "websocket_manager_rationale_129": "Remove the current registration, optionally only for one socket.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L129 | neighbors=[.unregister()]
- "websocket_manager_rationale_131": "Remove the current registration, optionally only for one socket.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L131 | neighbors=[.unregister()]
- "websocket_manager_rationale_136": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L136 | neighbors=[.record_heartbeat()]
- "websocket_manager_rationale_147": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L147 | neighbors=[.push_job()]
- "websocket_manager_rationale_153": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L153 | neighbors=[.record_heartbeat()]
- "websocket_manager_rationale_155": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L155 | neighbors=[.record_heartbeat()]
- "websocket_manager_rationale_165": "Push a job to the first online connected agent.          Returns the agent_id th" | kind=entity | source=manager/backend/app/websocket/manager.py:L165 | neighbors=[.push_job_to_first_online()]
- "websocket_manager_rationale_166": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L166 | neighbors=[.record_features()]
- "websocket_manager_rationale_168": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L168 | neighbors=[.record_features()]
- "websocket_manager_rationale_170": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L170 | neighbors=[.record_features()]
- "websocket_manager_rationale_181": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L181 | neighbors=[.push_job()]
- "websocket_manager_rationale_183": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L183 | neighbors=[.push_job()]
- "websocket_manager_rationale_185": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L185 | neighbors=[.push_job()]
- "websocket_manager_rationale_187": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L187 | neighbors=[.is_connected()]
- "websocket_manager_rationale_191": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L191 | neighbors=[.is_online()]
- "websocket_manager_rationale_196": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L196 | neighbors=[.connected_agents()]
- "websocket_manager_rationale_201": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L201 | neighbors=[.online_agents()]
- "websocket_manager_rationale_211": "Push a job to the first online agent in the requested tenant.          Returns t" | kind=entity | source=manager/backend/app/websocket/manager.py:L211 | neighbors=[.push_job_to_first_online()]
- "websocket_manager_rationale_229": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L229 | neighbors=[.is_connected()]
- "websocket_manager_rationale_230": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L230 | neighbors=[GraphWebSocketManager]
- "websocket_manager_rationale_231": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L231 | neighbors=[.is_connected()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-321.json

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
