# Node Description Batch 7 of 119

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

- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 95904f1 feat(probe): detect SMB signing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main()]
- "services_llm_managerllmservice": "ManagerLlmService" | kind=code-symbol | source=manager/backend/app/services/llm.py:L64 | neighbors=[llm.py, Settings, AiGenerateRequest, AiProviderStatus, AiStatusResponse, ._anthropic()]
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L174 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L166 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L925 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L296 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator]
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, transport.py, TestFetchScope, TestHeartbeat]
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr]
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()]
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py]
- "app_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L1 | neighbors=[metadata, RootLayout(), AssistantProvider.tsx, AssistantProvider(), QueryProvider.tsx, QueryProvider()]
- "assistant_assistantdrawer": "AssistantDrawer.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L1 | neighbors=[AssistantDrawer(), Msg, AssistantProvider.tsx, useAssistant(), AssistantText.tsx, AssistantText()]
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()]
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…]
- "lib_assistant": "assistant.ts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, 1fe16c8 stable but some dead code, need…, cveRecordToFactCard()]
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[ask.ts, findings.ts, interactive.ts, findings-store.ts, deleteFinding(), ensureDir()]
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()]
- "lib_scanner_request_validation": "scanner-request-validation.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L1 | neighbors=[b4b12a9 Rename project and update files, isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest]
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, Base, TimestampMixin, TimestampMixin, AgentRegisterRequest]
- "routers_ai_report_reviewrequest": "ReviewRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L49 | neighbors=[ai_report.py, RejectRequest, LLMReportGenerator, LLMUnavailableError, BaseModel, Asset]
- "routers_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, configure_siem(), get_coverage(), get_gaps()]
- "routers_vuln_scans_findingimport": "FindingImport" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L49 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nessusscanrequest": "NessusScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L35 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nucleiscanrequest": "NucleiScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L43 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _auth_shaped_json_body(), _known_false_positive(), main()]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _get_cert_der(), main()]
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _fetch()]
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB, IngestResult]
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, currentPlatform(), Platform, TOOL_MANIFEST]
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L55 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_users(), _FakeAttr, _FakeEntry]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-006.json

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
