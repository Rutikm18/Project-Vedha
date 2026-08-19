# Node Description Batch 19 of 227

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

- "tests_test_main_scripts_ja4s": "test_main_scripts_ja4s.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _ext(), _serverhello(), test_empty_extensions_sentinel(), test_extension_hash_is_order_sensitive(), test_ja4s_from_bad_serverhello_is_none()]
- "tests_test_os_fingerprint_testfingerprintos": "TestFingerprintOs" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L224 | neighbors=[test_os_fingerprint.py, .test_mss_flags_jumbo_even_without_os_s…, .test_mss_flags_tunnel_or_vpn(), .test_mss_is_path_intel_not_an_os_signa…, .test_mss_yields_ethernet_mtu(), .test_network_device_from_ttl_255()]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L145 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L745 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_scan_funnel_testscanfunnel": "TestScanFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L119 | neighbors=[test_scan_funnel.py, .test_db_scanner_invoked_with_db_port(), .test_db_scanner_not_invoked_without_db…, .test_dead_host_forced_runs_full(), .test_dead_host_skips_port_scan(), .test_deep_scanner_receives_only_open_p…]
- "tests_test_seed_admin": "test_seed_admin.py" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, seed_admin.py, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset]
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L118 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, ._consume_stdout(), ._partial_or_raise(), ._read_stderr()]
- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode()]
- "ad_orchestrator_rationale_1": "ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[orchestrator.py, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "ad_orchestrator_rationale_40": "Coordinates all AD checkers for a single engagement." | kind=entity | source=manager/backend/app/ad/orchestrator.py:L40 | neighbors=[ADAssessmentRunner, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "ad_orchestrator_rationale_63": "Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L63 | neighbors=[.run(), ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=probe/agent/agent.py:L918 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet(), Detect common debugging/tracing tools. …, Detect common debugging/tracing tools. …]
- "agent_agent_load_or_create_identity": "_load_or_create_identity()" | kind=code-symbol | source=probe/agent/agent.py:L966 | neighbors=[agent.py, say(), _obtain_identity(), Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L55 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L196 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()]
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), RuntimeError, Raised when the Anthropic SDK or API ke…, AgentRecommendation, Asset]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "assistant_advisorflow": "AdvisorFlow.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L1 | neighbors=[AdvisorFlow(), CommandRow(), CopyButton(), PATCH_PILL, RichText(), Section()]
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_device_access_token(), create_refresh_token(), decode_token(), _now()]
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L58 | neighbors=[middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware, GzipRequestMiddleware]
- "chat_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L1 | neighbors=[ManagerAiResponse, POST(), backend.ts, backend(), BackendError, bearerFrom()]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR]
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@00c6648b4d38308e37ce245514b25f99cb5b3ae9": "00c6648 feat(settings): editable email/Slack/Jira integrations wired to backend…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, testing/all-features, 6be8259 feat(integrations): outbox deli…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bc08715ed9a3be7d600b4595a6872f649784fd00": "bc08715 feat(agent): risk-tier action classification (fail-closed)" | kind=Commit | source=git | neighbors=[3569103 docs(agent): research + design …, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@ecbb4adbc9733f25281faa5986dbcfdc1e7520ae": "ecbb4ad feat(agent): rules-of-engagement policy evaluation (verdict-vs-action, …" | kind=Commit | source=git | neighbors=[bc08715 feat(agent): risk-tier action c…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main]
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender]
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient]
- "detection_engine_enrichment_db": "enrichment_db.py" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _cache_key(), _clear_caches(), EpssDB, KevDB]
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context(), sync_epss_snapshot()]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-018.json

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
