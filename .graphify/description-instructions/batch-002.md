# Node Description Batch 3 of 104

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

- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L38 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Background task: run nuclei, persist fi…, Unit tests for NessusScanner — all HTTP…]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), LDAPEnumerator]
- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, FindingSeverity, FindingStatus, Raised when an LDAP/Kerberos/SMB connec…, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, FindingSeverity, FindingStatus, Raised when an optional offensive depen…, ACE]
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L80 | neighbors=[llm_report.py, HallucinationGuard, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation()]
- "cli_auth": "auth.ts" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L1 | neighbors=[apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl()]
- "cli_llm": "llm.ts" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L1 | neighbors=[client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId]
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[index.ts, auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L75 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L45 | neighbors=[orchestrator.py, MetasploitRPCClient, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, openvas-client.ts, OpenVASFinding, computeOverallProgress()]
- "routers_agents": "agents.py" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1 | neighbors=[0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, config.py, dependencies.py, _agent_ownership_check()]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L391 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L867 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), FindingSeverity]
- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, route.ts, route.ts, route.ts, DETECTION_TO_UI]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_enums_assetcriticality": "AssetCriticality" | kind=code-symbol | source=manager/backend/app/models/enums.py:L28 | neighbors=[Asset, enums.py, str, Attack path analysis API (AttackPathSer…, AssetIn, AssetOut]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, dependencies.py, bulk_import_assets(), _compute_overview(), create_engagement()]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit(), ApproveRequest]
- "tests_test_detection_core_testdeceptionscore": "TestDeceptionScore" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L616 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testingestfile": "TestIngestFile" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L220 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "commands_interactive_confirm": "confirm()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L79 | neighbors=[interactive.ts, ask(), mainMenu(), pickHostSubset(), pickModulesByCategory(), pickTargets()]
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, ActivityItem, Bone(), ChartTooltip()]
- "lib_clients_store": "clients-store.ts" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Client, ClientJiraConfig, ClientNotifyConfig, ClientSettings, ClientsFile]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[page.tsx, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, DashboardCharts.tsx, PageShell.tsx, Exposure.tsx]
- "tests_test_detection_core_testasset": "TestAsset" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L128 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testcvss": "TestCvss" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L280 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testenrichfinding": "TestEnrichFinding" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L786 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testingestvalidation": "TestIngestValidation" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L184 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testnormalizedb": "TestNormalizeDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L932 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_testsigmarulegenerator": "TestSigmaRuleGenerator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L146 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testnucleiexploitrunner": "TestNucleiExploitRunner" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L349 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "tests_test_exploit_engine_testvalidatepayload": "TestValidatePayload" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L62 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError]
- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, transport.py, .ConnectWS(), .get(), .Heartbeat(), .Login()]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L36 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .agent_id(), .agent_token(), .auth_header(), .clear_state()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-002.json

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
