# Node Description Batch 42 of 336

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_remediation_routes_testupsertstatement": "TestUpsertStatement" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L188 | neighbors=[test_remediation_routes.py, Verify the ON CONFLICT logic at the SQL…, ._sql(), .test_refreshes_generated_at_on_conflic…, .test_regeneration_resets_review_gate_n…, .test_targets_the_unique_constraint()] | lang=en
- "tests_test_resolution_apply": "test_resolution_apply.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L1 | neighbors=[bd409f5 feat(resolution): async applier…, d98f654 feat(manager): network-VA campa…, _db_returning(), _finding(), test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…] | lang=en
- "tests_test_result_archive_ok_result": "_ok_result()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L53 | neighbors=[test_result_archive.py, .test_archived_json_equals_the_submitte…, .test_filename_is_result_plus_timestamp…, .test_no_partial_files_are_left_behind(), .test_two_jobs_in_the_same_second_do_no…, .test_empty_env_var_disables_archiving()] | lang=en
- "tests_test_scan_funnel_testrpcreconcile_funnel": "._funnel()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L267 | neighbors=[TestRpcReconcile, FakeDiscovery, _FakeMSRPC, _OpenSetPortFactory, _scope(), .test_advertised_ports_are_scanned_and_…] | lang=en
- "tests_test_scanner_congestion_testconnectcongestionwindow": "TestConnectCongestionWindow" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L144 | neighbors=[test_scanner_congestion.py, ._silent(), .test_all_silent_host_shrinks_the_windo…, .test_congestion_can_be_disabled(), .test_responsive_host_is_not_throttled(), .test_scan_completes_every_port_under_t…] | lang=en
- "tests_test_scope_validator_testmergeexclusions": "TestMergeExclusions" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L144 | neighbors=[test_scope_validator.py, .test_both_empty(), .test_empty_engagement_excludes(), .test_empty_job_excludes(), .test_merges_no_duplicates(), .test_none_job_excludes()] | lang=en
- "tests_test_smb_ntlm_build": "test_smb_ntlm_build.py" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, _challenge(), TestBuildMap, TestNtlmFingerprintFraming, TestParseChallenge, TestType1AndSpnego] | lang=en
- "tests_test_smtp_scanner": "test_smtp_scanner.py" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, TestParity, TestPureLogic, TestSMTPFindings, TestSMTPScanner] | lang=en
- "tests_test_stage2_reconcile_job": "_job()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L36 | neighbors=[test_stage2_reconcile.py, test_dead_lettered_facts_event_is_error…, test_fresh_heartbeat_reports_worker_ali…, test_multi_agent_all_covered_is_complet…, test_multi_agent_latest_done_but_earlie…, test_stale_heartbeat_with_pending_is_st…] | lang=en
- "tests_test_stage2_reconcile_rows": "_rows()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L32 | neighbors=[test_stage2_reconcile.py, test_dead_lettered_facts_event_is_error…, test_fresh_heartbeat_reports_worker_ali…, test_multi_agent_all_covered_is_complet…, test_multi_agent_latest_done_but_earlie…, test_stale_heartbeat_with_pending_is_st…] | lang=en
- "tests_test_stage2_reconcile_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L28 | neighbors=[test_stage2_reconcile.py, test_dead_lettered_facts_event_is_error…, test_fresh_heartbeat_reports_worker_ali…, test_multi_agent_all_covered_is_complet…, test_multi_agent_latest_done_but_earlie…, test_stale_heartbeat_with_pending_is_st…] | lang=en
- "tests_test_stage2_reconcile_test_fresh_heartbeat_reports_worker_alive": "test_fresh_heartbeat_reports_worker_alive()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L211 | neighbors=[test_stage2_reconcile.py, _hb(), _job(), _rows(), _run(), _scalars()] | lang=en
- "tests_test_stage2_reconcile_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L24 | neighbors=[test_stage2_reconcile.py, test_dead_lettered_facts_event_is_error…, test_fresh_heartbeat_reports_worker_ali…, test_multi_agent_all_covered_is_complet…, test_multi_agent_latest_done_but_earlie…, test_stale_heartbeat_with_pending_is_st…] | lang=en
- "tests_test_syn_scanner_testbuildresultsenrichment_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L350 | neighbors=[TestBuildResultsEnrichment, .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_os_guess_is_tagged_tcp_derived_no…, .test_p0f_stack_label_from_harvested_op…] | lang=en
- "tests_test_syn_scanner_testsynretransmit": "TestSynRetransmit" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L204 | neighbors=[test_syn_scanner.py, The raw SYN path resends ONLY still-sil…, ._patch(), .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…] | lang=en
- "tests_test_tarpit": "test_tarpit.py" | kind=code-symbol | source=probe/tests/test_tarpit.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, 9c973dd feat(scanner): tarpit/honeypot …, port_scanner.py, scanner_base.py, TestAssessTarpit, TestPortScannerTarpitFlag] | lang=en
- "tests_test_tls_fingerprint_testdigest": "TestDigest" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L83 | neighbors=[test_tls_fingerprint.py, .test_cipher_code_known_and_unknown(), .test_digest_differs_with_cipher(), .test_digest_is_62_chars(), .test_digest_is_deterministic(), .test_version_code()] | lang=en
- "tests_test_tls_integration_tlsserver": "_TLSServer" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L50 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade(), .__enter__(), .__exit__(), .__init__()] | lang=en
- "tests_test_udp_amplifiers": "test_udp_amplifiers.py" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L1 | neighbors=[fe868e6 feat(probe): real UDP amplifica…, udp_scanner.py, test_dns_open_recursion(), test_memcached_exposed(), test_ntp_monlist_absent(), test_ntp_monlist_enabled()] | lang=en
- "tests_test_va_campaign_buf": "_Buf" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L284 | neighbors=[test_va_campaign.py, .flush(), .__init__(), .isatty(), .write(), test_cli_view_deduplicates_unchanged_st…] | lang=en
- "tests_test_validation_endpoints_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L34 | neighbors=[test_validation_endpoints.py, _exec(), test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_deri…] | lang=en
- "tests_test_vnc_scanner": "test_vnc_scanner.py" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, TestParity, TestPureLogic, TestVNCFindings, TestVNCScanner] | lang=en
- "tests_test_weakness_map_wrapped": "_wrapped()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L43 | neighbors=[test_weakness_map.py, A detect-stage fact: ScanResult('findin…, .test_correlate_includes_weakness_findi…, .test_no_weakness_map_flag_disables_it(), .test_dedup_by_cve_target_port(), .test_smbv1_maps_to_eternalblue_with_li…] | lang=en
- "tools_probe_local_run": "probe_local_run.py" | kind=code-symbol | source=probe/tools/probe_local_run.py:L1 | neighbors=[b393dbe feat: Enhance Sidebar UI and in…, c7f226f chore: bundle pending working-t…, local_run.py, scanner_base.py, main(), summarize()] | lang=en
- "use_cases_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts] | lang=en
- "vuln_enrichment": "enrichment.py" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, TTLCache, VulnEnrichmentService, VulnEnrichmentService  External data so…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_enrichment_ttlcache_get": ".get()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L56 | neighbors=[TTLCache, .compute_composite_risk(), .enrich(), .fetch_epss(), .fetch_mitre_techniques(), .fetch_nvd()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_all": "._fetch_all()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L341 | neighbors=[Fetch NVD, EPSS, KEV and MITRE concurre…, VulnEnrichmentService, .enrich(), .check_cisa_kev(), .fetch_epss(), .fetch_mitre_techniques()] | lang=en
- "vuln_nessus": "nessus.py" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NessusScanner, NessusScanner — wraps the Tenable Nessu…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_nessus_nessusscanner_get_client": "._get_client()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L49 | neighbors=[NessusScanner, .create_scan(), .export_nessus_file(), ._auth_headers(), .get_results(), .launch_scan()] | lang=en
- "vuln_tasks_rationale_1": "Background tasks triggered after a vuln scan completes.  Pipeline:   1. Load all" | kind=entity | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[tasks.py, Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=pt
- "vuln_tasks_rationale_168": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L168 | neighbors=[_dedup_hash(), Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=en
- "vuln_tasks_rationale_171": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L171 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "vuln_tasks_rationale_35": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L35 | neighbors=[run_post_scan_enrichment(), Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=en
- "vuln_tasks_rationale_38": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L38 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "websocket_manager_agentconnectionmanager_is_connected": ".is_connected()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L293 | neighbors=[AgentConnectionManager, .run_backplane(), Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L405 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L424 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L414 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update., Broadcast a single node update., Broadcast a single node update., Broadcast a single node update.] | lang=en
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=probe/workflow/asset.py:L89 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
