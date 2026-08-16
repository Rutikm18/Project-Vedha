# Node Description Batch 2 of 209

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

- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "tests_test_detection_core_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L56 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), .test_authoritative_tier4()]
- "detection_engine_ingest_ingestresult": "IngestResult" | kind=code-symbol | source=manager/detection_engine/ingest.py:L42 | neighbors=[ingest.py, ingest_file(), ingest_files(), .get_or_create_asset(), .__init__(), Asset]
- "detection_engine_enrichment_db_epssdb": "EpssDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L24 | neighbors=[enrichment_db.py, .get(), .__init__(), load_epss(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "detection_engine_enrichment_db_kevdb": "KevDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L15 | neighbors=[enrichment_db.py, .__init__(), .is_kev(), load_kev(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "lib_ai_engine": "ai-engine.ts" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, types.ts, LiveFinding, aiReportStore]
- "routers_agents": "agents.py" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1 | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, 0e22dbf feat(probe): bounded auto-troub…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 30261eb feat: enhance advisor flow with…]
- "tests_test_probe_core_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L71 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "scanner_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, AdaptiveRateController]
- "lib_backend": "backend.ts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, route.ts, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "tests_test_detection_core": "test_detection_core.py" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, _candidate(), _fact(), _finding(), _mock_epss_db(), _mock_kev_db()]
- "app_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/page.tsx:L1 | neighbors=[Dashboard(), DashboardCharts.tsx, DashboardCharts(), PageShell.tsx, PageShell(), DashboardGrid.tsx]
- "detection_engine_consistency_findingconsistency": "FindingConsistency" | kind=code-symbol | source=manager/detection_engine/consistency.py:L50 | neighbors=[consistency.py, aggregate(), .ci(), .classification(), .rate(), Finding]
- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, modulesForPorts(), bySeverityCount()]
- "detection_engine_consistency_consistencyreport": "ConsistencyReport" | kind=code-symbol | source=manager/detection_engine/consistency.py:L86 | neighbors=[consistency.py, aggregate(), .intermittent(), .stable(), Finding, Detection engine test suite — unit test…]
- "detection_engine_verifier_evidencetier": "EvidenceTier" | kind=code-symbol | source=manager/detection_engine/verifier.py:L41 | neighbors=[verifier.py, IntEnum, Finding, FindingState, SourceConfidence, Detection engine test suite — unit test…]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[safety.py, Exception, .__init__(), Raised when a high-risk target requires…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "agent_engine": "engine.py" | kind=code-symbol | source=probe/agent/engine.py:L1 | neighbors=[agent.py, _applied_tuning(), _build_run_stats(), _clamp(), _count_open_port_facts(), _derive_post_stage()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cac022c40e254cd92ba6e8c73c79c0987b8650d2": "cac022c Everything is done and verified. Here's the wrap-up.What I did (as an a…" | kind=Commit | source=git | neighbors=[c5e2d0e chore: retire probe-go to spike…, kerberoast.py, ldap_enum.py, agent.py, license.py, task_runner.py]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[safety.py, Exception, Raised when a job would exceed the maxi…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[safety.py, Raised when a requested payload or modu…, Exception, validate_module(), validate_payload(), ApprovalOut]
- "detection_engine_vuln_db_snapshotmeta": "SnapshotMeta" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L73 | neighbors=[vuln_db.py, _read_snapshot(), load_snapshot(), Detection engine test suite — unit test…, TestAggregate, TestAllOsvSourcePackages]
- "id_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts]
- "tests_test_main_scripts_findings": "test_main_scripts_findings.py" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ids(), _run(), test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_build_service_index_extracts_confi…]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 81c81cb feat: implement outbox reclaim …, a789cca scanner: real use-case library,…, b4b12a9 Rename project and update files]
- "aibrain_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L1 | neighbors=[AIBrainPage(), AiStatus, Engagement, Message, providerLabel(), STARTER_PROMPTS]
- "branch:repo:github.com/Rutikm18/Project-Vedha#worktree-fleet-already-downloaded-cmd": "worktree-fleet-already-downloaded-cmd" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "workflow_workflow_engine": "workflow_engine.py" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, test_passive_collector.py]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L56 | neighbors=[enums.py, str, AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, buildAdminCommand(), buildAskCommand(), buildDoctorCommand(), buildEngagementCommand(), buildFindingsCommand()]
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, port_scanner.py, scanner_base.py, _ConcurrencyScanner, _ExplodingScanner]
- "app_dependencies": "dependencies.py" | kind=code-symbol | source=manager/backend/app/dependencies.py:L1 | neighbors=[config.py, database.py, close_redis(), get_current_user(), get_redis(), main.py]
- "basescanner": "BaseScanner" | kind=code-symbol | neighbors=[DBScanner, HostDiscoveryScanner, IoTScanner, _ConnectSweep, MCPAIScanner, MobileScanner]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[base.py, DeclarativeBase, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…]
- "routers_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, c0f3b4c feat(probe-enroll): trust-on-fi…, config.py, dependencies.py, activate_enrollment()]
- "tests_test_main_scripts_findings_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L15 | neighbors=[test_main_scripts_findings.py, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_dou…, test_confirmed_ftp_cleartext_is_high_co…, test_confirmed_redis_is_high_confidence…]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, AgentJob]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[safety.py, Exception, Raised when a target IP is outside the …, validate_scope(), ApprovalOut, ApproveRequest]
- "settings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), fetcher.ts]

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
