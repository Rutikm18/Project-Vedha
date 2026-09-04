# Node Description Batch 151 of 332

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

- "tests_test_detection_validation_testdetectioncorrelator_test_detected_when_edr_not_blocking": ".test_detected_when_edr_not_blocking()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L69 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_gap_report_ignores_detected": ".test_gap_report_ignores_detected()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L162 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_generate_gap_report": ".test_generate_gap_report()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L153 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_host_match_by_ip": ".test_host_match_by_ip()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L107 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_hostname_substring_collision_is_not_correlated": ".test_hostname_substring_collision_is_not_correlated()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L92 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_ip_prefix_collision_is_not_correlated": ".test_ip_prefix_collision_is_not_correlated()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L97 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_missed_when_nothing": ".test_missed_when_nothing()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L75 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_mixed_results_are_partial_not_covered": ".test_mixed_results_are_partial_not_covered()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L136 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_out_of_window_is_missed": ".test_out_of_window_is_missed()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L80 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_prevented_by_edr": ".test_prevented_by_edr()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L62 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_short_hostname_matches_its_fqdn": ".test_short_hostname_matches_its_fqdn()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L102 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_wrong_host_is_missed": ".test_wrong_host_is_missed()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L86 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_dns_scanner_testdnsfindings_test_dnssec_absent_only_for_confirmed_zone": ".test_dnssec_absent_only_for_confirmed_zone()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L143 | neighbors=[TestDNSFindings, ._fact()]
- "tests_test_dns_scanner_testdnsfindings_test_secure_server_silent": ".test_secure_server_silent()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L151 | neighbors=[TestDNSFindings, ._fact()]
- "tests_test_dns_scanner_testdnsfindings_test_zone_transfer_version_and_unsigned": ".test_zone_transfer_version_and_unsigned()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L130 | neighbors=[TestDNSFindings, ._fact()]
- "tests_test_dns_scanner_testdnsscanner_test_dnspython_missing_is_error": ".test_dnspython_missing_is_error()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L116 | neighbors=[TestDNSScanner, ._sc()]
- "tests_test_dns_scanner_testdnsscanner_test_no_dns_is_filtered": ".test_no_dns_is_filtered()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L111 | neighbors=[TestDNSScanner, ._sc()]
- "tests_test_dns_scanner_testdnsscanner_test_zone_transfer_open": ".test_zone_transfer_open()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L102 | neighbors=[TestDNSScanner, ._sc()]
- "tests_test_dns_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L158 | neighbors=[test_dns_scanner.py, .test_scanner_and_findings_in_main_scri…]
- "tests_test_dualstack_fallback_testosfingerprintsmbbuildfallback": "TestOsFingerprintSmbBuildFallback" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L118 | neighbors=[test_dualstack_fallback.py, .test_falls_back_across_families()]
- "tests_test_dualstack_fallback_testsmbnegotiatefallback_test_returns_none_only_when_every_family_fails": ".test_returns_none_only_when_every_family_fails()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L78 | neighbors=[TestSmbNegotiateFallback, ._patch_candidates()]
- "tests_test_dualstack_fallback_testsynscannerrequestsipv4": "TestSynScannerRequestsIPv4" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L201 | neighbors=[test_dualstack_fallback.py, .test_resolve_is_asked_for_ipv4()]
- "tests_test_e2e_engagement_to_findings_plant": "_plant()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L36 | neighbors=[test_e2e_engagement_to_findings.py, test_real_scan_of_open_datastore_yields…]
- "tests_test_e2e_engagement_to_findings_test_correlated_findings_cite_their_base_findings": "test_correlated_findings_cite_their_base_findings()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L161 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_engagement_dispatch_reaches_probe_and_enforces_scope": "test_engagement_dispatch_reaches_probe_and_enforces_scope()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L67 | neighbors=[test_e2e_engagement_to_findings.py, _manager()]
- "tests_test_e2e_engagement_to_findings_test_manager_correlation_finds_all_three_attack_paths": "test_manager_correlation_finds_all_three_attack_paths()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L148 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise": "test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L169 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_out_of_scope_target_is_refused_end_to_end": "test_out_of_scope_target_is_refused_end_to_end()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L88 | neighbors=[test_e2e_engagement_to_findings.py, _manager()]
- "tests_test_engine_bridge_ingest_health_test_census_survives_an_engine_that_returns_no_ingest_result": "test_census_survives_an_engine_that_returns_no_ingest_result()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L84 | neighbors=[test_engine_bridge_ingest_health.py, The census is best-effort by contract: …]
- "tests_test_engine_bridge_ingest_health_test_healthy_facts_ingest_completely_and_detect": "test_healthy_facts_ingest_completely_and_detect()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L43 | neighbors=[test_engine_bridge_ingest_health.py, Baseline: the shape the agent actually …]
- "tests_test_engine_bridge_ingest_health_test_partial_drift_still_detects_but_reports_the_loss": "test_partial_drift_still_detects_but_reports_the_loss()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L72 | neighbors=[test_engine_bridge_ingest_health.py, A partly-bad batch must keep its good f…]
- "tests_test_engine_bridge_ingest_health_test_total_shape_drift_is_reported_not_silently_zero": "test_total_shape_drift_is_reported_not_silently_zero()" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L55 | neighbors=[test_engine_bridge_ingest_health.py, The regression. Drop the one field an a…]
- "tests_test_engine_bridge_regression": "test_engine_bridge_regression.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_regression.py:L1 | neighbors=[937737b feat(resolution): reopen + flag…, test_reopen_flips_remediated_to_open_an…]
- "tests_test_engine_bridge_verification": "test_engine_bridge_verification.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_verification.py:L1 | neighbors=[2fcec73 feat(verification): stamp verdi…, test_stamp_verification_sets_columns_wh…]
- "tests_test_exploit_engine_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L49 | neighbors=[test_exploit_engine.py, .test_validate_scope_out_of_range()]
- "tests_test_exploit_engine_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L464 | neighbors=[test_exploit_engine.py, Register --msf-host CLI option for inte…]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_format": ".test_generate_dns_callback_token_format()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L290 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_unique": ".test_generate_dns_callback_token_unique()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L298 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_safety_meterpreter_raises": ".test_validate_safety_meterpreter_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L275 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_get_job_status_running": ".test_get_job_status_running()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L218 | neighbors=[TestMetasploitRPCClient, ._make_client()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-150.json

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
