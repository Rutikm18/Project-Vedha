# Node Description Batch 299 of 330

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

- "tests_test_probe_simple_approve_testsimpleapproveinput_test_overrides_accepted": ".test_overrides_accepted()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L46 | neighbors=[TestSimpleApproveInput] | lang=en
- "tests_test_project_time_rationale_1": "Manager-side project time: render in IST, stay timezone-AWARE.  The manager stor" | kind=entity | source=manager/backend/tests/test_project_time.py:L1 | neighbors=[test_project_time.py] | lang=en
- "tests_test_project_time_rationale_38": "The property that makes this safe next to existing UTC data." | kind=entity | source=manager/backend/tests/test_project_time.py:L38 | neighbors=[.test_still_orders_against_utc_rows()] | lang=en
- "tests_test_project_time_rationale_46": "Every naive datetime in this codebase's history came from utcnow().         Assu" | kind=entity | source=manager/backend/tests/test_project_time.py:L46 | neighbors=[.test_naive_is_assumed_utc()] | lang=en
- "tests_test_project_time_rationale_87": "Guards the actual bug: utcnow() strings carried no offset." | kind=entity | source=manager/backend/tests/test_project_time.py:L87 | neighbors=[test_websocket_no_longer_emits_naive_ti…] | lang=en
- "tests_test_project_time_testfilestamp_test_filename_safe": ".test_filename_safe()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L64 | neighbors=[TestFileStamp] | lang=en
- "tests_test_project_time_testfilestamp_test_no_z_suffix_on_local_time": ".test_no_z_suffix_on_local_time()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L61 | neighbors=[TestFileStamp] | lang=en
- "tests_test_project_time_testoverrideandfallback_test_bad_zone_does_not_crash_the_api": ".test_bad_zone_does_not_crash_the_api()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L75 | neighbors=[TestOverrideAndFallback] | lang=en
- "tests_test_project_time_testoverrideandfallback_test_ist_survives_missing_tzdata": ".test_ist_survives_missing_tzdata()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L81 | neighbors=[TestOverrideAndFallback] | lang=en
- "tests_test_project_time_testoverrideandfallback_test_vedha_tz_override": ".test_vedha_tz_override()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L69 | neighbors=[TestOverrideAndFallback] | lang=en
- "tests_test_project_time_testrendering_test_default_is_ist": ".test_default_is_ist()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L24 | neighbors=[TestRendering] | lang=en
- "tests_test_project_time_testrendering_test_same_instant_as_utc": ".test_same_instant_as_utc()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L32 | neighbors=[TestRendering] | lang=en
- "tests_test_project_time_testrendering_test_timestamp_carries_an_offset": ".test_timestamp_carries_an_offset()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L27 | neighbors=[TestRendering] | lang=en
- "tests_test_project_time_testtoprojecttz_test_aware_input_keeps_its_instant": ".test_aware_input_keeps_its_instant()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L51 | neighbors=[TestToProjectTz] | lang=en
- "tests_test_project_time_testtoprojecttz_test_none_passes_through": ".test_none_passes_through()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L56 | neighbors=[TestToProjectTz] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-298.json

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
