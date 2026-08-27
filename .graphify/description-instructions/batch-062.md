# Node Description Batch 63 of 236

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

- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L308 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L419 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=probe/tests/test_probe_core.py:L227 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_probe_manifest_manifest": "_manifest()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L20 | neighbors=[test_probe_manifest.py, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_c…]
- "tests_test_probe_simple_approve_testnextprobename": "TestNextProbeName" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L20 | neighbors=[test_probe_simple_approve.py, .test_first_is_01(), .test_ignores_non_matching_and_non_nume…, .test_increments_past_highest_with_gaps…]
- "tests_test_reaper": "test_reaper.py" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _objects(), test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_remediation_generator_testgenerateremediationplan": "TestGenerateRemediationPlan" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L116 | neighbors=[test_remediation_generator.py, ._gen(), .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testnormalizeaiplan_raw": "._raw()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L69 | neighbors=[TestNormalizeAiPlan, .test_drops_unsafe_command_and_flags_st…, .test_emits_kb_schema_with_source_ai(), .test_keeps_safe_command_without_flag()]
- "tests_test_remediation_routes_db_scalar": "_db_scalar()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L35 | neighbors=[test_remediation_routes.py, .test_cached_ai_on_hit(), .test_cross_tenant_is_404(), .test_kb_on_cache_miss()]
- "tests_test_remediation_routes_one_result": "_one_result()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L52 | neighbors=[test_remediation_routes.py, A result whose .one() yields the RETURN…, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…]
- "tests_test_remediation_routes_testgenerateremediation_test_cross_tenant_is_404": ".test_cross_tenant_is_404()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L172 | neighbors=[TestGenerateRemediation, _FakeDB, _operator(), _scalar_result()]
- "tests_test_remediation_routes_testgetremediation": "TestGetRemediation" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L109 | neighbors=[test_remediation_routes.py, .test_cached_ai_on_hit(), .test_cross_tenant_is_404(), .test_kb_on_cache_miss()]
- "tests_test_remediation_routes_testgetremediation_test_cached_ai_on_hit": ".test_cached_ai_on_hit()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L118 | neighbors=[TestGetRemediation, _db_scalar(), _finding(), _operator()]
- "tests_test_remediation_routes_testgetremediation_test_kb_on_cache_miss": ".test_kb_on_cache_miss()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L110 | neighbors=[TestGetRemediation, _db_scalar(), _finding(), _operator()]
- "tests_test_remediation_routes_testupsertstatement_sql": "._sql()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L184 | neighbors=[TestUpsertStatement, .test_refreshes_generated_at_on_conflic…, .test_regeneration_resets_review_gate_n…, .test_targets_the_unique_constraint()]
- "tests_test_resolution_apply_db_returning": "_db_returning()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L26 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_apply_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L16 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_coverage": "test_resolution_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L1 | neighbors=[9a36729 feat(resolution): coverage buil…, test_coverage_counts_only_completed_sca…, test_coverage_empty_when_no_scanner_run…, test_host_of_strips_single_port()]
- "tests_test_resolve": "test_resolve.py" | kind=code-symbol | source=probe/tests/test_resolve.py:L1 | neighbors=[dec1e7c fix(scanner): resolve() family …, _infos(), TestResolveFamily, test_resolve.py — resolve() address-fam…]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L22 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L34 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L60 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L190 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_health_summary": "_summary()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L13 | neighbors=[test_scan_health.py, test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scope_targets_testexclusions": "TestExclusions" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L70 | neighbors=[test_scope_targets.py, .test_target_clear_of_exclusions_is_all…, .test_target_inside_an_exclusion_is_rej…, .test_target_overlapping_an_exclusion_i…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_sla_policy_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L32 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_custom_when_row_present": ".test_get_custom_when_row_present()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L58 | neighbors=[TestSlaPolicyRoutes, _db(), _operator(), _row()]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311(), test_signing_supported_field_present()]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L138 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]
- "tests_test_syn_scanner_testchecksum": "TestChecksum" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L27 | neighbors=[test_syn_scanner.py, .test_checksum_handles_odd_length(), .test_checksum_of_valid_ip_header_is_ze…, .test_tcp_checksum_verifies_to_zero()]
- "tests_test_syn_scanner_testclassify": "TestClassify" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L94 | neighbors=[test_syn_scanner.py, .test_other_flags_are_none(), .test_rst_is_closed(), .test_syn_ack_is_open()]
- "tests_test_syn_scanner_testsynretransmit_patch": "._patch()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L209 | neighbors=[TestSynRetransmit, .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…]
- "tests_test_syn_scanner_testsynscannerfallback": "TestSynScannerFallback" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L157 | neighbors=[test_syn_scanner.py, .test_fallback_detects_open_port_on_loo…, .test_fallback_labels_scanner_name(), .test_forced_fallback_builds_connect_sc…]
- "tests_test_syn_scanner_testverifyreplycookie_make_synack_reply": "._make_synack_reply()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L110 | neighbors=[TestVerifyReplyCookie, .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]

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
