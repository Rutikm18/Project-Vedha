# Node Description Batch 221 of 227

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
- "versions_0016_user_tenant_is_active_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L53 | neighbors=[0016_user_tenant_is_active.py]
- "versions_0016_user_tenant_is_active_rationale_1": "Add is_active to users and tenants; add password_expires_at to users.  All exist" | kind=entity | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L1 | neighbors=[0016_user_tenant_is_active.py]
- "versions_0016_user_tenant_is_active_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L21 | neighbors=[0016_user_tenant_is_active.py]
- "versions_0017_scan_job_attempts_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L105 | neighbors=[0017_scan_job_attempts.py]
- "versions_0017_scan_job_attempts_rationale_1": "Add fenced execution attempts for agent-dispatched scan jobs.  Revision ID: 0017" | kind=entity | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L1 | neighbors=[0017_scan_job_attempts.py]
- "versions_0017_scan_job_attempts_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L18 | neighbors=[0017_scan_job_attempts.py]
- "versions_0018_probe_enrollment_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L129 | neighbors=[0018_probe_enrollment.py]
- "versions_0018_probe_enrollment_rationale_1": "Add Manager-approved device-key probe enrollment and Site policy.  Revision ID:" | kind=entity | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L1 | neighbors=[0018_probe_enrollment.py]
- "versions_0018_probe_enrollment_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L18 | neighbors=[0018_probe_enrollment.py]
- "versions_0020_finding_resolution_lifecycle_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py:L31 | neighbors=[0020_finding_resolution_lifecycle.py]
- "versions_0020_finding_resolution_lifecycle_rationale_1": "Finding resolution lifecycle: coverage-gated auto-resolution columns.  Revision" | kind=entity | source=manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py:L1 | neighbors=[0020_finding_resolution_lifecycle.py]
- "versions_0020_finding_resolution_lifecycle_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py:L18 | neighbors=[0020_finding_resolution_lifecycle.py]
- "versions_0021_finding_verification_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0021_finding_verification.py:L27 | neighbors=[0021_finding_verification.py]
- "versions_0021_finding_verification_rationale_1": "Finding verification verdict columns (P2 passive verification).  Revision ID: 00" | kind=entity | source=manager/backend/alembic/versions/0021_finding_verification.py:L1 | neighbors=[0021_finding_verification.py]
- "versions_0021_finding_verification_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0021_finding_verification.py:L17 | neighbors=[0021_finding_verification.py]
- "versions_0022_validation_requests_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0022_validation_requests.py:L43 | neighbors=[0022_validation_requests.py]
- "versions_0022_validation_requests_rationale_1": "Approval-gated safe active-validation requests (P3).  Revision ID: 0022 Revises:" | kind=entity | source=manager/backend/alembic/versions/0022_validation_requests.py:L1 | neighbors=[0022_validation_requests.py]
- "versions_0022_validation_requests_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0022_validation_requests.py:L18 | neighbors=[0022_validation_requests.py]
- "versions_0023_customer_portal_foundation_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L64 | neighbors=[0023_customer_portal_foundation.py]
- "versions_0023_customer_portal_foundation_rationale_1": "Customer portal foundation (Part 2, Phase 0): client role, engagement↔agent assi" | kind=entity | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L1 | neighbors=[0023_customer_portal_foundation.py]
- "versions_0023_customer_portal_foundation_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L19 | neighbors=[0023_customer_portal_foundation.py]
- "versions_0024_device_role_inventory_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L33 | neighbors=[0024_device_role_inventory.py]
- "versions_0024_device_role_inventory_rationale_1": "Device-role inventory: persist the probe device_classifier's role on assets.  Ad" | kind=entity | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L1 | neighbors=[0024_device_role_inventory.py]
- "versions_0024_device_role_inventory_rationale_37": "# NOTE: Postgres cannot DROP a single enum value; the added 'printer' /" | kind=entity | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L37 | neighbors=[0024_device_role_inventory.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-220.json

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
