# Node Description Batch 15 of 236

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

- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker]
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L413 | neighbors=[test_agents.py, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…, .test_empty_segments_are_fail_closed()]
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
- "workflow_execution_executiontrace": "ExecutionTrace" | kind=code-symbol | source=probe/workflow/execution.py:L231 | neighbors=[execution.py, .as_list(), .degraded(), ._ensure(), .failed(), .finalize()]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L178 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L880 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=probe/agent/cli.py:L573 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()]
- "agent_cli_output": "output()" | kind=code-symbol | source=probe/agent/cli.py:L177 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()]
- "ai_prioritizer_vulnprioritizer": "VulnPrioritizer" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L99 | neighbors=[prioritizer.py, .explain_prediction(), .fallback_score(), ._formula_contributions(), .__init__(), .is_trained()]
- "auth_exceptions_authenticationerror": "AuthenticationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L28 | neighbors=[exceptions.py, VedhaAuthError, BcryptFailureError, DatabaseFailureError, DisabledTenantError, DisabledUserError]
- "commands_admin": "admin.ts" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildAdminCommand(), c, PermittedUser, 10dfc80 Add comprehensive probe testing…]
- "commands_login": "login.ts" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L1 | neighbors=[loadSession(), saveSession(), serverUrl(), buildLoginCommand(), prompt(), promptSilent()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@00c6648b4d38308e37ce245514b25f99cb5b3ae9": "00c6648 feat(settings): editable email/Slack/Jira integrations wired to backend…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bc08715ed9a3be7d600b4595a6872f649784fd00": "bc08715 feat(agent): risk-tier action classification (fail-closed)" | kind=Commit | source=git | neighbors=[3569103 docs(agent): research + design …, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "commit:repo:github.com/Rutikm18/Project-Vedha@ecbb4adbc9733f25281faa5986dbcfdc1e7520ae": "ecbb4ad feat(agent): rules-of-engagement policy evaluation (verdict-vs-action, …" | kind=Commit | source=git | neighbors=[bc08715 feat(agent): risk-tier action c…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "detection_correlator_detectiongap": "DetectionGap" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L61 | neighbors=[correlator.py, .generate_gap_report(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[0236a60 fix(detection): full EPSS catal…, d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context()]
- "detection_resolution": "resolution.py" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, 9a36729 feat(resolution): coverage buil…, bd409f5 feat(resolution): async applier…, cbf5d6c feat(resolution): pure decision…, apply_manual_reopen(), build_coverage()]
- "detection_siem_elasticsiem": "ElasticSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L184 | neighbors=[siem.py, .build_query(), .parse_response(), .query_alerts(), SIEMQueryEngine, Elasticsearch via the _search API (KQL/…]
- "detection_siem_sentinelsiem": "SentinelSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L134 | neighbors=[siem.py, Microsoft Sentinel via the Azure Monito…, .build_kql(), .parse_response(), .query_alerts(), SIEMQueryEngine]
- "detection_siem_splunksiem": "SplunkSIEM" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L81 | neighbors=[siem.py, Splunk via the REST search endpoint (``…, SIEMQueryEngine, .build_spl(), .parse_response(), .query_alerts()]
- "discovery_worker_discoveryjobpayload": "DiscoveryJobPayload" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L42 | neighbors=[worker.py, .__post_init__(), RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost]
- "engine_types_discoveredhost": "DiscoveredHost" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L63 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, VedhaAuthError, MetasploitRPCError]
- "exploit_orchestrator_rationale_1": "ExploitOrchestrator — safe, scoped, audited exploit execution.  Every action is" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[orchestrator.py, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_107": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L107 | neighbors=[MetasploitRPCClient, .validate_safety(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_114": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L114 | neighbors=[MetasploitRPCClient, .validate_scope(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_134": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L134 | neighbors=[MetasploitRPCClient, .execute(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_256": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L256 | neighbors=[MetasploitRPCClient, .generate_dns_callback_token(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_269": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L269 | neighbors=[MetasploitRPCClient, ._check_blast_radius(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]
- "exploit_orchestrator_rationale_300": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L300 | neighbors=[MetasploitRPCClient, ._check_approval_required(), ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, SafetyViolationError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-014.json

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
