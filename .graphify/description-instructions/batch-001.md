# Node Description Batch 2 of 119

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

- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, modulesForPorts(), bySeverityCount()]
- "detection_engine_consistency_consistencyreport": "ConsistencyReport" | kind=code-symbol | source=manager/detection_engine/consistency.py:L86 | neighbors=[consistency.py, aggregate(), .intermittent(), .stable(), Finding, Detection engine test suite — unit test…]
- "detection_engine_verifier_evidencetier": "EvidenceTier" | kind=code-symbol | source=manager/detection_engine/verifier.py:L41 | neighbors=[verifier.py, Finding, FindingState, SourceConfidence, IntEnum, Detection engine test suite — unit test…]
- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[NucleiExploitRunner, NucleiExploitRunner — CVE PoC validatio…, Run Nuclei CVE PoC template against tar…, Parse nuclei JSONL output for a single …, Run Nuclei CVE PoC templates against a …, Parse template YAML and validate it con…]
- "detection_engine_vuln_db_snapshotmeta": "SnapshotMeta" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L70 | neighbors=[vuln_db.py, load_snapshot(), Detection engine test suite — unit test…, TestAggregate, TestAllOsvSourcePackages, TestAsset]
- "id_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts, useToast()]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, buildAdminCommand(), buildAskCommand(), buildDoctorCommand(), buildEngagementCommand(), buildFindingsCommand()]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, a789cca scanner: real use-case library,…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell()]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, test_passive_collector.py, test_workflow_execution.py]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset, AttackPath]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L51 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L1 | neighbors=[b4b12a9 Rename project and update files, port_scanner.py, scanner_base.py, _ConcurrencyScanner, _ExplodingScanner, test_agent_scan_types_have_distinct_sta…]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, AgentJob]
- "routers_agents": "agents.py" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, a789cca scanner: real use-case library,…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, config.py, dependencies.py]
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DiscoveredHost, LiveFinding, ScanSummary]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "lib_backend": "backend.ts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, route.ts]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, Evidence, LiveFinding, Severity]
- "settings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), fetcher.ts, fetchJson()]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ADJ, adjacency(), ATTACK_PATHS, AttackPath, bfsReach()]
- "scanner_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, base_argparser()]
- "agent_engine": "engine.py" | kind=code-symbol | source=probe/agent/engine.py:L1 | neighbors=[_applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _env_number(), _error_result()]
- "aibrain_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L1 | neighbors=[AIBrainPage(), AiStatus, Engagement, Message, providerLabel(), STARTER_PROMPTS]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset, AttackPath]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ATTACK_TIMELINE, AttackAction, computeCoverage(), correlate()]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L12 | neighbors=[Engagement, enums.py, str, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L637 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, transport.py, _atomic_write_private_state(), .ConnectWS(), .get(), .Heartbeat()]
- "app_dependencies": "dependencies.py" | kind=code-symbol | source=manager/backend/app/dependencies.py:L1 | neighbors=[config.py, database.py, close_redis(), get_current_user(), get_redis(), main.py]
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Agent, AgentCapability, AGENTS, agentsStore, AgentStatus]
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L39 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-001.json

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
