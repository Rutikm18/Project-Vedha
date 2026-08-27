# Node Description Batch 86 of 236

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

- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L535 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L560 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L544 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L593 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L552 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L489 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L893 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_probe_simple_approve_testsimpleapproveinput": "TestSimpleApproveInput" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L33 | neighbors=[test_probe_simple_approve.py, .test_defaults_are_all_optional(), .test_overrides_accepted()]
- "tests_test_reaper_objects": "_objects()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L8 | neighbors=[test_reaper.py, test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_remediation_generator_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L26 | neighbors=[test_remediation_generator.py, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_gen": "._gen()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L117 | neighbors=[TestGenerateRemediationPlan, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_test_unparseable_output_raises_value_error": ".test_unparseable_output_raises_value_error()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L122 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testgenerateremediationplan_test_valid_output_returns_ai_plan_with_model": ".test_valid_output_returns_ai_plan_with_model()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L127 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testsafecommands": "TestSafeCommands" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L55 | neighbors=[test_remediation_generator.py, .test_drops_destructive_keeps_safe(), .test_null_command_yields_nothing()]
- "tests_test_remediation_kb_testrecipeshape": "TestRecipeShape" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L43 | neighbors=[test_remediation_kb.py, .test_every_recipe_has_required_fields(), .test_every_recipe_step_has_all_os_keys…]
- "tests_test_remediation_routes_genai": "_GenAI" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L84 | neighbors=[test_remediation_routes.py, .generate_remediation_plan(), .__init__()]
- "tests_test_remediation_routes_returning_row": "_returning_row()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L59 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…]
- "tests_test_remediation_routes_testgetremediation_test_cross_tenant_is_404": ".test_cross_tenant_is_404()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L129 | neighbors=[TestGetRemediation, _db_scalar(), _operator()]
- "tests_test_remediation_upsert_integration_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L55 | neighbors=[test_remediation_upsert_integration.py, _stmt(), test_upsert_resets_gate_and_is_race_saf…]
- "tests_test_resolution_apply_test_covered_clean_medium_finding_is_auto_resolved": "test_covered_clean_medium_finding_is_auto_resolved()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L34 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_db_version_change_blocks_resolution": "test_db_version_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L63 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_uncovered_finding_is_left_open": "test_uncovered_finding_is_left_open()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L50 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_result_spool_spool": "spool()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L13 | neighbors=[test_result_spool.py, ResultSpool with tiny retry delay for f…, ResultSpool with tiny retry delay for f…]
- "tests_test_scan_funnel_recordingdeep": "RecordingDeep" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L47 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target()]
- "tests_test_scanner_parity_py_files": "_py_files()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L25 | neighbors=[test_scanner_parity.py, test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_…]
- "tests_test_scanner_parity_test_no_extra_scanner_files": "test_no_extra_scanner_files()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L38 | neighbors=[test_scanner_parity.py, scanner/ must not carry modules that ma…, _py_files()]
- "tests_test_scanner_parity_test_scanner_is_superset_of_no_missing_files": "test_scanner_is_superset_of_no_missing_files()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L29 | neighbors=[test_scanner_parity.py, Every scanner module authored in main_s…, _py_files()]
- "tests_test_scope_crypt_testkeygeneration": "TestKeyGeneration" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L15 | neighbors=[test_scope_crypt.py, .test_generates_32_byte_keys(), .test_generates_different_keys_each_cal…]
- "tests_test_scope_targets_testipversionsafety": "TestIpVersionSafety" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L88 | neighbors=[test_scope_targets.py, .test_v6_in_v6_scope(), .test_v6_target_against_v4_scope_is_rej…]
- "tests_test_seed_admin_testdriftdetection": "TestDriftDetection" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L308 | neighbors=[test_seed_admin.py, .test_warns_on_multiple_admins(), .test_warns_on_stale_admin_emails()]
- "tests_test_seed_admin_testpasswordrotation": "TestPasswordRotation" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L189 | neighbors=[test_seed_admin.py, .test_rotation_raises_on_hash_verify_fa…, .test_rotation_updates_hash_and_verifie…]
- "tests_test_service_match_testnomatch": "TestNoMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L87 | neighbors=[test_service_match.py, .test_empty_returns_none(), .test_unrecognized_returns_none()]
- "tests_test_service_match_testprobeladder": "TestProbeLadder" | kind=code-symbol | source=probe/tests/test_service_match.py:L95 | neighbors=[test_service_match.py, .test_ladder_has_http_and_generic(), .test_ladder_starts_with_null_probe()]
- "tests_test_sla_policy_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L16 | neighbors=[test_sla_policy.py, .test_custom_window_relaxes_state(), .test_default_window_breaches()]
- "tests_test_sla_policy_row": "_row()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L46 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_resolve_windows_fallback_and_cust…]
- "tests_test_sla_policy_testpolicyawarecompute": "TestPolicyAwareCompute" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L23 | neighbors=[test_sla_policy.py, .test_custom_window_relaxes_state(), .test_default_window_breaches()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_env_defaults_when_no_row": ".test_get_env_defaults_when_no_row()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L53 | neighbors=[TestSlaPolicyRoutes, _db(), _operator()]
- "tests_test_sla_policy_testslapolicyroutes_test_put_creates_when_absent": ".test_put_creates_when_absent()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L63 | neighbors=[TestSlaPolicyRoutes, _db(), _operator()]
- "tests_test_sla_policy_testslapolicyroutes_test_resolve_windows_fallback_and_custom": ".test_resolve_windows_fallback_and_custom()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L71 | neighbors=[TestSlaPolicyRoutes, _db(), _row()]
- "tests_test_smb_scanner_smb2_error_response": "_smb2_error_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L14 | neighbors=[test_smb_scanner.py, An SMB2 ERROR response (e.g. STATUS_INV…, test_error_response_not_parsed_as_signi…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-085.json

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
