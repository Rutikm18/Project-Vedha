# Node Description Batch 61 of 236

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

- "tests_test_adaptive_rate_testudpscanneradaptive": "TestUdpScannerAdaptive" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L185 | neighbors=[test_adaptive_rate.py, .test_adaptive_scanner_creates_controll…, .test_adaptive_scanner_detects_open_on_…, .test_non_adaptive_scanner_has_no_contr…]
- "tests_test_adaptive_rate_testwindowgating": "TestWindowGating" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L79 | neighbors=[test_adaptive_rate.py, .test_acquire_blocks_when_window_full(), .test_release_unblocks_waiter(), .test_report_loss_shrinks_and_releases()]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L195 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L34 | neighbors=[test_agents.py, .test_network_types_included(), .test_server_side_types_excluded(), ScanJobType]
- "tests_test_agents_testagentregistrationrefresh": "TestAgentRegistrationRefresh" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L238 | neighbors=[test_agents.py, .test_agent_can_refresh_only_its_own_ro…, .test_agent_cannot_refresh_another_iden…, ScanJobType]
- "tests_test_agents_testlistagents": "TestListAgents" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L534 | neighbors=[test_agents.py, .test_fresh_disconnected_agent_is_not_r…, .test_lists_with_online_flag(), ScanJobType]
- "tests_test_auth_login_testauthenticatebcryptfailure_test_raises_bcrypt_failure_on_passlib_error": ".test_raises_bcrypt_failure_on_passlib_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L164 | neighbors=[TestAuthenticateBcryptFailure, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatedisabledtenant_test_raises_disabled_tenant": ".test_raises_disabled_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L124 | neighbors=[TestAuthenticateDisabledTenant, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_not_expired_when_future": ".test_not_expired_when_future()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L149 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_raises_expired_password": ".test_raises_expired_password()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L137 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatepasswordmismatch_test_raises_password_mismatch": ".test_raises_password_mismatch()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L97 | neighbors=[TestAuthenticatePasswordMismatch, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_null_password_expires_at_never_expires": ".test_null_password_expires_at_never_expires()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L208 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_returns_user_on_valid_credentials": ".test_returns_user_on_valid_credentials()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L195 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_customer_access_testapprovescanrequest": "TestApproveScanRequest" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L150 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…]
- "tests_test_customer_access_testapprovescanrequest_test_approve_non_pending_is_conflict": ".test_approve_non_pending_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L180 | neighbors=[TestApproveScanRequest, _mock_db(), _operator(), _pending_request()]
- "tests_test_customer_access_testapprovescanrequest_test_approve_without_assigned_agent_is_conflict": ".test_approve_without_assigned_agent_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L169 | neighbors=[TestApproveScanRequest, _mock_db(), _operator(), _pending_request()]
- "tests_test_customer_access_testbuildscanjob": "TestBuildScanJob" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L58 | neighbors=[test_customer_access.py, .test_dispatches_on_the_assigned_agent(), .test_no_assigned_agent_raises(), .test_unknown_scan_type_falls_back_to_v…]
- "tests_test_customer_access_testprovisionclientuser": "TestProvisionClientUser" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L89 | neighbors=[test_customer_access.py, .test_creates_a_scoped_client_login(), .test_duplicate_email_in_tenant_is_conf…, .test_duplicate_is_conflict()]
- "tests_test_customer_access_testprovisionclientuser_test_creates_a_scoped_client_login": ".test_creates_a_scoped_client_login()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L90 | neighbors=[TestProvisionClientUser, _added(), _mock_db(), _operator()]
- "tests_test_customer_access_testprovisionclientuser_test_duplicate_email_in_tenant_is_conflict": ".test_duplicate_email_in_tenant_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L124 | neighbors=[An email already used elsewhere in the …, TestProvisionClientUser, _mock_db(), _operator()]
- "tests_test_customer_access_testrejectscanrequest_test_reject_records_reason": ".test_reject_records_reason()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L194 | neighbors=[TestRejectScanRequest, _mock_db(), _operator(), _pending_request()]
- "tests_test_customer_reveal_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L21 | neighbors=[test_customer_reveal.py, test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
- "tests_test_customer_reveal_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L17 | neighbors=[test_customer_reveal.py, test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
- "tests_test_customer_reveal_test_reveal_null_ciphertext_returns_none": "test_reveal_null_ciphertext_returns_none()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L42 | neighbors=[test_customer_reveal.py, _db(), _operator(), _user()]
- "tests_test_customer_reveal_test_reveal_returns_decrypted_password": "test_reveal_returns_decrypted_password()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L35 | neighbors=[test_customer_reveal.py, _db(), _operator(), _user()]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L1 | neighbors=[e8262a3 feat(probe): explicit unauthent…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_exploit_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L38 | neighbors=[test_exploit_engine.py, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_finding_reopen_endpoint": "test_finding_reopen_endpoint.py" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L1 | neighbors=[3c277ba feat(lifecycle): add POST /find…, _db_with(), test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_ope…]
- "tests_test_finding_schema": "test_finding_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_finding_patch_accepts_documented_m…, test_finding_patch_rejects_risk_score_a…, test_finding_summary_exposes_full_open_…]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_integrations_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L21 | neighbors=[test_integrations.py, .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_integrations_testputintegration": "TestPutIntegration" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L31 | neighbors=[test_integrations.py, .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_loaders_valid_snapshot": "_valid_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L28 | neighbors=[test_loaders.py, .test_content_hash_mismatch_raises_valu…, .test_hash_mismatch_message_truncates_h…, _write_snapshot()]
- "tests_test_main_scripts_coverage_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L23 | neighbors=[test_main_scripts_coverage.py, _mk_scanner(), .test_default_ports_are_nmap_top100_not…, .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout": "TestDefaultsAndAdaptiveTimeout" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L186 | neighbors=[test_main_scripts_coverage.py, .test_adaptive_estimator_is_shared_and_…, .test_default_ports_are_nmap_top100_not…, .test_fixed_timeout_flag_disables_the_e…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-060.json

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
