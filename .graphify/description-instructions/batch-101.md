# Node Description Batch 102 of 330

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

- "models_validation_request": "validation_request.py" | kind=code-symbol | source=manager/backend/app/models/validation_request.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, ValidationRequest, validation_request.py — an approval-gat…]
- "models_validation_request_validationrequest": "ValidationRequest" | kind=code-symbol | source=manager/backend/app/models/validation_request.py:L28 | neighbors=[validation_request.py, Base, TimestampMixin]
- "models_worker_heartbeat": "worker_heartbeat.py" | kind=code-symbol | source=manager/backend/app/models/worker_heartbeat.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, WorkerHeartbeat, worker_heartbeat.py — one row per backg…]
- "models_worker_heartbeat_workerheartbeat": "WorkerHeartbeat" | kind=code-symbol | source=manager/backend/app/models/worker_heartbeat.py:L21 | neighbors=[worker_heartbeat.py, Base, TimestampMixin]
- "native_port_scan_nativeportscan": "nativePortScan()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L221 | neighbors=[tool-runners.ts, port-scan.ts, resolvePorts()]
- "portscan_classify_os_error": "classify_os_error()" | kind=code-symbol | source=portscan.py:L73 | neighbors=[portscan.py, ._attempt(), Map a connect()-time OSError to (state,…]
- "portscan_portscanner_run": ".run()" | kind=code-symbol | source=portscan.py:L195 | neighbors=[main(), PortScanner, .scan_port()]
- "prompts_report": "report.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, 298a9d4 trim frontend to 7 core pages; …]
- "prompts_triage": "triage.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/triage.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, 298a9d4 trim frontend to 7 core pages; …]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[AIClient, _Scanner, _Scanner]
- "reports_page_reportspage": "ReportsPage()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L812 | neighbors=[page.tsx, fmtDate(), formatDate()]
- "routers_ad_run_ad_assessment_and_save": "_run_ad_assessment_and_save()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L129 | neighbors=[ad.py, Background task: run the AD assessment …, _set_job_status()]
- "routers_agent_ws_rationale_1": "agent_ws.py — WebSocket endpoint for probe push connectivity.  Probes connect vi" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[agent_ws.py, Engagement, ScanJob]
- "routers_agent_ws_rationale_131": "Persistent WebSocket for probe → manager push communication.      Authentication" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L131 | neighbors=[Engagement, ScanJob, agent_websocket_endpoint()]
- "routers_agent_ws_rationale_42": "Read an agent bearer token exclusively from the non-logged auth header." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L42 | neighbors=[Engagement, ScanJob, _agent_token_from_websocket()]
- "routers_agent_ws_rationale_53": "Validate eligibility and atomically claim a WebSocket job offer." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L53 | neighbors=[Engagement, ScanJob, _claim_pushed_job()]
- "routers_agents_agentbootstraprequest": "AgentBootstrapRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L590 | neighbors=[agents.py, BaseModel, .validate_network_segments()]
- "routers_agents_cancel_agent_job": "cancel_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1135 | neighbors=[agents.py, _pending_job_count(), Operator-initiated stop for a queued or…]
- "routers_agents_refresh_agent_registration": "refresh_agent_registration()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L866 | neighbors=[agents.py, _agent_ownership_check(), _scope_is_reachable()]
- "routers_agents_resolve_scan_type": "_resolve_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L89 | neighbors=[agents.py, enqueue_agent_job(), _required_scan_type()]
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
- "routers_engagements_job_phase": "_job_phase()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L681 | neighbors=[engagements.py, campaign_progress(), Map a ScanJob status to the operator-fa…]
- "routers_engagements_overview_cache_key": "_overview_cache_key()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L62 | neighbors=[engagements.py, engagements_overview(), _refresh_overview_cache()]
- "routers_engagements_reconcile_status": "_reconcile_status()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L691 | neighbors=[engagements.py, campaign_progress(), Derive ONE authoritative campaign phase…]
- "routers_engagements_result_summary": "_result_summary()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L744 | neighbors=[engagements.py, campaign_progress(), A SAFE, bounded view of a job's raw res…]
- "routers_exploits_approval_out": "_approval_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L433 | neighbors=[exploits.py, ApprovalOut, list_approvals()]
- "routers_exploits_get_approval_or_404": "_get_approval_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L408 | neighbors=[exploits.py, approve_exploit(), reject_exploit()]

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
