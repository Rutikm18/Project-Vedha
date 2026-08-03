# Node Description Batch 24 of 131

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

- "tests_test_agent_dispatch_testagentwebsocketauthentication": "TestAgentWebSocketAuthentication" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L16 | neighbors=[test_agent_dispatch.py, .test_accepts_bearer_header(), .test_rejects_query_string_credentials(), ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_dispatch_testjobsecretboundary": "TestJobSecretBoundary" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L62 | neighbors=[test_agent_dispatch.py, .test_allows_non_secret_scan_tuning(), .test_detects_persisted_secret_material…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agents_testgetagentjobs": "TestGetAgentJobs" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L290 | neighbors=[test_agents.py, .test_404_when_agent_unknown(), .test_jobs_include_params(), .test_skips_job_outside_declared_networ…, .test_skips_job_when_capability_is_miss…, ScanJobType]
- "tests_test_agents_testotprofilegate": "TestOTProfileGate" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L162 | neighbors=[test_agents.py, .test_allows_passive_discovery_on_ot_en…, .test_blocks_active_scan_type_on_ot_eng…, .test_blocks_explicit_active_scan_type_…, .test_it_and_iot_profiles_unaffected(), ScanJobType]
- "tests_test_ai_engine_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L36 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher(), .test_predict_priority_uses_fallback_wh…]
- "tests_test_ai_engine_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L170 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_ai_engine_rationale_1": "Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API" | kind=entity | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_exploit_engine_testmetasploitrpcclient_make_client": "._make_client()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L183 | neighbors=[TestMetasploitRPCClient, .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit(), .test_run_module_error_raises(), .test_run_module_returns_job_id()]
- "tests_test_hw_bind": "test_hw_bind.py" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, hw_bind.py, TestCheckHwBind, TestGetHwId, Tests for agent/hw_bind.py, 2885afa Add comprehensive probe testing…]
- "tests_test_integration_testscopevalidationpipeline": "TestScopeValidationPipeline" | kind=code-symbol | source=probe/tests/test_integration.py:L165 | neighbors=[test_integration.py, Phase 1: combined scope validation (val…, .test_accepts_in_scope_rejects_out_of_s…, .test_all_excluded_returns_empty(), .test_excludes_override_scope(), .test_merge_exclusions_deduplicates()]
- "tests_test_integration_testwebsocketmessageprotocol": "TestWebSocketMessageProtocol" | kind=code-symbol | source=probe/tests/test_integration.py:L273 | neighbors=[test_integration.py, Phase 2: WebSocket message parsing., .test_heartbeat_message(), .test_hello_message(), .test_job_push_message(), .test_result_message()]
- "tests_test_nessus_scanner_mock_response": "_mock_response()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L25 | neighbors=[test_nessus_scanner.py, test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()]
- "tests_test_passive_collector_writer": "_Writer" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L15 | neighbors=[test_passive_collector.py, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…, test_subset_listener_failure_reports_de…, .__init__(), .write()]
- "tests_test_probe_core_testclamp": "TestClamp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L830 | neighbors=[test_probe_core.py, .test_bad_value_uses_default(), .test_clamped_high(), .test_clamped_low(), .test_in_range(), .test_none_uses_default()]
- "tests_test_probe_core_testengagementmodes": "TestEngagementModes" | kind=code-symbol | source=probe/tests/test_probe_core.py:L444 | neighbors=[test_probe_core.py, .test_assessment(), .test_re_scan(), .test_service_specific_invalid_raises(), .test_service_specific_valid(), .test_triage()]
- "tests_test_scope_crypt": "test_scope_crypt.py" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, scope_crypt.py, TestEncryptDecryptRoundtrip, TestKeyGeneration, Tests for agent/scope_crypt.py, 2885afa Add comprehensive probe testing…]
- "tests_test_scope_validator_testfetchengagementscope": "TestFetchEngagementScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L170 | neighbors=[test_scope_validator.py, .test_http_get_raises(), .test_http_get_returns_incomplete(), .test_http_get_returns_none(), .test_returns_excludes(), .test_returns_scope_from_http_get()]
- "tests_test_seed_admin_testvalidateenv": "TestValidateEnv" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L38 | neighbors=[test_seed_admin.py, .test_all_known_weak_passwords_blocked_…, .test_allows_weak_password_in_developme…, .test_raises_on_weak_password_in_produc…, .test_raises_when_email_missing(), .test_returns_force_reset_true()]
- "tests_test_smb_scanner": "test_smb_scanner.py" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L1 | neighbors=[95904f1 feat(probe): detect SMB signing…, smb_scanner.py, _smb2_negotiate_response(), test_garbage_response(), test_signing_not_required(), test_signing_required_smb311()]
- "tests_test_validation_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_validation.py:L110 | neighbors=[test_validation.py, .__init__(), .request(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_version_compare": "test_version_compare.py" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, test_dpkg_compare_public_api(), test_pure_python_matches_known_pairs(), test_pure_python_matches_real_dpkg_bina…, Cross-validates the pure-Python Debian …, 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_managedpath": "managedPath()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L48 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), isManaged(), removeTool()]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nuclei_nucleiscanner_parse_output": ".parse_output()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L381 | neighbors=[NucleiScanner, ._map_finding(), Parse nuclei JSONL output → list of Fin…, Parse nuclei JSONL output → list of Fin…, .run_scan(), Parse nuclei JSONL output → list of Fin…]
- "websocket_manager_agentconnectionmanager_push_job": ".push_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L177 | neighbors=[AgentConnectionManager, .unregister(), .push_job_to_first_online(), Push a job to a specific agent over Web…, Push a job to a specific agent over Web…, Push a job to a specific agent over Web…]
- "workers_outbox_claim_batch": "_claim_batch()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L130 | neighbors=[outbox.py, Event, Atomically claim up to `batch_size` due…, run_worker(), Atomically claim up to `batch_size` due…, Atomically claim up to `batch_size` due…]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L63 | neighbors=[outbox.py, _claim_batch(), main(), run_worker(), OutboxEvent, ScanResult]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L71 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_tls(), For every open port with a banner fact,…]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L556 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop(), Acknowledge an offer without executing …, Acknowledge an offer without executing …]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L274 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L59 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L33 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L46 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
