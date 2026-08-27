# Node Description Batch 9 of 92

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

- "scanner_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=scanner/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()] | lang=en
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=scanner/syn_scanner.py:L312 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()] | lang=en
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()] | lang=en
- "tests_test_adaptive_rate": "test_adaptive_rate.py" | kind=code-symbol | source=tests/test_adaptive_rate.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scanner_base.py, _EchoProtocol, TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating] | lang=en
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()] | lang=en
- "tests_test_main_scripts_vantage_r": "_r()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L12 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…] | lang=en
- "tests_test_main_scripts_vantage_testreconcilevantages": "TestReconcileVantages" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L16 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…] | lang=en
- "tests_test_probe_core_testtuningfromparams": "TestTuningFromParams" | kind=code-symbol | source=tests/test_probe_core.py:L861 | neighbors=[test_probe_core.py, .test_clamped_rate(), .test_defaults(), .test_no_ssh_creds_without_user(), .test_passive_listen_seconds(), .test_recheck_hours()] | lang=en
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=tests/test_scope_validator.py:L93 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_fully_excluded_cidr_is_dropped(), .test_hostname_passes_through()] | lang=en
- "tests_test_tls_integration": "test_tls_integration.py" | kind=code-symbol | source=tests/test_tls_integration.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scanner_base.py, tls_scanner.py, _self_signed(), test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()] | lang=en
- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()] | lang=en
- "tests_test_wire_identity": "test_wire_identity.py" | kind=code-symbol | source=tests/test_wire_identity.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, TestChooseSourcePort, TestEvasionFlags, TestJitteredDelay, TestModuleConstantsUnbranded, TestProbePayload] | lang=en
- "workflow_asset_asset_merge_result": ".merge_result()" | kind=code-symbol | source=workflow/asset.py:L95 | neighbors=[Asset, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…] | lang=en
- "workflow_cli": "cli.py" | kind=code-symbol | source=workflow/cli.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, scanner_base.py, _build_creds(), _build_mode(), build_parser(), _main()] | lang=en
- "workflow_gates_gate_5_branch_eligible": "gate_5_branch_eligible()" | kind=code-symbol | source=workflow/gates.py:L87 | neighbors=[gates.py, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …, Does `branch` apply to this host?      …] | lang=en
- "agent_agent_enroll_device": "_enroll_device()" | kind=code-symbol | source=agent/agent.py:L1050 | neighbors=[agent.py, _bounded_env_int(), _classify_connection_error(), _dbg(), say(), _obtain_identity()] | lang=en
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=agent/cli.py:L495 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()] | lang=en
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=agent/cli.py:L103 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()] | lang=en
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=agent/engine.py:L377 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()] | lang=en
- "agent_engine_derive_post_stage": "_derive_post_stage()" | kind=code-symbol | source=agent/engine.py:L442 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), Return (extra ScanResults to append as …, run_scan(), _results_by_target()] | lang=en
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError] | lang=en
- "agent_local_run_main": "_main()" | kind=code-symbol | source=agent/local_run.py:L158 | neighbors=[local_run.py, _parse_args(), _ports_from_env(), _scope_file(), summarize(), _usage_error()] | lang=en
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()] | lang=en
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=agent/transport.py:L208 | neighbors=[Transport, .activate_enrollment(), .ensure_device_access(), .__init__(), .refresh_device_access(), .refresh_registration()] | lang=en
- "main_scripts_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L160 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()] | lang=en
- "main_scripts_findings_by_target": "_by_target()" | kind=code-symbol | source=main_scripts/findings.py:L1006 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()] | lang=en
- "main_scripts_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=main_scripts/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()] | lang=en
- "main_scripts_ja4x": "ja4x.py" | kind=code-symbol | source=main_scripts/ja4x.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious()] | lang=en
- "main_scripts_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=main_scripts/mass_scan.py:L51 | neighbors=[mass_scan.py, BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=main_scripts/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()] | lang=en
- "main_scripts_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L237 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()] | lang=en
- "main_scripts_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=main_scripts/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()] | lang=en
- "main_scripts_run_all": "run_all.py" | kind=code-symbol | source=main_scripts/run_all.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _log(), main(), _open_tcp_ports(), _ports_arg(), _read_jsonl()] | lang=en
- "main_scripts_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=main_scripts/scanner_base.py:L864 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=main_scripts/scanner_base.py:L564 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()] | lang=en
- "main_scripts_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/service_enum.py:L529 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()] | lang=en
- "main_scripts_syn_scanner_rationale_1": "syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH" | kind=entity | source=main_scripts/syn_scanner.py:L1 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_105": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=main_scripts/syn_scanner.py:L105 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_syn_scanner_rationale_126": "Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked" | kind=entity | source=main_scripts/syn_scanner.py:L126 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_152": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also" | kind=entity | source=main_scripts/syn_scanner.py:L152 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-008.json

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
