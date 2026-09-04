# Node Description Batch 80 of 332

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

- "services_remediation_kb_recipe_for_finding": "recipe_for_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L346 | neighbors=[remediation_kb.py, Return a structured, OS-filtered remedi…, classify_finding(), os_key()]
- "services_scope_targets_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L66 | neighbors=[scope_targets.py, Return the normalized list of authorize…, _expand_requested(), _parse_networks()]
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L113 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute(), Aggregate SLA states across a set of fi…]
- "services_validation_ingest_ingest_validation_result": "ingest_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L51 | neighbors=[validation_ingest.py, apply_validation_outcome(), looks_like_validation_result(), If ``job_id`` belongs to a ValidationRe…]
- "settings_page_inlineinput": "inlineInput()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L183 | neighbors=[page.tsx, ApiKeysSection(), AuditLogSection(), IntegrationSection()]
- "supporting_research_evidence_store_identityresult": "IdentityResult" | kind=code-symbol | source=Supporting_research/evidence_store.py:L133 | neighbors=[evidence_store.py, .asset_count(), .observations_for(), resolve_identity()]
- "supporting_research_evidence_store_time_travel": "time_travel()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L378 | neighbors=[evidence_store.py, Audit-grade: what did the evidence supp…, AssetVerdict, retroactive_detect()]
- "supporting_research_test_evidence_store_ssh_obs": "ssh_obs()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L32 | neighbors=[test_evidence_store.py, build_fleet(), .test_hostname_never_overrides_a_finger…, .test_third_party_conclusions_are_kept_…]
- "tests_backend_auth_test": "backend-auth.test.ts" | kind=code-symbol | source=manager/frontend/tests/backend-auth.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, bearerFrom(), cookieFrom()]
- "tests_findings_detail_layout_test": "findings-detail-layout.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-detail-layout.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, findingsPage]
- "tests_test_accuracy_gate_testcli": "TestCli" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L205 | neighbors=[test_accuracy_gate.py, .test_cli_exits_two_on_a_corpus_error(), .test_cli_exits_zero_on_passing_corpora…, .test_cli_json_mode_is_machine_readable…]
- "tests_test_accuracy_gate_testprovenance": "TestProvenance" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L129 | neighbors=[test_accuracy_gate.py, .test_gate_counts_the_two_kinds_separat…, .test_nmap_labels_count_as_accuracy_evi…, .test_self_regression_labels_do_not()]
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
