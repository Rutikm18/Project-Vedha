# Node Description Batch 115 of 119

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

- "versions_0009_outbox_events_rationale_1": "Transactional outbox for durable background work (detection, etc.).  Producers i" | kind=entity | source=manager/backend/alembic/versions/0009_outbox_events.py:L1 | neighbors=[0009_outbox_events.py]
- "versions_0009_outbox_events_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0009_outbox_events.py:L23 | neighbors=[0009_outbox_events.py]
- "versions_0010_detection_runs_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L63 | neighbors=[0010_detection_runs.py]
- "versions_0010_detection_runs_rationale_1": "Temporal detection: detection_runs table + finding provenance columns.  Records" | kind=entity | source=manager/backend/alembic/versions/0010_detection_runs.py:L1 | neighbors=[0010_detection_runs.py]
- "versions_0010_detection_runs_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L23 | neighbors=[0010_detection_runs.py]
- "versions_0011_job_lease_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L33 | neighbors=[0011_job_lease.py]
- "versions_0011_job_lease_rationale_1": "Job leasing: scan_jobs.lease_expires_at for the dead-probe reaper.  A claimed (r" | kind=entity | source=manager/backend/alembic/versions/0011_job_lease.py:L1 | neighbors=[0011_job_lease.py]
- "versions_0011_job_lease_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L21 | neighbors=[0011_job_lease.py]
- "versions_0012_agent_recommendations_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L48 | neighbors=[0012_agent_recommendations.py]
- "versions_0012_agent_recommendations_rationale_1": "Agentic AI advisor: agent_recommendations (recommend-only, human-approved).  Sto" | kind=entity | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L1 | neighbors=[0012_agent_recommendations.py]
- "versions_0012_agent_recommendations_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L22 | neighbors=[0012_agent_recommendations.py]
- "versions_0013_agent_public_key_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L26 | neighbors=[0013_agent_public_key.py]
- "versions_0013_agent_public_key_rationale_1": "Add agents.public_key (Phase-4 X25519 identity for scope encryption).  The probe" | kind=entity | source=manager/backend/alembic/versions/0013_agent_public_key.py:L1 | neighbors=[0013_agent_public_key.py]
- "versions_0013_agent_public_key_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L22 | neighbors=[0013_agent_public_key.py]
- "versions_0015_finding_risk_score_scale_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L27 | neighbors=[0015_finding_risk_score_scale.py]
- "versions_0015_finding_risk_score_scale_rationale_1": "Allow the documented 0-1000 finding risk score range.  Revision ID: 0015 Revises" | kind=entity | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L1 | neighbors=[0015_finding_risk_score_scale.py]
- "versions_0015_finding_risk_score_scale_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L17 | neighbors=[0015_finding_risk_score_scale.py]
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
- "websocket_manager_agentconnectionmanager_connected_count": ".connected_count()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L266 | neighbors=[AgentConnectionManager]
- "websocket_manager_agentconnectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L86 | neighbors=[AgentConnectionManager]
- "websocket_manager_connectionmanager_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L28 | neighbors=[ConnectionManager]
- "websocket_manager_rationale_1": "WebSocket manager for real-time graph updates, agent push, and live collaboratio" | kind=entity | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[manager.py]
- "websocket_manager_rationale_123": "Remove an agent's WebSocket registration." | kind=entity | source=manager/backend/app/websocket/manager.py:L123 | neighbors=[.unregister()]
- "websocket_manager_rationale_129": "Remove the current registration, optionally only for one socket.          Return" | kind=entity | source=manager/backend/app/websocket/manager.py:L129 | neighbors=[.unregister()]
- "websocket_manager_rationale_136": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L136 | neighbors=[.record_heartbeat()]
- "websocket_manager_rationale_147": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L147 | neighbors=[.push_job()]
- "websocket_manager_rationale_153": "Record a heartbeat from an agent." | kind=entity | source=manager/backend/app/websocket/manager.py:L153 | neighbors=[.record_heartbeat()]
- "websocket_manager_rationale_165": "Push a job to the first online connected agent.          Returns the agent_id th" | kind=entity | source=manager/backend/app/websocket/manager.py:L165 | neighbors=[.push_job_to_first_online()]
- "websocket_manager_rationale_166": "Record transport features explicitly advertised by a connected probe." | kind=entity | source=manager/backend/app/websocket/manager.py:L166 | neighbors=[.record_features()]
- "websocket_manager_rationale_181": "Push a job to a specific agent over WebSocket.          Returns True if the job" | kind=entity | source=manager/backend/app/websocket/manager.py:L181 | neighbors=[.push_job()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-114.json

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
