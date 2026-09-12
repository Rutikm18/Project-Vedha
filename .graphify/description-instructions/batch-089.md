# Node Description Batch 90 of 380

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

- "tests_test_auth_login_testauthenticatepasswordmismatch_test_raises_password_mismatch": ".test_raises_password_mismatch()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L97 | neighbors=[TestAuthenticatePasswordMismatch, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_null_password_expires_at_never_expires": ".test_null_password_expires_at_never_expires()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L208 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_returns_user_on_valid_credentials": ".test_returns_user_on_valid_credentials()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L195 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_surface_testrobustness": "TestRobustness" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L88 | neighbors=[test_auth_surface.py, .test_body_scan_is_bounded(), .test_empty_inputs_are_survivable(), .test_none_inputs_are_survivable()]
- "tests_test_auth_surface_testvendorhint": "TestVendorHint" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L74 | neighbors=[test_auth_surface.py, .test_unknown_vendor_is_none_not_a_gues…, .test_vendor_found_in_body(), .test_vendor_found_in_realm()]
- "tests_test_branch_registry_asset_with": "_asset_with()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L150 | neighbors=[test_branch_registry.py, test_db_branch_splits_known_and_router_…, test_snmp_scanner_is_constructed_withou…, test_web_branch_passes_observed_tls_por…]
- "tests_test_branch_rule_coverage_scanners_with_rules": "_scanners_with_rules()" | kind=code-symbol | source=manager/detection_engine/tests/test_branch_rule_coverage.py:L55 | neighbors=[test_branch_rule_coverage.py, test_db_scan_is_assessed(), test_every_deep_branch_has_at_least_one…, test_exemptions_are_still_real()]
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
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_long_dead_agent_releases_its_pin": ".test_long_dead_agent_releases_its_pin()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L61 | neighbors=[The observed case: ~11 hours silent., TestPinnedAgentLiveness, _ago(), _db_heartbeat()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_restarting_probe_keeps_its_pin": ".test_restarting_probe_keeps_its_pin()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L54 | neighbors=[The 15-minute window exists so a redepl…, TestPinnedAgentLiveness, _ago(), _db_heartbeat()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_string_form_of_a_real_id_is_accepted": ".test_string_form_of_a_real_id_is_accepted()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L91 | neighbors=[Pins arrive from JSON params, so they a…, TestPinnedAgentLiveness, _ago(), _db_heartbeat()]
- "tests_test_db_posture_rules_testcleartexttransport_test_silent_on_real_tls_capable_mysql": ".test_silent_on_real_tls_capable_mysql()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L101 | neighbors=[MySQL 8.4.11 advertises CLIENT_SSL — mu…, TestCleartextTransport, _captured(), _fire()]
- "tests_test_db_posture_rules_testcontract": "TestContract" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L120 | neighbors=[test_db_posture_rules.py, .test_declared_inputs_exist_in_the_real…, .test_every_captured_engine_carries_the…, .test_requires_names_only_universal_pat…]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_tds_prelogin_testencryptionposture": "TestEncryptionPosture" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L47 | neighbors=[test_db_tds_prelogin.py, .test_not_supported_means_no_tls_at_all…, .test_off_still_supports_tls(), .test_required_is_the_hardened_case()]
- "tests_test_db_tds_prelogin_testrequestiswellformed": "TestRequestIsWellFormed" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L99 | neighbors=[test_db_tds_prelogin.py, The malformed original could not elicit…, .test_header_length_matches_body(), .test_option_table_parses_and_offsets_a…]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L1 | neighbors=[e8262a3 feat(probe): explicit unauthent…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_default_cred_rule_testrulefires_test_evidence_explains_what_was_not_tested": ".test_evidence_explains_what_was_not_tested()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L77 | neighbors=[The finding must read as a candidate, n…, TestRuleFires, _fact(), _rule()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-089.json

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
