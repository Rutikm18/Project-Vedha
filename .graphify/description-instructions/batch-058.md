# Node Description Batch 59 of 380

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
- "workflow_intensity_resolve_intensity": "resolve_intensity()" | kind=code-symbol | source=probe/workflow/intensity.py:L87 | neighbors=[intensity.py, intensity_first_pass(), intensity_port_override(), Return a COPY of the preset for `name` …, Return a COPY of the preset for `name` …, Return a COPY of the preset for `name` …]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_workflow_engine_timed": "_timed()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L287 | neighbors=[workflow_engine.py, Accumulate wall time for a stage. No-op…, _run_branch(), run_engagement(), Accumulate wall time for a stage. No-op…, Hosts scanned in parallel during the de…]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_bootstrap": "bootstrap.py" | kind=code-symbol | source=probe/agent/bootstrap.py:L1 | neighbors=[python_install_cmd(), security_mode(), verify_download(), bootstrap.py — Layer-1 (Python runtime)…, ac8d1ee Phase 7: dependency bootstrap +…]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L276 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L61 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L35 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L48 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L480 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()]
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L155 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-058.json

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
