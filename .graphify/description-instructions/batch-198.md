# Node Description Batch 199 of 209

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

- "tests_test_udp_amplifiers_test_ntp_monlist_absent": "test_ntp_monlist_absent()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L13 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_ntp_monlist_enabled": "test_ntp_monlist_enabled()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L8 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_probe_builders_are_bytes": "test_probe_builders_are_bytes()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L31 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_use_cases_rationale_1": "Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only" | kind=entity | source=probe/tests/test_use_cases.py:L1 | neighbors=[test_use_cases.py] | lang=pt
- "tests_test_use_cases_test_codes_are_unique_and_stable": "test_codes_are_unique_and_stable()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L82 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_descriptions_do_not_overclaim": "test_descriptions_do_not_overclaim()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L25 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_every_code_maps_to_a_real_use_case": "test_every_code_maps_to_a_real_use_case()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L77 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_full_port_audit_is_deep": "test_full_port_audit_is_deep()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L64 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_intensity_code_and_name_equivalent": "test_intensity_code_and_name_equivalent()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L100 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_iot_survey_collects_banners": "test_iot_survey_collects_banners()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L45 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_new_use_cases_resolve": "test_new_use_cases_resolve()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L52 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_params_intensity_overrides_use_case": "test_params_intensity_overrides_use_case()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L69 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_resolve_accepts_string_digits_too": "test_resolve_accepts_string_digits_too()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L95 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_resolve_by_numeric_code": "test_resolve_by_numeric_code()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L90 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_string_use_case_id_still_wins_over_code": "test_string_use_case_id_still_wins_over_code()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L113 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_udp_claims_amplification": "test_udp_claims_amplification()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L36 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_unknown_code_is_rejected": "test_unknown_code_is_rejected()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L106 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_web_claims_methods": "test_web_claims_methods()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L41 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_windows_estate_claims_signing": "test_windows_estate_claims_signing()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L32 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_validation_endpoints_rationale_1": "Mocked-session unit tests for the P3 active-validation endpoints (Task 4).  No D" | kind=entity | source=manager/backend/tests/test_validation_endpoints.py:L1 | neighbors=[test_validation_endpoints.py] | lang=en
- "tests_test_validation_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_validation.py:L111 | neighbors=[FakeClient] | lang=en
- "tests_test_validation_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_validation.py:L115 | neighbors=[FakeClient] | lang=en
- "tests_test_validation_ingest_rationale_1": "Unit tests for P3 Task 7: validation-result ingestion → finding verdict.  Pure t" | kind=entity | source=manager/backend/tests/test_validation_ingest.py:L1 | neighbors=[test_validation_ingest.py] | lang=en
- "tests_test_validation_ingest_test_ingest_normal_scan_is_noop": "test_ingest_normal_scan_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L79 | neighbors=[test_validation_ingest.py] | lang=en
- "tests_test_validation_ingest_test_scan_result_is_not_mistaken_for_validation": "test_scan_result_is_not_mistaken_for_validation()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L64 | neighbors=[test_validation_ingest.py] | lang=en
- "tests_test_validation_request_schema_test_validation_request_columns_and_defaults": "test_validation_request_columns_and_defaults()" | kind=code-symbol | source=manager/backend/tests/test_validation_request_schema.py:L8 | neighbors=[test_validation_request_schema.py] | lang=en
- "tests_test_validation_test_parser_accepts_validate_command": "test_parser_accepts_validate_command()" | kind=code-symbol | source=probe/tests/test_validation.py:L254 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_resolve_use_cases_deduplicates_combined_suites": "test_resolve_use_cases_deduplicates_combined_suites()" | kind=code-symbol | source=probe/tests/test_validation.py:L19 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_score_inventory_reports_precision_recall_and_unscored_dimensions": "test_score_inventory_reports_precision_recall_and_unscored_dimensions()" | kind=code-symbol | source=probe/tests/test_validation.py:L62 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_target_address_count_is_conservative": "test_target_address_count_is_conservative()" | kind=code-symbol | source=probe/tests/test_validation.py:L47 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts": "test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts()" | kind=code-symbol | source=probe/tests/test_validation.py:L51 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_validate_targets_enforces_scope_and_exclusions": "test_validate_targets_enforces_scope_and_exclusions()" | kind=code-symbol | source=probe/tests/test_validation.py:L32 | neighbors=[test_validation.py] | lang=en
- "tests_test_vantage_fusion_rationale_1": "test_vantage_fusion.py — fleet-level reconciliation of exposure_matrix across pr" | kind=entity | source=manager/backend/tests/test_vantage_fusion.py:L1 | neighbors=[test_vantage_fusion.py] | lang=en
- "tests_test_vantage_fusion_rationale_16": "Build a one-target probe exposure result. `ports` maps 'proto/port' →     {vanta" | kind=entity | source=manager/backend/tests/test_vantage_fusion.py:L16 | neighbors=[_probe()] | lang=pt
- "tests_test_vantage_fusion_test_empty_and_malformed_are_safe": "test_empty_and_malformed_are_safe()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L87 | neighbors=[test_vantage_fusion.py] | lang=en
- "tests_test_vantage_fusion_test_reconstruct_probe_results_from_persisted_facts": "test_reconstruct_probe_results_from_persisted_facts()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L93 | neighbors=[test_vantage_fusion.py] | lang=en
- "tests_test_verification_core_test_authoritative_is_confirmed": "test_authoritative_is_confirmed()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L6 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_high_confidence_inferred_is_corroborated": "test_high_confidence_inferred_is_corroborated()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L14 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_kev_suspected_finding_needs_review": "test_kev_suspected_finding_needs_review()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L26 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_low_confidence_inferred_is_inferred": "test_low_confidence_inferred_is_inferred()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L20 | neighbors=[test_verification_core.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-198.json

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
