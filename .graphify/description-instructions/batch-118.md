# Node Description Batch 119 of 332

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

- "tests_test_tarpit_testportscannertarpitflag_summary": "._summary()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L48 | neighbors=[TestPortScannerTarpitFlag, .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tarpit_testportscannertarpitflag_test_all_open_host_flagged_as_tarpit": ".test_all_open_host_flagged_as_tarpit()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L51 | neighbors=[TestPortScannerTarpitFlag, ._scanner(), ._summary()]
- "tests_test_tarpit_testportscannertarpitflag_test_mostly_closed_host_not_flagged": ".test_mostly_closed_host_not_flagged()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L63 | neighbors=[TestPortScannerTarpitFlag, ._scanner(), ._summary()]
- "tests_test_task_runner_testrunnerscantypes": "TestRunnerScanTypes" | kind=code-symbol | source=probe/tests/test_task_runner.py:L447 | neighbors=[test_task_runner.py, .test_ot_passive_profile(), .test_web_triage_scan_type()]
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_out_of_scope_target": ".test_rejects_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L205 | neighbors=[When scope is fetched and targets are o…, TestRunnerScopeValidation, When scope is fetched and targets are o…]
- "tests_test_task_runner_testrunnerscopevalidation_test_scope_fallback_when_fetch_fails": ".test_scope_fallback_when_fetch_fails()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L318 | neighbors=[When scope fetch fails, manager-embedde…, TestRunnerScopeValidation, When scope fetch fails, manager-embedde…]
- "tests_test_task_runner_testrunnersubmission": "TestRunnerSubmission" | kind=code-symbol | source=probe/tests/test_task_runner.py:L389 | neighbors=[test_task_runner.py, .test_calls_submit_with_result(), .test_uses_spool_when_available()]
- "tests_test_task_runner_testrunnersubmission_test_calls_submit_with_result": ".test_calls_submit_with_result()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L390 | neighbors=[Verify the submit callback is called wi…, TestRunnerSubmission, Verify the submit callback is called wi…]
- "tests_test_task_runner_testrunnersubmission_test_uses_spool_when_available": ".test_uses_spool_when_available()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L415 | neighbors=[When spool_submit is provided, it's use…, TestRunnerSubmission, When spool_submit is provided, it's use…]
- "tests_test_tls_fingerprint_synthetic_server_hello": "_synthetic_server_hello()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L45 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_integration_self_signed": "_self_signed()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L29 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_integration_test_tls_fingerprint_is_nonzero_and_stable": "test_tls_fingerprint_is_nonzero_and_stable()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L111 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_tls_integration_test_tls_scanner_reports_posture_grade": "test_tls_scanner_reports_posture_grade()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L87 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_tls_legacy_versions_self_signed": "_self_signed()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L35 | neighbors=[test_tls_legacy_versions.py, test_legacy_version_is_detected_not_mas…, test_untested_versions_are_surfaced_in_…]
- "tests_test_tls_legacy_versions_server_supports": "_server_supports()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L97 | neighbors=[test_tls_legacy_versions.py, Skip rather than fail on a build with t…, test_legacy_version_is_detected_not_mas…]
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=probe/tests/test_transport.py:L405 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()]
- "tests_test_transport_transport": "transport()" | kind=code-symbol | source=probe/tests/test_transport.py:L17 | neighbors=[test_transport.py, Create a Transport with a real state fi…, Create a Transport with a real state fi…]
- "tests_test_trust_alignment": "test_trust_alignment.py" | kind=code-symbol | source=manager/detection_engine/tests/test_trust_alignment.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, test_manager_and_probe_trust_sets_match…, test_trust_alignment.py — cross-tree in…]
- "tests_test_two_tree_parity_mirrored_py_files": "_mirrored_py_files()" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L33 | neighbors=[test_two_tree_parity.py, Every .py present in BOTH trees (the mi…, test_mirrored_set_is_nonempty()]
- "tests_test_va_campaign_reporter": "_reporter()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L26 | neighbors=[test_va_campaign.py, test_percent_and_current_stage_transiti…, test_progress_snapshot_shape()]
- "tests_test_va_campaign_test_detect_stage_skipped_when_nothing_was_collected": "test_detect_stage_skipped_when_nothing_was_collected()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L274 | neighbors=[test_va_campaign.py, _detect_stage(), _run()]
- "tests_test_va_campaign_test_detect_stage_turns_facts_into_weakness_findings": "test_detect_stage_turns_facts_into_weakness_findings()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L250 | neighbors=[test_va_campaign.py, _detect_stage(), _scope()]
- "tests_test_validation_endpoints_test_approve_conflict_when_not_pending": "test_approve_conflict_when_not_pending()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L116 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_approve_enqueues_safe_validate_job": "test_approve_enqueues_safe_validate_job()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L89 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_create_rejected_when_roe_forbids": "test_create_rejected_when_roe_forbids()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L74 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_create_request_is_pending_and_derives_tls_check": "test_create_request_is_pending_and_derives_tls_check()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L55 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_reject_marks_rejected": "test_reject_marks_rejected()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L126 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_gate_testrdpnlagate": "TestRdpNlaGate" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L53 | neighbors=[test_validation_gate.py, .test_nla_enforced_suppresses_no_nla_fi…, .test_positive_control_nla_off_is_flagg…]
- "tests_test_validation_gate_testudpnoreplyrejected": "TestUdpNoReplyRejected" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L33 | neighbors=[test_validation_gate.py, .test_open_filtered_amplifier_not_flagg…, .test_positive_control_answered_amplifi…]
- "tests_test_validation_ingest_exec": "_exec()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L72 | neighbors=[test_validation_ingest.py, test_ingest_confirmed_updates_request_a…, test_ingest_unknown_job_is_noop()]
- "tests_test_validation_ingest_test_ingest_confirmed_updates_request_and_finding": "test_ingest_confirmed_updates_request_and_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L88 | neighbors=[test_validation_ingest.py, _exec(), _finding()]
- "tests_test_verification_graph": "test_verification_graph.py" | kind=code-symbol | source=manager/backend/tests/test_verification_graph.py:L1 | neighbors=[c02c465 feat(verification): optional La…, test_graph_available_is_boolean(), test_run_verification_matches_core_with…]
- "tests_test_vnc_scanner_testpurelogic": "TestPureLogic" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L18 | neighbors=[test_vnc_scanner.py, .test_classify(), .test_parse_version()]
- "tests_test_vnc_scanner_testvncscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L34 | neighbors=[TestVNCScanner, .test_no_auth_open(), .test_no_vnc_filtered()]
- "tests_test_weakness_map_testclistatus": "TestCliStatus" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L156 | neighbors=[test_weakness_map.py, ._disk_db(), .test_status_reports_counts_and_gaps()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_dedup_by_cve_target_port": ".test_dedup_by_cve_target_port()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L124 | neighbors=[TestCorrelateWeaknesses, _raw(), _wrapped()]
- "tests_test_weakness_map_testmirrorgap": "TestMirrorGap" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L142 | neighbors=[test_weakness_map.py, .test_every_mapping_has_at_least_one_cv…, .test_missing_from_mirror_lists_absent_…]
- "tests_test_wire_identity_testprobepayload": "TestProbePayload" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L28 | neighbors=[test_wire_identity.py, .test_default_carries_no_brand(), .test_env_override()]
- "tests_test_wire_identity_testuseragent": "TestUserAgent" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L17 | neighbors=[test_wire_identity.py, .test_default_is_generic_browser_no_bra…, .test_env_override()]
- "tests_test_workflow_execution_explodingscanner": "_ExplodingScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L29 | neighbors=[test_workflow_execution.py, .scan_target(), test_per_target_exception_preserves_oth…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-118.json

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
