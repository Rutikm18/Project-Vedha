# Node Description Batch 95 of 104

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

- "tests_test_integration_testwebsocketmessageprotocol_test_hello_message": ".test_hello_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L276 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_job_push_message": ".test_job_push_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L280 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_result_message": ".test_result_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L294 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_nessus_scanner_scanner": "scanner()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L18 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_authenticate_api_key": "test_authenticate_api_key()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L37 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_critical": "test_map_finding_critical()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L129 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_info_severity": "test_map_finding_info_severity()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L163 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_no_cvss": "test_map_finding_no_cvss()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L170 | neighbors=[test_nessus_scanner.py]
- "tests_test_pat_auth_test_new_pat_token_shape_and_hash_stability": "test_new_pat_token_shape_and_hash_stability()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L44 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_builder_rejects_unknown_scope": "test_pat_builder_rejects_unknown_scope()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L88 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_builder_returns_token_once_and_stores_hash_only": "test_pat_builder_returns_token_once_and_stores_hash_only()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L52 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_builder_supports_non_expiring_tokens_only_when_requested": "test_pat_builder_supports_non_expiring_tokens_only_when_requested()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L74 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_scope_allows_probe_cli_paths": "test_pat_scope_allows_probe_cli_paths()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L16 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_pat_scope_matrix_for_api_scopes": "test_pat_scope_matrix_for_api_scopes()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L27 | neighbors=[test_pat_auth.py]
- "tests_test_pat_auth_test_validate_pat_scopes_dedupes_and_rejects_unknown": "test_validate_pat_scopes_dedupes_and_rejects_unknown()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L35 | neighbors=[test_pat_auth.py]
- "tests_test_probe_core_rationale_1": "Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG" | kind=entity | source=probe/tests/test_probe_core.py:L1 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_testcapabilities_test_capabilities_sorted": ".test_capabilities_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L780 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testcapabilities_test_known_scan_types": ".test_known_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L783 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testclamp_test_bad_value_uses_default": ".test_bad_value_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L726 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_high": ".test_clamped_high()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L720 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_low": ".test_clamped_low()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L723 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_in_range": ".test_in_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L717 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_none_uses_default": ".test_none_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L729 | neighbors=[TestClamp]
- "tests_test_probe_core_testengagementmodes_test_assessment": ".test_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L425 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_re_scan": ".test_re_scan()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L438 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_invalid_raises": ".test_service_specific_invalid_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L434 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_valid": ".test_service_specific_valid()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L430 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_triage": ".test_triage()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L419 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testenginesummary_test_open_port_count_excludes_host_liveness": ".test_open_port_count_excludes_host_liveness()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L579 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testexpandtargets_test_cidr_24": ".test_cidr_24()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L127 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_dedup": ".test_dedup()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L144 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_empty_input": ".test_empty_input()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L156 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_hostname_passthrough": ".test_hostname_passthrough()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L133 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_range": ".test_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L136 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_range_reversed_raises": ".test_range_reversed_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L140 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_safety_cap_cidr": ".test_safety_cap_cidr()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L148 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_safety_cap_range": ".test_safety_cap_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L152 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_single_ip": ".test_single_ip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L124 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_whitespace_entries": ".test_whitespace_entries()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L159 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testgate0_test_iot_not_passive": ".test_iot_not_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L250 | neighbors=[TestGate0]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-094.json

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
