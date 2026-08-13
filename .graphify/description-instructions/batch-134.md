# Node Description Batch 135 of 144

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

- "tests_test_transport_testsubmitresult_test_permanent_client_errors_are_marked_for_quarantine": ".test_permanent_client_errors_are_marked_for_quarantine()" | kind=code-symbol | source=probe/tests/test_transport.py:L439 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testsubmitresult_test_retryable_client_errors_return_false_no_data_loss": ".test_retryable_client_errors_return_false_no_data_loss()" | kind=code-symbol | source=probe/tests/test_transport.py:L429 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testsubmitresult_test_server_error_returns_false": ".test_server_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L412 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testsubmitresult_test_small_payload_not_gzipped": ".test_small_payload_not_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L469 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testsubmitresult_test_successful_submit": ".test_successful_submit()" | kind=code-symbol | source=probe/tests/test_transport.py:L403 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testwebsocket_test_is_ws_connected_false_by_default": ".test_is_ws_connected_false_by_default()" | kind=code-symbol | source=probe/tests/test_transport.py:L508 | neighbors=[TestWebSocket] | lang=en
- "tests_test_transport_testwebsocket_test_ws_requires_token": ".test_ws_requires_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L526 | neighbors=[TestWebSocket] | lang=en
- "tests_test_transport_testwebsocket_test_ws_url_http": ".test_ws_url_http()" | kind=code-symbol | source=probe/tests/test_transport.py:L512 | neighbors=[TestWebSocket] | lang=en
- "tests_test_transport_testwebsocket_test_ws_url_https": ".test_ws_url_https()" | kind=code-symbol | source=probe/tests/test_transport.py:L519 | neighbors=[TestWebSocket] | lang=en
- "tests_test_udp_amplifiers_test_dns_open_recursion": "test_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L18 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_memcached_exposed": "test_memcached_exposed()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L26 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_ntp_monlist_absent": "test_ntp_monlist_absent()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L13 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_ntp_monlist_enabled": "test_ntp_monlist_enabled()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L8 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_probe_builders_are_bytes": "test_probe_builders_are_bytes()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L31 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_use_cases_rationale_1": "Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only" | kind=entity | source=probe/tests/test_use_cases.py:L1 | neighbors=[test_use_cases.py] | lang=pt
- "tests_test_use_cases_test_descriptions_do_not_overclaim": "test_descriptions_do_not_overclaim()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L16 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_iot_survey_collects_banners": "test_iot_survey_collects_banners()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L36 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_udp_claims_amplification": "test_udp_claims_amplification()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L27 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_web_claims_methods": "test_web_claims_methods()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L32 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_windows_estate_claims_signing": "test_windows_estate_claims_signing()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L23 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_validation_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_validation.py:L111 | neighbors=[FakeClient] | lang=en
- "tests_test_validation_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_validation.py:L115 | neighbors=[FakeClient] | lang=en
- "tests_test_validation_request_schema_test_validation_request_columns_and_defaults": "test_validation_request_columns_and_defaults()" | kind=code-symbol | source=manager/backend/tests/test_validation_request_schema.py:L8 | neighbors=[test_validation_request_schema.py] | lang=en
- "tests_test_validation_test_parser_accepts_validate_command": "test_parser_accepts_validate_command()" | kind=code-symbol | source=probe/tests/test_validation.py:L254 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_resolve_use_cases_deduplicates_combined_suites": "test_resolve_use_cases_deduplicates_combined_suites()" | kind=code-symbol | source=probe/tests/test_validation.py:L19 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_score_inventory_reports_precision_recall_and_unscored_dimensions": "test_score_inventory_reports_precision_recall_and_unscored_dimensions()" | kind=code-symbol | source=probe/tests/test_validation.py:L62 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_target_address_count_is_conservative": "test_target_address_count_is_conservative()" | kind=code-symbol | source=probe/tests/test_validation.py:L47 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts": "test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts()" | kind=code-symbol | source=probe/tests/test_validation.py:L51 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_validate_targets_enforces_scope_and_exclusions": "test_validate_targets_enforces_scope_and_exclusions()" | kind=code-symbol | source=probe/tests/test_validation.py:L32 | neighbors=[test_validation.py] | lang=en
- "tests_test_verification_core_test_authoritative_is_confirmed": "test_authoritative_is_confirmed()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L6 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_high_confidence_inferred_is_corroborated": "test_high_confidence_inferred_is_corroborated()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L14 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_kev_suspected_finding_needs_review": "test_kev_suspected_finding_needs_review()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L26 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_low_confidence_inferred_is_inferred": "test_low_confidence_inferred_is_inferred()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L20 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_core_test_missing_confidence_defaults_to_inferred_not_crash": "test_missing_confidence_defaults_to_inferred_not_crash()" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L33 | neighbors=[test_verification_core.py] | lang=en
- "tests_test_verification_graph_test_graph_available_is_boolean": "test_graph_available_is_boolean()" | kind=code-symbol | source=manager/backend/tests/test_verification_graph.py:L15 | neighbors=[test_verification_graph.py] | lang=en
- "tests_test_verification_graph_test_run_verification_matches_core_without_llm": "test_run_verification_matches_core_without_llm()" | kind=code-symbol | source=manager/backend/tests/test_verification_graph.py:L9 | neighbors=[test_verification_graph.py] | lang=en
- "tests_test_verification_llm_test_llm_can_flag_false_positive_and_lower": "test_llm_can_flag_false_positive_and_lower()" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L30 | neighbors=[test_verification_llm.py] | lang=en
- "tests_test_verification_llm_test_llm_error_falls_back_to_deterministic": "test_llm_error_falls_back_to_deterministic()" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L19 | neighbors=[test_verification_llm.py] | lang=en
- "tests_test_verification_llm_test_no_llm_matches_deterministic": "test_no_llm_matches_deterministic()" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L11 | neighbors=[test_verification_llm.py] | lang=en
- "tests_test_version_compare_rationale_1": "Cross-validates the pure-Python Debian version comparator against the real `dpkg" | kind=entity | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[test_version_compare.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-134.json

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
