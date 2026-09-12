# Node Description Batch 353 of 380

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

- "tests_test_scanner_congestion_testresolvecandidates_test_unresolvable_name_raises": ".test_unresolvable_name_raises()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L325 | neighbors=[TestResolveCandidates] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_backoff_is_bounded_by_min_rate": ".test_backoff_is_bounded_by_min_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L52 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_clean_round_increases_rate_additively": ".test_clean_round_increases_rate_additively()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L40 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_empty_round_is_ignored_not_treated_as_total_loss": ".test_empty_round_is_ignored_not_treated_as_total_loss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L71 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_first_pace_does_not_block": ".test_first_pace_does_not_block()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L85 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_growth_is_bounded_by_max_rate": ".test_growth_is_bounded_by_max_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L58 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_loss_just_under_threshold_does_not_back_off": ".test_loss_just_under_threshold_does_not_back_off()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L65 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_lossy_round_halves_the_rate": ".test_lossy_round_halves_the_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L46 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_pace_actually_spends_wall_time_at_a_low_rate": ".test_pace_actually_spends_wall_time_at_a_low_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L76 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_rate_zero_disables_pacing": ".test_rate_zero_disables_pacing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L91 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_stats_expose_throttling": ".test_stats_expose_throttling()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L98 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_returns_false_when_nothing_arrives_before_deadline": ".test_returns_false_when_nothing_arrives_before_deadline()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L108 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_returns_true_as_soon_as_data_is_waiting": ".test_returns_true_as_soon_as_data_is_waiting()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L115 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_unselectable_object_degrades_to_assume_readable": ".test_unselectable_object_degrades_to_assume_readable()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L130 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_zero_timeout_never_blocks": ".test_zero_timeout_never_blocks()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L123 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_parity_rationale_1": "test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1" | kind=entity | source=probe/tests/test_scanner_parity.py:L1 | neighbors=[test_scanner_parity.py] | lang=en
- "tests_test_scanner_parity_rationale_30": "Every scanner module authored in main_scripts must exist in scanner/." | kind=entity | source=probe/tests/test_scanner_parity.py:L30 | neighbors=[test_scanner_is_superset_of_no_missing_…] | lang=en
- "tests_test_scanner_parity_rationale_39": "scanner/ must not carry modules that main_scripts/ does not — otherwise the" | kind=entity | source=probe/tests/test_scanner_parity.py:L39 | neighbors=[test_no_extra_scanner_files()] | lang=en
- "tests_test_scanner_parity_rationale_49": "Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py." | kind=entity | source=probe/tests/test_scanner_parity.py:L49 | neighbors=[test_scanner_module_matches_main_script…] | lang=en
- "tests_test_scheduler_rationale_1": "Which schedules are due, and when they run next.  Three decisions these pin down" | kind=entity | source=manager/backend/tests/test_scheduler.py:L1 | neighbors=[test_scheduler.py] | lang=en
- "tests_test_scheduler_rationale_109": "A single bad schedule must not wedge the whole fleet's scanning." | kind=entity | source=manager/backend/tests/test_scheduler.py:L109 | neighbors=[.test_one_failure_does_not_stop_the_oth…] | lang=en
- "tests_test_scheduler_rationale_45": "<= not <: a schedule due this instant must fire, not wait a tick." | kind=entity | source=manager/backend/tests/test_scheduler.py:L45 | neighbors=[.test_exactly_due_is_selected()] | lang=pt
- "tests_test_scheduler_rationale_72": "The catch-up-storm guard: two days late on a 24h schedule must produce         O" | kind=entity | source=manager/backend/tests/test_scheduler.py:L72 | neighbors=[.test_advances_from_now_not_from_the_mi…] | lang=pt
- "tests_test_scheduler_rationale_98": "Advancing a failure would silently skip the window, and the estate         would" | kind=entity | source=manager/backend/tests/test_scheduler.py:L98 | neighbors=[.test_failed_enqueue_does_not_advance()] | lang=en
- "tests_test_scheduler_testdueselection_test_empty": ".test_empty()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L60 | neighbors=[TestDueSelection] | lang=en
- "tests_test_scope_crypt_rationale_1": "Tests for agent/scope_crypt.py" | kind=entity | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[test_scope_crypt.py] | lang=en
- "tests_test_scope_crypt_rationale_79": "Each encryption uses a fresh ephemeral key, so blobs are different." | kind=entity | source=probe/tests/test_scope_crypt.py:L79 | neighbors=[.test_multiple_encrypts_different()] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_b64_roundtrip": ".test_b64_roundtrip()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L70 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_plaintexts_are_distinct": ".test_different_plaintexts_are_distinct()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L64 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_recipient_cannot_decrypt": ".test_different_recipient_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L43 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_empty_scope": ".test_roundtrip_empty_scope()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L36 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_plaintext": ".test_roundtrip_plaintext()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L29 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_tampered_blob": ".test_tampered_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L51 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_too_short_blob": ".test_too_short_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L59 | neighbors=[TestEncryptDecryptRoundtrip] | lang=en
- "tests_test_scope_crypt_testkeygeneration_test_generates_32_byte_keys": ".test_generates_32_byte_keys()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L16 | neighbors=[TestKeyGeneration] | lang=en
- "tests_test_scope_crypt_testkeygeneration_test_generates_different_keys_each_call": ".test_generates_different_keys_each_call()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L21 | neighbors=[TestKeyGeneration] | lang=en
- "tests_test_scope_model_rationale_1": "Phase 1 — typed-scope model: interface classification, the permanent denylist, S" | kind=entity | source=probe/tests/test_scope_model.py:L1 | neighbors=[test_scope_model.py] | lang=en
- "tests_test_scope_model_test_active_segment_requires_site_and_valid_cidr": "test_active_segment_requires_site_and_valid_cidr()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L62 | neighbors=[test_scope_model.py] | lang=en
- "tests_test_scope_model_test_classify_container_and_virtual": "test_classify_container_and_virtual()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L18 | neighbors=[test_scope_model.py] | lang=en
- "tests_test_scope_model_test_classify_loopback": "test_classify_loopback()" | kind=code-symbol | source=probe/tests/test_scope_model.py:L10 | neighbors=[test_scope_model.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-352.json

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
