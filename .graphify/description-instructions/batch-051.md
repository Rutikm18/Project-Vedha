# Node Description Batch 52 of 330

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

- "tests_test_tier1_correlations_run": "_run()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L13 | neighbors=[test_tier1_correlations.py, test_anon_data_exposure_cluster(), test_mgmt_plane_exposed_on_cipher_zero_…, test_mgmt_plane_needs_two_when_no_ciphe…, test_single_anon_finding_does_not_corre…, test_user_enum_plus_weak_auth()]
- "tests_test_tls_fingerprint": "test_tls_fingerprint.py" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello, test_tls_fingerprint.py — Tier 2.3: act…]
- "tests_test_tls_posture": "test_tls_posture.py" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, tls_scanner.py, _modern(), TestClassifyCipher, TestGradeTlsPosture, test_tls_posture.py — Tier 2.4: cipher-…]
- "tests_test_two_tree_parity": "test_two_tree_parity.py" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L1 | neighbors=[6e2818f Add support for additional serv…, _mirrored_py_files(), test_mirrored_set_is_nonempty(), test_no_unmirrored_scanner_files(), test_scanner_and_main_scripts_are_byte_…, test_two_tree_parity.py — the guard the…]
- "tests_test_validation_endpoints_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L50 | neighbors=[test_validation_endpoints.py, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_deri…, test_reject_marks_rejected()]
- "tests_test_validation_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_validation.py:L110 | neighbors=[test_validation.py, .__init__(), .request(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_gate": "test_validation_gate.py" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, _ids(), TestNoFabricatedIcmpLiveness, TestRdpNlaGate, TestUdpNoReplyRejected, test_validation_gate.py — the "validati…]
- "tests_test_validation_gate_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L27 | neighbors=[test_validation_gate.py, .test_icmp_unavailable_os_observation_r…, .test_nla_enforced_suppresses_no_nla_fi…, .test_positive_control_nla_off_is_flagg…, .test_open_filtered_amplifier_not_flagg…, .test_positive_control_answered_amplifi…]
- "tests_test_validation_ingest_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L23 | neighbors=[test_validation_ingest.py, test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…, test_inconclusive_leaves_finding_unchan…, test_ingest_confirmed_updates_request_a…]
- "tests_test_verification_core": "test_verification_core.py" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, test_authoritative_is_confirmed(), test_high_confidence_inferred_is_corrob…, test_kev_suspected_finding_needs_review…, test_low_confidence_inferred_is_inferre…, test_missing_confidence_defaults_to_inf…]
- "tests_test_version_compare": "test_version_compare.py" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, test_dpkg_compare_public_api(), test_pure_python_matches_known_pairs(), test_pure_python_matches_real_dpkg_bina…, Cross-validates the pure-Python Debian …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_wire_identity_testchoosesourceport": "TestChooseSourcePort" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L38 | neighbors=[test_wire_identity.py, Evasion: a fixed source port (e.g. 53/8…, .test_boundary_ports_are_valid(), .test_none_gives_random_ephemeral(), .test_out_of_range_falls_back_to_random…, .test_uses_configured_valid_port()]
- "tools_installer_managedpath": "managedPath()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L48 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), isManaged(), removeTool()]
- "users_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/users/route.ts:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, backend.ts, backend(), with-backend.ts, withBackend(), GET]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nuclei_nucleiscanner_parse_output": ".parse_output()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L381 | neighbors=[NucleiScanner, ._map_finding(), Parse nuclei JSONL output → list of Fin…, Parse nuclei JSONL output → list of Fin…, .run_scan(), Parse nuclei JSONL output → list of Fin…]
- "websocket_manager_agentconnectionmanager_agent_stale_after": ".agent_stale_after()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L338 | neighbors=[AgentConnectionManager, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…, Return agent_ids whose last heartbeat i…, Push a job to the first online agent in…]
- "websocket_manager_agentconnectionmanager_connected_agents": ".connected_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L302 | neighbors=[AgentConnectionManager, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…, Return a snapshot of all connected agen…]
- "websocket_manager_agentconnectionmanager_get_agent_status": ".get_agent_status()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L334 | neighbors=[AgentConnectionManager, Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Return 'online', 'busy', or 'offline'., Push a job to the first online agent in…]
- "websocket_manager_agentconnectionmanager_is_online": ".is_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L297 | neighbors=[AgentConnectionManager, Check if a specific agent is online (co…, Check if a specific agent is online (co…, Check if a specific agent is online (co…, Check if a specific agent is online (co…, Check if a specific agent is online (co…]
- "websocket_manager_agentconnectionmanager_online_agents": ".online_agents()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L307 | neighbors=[AgentConnectionManager, Return agent IDs whose status is 'onlin…, Return agent IDs whose status is 'onlin…, Deliver a job-push to an agent wherever…, Deliver a job-push to an agent wherever…, Return agent IDs whose status is 'onlin…]
- "websocket_manager_agentconnectionmanager_online_agents_for_tenant": ".online_agents_for_tenant()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L311 | neighbors=[AgentConnectionManager, .push_job_to_first_online(), Return idle connected agents belonging …, Return idle connected agents belonging …, Return idle connected agents belonging …, Return idle connected agents belonging …]
- "websocket_manager_agentconnectionmanager_unregister": ".unregister()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L126 | neighbors=[AgentConnectionManager, .push_job(), Remove the current registration, option…, Remove the current registration, option…, .push_job_to_first_online(), Remove an agent's WebSocket registratio…]
- "websocket_manager_connectionmanager_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L43 | neighbors=[ConnectionManager, .broadcast(), .send_personal(), .handle_client(), Remove connection from room., Remove connection from room.]
- "websocket_manager_connectionmanager_send_personal": ".send_personal()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L68 | neighbors=[ConnectionManager, .disconnect(), .handle_client(), ._handle_message(), Send message to a specific connection., Send message to a specific connection.]
- "workers_outbox_dead_letter_stale_stmt": "_dead_letter_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L251 | neighbors=[outbox.py, Stranded events that already exhausted …, _reclaim_stale(), Stranded events that already exhausted …, Stranded events that already exhausted …, Stranded events that already exhausted …]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L75 | neighbors=[outbox.py, _claim_batch(), main(), run_worker(), OutboxEvent, ScanResult]
- "workers_outbox_requeue_stale_stmt": "_requeue_stale_stmt()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L268 | neighbors=[outbox.py, Stranded events with retry budget left …, _reclaim_stale(), Stranded events with retry budget left …, Stranded events with retry budget left …, Stranded events with retry budget left …]
- "workers_outbox_stale_cutoff": "_stale_cutoff()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L246 | neighbors=[outbox.py, The `locked_at` boundary before which a…, _reclaim_stale(), The `locked_at` boundary before which a…, The `locked_at` boundary before which a…, The `locked_at` boundary before which a…]
- "workflow_asset_asset_merge_result": ".merge_result()" | kind=code-symbol | source=probe/workflow/asset.py:L102 | neighbors=[Asset, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…, Dispatch a real ScanResult into the rig…]
- "workflow_host_health_hosthealthmonitor_watch": ".watch()" | kind=code-symbol | source=probe/workflow/host_health.py:L255 | neighbors=[HostHealthMonitor, _heartbeat_interval(), _heartbeat_misses(), .is_offline(), ._mark_offline(), Heartbeat a host for as long as it is b…]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=probe/agent/agent.py:L66 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…, Recognize only explicit single-host dev…, Recognize only explicit single-host dev…]
- "agent_agent_manager_reachable": "_manager_reachable()" | kind=code-symbol | source=probe/agent/agent.py:L166 | neighbors=[agent.py, _classify_connection_error(), GET /health. Returns (ok, human-detail)…, _wait_for_manager(), GET /health. Returns (ok, human-detail)…]
- "agent_agent_result_summary": "_result_summary()" | kind=code-symbol | source=probe/agent/agent.py:L116 | neighbors=[agent.py, main(), One-line, transparent summary of what a…, _ws_run_job(), One-line, transparent summary of what a…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-051.json

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
