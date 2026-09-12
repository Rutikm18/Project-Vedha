# Node Description Batch 320 of 380

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

- "tests_test_engine_bridge_posture_rationale_1": "test_engine_bridge_posture.py — the posture/config-exposure track reaches Findin" | kind=entity | source=manager/backend/tests/test_engine_bridge_posture.py:L1 | neighbors=[test_engine_bridge_posture.py] | lang=en
- "tests_test_engine_bridge_posture_test_no_posture_no_finding": "test_no_posture_no_finding()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L69 | neighbors=[test_engine_bridge_posture.py] | lang=en
- "tests_test_engine_bridge_posture_test_posture_finding_becomes_a_finding_row": "test_posture_finding_becomes_a_finding_row()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L33 | neighbors=[test_engine_bridge_posture.py] | lang=en
- "tests_test_engine_bridge_regression_test_reopen_flips_remediated_to_open_and_flags_regression": "test_reopen_flips_remediated_to_open_and_flags_regression()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_regression.py:L10 | neighbors=[test_engine_bridge_regression.py] | lang=en
- "tests_test_engine_bridge_resolution_test_run_records_coverage_and_invokes_resolution": "test_run_records_coverage_and_invokes_resolution()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_resolution.py:L12 | neighbors=[test_engine_bridge_resolution.py] | lang=en
- "tests_test_engine_bridge_verification_test_stamp_verification_sets_columns_when_enabled": "test_stamp_verification_sets_columns_when_enabled()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_verification.py:L13 | neighbors=[test_engine_bridge_verification.py] | lang=en
- "tests_test_enqueue_intensity_rationale_1": "test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper" | kind=entity | source=manager/backend/tests/test_enqueue_intensity.py:L1 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_every_manager_code_maps_to_a_known_use_case": "test_every_manager_code_maps_to_a_known_use_case()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L76 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_intensity_accepts_code_or_name": "test_intensity_accepts_code_or_name()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L62 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_invalid_intensity_is_rejected_at_the_schema": "test_invalid_intensity_is_rejected_at_the_schema()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L35 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_normalize_intensity_name_maps_codes": "test_normalize_intensity_name_maps_codes()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L69 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_numeric_uc_code_accepted": "test_numeric_uc_code_accepted()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L52 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_omitted_intensity_is_none": "test_omitted_intensity_is_none()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L30 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_unknown_uc_code_rejected": "test_unknown_uc_code_rejected()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L57 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_use_case_catalog_exposes_intensity_for_new_cases": "test_use_case_catalog_exposes_intensity_for_new_cases()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L44 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_valid_intensities_mirror_the_probe_set": "test_valid_intensities_mirror_the_probe_set()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L40 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_enqueue_intensity_test_valid_intensity_is_accepted": "test_valid_intensity_is_accepted()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L24 | neighbors=[test_enqueue_intensity.py] | lang=en
- "tests_test_eol_detection_rationale_1": "End-of-life / end-of-support OS detection.  An unsupported OS receives no securi" | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L1 | neighbors=[test_eol_detection.py] | lang=pt
- "tests_test_eol_detection_rationale_36": "Evidence invariant: no input, no verdict." | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L36 | neighbors=[.test_missing_os_release_returns_none()] | lang=en
- "tests_test_eol_detection_rationale_41": "windows server 2012 r2' must not be shadowed by 'windows server 2012'." | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L41 | neighbors=[.test_longest_match_wins()] | lang=en
- "tests_test_eol_detection_rationale_50": "Windows 7 died in 2020; the number must be large and positive, not a         sig" | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L50 | neighbors=[.test_days_past_eol_is_positive_for_lon…] | lang=en
- "tests_test_eol_detection_rationale_63": "Same shape the other posture-rule tests use (tests/test_posture_rules.py)." | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L63 | neighbors=[_fact()] | lang=en
- "tests_test_eol_detection_rationale_93": "Evidence invariant: os_guess alone is not enough to claim EOL." | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L93 | neighbors=[.test_silent_without_os_release()] | lang=en
- "tests_test_eol_detection_rationale_97": "The `requires` contract makes a missing input report MISSING_INPUT         (drif" | kind=entity | source=manager/detection_engine/tests/test_eol_detection.py:L97 | neighbors=[.test_declares_its_required_input()] | lang=en
- "tests_test_eol_detection_testcataloglookup_test_match_is_case_insensitive": ".test_match_is_case_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L46 | neighbors=[TestCatalogLookup] | lang=en
- "tests_test_eol_detection_testcataloglookup_test_supported_os_returns_none": ".test_supported_os_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L29 | neighbors=[TestCatalogLookup] | lang=en
- "tests_test_eol_detection_testcataloglookup_test_unknown_os_returns_none": ".test_unknown_os_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L32 | neighbors=[TestCatalogLookup] | lang=en
- "tests_test_eol_detection_testcataloglookup_test_windows_10_22h2_is_past_eol": ".test_windows_10_22h2_is_past_eol()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L21 | neighbors=[TestCatalogLookup] | lang=en
- "tests_test_evidence_summary_rationale_1": "evidence_summary — turn the messy evidence JSONB into a short, plain fact list." | kind=entity | source=manager/backend/tests/test_evidence_summary.py:L1 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_booleans_render_yes_no_with_exposure_labels": "test_booleans_render_yes_no_with_exposure_labels()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L29 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_common_keys_get_friendly_labels_in_priority_order": "test_common_keys_get_friendly_labels_in_priority_order()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L23 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_enrichment_kev_and_epss_are_surfaced_simply": "test_enrichment_kev_and_epss_are_surfaced_simply()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L36 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_lists_are_joined_not_json": "test_lists_are_joined_not_json()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L43 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_nested_dicts_do_not_leak_raw_json": "test_nested_dicts_do_not_leak_raw_json()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L68 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_noise_and_internal_keys_are_skipped": "test_noise_and_internal_keys_are_skipped()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L51 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_none_and_non_dict_inputs_are_empty": "test_none_and_non_dict_inputs_are_empty()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L12 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_output_is_capped_for_readability": "test_output_is_capped_for_readability()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L63 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_passthrough_of_already_shaped_list": "test_passthrough_of_already_shaped_list()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L18 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_evidence_summary_test_unknown_scalar_keys_fall_back_to_sentence_case": "test_unknown_scalar_keys_fall_back_to_sentence_case()" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L58 | neighbors=[test_evidence_summary.py] | lang=en
- "tests_test_exit_state_rationale_1": "Phase 3 — exit-state protocol (0b contract): 5 classes, reason->class map, exit-" | kind=entity | source=probe/tests/test_exit_state.py:L1 | neighbors=[test_exit_state.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-319.json

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
