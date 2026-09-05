# Node Description Batch 81 of 336

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

- "tests_test_agents_testlistagents": "TestListAgents" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L564 | neighbors=[test_agents.py, .test_fresh_disconnected_agent_is_not_r…, .test_lists_with_online_flag(), ScanJobType]
- "tests_test_auth_login_testauthenticatebcryptfailure_test_raises_bcrypt_failure_on_passlib_error": ".test_raises_bcrypt_failure_on_passlib_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L164 | neighbors=[TestAuthenticateBcryptFailure, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatedisabledtenant_test_raises_disabled_tenant": ".test_raises_disabled_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L124 | neighbors=[TestAuthenticateDisabledTenant, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_not_expired_when_future": ".test_not_expired_when_future()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L149 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_raises_expired_password": ".test_raises_expired_password()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L137 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatepasswordmismatch_test_raises_password_mismatch": ".test_raises_password_mismatch()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L97 | neighbors=[TestAuthenticatePasswordMismatch, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_null_password_expires_at_never_expires": ".test_null_password_expires_at_never_expires()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L208 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_returns_user_on_valid_credentials": ".test_returns_user_on_valid_credentials()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L195 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_branch_registry_asset_with": "_asset_with()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L150 | neighbors=[test_branch_registry.py, test_db_branch_splits_known_and_router_…, test_snmp_scanner_is_constructed_withou…, test_web_branch_passes_observed_tls_por…]
- "tests_test_campaign_progress_test_a_briefly_running_run_with_a_dead_worker_is_still_given_a_moment": "test_a_briefly_running_run_with_a_dead_worker_is_still_given_a_moment()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L345 | neighbors=[test_campaign_progress.py, Under the floor: a heartbeat gap of a f…, _beat(), _running_run()]
- "tests_test_campaign_progress_test_a_dead_worker_is_called_out_quickly": "test_a_dead_worker_is_called_out_quickly()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L336 | neighbors=[test_campaign_progress.py, No patience needed when the thing that …, _beat(), _running_run()]
- "tests_test_campaign_progress_test_a_long_run_with_a_live_worker_is_not_stalled": "test_a_long_run_with_a_live_worker_is_not_stalled()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L326 | neighbors=[test_campaign_progress.py, THE CRY-WOLF CASE. 90 minutes in, worke…, _beat(), _running_run()]
- "tests_test_campaign_progress_test_campaign_progress_aggregates_jobs_detection_and_findings": "test_campaign_progress_aggregates_jobs_detection_and_findings()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L31 | neighbors=[test_campaign_progress.py, _rows(), _scalars(), _user()]
- "tests_test_campaign_progress_test_campaign_progress_no_detection_yet_is_scanning": "test_campaign_progress_no_detection_yet_is_scanning()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L92 | neighbors=[test_campaign_progress.py, _rows(), _scalars(), _user()]
- "tests_test_campaign_progress_test_completed_run_is_not_stuck_at_detecting": "test_completed_run_is_not_stuck_at_detecting()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L167 | neighbors=[test_campaign_progress.py, Regression: RUN_COMPLETED is 'completed…, _run_scenario(), _user()]
- "tests_test_campaign_progress_test_full_coverage_completes_at_100": "test_full_coverage_completes_at_100()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L255 | neighbors=[test_campaign_progress.py, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_stall_never_claims_completion_either_way": "test_stall_never_claims_completion_either_way()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L366 | neighbors=[test_campaign_progress.py, Whatever the verdict, a stalled run mus…, _beat(), _running_run()]
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
- "tests_test_cve_correlation_testingestfeeds": "TestIngestFeeds" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L294 | neighbors=[test_cve_correlation.py, .test_epss_tolerates_plain_csv(), .test_ingest_all_stamps_last_ingest(), .test_kev_and_epss()]
- "tests_test_cve_correlation_testriskscore": "TestRiskScore" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L150 | neighbors=[test_cve_correlation.py, .test_bands(), .test_capped_at_100(), .test_kev_and_exposure_weight()]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L1 | neighbors=[e8262a3 feat(probe): explicit unauthent…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_detection_coverage_job": "_job()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L30 | neighbors=[test_detection_coverage.py, test_aggregating_reason_names_the_outbo…, test_completed_no_blind_is_plain_comple…, test_completed_with_blind_rules_is_comp…]
- "tests_test_detection_coverage_rows": "_rows()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L26 | neighbors=[test_detection_coverage.py, test_aggregating_reason_names_the_outbo…, test_completed_no_blind_is_plain_comple…, test_completed_with_blind_rules_is_comp…]
- "tests_test_detection_coverage_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L22 | neighbors=[test_detection_coverage.py, test_aggregating_reason_names_the_outbo…, test_completed_no_blind_is_plain_comple…, test_completed_with_blind_rules_is_comp…]
- "tests_test_detection_pipeline_gaps_test_facts_ready_reads_scanner_runs_from_the_job": "test_facts_ready_reads_scanner_runs_from_the_job()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L96 | neighbors=[test_detection_pipeline_gaps.py, scan_results has no scanner_runs column…, _ctx, _fact()]
- "tests_test_detection_pipeline_gaps_test_missing_scanner_runs_degrades_to_empty_coverage": "test_missing_scanner_runs_degrades_to_empty_coverage()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L125 | neighbors=[test_detection_pipeline_gaps.py, An older probe reports none. Coverage s…, _ctx, _fact()]
- "tests_test_dns_scanner_testdnsfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L126 | neighbors=[TestDNSFindings, .test_dnssec_absent_only_for_confirmed_…, .test_secure_server_silent(), .test_zone_transfer_version_and_unsigne…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-080.json

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
