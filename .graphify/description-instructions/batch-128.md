# Node Description Batch 129 of 134

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

- "versions_0001_initial_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L174 | neighbors=[0001_initial.py]
- "versions_0001_initial_rationale_1": "Initial schema — all tables  Revision ID: 0001 Revises: Create Date: 2026-05-19" | kind=entity | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[0001_initial.py]
- "versions_0001_initial_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L19 | neighbors=[0001_initial.py]
- "versions_0002_services_agents_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L59 | neighbors=[0002_services_agents.py]
- "versions_0002_services_agents_rationale_1": "Add services and agents tables  Revision ID: 0002 Revises: 0001 Create Date: 202" | kind=entity | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[0002_services_agents.py]
- "versions_0002_services_agents_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L19 | neighbors=[0002_services_agents.py]
- "versions_0003_vuln_scan_fields_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L43 | neighbors=[0003_vuln_scan_fields.py]
- "versions_0003_vuln_scan_fields_rationale_1": "Add enrichment fields index + webhook column to engagements  Revision ID: 0003 R" | kind=entity | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[0003_vuln_scan_fields.py]
- "versions_0003_vuln_scan_fields_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L18 | neighbors=[0003_vuln_scan_fields.py]
- "versions_0004_exploit_tables_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L93 | neighbors=[0004_exploit_tables.py]
- "versions_0004_exploit_tables_rationale_1": "Exploit results, approvals, and audit log tables  Revision ID: 0004 Revises: 000" | kind=entity | source=manager/backend/alembic/versions/0004_exploit_tables.py:L1 | neighbors=[0004_exploit_tables.py]
- "versions_0004_exploit_tables_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L19 | neighbors=[0004_exploit_tables.py]
- "versions_0005_detection_validation_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L80 | neighbors=[0005_detection_validation.py]
- "versions_0005_detection_validation_rationale_1": "Detection validation: attack_timeline, detection_configs, extend detection_resul" | kind=entity | source=manager/backend/alembic/versions/0005_detection_validation.py:L1 | neighbors=[0005_detection_validation.py]
- "versions_0005_detection_validation_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L19 | neighbors=[0005_detection_validation.py]
- "versions_0006_llm_outputs_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L48 | neighbors=[0006_llm_outputs.py]
- "versions_0006_llm_outputs_rationale_1": "AI engine: llm_outputs table + reviewstatus enum  Revision ID: 0006 Revises: 000" | kind=entity | source=manager/backend/alembic/versions/0006_llm_outputs.py:L1 | neighbors=[0006_llm_outputs.py]
- "versions_0006_llm_outputs_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L19 | neighbors=[0006_llm_outputs.py]
- "versions_0007_scale_indexes_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L35 | neighbors=[0007_scale_indexes.py]
- "versions_0007_scale_indexes_rationale_1": "P3: composite indexes for the hot aggregate + poll query paths.  The dashboard's" | kind=entity | source=manager/backend/alembic/versions/0007_scale_indexes.py:L1 | neighbors=[0007_scale_indexes.py]
- "versions_0007_scale_indexes_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L22 | neighbors=[0007_scale_indexes.py]
- "versions_0008_scan_results_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L39 | neighbors=[0008_scan_results.py]
- "versions_0008_scan_results_rationale_1": "P3-#10: append-only scan_results table (raw facts).  Decouples the (large) raw f" | kind=entity | source=manager/backend/alembic/versions/0008_scan_results.py:L1 | neighbors=[0008_scan_results.py]
- "versions_0008_scan_results_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L21 | neighbors=[0008_scan_results.py]
- "versions_0009_outbox_events_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0009_outbox_events.py:L45 | neighbors=[0009_outbox_events.py]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-128.json

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
