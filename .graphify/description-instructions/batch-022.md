# Node Description Batch 23 of 332

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
- "tests_test_scanner_congestion_scanner": "_scanner()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L138 | neighbors=[test_scanner_congestion.py, .test_all_silent_host_shrinks_the_windo…, .test_congestion_can_be_disabled(), .test_responsive_host_is_not_throttled(), .test_scan_completes_every_port_under_t…, .test_cleanup_raises_the_timeout_floor()]
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
- "ad_orchestrator_rationale_63": "Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L63 | neighbors=[.run(), ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L58 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()]
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L813 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L57 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L198 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L398 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L141 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state(), Durably replace one private JSON state …, Durably replace one private JSON state …]
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), RuntimeError, Raised when the Anthropic SDK or API ke…, AgentRecommendation, Asset]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L262 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "assistant_advisorflow": "AdvisorFlow.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L1 | neighbors=[AdvisorFlow(), CommandRow(), CopyButton(), PATCH_PILL, RichText(), Section()]
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_device_access_token(), create_refresh_token(), decode_token(), _now()]

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
