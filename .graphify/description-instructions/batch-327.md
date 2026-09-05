# Node Description Batch 328 of 336

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

- "versions_0033_finding_events_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0033_finding_events.py:L47 | neighbors=[0033_finding_events.py] | lang=en
- "versions_0033_finding_events_rationale_1": "Finding lifecycle audit trail — append-only per-finding event log.  One row per" | kind=entity | source=manager/backend/alembic/versions/0033_finding_events.py:L1 | neighbors=[0033_finding_events.py] | lang=it
- "versions_0033_finding_events_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0033_finding_events.py:L23 | neighbors=[0033_finding_events.py] | lang=en
- "versions_0034_run_lease_worker_heartbeat_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0034_run_lease_worker_heartbeat.py:L54 | neighbors=[0034_run_lease_worker_heartbeat.py] | lang=en
- "versions_0034_run_lease_worker_heartbeat_rationale_1": "Stage 2b: DetectionRun lease + worker heartbeat (precise liveness).  Two additiv" | kind=entity | source=manager/backend/alembic/versions/0034_run_lease_worker_heartbeat.py:L1 | neighbors=[0034_run_lease_worker_heartbeat.py] | lang=en
- "versions_0034_run_lease_worker_heartbeat_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0034_run_lease_worker_heartbeat.py:L31 | neighbors=[0034_run_lease_worker_heartbeat.py] | lang=en
- "versions_0035_engagement_lifecycle_states_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0035_engagement_lifecycle_states.py:L44 | neighbors=[0035_engagement_lifecycle_states.py] | lang=en
- "versions_0035_engagement_lifecycle_states_rationale_1": "engagement lifecycle: add 'ongoing' and 'running' states  The engagement lifecyc" | kind=entity | source=manager/backend/alembic/versions/0035_engagement_lifecycle_states.py:L1 | neighbors=[0035_engagement_lifecycle_states.py] | lang=en
- "versions_0035_engagement_lifecycle_states_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0035_engagement_lifecycle_states.py:L39 | neighbors=[0035_engagement_lifecycle_states.py] | lang=en
- "versions_0036_scan_job_reference_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0036_scan_job_reference.py:L78 | neighbors=[0036_scan_job_reference.py] | lang=en
- "versions_0036_scan_job_reference_rationale_1": "scan jobs get a human-readable reference (SCN-YYMMDD-XXXXXX)  A scan job could o" | kind=entity | source=manager/backend/alembic/versions/0036_scan_job_reference.py:L1 | neighbors=[0036_scan_job_reference.py] | lang=pt
- "versions_0036_scan_job_reference_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0036_scan_job_reference.py:L31 | neighbors=[0036_scan_job_reference.py] | lang=en
- "versions_0037_scan_job_cancelled_status_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L40 | neighbors=[0037_scan_job_cancelled_status.py] | lang=en
- "versions_0037_scan_job_cancelled_status_rationale_1": "scan jobs gain a terminal `cancelled` status  An operator could start work but n" | kind=entity | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L1 | neighbors=[0037_scan_job_cancelled_status.py] | lang=en
- "versions_0037_scan_job_cancelled_status_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0037_scan_job_cancelled_status.py:L34 | neighbors=[0037_scan_job_cancelled_status.py] | lang=en
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
- "websocket_manager_agentconnectionmanager_connected_count": ".connected_count()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L331 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_agentconnectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L88 | neighbors=[AgentConnectionManager] | lang=en
- "websocket_manager_connectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L30 | neighbors=[ConnectionManager] | lang=en
- "websocket_manager_rationale_1": "WebSocket manager for real-time graph updates, agent push, and live collaboratio" | kind=entity | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[manager.py] | lang=en
- "websocket_manager_rationale_101": "Register an agent's WebSocket connection.          If the agent already has a co" | kind=entity | source=manager/backend/app/websocket/manager.py:L101 | neighbors=[.register()] | lang=en
- "websocket_manager_rationale_123": "Remove an agent's WebSocket registration." | kind=entity | source=manager/backend/app/websocket/manager.py:L123 | neighbors=[.unregister()] | lang=en
- "websocket_manager_rationale_129": "Remove the current registration, optionally only for one socket.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L129 | neighbors=[.unregister()] | lang=en
- "websocket_manager_rationale_131": "Remove the current registration, optionally only for one socket.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L131 | neighbors=[.unregister()] | lang=en
- "websocket_manager_rationale_136": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L136 | neighbors=[.record_heartbeat()] | lang=en
- "websocket_manager_rationale_147": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L147 | neighbors=[.push_job()] | lang=en
- "websocket_manager_rationale_153": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L153 | neighbors=[.record_heartbeat()] | lang=en
- "websocket_manager_rationale_155": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L155 | neighbors=[.record_heartbeat()] | lang=en
- "websocket_manager_rationale_165": "Push a job to the first online connected agent.          Returns the agent_id th" | kind=entity | source=manager/backend/app/websocket/manager.py:L165 | neighbors=[.push_job_to_first_online()] | lang=en
- "websocket_manager_rationale_166": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L166 | neighbors=[.record_features()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-327.json

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
