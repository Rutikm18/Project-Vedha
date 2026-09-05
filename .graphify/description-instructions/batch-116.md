# Node Description Batch 117 of 336

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

- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L569 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L576 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L502 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L503 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L510 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L584 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L521 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L522 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L528 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L535 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L560 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L544 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L593 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L552 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L489 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L930 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_probe_simple_approve_testsimpleapproveinput": "TestSimpleApproveInput" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L38 | neighbors=[test_probe_simple_approve.py, .test_defaults_are_all_optional(), .test_overrides_accepted()]
- "tests_test_project_time_testfilestamp": "TestFileStamp" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L60 | neighbors=[test_project_time.py, .test_filename_safe(), .test_no_z_suffix_on_local_time()]
- "tests_test_raw_facts_sr": "_sr()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L21 | neighbors=[test_raw_facts.py, test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner()]
- "tests_test_raw_facts_test_raw_facts_bounds_and_no_results": "test_raw_facts_bounds_and_no_results()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L72 | neighbors=[test_raw_facts.py, _scalars(), _user()]
- "tests_test_reaper_objects": "_objects()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L8 | neighbors=[test_reaper.py, test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_reference_testshape_test_uses_the_rows_own_date_not_today": ".test_uses_the_rows_own_date_not_today()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L35 | neighbors=[A backfilled reference must match what …, TestShape, _at()]
- "tests_test_reference_teststability": "TestStability" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L86 | neighbors=[test_reference.py, .test_different_rows_get_different_refe…, .test_the_same_row_always_gets_the_same…]
- "tests_test_reference_teststability_test_the_same_row_always_gets_the_same_reference": ".test_the_same_row_always_gets_the_same_reference()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L87 | neighbors=[It is quoted in tickets — it must not m…, TestStability, _at()]
- "tests_test_reference_testtellingthemapart": "TestTellingThemApart" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L74 | neighbors=[test_reference.py, .test_a_reference_is_distinguishable_fr…, .test_an_unregistered_prefix_is_not_our…]
- "tests_test_remediation_generator_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L26 | neighbors=[test_remediation_generator.py, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_gen": "._gen()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L117 | neighbors=[TestGenerateRemediationPlan, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_test_unparseable_output_raises_value_error": ".test_unparseable_output_raises_value_error()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L122 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testgenerateremediationplan_test_valid_output_returns_ai_plan_with_model": ".test_valid_output_returns_ai_plan_with_model()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L127 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testsafecommands": "TestSafeCommands" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L55 | neighbors=[test_remediation_generator.py, .test_drops_destructive_keeps_safe(), .test_null_command_yields_nothing()]
- "tests_test_remediation_kb_testrecipeshape": "TestRecipeShape" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L43 | neighbors=[test_remediation_kb.py, .test_every_recipe_has_required_fields(), .test_every_recipe_step_has_all_os_keys…]
- "tests_test_remediation_routes_genai": "_GenAI" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L85 | neighbors=[test_remediation_routes.py, .generate_remediation_plan(), .__init__()]
- "tests_test_remediation_routes_returning_row": "_returning_row()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L60 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…]
- "tests_test_remediation_routes_testgetremediation_test_cross_tenant_is_404": ".test_cross_tenant_is_404()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L136 | neighbors=[TestGetRemediation, _db_scalar(), _operator()]
- "tests_test_remediation_upsert_integration_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L55 | neighbors=[test_remediation_upsert_integration.py, _stmt(), test_upsert_resets_gate_and_is_race_saf…]
- "tests_test_resolution_apply_test_covered_clean_medium_finding_is_auto_resolved": "test_covered_clean_medium_finding_is_auto_resolved()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L35 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_db_version_change_blocks_resolution": "test_db_version_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L64 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_uncovered_finding_is_left_open": "test_uncovered_finding_is_left_open()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L51 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_result_spool_spool": "spool()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L13 | neighbors=[test_result_spool.py, ResultSpool with tiny retry delay for f…, ResultSpool with tiny retry delay for f…]
- "tests_test_risk_port_coverage_port_intel": "_port_intel()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L35 | neighbors=[test_risk_port_coverage.py, _risk_ports(), test_every_backdoor_port_is_swept()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-116.json

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
