# Node Description Batch 120 of 236

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_seed_admin_testfirstdeployment": "TestFirstDeployment" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L96 | neighbors=[test_seed_admin.py, .test_creates_tenant_and_admin_on_first…]
- "tests_test_service_identifier_rationale_1": "Unit tests for ServiceIdentifier." | kind=entity | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[test_service_identifier.py, ServiceIdentifier]
- "tests_test_service_identifier_testserviceidentifier_test_confidence_floor_port_hint": ".test_confidence_floor_port_hint()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L70 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ftp_banner": ".test_ftp_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L28 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_high_confidence_combined": ".test_high_confidence_combined()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L75 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_http_server_header": ".test_http_server_header()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L19 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_kerberos_banner": ".test_kerberos_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L48 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ldap_banner": ".test_ldap_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L52 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_mssql_banner": ".test_mssql_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L44 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_mysql_banner": ".test_mysql_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L36 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_rdp_port_hint": ".test_rdp_port_hint()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L56 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_redis_pong": ".test_redis_pong()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L40 | neighbors=[TestServiceIdentifier, ._id()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-119.json

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
