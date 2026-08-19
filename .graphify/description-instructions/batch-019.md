# Node Description Batch 20 of 227

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

- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "exploit_orchestrator_rationale_104": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L104 | neighbors=[.validate_safety(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_111": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L111 | neighbors=[.validate_scope(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_131": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L131 | neighbors=[.execute(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_253": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L253 | neighbors=[.generate_dns_callback_token(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_266": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L266 | neighbors=[._check_blast_radius(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_297": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L297 | neighbors=[._check_approval_required(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_43": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L43 | neighbors=[ExploitOrchestrator, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_68": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L68 | neighbors=[.select_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()]
- "main_scripts_accuracy": "accuracy.py" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "main_scripts_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]
- "main_scripts_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L401 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()]
- "main_scripts_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[agent_recommendation.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, TimestampMixin, Per-engagement SIEM + EDR connection se…, Base, TimestampMixin]
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()]
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig]
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus]
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus]
- "routers_agents_agent_can_execute_job": "_agent_can_execute_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L160 | neighbors=[agents.py, _job_reachability_scope(), _required_scan_type(), _scope_is_reachable(), enqueue_agent_job(), get_agent_jobs()]
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L221 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "routers_agents_get_job_status": "get_job_status()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L943 | neighbors=[agents.py, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…]
- "runtimeerror": "RuntimeError" | kind=code-symbol | neighbors=[LeaseLostError, HWBindError, AgentUnavailableError, LLMUnavailableError, StartupAbortError, PassiveListenerError]
- "scanner_accuracy": "accuracy.py" | kind=code-symbol | source=probe/scanner/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, c5ebd38 feat(sla): per-tenant custom SL…, config.py, compute(), default_windows(), SlaResult]
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET]
- "tests_test_agent_dispatch": "test_agent_dispatch.py" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, _claim_fixture(), TestAgentWebSocketAuthentication]
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, agent.py, engine.py, transport.py, _cached_transport()]
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard]
- "tests_test_ai_normalizer_testproposecandidates": "TestProposeCandidates" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L153 | neighbors=[test_ai_normalizer.py, .test_ai_assisted_flag_set_on_candidate…, .test_cache_hit_bypasses_client(), .test_client_failure_returns_empty(), .test_malformed_response_missing_produc…, .test_malformed_response_not_a_list_ret…]
- "tests_test_attack_path_correlation_get": "_get()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L19 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_device_role_from_facts_also_amplif…, test_exposed_db_with_unauth_is_critical…, test_legacy_windows_smbv1_plus_rdp(), test_ntlm_relay_high_when_smbv1_also_en…]
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, .test_run_without_connection_returns_em…, .test_run_write_noop_without_connection…, .test_sync_to_neo4j_noop_without_client…, PathAnalyzer, GraphBuilder]
- "tests_test_auth_login_teststartupdiagnostics": "TestStartupDiagnostics" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L251 | neighbors=[test_auth_login.py, .test_bcrypt_round_trip_passes(), .test_cookie_config_fatal_in_production…, .test_cookie_config_ok_in_development(), .test_database_check_returns_fatal_on_c…, .test_jwt_secret_known_weak_is_fatal()]
- "tests_test_customer_access_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L23 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()]
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
