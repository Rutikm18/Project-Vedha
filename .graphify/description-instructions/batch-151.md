# Node Description Batch 152 of 336

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

- "tests_test_detection_core_testvulndb_test_cvss_vector_index": ".test_cvss_vector_index()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L951 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_cvss_vector_missing": ".test_cvss_vector_missing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L959 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_known_products_sorted": ".test_known_products_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L963 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_lookup_existing": ".test_lookup_existing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L937 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_lookup_missing_returns_empty": ".test_lookup_missing_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L942 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_coverage_test_explain_no_run_says_never_ran": "test_explain_no_run_says_never_ran()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L144 | neighbors=[test_detection_coverage.py, _user()]
- "tests_test_detection_pipeline_gaps_test_enqueue_is_not_gated_on_success": "test_enqueue_is_not_gated_on_success()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L149 | neighbors=[test_detection_pipeline_gaps.py, Facts are persisted whenever they are p…]
- "tests_test_detection_pipeline_gaps_test_total_rejection_leaves_no_facts_for_correlation": "test_total_rejection_leaves_no_facts_for_correlation()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L78 | neighbors=[test_detection_pipeline_gaps.py, _fact()]
- "tests_test_detection_validation_testdetectioncorrelator_test_compute_coverage": ".test_compute_coverage()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L120 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_detected_by_siem": ".test_detected_by_siem()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L54 | neighbors=[TestDetectionCorrelator, _action()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-151.json

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
