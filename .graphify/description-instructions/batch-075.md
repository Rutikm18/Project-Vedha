# Node Description Batch 76 of 336

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

- "reports_page_findingcard": "FindingCard()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L242 | neighbors=[page.tsx, cvssColor(), fmtDate(), parseCvss()]
- "reports_page_fmtdate": "fmtDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L63 | neighbors=[page.tsx, FindingCard(), PortalReports(), ReportsPage()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[activity.py, Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_token_from_websocket": "_agent_token_from_websocket()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L40 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Read an agent bearer token exclusively …, Read an agent bearer token exclusively …]
- "routers_agent_ws_claim_pushed_job": "_claim_pushed_job()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L46 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Validate eligibility and atomically cla…, Validate eligibility and atomically cla…]
- "routers_agents_cancel_agent_job": "cancel_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1169 | neighbors=[agents.py, _pending_job_count(), Operator-initiated stop for a queued or…, Operator-initiated stop for a queued or…]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L952 | neighbors=[agents.py, _agent_can_execute_job(), _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_ai_report_run_regeneration": "_run_regeneration()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L381 | neighbors=[ai_report.py, Background task: regenerate rejected se…, _build_engagement_summary(), Background task: regenerate rejected se…]
- "routers_analytics_finding_views": "_finding_views()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L86 | neighbors=[analytics.py, _sev_str(), posture(), Map joined (Finding, Asset.criticality)…]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L191 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L225 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L153 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L181 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_customer_access_existing_client_user": "_existing_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L157 | neighbors=[customer_access.py, get_client_user(), patch_client_user(), provision_client_user()]
- "routers_customer_access_patch_client_user": "patch_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L242 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password()]
- "routers_customer_access_reveal_customer_password": "reveal_customer_password()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L425 | neighbors=[customer_access.py, Decrypt and return a customer login's s…, RevealOut, Decrypt and return a customer login's s…]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L421 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_integrations_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L43 | neighbors=[integrations.py, list_integrations(), IntegrationOut, put_integration()]
- "routers_portal_metric_finding": "_metric_finding()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L183 | neighbors=[portal.py, _enum_val(), portal_summary(), portal_trends()]
- "routers_portal_portal_finding_remediation": "portal_finding_remediation()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L135 | neighbors=[portal.py, Customer-facing structured remediation,…, Customer-facing structured remediation,…, Customer-facing structured remediation,…]
- "routers_portal_portal_use_cases": "_portal_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L75 | neighbors=[portal.py, create_scan_request(), The operator use-case catalog (single s…, The operator use-case catalog (single s…]
- "routers_portal_posture_view": "_posture_view()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L190 | neighbors=[portal.py, portal_posture(), portal_summary(), _enum_val()]
- "routers_probe_enrollment_authenticated_request": "_authenticated_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L477 | neighbors=[probe_enrollment.py, activate_enrollment(), _secret_hash(), poll_enrollment()]
- "routers_probe_enrollment_auto_enroll_cidrs": "auto_enroll_cidrs()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L313 | neighbors=[probe_enrollment.py, approve_request_simple(), _get_or_create_auto_enroll_site(), Parse settings.probe_auto_enroll_cidrs …]
- "routers_probe_enrollment_decode_public_key": "_decode_public_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L78 | neighbors=[probe_enrollment.py, create_enrollment_request(), .validate_key(), _verify_signature()]
- "routers_probe_enrollment_get_or_create_auto_enroll_site": "_get_or_create_auto_enroll_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L321 | neighbors=[probe_enrollment.py, create_enrollment_request(), auto_enroll_cidrs(), The singleton per-tenant Site that trus…]
- "routers_probe_enrollment_refresh_device_token": "refresh_device_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L724 | neighbors=[probe_enrollment.py, _rate_limit(), _secret_hash(), _verify_signature()]
- "routers_probe_enrollment_sitepolicyinput": "SitePolicyInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L148 | neighbors=[probe_enrollment.py, BaseModel, .require_site_reference(), .validate_networks()]
- "routers_probe_enrollment_verify_signature": "_verify_signature()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L88 | neighbors=[probe_enrollment.py, activate_enrollment(), refresh_device_token(), _decode_public_key()]
- "routers_remediation_build_upsert_stmt": "_build_upsert_stmt()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L64 | neighbors=[remediation.py, Build the atomic INSERT … ON CONFLICT D…, _upsert_plan(), Build the atomic INSERT … ON CONFLICT D…]
- "routers_remediation_get_remediation": "get_remediation()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L122 | neighbors=[remediation.py, _cached_plan(), _serialize(), _tenant_finding()]
- "routers_sla_policy_resolve_windows": "resolve_windows()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L58 | neighbors=[sla_policy.py, The tenant's custom SLA windows if set,…, _row(), _windows_of()]
- "routers_sla_policy_row": "_row()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L47 | neighbors=[sla_policy.py, get_sla_policy(), put_sla_policy(), resolve_windows()]
- "routers_users_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L42 | neighbors=[users.py, get_user(), list_users(), UserOut]
- "routers_validation_request_out": "_request_out()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L128 | neighbors=[validation.py, create_validation_request(), list_validation_requests(), ValidationRequestOut]
- "routers_validation_roe_allows_active_validation": "_roe_allows_active_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L81 | neighbors=[validation.py, approve_validation(), create_validation_request(), RoE gate: active validation is allowed …]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L525 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_accuracy_gate_load_corpus": "load_corpus()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L65 | neighbors=[accuracy_gate.py, load_corpora(), CorpusError, Load and structurally validate one corp…]
- "scanner_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "scanner_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L123 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…, Best-effort service name from data dict…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-075.json

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
