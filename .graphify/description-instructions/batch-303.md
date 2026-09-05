# Node Description Batch 304 of 336

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

- "tests_test_probe_core_testtuningfromparams_test_ssh_creds": ".test_ssh_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L909 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_win_creds": ".test_win_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L917 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testusecasesresolve_test_default_discovery": ".test_default_discovery()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L979 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_fallback_to_job_type": ".test_fallback_to_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L975 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_fallback_to_scan_type": ".test_fallback_to_scan_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L968 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_full_assessment": ".test_full_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L954 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_network_va_resolves": ".test_network_va_resolves()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L986 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_ot_passive": ".test_ot_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L959 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_unknown_use_case_raises": ".test_unknown_use_case_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L964 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_use_cases_count": ".test_use_cases_count()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L983 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_valid_use_case": ".test_valid_use_case()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L949 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testworkflowcache_test_get_missing": ".test_get_missing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L791 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_load_handles_corrupt_lines": ".test_load_handles_corrupt_lines()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L842 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_save_raises_without_path": ".test_save_raises_without_path()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L837 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_missing": ".test_should_recheck_missing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L795 | neighbors=[TestWorkflowCache]
- "tests_test_probe_enrollment_test_device_access_token_has_dedicated_audience_and_generation": "test_device_access_token_has_dedicated_audience_and_generation()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L18 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_ed25519_proof_of_possession_rejects_tampering": "test_ed25519_proof_of_possession_rejects_tampering()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L39 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_enroll_token_create_defaults_and_bounds": "test_enroll_token_create_defaults_and_bounds()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L113 | neighbors=[test_probe_enrollment.py]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-303.json

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
