# Node Description Batch 6 of 104

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

- "probe_run_scan": "run_scan.py" | kind=code-symbol | source=probe/run_scan.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, main(), _orchestrate(), db_scanner.py, host_discovery.py, mass_scan.py]
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/scanner/db_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, DBScanner, main()]
- "tests_findings_store_test": "findings-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, types.ts, LiveFinding, finding-id.ts, resetCounters()]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), naabu-parser.ts, groupNaabuResults(), parseNaabuLine()]
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L174 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L166 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L925 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L296 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_integration": "test_integration.py" | kind=code-symbol | source=probe/tests/test_integration.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, result_spool.py, scope_crypt.py, scope_validator.py, task_runner.py, transport.py]
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()]
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr]
- "agent_engine": "engine.py" | kind=code-symbol | source=probe/agent/engine.py:L1 | neighbors=[_clamp(), _count_open_port_facts(), _error_result(), resolve_scan_type(), run_scan(), _targets()]
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py]
- "commands_ask": "ask.ts" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L1 | neighbors=[index.ts, auth.ts, requireAuth(), llm.ts, streamAsk(), buildAskCommand()]
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2044 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()]
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, Engagement, Finding, isActiveEngagement()]
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…]
- "lib_exploit_store": "exploit-store.ts" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest]
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, Severity, countBySeverity(), NucleiMatch]
- "lib_openvas_client": "openvas-client.ts" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, findings-store.ts, FindingSeverity, cvssToSeverity(), getTask()]
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, Base, TimestampMixin, TimestampMixin, AgentRegisterRequest]
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, DiscoveredHost, CheckOpts, checkPort()]
- "routers_ai_report_reviewrequest": "ReviewRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L49 | neighbors=[ai_report.py, RejectRequest, LLMReportGenerator, LLMUnavailableError, BaseModel, Asset]
- "routers_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dependencies.py, _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius()]
- "str": "str" | kind=code-symbol | neighbors=[JobType, FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType]
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB, IngestResult]
- "websocket_manager_agentconnectionmanager": "AgentConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L78 | neighbors=[manager.py, .agent_stale_after(), .connected_agents(), .connected_count(), .get_agent_status(), .__init__()]
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L56 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_users(), _FakeAttr, _FakeEntry]
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py]
- "commands_interactive_ask": "ask()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L39 | neighbors=[interactive.ts, choose(), confirm(), ensureAuthenticated(), pickHostSubset(), pickTargets()]
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, Base, TimestampMixin, str, AgentRegisterRequest, AgentRegisterResponse]
- "nmap_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, createVulnFindings(), NSE_VULN_MAP, NseScript, parseNmapXml()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-005.json

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
