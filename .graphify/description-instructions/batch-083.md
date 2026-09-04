# Node Description Batch 84 of 332

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

- "tests_test_posture_fv": "_fv()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L12 | neighbors=[test_posture.py, test_build_posture_buckets_resolved_new…, test_build_posture_single_run_has_no_pr…, test_compute_scores_uses_risk_epss_expl…]
- "tests_test_posture_row": "_Row" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L109 | neighbors=[test_posture.py, .__init__(), test_finding_views_handles_null_asset_a…, test_finding_views_maps_columns_and_ass…]
- "tests_test_posture_rules_testinvariants": "TestInvariants" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L154 | neighbors=[test_posture_rules.py, .test_dedup_same_rule_same_port(), .test_detect_all_sorts_by_risk_desc(), .test_deterministic_id_across_runs()]
- "tests_test_posture_rules_testtrusttier": "TestTrustTier" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L30 | neighbors=[test_posture_rules.py, .test_registry_contains_user_validated_…, .test_unvalidated_scanner_only_suspects…, .test_validated_scanner_confirms()]
- "tests_test_posture_rules_testvulnerablehost_test_deprecated_tls_version_underscore_labels": ".test_deprecated_tls_version_underscore_labels()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L95 | neighbors=[The live tls_scanner labels its probe l…, TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_trace_testabsentversusclean_test_key_absent_is_missing_input_not_clean": ".test_key_absent_is_missing_input_not_clean()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L50 | neighbors=[TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testabsentversusclean_test_key_present_false_is_clean_no_match": ".test_key_present_false_is_clean_no_match()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L44 | neighbors=[TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testabsentversusclean_test_key_present_true_is_match": ".test_key_present_true_is_match()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L39 | neighbors=[TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testbehaviourpreserved": "TestBehaviourPreserved" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L110 | neighbors=[test_posture_trace.py, ._mixed(), .test_dedup_still_one_finding_per_rule_…, .test_detect_posture_matches_traced_fin…]
- "tests_test_posture_trace_testbehaviourpreserved_mixed": "._mixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L111 | neighbors=[TestBehaviourPreserved, _asset(), _fact(), .test_detect_posture_matches_traced_fin…]
- "tests_test_posture_trace_testnoevidence_test_scanner_absent_yields_no_evidence": ".test_scanner_absent_yields_no_evidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L78 | neighbors=[TestNoEvidence, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testruleisolation_test_raising_rule_is_error_and_others_still_fire": ".test_raising_rule_is_error_and_others_still_fire()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L96 | neighbors=[TestRuleIsolation, _asset(), _fact(), _outcome()]
- "tests_test_printer_scanner_testprinterscanner": "TestPrinterScanner" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L34 | neighbors=[test_printer_scanner.py, ._sc(), .test_no_printer_filtered(), .test_open()]
- "tests_test_printer_scanner_testpurelogic": "TestPureLogic" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L18 | neighbors=[test_printer_scanner.py, .test_build_ipp(), .test_parse_ipp_make_model(), .test_parse_pjl_id()]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L475 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-083.json

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
