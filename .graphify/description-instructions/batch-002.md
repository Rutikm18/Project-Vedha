# Node Description Batch 3 of 131

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

- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, Raised when an LDAP/Kerberos/SMB connec…, FindingSeverity, FindingStatus, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, Raised when an optional offensive depen…, FindingSeverity, FindingStatus, ACE]
- "app_dependencies": "dependencies.py" | kind=code-symbol | source=manager/backend/app/dependencies.py:L1 | neighbors=[config.py, database.py, close_redis(), get_current_user(), get_redis(), main.py]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L12 | neighbors=[enums.py, str, Engagement, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts, DETECTION_TO_UI]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L33 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ATTACK_TIMELINE, AttackAction, computeCoverage(), correlate()]
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L637 | neighbors=[test_detection_core.py, .test_ai_cap_at_60(), .test_ai_no_cap_if_already_below(), .test_auth_enforced_penalty(), .test_authoritative_tier_base_95(), .test_backport_penalty()]
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Agent, AgentCapability, AGENTS, agentsStore, AgentStatus]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …]
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[common.py, paginate(), BaseModel, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, .setup_method(), .test_compute_coverage(), .test_coverage_empty(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking()]
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L61 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[enrichment.py, Enriches Finding objects with NVD, EPSS…, .check_cisa_kev(), .compute_composite_risk(), .dedup_hash(), .enrich()]
- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L37 | neighbors=[nessus.py, ._auth_headers(), .authenticate(), .close(), .create_scan(), .export_nessus_file()]
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()]
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C, checkDataDir()]
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ActivityItem, Bone()]
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, bulk_import_assets()]
- "tests_test_detection_core_testversioninranges": "TestVersionInRanges" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L312 | neighbors=[test_detection_core.py, .test_empty_ranges(), .test_ignores_unknown_type(), .test_introduced_fixed(), .test_last_affected(), .test_no_match_returns_false_none()]
- "ad_kerberoast_kerberoastchecker": "KerberoastChecker" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L39 | neighbors=[kerberoast.py, ._encode_tgs_rep(), .generate_finding(), .get_spn_accounts(), ._pwd_last_set(), .request_tgs()]
- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L84 | neighbors=[ldap_enum.py, ._parse_security_descriptor(), A simplified access-control entry parse…, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…]
- "cli_auth": "auth.ts" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L1 | neighbors=[apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl()]
- "cli_llm": "llm.ts" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L1 | neighbors=[client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), EMPTY_FORM]
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[neo4j_client.py, .available(), .close(), .connect(), .ensure_schema(), .__init__()]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L726 | neighbors=[test_detection_core.py, .test_cvss_critical(), .test_cvss_high(), .test_cvss_low(), .test_cvss_medium(), .test_elevated_epss_high()]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L108 | neighbors=[nuclei.py, ._consume_stdout(), .__init__(), ._map_finding(), .parse_output(), ._partial_or_raise()]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), assistant.ts]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L42 | neighbors=[orchestrator.py, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute(), .generate_dns_callback_token()]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress()]
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit()]
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig]

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
