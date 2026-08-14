# Node Description Batch 38 of 186

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

- "schemas_finding_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L55 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slaitem": "SlaItem" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L35 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slasummary": "SlaSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L45 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_log_warn": "log_warn()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L85 | neighbors=[seed_admin.py, _detect_drift(), _log(), _seed_with_retry(), _validate_env()]
- "scripts_seed_admin_main": "main()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L331 | neighbors=[seed_admin.py, log_error(), log_info(), _seed_with_retry(), _validate_env()]
- "services_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, compute_exposure(), _sev(), Exposure analytics — protocol risk + zo…, 2885afa Add comprehensive probe testing…]
- "services_job_attempt_service": "job_attempt_service.py" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, config.py, AttemptClaim, claim_job_attempt(), renew_job_attempt()]
- "services_job_result_service_validate_result_scope": "validate_result_scope()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L86 | neighbors=[job_result_service.py, process_job_result(), Return result identities outside the jo…, _identity_ip(), _result_network_identities()]
- "services_llm_managerllmservice_ensure_installed_ollama_model": "._ensure_installed_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L373 | neighbors=[ManagerLlmService, AiRuntimeError, ._client(), .generate(), .generate_with_fallback()]
- "services_posture_build_posture": "build_posture()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L159 | neighbors=[posture.py, compare(), compute_scores(), _to_utc(), Full dashboard/report payload. Degrades…]
- "services_posture_compare": "compare()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L120 | neighbors=[posture.py, build_posture(), _present_in_run(), _severity(), Bucket findings across the previous→lat…]
- "services_sla_compute": "compute()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L60 | neighbors=[sla.py, SlaResult, _windows(), Compute the SLA state for one finding. …, summarize()]
- "services_sla_slaresult": "SlaResult" | kind=code-symbol | source=manager/backend/app/services/sla.py:L46 | neighbors=[sla.py, compute(), .is_tracked(), FindingStatus, Finding]
- "services_validation_ingest": "validation_ingest.py" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's s…]
- "tests_test_active_validation_interpret": "test_active_validation_interpret.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L1 | neighbors=[7bd104a feat(active-validation): pure r…, test_confirmed_upgrades_and_sets_exploi…, test_contradicted_marks_false_positive(), test_inconclusive_keeps_state_unchanged…, test_missing_or_garbage_result_is_incon…]
- "tests_test_ad_assessment_enum_with_entries": "_enum_with_entries()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L45 | neighbors=[test_ad_assessment.py, .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_adaptive_rate_testudpretransmit": "TestUdpRetransmit" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L119 | neighbors=[test_adaptive_rate.py, .test_retries_exhaust_on_silence(), .test_retry_recovers_dropped_reply(), .test_returns_immediately_on_closed(), .test_returns_immediately_on_reply()]
- "tests_test_agent_dispatch_testusecasecatalogparity": "TestUseCaseCatalogParity" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L35 | neighbors=[test_agent_dispatch.py, .test_manager_and_probe_route_use_cases…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agents_testregisteragent": "TestRegisterAgent" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L637 | neighbors=[test_agents.py, .test_agent_token_is_long_lived(), .test_creates_when_none_exists(), .test_reuses_existing_probe_by_name(), ScanJobType]
- "tests_test_agents_testregisteragent_test_agent_token_is_long_lived": ".test_agent_token_is_long_lived()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L675 | neighbors=[Agent token must outlive the 15-min acc…, TestRegisterAgent, _user(), Agent token must outlive the 15-min acc…, Agent token must outlive the 15-min acc…]
- "tests_test_agents_testregisteragent_test_reuses_existing_probe_by_name": ".test_reuses_existing_probe_by_name()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L640 | neighbors=[Re-registering the same-named probe mus…, TestRegisterAgent, _user(), Re-registering the same-named probe mus…, Re-registering the same-named probe mus…]
- "tests_test_ai_engine_resp": "_resp()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L165 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard()]
- "tests_test_ai_engine_testllmreportgenerator_test_technical_finding_runs_guard": ".test_technical_finding_runs_guard()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L205 | neighbors=[TestLLMReportGenerator, _asset(), _finding(), _mock_db(), _resp()]
- "tests_test_ai_normalizer_testainormalizercache": "TestAINormalizerCache" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L123 | neighbors=[test_ai_normalizer.py, .test_cache_persists_across_instances(), .test_get_returns_none_on_miss(), .test_key_is_content_hash_not_plaintext…, .test_put_and_get_roundtrip()]
- "tests_test_detection_core_testenrichfinding_test_enriches_cvss_from_vuln_db": ".test_enriches_cvss_from_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L787 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_epss": ".test_enriches_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L809 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_kev": ".test_enriches_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L801 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_idempotent": ".test_idempotent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L825 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_no_data_still_sets_priority": ".test_no_data_still_sets_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L817 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_device_identity": "test_device_identity.py" | kind=code-symbol | source=probe/tests/test_device_identity.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, device_identity.py, test_device_identity_rejects_invalid_pr…, test_device_identity_round_trip_and_sig…, test_site_policy_signature_and_tofu_pin…]
- "tests_test_engagement_validation": "test_engagement_validation.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_create_normalizes_name_scopes_and_…, test_create_rejects_invalid_scope_entri…, test_create_rejects_reversed_date_range…, test_update_rejects_blank_name_invalid_…]
- "tests_test_finding_out_computed_base": "_base()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L11 | neighbors=[test_finding_out_computed.py, test_confirmed_exploited_outranks_contr…, test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_job_attempt_service": "test_job_attempt_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, test_claim_creates_immutable_attempt_wi…, test_current_fence_renews_attempt_and_l…, test_lost_claim_does_not_create_attempt…, test_stale_fence_cannot_renew_attempt()]
- "tests_test_loaders_testloadkeverrors": "TestLoadKevErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L124 | neighbors=[test_loaders.py, .setup_method(), .test_malformed_kev_json_raises(), .test_missing_kev_file_raises(), .test_valid_kev_loads()]
- "tests_test_main_scripts_correlation_get": "_get()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L21 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_legacy_windows_surface_smbv1_plus_…, test_ntlm_relay_is_high_when_smbv1_also…, test_ntlm_relay_is_medium_when_only_sig…]
- "tests_test_main_scripts_correlation_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L17 | neighbors=[test_main_scripts_correlation.py, test_correlation_does_not_cross_hosts(), test_no_legacy_surface_with_only_smbv1(), test_no_relay_finding_when_signing_requ…, test_single_cleartext_service_does_not_…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-037.json

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
