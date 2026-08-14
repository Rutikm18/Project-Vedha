# Node Description Batch 31 of 186

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

- "services_scope_crypto": "scope_crypto.py" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt…, 2885afa Add comprehensive probe testing…]
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L106 | neighbors=[DashboardGrid.tsx, page.tsx, page.tsx, page.tsx, DataState.tsx, page.tsx]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L50 | neighbors=[ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, DataState.tsx]
- "tests_engagement_adapters_test": "engagement-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/engagement-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, adapters.ts, toApiEngagementCreate(), toApiEngagementPatch(), toApiFindingPatch(), toUiFinding()]
- "tests_test_agent_dispatch_testagentwebsocketauthentication": "TestAgentWebSocketAuthentication" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L16 | neighbors=[test_agent_dispatch.py, .test_accepts_bearer_header(), .test_rejects_query_string_credentials(), ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_dispatch_testjobsecretboundary": "TestJobSecretBoundary" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L67 | neighbors=[test_agent_dispatch.py, .test_allows_non_secret_scan_tuning(), .test_detects_persisted_secret_material…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agents_testgetagentjobs": "TestGetAgentJobs" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L290 | neighbors=[test_agents.py, .test_404_when_agent_unknown(), .test_jobs_include_params(), .test_skips_job_outside_declared_networ…, .test_skips_job_when_capability_is_miss…, ScanJobType]
- "tests_test_agents_testotprofilegate": "TestOTProfileGate" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L162 | neighbors=[test_agents.py, .test_allows_passive_discovery_on_ot_en…, .test_blocks_active_scan_type_on_ot_eng…, .test_blocks_explicit_active_scan_type_…, .test_it_and_iot_profiles_unaffected(), ScanJobType]
- "tests_test_ai_engine_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L36 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher(), .test_predict_priority_uses_fallback_wh…]
- "tests_test_ai_engine_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L170 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_ai_engine_rationale_1": "Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API" | kind=entity | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_exploit_engine_testmetasploitrpcclient_make_client": "._make_client()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L183 | neighbors=[TestMetasploitRPCClient, .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit(), .test_run_module_error_raises(), .test_run_module_returns_job_id()]
- "tests_test_host_discovery_mobile_testdevicehint": "TestDeviceHint" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L52 | neighbors=[test_host_discovery_mobile.py, .test_iphone_lockdownd_port(), .test_mobile_vendor(), .test_no_signal(), .test_plain_vendor_passthrough(), .test_randomized_mac_is_mobile()]
- "tests_test_hw_bind": "test_hw_bind.py" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, hw_bind.py, TestCheckHwBind, TestGetHwId, Tests for agent/hw_bind.py, 2885afa Add comprehensive probe testing…]
- "tests_test_integration_testscopevalidationpipeline": "TestScopeValidationPipeline" | kind=code-symbol | source=probe/tests/test_integration.py:L165 | neighbors=[test_integration.py, Phase 1: combined scope validation (val…, .test_accepts_in_scope_rejects_out_of_s…, .test_all_excluded_returns_empty(), .test_excludes_override_scope(), .test_merge_exclusions_deduplicates()]
- "tests_test_integration_testwebsocketmessageprotocol": "TestWebSocketMessageProtocol" | kind=code-symbol | source=probe/tests/test_integration.py:L273 | neighbors=[test_integration.py, Phase 2: WebSocket message parsing., .test_heartbeat_message(), .test_hello_message(), .test_job_push_message(), .test_result_message()]
- "tests_test_loaders_testloadepsserrors": "TestLoadEpssErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L150 | neighbors=[test_loaders.py, .setup_method(), .test_epss_get_returns_none_for_unknown…, .test_malformed_epss_json_raises(), .test_missing_epss_file_raises(), .test_valid_epss_loads()]
- "tests_test_main_scripts_device": "test_main_scripts_device.py" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, device_classifier.py, scanner_base.py, TestClassifyDevice, TestClassifyFromResults, test_main_scripts_device.py — device-ro…]
- "tests_test_main_scripts_vantage": "test_main_scripts_vantage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, vantage_matrix.py, _r(), TestReconcileVantages, test_main_scripts_vantage.py — multi-va…]
- "tests_test_nessus_scanner_mock_response": "_mock_response()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L25 | neighbors=[test_nessus_scanner.py, test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()]
- "tests_test_new_scanners_teststablehostid": "TestStableHostId" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L328 | neighbors=[test_new_scanners.py, .test_hostname_second_priority(), .test_ip_fallback(), .test_mac_normalises_dashes(), .test_mac_takes_priority(), .test_zero_mac_skipped()]
- "tests_test_passive_collector_writer": "_Writer" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L15 | neighbors=[test_passive_collector.py, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…, test_subset_listener_failure_reports_de…, .__init__(), .write()]
- "tests_test_pipeline_testrunpipelineaiassist_test_ab_evaluate_no_precision_regression_without_ai_gain": ".test_ab_evaluate_no_precision_regression_without_ai_gain()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L303 | neighbors=[When FakeAIClient returns nothing new, …, TestRunPipelineAiAssist, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelineaiassist_test_ab_evaluate_returns_expected_keys": ".test_ab_evaluate_returns_expected_keys()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L291 | neighbors=[ab_evaluate must return a dict with the…, TestRunPipelineAiAssist, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelineaiassist_test_ai_assist_off_by_default": ".test_ai_assist_off_by_default()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L280 | neighbors=[With use_ai_assist=False (the default) …, TestRunPipelineAiAssist, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinededup_test_findings_deduped_within_same_host": ".test_findings_deduped_within_same_host()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L246 | neighbors=[The same (asset, CVE) can't appear twic…, TestRunPipelineDedup, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinededup_test_two_identical_hosts_each_get_their_own_finding": ".test_two_identical_hosts_each_get_their_own_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L233 | neighbors=[Different IPs must produce independent …, TestRunPipelineDedup, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelineemptyinput_test_empty_jsonl_returns_no_findings": ".test_empty_jsonl_returns_no_findings()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L113 | neighbors=[A completely empty file must not produc…, TestRunPipelineEmptyInput, _empty_epss(), _empty_jsonl(), _empty_kev(), _mock_vuln_db()]
- "tests_test_pipeline_testrunpipelineexposure_test_no_exposure_fields_are_none": ".test_no_exposure_fields_are_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L216 | neighbors=[Without an exposure dict the fields sta…, TestRunPipelineExposure, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinevulnmatching": "TestRunPipelineVulnMatching" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L138 | neighbors=[test_pipeline.py, .test_banner_finding_is_suspected_not_c…, .test_injected_dbs_used_no_file_io(), .test_no_finding_for_patched_version(), .test_ssh_inventory_finding_is_confirme…, .test_ssh_inventory_vulnerable_package_…]
- "tests_test_pipeline_testrunpipelinevulnmatching_test_banner_finding_is_suspected_not_confirmed": ".test_banner_finding_is_suspected_not_confirmed()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L163 | neighbors=[A banner-derived (inferred) source matc…, TestRunPipelineVulnMatching, _banner_jsonl(), _empty_epss(), _empty_kev(), _openssh_vuln_db()]
- "tests_test_pipeline_testrunpipelinevulnmatching_test_injected_dbs_used_no_file_io": ".test_injected_dbs_used_no_file_io()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L187 | neighbors=[When all three dbs are injected, the pi…, TestRunPipelineVulnMatching, _empty_epss(), _empty_kev(), _mock_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinevulnmatching_test_no_finding_for_patched_version": ".test_no_finding_for_patched_version()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L176 | neighbors=[A host running the fixed version must n…, TestRunPipelineVulnMatching, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinevulnmatching_test_ssh_inventory_finding_is_confirmed": ".test_ssh_inventory_finding_is_confirmed()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L150 | neighbors=[Findings from an authoritative (credent…, TestRunPipelineVulnMatching, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinevulnmatching_test_ssh_inventory_vulnerable_package_produces_finding": ".test_ssh_inventory_vulnerable_package_produces_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L139 | neighbors=[A credentialed package at a version ins…, TestRunPipelineVulnMatching, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_probe_core_testclamp": "TestClamp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L830 | neighbors=[test_probe_core.py, .test_bad_value_uses_default(), .test_clamped_high(), .test_clamped_low(), .test_in_range(), .test_none_uses_default()]
- "tests_test_probe_core_testengagementmodes": "TestEngagementModes" | kind=code-symbol | source=probe/tests/test_probe_core.py:L444 | neighbors=[test_probe_core.py, .test_assessment(), .test_re_scan(), .test_service_specific_invalid_raises(), .test_service_specific_valid(), .test_triage()]
- "tests_test_resolution_apply": "test_resolution_apply.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L1 | neighbors=[bd409f5 feat(resolution): async applier…, _db_returning(), _finding(), test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_decision": "test_resolution_decision.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L1 | neighbors=[cbf5d6c feat(resolution): pure decision…, test_db_change_blocks_resolution(), test_high_needs_two_covered_clean_runs(), test_medium_resolves_on_first_covered_c…, test_not_covered_is_skipped_and_counter…, test_threshold_is_stricter_for_critical…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-030.json

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
