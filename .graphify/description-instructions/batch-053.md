# Node Description Batch 54 of 209

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
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L1 | neighbors=[e8262a3 feat(probe): explicit unauthent…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_exploit_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L38 | neighbors=[test_exploit_engine.py, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_finding_reopen_endpoint": "test_finding_reopen_endpoint.py" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L1 | neighbors=[3c277ba feat(lifecycle): add POST /find…, _db_with(), test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_ope…]
- "tests_test_finding_schema": "test_finding_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_finding_patch_accepts_documented_m…, test_finding_patch_rejects_risk_score_a…, test_finding_summary_exposes_full_open_…]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_loaders_valid_snapshot": "_valid_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L28 | neighbors=[test_loaders.py, .test_content_hash_mismatch_raises_valu…, .test_hash_mismatch_message_truncates_h…, _write_snapshot()]
- "tests_test_main_scripts_coverage_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L23 | neighbors=[test_main_scripts_coverage.py, _mk_scanner(), .test_default_ports_are_nmap_top100_not…, .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout": "TestDefaultsAndAdaptiveTimeout" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L186 | neighbors=[test_main_scripts_coverage.py, .test_adaptive_estimator_is_shared_and_…, .test_default_ports_are_nmap_top100_not…, .test_fixed_timeout_flag_disables_the_e…]
- "tests_test_main_scripts_datastore_probe_svc": "_svc()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L15 | neighbors=[test_main_scripts_datastore_probe.py, test_elasticsearch_and_couchdb_win_over…, test_memcached_version_and_stat_identif…, test_redis_info_and_noauth_identify_as_…]
- "tests_test_main_scripts_hardening_make_smb2_error": "make_smb2_error()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L122 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), STATUS_INVALID_PARAMETER error response…, .test_error_response_not_trusted()]
- "tests_test_main_scripts_hardening_make_smb2_success": "make_smb2_success()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L113 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_main_scripts_hardening_smb2_header": "_smb2_header()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L100 | neighbors=[test_main_scripts_hardening.py, make_smb2_error(), make_smb2_success(), A 64-byte SMB2 header. Caller prepends …]
- "tests_test_main_scripts_hardening_testudpstatemodel": "TestUdpStateModel" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L42 | neighbors=[test_main_scripts_hardening.py, ._scanner(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_hardening_testudpstatemodel_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L43 | neighbors=[TestUdpStateModel, _scope(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_rdp_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L64 | neighbors=[test_main_scripts_rdp.py, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…, test_confirmed_rdp_without_nla_is_high_…]
- "tests_test_main_scripts_unauth_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L51 | neighbors=[test_main_scripts_unauth.py, test_protected_redis_raises_no_unauth_f…, test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_f…]
- "tests_test_nessus_scanner_rationale_1": "Unit tests for NessusScanner — all HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[test_nessus_scanner.py, FindingSeverity, FindingStatus, NessusScanner]
- "tests_test_nuclei_scanner_finding_line": "_finding_line()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L12 | neighbors=[test_nuclei_scanner.py, test_nonzero_exit_retains_and_marks_par…, test_run_scan_streams_jsonl_and_separat…, test_timeout_retains_findings_emitted_b…]
- "tests_test_outbox_reclaim_mock_session": "_mock_session()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L104 | neighbors=[test_outbox_reclaim.py, test_reclaim_handles_none_rowcount_from…, test_reclaim_is_noop_when_nothing_is_st…, test_reclaim_runs_both_sweeps_commits_a…]
- "tests_test_outbox_reclaim_sql": "_sql()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L20 | neighbors=[test_outbox_reclaim.py, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_requeue_stmt_makes_retryable_stran…]
- "tests_test_pipeline_testrunpipelineaiassist": "TestRunPipelineAiAssist" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L279 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default()]
- "tests_test_portal_metrics_testseveritybreakdown": "TestSeverityBreakdown" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L19 | neighbors=[test_portal_metrics.py, .test_all_buckets_present_zero_filled(), .test_open_only_excludes_closed(), .test_unknown_severity_falls_into_info()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-053.json

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
