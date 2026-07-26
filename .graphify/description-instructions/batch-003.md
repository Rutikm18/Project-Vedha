# Node Description Batch 4 of 104

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "aibrain_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L1 | neighbors=[Agent, AIBrainPage(), AnimatedMessage(), barColor(), criticalChain, defaultAgents]
- "commands_scan": "scan.ts" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L1 | neighbors=[index.ts, auth.ts, requireAuth(), llm.ts, buildScanCommand(), printAiComment()]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, pct(), Sev, SEV_STYLE, SlaItem]
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L57 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, ._banner_grab_all(), ._grab_one(), .__init__()]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), EMPTY_FORM, Engagement]
- "pipeline_pipeline": "pipeline.go" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, Fact, Job, assemble(), assembleError(), buildHostsMap()]
- "probe_pipeline": "pipeline.py" | kind=code-symbol | source=probe/pipeline.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _clean(), _Collector, _ip_key(), main(), _render_summary()]
- "reports_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, Sidebar.tsx, Sidebar(), useToast.ts, useToast()]
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[page.tsx, 298a9d4 trim frontend to 7 core pages; …, Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, page.tsx]
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_cli": "test_cli.py" | kind=code-symbol | source=probe/tests/test_cli.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, FakeClient, test_cmd_daemon_run_overrides_stale_env…, test_cmd_doctor_fails_when_no_agent_unl…, test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…]
- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L32 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…]
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L75 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1053 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L595 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L560 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L483 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1027 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testsuppressnegated": "TestSuppressNegated" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L516 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testwilsonci": "TestWilsonCi" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1008 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testsiemparsing": "TestSIEMParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L186 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_service_identifier_testserviceidentifier": "TestServiceIdentifier" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L6 | neighbors=[test_service_identifier.py, ServiceIdentifier, ._id(), .setup_method(), .test_confidence_floor_port_hint(), .test_ftp_banner()]
- "ad_orchestrator_adassessmentrunner": "ADAssessmentRunner" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L39 | neighbors=[orchestrator.py, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "ai_agent_agentdecisionengine": "AgentDecisionEngine" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L161 | neighbors=[agent.py, .available(), ._count(), ._create(), ._exec_read_tool(), .__init__()]
- "commands_interactive_choose": "choose()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L85 | neighbors=[interactive.ts, ask(), ln(), chooseNextPhase(), mainMenu(), pickEngagementId()]
- "commands_interactive_wizardscan": "wizardScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L329 | neighbors=[interactive.ts, mainMenu(), ask(), banner(), choose(), confirm()]
- "commands_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L1 | neighbors=[index.ts, buildToolsCommand(), C, ln(), showSpinner(), w()]
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L48 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), SafetyViolationError]
- "graph_builder_graphbuilder": "GraphBuilder" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L90 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph(), .build_from_db()]
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, 298a9d4 trim frontend to 7 core pages; …, route.ts, route.ts, route.ts, route.ts]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L12 | neighbors=[Engagement, enums.py, str, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "models_enums_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L76 | neighbors=[LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…, enums.py, str]
- "tests_test_ad_assessment_fakeentry": "_FakeEntry" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L36 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ad_assessment_testbloodhoundcollector": "TestBloodHoundCollector" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L356 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ad_assessment_testldapenumeratorparsing": "TestLDAPEnumeratorParsing" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L97 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_attack_paths_testpathanalyzer": "TestPathAnalyzer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L112 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_detection_core_testcleandebianversion": "TestCleanDebianVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L971 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testepssdb": "TestEpssDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L849 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testmakefindingid": "TestMakeFindingId" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L98 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testedrparsing": "TestEDRParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L241 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-003.json

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
