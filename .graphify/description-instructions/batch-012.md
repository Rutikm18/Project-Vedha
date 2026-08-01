# Node Description Batch 13 of 119

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

- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), run_detection_job()]
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context(), sync_epss_snapshot()]
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _content_hash(), _default_products(), load_snapshot(), SnapshotMeta]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]
- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, MetasploitRPCError, ApprovalRequiredError]
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, ManagerAiResponse, POST(), backend.ts, backend(), BackendError]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "exploit_orchestrator_rationale_104": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L104 | neighbors=[MetasploitRPCClient, .validate_safety(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_111": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L111 | neighbors=[MetasploitRPCClient, .validate_scope(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_131": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L131 | neighbors=[MetasploitRPCClient, .execute(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_253": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L253 | neighbors=[MetasploitRPCClient, .generate_dns_callback_token(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_266": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L266 | neighbors=[MetasploitRPCClient, ._check_blast_radius(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_297": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L297 | neighbors=[MetasploitRPCClient, ._check_approval_required(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_43": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L43 | neighbors=[MetasploitRPCClient, ExploitOrchestrator, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_68": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L68 | neighbors=[MetasploitRPCClient, .select_exploit(), ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()]
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, agent_recommendation.py, Base]
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, Base, TimestampMixin, TimestampMixin, Per-engagement SIEM + EDR connection se…]
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()]
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig]
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, ADAssessmentRunner, BaseModel, Engagement, FindingSeverity, FindingStatus]
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, ADAssessmentRunner, BaseModel, Engagement, FindingSeverity, FindingStatus]
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, config.py, database.py, _agent_token_from_websocket()]
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L252 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType]
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), PortScanner]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L68 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), ServiceBannerScanner]
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated]
- "services_llm_airuntimeerror": "AiRuntimeError" | kind=code-symbol | source=manager/backend/app/services/llm.py:L21 | neighbors=[llm.py, Settings, RuntimeError, AiGenerateRequest, AiProviderStatus, AiStatusResponse]
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET]
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard]
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing]
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-012.json

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
