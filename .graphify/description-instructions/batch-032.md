# Node Description Batch 33 of 119

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

- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L272 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L286 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L225 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L397 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=probe/tests/test_probe_core.py:L205 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L216 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L364 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L247 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=probe/tests/test_transport.py:L171 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…, 298a9d4 trim frontend to 7 core pages; …]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_enrichment_vulnenrichmentservice_check_cisa_kev": ".check_cisa_kev()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L244 | neighbors=[True if CVE is in the CISA Known Exploi…, VulnEnrichmentService, ._get_kev_catalog(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_compute_composite_risk": ".compute_composite_risk()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L297 | neighbors=[Returns composite risk score on 0-1000 …, VulnEnrichmentService, .get(), .enrich()]
- "vuln_enrichment_vulnenrichmentservice_fetch_epss": ".fetch_epss()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L215 | neighbors=[Returns {epss_score: float, percentile:…, VulnEnrichmentService, ._fetch_all(), .get()]
- "vuln_nessus_nessusscanner_create_scan": ".create_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L95 | neighbors=[NessusScanner, ._get_client(), ._get_template_uuid(), Returns nessus scan_id as string.]
- "vuln_nessus_nessusscanner_get_results": ".get_results()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L167 | neighbors=[NessusScanner, ._get_client(), ._get_plugin_detail(), Returns list of raw finding dicts from …]
- "vuln_nuclei_nucleiscanner_partial_or_raise": "._partial_or_raise()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L338 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, .run_scan()]
- "vuln_nuclei_rationale_1": "NucleiScanner — async subprocess wrapper around the Nuclei CLI.  Nuclei outputs" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, nuclei.py]
- "vuln_nuclei_rationale_110": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L110 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_127": "Run Nuclei and stream JSONL findings from stdout.          ``request_timeout_sec" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L127 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_132": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L132 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_195": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L195 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_383": "Parse nuclei JSONL output → list of Finding-compatible dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L383 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .parse_output()]
- "vuln_nuclei_rationale_446": "Given a list of service names on an asset, return the union         of relevant" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L446 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .template_selector()]
- "vuln_nuclei_rationale_68": "Run Nuclei against targets and parse JSONL output into Finding dicts." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L68 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanner]
- "vuln_nuclei_rationale_80": "Machine-readable state for the most recent scanner invocation." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L80 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiRunReport]
- "vuln_nuclei_rationale_81": "Runs nuclei as an async subprocess.         Returns a list of parsed finding dic" | kind=entity | source=manager/backend/app/vuln/nuclei.py:L81 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, .run_scan()]
- "vuln_nuclei_rationale_91": "Fatal Nuclei failure, optionally carrying findings emitted before failure." | kind=entity | source=manager/backend/app/vuln/nuclei.py:L91 | neighbors=[ServiceFingerprint, FindingSeverity, FindingStatus, NucleiScanError]
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L340 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…, Broadcast graph data update to all subs…]
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L359 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…]
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L349 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update., Broadcast a single node update.]
- "workers_outbox_claim_batch": "_claim_batch()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L109 | neighbors=[outbox.py, Event, Atomically claim up to `batch_size` due…, run_worker()]
- "workers_outbox_process": "_process()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L173 | neighbors=[outbox.py, _mark_done(), _mark_retry_or_dead(), run_worker()]
- "workflow_asset_parse_ts": "_parse_ts()" | kind=code-symbol | source=probe/workflow/asset.py:L32 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]
- "workflow_asset_portfact": "PortFact" | kind=code-symbol | source=probe/workflow/asset.py:L37 | neighbors=[asset.py, ._merge_host_discovery(), ._merge_port_scan(), ._merge_udp_scan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-032.json

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
