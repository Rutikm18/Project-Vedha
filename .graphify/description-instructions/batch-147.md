# Node Description Batch 148 of 330

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

- "tests_test_branch_registry_test_web_branch_passes_observed_tls_ports": "test_web_branch_passes_observed_tls_ports()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L197 | neighbors=[test_branch_registry.py, _asset_with()]
- "tests_test_branch_registry_testregistryconsistency_test_every_branch_is_gateable": ".test_every_branch_is_gateable()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L35 | neighbors=[A spec the profile tables don't know ab…, TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_every_component_can_be_merged_into_an_asset": ".test_every_component_can_be_merged_into_an_asset()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L65 | neighbors=[A fact whose scanner name has no merge …, TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_every_component_has_a_cache_certainty": ".test_every_component_has_a_cache_certainty()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L71 | neighbors=[An unlisted scanner falls back to 'unce…, TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_port_tables_match_gates": ".test_port_tables_match_gates()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L40 | neighbors=[gate_5 intersects open ports with its o…, TestRegistryConsistency]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_complete_campaign": ".test_complete_campaign()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L75 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_complete_with_gaps": ".test_complete_with_gaps()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L79 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_defaults_keep_backwards_compatibility": ".test_defaults_keep_backwards_compatibility()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L93 | neighbors=[Callers that don't pass the new inputs …, TestNormalPipelineUnaffected]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_no_jobs_is_pending": ".test_no_jobs_is_pending()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L89 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_uncovered_submission_keeps_it_detecting": ".test_uncovered_submission_keeps_it_detecting()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L84 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_a_dead_queue_is_still_reported_as_error_first": ".test_a_dead_queue_is_still_reported_as_error_first()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L62 | neighbors=[TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_all_cancelled_campaign_is_terminal": ".test_all_cancelled_campaign_is_terminal()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L39 | neighbors=[TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_all_failed_campaign_is_terminal": ".test_all_failed_campaign_is_terminal()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L44 | neighbors=[TestTerminalWithoutResults, _status()]
- "tests_test_cli_test_cmd_doctor_success_with_online_agent": "test_cmd_doctor_success_with_online_agent()" | kind=code-symbol | source=probe/tests/test_cli.py:L204 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_cmd_scan_run_builds_dispatch_payload": "test_cmd_scan_run_builds_dispatch_payload()" | kind=code-symbol | source=probe/tests/test_cli.py:L167 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_rejects_invalid_timing": "test_poll_job_rejects_invalid_timing()" | kind=code-symbol | source=probe/tests/test_cli.py:L291 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_returns_terminal_status": "test_poll_job_returns_terminal_status()" | kind=code-symbol | source=probe/tests/test_cli.py:L298 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_times_out": "test_poll_job_times_out()" | kind=code-symbol | source=probe/tests/test_cli.py:L308 | neighbors=[test_cli.py, FakeClient]
- "tests_test_customer_access_testrejectscanrequest": "TestRejectScanRequest" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L193 | neighbors=[test_customer_access.py, .test_reject_records_reason()]
- "tests_test_cve_correlation_testingestpagination_pages": "._pages()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L266 | neighbors=[TestIngestPagination, .test_resume()]
- "tests_test_cve_correlation_testingestpagination_test_resume": ".test_resume()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L274 | neighbors=[TestIngestPagination, ._pages()]
- "tests_test_db_scanner_run": "_run()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L33 | neighbors=[test_db_scanner.py, _probe()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_rejects_garbage_with_type_byte": ".test_oracle_rejects_garbage_with_type_byte()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L73 | neighbors=[TestMysqlxVsOracle, _probe()]
- "tests_test_detection_core_testaggregate_test_dedup_within_run": ".test_dedup_within_run()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1143 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_multi_run_intermittent": ".test_multi_run_intermittent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1137 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_multi_run_stable": ".test_multi_run_stable()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1130 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_single_run": ".test_single_run()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1123 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testasset_test_add_fact_updates_first_last_seen": ".test_add_fact_updates_first_last_seen()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L135 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testasset_test_as_of_cutoff": ".test_as_of_cutoff()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L156 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testasset_test_facts_by_scanner": ".test_facts_by_scanner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L142 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testasset_test_open_ports": ".test_open_ports()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L149 | neighbors=[TestAsset, _fact()]
- "tests_test_detection_core_testclassifytier_test_authoritative_tier4": ".test_authoritative_tier4()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L665 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testclassifytier_test_multi_signal_tier2": ".test_multi_signal_tier2()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L674 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testclassifytier_test_protocol_scanner_tier3": ".test_protocol_scanner_tier3()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L669 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testclassifytier_test_single_banner_tier1": ".test_single_banner_tier1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L679 | neighbors=[TestClassifyTier, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_critical": ".test_cvss_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L825 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_high": ".test_cvss_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L831 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_low": ".test_cvss_low()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L843 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_cvss_medium": ".test_cvss_medium()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L837 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcomputepriority_test_elevated_epss_high": ".test_elevated_epss_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L818 | neighbors=[TestComputePriority, _finding()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-147.json

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
