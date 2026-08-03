# Node Description Batch 14 of 131

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "exploit_orchestrator_rationale_131": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L131 | neighbors=[.execute(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_253": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L253 | neighbors=[.generate_dns_callback_token(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_266": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L266 | neighbors=[._check_blast_radius(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_297": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L297 | neighbors=[._check_approval_required(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_43": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L43 | neighbors=[ExploitOrchestrator, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_68": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L68 | neighbors=[.select_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, PageShell.tsx, PageShell(), EnrollmentRequest, fetchJson(), FleetPage()] | lang=en
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError] | lang=en
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()] | lang=en
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult] | lang=en
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()] | lang=en
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[agent_recommendation.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…] | lang=en
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, TimestampMixin, Per-engagement SIEM + EDR connection se…, Base, TimestampMixin] | lang=en
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()] | lang=en
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig] | lang=en
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L270 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType] | lang=en
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), PortScanner] | lang=en
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L68 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()] | lang=en
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), ServiceBannerScanner] | lang=en
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated] | lang=en
- "services_llm_airuntimeerror": "AiRuntimeError" | kind=code-symbol | source=manager/backend/app/services/llm.py:L21 | neighbors=[llm.py, RuntimeError, .__init__(), ._ensure_installed_ollama_model(), .generate(), ._runtime()] | lang=en
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET] | lang=en
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard] | lang=en
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, .test_run_without_connection_returns_em…, .test_run_write_noop_without_connection…, .test_sync_to_neo4j_noop_without_client…, PathAnalyzer, GraphBuilder] | lang=en
- "tests_test_auth_login_teststartupdiagnostics": "TestStartupDiagnostics" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L251 | neighbors=[test_auth_login.py, .test_bcrypt_round_trip_passes(), .test_cookie_config_fatal_in_production…, .test_cookie_config_ok_in_development(), .test_database_check_returns_fatal_on_c…, .test_jwt_secret_known_weak_is_fatal()] | lang=en
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing] | lang=en
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_exploit_engine_rationale_420": "Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L420 | neighbors=[TestMetasploitIntegration, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=pt
- "tests_test_exploit_engine_rationale_465": "Register --msf-host CLI option for integration tests." | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L465 | neighbors=[pytest_addoption(), MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=probe/tests/test_http_lease.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, engine.py, transport.py, test_engine_cancellation_stops_async_sc…] | lang=en
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()] | lang=en
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L402 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_permanent_client_errors_are_marke…, .test_retryable_client_errors_return_fa…] | lang=en
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()] | lang=en
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…] | lang=en
- "verify_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, verifyOtp(), addUser(), getUser(), POST()] | lang=en
- "vuln_enrichment_ttlcache": "TTLCache" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L27 | neighbors=[enrichment.py, LRU + TTL eviction. Expired keys are pu…, OrderedDict, .__contains__(), .get(), .__getitem__()] | lang=en
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, AgentConnectionManager, ConnectionManager] | lang=en
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L292 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-013.json

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
