# Node Description Batch 302 of 332

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_remediation_generator_testparsejsonresponse_test_strips_json_fence": ".test_strips_json_fence()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L36 | neighbors=[TestParseJsonResponse] | lang=en
- "tests_test_remediation_generator_testsafecommands_test_drops_destructive_keeps_safe": ".test_drops_destructive_keeps_safe()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L56 | neighbors=[TestSafeCommands] | lang=en
- "tests_test_remediation_generator_testsafecommands_test_null_command_yields_nothing": ".test_null_command_yields_nothing()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L63 | neighbors=[TestSafeCommands] | lang=en
- "tests_test_remediation_kb_rationale_1": "test_remediation_kb.py — the pure deterministic remediation knowledge base." | kind=entity | source=manager/backend/tests/test_remediation_kb.py:L1 | neighbors=[test_remediation_kb.py] | lang=en
- "tests_test_remediation_kb_testrecipeshape_test_every_recipe_has_required_fields": ".test_every_recipe_has_required_fields()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L52 | neighbors=[TestRecipeShape] | lang=en
- "tests_test_remediation_kb_testrecipeshape_test_every_recipe_step_has_all_os_keys": ".test_every_recipe_step_has_all_os_keys()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L44 | neighbors=[TestRecipeShape] | lang=en
- "tests_test_remediation_routes_fakedb_flush": ".flush()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L76 | neighbors=[_FakeDB] | lang=en
- "tests_test_remediation_routes_fakedb_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L67 | neighbors=[_FakeDB] | lang=en
- "tests_test_remediation_routes_genai_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L89 | neighbors=[_GenAI] | lang=en
- "tests_test_remediation_routes_genai_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L86 | neighbors=[_GenAI] | lang=en
- "tests_test_remediation_routes_genunavailable_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L81 | neighbors=[_GenUnavailable] | lang=en
- "tests_test_remediation_routes_rationale_1": "test_remediation_routes.py — Section 5: operator remediation endpoints + wiring." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L1 | neighbors=[test_remediation_routes.py] | lang=en
- "tests_test_remediation_routes_rationale_182": "Verify the ON CONFLICT logic at the SQL level (no DB needed)." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L182 | neighbors=[TestUpsertStatement] | lang=en
- "tests_test_remediation_routes_rationale_189": "Verify the ON CONFLICT logic at the SQL level (no DB needed)." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L189 | neighbors=[TestUpsertStatement] | lang=en
- "tests_test_remediation_routes_rationale_53": "A result whose .one() yields the RETURNING row (upsert path)." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L53 | neighbors=[_one_result()] | lang=en
- "tests_test_remediation_routes_rationale_54": "A result whose .one() yields the RETURNING row (upsert path)." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L54 | neighbors=[_one_result()] | lang=en
- "tests_test_remediation_routes_rationale_65": "execute() returns the next queued result object; flush is counted." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L65 | neighbors=[_FakeDB] | lang=en
- "tests_test_remediation_routes_rationale_66": "execute() returns the next queued result object; flush is counted." | kind=entity | source=manager/backend/tests/test_remediation_routes.py:L66 | neighbors=[_FakeDB] | lang=en
- "tests_test_remediation_routes_test_remediation_router_is_mounted": "test_remediation_router_is_mounted()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L101 | neighbors=[test_remediation_routes.py] | lang=en
- "tests_test_remediation_upsert_integration_rationale_1": "test_remediation_upsert_integration.py — real-Postgres verification of the remed" | kind=entity | source=manager/backend/tests/test_remediation_upsert_integration.py:L1 | neighbors=[test_remediation_upsert_integration.py] | lang=en
- "tests_test_resolution_coverage_test_coverage_counts_only_completed_scanner_observations": "test_coverage_counts_only_completed_scanner_observations()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L12 | neighbors=[test_resolution_coverage.py] | lang=en
- "tests_test_resolution_coverage_test_coverage_empty_when_no_scanner_runs": "test_coverage_empty_when_no_scanner_runs()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L27 | neighbors=[test_resolution_coverage.py] | lang=en
- "tests_test_resolution_coverage_test_host_of_strips_single_port": "test_host_of_strips_single_port()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L6 | neighbors=[test_resolution_coverage.py] | lang=en
- "tests_test_resolution_decision_test_db_change_blocks_resolution": "test_db_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L22 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolution_decision_test_high_needs_two_covered_clean_runs": "test_high_needs_two_covered_clean_runs()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L36 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolution_decision_test_medium_resolves_on_first_covered_clean_run": "test_medium_resolves_on_first_covered_clean_run()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L29 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolution_decision_test_not_covered_is_skipped_and_counter_untouched": "test_not_covered_is_skipped_and_counter_untouched()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L15 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolution_decision_test_threshold_is_stricter_for_critical_and_high": "test_threshold_is_stricter_for_critical_and_high()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L7 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolve_asset_cache_rationale_1": "Perf/N+1: _resolve_asset memoizes per-run so a host with many findings is resolv" | kind=entity | source=manager/backend/tests/test_resolve_asset_cache.py:L1 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_asset_cache_test_cache_resolves_each_host_once": "test_cache_resolves_each_host_once()" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L15 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_asset_cache_test_host_port_target_normalized": "test_host_port_target_normalized()" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L42 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_asset_cache_test_no_cache_keeps_old_behavior": "test_no_cache_keeps_old_behavior()" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L31 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_rationale_1": "test_resolve.py — resolve() address-family selection (task A9)." | kind=entity | source=probe/tests/test_resolve.py:L1 | neighbors=[test_resolve.py] | lang=pt
- "tests_test_resolve_rationale_12": "Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)." | kind=entity | source=probe/tests/test_resolve.py:L12 | neighbors=[_infos()] | lang=en
- "tests_test_resolve_testresolvefamily_test_unresolvable_raises": ".test_unresolvable_raises()" | kind=code-symbol | source=probe/tests/test_resolve.py:L40 | neighbors=[TestResolveFamily] | lang=en
- "tests_test_result_archive_rationale_1": "test_result_archive.py — the local result archive written before submission.  Th" | kind=entity | source=probe/tests/test_result_archive.py:L1 | neighbors=[test_result_archive.py] | lang=en
- "tests_test_result_archive_rationale_130": "A read-only filesystem must cost a warning, never a scan result." | kind=entity | source=probe/tests/test_result_archive.py:L130 | neighbors=[.test_unwritable_directory_does_not_fai…] | lang=pt
- "tests_test_result_archive_rationale_152": "Unset env => alongside agent/ scanner/ workflow/ (in the image, /app/result)." | kind=entity | source=probe/tests/test_result_archive.py:L152 | neighbors=[.test_default_location_is_the_probe_roo…] | lang=en
- "tests_test_result_archive_rationale_163": "The agent creates the archive directory at boot so the operator sees the     pat" | kind=entity | source=probe/tests/test_result_archive.py:L163 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_archive_rationale_186": "The Linux bind-mount case: Docker creates the source as root, so the         dir" | kind=entity | source=probe/tests/test_result_archive.py:L186 | neighbors=[.test_existing_but_unwritable_directory…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-301.json

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
