# Node Description Batch 5 of 131

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

- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, _atomic_write_private_state(), _sync_directory(), Transport, TransportError, transport.py — all manager communicatio…]
- "auth_startup": "startup.py" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L1 | neighbors=[config.py, database.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, Engagement, FindingSummary]
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …]
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[FactCard.tsx, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, page.tsx, COVERAGE_COLOR, DetectionCoverage]
- "routers_ai_report": "ai_report.py" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, approve_report(), _build_engagement_summary(), generate_report()]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _ConnectSweep, _have_masscan()]
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _detect_drift(), _hash()]
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ._ldap_with_users(), .setup_method(), .test_finding_critical_when_privileged(), .test_finding_high_when_not_privileged(), .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L32 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…]
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L75 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1053 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), ConsistencyReport]
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L595 | neighbors=[test_detection_core.py, .test_authoritative_tier4(), .test_multi_signal_tier2(), .test_protocol_scanner_tier3(), .test_single_banner_tier1(), ConsistencyReport]
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L560 | neighbors=[test_detection_core.py, .test_no_smb_facts_returns_none(), .test_smbv1_with_missing_hotfixes_retur…, .test_smbv1_with_patched_host_returns_n…, .test_smbv1_without_hotfix_data_returns…, ConsistencyReport]
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L483 | neighbors=[test_detection_core.py, .test_authoritative_upgrades_state(), .test_different_ids_preserved(), .test_evidence_refs_dedup_preserving_or…, .test_merges_same_id(), ConsistencyReport]
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1027 | neighbors=[test_detection_core.py, .test_classification_intermittent(), .test_classification_mostly_stable(), .test_classification_stable(), .test_rate(), ConsistencyReport]
- "tests_test_detection_core_testsuppressnegated": "TestSuppressNegated" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L516 | neighbors=[test_detection_core.py, .test_keeps_authoritative_finding(), .test_keeps_inferred_when_auth_version_…, .test_keeps_inferred_when_no_authoritat…, .test_suppresses_inferred_when_authorit…, ConsistencyReport]
- "tests_test_detection_core_testwilsonci": "TestWilsonCi" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1008 | neighbors=[test_detection_core.py, .test_all_appearances(), .test_perfect_appearance(), .test_zero_appearances(), .test_zero_n(), ConsistencyReport]
- "tests_test_detection_validation_testsiemparsing": "TestSIEMParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L186 | neighbors=[test_detection_validation.py, .test_elastic_parse(), .test_factory(), .test_sentinel_parse(), .test_splunk_parse(), .test_splunk_spl_includes_host_and_time…]
- "tests_test_service_identifier_testserviceidentifier": "TestServiceIdentifier" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L6 | neighbors=[test_service_identifier.py, ._id(), .setup_method(), .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined()]
- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, database.py, _claim_batch(), _dead_letter_stale_stmt(), enqueue(), Event]
- "ad_orchestrator_adassessmentrunner": "ADAssessmentRunner" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L39 | neighbors=[orchestrator.py, ._anonymous_bind_finding(), .__init__(), .run(), Coordinates all AD checkers for a singl…, ADCSChecker]
- "ai_agent_agentdecisionengine": "AgentDecisionEngine" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L161 | neighbors=[agent.py, .available(), ._count(), ._create(), ._exec_read_tool(), .__init__()]
- "commands_interactive_choose": "choose()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L85 | neighbors=[interactive.ts, ask(), ln(), chooseNextPhase(), mainMenu(), pickEngagementId()]
- "commands_interactive_wizardscan": "wizardScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L329 | neighbors=[interactive.ts, mainMenu(), ask(), banner(), choose(), confirm()]
- "data_mock_dashboard": "mock-dashboard.ts" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AgentStatus, ATTACK_PATHS, AttackPath, PathStatus, ProtocolRisk]
- "generate_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, POST(), backend.ts, backend(), BackendError]
- "graph_builder_graphbuilder": "GraphBuilder" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L90 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph(), .build_from_db()]
- "lib_cases_store": "cases-store.ts" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addComment(), Case, CaseActivity, CaseComment, CaseSeverity]
- "lib_testssl_parser": "testssl-parser.ts" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, LiveFinding, Severity]
- "models_enums_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L76 | neighbors=[enums.py, str, LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…]
- "tests_findings_store_test": "findings-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, LiveFinding, resetCounters(), getAllFindings(), getFindingById()]
- "tests_test_ad_assessment_fakeentry": "_FakeEntry" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L36 | neighbors=[test_ad_assessment.py, .__getitem__(), .__init__(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account()]
- "tests_test_ad_assessment_testbloodhoundcollector": "TestBloodHoundCollector" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L356 | neighbors=[test_ad_assessment.py, .setup_method(), .test_da_path_finding_critical_when_sho…, .test_da_path_finding_high_when_long(), .test_import_without_neo4j(), .test_no_finding_without_paths()]
- "tests_test_ad_assessment_testldapenumeratorparsing": "TestLDAPEnumeratorParsing" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L97 | neighbors=[test_ad_assessment.py, .test_domain_to_base_dn(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_attack_paths_testpathanalyzer": "TestPathAnalyzer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L112 | neighbors=[test_attack_paths.py, .test_blast_radius_unknown_asset(), .test_chokepoints_empty_without_paths(), .test_cypher_constants_present(), .test_find_blast_radius(), .test_find_paths_to_target()]
- "tests_test_detection_core_testcleandebianversion": "TestCleanDebianVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L971 | neighbors=[test_detection_core.py, .test_no_revision(), .test_strips_epoch(), .test_strips_revision(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testepssdb": "TestEpssDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L849 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_get_existing(), .test_get_missing(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testmakefindingid": "TestMakeFindingId" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L98 | neighbors=[test_detection_core.py, .test_deterministic(), .test_different_inputs_different_ids(), .test_length_16(), ConsistencyReport, FindingConsistency]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-004.json

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
