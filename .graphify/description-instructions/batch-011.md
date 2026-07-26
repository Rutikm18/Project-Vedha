# Node Description Batch 12 of 104

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

- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context(), sync_epss_snapshot()]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]
- "e2e_mock_manager": "mock_manager.py" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, b64e(), _make_handler(), ManagerState, _QuietServer, _self_signed()]
- "e2e_mock_manager_managerstate": "ManagerState" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L44 | neighbors=[mock_manager.py, .ingest(), .__init__(), .mgr_box_pub_b64(), .mgr_sig_pub_b64(), ._mint_scope_token()]
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L70 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()]
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L131 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()]
- "enum": "Enum" | kind=code-symbol | neighbors=[agent.py, JobType, models.py, FindingState, SourceConfidence, verifier.py]
- "frontend_middleware": "middleware.ts" | kind=code-symbol | source=manager/frontend/middleware.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, config, isPublic(), middleware(), PUBLIC_PATHS]
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder]
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()]
- "lib_findings_store_createfinding": "createFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L114 | neighbors=[route.ts, findings-store.ts, saveFindings(), route.ts, route.ts, route.ts]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw]
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, clients-store.ts, Client, getClientBySubdomain(), tenant.ts, clientFromRequest()]
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()]
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig]
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, run_scan.py, _build_get(), _extract_sysdescr(), main()]
- "scanner_vulncheck_correlate": "Correlate()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L140 | neighbors=[vulncheck.go, checkDB(), checkService(), checkTLS(), checkUDP(), checkWeb()]
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, backend.ts, backend(), with-backend.ts, withBackend(), ApiSlaItem]
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard]
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L90 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing]
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L796 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_ot_passive()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, task_runner.py, _fake_run_scan(), runner(), TestRunnerHeadless, TestRunnerScanTypes]
- "websocket_manager_connectionmanager": "ConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L25 | neighbors=[manager.py, .broadcast(), .connect(), .disconnect(), .get_room_clients(), .__init__()]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, test_probe_core.py, scanner_base.py, CacheEntry]
- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=probe/workflow/cache.py:L78 | neighbors=[cache.py, In-memory (host, port, scanner) -> Cach…, .all_entries_for_host(), .get(), .__init__(), ._load()]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…, 2885afa Add comprehensive probe testing…]
- "app_main": "main.py" | kind=code-symbol | source=manager/backend/app/main.py:L1 | neighbors=[config.py, dependencies.py, GzipRequestMiddleware, lifespan(), _root_redirect(), unhandled_exception_handler()]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…]
- "cli_auth_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L46 | neighbors=[auth.ts, serverUrl(), admin.ts, engagement.ts, interactive.ts, report.ts]
- "cli_llm_client": "client()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L10 | neighbors=[llm.ts, commentOnStage(), explainFindings(), planExploit(), recommendNextPhase(), streamAsk()]
- "commands_interactive_picktargets": "pickTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L226 | neighbors=[interactive.ts, ask(), choose(), confirm(), detectLocalSubnet(), inferHostsFromFindings()]
- "commands_interactive_wizardengagement": "wizardEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1772 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), divider(), fetchEngagements()]
- "commands_interactive_wizardreport": "wizardReport()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1850 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-011.json

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
