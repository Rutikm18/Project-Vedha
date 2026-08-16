# Node Description Batch 75 of 209

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

- "tests_test_engagement_lists_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L13 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_by_cve": ".test_select_exploit_by_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L256 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_fallback_no_cve": ".test_select_exploit_fallback_no_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L269 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_log4shell": ".test_select_exploit_log4shell()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L263 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_scope_out_of_range": ".test_validate_scope_out_of_range()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L284 | neighbors=[TestExploitOrchestrator, _engagement(), ._make_orchestrator()]
- "tests_test_finding_reopen_endpoint_db_with": "_db_with()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L14 | neighbors=[test_finding_reopen_endpoint.py, test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_ope…]
- "tests_test_host_discovery_mobile_testlocallyadministered": "TestLocallyAdministered" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L32 | neighbors=[test_host_discovery_mobile.py, .test_globally_unique_macs(), .test_randomized_phone_macs()]
- "tests_test_host_discovery_mobile_testvendorlookup": "TestVendorLookup" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L44 | neighbors=[test_host_discovery_mobile.py, .test_known_oui(), .test_unknown_oui()]
- "tests_test_hw_bind_testgethwid": "TestGetHwId" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L11 | neighbors=[test_hw_bind.py, .test_deterministic_within_session(), .test_returns_32_hex_chars()]
- "tests_test_installer_contract_dry_run": "_dry_run()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L55 | neighbors=[test_installer_contract.py, test_installer_accepts_enroll_token_and…, test_installer_without_token_still_show…]
- "tests_test_loaders_testloadsnapshoterrors_test_content_hash_mismatch_raises_value_error": ".test_content_hash_mismatch_raises_value_error()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L65 | neighbors=[A snapshot whose records don't match th…, TestLoadSnapshotErrors, _valid_snapshot()]
- "tests_test_loaders_testloadsnapshoterrors_test_hash_mismatch_message_truncates_hash": ".test_hash_mismatch_message_truncates_hash()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L107 | neighbors=[The ValueError for a hash mismatch must…, TestLoadSnapshotErrors, _valid_snapshot()]
- "tests_test_loaders_testloadsnapshoterrors_test_valid_snapshot_loads_cleanly": ".test_valid_snapshot_loads_cleanly()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L93 | neighbors=[A well-formed snapshot must load withou…, TestLoadSnapshotErrors, _write_snapshot()]
- "tests_test_loaders_valid_epss": "_valid_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L46 | neighbors=[test_loaders.py, .test_epss_get_returns_none_for_unknown…, .test_valid_epss_loads()]
- "tests_test_loaders_write_snapshot": "_write_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L38 | neighbors=[test_loaders.py, .test_valid_snapshot_loads_cleanly(), _valid_snapshot()]
- "tests_test_main_scripts_completeness_test_duplicate_port_is_detected": "test_duplicate_port_is_detected()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L39 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_full_scan_is_complete": "test_full_scan_is_complete()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L24 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_missing_port_is_detected": "test_missing_port_is_detected()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L32 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_skip_plus_duplicate_is_not_falsely_complete": "test_skip_plus_duplicate_is_not_falsely_complete()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L46 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_summary_exposes_missing_and_duplicates": "test_summary_exposes_missing_and_duplicates()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L55 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_correlation_test_cleartext_cluster_fires_on_two_cleartext_services": "test_cleartext_cluster_fires_on_two_cleartext_services()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L67 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_correlation_does_not_cross_hosts": "test_correlation_does_not_cross_hosts()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L83 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_correlation_test_legacy_windows_surface_smbv1_plus_rdp": "test_legacy_windows_surface_smbv1_plus_rdp()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L49 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_no_legacy_surface_with_only_smbv1": "test_no_legacy_surface_with_only_smbv1()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L60 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_correlation_test_no_relay_finding_when_signing_required": "test_no_relay_finding_when_signing_required()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L42 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_correlation_test_ntlm_relay_is_high_when_smbv1_also_enabled": "test_ntlm_relay_is_high_when_smbv1_also_enabled()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L34 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_ntlm_relay_is_medium_when_only_signing_not_required": "test_ntlm_relay_is_medium_when_only_signing_not_required()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L26 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_single_cleartext_service_does_not_cluster": "test_single_cleartext_service_does_not_cluster()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L77 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_every_port_scanned_exactly_once": ".test_every_port_scanned_exactly_once()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L82 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner(), _summary()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_local_resource_error_marks_scan_degraded": ".test_local_resource_error_marks_scan_degraded()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L150 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner(), _summary()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_metrics_counts_every_state": ".test_metrics_counts_every_state()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L136 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner(), _summary()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_open_only_output_still_keeps_full_metrics": ".test_open_only_output_still_keeps_full_metrics()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L165 | neighbors=[TestWorkerPoolAndMetrics, _scope(), _summary()]
- "tests_test_main_scripts_findings_test_all_security_headers_present_no_finding": "test_all_security_headers_present_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L232 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_closed_port_no_finding": "test_closed_port_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L152 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_ntp_monlist_and_dns_open_recursion": "test_ntp_monlist_and_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L110 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_open_filtered_never_raises_exposure": "test_open_filtered_never_raises_exposure()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L145 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_smb_hardened_host_no_finding": "test_smb_hardened_host_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L77 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_smb_signing_not_required_is_medium": "test_smb_signing_not_required_is_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L70 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_snmp_amplification": "test_snmp_amplification()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L97 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_snmpv3_only_no_finding": "test_snmpv3_only_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L103 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-074.json

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
