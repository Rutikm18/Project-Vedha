# Node Description Batch 321 of 330

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

- "versions_0023_customer_portal_foundation_rationale_1": "Customer portal foundation (Part 2, Phase 0): client role, engagement↔agent assi" | kind=entity | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L1 | neighbors=[0023_customer_portal_foundation.py] | lang=en
- "versions_0023_customer_portal_foundation_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L19 | neighbors=[0023_customer_portal_foundation.py] | lang=en
- "versions_0024_device_role_inventory_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L33 | neighbors=[0024_device_role_inventory.py] | lang=en
- "versions_0024_device_role_inventory_rationale_1": "Device-role inventory: persist the probe device_classifier's role on assets.  Ad" | kind=entity | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L1 | neighbors=[0024_device_role_inventory.py] | lang=en
- "versions_0024_device_role_inventory_rationale_37": "# NOTE: Postgres cannot DROP a single enum value; the added 'printer' /" | kind=entity | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L37 | neighbors=[0024_device_role_inventory.py] | lang=en
- "versions_0024_device_role_inventory_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L22 | neighbors=[0024_device_role_inventory.py] | lang=en
- "versions_0025_service_exposure_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0025_service_exposure.py:L25 | neighbors=[0025_service_exposure.py] | lang=en
- "versions_0025_service_exposure_rationale_1": "Service exposure: persist the exposure_matrix reachability verdict.  Adds servic" | kind=entity | source=manager/backend/alembic/versions/0025_service_exposure.py:L1 | neighbors=[0025_service_exposure.py] | lang=en
- "versions_0025_service_exposure_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0025_service_exposure.py:L21 | neighbors=[0025_service_exposure.py] | lang=en
- "versions_0026_client_portal_slug_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0026_client_portal_slug.py:L29 | neighbors=[0026_client_portal_slug.py] | lang=en
- "versions_0026_client_portal_slug_rationale_1": "Client portal slug — the customer's stable 'user as domain' handle.  Adds users." | kind=entity | source=manager/backend/alembic/versions/0026_client_portal_slug.py:L1 | neighbors=[0026_client_portal_slug.py] | lang=en
- "versions_0026_client_portal_slug_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0026_client_portal_slug.py:L22 | neighbors=[0026_client_portal_slug.py] | lang=en
- "versions_0027_scan_request_targets_intensity_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0027_scan_request_targets_intensity.py:L39 | neighbors=[0027_scan_request_targets_intensity.py] | lang=en
- "versions_0027_scan_request_targets_intensity_rationale_1": "Scan-request targets + intensity — the rich customer scan request.  Adds two nul" | kind=entity | source=manager/backend/alembic/versions/0027_scan_request_targets_intensity.py:L1 | neighbors=[0027_scan_request_targets_intensity.py] | lang=en
- "versions_0027_scan_request_targets_intensity_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0027_scan_request_targets_intensity.py:L28 | neighbors=[0027_scan_request_targets_intensity.py] | lang=en
- "versions_0028_remediation_plans_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0028_remediation_plans.py:L51 | neighbors=[0028_remediation_plans.py] | lang=en
- "versions_0028_remediation_plans_rationale_1": "Remediation plans — cached, OS-specific, structured remediation for a finding." | kind=entity | source=manager/backend/alembic/versions/0028_remediation_plans.py:L1 | neighbors=[0028_remediation_plans.py] | lang=en
- "versions_0028_remediation_plans_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0028_remediation_plans.py:L22 | neighbors=[0028_remediation_plans.py] | lang=en
- "versions_0030_sla_policies_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0030_sla_policies.py:L42 | neighbors=[0030_sla_policies.py] | lang=en
- "versions_0030_sla_policies_rationale_1": "SLA policies — per-tenant custom remediation windows (hours per severity).  One" | kind=entity | source=manager/backend/alembic/versions/0030_sla_policies.py:L1 | neighbors=[0030_sla_policies.py] | lang=it
- "versions_0030_sla_policies_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0030_sla_policies.py:L21 | neighbors=[0030_sla_policies.py] | lang=en
- "versions_0031_integrations_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0031_integrations.py:L42 | neighbors=[0031_integrations.py] | lang=en
- "versions_0031_integrations_rationale_1": "Integrations — per-tenant notification config (email / Slack / Jira).  One row p" | kind=entity | source=manager/backend/alembic/versions/0031_integrations.py:L1 | neighbors=[0031_integrations.py] | lang=en
- "versions_0031_integrations_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0031_integrations.py:L21 | neighbors=[0031_integrations.py] | lang=en
- "versions_0032_scan_request_use_case_downgrade": "downgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0032_scan_request_use_case.py:L29 | neighbors=[0032_scan_request_use_case.py] | lang=en
- "versions_0032_scan_request_use_case_rationale_1": "scan_requests.use_case_id — the capability use-case a customer requested.  The p" | kind=entity | source=manager/backend/alembic/versions/0032_scan_request_use_case.py:L1 | neighbors=[0032_scan_request_use_case.py] | lang=en
- "versions_0032_scan_request_use_case_upgrade": "upgrade()" | kind=code-symbol | source=manager/backend/alembic/versions/0032_scan_request_use_case.py:L22 | neighbors=[0032_scan_request_use_case.py] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-320.json

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
