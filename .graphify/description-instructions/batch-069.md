# Node Description Batch 70 of 131

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

- "tests_test_probe_core_testgate2_test_ot_always_false": ".test_ot_always_false()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L289 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate2_test_recently_seen_alive": ".test_recently_seen_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L281 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate2_test_stale_seen_alive": ".test_stale_seen_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L285 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate3_test_not_alive": ".test_not_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L299 | neighbors=[TestGate3, _asset()]
- "tests_test_probe_core_testgate3_test_ot_always_false": ".test_ot_always_false()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L303 | neighbors=[TestGate3, _asset()]
- "tests_test_probe_core_testgate3_test_requires_alive": ".test_requires_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L295 | neighbors=[TestGate3, _asset()]
- "tests_test_probe_core_testgate4_test_all_closed": ".test_all_closed()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L317 | neighbors=[TestGate4, _asset()]
- "tests_test_probe_core_testgate4_test_no_open_ports": ".test_no_open_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L313 | neighbors=[TestGate4, _asset()]
- "tests_test_probe_core_testgate4_test_with_open_ports": ".test_with_open_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L309 | neighbors=[TestGate4, _asset()]
- "tests_test_probe_core_testgate5_test_dynamically_routed_overrides_port": ".test_dynamically_routed_overrides_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L343 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_explicit_snmp_does_not_require_tcp_liveness": ".test_explicit_snmp_does_not_require_tcp_liveness()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L359 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_iot_profile_no_smb": ".test_iot_profile_no_smb()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L327 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_it_profile_tls_with_tls_port": ".test_it_profile_tls_with_tls_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L323 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_mcp_ai_allowed_on_it_ai_port": ".test_mcp_ai_allowed_on_it_ai_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L351 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_no_matching_ports": ".test_no_matching_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L347 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_ot_no_branches": ".test_ot_no_branches()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L331 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_service_filter_allows": ".test_service_filter_allows()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L339 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_service_filter_blocks": ".test_service_filter_blocks()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L335 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_snmp_allowed_on_live_it_host": ".test_snmp_allowed_on_live_it_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L355 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_snmp_not_allowed_on_iot_profile": ".test_snmp_not_allowed_on_iot_profile()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L363 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate6_test_already_collected": ".test_already_collected()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L377 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_no_creds": ".test_no_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L369 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_not_alive": ".test_not_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L381 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_ssh_creds_alive_uncollected": ".test_ssh_creds_alive_uncollected()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L373 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testroutebranches_test_http_banner_routes_web": ".test_http_banner_routes_web()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L420 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testroutebranches_test_no_banners_no_routing": ".test_no_banners_no_routing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L434 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testroutebranches_test_silent_nonstandard_port_routes_tls": ".test_silent_nonstandard_port_routes_tls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L427 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testscanresult_test_to_json_roundtrip": ".test_to_json_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L228 | neighbors=[TestScanResult, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_all_entries_for_host": ".test_all_entries_for_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L782 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_put_get": ".test_put_get()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L746 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_save_and_load_roundtrip": ".test_save_and_load_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L790 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_deterministic_fresh": ".test_should_recheck_deterministic_fresh()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L768 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_force_expired": ".test_should_recheck_force_expired()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L774 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_uncertain_always": ".test_should_recheck_uncertain_always()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L762 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_enrollment_test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses": "test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L102 | neighbors=[test_probe_enrollment.py, _token()]
- "tests_test_probe_enrollment_token": "_token()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L85 | neighbors=[test_probe_enrollment.py, test_enroll_token_usable_only_while_liv…]
- "tests_test_reaper_test_expired_attempt_fails_job_when_retry_budget_is_exhausted": "test_expired_attempt_fails_job_when_retry_budget_is_exhausted()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L39 | neighbors=[test_reaper.py, _objects()]
- "tests_test_reaper_test_expired_attempt_requeues_with_fence_history_preserved": "test_expired_attempt_requeues_with_fence_history_preserved()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L24 | neighbors=[test_reaper.py, _objects()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_multiple_encrypts_different": ".test_multiple_encrypts_different()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L78 | neighbors=[Each encryption uses a fresh ephemeral …, TestEncryptDecryptRoundtrip]
- "tests_test_seed_admin_testdatabaseunavailable": "TestDatabaseUnavailable" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L288 | neighbors=[test_seed_admin.py, .test_retries_then_raises_database_unav…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-069.json

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
