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

- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L391 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L867 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "websocket_manager_agentconnectionmanager": "AgentConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L78 | neighbors=[TestAgentWebSocketAuthentication, TestAtomicWebSocketClaim, TestJobSecretBoundary, TestTenantWebSocketSelection, TestUseCaseCatalogParity, manager.py]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), FindingSeverity]
- "commands_scan": "scan.ts" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L1 | neighbors=[requireAuth(), buildScanCommand(), printAiComment(), PROFILE_TOOLS, resolveTargets(), scanCommand()]
- "commands_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L1 | neighbors=[buildToolsCommand(), C, ln(), showSpinner(), w(), installer.ts]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell()]
- "id_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, a789cca scanner: real use-case library,…, d1b4dd3 trim frontend to 7 core pages; …, ApiActivity, DELETE(), fail()]
- "lib_clients_store": "clients-store.ts" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, ClientJiraConfig, ClientNotifyConfig, ClientSettings, ClientsFile]
- "lib_openvas_client": "openvas-client.ts" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, findings-store.ts, FindingSeverity, boundedEnvMs()]
- "models_enums_assetcriticality": "AssetCriticality" | kind=code-symbol | source=manager/backend/app/models/enums.py:L28 | neighbors=[Asset, enums.py, str, Attack path analysis API (AttackPathSer…, AssetIn, AssetOut]
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[page.tsx, d1b4dd3 trim frontend to 7 core pages; …, LiveOverview.tsx, page.tsx, page.tsx, page.tsx]
- "tests_test_detection_core_testdeceptionscore": "TestDeceptionScore" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L616 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testingestfile": "TestIngestFile" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L220 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "vuln_nuclei_nucleiscanerror": "NucleiScanError" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L89 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Run Nuclei and always leave its job in …, _FakeSession]
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/probe-usecase-alignment": "feat/probe-usecase-alignment" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "commands_interactive_confirm": "confirm()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L79 | neighbors=[interactive.ts, ask(), mainMenu(), pickHostSubset(), pickModulesByCategory(), pickTargets()]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, pct(), Sev, SEV_STYLE, SlaItem]
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L55 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, ._banner_grab_all(), ._grab_one(), .__init__()]
- "probe_pipeline": "pipeline.py" | kind=code-symbol | source=probe/pipeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _clean(), _Collector, _ip_key(), main(), _render_summary()]
- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, FindingImport, _finish_cancelled_nuclei_job()]
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
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, Engagement, FindingSummary]
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …]
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[FactCard.tsx, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, page.tsx, COVERAGE_COLOR, DetectionCoverage]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, approve_report(), _build_engagement_summary(), generate_report()]

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
