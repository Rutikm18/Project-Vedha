# Node Description Batch 48 of 92

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

- "tests_test_probe_core_testgate5_test_dynamically_routed_overrides_port": ".test_dynamically_routed_overrides_port()" | kind=code-symbol | source=tests/test_probe_core.py:L343 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_explicit_snmp_does_not_require_tcp_liveness": ".test_explicit_snmp_does_not_require_tcp_liveness()" | kind=code-symbol | source=tests/test_probe_core.py:L359 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_iot_profile_no_smb": ".test_iot_profile_no_smb()" | kind=code-symbol | source=tests/test_probe_core.py:L327 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_it_profile_tls_with_tls_port": ".test_it_profile_tls_with_tls_port()" | kind=code-symbol | source=tests/test_probe_core.py:L323 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_mcp_ai_allowed_on_it_ai_port": ".test_mcp_ai_allowed_on_it_ai_port()" | kind=code-symbol | source=tests/test_probe_core.py:L351 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_no_matching_ports": ".test_no_matching_ports()" | kind=code-symbol | source=tests/test_probe_core.py:L347 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_ot_no_branches": ".test_ot_no_branches()" | kind=code-symbol | source=tests/test_probe_core.py:L331 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_service_filter_allows": ".test_service_filter_allows()" | kind=code-symbol | source=tests/test_probe_core.py:L339 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_service_filter_blocks": ".test_service_filter_blocks()" | kind=code-symbol | source=tests/test_probe_core.py:L335 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_snmp_allowed_on_live_it_host": ".test_snmp_allowed_on_live_it_host()" | kind=code-symbol | source=tests/test_probe_core.py:L355 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_snmp_not_allowed_on_iot_profile": ".test_snmp_not_allowed_on_iot_profile()" | kind=code-symbol | source=tests/test_probe_core.py:L363 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate6_test_already_collected": ".test_already_collected()" | kind=code-symbol | source=tests/test_probe_core.py:L377 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_no_creds": ".test_no_creds()" | kind=code-symbol | source=tests/test_probe_core.py:L369 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_not_alive": ".test_not_alive()" | kind=code-symbol | source=tests/test_probe_core.py:L381 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_ssh_creds_alive_uncollected": ".test_ssh_creds_alive_uncollected()" | kind=code-symbol | source=tests/test_probe_core.py:L373 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testroutebranches_test_http_banner_routes_web": ".test_http_banner_routes_web()" | kind=code-symbol | source=tests/test_probe_core.py:L420 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testroutebranches_test_no_banners_no_routing": ".test_no_banners_no_routing()" | kind=code-symbol | source=tests/test_probe_core.py:L434 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testroutebranches_test_silent_nonstandard_port_routes_tls": ".test_silent_nonstandard_port_routes_tls()" | kind=code-symbol | source=tests/test_probe_core.py:L427 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testscanresult_test_to_json_roundtrip": ".test_to_json_roundtrip()" | kind=code-symbol | source=tests/test_probe_core.py:L228 | neighbors=[TestScanResult, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_all_entries_for_host": ".test_all_entries_for_host()" | kind=code-symbol | source=tests/test_probe_core.py:L782 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_put_get": ".test_put_get()" | kind=code-symbol | source=tests/test_probe_core.py:L746 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_save_and_load_roundtrip": ".test_save_and_load_roundtrip()" | kind=code-symbol | source=tests/test_probe_core.py:L790 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_deterministic_fresh": ".test_should_recheck_deterministic_fresh()" | kind=code-symbol | source=tests/test_probe_core.py:L768 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_force_expired": ".test_should_recheck_force_expired()" | kind=code-symbol | source=tests/test_probe_core.py:L774 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_uncertain_always": ".test_should_recheck_uncertain_always()" | kind=code-symbol | source=tests/test_probe_core.py:L762 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_manifest_test_manifest_is_clean_parseable_json": "test_manifest_is_clean_parseable_json()" | kind=code-symbol | source=tests/test_probe_manifest.py:L30 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_manifest_test_manifest_is_deterministic": "test_manifest_is_deterministic()" | kind=code-symbol | source=tests/test_probe_manifest.py:L47 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_manifest_test_manifest_surfaces_the_capability_contract": "test_manifest_surfaces_the_capability_contract()" | kind=code-symbol | source=tests/test_probe_manifest.py:L37 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_next_features_test_device_inventory_post_stage_classifies_from_open_ports": "test_device_inventory_post_stage_classifies_from_open_ports()" | kind=code-symbol | source=tests/test_probe_next_features.py:L110 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_device_inventory_skips_hosts_without_evidence": "test_device_inventory_skips_hosts_without_evidence()" | kind=code-symbol | source=tests/test_probe_next_features.py:L124 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_exposure_matrix_flags_internet_reachable_ports": "test_exposure_matrix_flags_internet_reachable_ports()" | kind=code-symbol | source=tests/test_probe_next_features.py:L135 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_exposure_matrix_internal_only_from_lan_vantage": "test_exposure_matrix_internal_only_from_lan_vantage()" | kind=code-symbol | source=tests/test_probe_next_features.py:L150 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_no_post_stage_for_ordinary_scan_types": "test_no_post_stage_for_ordinary_scan_types()" | kind=code-symbol | source=tests/test_probe_next_features.py:L161 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_resolve_testresolvefamily_test_default_no_family_is_backward_compatible": ".test_default_no_family_is_backward_compatible()" | kind=code-symbol | source=tests/test_resolve.py:L34 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_family_absent_falls_back_to_first": ".test_requested_family_absent_falls_back_to_first()" | kind=code-symbol | source=tests/test_resolve.py:L28 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_ipv4_selected_over_v6_first": ".test_requested_ipv4_selected_over_v6_first()" | kind=code-symbol | source=tests/test_resolve.py:L21 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_result_spool_spool": "spool()" | kind=code-symbol | source=tests/test_result_spool.py:L13 | neighbors=[test_result_spool.py, ResultSpool with tiny retry delay for f…]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_constructs_and_wires_real_scanners": ".test_constructs_and_wires_real_scanners()" | kind=code-symbol | source=tests/test_scan_funnel.py:L191 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_port_scanner_is_syn_scanner": ".test_port_scanner_is_syn_scanner()" | kind=code-symbol | source=tests/test_scan_funnel.py:L201 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_invoked_with_db_port": ".test_db_scanner_invoked_with_db_port()" | kind=code-symbol | source=tests/test_scan_funnel.py:L154 | neighbors=[TestScanFunnel, _make_funnel()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-047.json

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
