# Node Description Batch 45 of 119

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

- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_by_cve": ".test_select_exploit_by_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L256 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_fallback_no_cve": ".test_select_exploit_fallback_no_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L269 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_log4shell": ".test_select_exploit_log4shell()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L263 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_scope_out_of_range": ".test_validate_scope_out_of_range()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L284 | neighbors=[TestExploitOrchestrator, _engagement(), ._make_orchestrator()]
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=probe/tests/test_http_lease.py:L1 | neighbors=[b4b12a9 Rename project and update files, agent.py, test_polled_job_renews_lease_until_runn…]
- "tests_test_hw_bind_testgethwid": "TestGetHwId" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L11 | neighbors=[test_hw_bind.py, .test_deterministic_within_session(), .test_returns_32_hex_chars()]
- "tests_test_nuclei_scanner_test_nonzero_exit_retains_and_marks_partial_findings": "test_nonzero_exit_retains_and_marks_partial_findings()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L128 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_nuclei_scanner_test_run_scan_streams_jsonl_and_separates_timeouts": "test_run_scan_streams_jsonl_and_separates_timeouts()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L67 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_nuclei_scanner_test_timeout_retains_findings_emitted_before_termination": "test_timeout_retains_findings_emitted_before_termination()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L153 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_passive_collector_test_ot_udp_backend_never_joins_or_transmits": "test_ot_udp_backend_never_joins_or_transmits()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L74 | neighbors=[test_passive_collector.py, .close(), _Writer]
- "tests_test_passive_collector_test_subset_listener_failure_reports_degraded_coverage": "test_subset_listener_failure_reports_degraded_coverage()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L35 | neighbors=[test_passive_collector.py, _Socket, _Writer]
- "tests_test_port_catalog": "test_port_catalog.py" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L1 | neighbors=[cdee859 feat(probe): add container/clou…, test_modern_infra_ports_present(), gates.py]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=probe/tests/test_probe_core.py:L546 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]
- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L547 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L554 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L480 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L481 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L488 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L562 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L499 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L500 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L506 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L513 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L538 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L522 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L571 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L530 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L467 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L871 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_result_spool_spool": "spool()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L13 | neighbors=[test_result_spool.py, ResultSpool with tiny retry delay for f…, ResultSpool with tiny retry delay for f…]
- "tests_test_scope_crypt_testkeygeneration": "TestKeyGeneration" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L15 | neighbors=[test_scope_crypt.py, .test_generates_32_byte_keys(), .test_generates_different_keys_each_cal…]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311()]
- "tests_test_task_runner_testrunnerscantypes": "TestRunnerScanTypes" | kind=code-symbol | source=probe/tests/test_task_runner.py:L447 | neighbors=[test_task_runner.py, .test_ot_passive_profile(), .test_web_triage_scan_type()]
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_out_of_scope_target": ".test_rejects_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L205 | neighbors=[When scope is fetched and targets are o…, TestRunnerScopeValidation, When scope is fetched and targets are o…]
- "tests_test_task_runner_testrunnerscopevalidation_test_scope_fallback_when_fetch_fails": ".test_scope_fallback_when_fetch_fails()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L318 | neighbors=[When scope fetch fails, manager-embedde…, TestRunnerScopeValidation, When scope fetch fails, manager-embedde…]
- "tests_test_task_runner_testrunnersubmission": "TestRunnerSubmission" | kind=code-symbol | source=probe/tests/test_task_runner.py:L389 | neighbors=[test_task_runner.py, .test_calls_submit_with_result(), .test_uses_spool_when_available()]
- "tests_test_task_runner_testrunnersubmission_test_calls_submit_with_result": ".test_calls_submit_with_result()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L390 | neighbors=[Verify the submit callback is called wi…, TestRunnerSubmission, Verify the submit callback is called wi…]
- "tests_test_task_runner_testrunnersubmission_test_uses_spool_when_available": ".test_uses_spool_when_available()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L415 | neighbors=[When spool_submit is provided, it's use…, TestRunnerSubmission, When spool_submit is provided, it's use…]
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=probe/tests/test_transport.py:L280 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()]
- "tests_test_transport_transport": "transport()" | kind=code-symbol | source=probe/tests/test_transport.py:L17 | neighbors=[test_transport.py, Create a Transport with a real state fi…, Create a Transport with a real state fi…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-044.json

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
