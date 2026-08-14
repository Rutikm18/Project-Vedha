# Node Description Batch 94 of 186

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

- "tests_test_main_scripts_findings_test_findings_sorted_most_severe_first": "test_findings_sorted_most_severe_first()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L251 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_missing_security_headers_is_low": "test_missing_security_headers_is_low()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L222 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_no_finding_carries_a_cve_id": "test_no_finding_carries_a_cve_id()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L259 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed": "test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L183 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_rdp_exposed_medium": "test_rdp_exposed_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L140 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_server_version_disclosure_is_info": "test_server_version_disclosure_is_info()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L216 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_smbv1_enabled_is_high": "test_smbv1_enabled_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L63 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_default_community_is_high": "test_snmp_default_community_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L84 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_nondefault_community_is_medium": "test_snmp_nondefault_community_is_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L91 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_summarize_counts_by_severity_and_actionable": "test_summarize_counts_by_severity_and_actionable()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L273 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_telnet_is_high_cleartext": "test_telnet_is_high_cleartext()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L127 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_obsolete_protocol_is_high": "test_tls_obsolete_protocol_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L24 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_weak_cipher_is_high_with_reasons": "test_tls_weak_cipher_is_high_with_reasons()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L47 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_x_powered_by_disclosure_is_info": "test_x_powered_by_disclosure_is_info()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L238 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_hardening_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L32 | neighbors=[test_main_scripts_hardening.py, ._scanner()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_error_response_not_trusted": ".test_error_response_not_trusted()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L132 | neighbors=[TestSmbParsing, make_smb2_error()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_success_response_signing_and_dialect": ".test_success_response_signing_and_dialect()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L139 | neighbors=[TestSmbParsing, make_smb2_success()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_success_signing_supported_not_required": ".test_success_signing_supported_not_required()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L147 | neighbors=[TestSmbParsing, make_smb2_success()]
- "tests_test_main_scripts_ja4x_fake_cert": "_fake_cert()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L52 | neighbors=[test_main_scripts_ja4x.py, test_ja4x_from_cert_matches_pure_core()]
- "tests_test_main_scripts_ja4x_test_ja4x_from_cert_matches_pure_core": "test_ja4x_from_cert_matches_pure_core()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L59 | neighbors=[test_main_scripts_ja4x.py, _fake_cert()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_ambiguous_when_only_open_filtered": ".test_ambiguous_when_only_open_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L44 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_auto_detects_external_by_name": ".test_auto_detects_external_by_name()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L63 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_explicit_external_vantage_by_name_override": ".test_explicit_external_vantage_by_name_override()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L56 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_external_exposure_is_flagged": ".test_external_exposure_is_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L17 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_internal_only_not_called_external": ".test_internal_only_not_called_external()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L26 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_not_exposed_everywhere": ".test_not_exposed_everywhere()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L39 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_vantages_are_not_collapsed": ".test_vantages_are_not_collapsed()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L49 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_manager_ai_test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter": "test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L247 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_default_auto_detects_the_configured_cloud_provider": "test_default_auto_detects_the_configured_cloud_provider()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L240 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_default_runtime_fails_closed_without_any_cloud_key": "test_default_runtime_fails_closed_without_any_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L254 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_fallback_never_includes_local_ollama": "test_fallback_never_includes_local_ollama()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L271 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_generate_fails_closed_when_no_cloud_provider_configured": "test_generate_fails_closed_when_no_cloud_provider_configured()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L262 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_status_fails_safe_without_cloud_key": "test_status_fails_safe_without_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L283 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manual_reopen": "test_manual_reopen.py" | kind=code-symbol | source=manager/backend/tests/test_manual_reopen.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, test_manual_reopen_restores_open_and_au…]
- "tests_test_nessus_scanner_test_create_scan": "test_create_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L48 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_create_scan_with_credentials": "test_create_scan_with_credentials()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L65 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_launch_scan": "test_launch_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L85 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_completed": "test_poll_status_completed()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L114 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_running": "test_poll_status_running()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L99 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_skips_invalid_json": ".test_load_jsonl_skips_invalid_json()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L499 | neighbors=[TestDeltaEngine, _make_scan_record()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-093.json

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
