# Node Description Batch 116 of 227

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

- "tests_test_probe_core_testworkflowcache_test_should_recheck_force_expired": ".test_should_recheck_force_expired()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L774 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_uncertain_always": ".test_should_recheck_uncertain_always()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L762 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_enrollment_test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses": "test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L102 | neighbors=[test_probe_enrollment.py, _token()]
- "tests_test_probe_enrollment_token": "_token()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L85 | neighbors=[test_probe_enrollment.py, test_enroll_token_usable_only_while_liv…]
- "tests_test_probe_manifest_test_manifest_is_clean_parseable_json": "test_manifest_is_clean_parseable_json()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L30 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_manifest_test_manifest_is_deterministic": "test_manifest_is_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L47 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_manifest_test_manifest_surfaces_the_capability_contract": "test_manifest_surfaces_the_capability_contract()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L37 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_next_features_test_device_inventory_post_stage_classifies_from_open_ports": "test_device_inventory_post_stage_classifies_from_open_ports()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L110 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_device_inventory_skips_hosts_without_evidence": "test_device_inventory_skips_hosts_without_evidence()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L124 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_exposure_matrix_flags_internet_reachable_ports": "test_exposure_matrix_flags_internet_reachable_ports()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L135 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_exposure_matrix_internal_only_from_lan_vantage": "test_exposure_matrix_internal_only_from_lan_vantage()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L150 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_no_post_stage_for_ordinary_scan_types": "test_no_post_stage_for_ordinary_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L161 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_simple_approve_testnextprobename_test_first_is_01": ".test_first_is_01()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L21 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_probe_simple_approve_testnextprobename_test_ignores_non_matching_and_non_numeric": ".test_ignores_non_matching_and_non_numeric()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L28 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_probe_simple_approve_testnextprobename_test_increments_past_highest_with_gaps": ".test_increments_past_highest_with_gaps()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L24 | neighbors=[TestNextProbeName, _db_names()]
- "tests_test_reaper_test_expired_attempt_fails_job_when_retry_budget_is_exhausted": "test_expired_attempt_fails_job_when_retry_budget_is_exhausted()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L39 | neighbors=[test_reaper.py, _objects()]
- "tests_test_reaper_test_expired_attempt_requeues_with_fence_history_preserved": "test_expired_attempt_requeues_with_fence_history_preserved()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L24 | neighbors=[test_reaper.py, _objects()]
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
- "tests_test_remediation_routes_fakedb_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L71 | neighbors=[_FakeDB, _scalar_result()]
- "tests_test_remediation_routes_genunavailable": "_GenUnavailable" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L79 | neighbors=[test_remediation_routes.py, .__init__()]
- "tests_test_remediation_routes_testupsertstatement_test_refreshes_generated_at_on_conflict": ".test_refreshes_generated_at_on_conflict()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L203 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_regeneration_resets_review_gate_not_inherits_prior_approval": ".test_regeneration_resets_review_gate_not_inherits_prior_approval()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L194 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_targets_the_unique_constraint": ".test_targets_the_unique_constraint()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L191 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_upsert_integration_stmt": "_stmt()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L49 | neighbors=[test_remediation_upsert_integration.py, _run()]
- "tests_test_remediation_upsert_integration_test_upsert_resets_gate_and_is_race_safe": "test_upsert_resets_gate_and_is_race_safe()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L103 | neighbors=[test_remediation_upsert_integration.py, _run()]
- "tests_test_resolve_testresolvefamily_test_default_no_family_is_backward_compatible": ".test_default_no_family_is_backward_compatible()" | kind=code-symbol | source=probe/tests/test_resolve.py:L34 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_family_absent_falls_back_to_first": ".test_requested_family_absent_falls_back_to_first()" | kind=code-symbol | source=probe/tests/test_resolve.py:L28 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_ipv4_selected_over_v6_first": ".test_requested_ipv4_selected_over_v6_first()" | kind=code-symbol | source=probe/tests/test_resolve.py:L21 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_risk_rank_test_bounds": "test_bounds()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L15 | neighbors=[test_risk_rank.py, _rank()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-115.json

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
