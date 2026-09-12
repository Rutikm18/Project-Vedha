# Node Description Batch 13 of 380

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

- "tests_test_ad_assessment_testbloodhoundcollector": "TestBloodHoundCollector" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L356 | neighbors=[test_ad_assessment.py, .setup_method(), .test_da_path_finding_critical_when_sho…, .test_da_path_finding_high_when_long(), .test_import_without_neo4j(), .test_no_finding_without_paths()]
- "tests_test_ad_assessment_testldapenumeratorparsing": "TestLDAPEnumeratorParsing" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L97 | neighbors=[test_ad_assessment.py, .test_domain_to_base_dn(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_attack_path_correlation": "test_attack_path_correlation.py" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _get(), _ids(), test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_device_role_from_facts_also_amplif…]
- "tests_test_attack_paths_testpathanalyzer": "TestPathAnalyzer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L112 | neighbors=[test_attack_paths.py, .test_blast_radius_unknown_asset(), .test_chokepoints_empty_without_paths(), .test_cypher_constants_present(), .test_find_blast_radius(), .test_find_paths_to_target()]
- "tests_test_cve_correlation": "test_cve_correlation.py" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L1 | neighbors=[6e2818f Add support for additional serv…, cli.py, correlator.py, ingest.py, vulndb.py, cpe.py]
- "tests_test_detection_core_testcleandebianversion": "TestCleanDebianVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1040 | neighbors=[test_detection_core.py, .test_no_revision(), .test_strips_epoch(), .test_strips_revision(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testepssdb": "TestEpssDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L918 | neighbors=[test_detection_core.py, .test_case_insensitive(), .test_get_existing(), .test_get_missing(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_core_testmakefindingid": "TestMakeFindingId" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L104 | neighbors=[test_detection_core.py, .test_deterministic(), .test_different_inputs_different_ids(), .test_length_16(), ConsistencyReport, FindingConsistency]
- "tests_test_detection_validation_testedrparsing": "TestEDRParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L268 | neighbors=[test_detection_validation.py, .test_crowdstrike_parse(), .test_defender_parse_and_host_filter(), .test_factory(), .test_sentinelone_parse(), AttackAction]
- "tests_test_exploit_engine_testexploitorchestrator": "TestExploitOrchestrator" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L244 | neighbors=[test_exploit_engine.py, ._make_orchestrator(), .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve()]
- "tests_test_job_cancel": "test_job_cancel.py" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _count(), _db(), _job(), _one(), test_cancel_records_who_did_it()]
- "tests_test_network_va_accuracy": "test_network_va_accuracy.py" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, engine.py, _Listener, test_etcd_is_identified_and_cpe_mapped(), test_every_planted_risk_port_is_found()]
- "tests_test_portal_read_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L26 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict(), .test_unknown_scan_type_is_422()]
- "tests_test_scan_funnel": "test_scan_funnel.py" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, scan_funnel.py, scanner_base.py, FakeDiscovery, _FakeMSRPC]
- "tests_test_service_posture_rules": "test_service_posture_rules.py" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _asset(), _corpus(), _fact(), _fire()]
- "tests_test_ssh_scanner": "test_ssh_scanner.py" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, scanner_base.py, _kexinit(), _nl(), TestEvaluate]
- "vuln_nuclei_nucleirunreport": "NucleiRunReport" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L78 | neighbors=[nuclei.py, ._partial_or_raise(), .run_scan(), Machine-readable state for the most rec…, FindingImport, NessusScanRequest]
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=probe/agent/agent.py:L1162 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet(), Detect common debugging/tracing tools. …, Detect common debugging/tracing tools. …]
- "agent_agent_load_or_create_identity": "_load_or_create_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1210 | neighbors=[agent.py, say(), _obtain_identity(), Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…]
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L91 | neighbors=[agent.py, _check_anti_debug(), _enroll_device(), _flush_spool_over_http(), _load_or_create_identity(), main()]
- "agent_local_run": "local_run.py" | kind=code-symbol | source=probe/agent/local_run.py:L1 | neighbors=[agent.py, _clean(), _main(), _parse_args(), _port_label(), _ports_from_env()]
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=probe/agent/result_spool.py:L27 | neighbors=[result_spool.py, Persists scan results locally and retri…, .at_capacity(), .exists(), .flush_spool(), .__init__()]
- "agent_setup": "setup.py" | kind=code-symbol | source=probe/agent/setup.py:L1 | neighbors=[build_parser(), cmd_collect_diagnostics(), cmd_config(), cmd_connect(), cmd_doctor(), cmd_self_scan()]
- "app_database": "database.py" | kind=code-symbol | source=manager/backend/app/database.py:L1 | neighbors=[config.py, get_db(), get_read_db(), dependencies.py, middleware.py, router.py]
- "approve_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/[id]/approve/route.ts:L1 | neighbors=[POST(), backend.ts, backend(), BackendError, bearerFrom(), with-backend.ts]
- "branch:repo:github.com/Rutikm18/Project-Vedha#backup-before-secret-removal": "backup-before-secret-removal" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 5c8e696 docs(probe): correct overclaimi…, 8d65c92 first commit, 95904f1 feat(probe): detect SMB signing…]
- "commands_ask": "ask.ts" | kind=code-symbol | source=manager/frontend/cli/commands/ask.ts:L1 | neighbors=[requireAuth(), streamAsk(), buildAskCommand(), ConvMessage, runInteractive(), DiscoveredHost]
- "commands_interactive_runiterativeengagement": "runIterativeEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L816 | neighbors=[interactive.ts, runHostDiscoveryOnly(), chooseNextPhase(), confirm(), ln(), phaseLabel()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@32feef6ad967e9b67c9439acb1b2eba507d8b4df": "32feef6 feat(engagement): enhance engagement metrics styling for better readabi…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@63d9c9a1c0afc8ba6edd5701b9603fba06b657a3": "63d9c9a fix(probe): recover from 409 when device key already enrolled" | kind=Commit | source=git | neighbors=[agent.py, transport.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer]
- "commit:repo:github.com/Rutikm18/Project-Vedha@78d51c5a8c9d6aaa3dabfd5ae21632e736865ea3": "78d51c5 opsec(scanner): de-sign service_enum UA — completes the sweep (task C6)" | kind=Commit | source=git | neighbors=[185e648 docs: pending-work inventory (b…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9b61c190ebbb02cde565390ea54bf2a5c806df8e": "9b61c19 feat(ui): improve engagement toolbar and metric card animations for enh…" | kind=Commit | source=git | neighbors=[32feef6 feat(engagement): enhance engag…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9c54022b619a38849646d9d912428a56b4073bbe": "9c54022 Refactor code structure and remove redundant sections for improved read…" | kind=Commit | source=git | neighbors=[6b41065 probe fixed, agent.py, transport.py, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer]
- "dashboard_dashboardworkspace": "DashboardWorkspace.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardWorkspace.tsx:L1 | neighbors=[page.tsx, 198bae4 snapshot: uncommitted system/ui…, DashboardCharts.tsx, DashboardCharts(), PageShell.tsx, PageShell()]
- "detection_edr_edrdetection": "EDRDetection" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L31 | neighbors=[edr.py, .parse_response(), .is_prevented(), .parse_response(), .parse_response(), AttackAction]
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, d0d1931 feat(detection): NVD/CPE vuln f…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, all_osv_source_packages(), clean_debian_version()]
- "engine_scan_modules": "scan-modules.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L1 | neighbors=[interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, defaultModules(), depthDefaults(), moduleById(), ModuleCategory]
- "exploit_msf_client_metasploitrpcerror": "MetasploitRPCError" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L23 | neighbors=[msf_client.py, ._call(), .connect(), ._raw_call(), .run_module(), Exception]
- "lib_security_context": "security-context.ts" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L1 | neighbors=[route.ts, route.ts, 1fe16c8 stable but some dead code, need…, route.ts, adapters.ts, toUiFinding()]
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-012.json

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
