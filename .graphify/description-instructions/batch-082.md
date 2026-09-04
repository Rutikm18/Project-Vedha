# Node Description Batch 83 of 332

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

- "tests_test_notifications_testdeliver": "TestDeliver" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L13 | neighbors=[test_notifications.py, .test_dispatches_to_the_kind(), .test_sender_error_is_swallowed(), .test_unknown_kind_returns_false()]
- "tests_test_nuclei_scanner_finding_line": "_finding_line()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L12 | neighbors=[test_nuclei_scanner.py, test_nonzero_exit_retains_and_marks_par…, test_run_scan_streams_jsonl_and_separat…, test_timeout_retains_findings_emitted_b…]
- "tests_test_online_get_raising": "_get_raising()" | kind=code-symbol | source=probe/tests/test_online.py:L58 | neighbors=[test_online.py, .test_fail_open_leaves_offline_result_u…, .test_network_error_is_fail_open(), .test_error_is_none()]
- "tests_test_online_nvd_bytes": "_nvd_bytes()" | kind=code-symbol | source=probe/tests/test_online.py:L25 | neighbors=[test_online.py, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…, .test_parses_score_severity_refs()]
- "tests_test_online_testenrichfindings_test_gap_fill_sets_cvss_and_recomputes_risk": ".test_gap_fill_sets_cvss_and_recomputes_risk()" | kind=code-symbol | source=probe/tests/test_online.py:L118 | neighbors=[TestEnrichFindings, _finding(), _get_returning(), _nvd_bytes()]
- "tests_test_online_testenrichfindings_test_online_all_cross_checks_and_annotates_mismatch": ".test_online_all_cross_checks_and_annotates_mismatch()" | kind=code-symbol | source=probe/tests/test_online.py:L139 | neighbors=[TestEnrichFindings, _finding(), _get_returning(), _nvd_bytes()]
- "tests_test_os_fingerprint_testtimestampfallback": "TestTimestampFallback" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L138 | neighbors=[test_os_fingerprint.py, ._scanner(), .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_outbox_reclaim_mock_session": "_mock_session()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L104 | neighbors=[test_outbox_reclaim.py, test_reclaim_handles_none_rowcount_from…, test_reclaim_is_noop_when_nothing_is_st…, test_reclaim_runs_both_sweeps_commits_a…]
- "tests_test_outbox_reclaim_sql": "_sql()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L20 | neighbors=[test_outbox_reclaim.py, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_requeue_stmt_makes_retryable_stran…]
- "tests_test_pipeline_concurrency_db_with": "_db_with()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L100 | neighbors=[test_pipeline_concurrency.py, test_a_first_delivery_still_runs_detect…, test_a_missing_submission_is_not_an_err…, test_a_redelivered_submission_is_not_de…]
- "tests_test_pipeline_concurrency_event": "_event()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L93 | neighbors=[test_pipeline_concurrency.py, test_a_first_delivery_still_runs_detect…, test_a_missing_submission_is_not_an_err…, test_a_redelivered_submission_is_not_de…]
- "tests_test_pipeline_concurrency_test_a_first_delivery_still_runs_detection": "test_a_first_delivery_still_runs_detection()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L128 | neighbors=[test_pipeline_concurrency.py, The guard must not swallow real work., _db_with(), _event()]
- "tests_test_pipeline_concurrency_test_a_missing_submission_is_not_an_error": "test_a_missing_submission_is_not_an_error()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L147 | neighbors=[test_pipeline_concurrency.py, Pre-existing behaviour: a vanished scan…, _db_with(), _event()]
- "tests_test_pipeline_openssh_upstream_vuln_db": "_openssh_upstream_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L73 | neighbors=[test_pipeline.py, _mock_vuln_db(), Upstream boundary for a banner-vs-inven…, .test_full_detection_exposes_authoritat…]
- "tests_test_pipeline_testrunpipelineaiassist": "TestRunPipelineAiAssist" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L323 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default()]
- "tests_test_portal_assistant_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L44 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_only_the_whitelisted_finding_field…]
- "tests_test_portal_metrics_testseveritybreakdown": "TestSeverityBreakdown" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L19 | neighbors=[test_portal_metrics.py, .test_all_buckets_present_zero_filled(), .test_open_only_excludes_closed(), .test_unknown_severity_falls_into_info()]
- "tests_test_portal_metrics_teststatustimeline": "TestStatusTimeline" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L41 | neighbors=[test_portal_metrics.py, .test_activity_outside_window_is_ignore…, .test_buckets_opened_and_closed(), .test_emits_continuous_zero_filled_mont…]
- "tests_test_portal_read_added": "_added()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L173 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_whole_scope_when_no_targets(), .test_creates_pending_request_and_audit…]
- "tests_test_portal_read_finding_with_internal": "_finding_with_internal()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L58 | neighbors=[test_portal_read.py, A finding-like ORM object carrying BOTH…, .test_serialization_drops_internal_fiel…, .test_findings_scoped_and_serialized()]
- "tests_test_portal_read_testcreatescanrequest_test_creates_pending_request_and_audits": ".test_creates_pending_request_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L181 | neighbors=[TestCreateScanRequest, _added(), _client(), _db_first()]
- "tests_test_portal_read_testcreatescanrequest_test_excluded_target_is_422": ".test_excluded_target_is_422()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L284 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_out_of_scope_target_is_422": ".test_out_of_scope_target_is_422()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L275 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_queue_cap_is_conflict": ".test_queue_cap_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L294 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_unknown_scan_type_is_422": ".test_unknown_scan_type_is_422()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L267 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testportalfindings": "TestPortalFindings" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L97 | neighbors=[test_portal_read.py, .test_findings_scoped_and_serialized(), .test_operator_is_forbidden(), .test_single_finding_404_when_out_of_sc…]
- "tests_test_portal_read_testportalfindings_test_findings_scoped_and_serialized": ".test_findings_scoped_and_serialized()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L98 | neighbors=[TestPortalFindings, _client(), _db_list(), _finding_with_internal()]
- "tests_test_portal_read_testportalreports": "TestPortalReports" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L114 | neighbors=[test_portal_read.py, .test_download_returns_content_for_appr…, .test_lists_approved_reports(), .test_unapproved_or_missing_report_is_4…]
- "tests_test_portal_read_testtrends_test_returns_severity_and_timeline": ".test_returns_severity_and_timeline()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L209 | neighbors=[TestTrends, _client(), _db_list(), _finding()]
- "tests_test_portal_remediation_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L27 | neighbors=[test_portal_remediation.py, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_portal_remediation_testportalremediation_test_serves_kb_when_no_stored_plan": ".test_serves_kb_when_no_stored_plan()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L45 | neighbors=[TestPortalRemediation, _client(), _db_scalar(), _finding()]
- "tests_test_portal_remediation_testportalremediation_test_serves_reviewed_ai_plan_stripping_operator_metadata": ".test_serves_reviewed_ai_plan_stripping_operator_metadata()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L53 | neighbors=[TestPortalRemediation, _client(), _db_scalar(), _finding()]
- "tests_test_portal_remediation_testportalremediation_test_unreviewed_ai_plan_does_not_leak": ".test_unreviewed_ai_plan_does_not_leak()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L64 | neighbors=[TestPortalRemediation, _client(), _db_scalar(), _finding()]
- "tests_test_portal_scope_testassertclient": "TestAssertClient" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L37 | neighbors=[test_portal_scope.py, .test_bound_client_returns_engagement(), .test_client_without_engagement_is_forb…, .test_operator_is_forbidden()]
- "tests_test_portal_scope_testportaltokenclaims": "TestPortalTokenClaims" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L84 | neighbors=[test_portal_scope.py, .test_client_role_enum_exists(), .test_client_token_carries_portal_aud_a…, .test_operator_and_portal_audiences_dif…]
- "tests_test_portal_scope_testresolvescope": "TestResolveScope" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L55 | neighbors=[test_portal_scope.py, .test_matching_request_ok(), .test_mismatched_request_is_403_idor_de…, .test_no_request_returns_bound()]
- "tests_test_posture_confidence_by_rule": "_by_rule()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L33 | neighbors=[test_posture_confidence.py, .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_confidence_testendtoend_test_corroborated_host_gets_floored_confidence_and_factors": ".test_corroborated_host_gets_floored_confidence_and_factors()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L94 | neighbors=[TestEndToEnd, _asset(), _by_rule(), _fact()]
- "tests_test_posture_confidence_testendtoend_test_filtered_port_lowers_confidence": ".test_filtered_port_lowers_confidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L114 | neighbors=[TestEndToEnd, _asset(), _by_rule(), _fact()]
- "tests_test_posture_confidence_testendtoend_test_lone_finding_keeps_base_confidence": ".test_lone_finding_keeps_base_confidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L107 | neighbors=[TestEndToEnd, _asset(), _by_rule(), _fact()]

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
