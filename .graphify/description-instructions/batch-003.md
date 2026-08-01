# Node Description Batch 4 of 119

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

- "commands_scan": "scan.ts" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L1 | neighbors=[requireAuth(), buildScanCommand(), printAiComment(), PROFILE_TOOLS, resolveTargets(), scanCommand()]
- "lib_clients_store": "clients-store.ts" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, ClientJiraConfig, ClientNotifyConfig, ClientSettings, ClientsFile]
- "lib_openvas_client": "openvas-client.ts" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, findings-store.ts, FindingSeverity, boundedEnvMs()]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_enums_assetcriticality": "AssetCriticality" | kind=code-symbol | source=manager/backend/app/models/enums.py:L28 | neighbors=[Asset, enums.py, str, Attack path analysis API (AttackPathSer…, AssetIn, AssetOut]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[page.tsx, d1b4dd3 trim frontend to 7 core pages; …, LiveOverview.tsx, page.tsx, page.tsx, page.tsx]
- "tests_test_detection_core_testdeceptionscore": "TestDeceptionScore" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L616 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testingestfile": "TestIngestFile" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L220 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L65 | neighbors=[agent.py, _check_anti_debug(), _flush_spool_over_http(), _load_or_create_identity(), main(), _obtain_identity()]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "commands_interactive_confirm": "confirm()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L79 | neighbors=[interactive.ts, ask(), mainMenu(), pickHostSubset(), pickModulesByCategory(), pickTargets()]
- "commands_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L1 | neighbors=[buildToolsCommand(), C, ln(), showSpinner(), w(), installer.ts]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, PageShell(), PageShellProps]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, pct(), Sev, SEV_STYLE, SlaItem]
- "id_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, d1b4dd3 trim frontend to 7 core pages; …, ApiActivity, DELETE(), fail(), GET]
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts, backend.ts]
- "probe_pipeline": "pipeline.py" | kind=code-symbol | source=probe/pipeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _clean(), _Collector, _ip_key(), main(), _render_summary()]
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, fe868e6 feat(probe): real UDP amplifica…, run_scan.py, _dns_probe(), interpret_dns_recursion()]
- "tests_test_cli": "test_cli.py" | kind=code-symbol | source=probe/tests/test_cli.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, FakeClient, test_cmd_daemon_run_overrides_stale_env…, test_cmd_doctor_fails_when_no_agent_unl…, test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…]
- "tests_test_detection_core_testasset": "TestAsset" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L128 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcvss": "TestCvss" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L280 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testenrichfinding": "TestEnrichFinding" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L786 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testingestvalidation": "TestIngestValidation" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L184 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalizedb": "TestNormalizeDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L932 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testsigmarulegenerator": "TestSigmaRuleGenerator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L146 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testnucleiexploitrunner": "TestNucleiExploitRunner" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L349 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_exploit_engine_testvalidatepayload": "TestValidatePayload" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L62 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "workflow_modes": "modes.py" | kind=code-symbol | source=probe/workflow/modes.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_workflow_execution.py]
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L57 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, ._banner_grab_all(), ._grab_one(), .__init__()]
- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, FindingImport, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job()]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _ConnectSweep, _have_masscan()]
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L32 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…]
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L75 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1053 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L595 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L560 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L483 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1027 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-003.json

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
