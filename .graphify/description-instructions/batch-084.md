# Node Description Batch 85 of 336

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

- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L308 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L419 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=probe/tests/test_probe_core.py:L227 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_probe_manifest_manifest": "_manifest()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L20 | neighbors=[test_probe_manifest.py, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_c…]
- "tests_test_project_time_testoverrideandfallback": "TestOverrideAndFallback" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L68 | neighbors=[test_project_time.py, .test_bad_zone_does_not_crash_the_api(), .test_ist_survives_missing_tzdata(), .test_vedha_tz_override()]
- "tests_test_project_time_testtoprojecttz": "TestToProjectTz" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L44 | neighbors=[test_project_time.py, .test_aware_input_keeps_its_instant(), .test_naive_is_assumed_utc(), .test_none_passes_through()]
- "tests_test_project_timezone_testoverrideandfallback": "TestOverrideAndFallback" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L78 | neighbors=[test_project_timezone.py, .test_ist_survives_a_missing_tzdata(), .test_unknown_zone_falls_back_without_c…, .test_vedha_tz_overrides_the_default()]
- "tests_test_raw_facts_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L17 | neighbors=[test_raw_facts.py, test_raw_facts_bounds_and_no_results(), test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner()]
- "tests_test_raw_facts_test_raw_facts_filter_by_scanner": "test_raw_facts_filter_by_scanner()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L54 | neighbors=[test_raw_facts.py, _scalars(), _sr(), _user()]
- "tests_test_raw_facts_test_raw_facts_grouped_by_scanner": "test_raw_facts_grouped_by_scanner()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L29 | neighbors=[test_raw_facts.py, _scalars(), _sr(), _user()]
- "tests_test_raw_facts_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L13 | neighbors=[test_raw_facts.py, test_raw_facts_bounds_and_no_results(), test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner()]
- "tests_test_reaper": "test_reaper.py" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _objects(), test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_reference_teststamping": "TestStamping" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L99 | neighbors=[test_reference.py, .test_an_explicit_reference_is_never_ov…, .test_every_insert_gets_one(), .test_the_reference_matches_the_row_id()]
- "tests_test_remediation_generator_testgenerateremediationplan": "TestGenerateRemediationPlan" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L116 | neighbors=[test_remediation_generator.py, ._gen(), .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testnormalizeaiplan_raw": "._raw()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L69 | neighbors=[TestNormalizeAiPlan, .test_drops_unsafe_command_and_flags_st…, .test_emits_kb_schema_with_source_ai(), .test_keeps_safe_command_without_flag()]
- "tests_test_remediation_routes_db_scalar": "_db_scalar()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L36 | neighbors=[test_remediation_routes.py, .test_cached_ai_on_hit(), .test_cross_tenant_is_404(), .test_kb_on_cache_miss()]
- "tests_test_remediation_routes_testgenerateremediation_test_cross_tenant_is_404": ".test_cross_tenant_is_404()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L179 | neighbors=[TestGenerateRemediation, _FakeDB, _operator(), _scalar_result()]
- "tests_test_remediation_routes_testgetremediation": "TestGetRemediation" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L110 | neighbors=[test_remediation_routes.py, .test_cached_ai_on_hit(), .test_cross_tenant_is_404(), .test_kb_on_cache_miss()]
- "tests_test_remediation_routes_testgetremediation_test_cached_ai_on_hit": ".test_cached_ai_on_hit()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L121 | neighbors=[TestGetRemediation, _db_scalar(), _finding(), _operator()]
- "tests_test_remediation_routes_testgetremediation_test_kb_on_cache_miss": ".test_kb_on_cache_miss()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L111 | neighbors=[TestGetRemediation, _db_scalar(), _finding(), _operator()]
- "tests_test_remediation_routes_testupsertstatement_sql": "._sql()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L191 | neighbors=[TestUpsertStatement, .test_refreshes_generated_at_on_conflic…, .test_regeneration_resets_review_gate_n…, .test_targets_the_unique_constraint()]
- "tests_test_resolution_apply_db_returning": "_db_returning()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L27 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_apply_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L16 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolve": "test_resolve.py" | kind=code-symbol | source=probe/tests/test_resolve.py:L1 | neighbors=[dec1e7c fix(scanner): resolve() family …, _infos(), TestResolveFamily, test_resolve.py — resolve() address-fam…]
- "tests_test_result_archive_testarchiveidentity_test_archived_json_equals_the_submitted_payload": ".test_archived_json_equals_the_submitted_payload()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L67 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_failure_envelopes_are_archived_too": ".test_failure_envelopes_are_archived_too()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L98 | neighbors=[A rejected job is exactly the case an o…, TestArchiveIdentity, _job(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_filename_is_result_plus_timestamp": ".test_filename_is_result_plus_timestamp()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L83 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_no_partial_files_are_left_behind": ".test_no_partial_files_are_left_behind()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L120 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_two_jobs_in_the_same_second_do_not_clobber": ".test_two_jobs_in_the_same_second_do_not_clobber()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L112 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveisbesteffort": "TestArchiveIsBestEffort" | kind=code-symbol | source=probe/tests/test_result_archive.py:L128 | neighbors=[test_result_archive.py, .test_default_location_is_the_probe_roo…, .test_empty_env_var_disables_archiving(), .test_unwritable_directory_does_not_fai…]
- "tests_test_result_archive_testarchiveisbesteffort_test_empty_env_var_disables_archiving": ".test_empty_env_var_disables_archiving()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L143 | neighbors=[TestArchiveIsBestEffort, _job(), _ok_result(), _runner()]
- "tests_test_risk_port_coverage_risk_ports": "_risk_ports()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L44 | neighbors=[test_risk_port_coverage.py, _port_intel(), test_network_va_scans_every_port_the_ri…, test_va_risk_ports_are_all_actually_in_…]
- "tests_test_risk_port_coverage_test_every_backdoor_port_is_swept": "test_every_backdoor_port_is_swept()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L71 | neighbors=[test_risk_port_coverage.py, Called out separately: these carry the …, _port_intel(), _swept_by_network_va()]
- "tests_test_router_signals_testpositivetls": "TestPositiveTls" | kind=code-symbol | source=probe/tests/test_router_signals.py:L24 | neighbors=[test_router_signals.py, .test_absence_heuristic_still_works(), .test_alert_record_service_routes(), .test_handshake_fact_routes_even_on_cli…]
- "tests_test_router_signals_teststructuredservice": "TestStructuredService" | kind=code-symbol | source=probe/tests/test_router_signals.py:L37 | neighbors=[test_router_signals.py, .test_db_by_service_field(), .test_http_by_service_field(), .test_ssh_by_service_field()]
- "tests_test_rsync_scanner_testparsemodules": "TestParseModules" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L18 | neighbors=[test_rsync_scanner.py, .test_bounded(), .test_protocol_lines_ignored(), .test_tab_and_space_separated()]
- "tests_test_rsync_scanner_testrsyncfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L100 | neighbors=[TestRsyncFindings, .test_anon_modules_high(), .test_auth_only_is_low_disclosure(), .test_no_modules_silent()]
- "tests_test_rsync_scanner_testrsyncscanner": "TestRsyncScanner" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L79 | neighbors=[test_rsync_scanner.py, ._sc(), .test_anon_modules_open(), .test_no_rsync_filtered()]
- "tests_test_runtime_requirements_coverage_declared": "_declared()" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L42 | neighbors=[test_runtime_requirements_coverage.py, Package names declared in a requirement…, test_runtime_image_installs_every_wired…, test_runtime_is_a_subset_of_the_develop…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-084.json

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
