# Node Description Batch 6 of 119

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

- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception]
- "generate_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, POST(), backend.ts, backend(), BackendError, bearerFrom()]
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[b4b12a9 Rename project and update files, page.tsx, COVERAGE_COLOR, DetectionCoverage, epssColor(), ExploitMaturity]
- "models_llm_output_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L12 | neighbors=[LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…, llm_output.py, Base]
- "probe_run_scan": "run_scan.py" | kind=code-symbol | source=probe/run_scan.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _orchestrate(), db_scanner.py, host_discovery.py, mass_scan.py]
- "tests_test_ad_assessment_testasreproastchecker": "TestASREPRoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L215 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ad_assessment_testntlmrelaychecker": "TestNTLMRelayChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L247 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_agents": "test_agents.py" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, TestAccessTokenExpiry, TestAgentExecutableTypes, TestAgentJobCompatibility]
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
- "tests_test_integration": "test_integration.py" | kind=code-symbol | source=probe/tests/test_integration.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, result_spool.py, scope_crypt.py, scope_validator.py, task_runner.py, transport.py]
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=probe/workflow/asset.py:L52 | neighbors=[asset.py, ._merge_db_scan(), ._merge_host_discovery(), ._merge_mcp_ai_scan(), ._merge_passive_collect(), ._merge_port_scan()]
- "workflow_gates": "gates.py" | kind=code-symbol | source=probe/workflow/gates.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, cdee859 feat(probe): add container/clou…, d1b4dd3 trim frontend to 7 core pages; …, test_port_catalog.py, test_probe_core.py]
- "detection_siem_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L24 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "detection_sigma_sigmarulegenerator": "SigmaRuleGenerator" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L107 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "discovery_service_id_servicefingerprint": "ServiceFingerprint" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L14 | neighbors=[service_id.py, .identify(), NucleiRunReport, NucleiScanError, NucleiScanner, NucleiScanner — async subprocess wrappe…]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, GET, positiveInt(), POST(), STATUS_TO_API]
- "graph_analyzer_pathanalyzer": "PathAnalyzer" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L60 | neighbors=[analyzer.py, ._exploit_info(), .find_blast_radius(), .find_paths_to_target(), .identify_chokepoints(), .__init__()]
- "lib_exploit_store": "exploit-store.ts" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[page.tsx, page.tsx, DashboardCharts.tsx, Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx]
- "models_attack_path_attackpath": "AttackPath" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L11 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, attack_path.py, Base]
- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, Base, TimestampMixin, DetectionStatus, TimestampMixin]
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, CheckOpts, checkPort(), expandTarget()]
- "routers_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _all_paths_to_critical(), _asset_labels(), attack_graph(), blast_radius()]
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L483 | neighbors=[engagements.py, BaseModel, Asset, Engagement, AssetType, EngagementStatus]
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, _coverage(), _device_hint(), _is_readable()]
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 95904f1 feat(probe): detect SMB signing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main()]
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L174 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-005.json

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
