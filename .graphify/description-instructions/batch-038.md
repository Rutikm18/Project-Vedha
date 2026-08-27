# Node Description Batch 39 of 236

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_resolution_decision": "test_resolution_decision.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L1 | neighbors=[cbf5d6c feat(resolution): pure decision…, test_db_change_blocks_resolution(), test_high_needs_two_covered_clean_runs(), test_medium_resolves_on_first_covered_c…, test_not_covered_is_skipped_and_counter…, test_threshold_is_stricter_for_critical…]
- "tests_test_scanner_parity": "test_scanner_parity.py" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _py_files(), test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_…, test_scanner_module_matches_main_script…, test_scanner_parity.py — the no-drift g…]
- "tests_test_scope_crypt": "test_scope_crypt.py" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, scope_crypt.py, TestEncryptDecryptRoundtrip, TestKeyGeneration, Tests for agent/scope_crypt.py, 2885afa Add comprehensive probe testing…]
- "tests_test_scope_targets_testtargetswithinscope": "TestTargetsWithinScope" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L23 | neighbors=[test_scope_targets.py, .test_cidr_subset_in_scope(), .test_no_targets_returns_whole_scope(), .test_range_expands_to_covered_networks…, .test_single_ip_in_scope(), .test_string_target_is_accepted()]
- "tests_test_scope_validator_testfetchengagementscope": "TestFetchEngagementScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L170 | neighbors=[test_scope_validator.py, .test_http_get_raises(), .test_http_get_returns_incomplete(), .test_http_get_returns_none(), .test_returns_excludes(), .test_returns_scope_from_http_get()]
- "tests_test_seed_admin_testvalidateenv": "TestValidateEnv" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L38 | neighbors=[test_seed_admin.py, .test_all_known_weak_passwords_blocked_…, .test_allows_weak_password_in_developme…, .test_raises_on_weak_password_in_produc…, .test_raises_when_email_missing(), .test_returns_force_reset_true()]
- "tests_test_service_match_testotherservices": "TestOtherServices" | kind=code-symbol | source=probe/tests/test_service_match.py:L58 | neighbors=[test_service_match.py, .test_mariadb_handshake(), .test_redis_info(), .test_redis_noauth(), .test_smtp_postfix(), .test_vsftpd()]
- "tests_test_syn_scanner_testbuildresultsenrichment": "TestBuildResultsEnrichment" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L348 | neighbors=[test_syn_scanner.py, ._scanner(), .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_windows_ttl_maps_to_windows()]
- "tests_test_syn_scanner_testoptionparsing": "TestOptionParsing" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L303 | neighbors=[test_syn_scanner.py, .test_malformed_options_never_raise(), .test_mss_absent_returns_none(), .test_mss_after_nop_padding(), .test_mss_extracted(), .test_mss_skips_other_options()]
- "tests_test_tarpit": "test_tarpit.py" | kind=code-symbol | source=probe/tests/test_tarpit.py:L1 | neighbors=[9c973dd feat(scanner): tarpit/honeypot …, port_scanner.py, scanner_base.py, TestAssessTarpit, TestPortScannerTarpitFlag, test_tarpit.py — tarpit / honeypot dete…]
- "tests_test_tarpit_testassesstarpit": "TestAssessTarpit" | kind=code-symbol | source=probe/tests/test_tarpit.py:L17 | neighbors=[test_tarpit.py, .test_boundary_floor_and_ratio_trip_exa…, .test_busy_real_host_is_not_flagged(), .test_nearly_all_open_large_scan_is_fla…, .test_tiny_all_open_scan_is_below_the_f…, .test_zero_attempted_is_safe()]
- "tests_test_tls_fingerprint": "test_tls_fingerprint.py" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello, test_tls_fingerprint.py — Tier 2.3: act…]
- "tests_test_tls_posture": "test_tls_posture.py" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, tls_scanner.py, _modern(), TestClassifyCipher, TestGradeTlsPosture, test_tls_posture.py — Tier 2.4: cipher-…]
- "tests_test_validation_endpoints_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L50 | neighbors=[test_validation_endpoints.py, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_deri…, test_reject_marks_rejected()]
- "tests_test_validation_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_validation.py:L110 | neighbors=[test_validation.py, .__init__(), .request(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_ingest_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L23 | neighbors=[test_validation_ingest.py, test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…, test_inconclusive_leaves_finding_unchan…, test_ingest_confirmed_updates_request_a…]
- "tests_test_verification_core": "test_verification_core.py" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, test_authoritative_is_confirmed(), test_high_confidence_inferred_is_corrob…, test_kev_suspected_finding_needs_review…, test_low_confidence_inferred_is_inferre…, test_missing_confidence_defaults_to_inf…]
- "tests_test_version_compare": "test_version_compare.py" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, test_dpkg_compare_public_api(), test_pure_python_matches_known_pairs(), test_pure_python_matches_real_dpkg_bina…, Cross-validates the pure-Python Debian …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_wire_identity_testchoosesourceport": "TestChooseSourcePort" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L38 | neighbors=[test_wire_identity.py, Evasion: a fixed source port (e.g. 53/8…, .test_boundary_ports_are_valid(), .test_none_gives_random_ephemeral(), .test_out_of_range_falls_back_to_random…, .test_uses_configured_valid_port()]
- "tools_installer_managedpath": "managedPath()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L48 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), isManaged(), removeTool()]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nuclei_nucleiscanner_parse_output": ".parse_output()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L381 | neighbors=[NucleiScanner, ._map_finding(), Parse nuclei JSONL output → list of Fin…, Parse nuclei JSONL output → list of Fin…, .run_scan(), Parse nuclei JSONL output → list of Fin…]
- "websocket_manager_agentconnectionmanager_is_connected": ".is_connected()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L291 | neighbors=[AgentConnectionManager, .run_backplane(), Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.]
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L403 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…]
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L422 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…]
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L412 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update., Broadcast a single node update., Broadcast a single node update., Broadcast a single node update.]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L63 | neighbors=[outbox.py, _claim_batch(), main(), run_worker(), OutboxEvent, ScanResult]
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=probe/workflow/asset.py:L82 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…]
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L63 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_poll_jobs_or_empty": "_poll_jobs_or_empty()" | kind=code-symbol | source=probe/agent/agent.py:L198 | neighbors=[agent.py, main(), Poll for work. Auth failures (Transport…, say(), Return no work for transient poll failu…]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L274 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L59 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L33 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L46 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
