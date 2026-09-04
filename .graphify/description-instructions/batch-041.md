# Node Description Batch 42 of 330

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

- "tests_test_tls_integration_tlsserver": "_TLSServer" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L50 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade(), .__enter__(), .__exit__(), .__init__()] | lang=en
- "tests_test_transport_testdeviceenrollment": "TestDeviceEnrollment" | kind=code-symbol | source=probe/tests/test_transport.py:L171 | neighbors=[test_transport.py, .test_activation_persists_recoverable_d…, .test_create_enrollment_request_409_rai…, .test_create_enrollment_request_409_wit…, .test_create_enrollment_request_forward…, .test_device_refresh_signs_unique_nonce…] | lang=en
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
- "workflow_intensity": "intensity.py" | kind=code-symbol | source=probe/workflow/intensity.py:L1 | neighbors=[engine.py, 22701ea Add tests for scanner parity an…, test_probe_next_features.py, port_scanner.py, intensity_port_override(), resolve_intensity()] | lang=en
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L310 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…, Parse the nTSecurityDescriptor of an ob…] | lang=en
- "agent_agent_dbg": "_dbg()" | kind=code-symbol | source=probe/agent/agent.py:L97 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), _wait_for_manager(), _ws_run_job()] | lang=en
- "agent_agent_poll_jobs_or_empty": "_poll_jobs_or_empty()" | kind=code-symbol | source=probe/agent/agent.py:L266 | neighbors=[agent.py, main(), Poll for work. Auth failures (Transport…, Poll for work. Auth failures (Transport…, say(), Return no work for transient poll failu…] | lang=en
- "agent_agent_ws_flush_spool": "_ws_flush_spool()" | kind=code-symbol | source=probe/agent/agent.py:L489 | neighbors=[agent.py, Re-submit previously spooled results ov…, _run_ws_push_loop(), say(), _ws_http_poll_fallback(), Re-submit previously spooled results ov…] | lang=en
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/cli.py:L313 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()] | lang=en
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=probe/agent/cli.py:L446 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()] | lang=en
- "agent_engine_scan_method_for": "_scan_method_for()" | kind=code-symbol | source=probe/agent/engine.py:L162 | neighbors=[engine.py, _applied_tuning(), syn' for wide sweeps (deep intensity / …, run_scan(), syn' for wide sweeps (deep intensity / …, syn' for wide sweeps (deep intensity / …] | lang=en
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L99 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…, Load a previously spooled result, retur…] | lang=en
- "agent_result_spool_resultspool_quarantine": ".quarantine()" | kind=code-symbol | source=probe/agent/result_spool.py:L115 | neighbors=[Move a terminally rejected result out o…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()] | lang=en
- "agent_transport_transport_refresh_device_access": ".refresh_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L456 | neighbors=[Backwards-compatible bool wrapper over …, Transport, .ensure_device_access(), .refresh_device_access_ex(), .load_state(), .update_state()] | lang=en
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=probe/agent/use_cases.py:L254 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code(), Coerce an int-or-numeric-string to int,…, Coerce an int-or-numeric-string to int,…] | lang=en
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=probe/agent/use_cases.py:L276 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…] | lang=en
- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=probe/agent/use_cases.py:L265 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int(), Map a numeric use-case code → use_case_…, Map a numeric use-case code → use_case_…] | lang=en
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L249 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()] | lang=en

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
