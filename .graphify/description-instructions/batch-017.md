# Node Description Batch 18 of 119

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

- "scanner_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L236 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()] | lang=en
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()] | lang=en
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L490 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()] | lang=en
- "scanner_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe-go/scanner/scope.go:L12 | neighbors=[scope.go, .ExpandRequested(), .InScope(), .isAllowed(), .isExcluded(), .networkAllowed()] | lang=en
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py] | lang=en
- "scanner_types": "types.go" | kind=code-symbol | source=probe-go/scanner/types.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, HostResult, PortResult, Result, newResult(), ptr()] | lang=en
- "scanner_udp_probeudpport": "probeUDPPort()" | kind=code-symbol | source=probe-go/scanner/udp.go:L34 | neighbors=[udp.go, ProbeUDP(), dnsVersionQuery(), extractSNMPCommunity(), netbiosNameQuery(), ntpRequest()] | lang=en
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…, auth.py, BaseModel, Parsed from JWT claims — attached to re…] | lang=en
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L45 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity, .normalize_name(), .validate_dates()] | lang=en
- "siem_config_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, SIEMConfig, GET(), POST(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L36 | neighbors=[page.tsx, Exposure.tsx, SlaStatus.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "tests_test_agent_dispatch": "test_agent_dispatch.py" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L1 | neighbors=[b4b12a9 Rename project and update files, _claim_fixture(), TestAgentWebSocketAuthentication, TestAtomicWebSocketClaim, TestJobSecretBoundary, TestTenantWebSocketSelection] | lang=en
- "tests_test_agent_dispatch_testatomicwebsocketclaim": "TestAtomicWebSocketClaim" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L202 | neighbors=[test_agent_dispatch.py, ScanJobStatus, ScanJobType, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…] | lang=en
- "tests_test_agent_dispatch_testtenantwebsocketselection": "TestTenantWebSocketSelection" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L90 | neighbors=[test_agent_dispatch.py, ScanJobStatus, ScanJobType, .test_displaced_socket_cannot_unregiste…, .test_first_online_push_cannot_cross_te…, .test_only_returns_online_agents_in_req…] | lang=en
- "tests_test_agents_testenqueueagentjob": "TestEnqueueAgentJob" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L43 | neighbors=[test_agents.py, ScanJobType, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…] | lang=en
- "tests_test_ai_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L24 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_unavailable_without_client(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher()] | lang=en
- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient, GraphVisualizer] | lang=en
- "tests_test_engagement_lists": "test_engagement_lists.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user(), Unit tests for the dashboard list endpo…] | lang=en
- "tests_test_nuclei_background": "test_nuclei_background.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L1 | neighbors=[b4b12a9 Rename project and update files, _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_backgroun…] | lang=en
- "tests_test_nuclei_background_nestedtransaction": "_NestedTransaction" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L22 | neighbors=[test_nuclei_background.py, .begin_nested(), ScanJobStatus, .__aenter__(), .__aexit__(), NucleiRunReport] | lang=en
- "tests_test_nuclei_background_scalarresult": "_ScalarResult" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L14 | neighbors=[test_nuclei_background.py, .execute(), ScanJobStatus, .__init__(), .scalar_one_or_none(), NucleiRunReport] | lang=en
- "tests_test_probe_core_testclassifycertainty": "TestClassifyCertainty" | kind=code-symbol | source=probe/tests/test_probe_core.py:L684 | neighbors=[test_probe_core.py, .test_error_overrides(), .test_host_discovery_uncertain(), .test_service_banner_deterministic(), .test_tcp_port_scan_deterministic(), .test_udp_port_scan_uncertain()] | lang=en
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=probe/tests/test_result_spool.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, result_spool.py, spool(), TestResultSpool, Tests for agent/result_spool.py] | lang=en
- "tests_test_scope_validator_testmergeexclusions": "TestMergeExclusions" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L144 | neighbors=[test_scope_validator.py, .test_both_empty(), .test_empty_engagement_excludes(), .test_empty_job_excludes(), .test_merges_no_duplicates(), .test_none_job_excludes()] | lang=en
- "tests_test_udp_amplifiers": "test_udp_amplifiers.py" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L1 | neighbors=[fe868e6 feat(probe): real UDP amplifica…, udp_scanner.py, test_dns_open_recursion(), test_memcached_exposed(), test_ntp_monlist_absent(), test_ntp_monlist_enabled()] | lang=en
- "use_cases_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts] | lang=en
- "vuln_enrichment": "enrichment.py" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, TTLCache, VulnEnrichmentService, VulnEnrichmentService  External data so…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_enrichment_ttlcache_get": ".get()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L56 | neighbors=[TTLCache, .compute_composite_risk(), .enrich(), .fetch_epss(), .fetch_mitre_techniques(), .fetch_nvd()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_all": "._fetch_all()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L341 | neighbors=[Fetch NVD, EPSS, KEV and MITRE concurre…, VulnEnrichmentService, .enrich(), .check_cisa_kev(), .fetch_epss(), .fetch_mitre_techniques()] | lang=en
- "vuln_nessus_nessusscanner_get_client": "._get_client()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L50 | neighbors=[NessusScanner, .create_scan(), .export_nessus_file(), ._auth_headers(), .get_results(), .launch_scan()] | lang=en
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner, NucleiScanner — async subprocess wrappe…] | lang=en
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment(), Background tasks triggered after a vuln…] | lang=en
- "vuln_tasks_rationale_1": "Background tasks triggered after a vuln scan completes.  Pipeline:   1. Load all" | kind=entity | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=pt
- "vuln_tasks_rationale_171": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L171 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "vuln_tasks_rationale_38": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L38 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L49 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()] | lang=en
- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L297 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…] | lang=en
- "workers_reaper": "reaper.py" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, config.py, database.py, reap_once(), run_reaper(), reaper.py — requeue jobs abandoned by a…] | lang=en
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L214 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…] | lang=en
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=probe/agent/agent.py:L661 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet(), Detect common debugging/tracing tools. …, Detect common debugging/tracing tools. …] | lang=en

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
