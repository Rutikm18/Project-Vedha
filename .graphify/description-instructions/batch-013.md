# Node Description Batch 14 of 209

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

- "routers_engagements_rationale_40": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L40 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_41": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L41 | neighbors=[_compute_overview(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_645": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L645 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_668": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L668 | neighbors=[get_engagement_scope(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_engagements_rationale_97": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[Asset, Engagement, AssetType, EngagementStatus, FindingSeverity, FindingStatus]
- "routers_engagements_rationale_98": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L98 | neighbors=[_refresh_overview_cache(), Asset, Engagement, AssetType, EngagementStatus, FindingSeverity]
- "routers_exploits_rationale_1": "Exploit validation API.  POST /exploits/run              — request exploit valid" | kind=entity | source=manager/backend/app/routers/exploits.py:L1 | neighbors=[exploits.py, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "routers_exploits_rationale_455": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L455 | neighbors=[_run_approved_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "routers_exploits_rationale_456": "Background task: run the exploit after manager approval." | kind=entity | source=manager/backend/app/routers/exploits.py:L456 | neighbors=[MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError, AuditLog]
- "routers_vuln_scans_rationale_272": "Background task: run nuclei, persist findings, trigger enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L272 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_findings_scanner": "_scanner()" | kind=code-symbol | source=probe/scanner/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_rdp(), _rule_smb(), _rule_snmp()]
- "scanner_mobile_scanner": "mobile_scanner.py" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), main(), MobileScanner]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L180 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "states_datastate_skeletonrows": "SkeletonRows()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L26 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx]
- "tests_test_ad_assessment_rationale_1": "Unit tests for the Active Directory assessment module (Prompt 5).  All directory" | kind=entity | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_enqueue_intensity": "test_enqueue_intensity.py" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_every_manager_code_maps_to_a_known…, test_intensity_accepts_code_or_name(), test_invalid_intensity_is_rejected_at_t…, test_normalize_intensity_name_maps_code…, test_numeric_uc_code_accepted()]
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=probe/tests/test_http_lease.py:L1 | neighbors=[0e22dbf feat(probe): bounded auto-troub…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, engine.py, transport.py]
- "tests_test_main_scripts_completeness": "test_main_scripts_completeness.py" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, port_scanner.py, scanner_base.py, _metrics(), _rec(), test_duplicate_port_is_detected()]
- "tests_test_main_scripts_coverage": "test_main_scripts_coverage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, ae08d19 feat(scanner): adaptive timeout…, port_scanner.py, scanner_base.py, _closed(), _mk_scanner()]
- "tests_test_new_scanners": "test_new_scanners.py" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, snmp_scanner.py, delta_engine(), _make_scan_record(), TestDeltaEngine, TestIoTScanner]
- "tests_test_new_scanners_testdeltaengine": "TestDeltaEngine" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L377 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner_fakeprocess": "FakeProcess" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L30 | neighbors=[test_nuclei_scanner.py, .__init__(), .kill(), .terminate(), .wait(), test_nonzero_exit_retains_and_marks_par…]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L322 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_probe_enrollment": "test_probe_enrollment.py" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, test_device_access_token_has_dedicated_…, test_ed25519_proof_of_possession_reject…, test_enroll_token_create_defaults_and_b…, test_enroll_token_usable_only_while_liv…]
- "tests_test_smb_scanner": "test_smb_scanner.py" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 95904f1 feat(probe): detect SMB signing…, smb_scanner.py, _smb2_error_response(), _smb2_negotiate_response(), test_error_response_not_parsed_as_signi…]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, task_runner.py, _fake_run_scan(), runner()]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "tests_test_validation_ingest": "test_validation_ingest.py" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _finding(), test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string(), .test_malformed_xml_returns_empty()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_workflow_execution.py, scanner_base.py]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_probe_next_features.py, scanner_base.py]
- "workflow_execution": "execution.py" | kind=code-symbol | source=probe/workflow/execution.py:L1 | neighbors=[engine.py, b4b12a9 Rename project and update files, test_passive_collector.py, test_workflow_execution.py, scanner_base.py, classify_scanner_error()]
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L871 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L226 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L29 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L31 | neighbors=[transport.py, Raised when a transport operation fails…, .bootstrap(), .connect_ws(), .poll_jobs(), .refresh_registration()]
- "assistant_assistantprovider": "AssistantProvider.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L1 | neighbors=[layout.tsx, AssistantDrawer.tsx, AssistantFab.tsx, AssistantDrawer(), AssistantFab(), AssistantCtx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-013.json

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
