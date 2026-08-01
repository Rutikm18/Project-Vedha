# Node Description Batch 16 of 119

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

- "scanner_discover": "discover.go" | kind=code-symbol | source=probe-go/scanner/discover.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, containsStr(), DiscoverHosts(), findStr(), intStr(), isRefused()]
- "scanner_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()]
- "scanner_scope": "scope.go" | kind=code-symbol | source=probe-go/scanner/scope.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, incrementIP(), lastIP(), NewScopeGuard(), ScopeFromFile()]
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/scanner/windows_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "services_job_result_service_rationale_1": "job_result_service.py — shared job result processing. Single source of truth for" | kind=entity | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_145": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L145 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, config.py, compute(), SlaResult, summarize(), _windows()]
- "states_datastate_skeletonrows": "SkeletonRows()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L24 | neighbors=[page.tsx, Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, page.tsx, page.tsx]
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L582 | neighbors=[test_agents.py, Discovery results → assets/services pro…, ScanJobType, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop()]
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()]
- "tests_test_detection_core_mock_kev_db": "_mock_kev_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L86 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_exploit_engine_testexploitorchestrator_make_orchestrator": "._make_orchestrator()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L246 | neighbors=[TestExploitOrchestrator, .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_nuclei_background_sessionfactory": "_SessionFactory" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L59 | neighbors=[test_nuclei_background.py, ScanJobStatus, .__call__(), .__init__(), NucleiRunReport, NucleiScanError]
- "tests_test_probe_core_testtuningfromparams": "TestTuningFromParams" | kind=code-symbol | source=probe/tests/test_probe_core.py:L839 | neighbors=[test_probe_core.py, .test_clamped_rate(), .test_defaults(), .test_no_ssh_creds_without_user(), .test_passive_listen_seconds(), .test_recheck_hours()]
- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes, TestValidateTargetsInScope]
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L300 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_client_errors_return_false_no_dat…, .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_server_error_returns_false()]
- "tools_issue_license": "issue_license.py" | kind=code-symbol | source=probe/tools/issue_license.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _b64(), issue(), keygen(), main()]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, FindingSeverity, FindingStatus, DependencyMissingError]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L758 | neighbors=[agent.py, main(), _load_or_create_identity(), say(), Return (agent_id, token, fresh, identit…, Return (agent_id, token, fresh, identit…]
- "agent_agent_run": ".Run()" | kind=code-symbol | source=probe-go/agent/agent.go:L52 | neighbors=[agent.py, .flushSpool(), .obtainIdentity(), .runPollLoop(), .runWSLoop(), say()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L613 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L498 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), say(), Run one job while keeping WS status/res…]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L495 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L103 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py]
- "agent_job_mapping_test": "job_mapping_test.go" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L1 | neighbors=[managerJob(), TestAdvertisedCapabilitiesHaveExecutabl…, TestMapToJobFailsClosedOnUnverifiableSc…, TestMapToJobMergesAuthoritativeExclusio…, TestMapToJobResolvesCanonicalUseCases(), TestMapToJobUsesParamsScanTypeAndPreser…]
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L52 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError]
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L101 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_state": "state.go" | kind=code-symbol | source=probe-go/agent/state.go:L1 | neighbors=[identityState, loadIdentityState(), saveIdentityState(), secureStateDirectory(), secureStatePath(), syncStateDirectory()]
- "agent_transport_transport_update_state": ".update_state()" | kind=code-symbol | source=probe/agent/transport.py:L180 | neighbors=[Merge and atomically persist private st…, Transport, .clear_state(), .save_state(), _atomic_write_private_state(), _sync_directory()]
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L262 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts]
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_refresh_token(), decode_token(), _now(), d1b4dd3 trim frontend to 7 core pages; …]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()]
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-015.json

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
