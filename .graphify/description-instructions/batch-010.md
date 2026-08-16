# Node Description Batch 11 of 209

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

- "str": "str" | kind=code-symbol | neighbors=[FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType, DetectionStatus]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, .__init__(), .__getitem__(), ADCSChecker, CertTemplate, ASREPRoastChecker]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, .setup_method(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_fallback_score_capped(), .test_higher_cvss_scores_higher()]
- "tests_test_customer_access": "test_customer_access.py" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, _added(), _mock_db(), _operator()]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, .skip_without_flag(), .test_connect_and_list_modules(), .test_run_safe_scanner_smb(), MetasploitRPCClient]
- "tests_test_main_scripts_correlation": "test_main_scripts_correlation.py" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L1 | neighbors=[6c1f014 feat(correlation): implement co…, _get(), _ids(), _run(), test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts()]
- "tests_test_main_scripts_findings_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L19 | neighbors=[test_main_scripts_findings.py, test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_ntp_monlist_and_dns_open_recursion…, test_open_filtered_never_raises_exposur…]
- "tests_test_main_scripts_rdp": "test_main_scripts_rdp.py" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _cc(), _run(), test_cc_without_negotiation_is_standard…, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…]
- "tests_test_main_scripts_unauth": "test_main_scripts_unauth.py" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, unauth_access.py, _run(), test_couchdb_and_memcached_and_mongodb(), test_elasticsearch_unauth_vs_secured(), test_non_datastore_service_is_unknown()]
- "tests_test_nessus_scanner": "test_nessus_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _mock_response(), scanner(), test_authenticate_api_key(), test_create_scan(), test_create_scan_with_credentials()]
- "tests_test_new_scanners_testmobilescanner": "TestMobileScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L515 | neighbors=[test_new_scanners.py, .test_adb_checksum_empty(), .test_adb_checksum_known_value(), .test_adb_cnxn_checksum_matches(), .test_adb_cnxn_command_field(), .test_adb_cnxn_magic_invariant()]
- "tests_test_nuclei_background_fakesession": "_FakeSession" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L30 | neighbors=[test_nuclei_background.py, .add(), .__aenter__(), .__aexit__(), .begin_nested(), .commit()]
- "tests_test_perf_optimization": "test_perf_optimization.py" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, clean_guard_cache(), test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_bin…, test_guard_is_noop_without_dpkg(), test_guard_passes_when_pure_python_agre…]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()]
- "tests_test_validation": "test_validation.py" | kind=code-symbol | source=probe/tests/test_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, validation.py, FakeClient, _preflight_responses(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…]
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=probe/agent/agent.py:L795 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), _flush_spool_over_http(), say(), _ws_run_job()]
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L733 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), _job_intent(), _result_summary()]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator]
- "auth_startup_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L51 | neighbors=[startup.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@01f43989ed63ef32dcf3abe8b305659ff281c464": "01f4398 feat(probe): IoT survey reaches the banner stage (service_fingerprint)" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@50d65540db573b6b680c257d3d693b216940069f": "50d6554 feat(active-validation): approve→enqueue endpoint + result ingestion (P…" | kind=Commit | source=git | neighbors=[3c277ba feat(lifecycle): add POST /find…, main.py, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c8e696210c1e7beaf5f6911e452bd38c701b1e8": "5c8e696 docs(probe): correct overclaiming use-case descriptions to match curren…" | kind=Commit | source=git | neighbors=[10dfc80 Add comprehensive probe testing…, use_cases.py, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@75650c143e0e92e93ca7fed76c46893953456bf8": "75650c1 feat: add Posture & Patch-Comparison Scorecard design spec" | kind=Commit | source=git | neighbors=[agent.py, config.py, ModelSwitcher.tsx, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cdee859546b57100944ef98e4f180fc049700dbe": "cdee859 feat(probe): add container/cloud/infra ports to IT catalog" | kind=Commit | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@e8262a30bd57c27b86d69584e3fee5ac6cd0af2b": "e8262a3 feat(probe): explicit unauthenticated_read fact for Redis exposure" | kind=Commit | source=git | neighbors=[95904f1 feat(probe): detect SMB signing…, backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main]
- "detection_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, attack_path_findings(), _bump(), _cleartext_cluster(), _exposed_db_unauth(), _group()]
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files()]
- "discovery_finding_translator": "finding_translator.py" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_probe_result(), create_scan_health_finding(), _escalate_by_exposure()]
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload]
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()]
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…, APP_VERSION]
- "hooks_usetoast": "useToast.ts" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, page.tsx, page.tsx, page.tsx, page.tsx, ToastContext]
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/login/page.tsx:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 81c81cb feat: implement outbox reclaim …, c52feb4 feat(portal): reskin User Porta…]
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L311 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-010.json

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
