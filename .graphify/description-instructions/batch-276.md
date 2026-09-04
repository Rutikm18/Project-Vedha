# Node Description Batch 277 of 330

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

- "tests_test_engine_bridge_ingest_health_rationale_85": "The census is best-effort by contract: an older engine returning no     IngestRe" | kind=entity | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L85 | neighbors=[test_census_survives_an_engine_that_ret…]
- "tests_test_engine_bridge_posture_rationale_1": "test_engine_bridge_posture.py — the posture/config-exposure track reaches Findin" | kind=entity | source=manager/backend/tests/test_engine_bridge_posture.py:L1 | neighbors=[test_engine_bridge_posture.py]
- "tests_test_engine_bridge_posture_test_no_posture_no_finding": "test_no_posture_no_finding()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L69 | neighbors=[test_engine_bridge_posture.py]
- "tests_test_engine_bridge_posture_test_posture_finding_becomes_a_finding_row": "test_posture_finding_becomes_a_finding_row()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L33 | neighbors=[test_engine_bridge_posture.py]
- "tests_test_engine_bridge_regression_test_reopen_flips_remediated_to_open_and_flags_regression": "test_reopen_flips_remediated_to_open_and_flags_regression()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_regression.py:L10 | neighbors=[test_engine_bridge_regression.py]
- "tests_test_engine_bridge_resolution_test_run_records_coverage_and_invokes_resolution": "test_run_records_coverage_and_invokes_resolution()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_resolution.py:L12 | neighbors=[test_engine_bridge_resolution.py]
- "tests_test_engine_bridge_verification_test_stamp_verification_sets_columns_when_enabled": "test_stamp_verification_sets_columns_when_enabled()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_verification.py:L13 | neighbors=[test_engine_bridge_verification.py]
- "tests_test_enqueue_intensity_rationale_1": "test_enqueue_intensity.py — the manager's first-class scan-intensity knob.  Oper" | kind=entity | source=manager/backend/tests/test_enqueue_intensity.py:L1 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_every_manager_code_maps_to_a_known_use_case": "test_every_manager_code_maps_to_a_known_use_case()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L76 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_intensity_accepts_code_or_name": "test_intensity_accepts_code_or_name()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L62 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_invalid_intensity_is_rejected_at_the_schema": "test_invalid_intensity_is_rejected_at_the_schema()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L35 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_normalize_intensity_name_maps_codes": "test_normalize_intensity_name_maps_codes()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L69 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_numeric_uc_code_accepted": "test_numeric_uc_code_accepted()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L52 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_omitted_intensity_is_none": "test_omitted_intensity_is_none()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L30 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_unknown_uc_code_rejected": "test_unknown_uc_code_rejected()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L57 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_use_case_catalog_exposes_intensity_for_new_cases": "test_use_case_catalog_exposes_intensity_for_new_cases()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L44 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_valid_intensities_mirror_the_probe_set": "test_valid_intensities_mirror_the_probe_set()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L40 | neighbors=[test_enqueue_intensity.py]
- "tests_test_enqueue_intensity_test_valid_intensity_is_accepted": "test_valid_intensity_is_accepted()" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L24 | neighbors=[test_enqueue_intensity.py]
- "tests_test_exploit_engine_testmetasploitintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L434 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_connect_and_list_modules": ".test_connect_and_list_modules()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L441 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_run_safe_scanner_smb": ".test_run_safe_scanner_smb()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L450 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_call_without_connect_raises": ".test_call_without_connect_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L233 | neighbors=[TestMetasploitRPCClient]
- "tests_test_exploit_engine_testnucleiexploitrunner_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L351 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_evidence_truncated_to_max_bytes": ".test_evidence_truncated_to_max_bytes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L405 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_extract_evidence_includes_curl": ".test_extract_evidence_includes_curl()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L395 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_nonexistent_template_not_safe": ".test_nonexistent_template_not_safe()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L369 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_hit": ".test_parse_poc_output_hit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L374 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_malformed_json_skipped": ".test_parse_poc_output_malformed_json_skipped()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L389 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_miss": ".test_parse_poc_output_miss()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L380 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_wrong_cve": ".test_parse_poc_output_wrong_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L385 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_safe_template_passes": ".test_safe_template_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L354 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_unsafe_template_blocked": ".test_unsafe_template_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L362 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testrequiresapproval_test_adcs_server": ".test_adcs_server()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L170 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_critical_asset_needs_approval": ".test_critical_asset_needs_approval()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L155 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_dc_hostname_needs_approval": ".test_dc_hostname_needs_approval()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L161 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_dc02_pattern": ".test_dc02_pattern()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L164 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_exchange_server": ".test_exchange_server()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L167 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_medium_non_dc_no_approval": ".test_medium_non_dc_no_approval()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L158 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_normal_workstation": ".test_normal_workstation()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L173 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testvalidatemodule_test_dos_blocked": ".test_dos_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L108 | neighbors=[TestValidateModule]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-276.json

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
