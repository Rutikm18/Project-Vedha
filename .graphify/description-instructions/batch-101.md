# Node Description Batch 102 of 104

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

- "versions_0010_detection_runs_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L63 | neighbors=[0010_detection_runs.py] | lang=en
- "versions_0010_detection_runs_rationale_1": "Temporal detection: detection_runs table + finding provenance columns.  Records" | kind=entity | source=manager/backend/alembic/versions/0010_detection_runs.py:L1 | neighbors=[0010_detection_runs.py] | lang=en
- "versions_0010_detection_runs_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L23 | neighbors=[0010_detection_runs.py] | lang=en
- "versions_0011_job_lease_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L33 | neighbors=[0011_job_lease.py] | lang=en
- "versions_0011_job_lease_rationale_1": "Job leasing: scan_jobs.lease_expires_at for the dead-probe reaper.  A claimed (r" | kind=entity | source=manager/backend/alembic/versions/0011_job_lease.py:L1 | neighbors=[0011_job_lease.py] | lang=en
- "versions_0011_job_lease_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L21 | neighbors=[0011_job_lease.py] | lang=en
- "versions_0012_agent_recommendations_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L48 | neighbors=[0012_agent_recommendations.py] | lang=en
- "versions_0012_agent_recommendations_rationale_1": "Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto" | kind=entity | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L1 | neighbors=[0012_agent_recommendations.py] | lang=en
- "versions_0012_agent_recommendations_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L22 | neighbors=[0012_agent_recommendations.py] | lang=en
- "versions_0013_agent_public_key_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L26 | neighbors=[0013_agent_public_key.py] | lang=en
- "versions_0013_agent_public_key_rationale_1": "Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe" | kind=entity | source=manager/backend/alembic/versions/0013_agent_public_key.py:L1 | neighbors=[0013_agent_public_key.py] | lang=en
- "versions_0013_agent_public_key_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L22 | neighbors=[0013_agent_public_key.py] | lang=en
- "vuln_enrichment_ttlcache_contains": ".__contains__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L36 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_getitem": ".__getitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L43 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L31 | neighbors=[TTLCache] | lang=en
- "vuln_enrichment_ttlcache_setitem": ".__setitem__()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L51 | neighbors=[TTLCache] | lang=en
- "vuln_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/vuln/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …] | lang=en
- "vuln_nessus_nessusscanner_close": ".close()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L67 | neighbors=[NessusScanner] | lang=en
- "vuln_nessus_nessusscanner_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L41 | neighbors=[NessusScanner] | lang=en
- "vuln_prioritizer_route_demo_assets": "DEMO_ASSETS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L16 | neighbors=[route.ts] | lang=en
- "vuln_prioritizer_route_demo_findings": "DEMO_FINDINGS" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L5 | neighbors=[route.ts] | lang=en
- "vuln_prioritizer_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L27 | neighbors=[route.ts] | lang=en
- "websocket_manager_agentconnectionmanager_connected_count": ".connected_count()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L205 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_agentconnectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L86 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_connectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L28 | neighbors=[ConnectionManager] | lang=en
- "websocket_manager_rationale_1": "WebSocket manager for real-time graph updates, agent push, and live collaboratio" | kind=entity | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[manager.py] | lang=en
- "websocket_manager_rationale_123": "Remove an agent's WebSocket registration." | kind=entity | source=manager/backend/app/websocket/manager.py:L123 | neighbors=[.unregister()] | lang=en
- "websocket_manager_rationale_136": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L136 | neighbors=[.record_heartbeat()] | lang=en
- "websocket_manager_rationale_147": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L147 | neighbors=[.push_job()] | lang=en
- "websocket_manager_rationale_165": "Push a job to the first online connected agent.          Returns the agent_id th" | kind=entity | source=manager/backend/app/websocket/manager.py:L165 | neighbors=[.push_job_to_first_online()] | lang=en
- "websocket_manager_rationale_187": "Check if a specific agent is connected." | kind=entity | source=manager/backend/app/websocket/manager.py:L187 | neighbors=[.is_connected()] | lang=en
- "websocket_manager_rationale_191": "Check if a specific agent is online (connected + not busy)." | kind=entity | source=manager/backend/app/websocket/manager.py:L191 | neighbors=[.is_online()] | lang=en
- "websocket_manager_rationale_196": "Return a snapshot of all connected agent IDs." | kind=entity | source=manager/backend/app/websocket/manager.py:L196 | neighbors=[.connected_agents()] | lang=en
- "websocket_manager_rationale_201": "Return agent IDs whose status is 'online' (idle, ready for job)." | kind=entity | source=manager/backend/app/websocket/manager.py:L201 | neighbors=[.online_agents()] | lang=en
- "websocket_manager_rationale_209": "Return 'online', 'busy', or 'offline'." | kind=entity | source=manager/backend/app/websocket/manager.py:L209 | neighbors=[.get_agent_status()] | lang=en
- "websocket_manager_rationale_213": "Return agent_ids whose last heartbeat is older than `seconds`.          These ag" | kind=entity | source=manager/backend/app/websocket/manager.py:L213 | neighbors=[.agent_stale_after()] | lang=en
- "websocket_manager_rationale_230": "High-level manager for graph-specific WebSocket operations." | kind=entity | source=manager/backend/app/websocket/manager.py:L230 | neighbors=[GraphWebSocketManager] | lang=en
- "websocket_manager_rationale_237": "Handle a new WebSocket client connection." | kind=entity | source=manager/backend/app/websocket/manager.py:L237 | neighbors=[.handle_client()] | lang=pt
- "websocket_manager_rationale_257": "Handle incoming WebSocket messages." | kind=entity | source=manager/backend/app/websocket/manager.py:L257 | neighbors=[._handle_message()] | lang=en
- "websocket_manager_rationale_26": "Manages WebSocket connections with room-based broadcasting." | kind=entity | source=manager/backend/app/websocket/manager.py:L26 | neighbors=[ConnectionManager] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-101.json

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
