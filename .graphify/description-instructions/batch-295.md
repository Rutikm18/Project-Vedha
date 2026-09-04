# Node Description Batch 296 of 330

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_probe_core_testcapabilities_test_capabilities_sorted": ".test_capabilities_sorted()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L931 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testcapabilities_test_known_scan_types": ".test_known_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L934 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testclamp_test_bad_value_uses_default": ".test_bad_value_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L877 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_high": ".test_clamped_high()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L871 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_low": ".test_clamped_low()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L874 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_in_range": ".test_in_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L868 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_none_uses_default": ".test_none_uses_default()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L880 | neighbors=[TestClamp]
- "tests_test_probe_core_testengagementmodes_test_assessment": ".test_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L451 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_re_scan": ".test_re_scan()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L464 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_invalid_raises": ".test_service_specific_invalid_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L460 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_valid": ".test_service_specific_valid()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L456 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_triage": ".test_triage()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L445 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testenginesummary_test_affirmative_fact_creates_one_deduplicated_host": ".test_affirmative_fact_creates_one_deduplicated_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L709 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_negative_or_ambiguous_facts_do_not_create_hosts": ".test_negative_or_ambiguous_facts_do_not_create_hosts()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L646 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_open_port_count_deduplicates_confirming_scanners": ".test_open_port_count_deduplicates_confirming_scanners()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L613 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_open_port_count_excludes_host_liveness": ".test_open_port_count_excludes_host_liveness()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L605 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_run_scoped_summary_with_interface_target_is_also_excluded": ".test_run_scoped_summary_with_interface_target_is_also_excluded()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L698 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testexpandtargets_test_cidr_24": ".test_cidr_24()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L149 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_dedup": ".test_dedup()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L166 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_empty_input": ".test_empty_input()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L178 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_hostname_passthrough": ".test_hostname_passthrough()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L155 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_range": ".test_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L158 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_range_reversed_raises": ".test_range_reversed_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L162 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_safety_cap_cidr": ".test_safety_cap_cidr()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L170 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_safety_cap_range": ".test_safety_cap_range()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L174 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_single_ip": ".test_single_ip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L146 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_whitespace_entries": ".test_whitespace_entries()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L181 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testgate0_test_iot_not_passive": ".test_iot_not_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L272 | neighbors=[TestGate0]
- "tests_test_probe_core_testgate0_test_it_not_passive": ".test_it_not_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L269 | neighbors=[TestGate0]
- "tests_test_probe_core_testgate0_test_ot_is_passive": ".test_ot_is_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L266 | neighbors=[TestGate0]
- "tests_test_probe_core_testlookslikehttp_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L400 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_http_1_1": ".test_http_1_1()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L391 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_http_2": ".test_http_2()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L394 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlookslikehttp_test_not_http": ".test_not_http()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L397 | neighbors=[TestLooksLikeHttp]
- "tests_test_probe_core_testlooksliketls_test_banner_present": ".test_banner_present()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L415 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_client_first_port_not_tls": ".test_client_first_port_not_tls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L409 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_no_banner_attempt": ".test_no_banner_attempt()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L412 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testlooksliketls_test_silent_non_client_first_port": ".test_silent_non_client_first_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L406 | neighbors=[TestLooksLikeTls]
- "tests_test_probe_core_testparseports_test_bad_token_raises": ".test_bad_token_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L214 | neighbors=[TestParsePorts]
- "tests_test_probe_core_testparseports_test_comma_separated": ".test_comma_separated()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L193 | neighbors=[TestParsePorts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-295.json

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
