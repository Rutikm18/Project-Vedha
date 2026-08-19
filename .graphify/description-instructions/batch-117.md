# Node Description Batch 118 of 227

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

- "tests_test_service_identifier_testserviceidentifier_test_smb_detection": ".test_smb_detection()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L32 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_smtp_banner": ".test_smtp_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L24 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ssh_banner": ".test_ssh_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L13 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_unknown_service_empty_banner": ".test_unknown_service_empty_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L65 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_version_extraction": ".test_version_extraction()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L61 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_match_testscannerintegration": "TestScannerIntegration" | kind=code-symbol | source=probe/tests/test_service_match.py:L108 | neighbors=[test_service_match.py, .test_scanner_identifies_ssh_on_nonstan…]
- "tests_test_sla_policy_testpolicyawarecompute_test_custom_window_relaxes_state": ".test_custom_window_relaxes_state()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L27 | neighbors=[TestPolicyAwareCompute, _finding()]
- "tests_test_sla_policy_testpolicyawarecompute_test_default_window_breaches": ".test_default_window_breaches()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L24 | neighbors=[TestPolicyAwareCompute, _finding()]
- "tests_test_smb_scanner_test_request_omits_311_without_preauth_context": "test_request_omits_311_without_preauth_context()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L80 | neighbors=[test_smb_scanner.py, Offering SMB 3.1.1 with no preauth-inte…]
- "tests_test_smb_scanner_test_signing_not_required": "test_signing_not_required()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L38 | neighbors=[test_smb_scanner.py, _smb2_negotiate_response()]
- "tests_test_smb_scanner_test_signing_required_smb311": "test_signing_required_smb311()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L29 | neighbors=[test_smb_scanner.py, _smb2_negotiate_response()]
- "tests_test_smb_scanner_test_truncated_negotiate_body_not_parsed": "test_truncated_negotiate_body_not_parsed()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L62 | neighbors=[test_smb_scanner.py, A response with the wrong body Structur…]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_closed_and_filtered_suppressed_by_default": ".test_closed_and_filtered_suppressed_by_default()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L374 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_open_result_carries_signals_and_os_guess": ".test_open_result_carries_signals_and_os_guess()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L353 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_open_without_signals_has_no_os_guess": ".test_open_without_signals_has_no_os_guess()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L369 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_windows_ttl_maps_to_windows": ".test_windows_ttl_maps_to_windows()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L363 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testparsepacketsignals_test_window_ttl_mss_surfaced": ".test_window_ttl_mss_surfaced()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L336 | neighbors=[TestParsePacketSignals, _synack_with_options()]
- "tests_test_syn_scanner_testsynretransmit_test_answered_ports_are_not_retransmitted": ".test_answered_ports_are_not_retransmitted()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L247 | neighbors=[TestSynRetransmit, ._patch()]
- "tests_test_syn_scanner_testsynretransmit_test_retries_zero_sends_one_syn_per_port": ".test_retries_zero_sends_one_syn_per_port()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L277 | neighbors=[TestSynRetransmit, ._patch()]
- "tests_test_syn_scanner_testsynretransmit_test_silent_ports_are_retried_retries_plus_one_times": ".test_silent_ports_are_retried_retries_plus_one_times()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L232 | neighbors=[TestSynRetransmit, ._patch()]
- "tests_test_syn_scanner_testverifyreplycookie_test_reply_from_other_host_fails": ".test_reply_from_other_host_fails()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L129 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_syn_scanner_testverifyreplycookie_test_valid_cookie_verifies": ".test_valid_cookie_verifies()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L119 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_syn_scanner_testverifyreplycookie_test_wrong_ack_fails": ".test_wrong_ack_fails()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L124 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_task_runner_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L12 | neighbors=[test_task_runner.py, Return a minimal successful result with…]
- "tests_test_task_runner_runner": "runner()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L37 | neighbors=[test_task_runner.py, TaskRunner with no-op dependencies (no …]
- "tests_test_tls_fingerprint_testparseserverhello_test_extracts_version_and_cipher": ".test_extracts_version_and_cipher()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L59 | neighbors=[TestParseServerHello, _synthetic_server_hello()]
- "tests_test_tls_fingerprint_testparseserverhello_test_tls13_version_from_supported_versions_ext": ".test_tls13_version_from_supported_versions_ext()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L65 | neighbors=[TestParseServerHello, _synthetic_server_hello()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_a_modern": ".test_grade_a_modern()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L73 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_b_no_tls13": ".test_grade_b_no_tls13()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L78 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_c_tls11": ".test_grade_c_tls11()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L83 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_f_tls10": ".test_grade_f_tls10()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L94 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_validation_endpoints_exec": "_exec()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L28 | neighbors=[test_validation_endpoints.py, _mock_db()]
- "tests_test_validation_ingest_test_confirmed_never_overrides_human_closed_finding": "test_confirmed_never_overrides_human_closed_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L55 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_confirmed_raises_certainty": "test_confirmed_raises_certainty()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L32 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_contradicted_marks_false_positive_without_touching_status": "test_contradicted_marks_false_positive_without_touching_status()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L40 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_inconclusive_leaves_finding_unchanged": "test_inconclusive_leaves_finding_unchanged()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L48 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_ingest_unknown_job_is_noop": "test_ingest_unknown_job_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L107 | neighbors=[test_validation_ingest.py, _exec()]
- "tests_test_validation_request_schema": "test_validation_request_schema.py" | kind=code-symbol | source=manager/backend/tests/test_validation_request_schema.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, test_validation_request_columns_and_def…]
- "tests_test_vantage_fusion_test_ambiguous_when_only_open_filtered": "test_ambiguous_when_only_open_filtered()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L51 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_declared_external_vantage_without_hint_name": "test_declared_external_vantage_without_hint_name()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L64 | neighbors=[test_vantage_fusion.py, _probe()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-117.json

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
