# Node Description Batch 7 of 104

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

- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L43 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, BaseModel, Asset, AttackPath]
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L53 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L87 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L70 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …, Parse a probe export into (facts, scan_…, Upsert assets (and their services) from…, Offline ingest path: upload a probe's s…]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection, MicrosoftDefender]
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L67 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Background task: run nuclei, persist fi…, nuclei.py]
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L123 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()]
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator]
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), CPECandidate, normalize()]
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L81 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()]
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, auth-middleware.ts, generateOtp(), OtpEntry, otpStore]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L51 | neighbors=[page.tsx, DashboardCharts.tsx, Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, page.tsx]
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, scanner.ts, tool-runners.ts, types.ts, Severity, counters]
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[AttackLogger, AttackLogger — records every attack act…, Persist a single attack action. Returns…, attack_timeline.py, Base, Base]
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L46 | neighbors=[outbox.py, Base, Base, TimestampMixin, TimestampMixin, Event]
- "pipeline_pipeline_run": "Run()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L68 | neighbors=[pipeline.go, assemble(), assembleError(), clamp(), clampInt(), dedup()]
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L71 | neighbors=[agents.py, BaseModel, Asset, Engagement, AssetType, ScanJobStatus]
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult, Engagement]
- "routers_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dependencies.py, configure_siem(), get_coverage(), get_gaps(), get_results()]
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L482 | neighbors=[engagements.py, BaseModel, Asset, Engagement, AssetType, EngagementStatus]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L62 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L48 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L66 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_vuln_scans_findingimport": "FindingImport" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L48 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nessusscanrequest": "NessusScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L34 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nucleiscanrequest": "NucleiScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L42 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, run_scan.py, _ConnectSweep, _have_masscan(), main()]
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, run_scan.py, _auth_shaped_json_body(), _known_false_positive(), main()]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _get_cert_der(), main()]
- "tests_test_nessus_scanner": "test_nessus_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _mock_response(), scanner(), test_authenticate_api_key(), test_create_scan(), test_create_scan_with_credentials()]
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=probe/tests/test_probe_core.py:L57 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()]
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, installer.ts, currentPlatform(), Platform]
- "ui_output_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L30 | neighbors=[output.ts, banner(), findingDetail(), findingLine(), findingsTable(), hostLine()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-006.json

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
