# Node Description Batch 161 of 330

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

- "tests_test_probe_next_features_test_no_post_stage_for_ordinary_scan_types": "test_no_post_stage_for_ordinary_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L161 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_simple_approve_testnextprobename_test_first_is_01": ".test_first_is_01()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L21 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_probe_simple_approve_testnextprobename_test_ignores_non_matching_and_non_numeric": ".test_ignores_non_matching_and_non_numeric()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L33 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_probe_simple_approve_testnextprobename_test_increments_past_highest_with_gaps": ".test_increments_past_highest_with_gaps()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L24 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_probe_simple_approve_testnextprobename_test_legacy_probe_names_still_advance_the_counter": ".test_legacy_probe_names_still_advance_the_counter()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L28 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_project_time_test_websocket_no_longer_emits_naive_timestamps": "test_websocket_no_longer_emits_naive_timestamps()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L86 | neighbors=[test_project_time.py, Guards the actual bug: utcnow() strings…]
- "tests_test_project_time_testrendering_test_still_orders_against_utc_rows": ".test_still_orders_against_utc_rows()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L37 | neighbors=[The property that makes this safe next …, TestRendering]
- "tests_test_project_time_testtoprojecttz_test_naive_is_assumed_utc": ".test_naive_is_assumed_utc()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L45 | neighbors=[Every naive datetime in this codebase's…, TestToProjectTz]
- "tests_test_project_timezone_testfilestamps_test_file_stamp_has_no_z_suffix": ".test_file_stamp_has_no_z_suffix()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L50 | neighbors=[A `Z` on a local-time stamp is an outri…, TestFileStamps]
- "tests_test_project_timezone_testoverrideandfallback_test_ist_survives_a_missing_tzdata": ".test_ist_survives_a_missing_tzdata()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L92 | neighbors=[Sealed/slim images may ship no tzdata. …, TestOverrideAndFallback]
- "tests_test_project_timezone_testoverrideandfallback_test_unknown_zone_falls_back_without_crashing": ".test_unknown_zone_falls_back_without_crashing()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L85 | neighbors=[A bad VEDHA_TZ must never take a scan d…, TestOverrideAndFallback]
- "tests_test_project_timezone_testprojecttimezone_test_aware_timestamps_still_compare_against_utc": ".test_aware_timestamps_still_compare_against_utc()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L41 | neighbors=[The ordering guarantee that makes this …, TestProjectTimezone]
- "tests_test_project_timezone_testprojecttimezone_test_timestamp_is_the_same_instant_as_utc": ".test_timestamp_is_the_same_instant_as_utc()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L35 | neighbors=[Rendering moved; the instant did not., TestProjectTimezone]
- "tests_test_project_timezone_testscanresultusesprojecttime": "TestScanResultUsesProjectTime" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L70 | neighbors=[test_project_timezone.py, .test_scan_result_timestamp_is_ist()]
- "tests_test_project_timezone_testscanresultusesprojecttime_test_scan_result_timestamp_is_ist": ".test_scan_result_timestamp_is_ist()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L71 | neighbors=[The timestamp that ends up inside every…, TestScanResultUsesProjectTime]
- "tests_test_reaper_test_expired_attempt_fails_job_when_retry_budget_is_exhausted": "test_expired_attempt_fails_job_when_retry_budget_is_exhausted()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L39 | neighbors=[test_reaper.py, _objects()]
- "tests_test_reaper_test_expired_attempt_requeues_with_fence_history_preserved": "test_expired_attempt_requeues_with_fence_history_preserved()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L24 | neighbors=[test_reaper.py, _objects()]
- "tests_test_reference_test_the_migration_backfill_agrees_with_the_application": "test_the_migration_backfill_agrees_with_the_application()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L117 | neighbors=[test_reference.py, Migration 0036 backfills in SQL so it n…]
- "tests_test_reference_testshape_test_reads_as_prefix_date_code": ".test_reads_as_prefix_date_code()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L28 | neighbors=[TestShape, _at()]
- "tests_test_reference_testsurvivesbeingreadaloud_test_only_the_suffix_is_alias_folded": ".test_only_the_suffix_is_alias_folded()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L69 | neighbors=[The prefix and date are literal — foldi…, TestSurvivesBeingReadAloud]
- "tests_test_reference_testsurvivesbeingreadaloud_test_typed_back_lowercase_still_resolves": ".test_typed_back_lowercase_still_resolves()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L58 | neighbors=[TestSurvivesBeingReadAloud, _at()]
- "tests_test_reference_testtellingthemapart_test_a_reference_is_distinguishable_from_a_uuid": ".test_a_reference_is_distinguishable_from_a_uuid()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L75 | neighbors=[TestTellingThemApart, _at()]
- "tests_test_remediation_generator_testnormalizeaiplan_test_drops_unsafe_command_and_flags_step": ".test_drops_unsafe_command_and_flags_step()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L93 | neighbors=[TestNormalizeAiPlan, ._raw()]
- "tests_test_remediation_generator_testnormalizeaiplan_test_emits_kb_schema_with_source_ai": ".test_emits_kb_schema_with_source_ai()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L83 | neighbors=[TestNormalizeAiPlan, ._raw()]
- "tests_test_remediation_generator_testnormalizeaiplan_test_keeps_safe_command_without_flag": ".test_keeps_safe_command_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L99 | neighbors=[TestNormalizeAiPlan, ._raw()]
- "tests_test_remediation_kb_testclassify_test_cve_without_keyword_is_patch": ".test_cve_without_keyword_is_patch()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L31 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testclassify_test_keyword_categories": ".test_keyword_categories()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L28 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testclassify_test_order_specificity_anon_ftp_beats_generic": ".test_order_specificity_anon_ftp_beats_generic()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L38 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testclassify_test_unmatched_is_generic": ".test_unmatched_is_generic()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L35 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_missing_os_defaults_to_generic": ".test_missing_os_defaults_to_generic()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L84 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_network_os_falls_back_to_generic_guidance": ".test_network_os_falls_back_to_generic_guidance()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L72 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_returns_kb_source_and_category": ".test_returns_kb_source_and_category()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L60 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_steps_are_numbered_and_os_filtered": ".test_steps_are_numbered_and_os_filtered()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L66 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_unknown_finding_yields_generic_plan": ".test_unknown_finding_yields_generic_plan()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L79 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_routes_fakedb_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L72 | neighbors=[_FakeDB, _scalar_result()]
- "tests_test_remediation_routes_genunavailable": "_GenUnavailable" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L80 | neighbors=[test_remediation_routes.py, .__init__()]
- "tests_test_remediation_routes_testupsertstatement_test_refreshes_generated_at_on_conflict": ".test_refreshes_generated_at_on_conflict()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L210 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_regeneration_resets_review_gate_not_inherits_prior_approval": ".test_regeneration_resets_review_gate_not_inherits_prior_approval()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L201 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_targets_the_unique_constraint": ".test_targets_the_unique_constraint()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L198 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_upsert_integration_stmt": "_stmt()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L49 | neighbors=[test_remediation_upsert_integration.py, _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-160.json

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
