# Node Description Batch 17 of 236

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

- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L864 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "states_datastate_skeletonrows": "SkeletonRows()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L26 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx]
- "tests_test_ad_assessment_rationale_1": "Unit tests for the Active Directory assessment module (Prompt 5).  All directory" | kind=entity | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_enqueue_intensity": "test_enqueue_intensity.py" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_every_manager_code_maps_to_a_known…, test_intensity_accepts_code_or_name(), test_invalid_intensity_is_rejected_at_t…, test_normalize_intensity_name_maps_code…, test_numeric_uc_code_accepted()]
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=probe/tests/test_http_lease.py:L1 | neighbors=[0e22dbf feat(probe): bounded auto-troub…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, engine.py, transport.py]
- "tests_test_main_scripts_completeness": "test_main_scripts_completeness.py" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, port_scanner.py, scanner_base.py, _metrics(), _rec(), test_duplicate_port_is_detected()]
- "tests_test_main_scripts_coverage": "test_main_scripts_coverage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, ae08d19 feat(scanner): adaptive timeout…, port_scanner.py, scanner_base.py, _closed(), _mk_scanner()]
- "tests_test_new_scanners": "test_new_scanners.py" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, snmp_scanner.py, delta_engine(), _make_scan_record(), TestDeltaEngine, TestIoTScanner]
- "tests_test_new_scanners_testdeltaengine": "TestDeltaEngine" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L380 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner_fakeprocess": "FakeProcess" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L30 | neighbors=[test_nuclei_scanner.py, .__init__(), .kill(), .terminate(), .wait(), test_nonzero_exit_retains_and_marks_par…]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L322 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_probe_enrollment": "test_probe_enrollment.py" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, test_device_access_token_has_dedicated_…, test_ed25519_proof_of_possession_reject…, test_enroll_token_create_defaults_and_b…, test_enroll_token_usable_only_while_liv…]
- "tests_test_smb_scanner": "test_smb_scanner.py" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 95904f1 feat(probe): detect SMB signing…, smb_scanner.py, _smb2_error_response(), _smb2_negotiate_response(), test_error_response_not_parsed_as_signi…]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, task_runner.py, _fake_run_scan(), runner()]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "tests_test_validation_ingest": "test_validation_ingest.py" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _finding(), test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string(), .test_malformed_xml_returns_empty()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]
- "workflow_execution": "execution.py" | kind=code-symbol | source=probe/workflow/execution.py:L1 | neighbors=[engine.py, b4b12a9 Rename project and update files, test_passive_collector.py, test_workflow_execution.py, scanner_base.py, classify_scanner_error()]
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()]
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=probe/agent/agent.py:L927 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet(), Detect common debugging/tracing tools. …, Detect common debugging/tracing tools. …]
- "agent_agent_load_or_create_identity": "_load_or_create_identity()" | kind=code-symbol | source=probe/agent/agent.py:L975 | neighbors=[agent.py, say(), _obtain_identity(), Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L226 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L29 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "assistant_assistantprovider": "AssistantProvider.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L1 | neighbors=[layout.tsx, AssistantDrawer.tsx, AssistantFab.tsx, AssistantDrawer(), AssistantFab(), AssistantCtx]
- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, agent_jwt_path_allows(), _is_public_enrollment_request(), TenantIsolationMiddleware, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()]
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[apiFetch(), requireAuth(), AiReport, buildReportCommand(), Engagement, errExit()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2b4ff7132c98967429d138e7459f25f879023fc7": "2b4ff71 feat(fleet): one-click Approve Site — optional name, no code/fields (it…" | kind=Commit | source=git | neighbors=[route.ts, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@37fa611652538968dbf827eaf98cdcab59c052b2": "37fa611 harden(scanner): XML-entity guard + list-form argv (CWE-611/78/88)" | kind=Commit | source=git | neighbors=[2c53ae9 evasion(scanner): randomized sc…, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 2de251b feat(scanner): ICMP timestamp f…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9c973dd02e4777bcd7cebae84b6c80fd96fa001f": "9c973dd feat(scanner): tarpit/honeypot detection in port-scan summary (C5)" | kind=Commit | source=git | neighbors=[2de251b feat(scanner): ICMP timestamp f…, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 5b980e1 docs(spec): installer warning +…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@aedddfae1bea375d5864f92e26f2ceb7f0bf8065": "aedddfa feat(settings): editable SLA policy windows wired to backend (item 4 UI)" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@dec1e7cfa829a295630af88da9f11a5f2e8175d4": "dec1e7c fix(scanner): resolve() family fallback for dual-stack hosts (task A9)" | kind=Commit | source=git | neighbors=[78d51c5 opsec(scanner): de-sign service…, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 2c53ae9 evasion(scanner): randomized sc…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@eff17d69ed457a0f00a6cec466932ff1357fb74f": "eff17d6 feat(probe): one-click approve endpoint — no code, auto name/caps/scope…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f8ff2296e5ec2c593a6bed4ab40633d8a857d40f": "f8ff229 feat(ui): remove decorative session clock from both dashboards (item 6)" | kind=Commit | source=git | neighbors=[ecbb4ad feat(agent): rules-of-engagemen…, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fc7afc36732bf000de12e42189e63124bd643652": "fc7afc3 chore(graphify): refresh knowledge graph for remediation subsystem" | kind=Commit | source=git | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L18 | neighbors=[page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx, page.tsx]
- "components_toastprovider": "ToastProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, Toast, TOAST_STYLES, ToastContext, ToastContextValue]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-016.json

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
