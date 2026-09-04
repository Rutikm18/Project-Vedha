# Node Description Batch 301 of 332

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

- "tests_test_project_timezone_rationale_1": "Project timestamps render in IST, and stay timezone-AWARE while doing it.  Opera" | kind=entity | source=probe/tests/test_project_timezone.py:L1 | neighbors=[test_project_timezone.py] | lang=en
- "tests_test_project_timezone_rationale_36": "Rendering moved; the instant did not." | kind=entity | source=probe/tests/test_project_timezone.py:L36 | neighbors=[.test_timestamp_is_the_same_instant_as_…] | lang=en
- "tests_test_project_timezone_rationale_42": "The ordering guarantee that makes this change safe." | kind=entity | source=probe/tests/test_project_timezone.py:L42 | neighbors=[.test_aware_timestamps_still_compare_ag…] | lang=en
- "tests_test_project_timezone_rationale_51": "A `Z` on a local-time stamp is an outright lie." | kind=entity | source=probe/tests/test_project_timezone.py:L51 | neighbors=[.test_file_stamp_has_no_z_suffix()] | lang=en
- "tests_test_project_timezone_rationale_72": "The timestamp that ends up inside every result file." | kind=entity | source=probe/tests/test_project_timezone.py:L72 | neighbors=[.test_scan_result_timestamp_is_ist()] | lang=en
- "tests_test_project_timezone_rationale_86": "A bad VEDHA_TZ must never take a scan down mid-engagement." | kind=entity | source=probe/tests/test_project_timezone.py:L86 | neighbors=[.test_unknown_zone_falls_back_without_c…] | lang=pt
- "tests_test_project_timezone_rationale_93": "Sealed/slim images may ship no tzdata. IST has no DST, so the fixed         +05:" | kind=entity | source=probe/tests/test_project_timezone.py:L93 | neighbors=[.test_ist_survives_a_missing_tzdata()] | lang=en
- "tests_test_project_timezone_testfilestamps_test_custom_format_is_honoured": ".test_custom_format_is_honoured()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L66 | neighbors=[TestFileStamps] | lang=en
- "tests_test_project_timezone_testfilestamps_test_file_stamp_is_filename_safe": ".test_file_stamp_is_filename_safe()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L57 | neighbors=[TestFileStamps] | lang=en
- "tests_test_project_timezone_testfilestamps_test_file_stamp_is_local_wall_clock": ".test_file_stamp_is_local_wall_clock()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L54 | neighbors=[TestFileStamps] | lang=en
- "tests_test_project_timezone_testfilestamps_test_file_stamp_sorts_chronologically": ".test_file_stamp_sorts_chronologically()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L61 | neighbors=[TestFileStamps] | lang=en
- "tests_test_project_timezone_testoverrideandfallback_test_vedha_tz_overrides_the_default": ".test_vedha_tz_overrides_the_default()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L79 | neighbors=[TestOverrideAndFallback] | lang=en
- "tests_test_project_timezone_testprojecttimezone_test_default_is_ist": ".test_default_is_ist()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L27 | neighbors=[TestProjectTimezone] | lang=en
- "tests_test_project_timezone_testprojecttimezone_test_timestamp_is_iso_with_offset_not_naive": ".test_timestamp_is_iso_with_offset_not_naive()" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L30 | neighbors=[TestProjectTimezone] | lang=en
- "tests_test_raw_facts_rationale_1": "Raw scanner facts endpoint — inspect exactly what the vedha-agent collected." | kind=entity | source=manager/backend/tests/test_raw_facts.py:L1 | neighbors=[test_raw_facts.py] | lang=en
- "tests_test_reference_rationale_1": "test_reference.py — the human-readable reference scheme.  A scan job could only" | kind=entity | source=manager/backend/tests/test_reference.py:L1 | neighbors=[test_reference.py] | lang=en
- "tests_test_reference_rationale_118": "Migration 0036 backfills in SQL so it needs no application layer. If the     two" | kind=entity | source=manager/backend/tests/test_reference.py:L118 | neighbors=[test_the_migration_backfill_agrees_with…] | lang=en
- "tests_test_reference_rationale_36": "A backfilled reference must match what the row would have been given         whe" | kind=entity | source=manager/backend/tests/test_reference.py:L36 | neighbors=[.test_uses_the_rows_own_date_not_today()] | lang=en
- "tests_test_reference_rationale_50": "The whole point of the scheme: a human relays it." | kind=entity | source=manager/backend/tests/test_reference.py:L50 | neighbors=[TestSurvivesBeingReadAloud] | lang=en
- "tests_test_reference_rationale_70": "The prefix and date are literal — folding them would corrupt a date." | kind=entity | source=manager/backend/tests/test_reference.py:L70 | neighbors=[.test_only_the_suffix_is_alias_folded()] | lang=en
- "tests_test_reference_rationale_88": "It is quoted in tickets — it must not move." | kind=entity | source=manager/backend/tests/test_reference.py:L88 | neighbors=[.test_the_same_row_always_gets_the_same…] | lang=en
- "tests_test_reference_testshape_test_an_unknown_prefix_is_refused": ".test_an_unknown_prefix_is_refused()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L44 | neighbors=[TestShape] | lang=en
- "tests_test_reference_testshape_test_naive_created_at_is_treated_as_utc": ".test_naive_created_at_is_treated_as_utc()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L40 | neighbors=[TestShape] | lang=en
- "tests_test_reference_teststability_test_different_rows_get_different_references": ".test_different_rows_get_different_references()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L92 | neighbors=[TestStability] | lang=en
- "tests_test_reference_teststamping_test_an_explicit_reference_is_never_overwritten": ".test_an_explicit_reference_is_never_overwritten()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L106 | neighbors=[TestStamping] | lang=en
- "tests_test_reference_teststamping_test_every_insert_gets_one": ".test_every_insert_gets_one()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L100 | neighbors=[TestStamping] | lang=en
- "tests_test_reference_teststamping_test_the_reference_matches_the_row_id": ".test_the_reference_matches_the_row_id()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L111 | neighbors=[TestStamping] | lang=en
- "tests_test_reference_testsurvivesbeingreadaloud_test_o_for_zero_and_l_for_one_resolve": ".test_o_for_zero_and_l_for_one_resolve()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L62 | neighbors=[TestSurvivesBeingReadAloud] | lang=en
- "tests_test_reference_testsurvivesbeingreadaloud_test_stray_spaces_are_tolerated": ".test_stray_spaces_are_tolerated()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L66 | neighbors=[TestSurvivesBeingReadAloud] | lang=en
- "tests_test_reference_testsurvivesbeingreadaloud_test_the_confusable_letters_are_absent": ".test_the_confusable_letters_are_absent()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L52 | neighbors=[TestSurvivesBeingReadAloud] | lang=en
- "tests_test_reference_testtellingthemapart_test_an_unregistered_prefix_is_not_ours": ".test_an_unregistered_prefix_is_not_ours()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L82 | neighbors=[TestTellingThemApart] | lang=en
- "tests_test_remediation_generator_rationale_1": "test_remediation_generator.py — Section 3: the AI remediation-plan helpers.  Pur" | kind=entity | source=manager/backend/tests/test_remediation_generator.py:L1 | neighbors=[test_remediation_generator.py] | lang=en
- "tests_test_remediation_generator_testnormalizeaiplan_test_missing_steps_yields_empty": ".test_missing_steps_yields_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L105 | neighbors=[TestNormalizeAiPlan] | lang=en
- "tests_test_remediation_generator_testnormalizeaiplan_test_non_dict_step_is_skipped_and_missing_title_defaults": ".test_non_dict_step_is_skipped_and_missing_title_defaults()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L109 | neighbors=[TestNormalizeAiPlan] | lang=en
- "tests_test_remediation_generator_testparsejsonresponse_test_empty_returns_empty": ".test_empty_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L51 | neighbors=[TestParseJsonResponse] | lang=en
- "tests_test_remediation_generator_testparsejsonresponse_test_junk_returns_empty": ".test_junk_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L45 | neighbors=[TestParseJsonResponse] | lang=en
- "tests_test_remediation_generator_testparsejsonresponse_test_non_object_json_returns_empty": ".test_non_object_json_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L48 | neighbors=[TestParseJsonResponse] | lang=en
- "tests_test_remediation_generator_testparsejsonresponse_test_plain_object": ".test_plain_object()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L33 | neighbors=[TestParseJsonResponse] | lang=en
- "tests_test_remediation_generator_testparsejsonresponse_test_recovers_from_preamble": ".test_recovers_from_preamble()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L42 | neighbors=[TestParseJsonResponse] | lang=en
- "tests_test_remediation_generator_testparsejsonresponse_test_strips_bare_fence": ".test_strips_bare_fence()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L39 | neighbors=[TestParseJsonResponse] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-300.json

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
