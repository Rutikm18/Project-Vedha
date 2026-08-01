# Node Description Batch 12 of 119

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

- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L123 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L723 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, task_runner.py, _fake_run_scan(), runner(), TestRunnerHeadless]
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_workflow_execution.py, scanner_base.py, Asset]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, scanner_base.py, CacheEntry]
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()]
- "ad_orchestrator_rationale_1": "ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "ad_orchestrator_rationale_40": "Coordinates all AD checkers for a single engagement." | kind=entity | source=manager/backend/app/ad/orchestrator.py:L40 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "ad_orchestrator_rationale_63": "Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L63 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "agent_agent_maptojob": "mapToJob()" | kind=code-symbol | source=probe-go/agent/agent.go:L742 | neighbors=[agent.py, dedupStrings(), defaultScanType(), firstStr(), firstTargetList(), floatOr()]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L55 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L196 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "agent_state_test": "state_test.go" | kind=code-symbol | source=probe-go/agent/state_test.go:L1 | neighbors=[identityServerState, identityTestConfig(), newIdentityServer(), TestConfiguredIdentityRejectsPartialCre…, TestConfiguredIdentityTakesPrecedenceOv…, TestIdentityStateRejectsDifferentManage…]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), AgentRecommendation, Asset, AttackPath, Finding]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR]
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "dashboard_slarow": "SlaRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, getSla(), SEV_BG, SEV_COLOR, SlaRow(), Severity]
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender]
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), run_detection_job()]
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context(), sync_epss_snapshot()]
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _content_hash(), _default_products(), load_snapshot(), SnapshotMeta]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]
- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()]
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, MetasploitRPCError, ApprovalRequiredError]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()]
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, agent_recommendation.py, Base]
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, Base, TimestampMixin, TimestampMixin, Per-engagement SIEM + EDR connection se…]
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-011.json

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
