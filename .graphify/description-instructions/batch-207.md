# Node Description Batch 208 of 227

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

- "tests_test_probe_next_features_test_unknown_intensity_raises": "test_unknown_intensity_raises()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L46 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_unsupported_intensity_is_rejected_before_scanning": "test_unsupported_intensity_is_rejected_before_scanning()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L93 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_simple_approve_rationale_1": "test_probe_simple_approve.py — one-click probe approval helpers (item 5)." | kind=entity | source=manager/backend/tests/test_probe_simple_approve.py:L1 | neighbors=[test_probe_simple_approve.py]
- "tests_test_probe_simple_approve_rationale_12": "db.execute(...).scalars().all() → the given agent-name list." | kind=entity | source=manager/backend/tests/test_probe_simple_approve.py:L12 | neighbors=[_db_names()]
- "tests_test_probe_simple_approve_testsimpleapproveinput_test_defaults_are_all_optional": ".test_defaults_are_all_optional()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L34 | neighbors=[TestSimpleApproveInput]
- "tests_test_probe_simple_approve_testsimpleapproveinput_test_overrides_accepted": ".test_overrides_accepted()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L41 | neighbors=[TestSimpleApproveInput]
- "tests_test_remediation_generator_rationale_1": "test_remediation_generator.py — Section 3: the AI remediation-plan helpers.  Pur" | kind=entity | source=manager/backend/tests/test_remediation_generator.py:L1 | neighbors=[test_remediation_generator.py]
- "tests_test_remediation_generator_testnormalizeaiplan_test_missing_steps_yields_empty": ".test_missing_steps_yields_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L105 | neighbors=[TestNormalizeAiPlan]
- "tests_test_remediation_generator_testnormalizeaiplan_test_non_dict_step_is_skipped_and_missing_title_defaults": ".test_non_dict_step_is_skipped_and_missing_title_defaults()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L109 | neighbors=[TestNormalizeAiPlan]
- "tests_test_remediation_generator_testparsejsonresponse_test_empty_returns_empty": ".test_empty_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L51 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testparsejsonresponse_test_junk_returns_empty": ".test_junk_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L45 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testparsejsonresponse_test_non_object_json_returns_empty": ".test_non_object_json_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L48 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testparsejsonresponse_test_plain_object": ".test_plain_object()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L33 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testparsejsonresponse_test_recovers_from_preamble": ".test_recovers_from_preamble()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L42 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testparsejsonresponse_test_strips_bare_fence": ".test_strips_bare_fence()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L39 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testparsejsonresponse_test_strips_json_fence": ".test_strips_json_fence()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L36 | neighbors=[TestParseJsonResponse]
- "tests_test_remediation_generator_testsafecommands_test_drops_destructive_keeps_safe": ".test_drops_destructive_keeps_safe()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L56 | neighbors=[TestSafeCommands]
- "tests_test_remediation_generator_testsafecommands_test_null_command_yields_nothing": ".test_null_command_yields_nothing()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L63 | neighbors=[TestSafeCommands]
- "tests_test_remediation_kb_rationale_1": "test_remediation_kb.py — the pure deterministic remediation knowledge base." | kind=entity | source=manager/backend/tests/test_remediation_kb.py:L1 | neighbors=[test_remediation_kb.py]
- "tests_test_remediation_kb_testrecipeshape_test_every_recipe_has_required_fields": ".test_every_recipe_has_required_fields()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L52 | neighbors=[TestRecipeShape]
- "tests_test_remediation_kb_testrecipeshape_test_every_recipe_step_has_all_os_keys": ".test_every_recipe_step_has_all_os_keys()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L44 | neighbors=[TestRecipeShape]
- "tests_test_remediation_routes_fakedb_flush": ".flush()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L75 | neighbors=[_FakeDB]
- "tests_test_remediation_routes_fakedb_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L66 | neighbors=[_FakeDB]
- "tests_test_remediation_routes_genai_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L88 | neighbors=[_GenAI]
- "tests_test_remediation_routes_genai_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L85 | neighbors=[_GenAI]
- "tests_test_remediation_routes_genunavailable_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L80 | neighbors=[_GenUnavailable]
- "tests_test_remediation_routes_rationale_1": "test_remediation_routes.py — Section 5: operator remediation endpoints + wiring." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L1 | neighbors=[test_remediation_routes.py]
- "tests_test_remediation_routes_rationale_182": "Verify the ON CONFLICT logic at the SQL level (no DB needed)." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L182 | neighbors=[TestUpsertStatement]
- "tests_test_remediation_routes_rationale_53": "A result whose .one() yields the RETURNING row (upsert path)." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L53 | neighbors=[_one_result()]
- "tests_test_remediation_routes_rationale_65": "execute() returns the next queued result object; flush is counted." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L65 | neighbors=[_FakeDB]
- "tests_test_remediation_routes_test_remediation_router_is_mounted": "test_remediation_router_is_mounted()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L100 | neighbors=[test_remediation_routes.py]
- "tests_test_remediation_upsert_integration_rationale_1": "test_remediation_upsert_integration.py — real-Postgres verification of the remed" | kind=entity | source=manager/backend/tests/test_remediation_upsert_integration.py:L1 | neighbors=[test_remediation_upsert_integration.py]
- "tests_test_resolution_coverage_test_coverage_counts_only_completed_scanner_observations": "test_coverage_counts_only_completed_scanner_observations()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L12 | neighbors=[test_resolution_coverage.py]
- "tests_test_resolution_coverage_test_coverage_empty_when_no_scanner_runs": "test_coverage_empty_when_no_scanner_runs()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L27 | neighbors=[test_resolution_coverage.py]
- "tests_test_resolution_coverage_test_host_of_strips_single_port": "test_host_of_strips_single_port()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L6 | neighbors=[test_resolution_coverage.py]
- "tests_test_resolution_decision_test_db_change_blocks_resolution": "test_db_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L22 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_high_needs_two_covered_clean_runs": "test_high_needs_two_covered_clean_runs()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L36 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_medium_resolves_on_first_covered_clean_run": "test_medium_resolves_on_first_covered_clean_run()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L29 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_not_covered_is_skipped_and_counter_untouched": "test_not_covered_is_skipped_and_counter_untouched()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L15 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_threshold_is_stricter_for_critical_and_high": "test_threshold_is_stricter_for_critical_and_high()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L7 | neighbors=[test_resolution_decision.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-207.json

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
