# Node Description Batch 30 of 332

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

- "tests_test_os_fingerprint_testttlinference": "TestTtlInference" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L192 | neighbors=[test_os_fingerprint.py, .test_hop_estimate(), .test_os_family_linux(), .test_os_family_network(), .test_os_family_unknown_on_none(), .test_os_family_windows()]
- "tests_test_os_stage_wiring_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L28 | neighbors=[test_os_stage_wiring.py, .test_closed_port_contributes_no_hints(), .test_connect_scan_without_stack_signal…, .test_os_fact_stored_and_ntlm_name_beco…, .test_syn_stack_hints_harvested_from_op…, .test_alive_host_is_eligible()]
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()]
- "tests_test_portal_assistant_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L39 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…, test_only_the_whitelisted_finding_field…]
- "tests_test_portal_assistant_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L55 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…, test_only_the_whitelisted_finding_field…]
- "tests_test_reference": "test_reference.py" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _at(), test_the_migration_backfill_agrees_with…, TestShape, TestStability, TestStamping]
- "tests_test_rsync_scanner_fakesock": "_FakeSock" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L34 | neighbors=[test_rsync_scanner.py, .__init__(), .recv(), .sendall(), Minimal socket stand-in: replays the da…, .test_echo_stops_at_the_first_line()]
- "tests_test_scanner_congestion_fakesock": "_FakeSock" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L210 | neighbors=[test_scanner_congestion.py, .getsockopt(), .__init__(), .test_absurd_values_are_rejected(), .test_maxseg_is_reported_but_never_as_a…, .test_never_synthesizes_an_initial_tcp_…]
- "tests_test_scanner_congestion_testharvesttcpstack": "TestHarvestTcpStack" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L224 | neighbors=[test_scanner_congestion.py, .test_absurd_values_are_rejected(), .test_maxseg_is_reported_but_never_as_a…, .test_never_synthesizes_an_initial_tcp_…, .test_none_socket_yields_nothing(), .test_object_without_getsockopt_is_surv…]
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()]
- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L93 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_fully_excluded_cidr_is_dropped(), .test_hostname_passes_through()]
- "tests_test_service_match": "test_service_match.py" | kind=code-symbol | source=probe/tests/test_service_match.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, service_banner.py, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder]
- "tests_test_service_posture_rules_corpus": "_corpus()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L41 | neighbors=[test_service_posture_rules.py, The captured fact for one scanner, stra…, test_experimental_scanner_findings_are_…, test_rule_fires_on_captured_shape(), test_smb_null_session_is_silent_on_the_…, test_ssh_rules_against_live_capture()]
- "tests_test_ssh_scanner_testevaluate": "TestEvaluate" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L94 | neighbors=[test_ssh_scanner.py, ._eval(), .test_arcfour_is_rc4_failure(), .test_cbc_cipher_is_warning_not_failure…, .test_group1_sha1_is_failure_with_modul…, .test_hmac_md5_is_failure()]
- "tests_test_tls_legacy_versions": "test_tls_legacy_versions.py" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _LegacyTLSServer, _self_signed(), _server_supports(), test_legacy_version_is_detected_not_mas…, test_try_version_reports_client_side_re…]
- "tests_test_tls_posture_testclassifycipher": "TestClassifyCipher" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L18 | neighbors=[test_tls_posture.py, .test_3des_is_weak(), .test_anonymous_is_weak(), .test_chacha20_is_aead(), .test_export_and_md5_are_weak(), .test_modern_aead_pfs()]
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds()]
- "tests_test_va_campaign_run": "_run()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L30 | neighbors=[test_va_campaign.py, _scope(), test_detect_stage_skipped_when_nothing_…, test_disabled_opt_in_stage_is_skipped_a…, test_enabled_opt_in_stage_runs(), test_facts_accumulate_into_totals()]
- "vuln_prioritizer_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetInput, FindingInput, vulnPrioritizer, DEMO_ASSETS, DEMO_FINDINGS]
- "websocket_manager_agentconnectionmanager_push_job": ".push_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L179 | neighbors=[AgentConnectionManager, .deliver_job(), .unregister(), .push_job_to_first_online(), .run_backplane(), Push a job to a specific agent over Web…]
- "websocket_manager_graphwebsocketmanager_handle_message": "._handle_message()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L382 | neighbors=[GraphWebSocketManager, .handle_client(), .broadcast(), .send_personal(), Handle incoming WebSocket messages., Handle incoming WebSocket messages.]
- "workers_outbox_claim_batch": "_claim_batch()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L213 | neighbors=[outbox.py, Event, Atomically claim up to `batch_size` due…, run_worker(), Atomically claim up to `batch_size` due…, Atomically claim up to `batch_size` due…]
- "workers_reaper": "reaper.py" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, config.py, database.py, expire_attempt(), reap_once()]
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L128 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_ssh(), looks_like_tls()]
- "workflow_workflow_engine_gather_per_host": "_gather_per_host()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L106 | neighbors=[workflow_engine.py, _scan_one(), Run per-host probes with bounded fan-ou…, run_engagement(), Run per-host probes with bounded fan-ou…, Run per-host probes with bounded fan-ou…]
- "workflow_workflow_engine_port_candidates": "_port_candidates()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L144 | neighbors=[workflow_engine.py, Return TCP ports worth scanning for thi…, run_engagement(), Return TCP ports worth scanning for thi…, Run per-host probes with bounded fan-ou…, Return TCP ports worth scanning for thi…]
- "workflow_workflow_engine_scan_one": "_scan_one()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L93 | neighbors=[workflow_engine.py, _gather_per_host(), Run one component without allowing a ta…, _run_branch(), run_engagement(), Run one component without allowing a ta…]
- "workflow_workflow_engine_split_cached": "_split_cached()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L126 | neighbors=[workflow_engine.py, Splits candidate_ports into (ports that…, _run_branch(), run_engagement(), Splits candidate_ports into (ports that…, Splits candidate_ports into (ports that…]
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…]
- "agent_agent_classify_connection_error": "_classify_connection_error()" | kind=code-symbol | source=probe/agent/agent.py:L141 | neighbors=[agent.py, _enroll_device(), main(), _manager_reachable(), _obtain_identity(), Map a low-level connection exception to…]
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L75 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…]
- "agent_agent_load_or_create_signing_identity": "_load_or_create_signing_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1128 | neighbors=[agent.py, _obtain_identity(), Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…]
- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=probe/agent/agent.py:L193 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()]
- "agent_device_identity": "device_identity.py" | kind=code-symbol | source=probe/agent/device_identity.py:L1 | neighbors=[decode_key(), encode_key(), generate_signing_identity(), sign_b64(), signing_public_from_private(), verify_site_policy()]
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=probe/agent/engine.py:L372 | neighbors=[engine.py, _scan_method_for(), _build_run_stats(), Serialize effective limits without ever…, Serialize effective limits without ever…, Serialize effective limits without ever…]
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L215 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan(), Return the effective whole-job deadline…, Return the effective whole-job deadline…]
- "agent_engine_leaselosterror": "LeaseLostError" | kind=code-symbol | source=probe/agent/engine.py:L535 | neighbors=[engine.py, RuntimeError, Raised when Manager fencing revokes the…, _run_with_cancellation(), Raised when Manager fencing revokes the…, Raised when Manager fencing revokes the…]
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-029.json

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
