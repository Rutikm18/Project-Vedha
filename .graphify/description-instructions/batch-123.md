# Node Description Batch 124 of 380

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

- "tests_test_auth_login_testauthenticatedisableduser_test_raises_disabled_user": ".test_raises_disabled_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L111 | neighbors=[TestAuthenticateDisabledUser, _make_db(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword": "TestAuthenticateExpiredPassword" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L135 | neighbors=[test_auth_login.py, .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testauthenticatesuccess": "TestAuthenticateSuccess" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L193 | neighbors=[test_auth_login.py, .test_null_password_expires_at_never_ex…, .test_returns_user_on_valid_credentials…]
- "tests_test_branch_registry_fake": "_fake()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L89 | neighbors=[test_branch_registry.py, test_host_level_branch_is_cached_under_…, test_service_specific_plan_matches_what…]
- "tests_test_branch_registry_test_db_branch_splits_known_and_router_discovered_ports": "test_db_branch_splits_known_and_router_discovered_ports()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L184 | neighbors=[test_branch_registry.py, The database branch is the one spec tha…, _asset_with()]
- "tests_test_branch_registry_test_host_level_branch_is_cached_under_a_null_port": "test_host_level_branch_is_cached_under_a_null_port()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L157 | neighbors=[test_branch_registry.py, smb's fact describes the host, so it mu…, _fake()]
- "tests_test_branch_registry_test_service_specific_plan_matches_what_the_engine_runs": "test_service_specific_plan_matches_what_the_engine_runs()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L111 | neighbors=[test_branch_registry.py, Before the registry, these five planned…, _fake()]
- "tests_test_branch_registry_test_snmp_scanner_is_constructed_without_a_ports_kwarg": "test_snmp_scanner_is_constructed_without_a_ports_kwarg()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L204 | neighbors=[test_branch_registry.py, SNMPScanner's signature has no `ports`;…, _asset_with()]
- "tests_test_branch_rule_coverage_branch_components": "_branch_components()" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L46 | neighbors=[test_branch_rule_coverage.py, test_every_deep_branch_has_at_least_one…, test_exemptions_name_real_branches()]
- "tests_test_branch_rule_coverage_test_db_scan_is_assessed": "test_db_scan_is_assessed()" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L85 | neighbors=[test_branch_rule_coverage.py, The regression this whole file exists f…, _scanners_with_rules()]
- "tests_test_branch_rule_coverage_test_every_deep_branch_has_at_least_one_rule": "test_every_deep_branch_has_at_least_one_rule()" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L62 | neighbors=[test_branch_rule_coverage.py, _branch_components(), _scanners_with_rules()]
- "tests_test_branch_rule_coverage_test_exemptions_are_still_real": "test_exemptions_are_still_real()" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L71 | neighbors=[test_branch_rule_coverage.py, An exemption that has since gained a ru…, _scanners_with_rules()]
- "tests_test_branch_rule_coverage_test_exemptions_name_real_branches": "test_exemptions_name_real_branches()" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L79 | neighbors=[test_branch_rule_coverage.py, A typo here would silently exempt nothi…, _branch_components()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_does_not_hijack_a_campaign_that_produced_results": ".test_does_not_hijack_a_campaign_that_produced_results()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L49 | neighbors=[The normal path must be untouched: a co…, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_partial_cancel_with_one_success_still_aggregates": ".test_partial_cancel_with_one_success_still_aggregates()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L66 | neighbors=[One good job is enough to expect a dete…, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_running_job_still_wins": ".test_running_job_still_wins()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L56 | neighbors=[Precedence: work in flight is reported …, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_test_pipeline_advances_through_every_phase": "test_pipeline_advances_through_every_phase()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L154 | neighbors=[test_campaign_progress.py, _run_scenario(), _user()]
- "tests_test_campaign_progress_test_unknown_worker_liveness_falls_back_to_patience": "test_unknown_worker_liveness_falls_back_to_patience()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L353 | neighbors=[test_campaign_progress.py, No heartbeat table (migration not yet r…, _running_run()]
- "tests_test_connect_test_admit_job_enforces_local_scope_after_signature": "test_admit_job_enforces_local_scope_after_signature()" | kind=code-symbol | source=probe/tests/test_connect.py:L85 | neighbors=[test_connect.py, _keypair(), _signed()]
- "tests_test_connect_test_expired_job_is_rejected": "test_expired_job_is_rejected()" | kind=code-symbol | source=probe/tests/test_connect.py:L69 | neighbors=[test_connect.py, _keypair(), _signed()]
- "tests_test_connect_test_tampered_job_is_rejected": "test_tampered_job_is_rejected()" | kind=code-symbol | source=probe/tests/test_connect.py:L60 | neighbors=[test_connect.py, _keypair(), _signed()]
- "tests_test_connect_test_valid_signed_job_verifies": "test_valid_signed_job_verifies()" | kind=code-symbol | source=probe/tests/test_connect.py:L53 | neighbors=[test_connect.py, _keypair(), _signed()]
- "tests_test_connect_test_wrong_contract_version_is_rejected": "test_wrong_contract_version_is_rejected()" | kind=code-symbol | source=probe/tests/test_connect.py:L77 | neighbors=[test_connect.py, _keypair(), _signed()]
- "tests_test_customer_access_added": "_added()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L48 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_creates_a_scoped_client_login()]
- "tests_test_customer_access_testassignagent": "TestAssignAgent" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L206 | neighbors=[test_customer_access.py, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()]
- "tests_test_customer_access_testassignagent_test_assigns_agent_to_engagement": ".test_assigns_agent_to_engagement()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L207 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testassignagent_test_unknown_agent_is_404": ".test_unknown_agent_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L218 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testprovisionclientuser_test_duplicate_is_conflict": ".test_duplicate_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L114 | neighbors=[TestProvisionClientUser, _mock_db(), _operator()]
- "tests_test_customer_reveal_test_reveal_missing_user_is_404": "test_reveal_missing_user_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L48 | neighbors=[test_customer_reveal.py, _db(), _operator()]
- "tests_test_customer_reveal_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L30 | neighbors=[test_customer_reveal.py, test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
- "tests_test_cve_correlation_testcli": "TestCli" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L350 | neighbors=[test_cve_correlation.py, .test_correlate_writes_findings(), .test_ingest_stdout_is_clean_json()]
- "tests_test_cve_correlation_testingestpagination": "TestIngestPagination" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L265 | neighbors=[test_cve_correlation.py, ._pages(), .test_resume()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_boundary_is_the_configured_window": ".test_boundary_is_the_configured_window()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L67 | neighbors=[TestPinnedAgentLiveness, _ago(), _db_heartbeat()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_recently_seen_agent_is_live": ".test_recently_seen_agent_is_live()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L49 | neighbors=[TestPinnedAgentLiveness, _ago(), _db_heartbeat()]
- "tests_test_db_mysql_greeting_testidentification": "TestIdentification" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L33 | neighbors=[test_db_mysql_greeting.py, .test_non_mysql_is_rejected(), .test_version_and_protocol()]
- "tests_test_db_mysql_greeting_testtlsposture_test_client_ssl_absent_means_cleartext": ".test_client_ssl_absent_means_cleartext()" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L51 | neighbors=[Flags present and CLIENT_SSL clear — a …, TestTLSPosture, _greeting()]
- "tests_test_db_mysql_greeting_testtlsposture_test_short_packet_claims_nothing": ".test_short_packet_claims_nothing()" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L56 | neighbors=[Absent evidence must not become a clear…, TestTLSPosture, _greeting()]
- "tests_test_db_posture_rules_testcleartexttransport_test_silent_when_the_probe_never_learned_it": ".test_silent_when_the_probe_never_learned_it()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L106 | neighbors=[Absent evidence is not a cleartext find…, TestCleartextTransport, _fire()]
- "tests_test_db_posture_rules_testunauthenticatedaccess_test_fires_on_real_open_mongodb": ".test_fires_on_real_open_mongodb()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L63 | neighbors=[TestUnauthenticatedAccess, _captured(), _fire()]
- "tests_test_db_posture_rules_testunauthenticatedaccess_test_fires_on_real_open_redis": ".test_fires_on_real_open_redis()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L57 | neighbors=[TestUnauthenticatedAccess, _captured(), _fire()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-123.json

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
