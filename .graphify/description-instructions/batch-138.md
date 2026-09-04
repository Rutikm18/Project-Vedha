# Node Description Batch 139 of 332

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

- "routers_customer_access_reject_scan_request": "reject_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L358 | neighbors=[customer_access.py, _get_scan_request()]
- "routers_customer_access_rejectbody": "RejectBody" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L89 | neighbors=[customer_access.py, BaseModel]
- "routers_customer_access_scanrequestout": "ScanRequestOut" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L75 | neighbors=[customer_access.py, BaseModel]
- "routers_detection_get_results": "get_results()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L128 | neighbors=[detection.py, _result_out()]
- "routers_detection_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L217 | neighbors=[detection.py, get_results()]
- "routers_detection_runs_latest_run_delta": "latest_run_delta()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L72 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_runs_list_detection_runs": "list_detection_runs()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L55 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L322 | neighbors=[detection.py, _run_correlation()]
- "routers_engagements_bulk_import_assets": "bulk_import_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L579 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_create_engagement": "create_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L378 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_detection_explain": "detection_explain()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1109 | neighbors=[engagements.py, The machine-readable answer to "the scr…]
- "routers_engagements_raw_facts": "raw_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1162 | neighbors=[engagements.py, The raw ScanResult facts as the probe s…]
- "routers_engagements_update_engagement": "update_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L545 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_exploits_approve_exploit": "approve_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L244 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_get_result_or_404": "_get_result_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L395 | neighbors=[exploits.py, get_exploit_result()]
- "routers_exploits_list_approvals": "list_approvals()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L217 | neighbors=[exploits.py, _approval_out()]
- "routers_exploits_list_exploit_results": "list_exploit_results()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L176 | neighbors=[exploits.py, _result_out()]
- "routers_exploits_load_finding_and_eng": "_load_finding_and_eng()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L368 | neighbors=[exploits.py, run_exploit()]
- "routers_exploits_reject_exploit": "reject_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L302 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_run_exploit": "run_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L110 | neighbors=[exploits.py, _load_finding_and_eng()]
- "routers_findings_patch_finding": "patch_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L281 | neighbors=[findings.py, _tenant_finding()]
- "routers_findings_rationale_50": "Build the detail contract with bounded asset context.      Portfolio/list respon" | kind=entity | source=manager/backend/app/routers/findings.py:L50 | neighbors=[_finding_detail_out(), sla_summary()]
- "routers_health_health_auth": "health_auth()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L81 | neighbors=[health.py, Validates the authentication subsystem …]
- "routers_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/routers/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "routers_integrations_delete_integration": "delete_integration()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L93 | neighbors=[integrations.py, _row()]
- "routers_integrations_integration_secret": "integration_secret()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L117 | neighbors=[integrations.py, Decrypt an integration's secret for the…]
- "routers_integrations_integrationin": "IntegrationIn" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L30 | neighbors=[integrations.py, BaseModel]
- "routers_integrations_list_integrations": "list_integrations()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L56 | neighbors=[integrations.py, _out()]
- "routers_integrations_test_integrations": "test_integrations()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L106 | neighbors=[integrations.py, Enqueue a durable test notification; th…]
- "routers_portal_create_scan_request": "create_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L321 | neighbors=[portal.py, _portal_use_cases()]
- "routers_portal_portal_agents": "portal_agents()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L549 | neighbors=[portal.py, The customer's own probe fleet — normal…]
- "routers_portal_portal_assistant_chat": "portal_assistant_chat()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L435 | neighbors=[portal.py, _assistant_finding_view()]
- "routers_portal_portal_engagement": "portal_engagement()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L88 | neighbors=[portal.py, _enum_val()]
- "routers_portal_portal_scans": "portal_scans()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L275 | neighbors=[portal.py, _enum_val()]
- "routers_portal_portal_trends": "portal_trends()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L235 | neighbors=[portal.py, _metric_finding()]
- "routers_probe_enrollment_create_enroll_token": "create_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L770 | neighbors=[probe_enrollment.py, generate_enroll_token()]
- "routers_probe_enrollment_derive_refresh_secret": "_derive_refresh_secret()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L49 | neighbors=[probe_enrollment.py, activate_enrollment()]
- "routers_probe_enrollment_enrollmentactivate": "EnrollmentActivate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L144 | neighbors=[probe_enrollment.py, EnrollmentSecret]
- "routers_probe_enrollment_enrollmentcreate_validate_key": ".validate_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L128 | neighbors=[EnrollmentCreate, _decode_public_key()]
- "routers_probe_enrollment_enrolltokencreate": "EnrollTokenCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L133 | neighbors=[probe_enrollment.py, BaseModel]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-138.json

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
