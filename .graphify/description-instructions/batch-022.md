# Node Description Batch 23 of 336

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

- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter]
- "scripts_startup_validator_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L34 | neighbors=[startup_validator.py, .validate(), .validate(), .validate(), .validate(), .validate()]
- "scripts_startup_validator_validationreport_add": ".add()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L45 | neighbors=[.validate(), .validate(), .validate(), .validate(), .validate(), .validate()]
- "services_llm_managerllmservice_generate": ".generate()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L328 | neighbors=[ManagerLlmService, ._build_system(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model(), ._runtime()]
- "tests_campaign_store_test": "campaign-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/campaign-store.test.ts:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, campaign-store.ts, CampaignSnapshot, getCampaign(), isSafeCampaignId(), listCampaigns()]
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput()]
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 9c54022 Refactor code structure and rem…, b4b12a9 Rename project and update files, agent.py, engine.py, transport.py]
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L731 | neighbors=[test_agents.py, Discovery results → assets/services pro…, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop(), .test_skips_host_without_ip()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, .test_d3_highlights_top_path(), .test_d3_marks_compromised(), .test_d3_shape(), .test_layout_is_deterministic(), PathAnalyzer]
- "tests_test_auth_login_make_db": "_make_db()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L69 | neighbors=[test_auth_login.py, AsyncSession mock that returns user on …, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future()]
- "tests_test_branch_registry_testregistryconsistency": "TestRegistryConsistency" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L34 | neighbors=[test_branch_registry.py, .test_branch_component_map_is_derived(), .test_catalog_entries_are_labelled(), .test_components_are_unique(), .test_every_branch_has_a_scanner_the_en…, .test_every_branch_is_gateable()]
- "tests_test_campaign_progress_progress": "_progress()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L204 | neighbors=[test_campaign_progress.py, _rows(), _scalars(), _user(), _running_run(), test_a_briefly_running_run_is_not_calle…]
- "tests_test_campaign_progress_terminal_status": "_status()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L34 | neighbors=[test_campaign_progress_terminal.py, .test_complete_campaign(), .test_complete_with_gaps(), .test_no_jobs_is_pending(), .test_uncovered_submission_keeps_it_det…, .test_a_dead_queue_is_still_reported_as…]
- "tests_test_customer_access_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L27 | neighbors=[test_customer_access.py, db.execute yields the given scalar_one_…, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement()]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_detection_pipeline_gaps": "test_detection_pipeline_gaps.py" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _ctx, _fact(), test_a_non_dict_data_payload_is_quarant…, test_accepted_facts_excludes_what_inges…, test_accepted_facts_falls_back_to_raw_w…]
- "tests_test_finding_events_testsynthesize": "TestSynthesize" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L44 | neighbors=[test_finding_events.py, .test_auto_resolution_event(), .test_detected_actor_falls_back_to_dete…, .test_detected_actor_labels_network_va_…, .test_genesis_detected_from_first_seen(), .test_manual_remediation_event()]
- "tests_test_main_scripts_ja4s": "test_main_scripts_ja4s.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _ext(), _serverhello(), test_empty_extensions_sentinel(), test_extension_hash_is_order_sensitive(), test_ja4s_from_bad_serverhello_is_none()]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_posture_rules": "test_posture_rules.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 8f6bf49 Refactor code structure and rem…, _asset(), _fact(), TestHardenedGroundTruth, TestInvariants]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L145 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L782 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_run_scoped_fact_scope_fact": "_fact()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L39 | neighbors=[test_run_scoped_fact_scope.py, .test_a_real_result_with_one_run_scoped…, .test_ipv6_discovery_auto_target_is_not…, .test_ipv6_discovery_interface_name_is_…, .test_run_scoped_fact_is_not_collected_…, .test_an_unknown_scanner_gets_no_exempt…]
- "tests_test_scan_funnel_testscanfunnel": "TestScanFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L121 | neighbors=[test_scan_funnel.py, .test_db_scanner_invoked_with_db_port(), .test_db_scanner_not_invoked_without_db…, .test_dead_host_forced_runs_full(), .test_dead_host_skips_port_scan(), .test_deep_scanner_receives_only_open_p…]
- "tests_test_scanner_congestion_testdeliveryawarebackoff": "TestDeliveryAwareBackoff" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L429 | neighbors=[test_scanner_congestion.py, Congestion control must react to a CHAN…, ._sc(), .test_collapsed_delivery_still_backs_of…, .test_floor_is_clamped(), .test_floor_is_configurable()]
- "tests_test_scanner_congestion_testreprobecleanuppass": "TestReprobeCleanupPass" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L336 | neighbors=[test_scanner_congestion.py, A host that rate-limits its RSTs answer…, ._rate_limited(), ._silent_attempt(), ._summary(), .test_cleanup_raises_the_timeout_floor()]
- "tests_test_scanner_congestion_testsendpacer": "TestSendPacer" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L38 | neighbors=[test_scanner_congestion.py, .test_backoff_is_bounded_by_min_rate(), .test_clean_round_increases_rate_additi…, .test_empty_round_is_ignored_not_treate…, .test_first_pace_does_not_block(), .test_growth_is_bounded_by_max_rate()]
- "tests_test_seed_admin": "test_seed_admin.py" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, seed_admin.py, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset]
- "tests_test_service_posture_rules_testnegatives": "TestNegatives" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L116 | neighbors=[test_service_posture_rules.py, .test_dns_refused_transfer(), .test_ftp_without_anonymous(), .test_ipmi_cipher_zero_rejected(), .test_ldap_bind_refused(), .test_nfs_restricted_exports()]
- "tests_test_smb_ldap_scanners": "test_smb_ldap_scanners.py" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, scanner_base.py, TestLDAPScanner, TestLDAPTimeoutTypes, TestMainScriptsParity]
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "tools_issue_license": "issue_license.py" | kind=code-symbol | source=probe/tools/issue_license.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 6e2818f Add support for additional serv…, d1b4dd3 trim frontend to 7 core pages; …, _b64(), issue()]
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L118 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, ._consume_stdout(), ._partial_or_raise(), ._read_stderr()]
- "workflow_branches": "branches.py" | kind=code-symbol | source=probe/workflow/branches.py:L1 | neighbors=[explain_plan.py, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, test_branch_registry.py, test_tls_port_coverage.py, BranchSpec]
- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=probe/workflow/cache.py:L99 | neighbors=[cache.py, In-memory (host, port, scanner) -> Cach…, .all_entries_for_host(), .get(), .__init__(), ._load()]
- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode()]
- "ad_orchestrator_rationale_1": "ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[orchestrator.py, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "ad_orchestrator_rationale_40": "Coordinates all AD checkers for a single engagement." | kind=entity | source=manager/backend/app/ad/orchestrator.py:L40 | neighbors=[ADAssessmentRunner, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-022.json

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
