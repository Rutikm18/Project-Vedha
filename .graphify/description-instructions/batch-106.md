# Node Description Batch 107 of 119

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

- "tests_test_port_catalog_test_modern_infra_ports_present": "test_modern_infra_ports_present()" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L4 | neighbors=[test_port_catalog.py]
- "tests_test_probe_core_rationale_1": "Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG" | kind=entity | source=probe/tests/test_probe_core.py:L1 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_testcapabilities_test_capabilities_sorted": ".test_capabilities_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L872 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testcapabilities_test_known_scan_types": ".test_known_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L875 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testclamp_test_bad_value_uses_default": ".test_bad_value_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L818 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_high": ".test_clamped_high()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L812 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_low": ".test_clamped_low()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L815 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_in_range": ".test_in_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L809 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_none_uses_default": ".test_none_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L821 | neighbors=[TestClamp]
- "tests_test_probe_core_testengagementmodes_test_assessment": ".test_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L429 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_re_scan": ".test_re_scan()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L442 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_invalid_raises": ".test_service_specific_invalid_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L438 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_valid": ".test_service_specific_valid()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L434 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_triage": ".test_triage()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L423 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testenginesummary_test_affirmative_fact_creates_one_deduplicated_host": ".test_affirmative_fact_creates_one_deduplicated_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L650 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_negative_or_ambiguous_facts_do_not_create_hosts": ".test_negative_or_ambiguous_facts_do_not_create_hosts()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L624 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_open_port_count_deduplicates_confirming_scanners": ".test_open_port_count_deduplicates_confirming_scanners()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L591 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_open_port_count_excludes_host_liveness": ".test_open_port_count_excludes_host_liveness()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L583 | neighbors=[TestEngineSummary]
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
- "tests_test_probe_core_testgate0_test_it_not_passive": ".test_it_not_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[TestGate0]
- "tests_test_probe_core_testgate0_test_ot_is_passive": ".test_ot_is_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L244 | neighbors=[TestGate0]
- "tests_test_probe_core_testlookslikehttp_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L378 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_http_1_1": ".test_http_1_1()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L369 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_http_2": ".test_http_2()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L372 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_not_http": ".test_not_http()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L375 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlooksliketls_test_banner_present": ".test_banner_present()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L393 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_client_first_port_not_tls": ".test_client_first_port_not_tls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L387 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_no_banner_attempt": ".test_no_banner_attempt()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L390 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_silent_non_client_first_port": ".test_silent_non_client_first_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L384 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testparseports_test_bad_token_raises": ".test_bad_token_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L192 | neighbors=[TestParsePorts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-106.json

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
