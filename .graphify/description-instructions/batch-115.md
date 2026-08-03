# Node Description Batch 116 of 131

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

- "tests_test_nuclei_background_nestedtransaction_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L23 | neighbors=[_NestedTransaction]
- "tests_test_nuclei_background_nestedtransaction_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L26 | neighbors=[_NestedTransaction]
- "tests_test_nuclei_background_scalarresult_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L15 | neighbors=[_ScalarResult]
- "tests_test_nuclei_background_scalarresult_scalar_one_or_none": ".scalar_one_or_none()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L18 | neighbors=[_ScalarResult]
- "tests_test_nuclei_background_sessionfactory_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L60 | neighbors=[_SessionFactory]
- "tests_test_nuclei_scanner_fakeprocess_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L31 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_kill": ".kill()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L61 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_terminate": ".terminate()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L57 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_wait": ".wait()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L50 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_test_missing_binary_is_a_reported_failure": "test_missing_binary_is_a_reported_failure()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L95 | neighbors=[test_nuclei_scanner.py]
- "tests_test_passive_collector_socket_fileno": ".fileno()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L28 | neighbors=[_Socket]
- "tests_test_passive_collector_socket_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L24 | neighbors=[_Socket]
- "tests_test_passive_collector_test_zero_listeners_returns_structured_failure": "test_zero_listeners_returns_structured_failure()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L135 | neighbors=[test_passive_collector.py]
- "tests_test_passive_collector_writer_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L16 | neighbors=[_Writer]
- "tests_test_passive_collector_writer_write": ".write()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L19 | neighbors=[_Writer]
- "tests_test_pat_auth_test_new_pat_token_shape_and_hash_stability": "test_new_pat_token_shape_and_hash_stability()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L44 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_builder_rejects_unknown_scope": "test_pat_builder_rejects_unknown_scope()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L88 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_builder_returns_token_once_and_stores_hash_only": "test_pat_builder_returns_token_once_and_stores_hash_only()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L52 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_builder_supports_non_expiring_tokens_only_when_requested": "test_pat_builder_supports_non_expiring_tokens_only_when_requested()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L74 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_scope_allows_probe_cli_paths": "test_pat_scope_allows_probe_cli_paths()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L16 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_scope_matrix_for_api_scopes": "test_pat_scope_matrix_for_api_scopes()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L27 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_validate_pat_scopes_dedupes_and_rejects_unknown": "test_validate_pat_scopes_dedupes_and_rejects_unknown()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L35 | neighbors=[test_pat_auth.py]
- "tests_test_port_catalog_test_modern_infra_ports_present": "test_modern_infra_ports_present()" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L4 | neighbors=[test_port_catalog.py]
- "tests_test_probe_core_rationale_1": "Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG" | kind=entity | source=probe/tests/test_probe_core.py:L1 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_test_explicit_local_manager_urls": "test_explicit_local_manager_urls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L47 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_test_nonlocal_manager_urls": "test_nonlocal_manager_urls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L57 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_testcapabilities_test_capabilities_sorted": ".test_capabilities_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L894 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testcapabilities_test_known_scan_types": ".test_known_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L897 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testclamp_test_bad_value_uses_default": ".test_bad_value_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L840 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_high": ".test_clamped_high()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L834 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_low": ".test_clamped_low()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L837 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_in_range": ".test_in_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L831 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_none_uses_default": ".test_none_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L843 | neighbors=[TestClamp]
- "tests_test_probe_core_testengagementmodes_test_assessment": ".test_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L451 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_re_scan": ".test_re_scan()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L464 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_invalid_raises": ".test_service_specific_invalid_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L460 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_valid": ".test_service_specific_valid()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L456 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_triage": ".test_triage()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L445 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testenginesummary_test_affirmative_fact_creates_one_deduplicated_host": ".test_affirmative_fact_creates_one_deduplicated_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L672 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_negative_or_ambiguous_facts_do_not_create_hosts": ".test_negative_or_ambiguous_facts_do_not_create_hosts()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L646 | neighbors=[TestEngineSummary]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-115.json

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
