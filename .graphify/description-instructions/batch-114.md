# Node Description Batch 115 of 332

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

- "tests_test_os_fingerprint_testinetchecksum": "TestInetChecksum" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L24 | neighbors=[test_os_fingerprint.py, .test_checksum_handles_odd_length(), .test_checksum_verifies_to_zero()]
- "tests_test_os_fingerprint_testremoteclock": "TestRemoteClock" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L123 | neighbors=[test_os_fingerprint.py, .test_high_bit_marks_nonstandard_clock(), .test_standard_value_decodes_to_wall_cl…]
- "tests_test_os_fingerprint_testtimestampfallback_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L139 | neighbors=[TestTimestampFallback, .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_outbox_reclaim_test_dead_letter_and_requeue_are_mutually_exclusive": "test_dead_letter_and_requeue_are_mutually_exclusive()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L92 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_dead_letter_stmt_targets_exhausted_stranded_rows": "test_dead_letter_stmt_targets_exhausted_stranded_rows()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L68 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_requeue_stmt_makes_retryable_stranded_rows_due_now": "test_requeue_stmt_makes_retryable_stranded_rows_due_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L81 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_passive_collector_test_ot_udp_backend_never_joins_or_transmits": "test_ot_udp_backend_never_joins_or_transmits()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L74 | neighbors=[test_passive_collector.py, .close(), _Writer]
- "tests_test_passive_collector_test_subset_listener_failure_reports_degraded_coverage": "test_subset_listener_failure_reports_degraded_coverage()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L35 | neighbors=[test_passive_collector.py, _Socket, _Writer]
- "tests_test_pipeline_banner_jsonl": "_banner_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L105 | neighbors=[test_pipeline.py, .test_banner_finding_is_suspected_not_c…, .test_full_detection_exposes_authoritat…]
- "tests_test_pipeline_concurrency_test_a_redelivered_submission_is_not_detected_twice": "test_a_redelivered_submission_is_not_detected_twice()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L111 | neighbors=[test_pipeline_concurrency.py, _db_with(), _event()]
- "tests_test_pipeline_testrunpipelinededup": "TestRunPipelineDedup" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L276 | neighbors=[test_pipeline.py, .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_pipeline_testrunpipelineemptyinput": "TestRunPipelineEmptyInput" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L129 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty()]
- "tests_test_pipeline_testrunpipelineexposure": "TestRunPipelineExposure" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L247 | neighbors=[test_pipeline.py, .test_exposure_internet_facing_propagat…, .test_no_exposure_fields_are_none()]
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
- "tests_test_posture_confidence_testchains": "TestChains" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L73 | neighbors=[test_posture_confidence.py, .test_chain_floor_never_lowers_confiden…, .test_ntlm_relay_chain_floors_both()]
- "tests_test_posture_confidence_testendtoend_test_confidence_is_serialized": ".test_confidence_is_serialized()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L121 | neighbors=[TestEndToEnd, _asset(), _fact()]
- "tests_test_posture_rules_testinvariants_test_dedup_same_rule_same_port": ".test_dedup_same_rule_same_port()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L161 | neighbors=[TestInvariants, _asset(), _fact()]
- "tests_test_posture_rules_testinvariants_test_detect_all_sorts_by_risk_desc": ".test_detect_all_sorts_by_risk_desc()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L167 | neighbors=[TestInvariants, _asset(), _fact()]
- "tests_test_posture_rules_testinvariants_test_deterministic_id_across_runs": ".test_deterministic_id_across_runs()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L155 | neighbors=[TestInvariants, _asset(), _fact()]
- "tests_test_posture_rules_testtrusttier_test_unvalidated_scanner_only_suspects": ".test_unvalidated_scanner_only_suspects()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L37 | neighbors=[TestTrustTier, _asset(), _fact()]
- "tests_test_posture_rules_testtrusttier_test_validated_scanner_confirms": ".test_validated_scanner_confirms()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L31 | neighbors=[TestTrustTier, _asset(), _fact()]
- "tests_test_posture_rules_testudphonesty": "TestUdpHonesty" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L120 | neighbors=[test_posture_rules.py, .test_amplifier_fires_only_when_it_answ…, .test_no_reply_udp_raises_nothing()]
- "tests_test_posture_rules_testudphonesty_test_amplifier_fires_only_when_it_answered": ".test_amplifier_fires_only_when_it_answered()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L121 | neighbors=[TestUdpHonesty, _asset(), _fact()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-114.json

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
