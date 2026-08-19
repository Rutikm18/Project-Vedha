# Node Description Batch 55 of 227

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

- "routers_agent_ws_agent_token_from_websocket": "_agent_token_from_websocket()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L40 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Read an agent bearer token exclusively …, Read an agent bearer token exclusively …]
- "routers_agent_ws_claim_pushed_job": "_claim_pushed_job()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L46 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Validate eligibility and atomically cla…, Validate eligibility and atomically cla…]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L858 | neighbors=[agents.py, _agent_can_execute_job(), _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_agents_list_intensities": "list_intensities()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L559 | neighbors=[agents.py, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…]
- "routers_ai_report_run_regeneration": "_run_regeneration()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L381 | neighbors=[ai_report.py, Background task: regenerate rejected se…, _build_engagement_summary(), Background task: regenerate rejected se…]
- "routers_analytics_finding_views": "_finding_views()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L86 | neighbors=[analytics.py, _sev_str(), posture(), Map joined (Finding, Asset.criticality)…]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L191 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L225 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L153 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L181 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_customer_access_existing_client_user": "_existing_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L157 | neighbors=[customer_access.py, get_client_user(), patch_client_user(), provision_client_user()]
- "routers_customer_access_patch_client_user": "patch_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L242 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password()]
- "routers_customer_access_reveal_customer_password": "reveal_customer_password()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L425 | neighbors=[customer_access.py, Decrypt and return a customer login's s…, RevealOut, Decrypt and return a customer login's s…]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…, Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L421 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_integrations_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L43 | neighbors=[integrations.py, list_integrations(), IntegrationOut, put_integration()]
- "routers_portal_metric_finding": "_metric_finding()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L178 | neighbors=[portal.py, _enum_val(), portal_summary(), portal_trends()]
- "routers_portal_posture_view": "_posture_view()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L185 | neighbors=[portal.py, portal_posture(), portal_summary(), _enum_val()]
- "routers_probe_enrollment_authenticated_request": "_authenticated_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L477 | neighbors=[probe_enrollment.py, activate_enrollment(), _secret_hash(), poll_enrollment()]
- "routers_probe_enrollment_auto_enroll_cidrs": "auto_enroll_cidrs()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L313 | neighbors=[probe_enrollment.py, approve_request_simple(), _get_or_create_auto_enroll_site(), Parse settings.probe_auto_enroll_cidrs …]
- "routers_probe_enrollment_decode_public_key": "_decode_public_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L78 | neighbors=[probe_enrollment.py, create_enrollment_request(), .validate_key(), _verify_signature()]
- "routers_probe_enrollment_get_or_create_auto_enroll_site": "_get_or_create_auto_enroll_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L321 | neighbors=[probe_enrollment.py, create_enrollment_request(), auto_enroll_cidrs(), The singleton per-tenant Site that trus…]
- "routers_probe_enrollment_refresh_device_token": "refresh_device_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L720 | neighbors=[probe_enrollment.py, _rate_limit(), _secret_hash(), _verify_signature()]
- "routers_probe_enrollment_sitepolicyinput": "SitePolicyInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L148 | neighbors=[probe_enrollment.py, BaseModel, .require_site_reference(), .validate_networks()]
- "routers_probe_enrollment_verify_signature": "_verify_signature()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L88 | neighbors=[probe_enrollment.py, activate_enrollment(), refresh_device_token(), _decode_public_key()]
- "routers_remediation_get_remediation": "get_remediation()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L119 | neighbors=[remediation.py, _cached_plan(), _serialize(), _tenant_finding()]
- "routers_remediation_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L39 | neighbors=[remediation.py, generate_remediation(), get_remediation(), Fetch a finding scoped to the caller's …]
- "routers_remediation_upsert_plan": "_upsert_plan()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L92 | neighbors=[remediation.py, generate_remediation(), Execute the atomic upsert and return th…, _build_upsert_stmt()]
- "routers_sla_policy_resolve_windows": "resolve_windows()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L58 | neighbors=[sla_policy.py, The tenant's custom SLA windows if set,…, _row(), _windows_of()]
- "routers_sla_policy_row": "_row()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L47 | neighbors=[sla_policy.py, get_sla_policy(), put_sla_policy(), resolve_windows()]
- "routers_validation_request_out": "_request_out()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L128 | neighbors=[validation.py, create_validation_request(), list_validation_requests(), ValidationRequestOut]
- "routers_validation_roe_allows_active_validation": "_roe_allows_active_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L81 | neighbors=[validation.py, approve_validation(), create_validation_request(), RoE gate: active validation is allowed …]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L525 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "scanner_delta_scanner_delta": "Delta" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L69 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…]
- "scanner_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/scanner/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…]
- "scanner_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/scanner/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "scanner_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/scanner/findings.py:L552 | neighbors=[findings.py, _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-054.json

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
