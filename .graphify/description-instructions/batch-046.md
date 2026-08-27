# Node Description Batch 47 of 236

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

- "scripts_seed_admin_main": "main()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L331 | neighbors=[seed_admin.py, log_error(), log_info(), _seed_with_retry(), _validate_env()]
- "services_agent_policy_evaluate_action": "evaluate_action()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L86 | neighbors=[agent_policy.py, classify_action(), Decision, _deny(), Decide whether `action` may proceed und…]
- "services_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, compute_exposure(), _sev(), Exposure analytics — protocol risk + zo…, 2885afa Add comprehensive probe testing…]
- "services_job_attempt_service": "job_attempt_service.py" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, config.py, AttemptClaim, claim_job_attempt(), renew_job_attempt()]
- "services_llm_managerllmservice_ensure_installed_ollama_model": "._ensure_installed_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L373 | neighbors=[ManagerLlmService, AiRuntimeError, ._client(), .generate(), .generate_with_fallback()]
- "services_posture_build_posture": "build_posture()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L159 | neighbors=[posture.py, compare(), compute_scores(), _to_utc(), Full dashboard/report payload. Degrades…]
- "services_posture_compare": "compare()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L120 | neighbors=[posture.py, build_posture(), _present_in_run(), _severity(), Bucket findings across the previous→lat…]
- "services_remediation_kb_classify_finding": "classify_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L79 | neighbors=[remediation_kb.py, _cves(), _text(), Map a finding to a KB category key usin…, recipe_for_finding()]
- "services_scope_targets": "scope_targets.py" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _expand_requested(), _parse_networks(), validate_targets_in_scope(), scope_targets.py — the single source of…]
- "services_sla_slaresult": "SlaResult" | kind=code-symbol | source=manager/backend/app/services/sla.py:L46 | neighbors=[sla.py, compute(), .is_tracked(), FindingStatus, Finding]
- "services_validation_ingest": "validation_ingest.py" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's s…]
- "tests_test_active_validation_interpret": "test_active_validation_interpret.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L1 | neighbors=[7bd104a feat(active-validation): pure r…, test_confirmed_upgrades_and_sets_exploi…, test_contradicted_marks_false_positive(), test_inconclusive_keeps_state_unchanged…, test_missing_or_garbage_result_is_incon…]
- "tests_test_ad_assessment_enum_with_entries": "_enum_with_entries()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L45 | neighbors=[test_ad_assessment.py, .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_adaptive_rate_testudpretransmit": "TestUdpRetransmit" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L119 | neighbors=[test_adaptive_rate.py, .test_retries_exhaust_on_silence(), .test_retry_recovers_dropped_reply(), .test_returns_immediately_on_closed(), .test_returns_immediately_on_reply()]
- "tests_test_agent_dispatch_testusecasecatalogparity": "TestUseCaseCatalogParity" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L35 | neighbors=[test_agent_dispatch.py, .test_manager_and_probe_route_use_cases…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_read_tools_test_list_assets_batches_services_no_n_plus_one": "test_list_assets_batches_services_no_n_plus_one()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L59 | neighbors=[test_agent_read_tools.py, _asset(), _FakeSession, _Result, _svc()]
- "tests_test_agent_read_tools_test_list_assets_caps_services_at_30": "test_list_assets_caps_services_at_30()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L79 | neighbors=[test_agent_read_tools.py, _asset(), _FakeSession, _Result, _svc()]
- "tests_test_agents_testpromoteassets_test_dedupes_duplicate_services_in_same_probe_result": ".test_dedupes_duplicate_services_in_same_probe_result()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L729 | neighbors=[A single web scan can emit multiple fac…, TestPromoteAssets, A single web scan can emit multiple fac…, A single web scan can emit multiple fac…, A single web scan can emit multiple fac…]
- "tests_test_agents_testregisteragent": "TestRegisterAgent" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L645 | neighbors=[test_agents.py, .test_agent_token_is_long_lived(), .test_creates_when_none_exists(), .test_reuses_existing_probe_by_name(), ScanJobType]
- "tests_test_ai_engine_resp": "_resp()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L165 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard()]
- "tests_test_ai_engine_testllmreportgenerator_test_technical_finding_runs_guard": ".test_technical_finding_runs_guard()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L205 | neighbors=[TestLLMReportGenerator, _asset(), _finding(), _mock_db(), _resp()]
- "tests_test_ai_normalizer_testainormalizercache": "TestAINormalizerCache" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L123 | neighbors=[test_ai_normalizer.py, .test_cache_persists_across_instances(), .test_get_returns_none_on_miss(), .test_key_is_content_hash_not_plaintext…, .test_put_and_get_roundtrip()]
- "tests_test_attack_path_correlation_ids": "_ids()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L15 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_exposed_db_without_unauth_does_not…, test_no_relay_when_signing_required()]
- "tests_test_customer_access_pending_request": "_pending_request()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L142 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_reject_records_reason()]
- "tests_test_customer_access_testapprovescanrequest_test_approve_dispatches_job_and_links_it": ".test_approve_dispatches_job_and_links_it()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L151 | neighbors=[TestApproveScanRequest, _added(), _mock_db(), _operator(), _pending_request()]
- "tests_test_detection_core_testenrichfinding_test_enriches_cvss_from_vuln_db": ".test_enriches_cvss_from_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L787 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_epss": ".test_enriches_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L809 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_kev": ".test_enriches_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L801 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_idempotent": ".test_idempotent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L825 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_no_data_still_sets_priority": ".test_no_data_still_sets_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L817 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_device_identity": "test_device_identity.py" | kind=code-symbol | source=probe/tests/test_device_identity.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, device_identity.py, test_device_identity_rejects_invalid_pr…, test_device_identity_round_trip_and_sig…, test_site_policy_signature_and_tofu_pin…]
- "tests_test_e2e_engagement_to_findings_manager": "_manager()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L51 | neighbors=[test_e2e_engagement_to_findings.py, Return (http_get, submit_result, captur…, test_engagement_dispatch_reaches_probe_…, test_out_of_scope_target_is_refused_end…, test_real_scan_of_open_datastore_yields…]
- "tests_test_e2e_engagement_to_findings_vulnerable_host_facts": "_vulnerable_host_facts()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L137 | neighbors=[test_e2e_engagement_to_findings.py, Exactly what the probe's smb/port scann…, test_correlated_findings_cite_their_bas…, test_manager_correlation_finds_all_thre…, test_ntlm_relay_is_high_when_smbv1_pres…]
- "tests_test_engagement_validation": "test_engagement_validation.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_create_normalizes_name_scopes_and_…, test_create_rejects_invalid_scope_entri…, test_create_rejects_reversed_date_range…, test_update_rejects_blank_name_invalid_…]
- "tests_test_finding_out_computed_base": "_base()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L11 | neighbors=[test_finding_out_computed.py, test_confirmed_exploited_outranks_contr…, test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_integrations_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L17 | neighbors=[test_integrations.py, .test_list_masks_secret(), .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-046.json

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
