# Node Description Batch 63 of 134

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

- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L681 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_job_params_contain_secret": "_job_params_contain_secret()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L73 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L585 | neighbors=[agents.py, AgentRegisterResponse]
- "routers_agents_submit_job_result": "submit_job_result()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1089 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_ai_report_approve_report": "approve_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L136 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_get_draft": "get_draft()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L119 | neighbors=[ai_report.py, _output_out()]
- "routers_ai_report_output_out": "_output_out()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L228 | neighbors=[ai_report.py, get_draft()]
- "routers_ai_report_reject_report": "reject_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L158 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L420 | neighbors=[ai_report.py, _run_generation()]
- "routers_analytics_sev_str": "_sev_str()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L82 | neighbors=[analytics.py, _finding_views()]
- "routers_analytics_two_latest_completed_runs": "_two_latest_completed_runs()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L106 | neighbors=[analytics.py, posture()]
- "routers_attack_paths_explain_hop": "_explain_hop()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L245 | neighbors=[attack_paths.py, get_attack_path()]
- "routers_attack_paths_path_summary": "_path_summary()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L234 | neighbors=[attack_paths.py, list_attack_paths()]
- "routers_detection_get_results": "get_results()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L128 | neighbors=[detection.py, _result_out()]
- "routers_detection_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L217 | neighbors=[detection.py, get_results()]
- "routers_detection_runs_latest_run_delta": "latest_run_delta()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L72 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_runs_list_detection_runs": "list_detection_runs()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L55 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L322 | neighbors=[detection.py, _run_correlation()]
- "routers_engagements_bulk_import_assets": "bulk_import_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L552 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_create_engagement": "create_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L351 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_update_engagement": "update_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L518 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_exploits_approve_exploit": "approve_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L244 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_get_result_or_404": "_get_result_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L395 | neighbors=[exploits.py, get_exploit_result()]
- "routers_exploits_list_approvals": "list_approvals()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L217 | neighbors=[exploits.py, _approval_out()]
- "routers_exploits_list_exploit_results": "list_exploit_results()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L176 | neighbors=[exploits.py, _result_out()]
- "routers_exploits_load_finding_and_eng": "_load_finding_and_eng()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L368 | neighbors=[exploits.py, run_exploit()]
- "routers_exploits_reject_exploit": "reject_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L302 | neighbors=[exploits.py, _get_approval_or_404()]
- "routers_exploits_run_exploit": "run_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L110 | neighbors=[exploits.py, _load_finding_and_eng()]
- "routers_findings_get_finding": "get_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L200 | neighbors=[findings.py, _tenant_finding()]
- "routers_findings_patch_finding": "patch_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L209 | neighbors=[findings.py, _tenant_finding()]
- "routers_health_health_auth": "health_auth()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L81 | neighbors=[health.py, Validates the authentication subsystem …]
- "routers_health_health_startup": "health_startup()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L164 | neighbors=[health.py, Returns the cached report from the last…]
- "routers_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/routers/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "routers_probe_enrollment_create_enroll_token": "create_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L610 | neighbors=[probe_enrollment.py, generate_enroll_token()]
- "routers_probe_enrollment_derive_refresh_secret": "_derive_refresh_secret()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L48 | neighbors=[probe_enrollment.py, activate_enrollment()]
- "routers_probe_enrollment_enrollmentactivate": "EnrollmentActivate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L143 | neighbors=[probe_enrollment.py, EnrollmentSecret]
- "routers_probe_enrollment_enrollmentcreate_validate_key": ".validate_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L127 | neighbors=[EnrollmentCreate, _decode_public_key()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-062.json

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
