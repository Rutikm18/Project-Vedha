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

- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L166 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L925 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L296 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator]
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()]
- "vuln_nuclei_nucleirunreport": "NucleiRunReport" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L79 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Run Nuclei and always leave its job in …, _FakeSession]
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr]
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()]
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py]
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), backend.ts]
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()]
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…]
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[ask.ts, findings.ts, interactive.ts, findings-store.ts, deleteFinding(), ensureDir()]
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()]
- "lib_scanner_request_validation": "scanner-request-validation.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L1 | neighbors=[b4b12a9 Rename project and update files, isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest]
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, Base, TimestampMixin, TimestampMixin, AgentRegisterRequest]
- "pipeline_pipeline_run": "Run()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L85 | neighbors=[pipeline.go, assemble(), assembleError(), clamp(), clampInt(), factsAsMaps()]
- "routers_ai_report_reviewrequest": "ReviewRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L49 | neighbors=[ai_report.py, RejectRequest, LLMReportGenerator, LLMUnavailableError, BaseModel, Asset]
- "routers_vuln_scans_findingimport": "FindingImport" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L50 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nessusscanrequest": "NessusScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L36 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nucleiscanrequest": "NucleiScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L44 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _auth_shaped_json_body(), _known_false_positive(), main()]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _get_cert_der(), main()]
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _fetch()]
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB, IngestResult]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, transport.py, TestFetchScope, TestHeartbeat, TestHttpGet]
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, currentPlatform(), Platform, TOOL_MANIFEST]
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L56 | neighbors=[ldap_enum.py, ADConnectionError, DependencyMissingError, .get_users(), _FakeAttr, _FakeEntry]
- "commands_interactive_ask": "ask()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L39 | neighbors=[interactive.ts, choose(), confirm(), ensureAuthenticated(), pickHostSubset(), pickTargets()]
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), CPECandidate, normalize()]
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult]
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()]
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()]
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, Base, TimestampMixin, str, AgentRegisterRequest, AgentRegisterResponse]
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult]
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L43 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, BaseModel, Asset, AttackPath]

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
