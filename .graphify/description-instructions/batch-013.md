# Node Description Batch 14 of 227

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

- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L312 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[attack_timeline.py, Base, TimestampMixin, Append-only ledger of every attack acti…, AttackLogger, AttackLogger — records every attack act…]
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L47 | neighbors=[outbox.py, Base, TimestampMixin, Base, TimestampMixin, Event]
- "routers_agents_agent_ownership_check": "_agent_ownership_check()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L514 | neighbors=[agents.py, get_agent_jobs(), heartbeat(), Verify that the JWT token bearer IS the…, refresh_agent_registration(), submit_job_result()]
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L179 | neighbors=[agents.py, BaseModel, .validate_network_segments(), Asset, Engagement, ScanJobStatus]
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L205 | neighbors=[agents.py, BaseModel, .require_fence_for_running_job(), Asset, Engagement, ScanJobStatus]
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[_run_generation(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[_run_regeneration(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L61 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L47 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L65 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_integrations": "integrations.py" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 6be8259 feat(integrations): outbox deli…, dependencies.py, delete_integration(), integration_secret(), IntegrationIn]
- "routers_vuln_scans_rationale_278": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L278 | neighbors=[_run_nuclei_and_save(), Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L251 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L312 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "services_llm_airuntimeerror": "AiRuntimeError" | kind=code-symbol | source=manager/backend/app/services/llm.py:L21 | neighbors=[llm.py, RuntimeError, .__init__(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model()]
- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker]
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L405 | neighbors=[test_agents.py, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…, .test_empty_segments_are_fail_closed()]
- "tests_test_ai_normalizer_testextractrawtext": "TestExtractRawText" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L47 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_e2e_engagement_to_findings": "test_e2e_engagement_to_findings.py" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, task_runner.py, _accept_loop(), _manager(), _plant(), test_correlated_findings_cite_their_bas…]
- "tests_test_external_engine_wrappers": "test_external_engine_wrappers.py" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L1 | neighbors=[b4b12a9 Rename project and update files, mass_scan.py, nmap_wrapper.py, scanner_base.py, test_masscan_nonzero_with_valid_output_…, test_masscan_range_must_be_fully_in_sco…]
- "tests_test_main_scripts_accuracy": "test_main_scripts_accuracy.py" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_by_rule_breakdown(), test_clean_host_has_zero_false_positive…, test_corpus_flags_a_missed_expected_fin…, test_corpus_matches_real_engine_output(), test_corpus_scores_port_states_when_gro…]
- "tests_test_main_scripts_ja4x": "test_main_scripts_ja4x.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fake_cert(), test_empty_list_hashes_to_sentinel(), test_ja4x_format_is_three_12hex_fields(), test_ja4x_from_cert_handles_garbage(), test_ja4x_from_cert_matches_pure_core()]
- "tests_test_pipeline_ssh_inventory_jsonl": "_ssh_inventory_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L73 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=probe/tests/test_probe_core.py:L79 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()]
- "tests_test_scan_funnel": "test_scan_funnel.py" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scan_funnel.py, scanner_base.py, FakeDiscovery, FakePortScanner, _make_funnel()]
- "tests_test_vantage_fusion": "test_vantage_fusion.py" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _probe(), test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_…, test_empty_and_malformed_are_safe(), test_external_vantage_open_makes_port_e…]
- "ui_output_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L30 | neighbors=[output.ts, banner(), findingDetail(), findingLine(), findingsTable(), hostLine()]
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[b4b12a9 Rename project and update files, c7f226f chore: bundle pending working-t…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_workflow_execution.py]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, c7f226f chore: bundle pending working-t…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_probe_next_features.py]
- "workflow_execution_executiontrace": "ExecutionTrace" | kind=code-symbol | source=probe/workflow/execution.py:L231 | neighbors=[execution.py, .as_list(), .degraded(), ._ensure(), .failed(), .finalize()]
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=probe/agent/cli.py:L573 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()]
- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L177 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L31 | neighbors=[transport.py, DeviceAlreadyEnrolledError, Raised when a transport operation fails…, .bootstrap(), .connect_ws(), .poll_jobs()]
- "ai_prioritizer_vulnprioritizer": "VulnPrioritizer" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L99 | neighbors=[prioritizer.py, .explain_prediction(), .fallback_score(), ._formula_contributions(), .__init__(), .is_trained()]
- "auth_exceptions_authenticationerror": "AuthenticationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L28 | neighbors=[exceptions.py, VedhaAuthError, BcryptFailureError, DatabaseFailureError, DisabledTenantError, DisabledUserError]

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
