# Node Description Batch 300 of 332

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

- "tests_test_probe_enrollment_test_enrollment_create_accepts_optional_enroll_token": "test_enrollment_create_accepts_optional_enroll_token()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L125 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_generate_enroll_token_is_prefixed_hashed_and_shown_once": "test_generate_enroll_token_is_prefixed_hashed_and_shown_once()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L92 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_public_key_must_be_canonical_base64_of_32_bytes": "test_public_key_must_be_canonical_base64_of_32_bytes()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L29 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_refresh_secret_is_stable_per_request_and_device_secret": "test_refresh_secret_is_stable_per_request_and_device_secret()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L50 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_site_policy_rejects_exclusion_outside_authorized_scope": "test_site_policy_rejects_exclusion_outside_authorized_scope()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L58 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_manifest_rationale_1": "test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity" | kind=entity | source=probe/tests/test_probe_manifest.py:L1 | neighbors=[test_probe_manifest.py]
- "tests_test_probe_next_features_rationale_1": "test_probe_next_features.py — the probe_next plan: run the improved main_scripts" | kind=entity | source=probe/tests/test_probe_next_features.py:L1 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_discovery_defaults_to_standard_intensity_no_override": "test_discovery_defaults_to_standard_intensity_no_override()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L77 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_force_profile_overrides_intensity": "test_force_profile_overrides_intensity()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L52 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_full_port_audit_advertises_syn_method": "test_full_port_audit_advertises_syn_method()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L200 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_full_port_audit_records_full_coverage_in_applied_tuning": "test_full_port_audit_records_full_coverage_in_applied_tuning()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L65 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_light_and_deep_change_port_breadth": "test_light_and_deep_change_port_breadth()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L37 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_new_scan_types_still_enforce_scope": "test_new_scan_types_still_enforce_scope()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L169 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_new_use_cases_are_rejected_if_not_in_library": "test_new_use_cases_are_rejected_if_not_in_library()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L183 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_new_use_cases_present_and_capable": "test_new_use_cases_present_and_capable()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L58 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_none_intensity_defaults_to_standard": "test_none_intensity_defaults_to_standard()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L42 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_params_intensity_overrides_and_is_applied": "test_params_intensity_overrides_and_is_applied()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L84 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_scan_method_selection_rule": "test_scan_method_selection_rule()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L191 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_standard_intensity_is_a_noop_baseline": "test_standard_intensity_is_a_noop_baseline()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L29 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_syn_scan_method_routes_through_syn_scanner": "test_syn_scan_method_routes_through_syn_scanner()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L206 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_unknown_intensity_raises": "test_unknown_intensity_raises()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L46 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_unsupported_intensity_is_rejected_before_scanning": "test_unsupported_intensity_is_rejected_before_scanning()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L93 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_simple_approve_rationale_1": "test_probe_simple_approve.py — one-click probe approval helpers (item 5)." | kind=entity | source=manager/backend/tests/test_probe_simple_approve.py:L1 | neighbors=[test_probe_simple_approve.py]
- "tests_test_probe_simple_approve_rationale_12": "db.execute(...).scalars().all() → the given agent-name list." | kind=entity | source=manager/backend/tests/test_probe_simple_approve.py:L12 | neighbors=[_db_names()]
- "tests_test_probe_simple_approve_testsimpleapproveinput_test_defaults_are_all_optional": ".test_defaults_are_all_optional()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L39 | neighbors=[TestSimpleApproveInput]
- "tests_test_probe_simple_approve_testsimpleapproveinput_test_overrides_accepted": ".test_overrides_accepted()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L46 | neighbors=[TestSimpleApproveInput]
- "tests_test_project_time_rationale_1": "Manager-side project time: render in IST, stay timezone-AWARE.  The manager stor" | kind=entity | source=manager/backend/tests/test_project_time.py:L1 | neighbors=[test_project_time.py]
- "tests_test_project_time_rationale_38": "The property that makes this safe next to existing UTC data." | kind=entity | source=manager/backend/tests/test_project_time.py:L38 | neighbors=[.test_still_orders_against_utc_rows()]
- "tests_test_project_time_rationale_46": "Every naive datetime in this codebase's history came from utcnow().         Assu" | kind=entity | source=manager/backend/tests/test_project_time.py:L46 | neighbors=[.test_naive_is_assumed_utc()]
- "tests_test_project_time_rationale_87": "Guards the actual bug: utcnow() strings carried no offset." | kind=entity | source=manager/backend/tests/test_project_time.py:L87 | neighbors=[test_websocket_no_longer_emits_naive_ti…]
- "tests_test_project_time_testfilestamp_test_filename_safe": ".test_filename_safe()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L64 | neighbors=[TestFileStamp]
- "tests_test_project_time_testfilestamp_test_no_z_suffix_on_local_time": ".test_no_z_suffix_on_local_time()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L61 | neighbors=[TestFileStamp]
- "tests_test_project_time_testoverrideandfallback_test_bad_zone_does_not_crash_the_api": ".test_bad_zone_does_not_crash_the_api()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L75 | neighbors=[TestOverrideAndFallback]
- "tests_test_project_time_testoverrideandfallback_test_ist_survives_missing_tzdata": ".test_ist_survives_missing_tzdata()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L81 | neighbors=[TestOverrideAndFallback]
- "tests_test_project_time_testoverrideandfallback_test_vedha_tz_override": ".test_vedha_tz_override()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L69 | neighbors=[TestOverrideAndFallback]
- "tests_test_project_time_testrendering_test_default_is_ist": ".test_default_is_ist()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L24 | neighbors=[TestRendering]
- "tests_test_project_time_testrendering_test_same_instant_as_utc": ".test_same_instant_as_utc()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L32 | neighbors=[TestRendering]
- "tests_test_project_time_testrendering_test_timestamp_carries_an_offset": ".test_timestamp_carries_an_offset()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L27 | neighbors=[TestRendering]
- "tests_test_project_time_testtoprojecttz_test_aware_input_keeps_its_instant": ".test_aware_input_keeps_its_instant()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L51 | neighbors=[TestToProjectTz]
- "tests_test_project_time_testtoprojecttz_test_none_passes_through": ".test_none_passes_through()" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L56 | neighbors=[TestToProjectTz]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-299.json

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
