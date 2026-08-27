# Node Description Batch 77 of 236

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

- "prompts_triage": "triage.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/triage.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, 298a9d4 trim frontend to 7 core pages; …]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[AIClient, _Scanner, _Scanner]
- "routers_ad_run_ad_assessment_and_save": "_run_ad_assessment_and_save()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L129 | neighbors=[ad.py, Background task: run the AD assessment …, _set_job_status()]
- "routers_agent_ws_rationale_1": "agent_ws.py — WebSocket endpoint for probe push connectivity.  Probes connect vi" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[agent_ws.py, Engagement, ScanJob]
- "routers_agent_ws_rationale_131": "Persistent WebSocket for probe → manager push communication.      Authentication" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L131 | neighbors=[Engagement, ScanJob, agent_websocket_endpoint()]
- "routers_agent_ws_rationale_42": "Read an agent bearer token exclusively from the non-logged auth header." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L42 | neighbors=[Engagement, ScanJob, _agent_token_from_websocket()]
- "routers_agent_ws_rationale_53": "Validate eligibility and atomically claim a WebSocket job offer." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L53 | neighbors=[Engagement, ScanJob, _claim_pushed_job()]
- "routers_agents_agentbootstraprequest": "AgentBootstrapRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L589 | neighbors=[agents.py, BaseModel, .validate_network_segments()]
- "routers_agents_get_agent_job_history": "get_agent_job_history()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1044 | neighbors=[agents.py, Read-only per-probe job list — the prob…, Read-only per-probe job list — the prob…]
- "routers_agents_refresh_agent_registration": "refresh_agent_registration()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L865 | neighbors=[agents.py, _agent_ownership_check(), _scope_is_reachable()]
- "routers_agents_resolve_scan_type": "_resolve_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L88 | neighbors=[agents.py, enqueue_agent_job(), _required_scan_type()]
- "routers_ai_report_build_engagement_summary": "_build_engagement_summary()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L241 | neighbors=[ai_report.py, _run_generation(), _run_regeneration()]
- "routers_ai_report_build_posture_report_section": "build_posture_report_section()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L191 | neighbors=[ai_report.py, Deterministic report section from the s…, _run_generation()]
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
- "routers_engagements_overview_cache_key": "_overview_cache_key()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L36 | neighbors=[engagements.py, engagements_overview(), _refresh_overview_cache()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-076.json

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
