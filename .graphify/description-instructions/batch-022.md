# Node Description Batch 23 of 330

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
- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L579 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, _bounded_env_int(), say(), Run an HTTP-claimed job while renewing …]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L57 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L198 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L398 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L776 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Establish an authenticated WebSocket co…, Establish an authenticated WebSocket co…]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L628 | neighbors=[Backwards-compatible bool form of `hear…, Transport, .heartbeat_ex(), Refresh a device token before expiry; l…, .ensure_device_access(), Send a heartbeat to the manager.       …]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L646 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L531 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L306 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L685 | neighbors=[Submit a scan result to the manager.   …, Transport, _strip_nul(), .ensure_device_access(), Submit a scan result to the manager.   …, Submit a scan result to the manager.   …]
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), RuntimeError, Raised when the Anthropic SDK or API ke…, AgentRecommendation, Asset]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L262 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "assistant_advisorflow": "AdvisorFlow.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L1 | neighbors=[AdvisorFlow(), CommandRow(), CopyButton(), PATCH_PILL, RichText(), Section()]
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_device_access_token(), create_refresh_token(), decode_token(), _now()]
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L58 | neighbors=[middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware, GzipRequestMiddleware]
- "chat_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L1 | neighbors=[ManagerAiResponse, POST(), backend.ts, backend(), BackendError, bearerFrom()]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR]

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
