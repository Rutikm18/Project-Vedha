# Node Description Batch 111 of 336

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

- "tests_test_ai_normalizer_testproposecandidates_test_source_confidence_propagated_from_fact": ".test_source_confidence_propagated_from_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L218 | neighbors=[source_confidence on the resulting CPEC…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_version_none_when_absent": ".test_version_none_when_absent()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L242 | neighbors=[A candidate without a version key produ…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_version_propagated_when_present": ".test_version_propagated_when_present()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L230 | neighbors=[When the AI response includes a version…, TestProposeCandidates, _fact()]
- "tests_test_async_udp_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=probe/tests/test_async_udp.py:L23 | neighbors=[test_async_udp.py, .connection_made(), .datagram_received()]
- "tests_test_attack_path_correlation_test_cleartext_cluster_needs_two": "test_cleartext_cluster_needs_two()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L82 | neighbors=[test_attack_path_correlation.py, _get(), _ids()]
- "tests_test_auth_login_testauthenticatedisableduser_test_raises_disabled_user": ".test_raises_disabled_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L111 | neighbors=[TestAuthenticateDisabledUser, _make_db(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword": "TestAuthenticateExpiredPassword" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L135 | neighbors=[test_auth_login.py, .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testauthenticatesuccess": "TestAuthenticateSuccess" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L193 | neighbors=[test_auth_login.py, .test_null_password_expires_at_never_ex…, .test_returns_user_on_valid_credentials…]
- "tests_test_branch_registry_fake": "_fake()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L89 | neighbors=[test_branch_registry.py, test_host_level_branch_is_cached_under_…, test_service_specific_plan_matches_what…]
- "tests_test_branch_registry_test_db_branch_splits_known_and_router_discovered_ports": "test_db_branch_splits_known_and_router_discovered_ports()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L184 | neighbors=[test_branch_registry.py, The database branch is the one spec tha…, _asset_with()]
- "tests_test_branch_registry_test_host_level_branch_is_cached_under_a_null_port": "test_host_level_branch_is_cached_under_a_null_port()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L157 | neighbors=[test_branch_registry.py, smb's fact describes the host, so it mu…, _fake()]
- "tests_test_branch_registry_test_service_specific_plan_matches_what_the_engine_runs": "test_service_specific_plan_matches_what_the_engine_runs()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L111 | neighbors=[test_branch_registry.py, Before the registry, these five planned…, _fake()]
- "tests_test_branch_registry_test_snmp_scanner_is_constructed_without_a_ports_kwarg": "test_snmp_scanner_is_constructed_without_a_ports_kwarg()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L204 | neighbors=[test_branch_registry.py, SNMPScanner's signature has no `ports`;…, _asset_with()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_does_not_hijack_a_campaign_that_produced_results": ".test_does_not_hijack_a_campaign_that_produced_results()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L49 | neighbors=[The normal path must be untouched: a co…, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_partial_cancel_with_one_success_still_aggregates": ".test_partial_cancel_with_one_success_still_aggregates()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L66 | neighbors=[One good job is enough to expect a dete…, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_running_job_still_wins": ".test_running_job_still_wins()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L56 | neighbors=[Precedence: work in flight is reported …, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_test_pipeline_advances_through_every_phase": "test_pipeline_advances_through_every_phase()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L154 | neighbors=[test_campaign_progress.py, _run_scenario(), _user()]
- "tests_test_campaign_progress_test_unknown_worker_liveness_falls_back_to_patience": "test_unknown_worker_liveness_falls_back_to_patience()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L353 | neighbors=[test_campaign_progress.py, No heartbeat table (migration not yet r…, _running_run()]
- "tests_test_customer_access_added": "_added()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L48 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_creates_a_scoped_client_login()]
- "tests_test_customer_access_testassignagent": "TestAssignAgent" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L206 | neighbors=[test_customer_access.py, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()]
- "tests_test_customer_access_testassignagent_test_assigns_agent_to_engagement": ".test_assigns_agent_to_engagement()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L207 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testassignagent_test_unknown_agent_is_404": ".test_unknown_agent_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L218 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testprovisionclientuser_test_duplicate_is_conflict": ".test_duplicate_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L114 | neighbors=[TestProvisionClientUser, _mock_db(), _operator()]
- "tests_test_customer_reveal_test_reveal_missing_user_is_404": "test_reveal_missing_user_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L48 | neighbors=[test_customer_reveal.py, _db(), _operator()]
- "tests_test_customer_reveal_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L30 | neighbors=[test_customer_reveal.py, test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
- "tests_test_cve_correlation_testcli": "TestCli" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L350 | neighbors=[test_cve_correlation.py, .test_correlate_writes_findings(), .test_ingest_stdout_is_clean_json()]
- "tests_test_cve_correlation_testingestpagination": "TestIngestPagination" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L265 | neighbors=[test_cve_correlation.py, ._pages(), .test_resume()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_identified": ".test_mysqlx_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L54 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_not_misread_as_oracle": ".test_mysqlx_not_misread_as_oracle()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L59 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_reply_not_misread_as_mysqlx": ".test_oracle_reply_not_misread_as_mysqlx()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L70 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_still_identified": ".test_oracle_still_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L64 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_tns_packet": "_tns_packet()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L44 | neighbors=[test_db_scanner.py, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_db_scanner_xproto_frame": "_xproto_frame()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L39 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_testmatchcandidate_test_ai_assisted_carried_through": ".test_ai_assisted_carried_through()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L505 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_authoritative_source_confirms": ".test_authoritative_source_confirms()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L462 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_inferred_match_has_backport_note": ".test_inferred_match_has_backport_note()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L477 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_match_produces_finding": ".test_match_produces_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L446 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_match_returns_empty": ".test_no_match_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L491 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_version_returns_empty": ".test_no_version_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L434 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_unknown_product_returns_empty": ".test_unknown_product_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L441 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-110.json

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
