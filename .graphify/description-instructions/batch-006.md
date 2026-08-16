# Node Description Batch 7 of 209

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
Write every description in Portuguese (pt). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_engine_version_compare": "version_compare.py" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part()]
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L1 | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, 30261eb feat: enhance advisor flow with…, a4b970c feat(fleet): add run command fo…, b5ffcb0 Refactor Vedha probe installer …, c4386e4 feat(customers): operator Custo…, PageShell.tsx]
- "generate_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, POST(), backend.ts, backend(), BackendError]
- "graph_builder_graphbuilder": "GraphBuilder" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L90 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph(), .build_from_db()]
- "lib_backend_bearerfrom": "bearerFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L97 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_cases_store": "cases-store.ts" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addComment(), Case, CaseActivity, CaseComment, CaseSeverity]
- "lib_testssl_parser": "testssl-parser.ts" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, LiveFinding, Severity]
- "models_enums_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L81 | neighbors=[enums.py, str, LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _ConnectSweep, _have_masscan(), main()]
- "scans_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, c52feb4 feat(portal): reskin User Porta…, portal-client.ts, portalApi(), PortalEngagement, PortalScan]
- "tests_findings_store_test": "findings-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, LiveFinding, resetCounters(), getAllFindings(), getFindingById()]
- "tests_test_ad_assessment_fakeentry": "_FakeEntry" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L36 | neighbors=[test_ad_assessment.py, .__getitem__(), .__init__(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account()]
- "tests_test_ad_assessment_testbloodhoundcollector": "TestBloodHoundCollector" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L356 | neighbors=[test_ad_assessment.py, .setup_method(), .test_da_path_finding_critical_when_sho…, .test_da_path_finding_high_when_long(), .test_import_without_neo4j(), .test_no_finding_without_paths()]
- "tests_test_ad_assessment_testldapenumeratorparsing": "TestLDAPEnumeratorParsing" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L97 | neighbors=[test_ad_assessment.py, .test_domain_to_base_dn(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_attack_path_correlation": "test_attack_path_correlation.py" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _get(), _ids(), test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_device_role_from_facts_also_amplif…]
- "tests_test_attack_paths_testpathanalyzer": "TestPathAnalyzer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L112 | neighbors=[test_attack_paths.py, .test_blast_radius_unknown_asset(), .test_chokepoints_empty_without_paths(), .test_cypher_constants_present(), .test_find_blast_radius(), .test_find_paths_to_target()]
- "tests_test_detection_core_testcleandebianversion": "TestCleanDebianVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L971 | neighbors=[test_detection_core.py, .test_no_revision(), .test_strips_epoch(), .test_strips_revision(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testepssdb": "TestEpssDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L849 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_get_existing(), .test_get_missing(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testmakefindingid": "TestMakeFindingId" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L98 | neighbors=[test_detection_core.py, .test_deterministic(), .test_different_inputs_different_ids(), .test_length_16(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_validation_testedrparsing": "TestEDRParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L241 | neighbors=[test_detection_validation.py, .test_crowdstrike_parse(), .test_defender_parse_and_host_filter(), .test_factory(), .test_sentinelone_parse(), AttackAction]
- "tests_test_exploit_engine_testexploitorchestrator": "TestExploitOrchestrator" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L244 | neighbors=[test_exploit_engine.py, ._make_orchestrator(), .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve()]
- "tests_test_portal_read_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L26 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict(), .test_unknown_scan_type_is_422()]
- "vuln_nuclei_nucleirunreport": "NucleiRunReport" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L78 | neighbors=[nuclei.py, ._partial_or_raise(), .run_scan(), Machine-readable state for the most rec…, FindingImport, NessusScanRequest]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1182 | neighbors=[agent.py, main(), _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device()]
- "agent_agent_run_ws_push_loop": "_run_ws_push_loop()" | kind=code-symbol | source=probe/agent/agent.py:L549 | neighbors=[agent.py, main(), Persistent WebSocket push loop.      Re…, _flush_spool_over_http(), say(), _ws_heartbeat_sender()]
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=probe/agent/result_spool.py:L27 | neighbors=[result_spool.py, Persists scan results locally and retri…, .at_capacity(), .exists(), .flush_spool(), .__init__()]
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py]
- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, _authenticate(), create_personal_access_token(), list_personal_access_tokens()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#backup-before-secret-removal": "backup-before-secret-removal" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 5c8e696 docs(probe): correct overclaimi…, 8d65c92 first commit, 95904f1 feat(probe): detect SMB signing…]
- "commands_ask": "ask.ts" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L1 | neighbors=[requireAuth(), streamAsk(), buildAskCommand(), ConvMessage, runInteractive(), DiscoveredHost]
- "commands_interactive_runiterativeengagement": "runIterativeEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L816 | neighbors=[interactive.ts, runHostDiscoveryOnly(), chooseNextPhase(), confirm(), ln(), phaseLabel()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@35f02a999c05b5ec503c4c44f7f158f5d0018937": "35f02a9 feat(portal): rich scan request (type/targets/intensity) + dashboard en…" | kind=Commit | source=git | neighbors=[portal_scope.py, feat/syn-scanner-osfp-adaptive, main, c52feb4 feat(portal): reskin User Porta…, scan_request.py, agents.py]
- "detection_edr_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L31 | neighbors=[edr.py, .parse_response(), .is_prevented(), .parse_response(), .parse_response(), AttackAction]
- "engine_scan_modules": "scan-modules.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L1 | neighbors=[interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, defaultModules(), depthDefaults(), moduleById(), ModuleCategory]
- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception]
- "lib_security_context": "security-context.ts" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L1 | neighbors=[route.ts, route.ts, 1fe16c8 stable but some dead code, need…, route.ts, adapters.ts, toUiFinding()]
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …]
- "models_llm_output_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L12 | neighbors=[llm_output.py, Base, TimestampMixin, Every LLM generation is persisted here …, LLMReportGenerator, LLMUnavailableError]
- "routers_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, _all_paths_to_critical(), _asset_labels(), attack_graph()]
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, ae08d19 feat(scanner): adaptive timeout…, build_ip_header(), build_syn_packet(), build_tcp_syn()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-006.json

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
