# Node Description Batch 80 of 227

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

- "tests_test_ai_normalizer_testproposecandidates_test_cache_hit_bypasses_client": ".test_cache_hit_bypasses_client()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L167 | neighbors=[When the cache already has an answer, t…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_client_failure_returns_empty": ".test_client_failure_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L154 | neighbors=[Any exception from the AI client yields…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_malformed_response_missing_product_skipped": ".test_malformed_response_missing_product_skipped()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L184 | neighbors=[A candidate dict without a 'product' ke…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_malformed_response_not_a_list_returns_empty": ".test_malformed_response_not_a_list_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L193 | neighbors=[If the client returns something that is…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_result_is_cached_after_first_call": ".test_result_is_cached_after_first_call()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L252 | neighbors=[The result of a first successful client…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_source_confidence_propagated_from_fact": ".test_source_confidence_propagated_from_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L218 | neighbors=[source_confidence on the resulting CPEC…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_version_none_when_absent": ".test_version_none_when_absent()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L242 | neighbors=[A candidate without a version key produ…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_version_propagated_when_present": ".test_version_propagated_when_present()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L230 | neighbors=[When the AI response includes a version…, TestProposeCandidates, _fact()]
- "tests_test_async_udp_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=probe/tests/test_async_udp.py:L23 | neighbors=[test_async_udp.py, .connection_made(), .datagram_received()]
- "tests_test_attack_path_correlation_test_cleartext_cluster_needs_two": "test_cleartext_cluster_needs_two()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L82 | neighbors=[test_attack_path_correlation.py, _get(), _ids()]
- "tests_test_auth_login_testauthenticatedisableduser_test_raises_disabled_user": ".test_raises_disabled_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L111 | neighbors=[TestAuthenticateDisabledUser, _make_db(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword": "TestAuthenticateExpiredPassword" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L135 | neighbors=[test_auth_login.py, .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testauthenticatesuccess": "TestAuthenticateSuccess" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L193 | neighbors=[test_auth_login.py, .test_null_password_expires_at_never_ex…, .test_returns_user_on_valid_credentials…]
- "tests_test_customer_access_added": "_added()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L48 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_creates_a_scoped_client_login()]
- "tests_test_customer_access_testassignagent": "TestAssignAgent" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L206 | neighbors=[test_customer_access.py, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()]
- "tests_test_customer_access_testassignagent_test_assigns_agent_to_engagement": ".test_assigns_agent_to_engagement()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L207 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testassignagent_test_unknown_agent_is_404": ".test_unknown_agent_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L218 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testprovisionclientuser_test_duplicate_is_conflict": ".test_duplicate_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L114 | neighbors=[TestProvisionClientUser, _mock_db(), _operator()]
- "tests_test_customer_reveal_test_reveal_missing_user_is_404": "test_reveal_missing_user_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L48 | neighbors=[test_customer_reveal.py, _db(), _operator()]
- "tests_test_customer_reveal_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L30 | neighbors=[test_customer_reveal.py, test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_identified": ".test_mysqlx_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L54 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_not_misread_as_oracle": ".test_mysqlx_not_misread_as_oracle()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L59 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_reply_not_misread_as_mysqlx": ".test_oracle_reply_not_misread_as_mysqlx()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L70 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_still_identified": ".test_oracle_still_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L64 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-079.json

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
