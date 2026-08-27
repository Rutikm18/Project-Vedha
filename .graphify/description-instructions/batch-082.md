# Node Description Batch 83 of 236

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

- "tests_test_db_scanner_tns_packet": "_tns_packet()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L44 | neighbors=[test_db_scanner.py, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_db_scanner_xproto_frame": "_xproto_frame()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L39 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_testmatchcandidate_test_ai_assisted_carried_through": ".test_ai_assisted_carried_through()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L463 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_authoritative_source_confirms": ".test_authoritative_source_confirms()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L420 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_inferred_match_has_backport_note": ".test_inferred_match_has_backport_note()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L435 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_match_produces_finding": ".test_match_produces_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L404 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_match_returns_empty": ".test_no_match_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L449 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_version_returns_empty": ".test_no_version_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L392 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_unknown_product_returns_empty": ".test_unknown_product_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L399 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_inferred_when_auth_version_lower": ".test_keeps_inferred_when_auth_version_lower()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L541 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_detection_core_testsuppressnegated_test_suppresses_inferred_when_authoritative_contradicts": ".test_suppresses_inferred_when_authoritative_contradicts()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L517 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_e2e_engagement_to_findings_test_real_scan_of_open_datastore_yields_manager_finding": "test_real_scan_of_open_datastore_yields_manager_finding()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L109 | neighbors=[test_e2e_engagement_to_findings.py, _manager(), _plant()]
- "tests_test_engagement_lists_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L17 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_engagement_lists_test_list_assets_groups_services": "test_list_assets_groups_services()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L39 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
- "tests_test_engagement_lists_test_list_jobs_returns_results": "test_list_jobs_returns_results()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L22 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
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
- "tests_test_integrations_testputintegration_test_create_encrypts_secret_and_masks_it": ".test_create_encrypts_secret_and_masks_it()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L38 | neighbors=[TestPutIntegration, _db(), _operator()]
- "tests_test_integrations_testputintegration_test_rejects_unknown_kind": ".test_rejects_unknown_kind()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L32 | neighbors=[TestPutIntegration, _db(), _operator()]
- "tests_test_integrations_testputintegration_test_update_without_secret_keeps_existing": ".test_update_without_secret_keeps_existing()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L52 | neighbors=[TestPutIntegration, _db(), _operator()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-082.json

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
