# Node Description Batch 32 of 186

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

- "tests_test_scope_crypt": "test_scope_crypt.py" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, scope_crypt.py, TestEncryptDecryptRoundtrip, TestKeyGeneration, Tests for agent/scope_crypt.py, 2885afa Add comprehensive probe testing…]
- "tests_test_scope_validator_testfetchengagementscope": "TestFetchEngagementScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L170 | neighbors=[test_scope_validator.py, .test_http_get_raises(), .test_http_get_returns_incomplete(), .test_http_get_returns_none(), .test_returns_excludes(), .test_returns_scope_from_http_get()]
- "tests_test_seed_admin_testvalidateenv": "TestValidateEnv" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L38 | neighbors=[test_seed_admin.py, .test_all_known_weak_passwords_blocked_…, .test_allows_weak_password_in_developme…, .test_raises_on_weak_password_in_produc…, .test_raises_when_email_missing(), .test_returns_force_reset_true()]
- "tests_test_service_match_testotherservices": "TestOtherServices" | kind=code-symbol | source=probe/tests/test_service_match.py:L58 | neighbors=[test_service_match.py, .test_mariadb_handshake(), .test_redis_info(), .test_redis_noauth(), .test_smtp_postfix(), .test_vsftpd()]
- "tests_test_tls_fingerprint": "test_tls_fingerprint.py" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello, test_tls_fingerprint.py — Tier 2.3: act…]
- "tests_test_tls_posture": "test_tls_posture.py" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, tls_scanner.py, _modern(), TestClassifyCipher, TestGradeTlsPosture, test_tls_posture.py — Tier 2.4: cipher-…]
- "tests_test_validation_endpoints_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L50 | neighbors=[test_validation_endpoints.py, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_deri…, test_reject_marks_rejected()]
- "tests_test_validation_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_validation.py:L110 | neighbors=[test_validation.py, .__init__(), .request(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_ingest_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L23 | neighbors=[test_validation_ingest.py, test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…, test_inconclusive_leaves_finding_unchan…, test_ingest_confirmed_updates_request_a…]
- "tests_test_verification_core": "test_verification_core.py" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, test_authoritative_is_confirmed(), test_high_confidence_inferred_is_corrob…, test_kev_suspected_finding_needs_review…, test_low_confidence_inferred_is_inferre…, test_missing_confidence_defaults_to_inf…]
- "tests_test_version_compare": "test_version_compare.py" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, test_dpkg_compare_public_api(), test_pure_python_matches_known_pairs(), test_pure_python_matches_real_dpkg_bina…, Cross-validates the pure-Python Debian …, 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_managedpath": "managedPath()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L48 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), isManaged(), removeTool()]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nuclei_nucleiscanner_parse_output": ".parse_output()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L381 | neighbors=[NucleiScanner, ._map_finding(), Parse nuclei JSONL output → list of Fin…, Parse nuclei JSONL output → list of Fin…, .run_scan(), Parse nuclei JSONL output → list of Fin…]
- "websocket_manager_agentconnectionmanager_push_job": ".push_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L177 | neighbors=[AgentConnectionManager, .unregister(), .push_job_to_first_online(), Push a job to a specific agent over Web…, Push a job to a specific agent over Web…, Push a job to a specific agent over Web…]
- "workers_outbox_claim_batch": "_claim_batch()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L130 | neighbors=[outbox.py, Event, Atomically claim up to `batch_size` due…, run_worker(), Atomically claim up to `batch_size` due…, Atomically claim up to `batch_size` due…]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L63 | neighbors=[outbox.py, _claim_batch(), main(), run_worker(), OutboxEvent, ScanResult]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L71 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_tls(), For every open port with a banner fact,…]
- "workflow_workflow_engine_gather_per_host": "_gather_per_host()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L72 | neighbors=[workflow_engine.py, _scan_one(), Run per-host probes with bounded fan-ou…, run_engagement(), Run per-host probes with bounded fan-ou…, Runs scanner.scan_target(host) across h…]
- "workflow_workflow_engine_port_candidates": "_port_candidates()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L110 | neighbors=[workflow_engine.py, Return TCP ports worth scanning for thi…, run_engagement(), Return TCP ports worth scanning for thi…, Return TCP ports worth scanning for thi…, Return TCP ports worth scanning for thi…]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_enroll_device": "_enroll_device()" | kind=code-symbol | source=probe/agent/agent.py:L905 | neighbors=[agent.py, say(), _obtain_identity(), Request UI approval, poll, prove key po…, Request UI approval, poll, prove key po…]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L274 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L59 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L33 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L46 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L478 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()]
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L153 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()]
- "agent_engine_derive_post_stage": "_derive_post_stage()" | kind=code-symbol | source=probe/agent/engine.py:L436 | neighbors=[engine.py, _results_by_target(), Return (extra ScanResults to append as …, run_scan(), Return (extra ScanResults to append as …]
- "agent_engine_hosts_from_facts": "_hosts_from_facts()" | kind=code-symbol | source=probe/agent/engine.py:L297 | neighbors=[engine.py, _build_run_stats(), Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L35 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license(), Stable per-machine ID, derived from hw_…]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L29 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L215 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists(), Number of pending (unsubmitted) results…, Number of pending (unsubmitted) results…]
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=probe/agent/result_spool.py:L59 | neighbors=[ResultSpool, .quarantine(), .remove(), .save(), .exists()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-031.json

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
