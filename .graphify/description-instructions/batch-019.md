# Node Description Batch 20 of 380

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

- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[_run_generation(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[_run_regeneration(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L61 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L47 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L65 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_vuln_scans_rationale_278": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L278 | neighbors=[_run_nuclei_and_save(), Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "scanner_nfs_scanner": "nfs_scanner.py" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, is_world_readable(), main(), NFSScanner, parse_mount_export(), parse_portmap_dump()]
- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/scanner/port_scanner.py:L339 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._is_ambiguous()]
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L473 | neighbors=[PortScanner, _family_of(), _harvest_tcp_stack(), ._build(), ._scan_port(), One connect() and its classification. A…]
- "scanner_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/scanner/port_scanner.py:L239 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()]
- "scanner_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=probe/scanner/scanner_base.py:L465 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()]
- "scanner_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/scanner/scanner_base.py:L968 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L938 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "scanner_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/scanner/scanner_base.py:L807 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()]
- "scanner_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L309 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L317 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "services_finding_content": "finding_content.py" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L1 | neighbors=[c6420a6 Add deterministic verification …, _build_exploitation(), detection_method(), _evidence(), exploit_maturity(), exploitation_signals()]
- "services_finding_events": "finding_events.py" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, build_timeline(), _decorate(), _detected_actor(), _detected_detail(), _ev()]
- "services_llm_airuntimeerror": "AiRuntimeError" | kind=code-symbol | source=manager/backend/app/services/llm.py:L93 | neighbors=[llm.py, RuntimeError, .__init__(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model()]
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L38 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, page.tsx]
- "tests_test_ad_assessment": "test_ad_assessment.py" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _enum_with_entries(), _FakeAttr, _FakeEntry, TestADCSChecker, TestASREPRoastChecker]
- "tests_test_ai_normalizer_testextractrawtext": "TestExtractRawText" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L47 | neighbors=[test_ai_normalizer.py, .test_db_scan_with_engine_and_version(), .test_db_scan_without_engine_returns_no…, .test_port_scan_returns_none(), .test_service_banner_falls_back_to_bann…, .test_service_banner_first_line_takes_p…]
- "tests_test_connect": "test_connect.py" | kind=code-symbol | source=probe/tests/test_connect.py:L1 | neighbors=[06ccae8 Phase 6: optional connect + upl…, _keypair(), _signed(), test_admit_job_enforces_local_scope_aft…, test_expired_job_is_rejected(), test_kill_switch_detects_stop_file()]
- "tests_test_detection_coverage": "test_detection_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _job(), _rows(), _run(), _scalars(), test_aggregating_reason_names_the_outbo…]
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, _action(), pytest_addoption()]
- "tests_test_e2e_engagement_to_findings": "test_e2e_engagement_to_findings.py" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, task_runner.py, _accept_loop(), _manager(), _plant(), test_correlated_findings_cite_their_bas…]
- "tests_test_external_engine_wrappers": "test_external_engine_wrappers.py" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L1 | neighbors=[b4b12a9 Rename project and update files, mass_scan.py, nmap_wrapper.py, scanner_base.py, test_masscan_nonzero_with_valid_output_…, test_masscan_range_must_be_fully_in_sco…]
- "tests_test_main_scripts_accuracy": "test_main_scripts_accuracy.py" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_by_rule_breakdown(), test_clean_host_has_zero_false_positive…, test_corpus_flags_a_missed_expected_fin…, test_corpus_matches_real_engine_output(), test_corpus_scores_port_states_when_gro…]
- "tests_test_main_scripts_ja4x": "test_main_scripts_ja4x.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fake_cert(), test_empty_list_hashes_to_sentinel(), test_ja4x_format_is_three_12hex_fields(), test_ja4x_from_cert_handles_garbage(), test_ja4x_from_cert_matches_pure_core()]
- "tests_test_new_scanners": "test_new_scanners.py" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, snmp_scanner.py, delta_engine(), _make_scan_record(), TestDeltaEngine]
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=probe/tests/test_probe_core.py:L79 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()]
- "tests_test_result_queue": "test_result_queue.py" | kind=code-symbol | source=probe/tests/test_result_queue.py:L1 | neighbors=[f8a6940 Phase 4: durable encrypted resu…, Clock, _q(), test_ack_removes_the_record(), test_age_prune_drops_stale_records(), test_backpressure_at_high_water()]
- "tests_test_scanner_congestion_testdeliveryawarebackoff": "TestDeliveryAwareBackoff" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L430 | neighbors=[test_scanner_congestion.py, Congestion control must react to a CHAN…, ._sc(), .test_collapsed_delivery_still_backs_of…, .test_each_scan_owns_its_delivery_windo…, .test_floor_is_clamped()]
- "tests_test_scheduler_sched": "_sched()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L31 | neighbors=[test_scheduler.py, .test_advances_from_now_not_from_the_mi…, .test_is_never_left_in_the_past(), .test_sets_last_run_and_next_by_interva…, .test_disabled_is_never_selected_even_w…, .test_exactly_due_is_selected()]
- "tests_test_vantage_fusion": "test_vantage_fusion.py" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _probe(), test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_…, test_empty_and_malformed_are_safe(), test_external_vantage_open_makes_port_e…]
- "tests_test_weakness_map": "test_weakness_map.py" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L1 | neighbors=[6e2818f Add support for additional serv…, cli.py, vulndb.py, weakness_map.py, db(), _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses": "TestCorrelateWeaknesses" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L69 | neighbors=[test_weakness_map.py, .test_cve_absent_from_mirror_still_emit…, .test_dedup_by_cve_target_port(), .test_exposure_boosts_risk(), .test_no_db_degrades_gracefully(), .test_obsolete_tls_both_when_both_offer…]
- "ui_output_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L30 | neighbors=[output.ts, banner(), findingDetail(), findingLine(), findingsTable(), hostLine()]
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L401 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process(), _reap_stale_runs()]
- "agent_agent_load_or_create_signing_identity": "_load_or_create_signing_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1259 | neighbors=[agent.py, _obtain_identity(), Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
