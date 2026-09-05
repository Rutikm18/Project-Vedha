# Node Description Batch 322 of 336

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

- "tests_test_use_cases_test_unknown_code_is_rejected": "test_unknown_code_is_rejected()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L106 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_web_claims_methods": "test_web_claims_methods()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L41 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_windows_estate_claims_signing": "test_windows_estate_claims_signing()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L32 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_va_campaign_buf_flush": ".flush()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L291 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_buf_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L285 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_buf_isatty": ".isatty()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L294 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_buf_write": ".write()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L288 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_rationale_1": "test_va_campaign.py — the VA-campaign orchestrator (scanner/va_campaign.py).  Th" | kind=entity | source=probe/tests/test_va_campaign.py:L1 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_callback_error_never_breaks_reporting": "test_callback_error_never_breaks_reporting()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L210 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_capability_list_covers_the_user_requested_set": "test_capability_list_covers_the_user_requested_set()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L233 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_ipv6_discovery_never_raises": "test_ipv6_discovery_never_raises()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L338 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_ipv6_discovery_reports_all_scans_only_in_scope": "test_ipv6_discovery_reports_all_scans_only_in_scope()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L323 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_ipv6_option_default_off": "test_ipv6_option_default_off()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L346 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_progress_file_written_atomically": "test_progress_file_written_atomically()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L195 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_validation_endpoints_rationale_1": "Mocked-session unit tests for the P3 active-validation endpoints (Task 4).  No D" | kind=entity | source=manager/backend/tests/test_validation_endpoints.py:L1 | neighbors=[test_validation_endpoints.py] | lang=en
- "tests_test_validation_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_validation.py:L111 | neighbors=[FakeClient] | lang=en
- "tests_test_validation_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_validation.py:L115 | neighbors=[FakeClient] | lang=en
- "tests_test_validation_gate_rationale_1": "test_validation_gate.py — the \"validation gate\" (build spec Card 7) as detection" | kind=entity | source=probe/tests/test_validation_gate.py:L1 | neighbors=[test_validation_gate.py] | lang=en
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
- "tests_test_verification_core_test_missing_confidence_defaults_to_inferred_not_crash": "test_missing_confidence_defaults_to_inferred_not_crash()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L33 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_graph_test_graph_available_is_boolean": "test_graph_available_is_boolean()" | kind=code-symbol | source=manager/backend/tests/test_verification_graph.py:L15 | neighbors=[test_verification_graph.py] | lang=en
- "tests_test_verification_graph_test_run_verification_matches_core_without_llm": "test_run_verification_matches_core_without_llm()" | kind=code-symbol | source=manager/backend/tests/test_verification_graph.py:L9 | neighbors=[test_verification_graph.py] | lang=en
- "tests_test_verification_llm_test_llm_can_flag_false_positive_and_lower": "test_llm_can_flag_false_positive_and_lower()" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L30 | neighbors=[test_verification_llm.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-321.json

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
