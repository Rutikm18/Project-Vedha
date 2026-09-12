# Node Description Batch 18 of 380

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

- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L69 | neighbors=[exploits.py, BaseModel, _result_out(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_integrations": "integrations.py" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 6be8259 feat(integrations): outbox deli…, f300b2a feat(integrations): ServiceNow …, dependencies.py, delete_integration(), integration_secret()]
- "routers_remediation": "remediation.py" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, dependencies.py]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[vuln_scans.py, Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_ipv6_discovery": "ipv6_discovery.py" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, discover_ipv6_hosts(), _is_ipv6(), main()]
- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L353 | neighbors=[os_fingerprint.py, BaseScanner, ._apply_smb_build(), ._icmp_echo_ttl(), ._icmp_scan_target(), ._icmp_timestamp()]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L697 | neighbors=[PortScanner, ._is_ambiguous(), ._reprobe_ambiguous(), ._silence_result(), ScanMetrics, .record()]
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1155 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L315 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "scanner_ssh_scanner": "ssh_scanner.py" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _Cursor, _dedup(), evaluate_algorithms(), main()]
- "states_datastate_skeletonrows": "SkeletonRows()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L26 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, .__init__(), .__getitem__(), ADCSChecker, CertTemplate, ASREPRoastChecker]
- "tests_test_agent_policy_roe": "_roe()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L30 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…]
- "tests_test_agent_policy_testevaluateaction": "TestEvaluateAction" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L36 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…]
- "tests_test_agents_testagentjobcompatibility": "TestAgentJobCompatibility" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L413 | neighbors=[test_agents.py, .test_agent_network_segments_are_normal…, .test_declared_segment_must_cover_entir…, .test_declared_segment_rejects_missing_…, .test_empty_capabilities_receive_no_job…, .test_empty_segments_are_fail_closed()]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, .setup_method(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_fallback_score_capped(), .test_higher_cvss_scores_higher()]
- "tests_test_customer_access": "test_customer_access.py" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, _added(), _mock_db(), _operator()]
- "tests_test_default_cred_rule_rule": "_rule()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L56 | neighbors=[test_default_cred_rule.py, .test_evidence_explains_what_was_not_te…, .test_known_vendor_with_basic_auth(), .test_known_vendor_with_login_form(), .test_vendor_falls_back_to_the_fact_whe…, .test_declares_its_required_input()]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, .skip_without_flag(), .test_connect_and_list_modules(), .test_run_safe_scanner_smb(), MetasploitRPCClient]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-017.json

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
