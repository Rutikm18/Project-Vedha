# Node Description Batch 78 of 92

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

- "tests_test_os_fingerprint_testttlinference_test_round_up_to_128": ".test_round_up_to_128()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L197 | neighbors=[TestTtlInference]
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_255": ".test_round_up_to_255()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L201 | neighbors=[TestTtlInference]
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_64": ".test_round_up_to_64()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L193 | neighbors=[TestTtlInference]
- "tests_test_passive_collector_socket_fileno": ".fileno()" | kind=code-symbol | source=tests/test_passive_collector.py:L28 | neighbors=[_Socket]
- "tests_test_passive_collector_socket_init": ".__init__()" | kind=code-symbol | source=tests/test_passive_collector.py:L24 | neighbors=[_Socket]
- "tests_test_passive_collector_test_zero_listeners_returns_structured_failure": "test_zero_listeners_returns_structured_failure()" | kind=code-symbol | source=tests/test_passive_collector.py:L135 | neighbors=[test_passive_collector.py]
- "tests_test_passive_collector_writer_init": ".__init__()" | kind=code-symbol | source=tests/test_passive_collector.py:L16 | neighbors=[_Writer]
- "tests_test_passive_collector_writer_write": ".write()" | kind=code-symbol | source=tests/test_passive_collector.py:L19 | neighbors=[_Writer]
- "tests_test_port_catalog_test_modern_infra_ports_present": "test_modern_infra_ports_present()" | kind=code-symbol | source=tests/test_port_catalog.py:L4 | neighbors=[test_port_catalog.py]
- "tests_test_probe_core_rationale_1": "Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG" | kind=entity | source=tests/test_probe_core.py:L1 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_test_explicit_local_manager_urls": "test_explicit_local_manager_urls()" | kind=code-symbol | source=tests/test_probe_core.py:L47 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_test_nonlocal_manager_urls": "test_nonlocal_manager_urls()" | kind=code-symbol | source=tests/test_probe_core.py:L57 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_testcapabilities_test_capabilities_sorted": ".test_capabilities_sorted()" | kind=code-symbol | source=tests/test_probe_core.py:L894 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testcapabilities_test_known_scan_types": ".test_known_scan_types()" | kind=code-symbol | source=tests/test_probe_core.py:L897 | neighbors=[TestCapabilities]
- "tests_test_probe_core_testclamp_test_bad_value_uses_default": ".test_bad_value_uses_default()" | kind=code-symbol | source=tests/test_probe_core.py:L840 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_high": ".test_clamped_high()" | kind=code-symbol | source=tests/test_probe_core.py:L834 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_clamped_low": ".test_clamped_low()" | kind=code-symbol | source=tests/test_probe_core.py:L837 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_in_range": ".test_in_range()" | kind=code-symbol | source=tests/test_probe_core.py:L831 | neighbors=[TestClamp]
- "tests_test_probe_core_testclamp_test_none_uses_default": ".test_none_uses_default()" | kind=code-symbol | source=tests/test_probe_core.py:L843 | neighbors=[TestClamp]
- "tests_test_probe_core_testengagementmodes_test_assessment": ".test_assessment()" | kind=code-symbol | source=tests/test_probe_core.py:L451 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_re_scan": ".test_re_scan()" | kind=code-symbol | source=tests/test_probe_core.py:L464 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_invalid_raises": ".test_service_specific_invalid_raises()" | kind=code-symbol | source=tests/test_probe_core.py:L460 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_service_specific_valid": ".test_service_specific_valid()" | kind=code-symbol | source=tests/test_probe_core.py:L456 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testengagementmodes_test_triage": ".test_triage()" | kind=code-symbol | source=tests/test_probe_core.py:L445 | neighbors=[TestEngagementModes]
- "tests_test_probe_core_testenginesummary_test_affirmative_fact_creates_one_deduplicated_host": ".test_affirmative_fact_creates_one_deduplicated_host()" | kind=code-symbol | source=tests/test_probe_core.py:L672 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_negative_or_ambiguous_facts_do_not_create_hosts": ".test_negative_or_ambiguous_facts_do_not_create_hosts()" | kind=code-symbol | source=tests/test_probe_core.py:L646 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_open_port_count_deduplicates_confirming_scanners": ".test_open_port_count_deduplicates_confirming_scanners()" | kind=code-symbol | source=tests/test_probe_core.py:L613 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testenginesummary_test_open_port_count_excludes_host_liveness": ".test_open_port_count_excludes_host_liveness()" | kind=code-symbol | source=tests/test_probe_core.py:L605 | neighbors=[TestEngineSummary]
- "tests_test_probe_core_testexpandtargets_test_cidr_24": ".test_cidr_24()" | kind=code-symbol | source=tests/test_probe_core.py:L149 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_dedup": ".test_dedup()" | kind=code-symbol | source=tests/test_probe_core.py:L166 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_empty_input": ".test_empty_input()" | kind=code-symbol | source=tests/test_probe_core.py:L178 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_hostname_passthrough": ".test_hostname_passthrough()" | kind=code-symbol | source=tests/test_probe_core.py:L155 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_range": ".test_range()" | kind=code-symbol | source=tests/test_probe_core.py:L158 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_range_reversed_raises": ".test_range_reversed_raises()" | kind=code-symbol | source=tests/test_probe_core.py:L162 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_safety_cap_cidr": ".test_safety_cap_cidr()" | kind=code-symbol | source=tests/test_probe_core.py:L170 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_safety_cap_range": ".test_safety_cap_range()" | kind=code-symbol | source=tests/test_probe_core.py:L174 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_single_ip": ".test_single_ip()" | kind=code-symbol | source=tests/test_probe_core.py:L146 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testexpandtargets_test_whitespace_entries": ".test_whitespace_entries()" | kind=code-symbol | source=tests/test_probe_core.py:L181 | neighbors=[TestExpandTargets]
- "tests_test_probe_core_testgate0_test_iot_not_passive": ".test_iot_not_passive()" | kind=code-symbol | source=tests/test_probe_core.py:L272 | neighbors=[TestGate0]
- "tests_test_probe_core_testgate0_test_it_not_passive": ".test_it_not_passive()" | kind=code-symbol | source=tests/test_probe_core.py:L269 | neighbors=[TestGate0]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-077.json

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
