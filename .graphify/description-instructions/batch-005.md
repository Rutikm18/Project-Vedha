# Node Description Batch 6 of 134

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

- "models_enums_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L76 | neighbors=[enums.py, str, LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…]
- "tests_findings_store_test": "findings-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, LiveFinding, resetCounters(), getAllFindings(), getFindingById()]
- "tests_test_ad_assessment_fakeentry": "_FakeEntry" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L36 | neighbors=[test_ad_assessment.py, .__getitem__(), .__init__(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account()]
- "tests_test_ad_assessment_testbloodhoundcollector": "TestBloodHoundCollector" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L356 | neighbors=[test_ad_assessment.py, .setup_method(), .test_da_path_finding_critical_when_sho…, .test_da_path_finding_high_when_long(), .test_import_without_neo4j(), .test_no_finding_without_paths()]
- "tests_test_ad_assessment_testldapenumeratorparsing": "TestLDAPEnumeratorParsing" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L97 | neighbors=[test_ad_assessment.py, .test_domain_to_base_dn(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_attack_paths_testpathanalyzer": "TestPathAnalyzer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L112 | neighbors=[test_attack_paths.py, .test_blast_radius_unknown_asset(), .test_chokepoints_empty_without_paths(), .test_cypher_constants_present(), .test_find_blast_radius(), .test_find_paths_to_target()]
- "tests_test_detection_core_testcleandebianversion": "TestCleanDebianVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L971 | neighbors=[test_detection_core.py, .test_no_revision(), .test_strips_epoch(), .test_strips_revision(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testepssdb": "TestEpssDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L849 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_get_existing(), .test_get_missing(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testmakefindingid": "TestMakeFindingId" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L98 | neighbors=[test_detection_core.py, .test_deterministic(), .test_different_inputs_different_ids(), .test_length_16(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_validation_testedrparsing": "TestEDRParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L241 | neighbors=[test_detection_validation.py, .test_crowdstrike_parse(), .test_defender_parse_and_host_filter(), .test_factory(), .test_sentinelone_parse(), AttackAction]
- "tests_test_exploit_engine_testexploitorchestrator": "TestExploitOrchestrator" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L244 | neighbors=[test_exploit_engine.py, ._make_orchestrator(), .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve()]
- "vuln_nuclei_nucleirunreport": "NucleiRunReport" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L78 | neighbors=[nuclei.py, ._partial_or_raise(), .run_scan(), Machine-readable state for the most rec…, FindingImport, NessusScanRequest]
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=probe/agent/result_spool.py:L27 | neighbors=[result_spool.py, Persists scan results locally and retri…, .at_capacity(), .exists(), .flush_spool(), .__init__()]
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=probe/agent/use_cases.py:L1 | neighbors=[task_runner.py, resolve(), use_cases.py — the finite, pre-defined …, 01f4398 feat(probe): IoT survey reaches…, 10dfc80 Add comprehensive probe testing…, 5c8e696 docs(probe): correct overclaimi…]
- "ai_llm_report_llmunavailableerror": "LLMUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L46 | neighbors=[llm_report.py, ._complete(), RuntimeError, Raised when the Anthropic SDK or API ke…, HallucinationGuard, ReviewStatus]
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py]
- "branch:repo:github.com/Rutikm18/Project-Vedha#backup-before-secret-removal": "backup-before-secret-removal" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 5c8e696 docs(probe): correct overclaimi…, 8d65c92 first commit, 95904f1 feat(probe): detect SMB signing…]
- "commands_ask": "ask.ts" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L1 | neighbors=[requireAuth(), streamAsk(), buildAskCommand(), ConvMessage, runInteractive(), DiscoveredHost]
- "commands_interactive_runiterativeengagement": "runIterativeEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L816 | neighbors=[interactive.ts, runHostDiscoveryOnly(), chooseNextPhase(), confirm(), ln(), phaseLabel()]
- "detection_edr_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L31 | neighbors=[edr.py, .parse_response(), .is_prevented(), .parse_response(), .parse_response(), AttackAction]
- "engine_scan_modules": "scan-modules.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L1 | neighbors=[interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, defaultModules(), depthDefaults(), moduleById(), ModuleCategory]
- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET, positiveInt(), POST()]
- "lib_backend_backenderror": "BackendError" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L13 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, DashboardCharts.tsx, LiveOverview.tsx, PostureScorecard.tsx]
- "lib_security_context": "security-context.ts" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L1 | neighbors=[route.ts, route.ts, 1fe16c8 stable but some dead code, need…, route.ts, adapters.ts, toUiFinding()]
- "models_llm_output_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L12 | neighbors=[llm_output.py, Base, TimestampMixin, Every LLM generation is persisted here …, LLMReportGenerator, LLMUnavailableError]
- "probe_run_scan": "run_scan.py" | kind=code-symbol | source=probe/run_scan.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _orchestrate(), db_scanner.py, host_discovery.py, mass_scan.py]
- "routers_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _all_paths_to_critical(), _asset_labels(), attack_graph()]
- "services_posture": "posture.py" | kind=code-symbol | source=manager/backend/app/services/posture.py:L1 | neighbors=[045c9ae fix(posture): normalize run_at …, 237a831 feat(posture): add run comparis…, 5238865 feat(posture): add pure scoring…, aggregate(), build_posture(), _clamp01()]
- "tests_test_ad_assessment_testasreproastchecker": "TestASREPRoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L215 | neighbors=[test_ad_assessment.py, .setup_method(), .test_finding_shape(), .test_get_no_preauth_accounts(), .test_no_finding_when_empty(), .test_request_asrep_without_impacket()]
- "tests_test_ad_assessment_testntlmrelaychecker": "TestNTLMRelayChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L247 | neighbors=[test_ad_assessment.py, .setup_method(), .test_finding_for_ldap_signing_only(), .test_finding_includes_ntlmrelayx_comma…, .test_no_finding_when_all_secure(), .test_smb_signing_without_impacket_mark…]
- "tests_test_detection_core_testallosvsourcepackages": "TestAllOsvSourcePackages" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L993 | neighbors=[test_detection_core.py, .test_returns_list(), .test_sorted(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testclassifyconfidence": "TestClassifyConfidence" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L202 | neighbors=[test_detection_core.py, .test_authoritative_scanners(), .test_inferred_scanners(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testfindingpostinit": "TestFindingPostInit" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L113 | neighbors=[test_detection_core.py, .test_accepts_nonempty_evidence_refs(), .test_refuses_zero_evidence_refs(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testisip": "TestIsIp" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L212 | neighbors=[test_detection_core.py, .test_hostname(), .test_valid_ipv4(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testkevdb": "TestKevDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L838 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_is_kev(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testnormalize": "TestNormalize" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L960 | neighbors=[test_detection_core.py, .test_dispatches_banner(), .test_unknown_scanner_returns_empty(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testnormalizebanner": "TestNormalizeBanner" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L913 | neighbors=[test_detection_core.py, .test_empty_banner(), .test_ssh_banner(), ConsistencyReport, FindingConsistency, CPECandidate]
- "tests_test_detection_core_testproductfromcpe": "TestProductFromCpe" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L552 | neighbors=[test_detection_core.py, .test_extracts_product(), .test_short_cpe_returns_cpe(), ConsistencyReport, FindingConsistency, CPECandidate]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-005.json

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
