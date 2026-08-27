# Node Description Batch 102 of 236

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

- "reports_page_fmtdate": "fmtDate()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L27 | neighbors=[page.tsx, PortalReports()]
- "reports_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L84 | neighbors=[page.tsx, ReportsPage()]
- "reports_page_portalreports": "PortalReports()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L179 | neighbors=[page.tsx, fmtDate()]
- "reports_page_reportcontent": "ReportContent" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L15 | neighbors=[page.tsx, PortalReport]
- "reports_page_reportspage": "ReportsPage()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L297 | neighbors=[page.tsx, formatDate()]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_enqueuejobrequest_validate_intensity": "._validate_intensity()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L321 | neighbors=[EnqueueJobRequest, _normalize_intensity_name()]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L820 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_job_params_contain_secret": "_job_params_contain_secret()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L74 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_rationale_548": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L548 | neighbors=[list_use_cases(), bootstrap_agent()]
- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L724 | neighbors=[agents.py, AgentRegisterResponse]
- "routers_agents_submit_job_result": "submit_job_result()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1280 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_ai_report_approve_report": "approve_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L136 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_get_draft": "get_draft()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L119 | neighbors=[ai_report.py, _output_out()]
- "routers_ai_report_output_out": "_output_out()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L228 | neighbors=[ai_report.py, get_draft()]
- "routers_ai_report_reject_report": "reject_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L158 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L420 | neighbors=[ai_report.py, _run_generation()]
- "routers_analytics_sev_str": "_sev_str()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L82 | neighbors=[analytics.py, _finding_views()]
- "routers_analytics_two_latest_completed_runs": "_two_latest_completed_runs()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L106 | neighbors=[analytics.py, posture()]
- "routers_attack_paths_explain_hop": "_explain_hop()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L245 | neighbors=[attack_paths.py, get_attack_path()]
- "routers_attack_paths_path_summary": "_path_summary()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L234 | neighbors=[attack_paths.py, list_attack_paths()]
- "routers_customer_access_assignagentbody": "AssignAgentBody" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L71 | neighbors=[customer_access.py, BaseModel]
- "routers_customer_access_clientusercreate": "ClientUserCreate" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L52 | neighbors=[customer_access.py, BaseModel]
- "routers_customer_access_clientuserpatch": "ClientUserPatch" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L57 | neighbors=[customer_access.py, BaseModel]
- "routers_customer_access_reject_scan_request": "reject_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L358 | neighbors=[customer_access.py, _get_scan_request()]
- "routers_customer_access_rejectbody": "RejectBody" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L89 | neighbors=[customer_access.py, BaseModel]
- "routers_customer_access_scanrequestout": "ScanRequestOut" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L75 | neighbors=[customer_access.py, BaseModel]
- "routers_detection_get_results": "get_results()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L128 | neighbors=[detection.py, _result_out()]
- "routers_detection_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L217 | neighbors=[detection.py, get_results()]
- "routers_detection_runs_latest_run_delta": "latest_run_delta()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L72 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_runs_list_detection_runs": "list_detection_runs()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L55 | neighbors=[detection_runs.py, _run_dict()]
- "routers_detection_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L322 | neighbors=[detection.py, _run_correlation()]
- "routers_engagements_bulk_import_assets": "bulk_import_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L553 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_create_engagement": "create_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L352 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_engagements_update_engagement": "update_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L519 | neighbors=[engagements.py, _refresh_overview_cache()]
- "routers_exploits_approve_exploit": "approve_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L244 | neighbors=[exploits.py, _get_approval_or_404()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-101.json

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
