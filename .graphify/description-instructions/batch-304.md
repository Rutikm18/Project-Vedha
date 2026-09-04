# Node Description Batch 305 of 330

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

- "tests_test_scanner_congestion_testsendpacer_test_clean_round_increases_rate_additively": ".test_clean_round_increases_rate_additively()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L39 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_empty_round_is_ignored_not_treated_as_total_loss": ".test_empty_round_is_ignored_not_treated_as_total_loss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L70 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_first_pace_does_not_block": ".test_first_pace_does_not_block()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L84 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_growth_is_bounded_by_max_rate": ".test_growth_is_bounded_by_max_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L57 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_loss_just_under_threshold_does_not_back_off": ".test_loss_just_under_threshold_does_not_back_off()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L64 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_lossy_round_halves_the_rate": ".test_lossy_round_halves_the_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L45 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_pace_actually_spends_wall_time_at_a_low_rate": ".test_pace_actually_spends_wall_time_at_a_low_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L75 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_rate_zero_disables_pacing": ".test_rate_zero_disables_pacing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L90 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testsendpacer_test_stats_expose_throttling": ".test_stats_expose_throttling()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L97 | neighbors=[TestSendPacer]
- "tests_test_scanner_congestion_testwaitreadable_test_returns_false_when_nothing_arrives_before_deadline": ".test_returns_false_when_nothing_arrives_before_deadline()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L107 | neighbors=[TestWaitReadable]
- "tests_test_scanner_congestion_testwaitreadable_test_returns_true_as_soon_as_data_is_waiting": ".test_returns_true_as_soon_as_data_is_waiting()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L114 | neighbors=[TestWaitReadable]
- "tests_test_scanner_congestion_testwaitreadable_test_unselectable_object_degrades_to_assume_readable": ".test_unselectable_object_degrades_to_assume_readable()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L129 | neighbors=[TestWaitReadable]
- "tests_test_scanner_congestion_testwaitreadable_test_zero_timeout_never_blocks": ".test_zero_timeout_never_blocks()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L122 | neighbors=[TestWaitReadable]
- "tests_test_scanner_parity_rationale_1": "test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1" | kind=entity | source=probe/tests/test_scanner_parity.py:L1 | neighbors=[test_scanner_parity.py]
- "tests_test_scanner_parity_rationale_30": "Every scanner module authored in main_scripts must exist in scanner/." | kind=entity | source=probe/tests/test_scanner_parity.py:L30 | neighbors=[test_scanner_is_superset_of_no_missing_…]
- "tests_test_scanner_parity_rationale_39": "scanner/ must not carry modules that main_scripts/ does not — otherwise the" | kind=entity | source=probe/tests/test_scanner_parity.py:L39 | neighbors=[test_no_extra_scanner_files()]
- "tests_test_scanner_parity_rationale_49": "Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py." | kind=entity | source=probe/tests/test_scanner_parity.py:L49 | neighbors=[test_scanner_module_matches_main_script…]
- "tests_test_scope_crypt_rationale_1": "Tests for agent/scope_crypt.py" | kind=entity | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[test_scope_crypt.py]
- "tests_test_scope_crypt_rationale_79": "Each encryption uses a fresh ephemeral key, so blobs are different." | kind=entity | source=probe/tests/test_scope_crypt.py:L79 | neighbors=[.test_multiple_encrypts_different()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_b64_roundtrip": ".test_b64_roundtrip()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L70 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_plaintexts_are_distinct": ".test_different_plaintexts_are_distinct()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L64 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_recipient_cannot_decrypt": ".test_different_recipient_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L43 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_empty_scope": ".test_roundtrip_empty_scope()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L36 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_plaintext": ".test_roundtrip_plaintext()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L29 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_tampered_blob": ".test_tampered_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L51 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_too_short_blob": ".test_too_short_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L59 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testkeygeneration_test_generates_32_byte_keys": ".test_generates_32_byte_keys()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L16 | neighbors=[TestKeyGeneration]
- "tests_test_scope_crypt_testkeygeneration_test_generates_different_keys_each_call": ".test_generates_different_keys_each_call()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L21 | neighbors=[TestKeyGeneration]
- "tests_test_scope_targets_rationale_1": "test_scope_targets.py — the pure scope-authorization core shared by the dispatch" | kind=entity | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[test_scope_targets.py]
- "tests_test_scope_targets_rationale_99": "Whatever the validator accepts must be provably inside the scope." | kind=entity | source=manager/backend/tests/test_scope_targets.py:L99 | neighbors=[test_property_every_accepted_target_is_…]
- "tests_test_scope_targets_testexclusions_test_target_clear_of_exclusions_is_allowed": ".test_target_clear_of_exclusions_is_allowed()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L82 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testexclusions_test_target_inside_an_exclusion_is_rejected": ".test_target_inside_an_exclusion_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L71 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testexclusions_test_target_overlapping_an_exclusion_is_rejected": ".test_target_overlapping_an_exclusion_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L76 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testipversionsafety_test_v6_in_v6_scope": ".test_v6_in_v6_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L92 | neighbors=[TestIpVersionSafety]
- "tests_test_scope_targets_testipversionsafety_test_v6_target_against_v4_scope_is_rejected": ".test_v6_target_against_v4_scope_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L89 | neighbors=[TestIpVersionSafety]
- "tests_test_scope_targets_testnoscopeauthorizesnothing_test_empty_scope_denies_all": ".test_empty_scope_denies_all()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L17 | neighbors=[TestNoScopeAuthorizesNothing]
- "tests_test_scope_targets_testoutofscopeisrejected_test_blank_token_is_rejected": ".test_blank_token_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L63 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_cidr_broader_than_scope": ".test_cidr_broader_than_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L48 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_explicit_empty_list_is_rejected": ".test_explicit_empty_list_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L57 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_hostname_is_not_routable": ".test_hostname_is_not_routable()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L60 | neighbors=[TestOutOfScopeIsRejected]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-304.json

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
