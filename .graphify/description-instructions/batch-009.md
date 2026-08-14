# Node Description Batch 10 of 186

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

- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L69 | neighbors=[exploits.py, BaseModel, _result_out(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[vuln_scans.py, Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, _dec()]
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip()]
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 72f68af feat(verification): expose veri…, 85e4537 feat(risk-rank): expose risk_ra…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …]
- "str": "str" | kind=code-symbol | neighbors=[FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType, DetectionStatus]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, .__init__(), .__getitem__(), ADCSChecker, CertTemplate, ASREPRoastChecker]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, .setup_method(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_fallback_score_capped(), .test_higher_cvss_scores_higher()]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, .skip_without_flag(), .test_connect_and_list_modules(), .test_run_safe_scanner_smb(), MetasploitRPCClient]
- "tests_test_main_scripts_correlation": "test_main_scripts_correlation.py" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L1 | neighbors=[6c1f014 feat(correlation): implement co…, _get(), _ids(), _run(), test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts()]
- "tests_test_main_scripts_findings_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L19 | neighbors=[test_main_scripts_findings.py, test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_ntp_monlist_and_dns_open_recursion…, test_open_filtered_never_raises_exposur…]
- "tests_test_nessus_scanner": "test_nessus_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _mock_response(), scanner(), test_authenticate_api_key(), test_create_scan(), test_create_scan_with_credentials()]
- "tests_test_new_scanners_testmobilescanner": "TestMobileScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L515 | neighbors=[test_new_scanners.py, .test_adb_checksum_empty(), .test_adb_checksum_known_value(), .test_adb_cnxn_checksum_matches(), .test_adb_cnxn_command_field(), .test_adb_cnxn_magic_invariant()]
- "tests_test_nuclei_background_fakesession": "_FakeSession" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L30 | neighbors=[test_nuclei_background.py, .add(), .__aenter__(), .__aexit__(), .begin_nested(), .commit()]
- "tests_test_perf_optimization": "test_perf_optimization.py" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, clean_guard_cache(), test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_bin…, test_guard_is_noop_without_dpkg(), test_guard_passes_when_pure_python_agre…]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()]
- "tests_test_validation": "test_validation.py" | kind=code-symbol | source=probe/tests/test_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, validation.py, FakeClient, _preflight_responses(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L991 | neighbors=[agent.py, main(), _enroll_device(), _load_or_create_identity(), _load_or_create_signing_identity(), say()]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator]
- "auth_startup_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L51 | neighbors=[startup.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, backup-before-secret-removal, feat/coverage-gated-auto-resolution, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, feat/coverage-gated-auto-resolution, integration/all-branches, main, spike/probe-go]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, backup-before-secret-removal, feat/coverage-gated-auto-resolution, integration/all-branches, main]
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, NAV_SECTIONS]
- "components_themeprovider": "ThemeProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L1 | neighbors=[layout.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, subscribeToHydration()]
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files()]
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload]
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()]
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L1 | neighbors=[30261eb feat: enhance advisor flow with…, a4b970c feat(fleet): add run command fo…, b5ffcb0 Refactor Vedha probe installer …, PageShell.tsx, PageShell(), EnrollmentRequest]
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "login_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, backend.ts, backend()]
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_ip_header(), build_syn_packet(), build_tcp_syn(), classify(), _local_source_ip()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-009.json

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
