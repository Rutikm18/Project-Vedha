# Node Description Batch 156 of 332

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

- "tests_test_main_scripts_rdp_test_negotiation_failure": "test_negotiation_failure()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L90 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_nla_required_rdp_is_low_severity_no_bluekeep_language": "test_nla_required_rdp_is_low_severity_no_bluekeep_language()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L157 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_nla_when_hybrid_selected": "test_nla_when_hybrid_selected()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L34 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_standard_rdp_security_no_nla": "test_standard_rdp_security_no_nla()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L85 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_tls_only_is_not_nla": "test_tls_only_is_not_nla()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L40 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_unauth_test_protected_redis_raises_no_unauth_finding": "test_protected_redis_raises_no_unauth_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L71 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_unauth_test_unauth_elasticsearch_is_high": "test_unauth_elasticsearch_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L63 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_unauth_test_unauth_redis_is_critical_and_rce_flagged": "test_unauth_redis_is_critical_and_rce_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L55 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_ambiguous_when_only_open_filtered": ".test_ambiguous_when_only_open_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L44 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_auto_detects_external_by_name": ".test_auto_detects_external_by_name()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L63 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_explicit_external_vantage_by_name_override": ".test_explicit_external_vantage_by_name_override()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L56 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_external_exposure_is_flagged": ".test_external_exposure_is_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L17 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_internal_only_not_called_external": ".test_internal_only_not_called_external()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L26 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_not_exposed_everywhere": ".test_not_exposed_everywhere()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L39 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_vantages_are_not_collapsed": ".test_vantages_are_not_collapsed()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L49 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_manager_ai_test_advisor_flow_prompt_grounds_lifecycle_facts": "test_advisor_flow_prompt_grounds_lifecycle_facts()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L231 | neighbors=[test_manager_ai.py, The advisor_flow rules instruct the mod…]
- "tests_test_manager_ai_test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter": "test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L313 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_default_auto_detects_the_configured_cloud_provider": "test_default_auto_detects_the_configured_cloud_provider()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L306 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_default_runtime_fails_closed_without_any_cloud_key": "test_default_runtime_fails_closed_without_any_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L320 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_fallback_never_includes_local_ollama": "test_fallback_never_includes_local_ollama()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L337 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_generate_fails_closed_when_no_cloud_provider_configured": "test_generate_fails_closed_when_no_cloud_provider_configured()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L328 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_status_fails_safe_without_cloud_key": "test_status_fails_safe_without_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L349 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manual_reopen": "test_manual_reopen.py" | kind=code-symbol | source=manager/backend/tests/test_manual_reopen.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, test_manual_reopen_restores_open_and_au…]
- "tests_test_msrpc_scanner_testmsrpcfindings_test_endpoints_low": ".test_endpoints_low()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L86 | neighbors=[TestMSRPCFindings, ._fact()]
- "tests_test_msrpc_scanner_testmsrpcfindings_test_zero_endpoints_silent": ".test_zero_endpoints_silent()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L92 | neighbors=[TestMSRPCFindings, ._fact()]
- "tests_test_msrpc_scanner_testmsrpcscanner_test_impacket_missing_is_error": ".test_impacket_missing_is_error()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L74 | neighbors=[TestMSRPCScanner, ._sc()]
- "tests_test_msrpc_scanner_testmsrpcscanner_test_no_msrpc_filtered": ".test_no_msrpc_filtered()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L69 | neighbors=[TestMSRPCScanner, ._sc()]
- "tests_test_msrpc_scanner_testmsrpcscanner_test_open": ".test_open()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L61 | neighbors=[TestMSRPCScanner, ._sc()]
- "tests_test_msrpc_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L97 | neighbors=[test_msrpc_scanner.py, .test_main_scripts()]
- "tests_test_msrpc_scanner_testsummarize": "TestSummarize" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L18 | neighbors=[test_msrpc_scanner.py, .test_distinct_interfaces_and_named()]
- "tests_test_nessus_scanner_test_create_scan": "test_create_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L48 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_create_scan_with_credentials": "test_create_scan_with_credentials()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L65 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_launch_scan": "test_launch_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L85 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_completed": "test_poll_status_completed()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L114 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_running": "test_poll_status_running()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L99 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_network_va_accuracy_listener_loop": "._loop()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L48 | neighbors=[_Listener, .start()]
- "tests_test_network_va_accuracy_listener_stop": ".stop()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L72 | neighbors=[_Listener, va_scan()]
- "tests_test_network_va_accuracy_test_every_planted_risk_port_is_found": "test_every_planted_risk_port_is_found()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L119 | neighbors=[test_network_va_accuracy.py, The regression this guards: these ports…]
- "tests_test_network_va_accuracy_test_irc_is_identified_by_protocol_not_port": "test_irc_is_identified_by_protocol_not_port()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L140 | neighbors=[test_network_va_accuracy.py, Positive protocol evidence turns the bo…]
- "tests_test_network_va_accuracy_test_no_branch_runs_without_evidence": "test_no_branch_runs_without_evidence()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L168 | neighbors=[test_network_va_accuracy.py, Every deep branch that ran must have pr…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-155.json

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
