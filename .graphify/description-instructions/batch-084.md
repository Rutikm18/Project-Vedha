# Node Description Batch 85 of 236

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

- "tests_test_os_fingerprint_testicmptimestamps_ts_reply": "._ts_reply()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L96 | neighbors=[TestIcmpTimestamps, .test_parse_datagram_delivery_has_no_tt…, .test_parse_extracts_ttl_and_transmit()]
- "tests_test_os_fingerprint_testinetchecksum": "TestInetChecksum" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L24 | neighbors=[test_os_fingerprint.py, .test_checksum_handles_odd_length(), .test_checksum_verifies_to_zero()]
- "tests_test_os_fingerprint_testremoteclock": "TestRemoteClock" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L123 | neighbors=[test_os_fingerprint.py, .test_high_bit_marks_nonstandard_clock(), .test_standard_value_decodes_to_wall_cl…]
- "tests_test_os_fingerprint_testtimestampfallback_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L139 | neighbors=[TestTimestampFallback, .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_outbox_reclaim_test_dead_letter_and_requeue_are_mutually_exclusive": "test_dead_letter_and_requeue_are_mutually_exclusive()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L92 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_dead_letter_stmt_targets_exhausted_stranded_rows": "test_dead_letter_stmt_targets_exhausted_stranded_rows()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L68 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_requeue_stmt_makes_retryable_stranded_rows_due_now": "test_requeue_stmt_makes_retryable_stranded_rows_due_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L81 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_passive_collector_test_ot_udp_backend_never_joins_or_transmits": "test_ot_udp_backend_never_joins_or_transmits()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L74 | neighbors=[test_passive_collector.py, .close(), _Writer]
- "tests_test_passive_collector_test_subset_listener_failure_reports_degraded_coverage": "test_subset_listener_failure_reports_degraded_coverage()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L35 | neighbors=[test_passive_collector.py, _Socket, _Writer]
- "tests_test_pipeline_testrunpipelinededup": "TestRunPipelineDedup" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L232 | neighbors=[test_pipeline.py, .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_pipeline_testrunpipelineemptyinput": "TestRunPipelineEmptyInput" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L112 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty()]
- "tests_test_pipeline_testrunpipelineexposure": "TestRunPipelineExposure" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L203 | neighbors=[test_pipeline.py, .test_exposure_internet_facing_propagat…, .test_no_exposure_fields_are_none()]
- "tests_test_port_catalog": "test_port_catalog.py" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L1 | neighbors=[cdee859 feat(probe): add container/clou…, test_modern_infra_ports_present(), gates.py]
- "tests_test_portal_read_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L180 | neighbors=[test_portal_read.py, .test_aggregates_posture_counts_and_que…, .test_returns_severity_and_timeline()]
- "tests_test_portal_read_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L31 | neighbors=[test_portal_read.py, .test_operator_cannot_create(), .test_operator_is_forbidden()]
- "tests_test_portal_read_testclientfindingwhitelist": "TestClientFindingWhitelist" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L82 | neighbors=[test_portal_read.py, .test_schema_is_a_whitelist(), .test_serialization_drops_internal_fiel…]
- "tests_test_portal_read_testcreatescanrequest_test_duplicate_pending_is_conflict": ".test_duplicate_pending_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L190 | neighbors=[TestCreateScanRequest, _client(), _db_first()]
- "tests_test_portal_read_testcreatescanrequest_test_operator_cannot_create": ".test_operator_cannot_create()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L303 | neighbors=[TestCreateScanRequest, _operator(), _db_first()]
- "tests_test_portal_read_testportalfindings_test_operator_is_forbidden": ".test_operator_is_forbidden()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L103 | neighbors=[TestPortalFindings, _db_list(), _operator()]
- "tests_test_portal_read_testportalfindings_test_single_finding_404_when_out_of_scope": ".test_single_finding_404_when_out_of_scope()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L108 | neighbors=[TestPortalFindings, _client(), _db_scalar()]
- "tests_test_portal_read_testportalpostureandengagement": "TestPortalPostureAndEngagement" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L133 | neighbors=[test_portal_read.py, .test_engagement_summary(), .test_posture_scores_open_findings()]
- "tests_test_portal_read_testportalpostureandengagement_test_engagement_summary": ".test_engagement_summary()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L143 | neighbors=[TestPortalPostureAndEngagement, _client(), _db_scalar()]
- "tests_test_portal_read_testportalpostureandengagement_test_posture_scores_open_findings": ".test_posture_scores_open_findings()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L134 | neighbors=[TestPortalPostureAndEngagement, _client(), _db_list()]
- "tests_test_portal_read_testportalreports_test_download_returns_content_for_approved": ".test_download_returns_content_for_approved()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L126 | neighbors=[TestPortalReports, _client(), _db_scalar()]
- "tests_test_portal_read_testportalreports_test_lists_approved_reports": ".test_lists_approved_reports()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L120 | neighbors=[TestPortalReports, _client(), _db_list()]
- "tests_test_portal_read_testportalreports_test_unapproved_or_missing_report_is_404": ".test_unapproved_or_missing_report_is_404()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L115 | neighbors=[TestPortalReports, _client(), _db_scalar()]
- "tests_test_portal_read_testsummary_test_aggregates_posture_counts_and_queue": ".test_aggregates_posture_counts_and_queue()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L190 | neighbors=[TestSummary, _client(), _finding()]
- "tests_test_portal_remediation_testportalremediation_test_missing_or_out_of_scope_finding_is_404": ".test_missing_or_out_of_scope_finding_is_404()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L75 | neighbors=[TestPortalRemediation, _client(), _db_scalar()]
- "tests_test_portal_scope_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L33 | neighbors=[test_portal_scope.py, .test_operator_is_forbidden(), .test_operator_cannot_scope()]
- "tests_test_portal_scope_testclientscoped": "TestClientScoped" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L70 | neighbors=[test_portal_scope.py, .test_applies_engagement_filter_for_bou…, .test_operator_cannot_scope()]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=probe/tests/test_probe_core.py:L568 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]
- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L569 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L576 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L502 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L503 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L510 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L584 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L521 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L522 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L528 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-084.json

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
