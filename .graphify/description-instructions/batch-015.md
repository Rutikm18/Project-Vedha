# Node Description Batch 16 of 330

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

- "tests_test_exposed_services": "test_exposed_services.py" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _asset(), _by_port()]
- "tests_test_finding_events_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L26 | neighbors=[test_finding_events.py, .test_manual_remediation_sets_close_met…, .test_status_change_records_event(), .test_auto_resolution_event(), .test_detected_actor_falls_back_to_dete…, .test_detected_actor_labels_network_va_…]
- "tests_test_host_health": "test_host_health.py" | kind=code-symbol | source=probe/tests/test_host_health.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, scanner_base.py, _monitor(), _r(), TestConfiguration, TestHeartbeat]
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=probe/tests/test_http_lease.py:L1 | neighbors=[0e22dbf feat(probe): bounded auto-troub…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, engine.py]
- "tests_test_main_scripts_correlation": "test_main_scripts_correlation.py" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L1 | neighbors=[6c1f014 feat(correlation): implement co…, _get(), _ids(), _run(), test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts()]
- "tests_test_main_scripts_unauth": "test_main_scripts_unauth.py" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, unauth_access.py, _run(), test_couchdb_and_memcached_and_mongodb(), test_elasticsearch_unauth_vs_secured(), test_non_datastore_service_is_unknown()]
- "tests_test_nessus_scanner": "test_nessus_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _mock_response(), scanner(), test_authenticate_api_key(), test_create_scan(), test_create_scan_with_credentials()]
- "tests_test_new_scanners_testmobilescanner": "TestMobileScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L518 | neighbors=[test_new_scanners.py, .test_adb_checksum_empty(), .test_adb_checksum_known_value(), .test_adb_cnxn_checksum_matches(), .test_adb_cnxn_command_field(), .test_adb_cnxn_magic_invariant()]
- "tests_test_nuclei_background_fakesession": "_FakeSession" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L30 | neighbors=[test_nuclei_background.py, .add(), .__aenter__(), .__aexit__(), .begin_nested(), .commit()]
- "tests_test_os_fingerprint_testfingerprintos": "TestFingerprintOs" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L224 | neighbors=[test_os_fingerprint.py, .test_mss_flags_jumbo_even_without_os_s…, .test_mss_flags_tunnel_or_vpn(), .test_mss_is_path_intel_not_an_os_signa…, .test_mss_yields_ethernet_mtu(), .test_network_device_from_ttl_255()]
- "tests_test_perf_optimization": "test_perf_optimization.py" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, clean_guard_cache(), test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_bin…, test_guard_is_noop_without_dpkg(), test_guard_passes_when_pure_python_agre…]
- "tests_test_pipeline_ssh_inventory_jsonl": "_ssh_inventory_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L90 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_risk_rank": "test_risk_rank.py" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L1 | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, _rank(), test_bounds()]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()]
- "tests_test_smb_scanner": "test_smb_scanner.py" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 95904f1 feat(probe): detect SMB signing…, smb_scanner.py, _smb2_error_response(), _smb2_negotiate_response()]
- "tests_test_ssh_scanner_kexinit": "_kexinit()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L35 | neighbors=[test_ssh_scanner.py, _nl(), ._eval(), ._eval(), .test_main_scripts_scanner_and_findings…, ._eval()]
- "tests_test_validation": "test_validation.py" | kind=code-symbol | source=probe/tests/test_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, validation.py, FakeClient, _preflight_responses(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…]
- "tests_test_weakness_map_raw": "_raw()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L50 | neighbors=[test_weakness_map.py, A bare Finding dict (findings.py --json…, .test_cve_absent_from_mirror_still_emit…, .test_dedup_by_cve_target_port(), .test_exposure_boosts_risk(), .test_no_db_degrades_gracefully()]
- "workflow_host_health_hosthealthmonitor": "HostHealthMonitor" | kind=code-symbol | source=probe/workflow/host_health.py:L113 | neighbors=[host_health.py, .confirm(), .finalize(), .__init__(), .is_offline(), ._is_silence()]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L174 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L972 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=probe/agent/cli.py:L575 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L49 | neighbors=[transport.py, DeviceAlreadyEnrolledError, Raised when a transport operation fails…, .bootstrap(), .connect_ws(), .poll_jobs()]
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator]
- "auth_startup_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L49 | neighbors=[startup.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2b4ff7132c98967429d138e7459f25f879023fc7": "2b4ff71 feat(fleet): one-click Approve Site — optional name, no code/fields (it…" | kind=Commit | source=git | neighbors=[route.ts, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "commit:repo:github.com/Rutikm18/Project-Vedha@37fa611652538968dbf827eaf98cdcab59c052b2": "37fa611 harden(scanner): XML-entity guard + list-form argv (CWE-611/78/88)" | kind=Commit | source=git | neighbors=[2c53ae9 evasion(scanner): randomized sc…, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9c973dd02e4777bcd7cebae84b6c80fd96fa001f": "9c973dd feat(scanner): tarpit/honeypot detection in port-scan summary (C5)" | kind=Commit | source=git | neighbors=[2de251b feat(scanner): ICMP timestamp f…, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@aedddfae1bea375d5864f92e26f2ceb7f0bf8065": "aedddfa feat(settings): editable SLA policy windows wired to backend (item 4 UI)" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@dec1e7cfa829a295630af88da9f11a5f2e8175d4": "dec1e7c fix(scanner): resolve() family fallback for dual-stack hosts (task A9)" | kind=Commit | source=git | neighbors=[78d51c5 opsec(scanner): de-sign service…, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@eff17d69ed457a0f00a6cec466932ff1357fb74f": "eff17d6 feat(probe): one-click approve endpoint — no code, auto name/caps/scope…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f8ff2296e5ec2c593a6bed4ab40633d8a857d40f": "f8ff229 feat(ui): remove decorative session clock from both dashboards (item 6)" | kind=Commit | source=git | neighbors=[ecbb4ad feat(agent): rules-of-engagemen…, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fc7afc36732bf000de12e42189e63124bd643652": "fc7afc3 chore(graphify): refresh knowledge graph for remediation subsystem" | kind=Commit | source=git | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "cve_ingest": "ingest.py" | kind=code-symbol | source=probe/cve/ingest.py:L1 | neighbors=[6e2818f Add support for additional serv…, _cvss(), _get(), ingest_all(), ingest_epss(), ingest_kev()]
- "detection_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, attack_path_findings(), _bump(), _cleartext_cluster(), _exposed_db_unauth(), _group()]
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, AttackAction, _aware()]
- "detection_engine_posture_rules_detect_posture_traced": "detect_posture_traced()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L827 | neighbors=[posture_rules.py, detect_all_traced(), detect_posture(), _calibrate_host_findings(), compute_risk(), detect_exposed_services()]
- "detection_resolution": "resolution.py" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, 9a36729 feat(resolution): coverage buil…, bd409f5 feat(resolution): async applier…, cbf5d6c feat(resolution): pure decision…, d98f654 feat(manager): network-VA campa…, apply_manual_reopen()]
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload]

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
