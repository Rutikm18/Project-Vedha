# Node Description Batch 3 of 119

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

- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts, DETECTION_TO_UI, ENG_STATUS_TO_API]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[page.tsx, page.tsx, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DashboardCharts.tsx, PageShell.tsx]
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …, Parse a probe export into (facts, scan_…, Upsert assets (and their services) from…, Offline ingest path: upload a probe's s…]
- "tests_test_detection_core_testversioninranges": "TestVersionInRanges" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L312 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "cli_auth": "auth.ts" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L1 | neighbors=[apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl()]
- "cli_llm": "llm.ts" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L1 | neighbors=[client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId]
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C, checkDataDir()]
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ActivityItem, Bone(), ChartTooltip()]
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[GraphBuilder, GraphBuilder — turns engagement assets/…, Build the full multi-type attack graph.…, For each exploitable finding add an EXP…, Add CONNECTS_TO (directed reachability)…, CREDENTIAL_REUSE edges between assets s…]
- "pipeline_pipeline": "pipeline.go" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, Fact, Job, assemble(), assembleError()]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L726 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Run Nuclei and always leave its job in …, Unit tests for VulnEnrichmentService — …]
- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L38 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Run Nuclei and always leave its job in …, Unit tests for NessusScanner — all HTTP…]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "ad_kerberoast_kerberoastchecker": "KerberoastChecker" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L40 | neighbors=[kerberoast.py, ._encode_tgs_rep(), .generate_finding(), .get_spn_accounts(), ._pwd_last_set(), .request_tgs()]
- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L85 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…, ESC1: enrollee supplies subject + clien…, ESC4: a low-privilege principal holds a…]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L79 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .agent_id(), .agent_token(), .auth_header(), .clear_state()]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), EMPTY_FORM, Engagement]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, bulk_import_assets(), _compute_overview(), create_engagement()]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), LDAPEnumerator]
- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, FindingSeverity, FindingStatus, Raised when an LDAP/Kerberos/SMB connec…, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, FindingSeverity, FindingStatus, Raised when an optional offensive depen…, ACE]
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L80 | neighbors=[llm_report.py, HallucinationGuard, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation()]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L75 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L45 | neighbors=[orchestrator.py, MetasploitRPCClient, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute()]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L29 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress(), createInitialPipelineState()]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit(), ApproveRequest]
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/scanner/db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, e8262a3 feat(probe): explicit unauthent…, pipeline.py, run_scan.py, DBScanner]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), httpx-parser.ts, HttpxJsonlDecoder]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L391 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L867 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L109 | neighbors=[FindingImport, NessusScanRequest, NucleiScanRequest, Vuln scan API — Nessus + Nuclei launch,…, Run Nuclei and always leave its job in …, FakeProcess]
- "websocket_manager_agentconnectionmanager": "AgentConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L78 | neighbors=[TestAgentWebSocketAuthentication, TestAtomicWebSocketClaim, TestJobSecretBoundary, TestTenantWebSocketSelection, TestUseCaseCatalogParity, manager.py]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), FindingSeverity]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-002.json

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
