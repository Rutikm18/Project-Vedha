# Node Description Batch 5 of 104

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

- "tests_test_exploit_engine_testexploitorchestrator": "TestExploitOrchestrator" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L244 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig]
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L54 | neighbors=[agent.py, _check_anti_debug(), _load_or_create_identity(), main(), _obtain_identity(), .obtainIdentity()]
- "ai_llm_report_llmunavailableerror": "LLMUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L46 | neighbors=[llm_report.py, ._complete(), HallucinationGuard, ReviewStatus, LLMOutput, RuntimeError]
- "commands_interactive_runiterativeengagement": "runIterativeEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L816 | neighbors=[interactive.ts, runHostDiscoveryOnly(), chooseNextPhase(), confirm(), ln(), phaseLabel()]
- "data_mock_dashboard": "mock-dashboard.ts" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ProtocolRow.tsx, SlaRow.tsx, ZoneRow.tsx, AgentStatus, ATTACK_PATHS]
- "detection_edr_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L31 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception]
- "id_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L1 | neighbors=[0557559 scanner: real use-case library,…, 298a9d4 trim frontend to 7 core pages; …, DELETE(), fail(), GET, PUT()]
- "lib_cases_store": "cases-store.ts" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, addComment(), Case, CaseActivity, CaseComment, CaseSeverity]
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()]
- "models_llm_output_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L12 | neighbors=[LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…, llm_output.py, Base]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dependencies.py, approve_report(), _build_engagement_summary(), generate_report(), GenerateRequest]
- "scanner_vulncheck": "vulncheck.go" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, Finding, buildVulnRules(), checkDB(), checkService(), checkTLS()]
- "settings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts, useToast()]
- "tests_test_ad_assessment_testasreproastchecker": "TestASREPRoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L215 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ad_assessment_testntlmrelaychecker": "TestNTLMRelayChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L247 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_detection_core_testallosvsourcepackages": "TestAllOsvSourcePackages" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L993 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testclassifyconfidence": "TestClassifyConfidence" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L202 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfindingpostinit": "TestFindingPostInit" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L113 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testisip": "TestIsIp" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L212 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testkevdb": "TestKevDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L838 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalize": "TestNormalize" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L960 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalizebanner": "TestNormalizeBanner" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L913 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testproductfromcpe": "TestProductFromCpe" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L552 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_exploit_engine_testmetasploitrpcclient": "TestMetasploitRPCClient" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L181 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_exploit_engine_testrequiresapproval": "TestRequiresApproval" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L153 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L17 | neighbors=[test_result_spool.py, .test_custom_retry_config(), .test_exists(), .test_flush_spool_empty(), .test_flush_spool_partial(), .test_flush_spool_with_pending()]
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=probe/workflow/asset.py:L52 | neighbors=[asset.py, ._merge_db_scan(), ._merge_host_discovery(), ._merge_mcp_ai_scan(), ._merge_passive_collect(), ._merge_port_scan()]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, PageShell(), PageShellProps, Sidebar.tsx]
- "dashboard_exposure": "Exposure.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/Exposure.tsx:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, Exposure, ProtocolRiskCard(), useExposure(), ZoneHealthCard()]
- "detection_siem_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L24 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "detection_sigma_sigmarulegenerator": "SigmaRuleGenerator" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L107 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "engine_scan_modules": "scan-modules.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L1 | neighbors=[interactive.ts, 298a9d4 trim frontend to 7 core pages; …, defaultModules(), depthDefaults(), moduleById(), ModuleCategory]
- "graph_analyzer_pathanalyzer": "PathAnalyzer" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L60 | neighbors=[analyzer.py, ._exploit_info(), .find_blast_radius(), .find_paths_to_target(), .identify_chokepoints(), .__init__()]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L29 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[tools.ts, route.ts, ask.ts, findings.ts, interactive.ts, findings-store.ts]
- "lib_testssl_parser": "testssl-parser.ts" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, LiveFinding, Severity, finding-id.ts]
- "models_attack_path_attackpath": "AttackPath" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L11 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, attack_path.py, Base]
- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, Base, TimestampMixin, DetectionStatus, TimestampMixin]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-004.json

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
