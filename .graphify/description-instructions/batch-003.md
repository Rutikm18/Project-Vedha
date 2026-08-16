# Node Description Batch 4 of 209

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

- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx]
- "vuln_enrichment_vulnenrichmentservice": "VulnEnrichmentService" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L91 | neighbors=[enrichment.py, Enriches Finding objects with NVD, EPSS…, .check_cisa_kev(), .compute_composite_risk(), .dedup_hash(), .enrich()]
- "vuln_nessus_nessusscanner": "NessusScanner" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L37 | neighbors=[nessus.py, ._auth_headers(), .authenticate(), .close(), .create_scan(), .export_nessus_file()]
- "ad_adcs_adcschecker": "ADCSChecker" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L52 | neighbors=[adcs.py, .check_esc1(), .check_esc4(), .check_esc8(), ._enrollment_principals(), .enumerate_templates()]
- "commands_doctor": "doctor.ts" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L1 | neighbors=[auth.ts, loadSession(), serverUrl(), buildDoctorCommand(), C, checkDataDir()]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…, PageShell.tsx, PageShell()]
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, bulk_import_assets()]
- "tests_test_detection_core_testversioninranges": "TestVersionInRanges" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L312 | neighbors=[test_detection_core.py, .test_empty_ranges(), .test_ignores_unknown_type(), .test_introduced_fixed(), .test_last_affected(), .test_no_match_returns_false_none()]
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig]
- "ad_kerberoast_kerberoastchecker": "KerberoastChecker" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L39 | neighbors=[kerberoast.py, ._encode_tgs_rep(), .generate_finding(), .get_spn_accounts(), ._pwd_last_set(), .request_tgs()]
- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L84 | neighbors=[ldap_enum.py, ._parse_security_descriptor(), A simplified access-control entry parse…, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…]
- "cli_auth": "auth.ts" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L1 | neighbors=[apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl()]
- "cli_llm": "llm.ts" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L1 | neighbors=[client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…]
- "dashboard_posturescorecard": "PostureScorecard.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, aa560a0 feat(posture): add dashboard Po…, DashboardGrid.tsx, PatchComparisonMatrix.tsx, Primitives.tsx, Delta()]
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[neo4j_client.py, .available(), .close(), .connect(), .ensure_schema(), .__init__()]
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts]
- "main_scripts_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _dns_probe(), _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi()]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L726 | neighbors=[test_detection_core.py, .test_cvss_critical(), .test_cvss_high(), .test_cvss_low(), .test_cvss_medium(), .test_elevated_epss_high()]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L108 | neighbors=[nuclei.py, ._consume_stdout(), .__init__(), ._map_finding(), .parse_output(), ._partial_or_raise()]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L81 | neighbors=[llm_report.py, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation(), .generate_executive_summary()]
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), assistant.ts]
- "dashboard_patchcomparisonmatrix": "PatchComparisonMatrix.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, d2eb44c feat(posture): add dashboard Pa…, DashboardGrid.tsx, Primitives.tsx, Meter(), cell]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L42 | neighbors=[orchestrator.py, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute(), .generate_dns_callback_token()]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress()]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[0f0097b feat(posture): mirror posture s…, 1fe16c8 stable but some dead code, need…, a0b870c fix(posture): score over open f…, d1b4dd3 trim frontend to 7 core pages; …, fadb4f5 fix(posture): hoist report-sect…, dependencies.py]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit()]
- "tests_test_posture": "test_posture.py" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 0f0097b feat(posture): mirror posture s…, 237a831 feat(posture): add run comparis…, 2cddd52 fix(posture): tenant-scope run …, 5238865 feat(posture): add pure scoring…, 9de087a feat(posture): add GET /analyti…]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=probe/tests/test_use_cases.py:L1 | neighbors=[01f4398 feat(probe): IoT survey reaches…, 22701ea Add tests for scanner parity an…, 5c8e696 docs(probe): correct overclaimi…, 95904f1 feat(probe): detect SMB signing…, bce780a feat(probe): enumerate HTTP met…, fe868e6 feat(probe): real UDP amplifica…]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), Enumerate AS-REP roastable accounts and…]
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=probe/agent/use_cases.py:L1 | neighbors=[agent.py, task_runner.py, _as_int(), normalize_intensity(), resolve(), use_case_for_code()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65f22a7e7696fead81236a6770771f450c0d15a6": "65f22a7 Add comprehensive tests for authentication and admin seeding- Implement…" | kind=Commit | source=git | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, main.py, AssistantDrawer.tsx, exceptions.py, router.py, startup.py]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L75 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "lib_portal_client": "portal-client.ts" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c52feb4 feat(portal): reskin User Porta…, page.tsx, GRADE_VAR, portalApi()]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), httpx-parser.ts, HttpxJsonlDecoder]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, .setup_method(), .test_esc1_negative_when_manager_approv…, .test_esc1_negative_without_low_priv_en…, .test_esc1_positive(), .test_esc4_negative_when_deny_ace()]
- "tests_test_ai_normalizer_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L32 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]

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
