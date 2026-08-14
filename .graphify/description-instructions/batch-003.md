# Node Description Batch 4 of 186

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

- "ad_ldap_enum_ace": "ACE" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L84 | neighbors=[ldap_enum.py, ._parse_security_descriptor(), A simplified access-control entry parse…, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…]
- "cli_auth": "auth.ts" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L1 | neighbors=[apiFetch(), clearSession(), loadSession(), requireAuth(), saveSession(), serverUrl()]
- "cli_llm": "llm.ts" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L1 | neighbors=[client(), commentOnStage(), explainFindings(), ExploitPlan, PHASE_LABELS, PhaseId]
- "dashboard_posturescorecard": "PostureScorecard.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, aa560a0 feat(posture): add dashboard Po…, DashboardGrid.tsx, PatchComparisonMatrix.tsx, Primitives.tsx, Delta()]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), EMPTY_FORM]
- "graph_neo4j_client_neo4jclient": "Neo4jClient" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L48 | neighbors=[neo4j_client.py, .available(), .close(), .connect(), .ensure_schema(), .__init__()]
- "main_scripts_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _dns_probe(), _ike_probe(), interpret_dns_recursion(), interpret_ike(), interpret_ipmi()]
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx]
- "tests_test_detection_core_testcomputepriority": "TestComputePriority" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L726 | neighbors=[test_detection_core.py, .test_cvss_critical(), .test_cvss_high(), .test_cvss_low(), .test_cvss_medium(), .test_elevated_epss_high()]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=probe/tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…]
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig]
- "vuln_nuclei_nucleiscanner": "NucleiScanner" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L108 | neighbors=[nuclei.py, ._consume_stdout(), .__init__(), ._map_finding(), .parse_output(), ._partial_or_raise()]
- "ad_bloodhound_bloodhoundcollector": "BloodHoundCollector" | kind=code-symbol | source=manager/backend/app/ad/bloodhound.py:L41 | neighbors=[bloodhound.py, .close(), .generate_finding(), .import_to_neo4j(), ._ingest_collection(), .__init__()]
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[AiMessage, evidenceText(), ManagerAiResponse, POST(), validMessages(), assistant.ts]
- "dashboard_patchcomparisonmatrix": "PatchComparisonMatrix.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, d2eb44c feat(posture): add dashboard Pa…, DashboardGrid.tsx, Primitives.tsx, Meter(), cell]
- "exploit_orchestrator_exploitorchestrator": "ExploitOrchestrator" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L42 | neighbors=[orchestrator.py, ._audit(), ._check_approval_required(), ._check_blast_radius(), .execute(), .generate_dns_callback_token()]
- "lib_permissions_store": "permissions-store.ts" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addUser(), DATA_PATH, ensureDir(), getAllUsers(), getUser()]
- "lib_scan_pipeline": "scan-pipeline.ts" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, nuclei-parser.ts, NucleiMatch, computeOverallProgress()]
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[0f0097b feat(posture): mirror posture s…, 1fe16c8 stable but some dead code, need…, a0b870c fix(posture): score over open f…, d1b4dd3 trim frontend to 7 core pages; …, fadb4f5 fix(posture): hoist report-sect…, dependencies.py]
- "routers_exploits": "exploits.py" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _approval_out(), ApprovalOut, approve_exploit()]
- "tests_test_posture": "test_posture.py" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 0f0097b feat(posture): mirror posture s…, 237a831 feat(posture): add run comparis…, 2cddd52 fix(posture): tenant-scope run …, 5238865 feat(posture): add pure scoring…, 9de087a feat(posture): add GET /analyti…]
- "ad_asreproast_asreproastchecker": "ASREPRoastChecker" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L34 | neighbors=[asreproast.py, ._format_asrep_hash(), .generate_finding(), .get_no_preauth_accounts(), .request_asrep(), Enumerate AS-REP roastable accounts and…]
- "ai_llm_report_llmreportgenerator": "LLMReportGenerator" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L80 | neighbors=[llm_report.py, .available(), ._complete(), ._generate_and_store(), .generate_detection_rule_explanation(), .generate_executive_summary()]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell()]
- "detection_correlator_detectioncorrelator": "DetectionCorrelator" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L75 | neighbors=[correlator.py, .compute_coverage(), .correlate(), .generate_gap_report(), ._host_for(), ._in_window()]
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/scanner/db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, e8262a3 feat(probe): explicit unauthent…, pipeline.py, run_scan.py, DBScanner]
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/scanner/host_discovery.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, device_hint()]
- "tests_parsers_test": "parsers.test.ts" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, finding-id.ts, resetCounters(), httpx-parser.ts, HttpxJsonlDecoder]
- "tests_test_ad_assessment_testadcschecker": "TestADCSChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L278 | neighbors=[test_ad_assessment.py, .setup_method(), .test_esc1_negative_when_manager_approv…, .test_esc1_negative_without_low_priv_en…, .test_esc1_positive(), .test_esc4_negative_when_deny_ace()]
- "tests_test_ai_normalizer_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L32 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_detection_core_testmatchcandidate": "TestMatchCandidate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L391 | neighbors=[test_detection_core.py, .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding(), .test_no_match_returns_empty()]
- "tests_test_detection_core_testvulndb": "TestVulnDB" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L867 | neighbors=[test_detection_core.py, .test_content_hash_deterministic(), .test_covers(), .test_cvss_vector_index(), .test_cvss_vector_missing(), .test_known_products_sorted()]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=probe/tests/test_use_cases.py:L1 | neighbors=[01f4398 feat(probe): IoT survey reaches…, 5c8e696 docs(probe): correct overclaimi…, 95904f1 feat(probe): detect SMB signing…, bce780a feat(probe): enumerate HTTP met…, fe868e6 feat(probe): real UDP amplifica…, use_cases.py]
- "tests_test_vuln_enrichment": "test_vuln_enrichment.py" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _make_http_mock(), test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_dedup_hash_case_insensitive_cve()]
- "websocket_manager_agentconnectionmanager": "AgentConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L78 | neighbors=[manager.py, .agent_stale_after(), .connected_agents(), .connected_count(), .get_agent_status(), .__init__()]
- "ad_ntlm_relay_ntlmrelaychecker": "NTLMRelayChecker" | kind=code-symbol | source=manager/backend/app/ad/ntlm_relay.py:L30 | neighbors=[ntlm_relay.py, .check_ldap_signing(), .check_smb_signing(), .generate_finding(), ._probe_smb_host(), Probe SMB/LDAP signing posture across a…]
- "commands_scan": "scan.ts" | kind=code-symbol | source=manager/frontend/cli/commands/scan.ts:L1 | neighbors=[requireAuth(), buildScanCommand(), printAiComment(), PROFILE_TOOLS, resolveTargets(), scanCommand()]
- "commands_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/cli/commands/tools.ts:L1 | neighbors=[buildToolsCommand(), C, ln(), showSpinner(), w(), installer.ts]
- "id_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, a789cca scanner: real use-case library,…, d1b4dd3 trim frontend to 7 core pages; …, ApiActivity, DELETE(), fail()]

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
