# Node Description Batch 75 of 227

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "routers_ai_report_pending_outputs": "_pending_outputs()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L218 | neighbors=[ai_report.py, approve_report(), reject_report()]
- "routers_analytics_posture": "posture()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L124 | neighbors=[analytics.py, _finding_views(), _two_latest_completed_runs()]
- "routers_attack_paths_blast_radius": "blast_radius()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L136 | neighbors=[attack_paths.py, _asset_labels(), _build_analyzer()]
- "routers_attack_paths_get_attack_path": "get_attack_path()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L74 | neighbors=[attack_paths.py, _asset_labels(), _explain_hop()]
- "routers_attack_paths_list_attack_paths": "list_attack_paths()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L42 | neighbors=[attack_paths.py, _path_summary(), _recompute_and_store()]
- "routers_customer_access_approve_scan_request": "approve_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L325 | neighbors=[customer_access.py, build_scan_job(), _get_scan_request()]
- "routers_customer_access_customerlistitem": "CustomerListItem" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L382 | neighbors=[customer_access.py, BaseModel, list_customers()]
- "routers_customer_access_get_client_user": "get_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L227 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user()]
- "routers_customer_access_get_scan_request": "_get_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L292 | neighbors=[customer_access.py, approve_scan_request(), reject_scan_request()]
- "routers_customer_access_revealout": "RevealOut" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L417 | neighbors=[customer_access.py, reveal_customer_password(), BaseModel]
- "routers_detection_run_correlation": "_run_correlation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L233 | neighbors=[detection.py, Background task: pull SIEM/EDR telemetr…, _set_job()]
- "routers_detection_runs_run_dict": "_run_dict()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L36 | neighbors=[detection_runs.py, latest_run_delta(), list_detection_runs()]
- "routers_engagements_get_engagement_scope": "get_engagement_scope()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L663 | neighbors=[engagements.py, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…]
- "routers_engagements_overview_cache_key": "_overview_cache_key()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L35 | neighbors=[engagements.py, engagements_overview(), _refresh_overview_cache()]
- "routers_engagements_re_detect": "re_detect()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L123 | neighbors=[engagements.py, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …]
- "routers_exploits_approval_out": "_approval_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L433 | neighbors=[exploits.py, ApprovalOut, list_approvals()]
- "routers_exploits_get_approval_or_404": "_get_approval_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L408 | neighbors=[exploits.py, approve_exploit(), reject_exploit()]
- "routers_exploits_get_exploit_result": "get_exploit_result()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L205 | neighbors=[exploits.py, _get_result_or_404(), _result_out()]
- "routers_exploits_run_approved_exploit": "_run_approved_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L445 | neighbors=[exploits.py, Background task: run the exploit after …, Background task: run the exploit after …]
- "routers_health_health_startup": "health_startup()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L162 | neighbors=[health.py, Returns the cached report from the last…, Returns the cached report from the last…]
- "routers_integrations_integrationout": "IntegrationOut" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L36 | neighbors=[integrations.py, BaseModel, _out()]
- "routers_integrations_put_integration": "put_integration()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L65 | neighbors=[integrations.py, _out(), _row()]
- "routers_integrations_row": "_row()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L48 | neighbors=[integrations.py, delete_integration(), put_integration()]
- "routers_portal_portal_finding_remediation": "portal_finding_remediation()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L130 | neighbors=[portal.py, Customer-facing structured remediation,…, Customer-facing structured remediation,…]
- "routers_portal_portal_posture": "portal_posture()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L165 | neighbors=[portal.py, _posture_view(), _enum_val()]
- "routers_portal_portal_summary": "portal_summary()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L197 | neighbors=[portal.py, _metric_finding(), _posture_view()]
- "routers_portal_portal_use_cases": "_portal_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L70 | neighbors=[portal.py, create_scan_request(), The operator use-case catalog (single s…]
- "routers_probe_enrollment_approve_enrollment": "approve_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L611 | neighbors=[probe_enrollment.py, _keyed_hash(), _provision_agent_for_site()]
- "routers_probe_enrollment_enrollmentcreate": "EnrollmentCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L113 | neighbors=[probe_enrollment.py, BaseModel, .validate_key()]
- "routers_probe_enrollment_enrollmentsecret": "EnrollmentSecret" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L140 | neighbors=[probe_enrollment.py, EnrollmentActivate, BaseModel]
- "routers_probe_enrollment_keyed_hash": "_keyed_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L41 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request()]
- "routers_probe_enrollment_next_probe_name": "_next_probe_name()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L546 | neighbors=[probe_enrollment.py, approve_request_simple(), Auto-assign the next sequential probe n…]
- "routers_probe_enrollment_poll_enrollment": "poll_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L491 | neighbors=[probe_enrollment.py, _authenticated_request(), _rate_limit()]
- "routers_remediation_build_upsert_stmt": "_build_upsert_stmt()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L62 | neighbors=[remediation.py, Build the atomic INSERT … ON CONFLICT D…, _upsert_plan()]
- "routers_remediation_cached_plan": "_cached_plan()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L52 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_remediation_serialize": "_serialize()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L103 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_sla_policy_get_sla_policy": "get_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L81 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_put_sla_policy": "put_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L86 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_slapolicyout": "SlaPolicyOut" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L30 | neighbors=[sla_policy.py, _out(), BaseModel]
- "routers_validation_approve_validation": "approve_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L214 | neighbors=[validation.py, _get_request_or_404(), _roe_allows_active_validation()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-074.json

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
