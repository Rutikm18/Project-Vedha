# Node Description Batch 49 of 236

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

- "tests_test_router_db": "test_router_db.py" | kind=code-symbol | source=probe/tests/test_router_db.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, test_mysql_greeting_on_odd_port(), test_plain_http_is_not_db(), test_redis_noauth_signature(), router.py]
- "tests_test_runtime_topology": "test_runtime_topology.py" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, main.py, test_manager_does_not_mount_a_static_da…, test_manager_root_is_service_metadata(), Product-boundary tests for the single-d…]
- "tests_test_scan_funnel_testrouteports": "TestRoutePorts" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L98 | neighbors=[test_scan_funnel.py, .test_intersection_only(), .test_no_match_returns_empty(), .test_port_in_multiple_routes(), .test_sorted_output()]
- "tests_test_service_match_testhttpmatch": "TestHttpMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L35 | neighbors=[test_service_match.py, .test_apache_version(), .test_iis_version(), .test_nginx_version(), .test_nginx_without_version()]
- "tests_test_sla_policy_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L36 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent(), .test_resolve_windows_fallback_and_cust…]
- "tests_test_sla_policy_testslapolicyroutes": "TestSlaPolicyRoutes" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L52 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent(), .test_resolve_windows_fallback_and_cust…]
- "tests_test_syn_scanner_testbuildresultsenrichment_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L349 | neighbors=[TestBuildResultsEnrichment, .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_windows_ttl_maps_to_windows()]
- "tests_test_syn_scanner_testpacketroundtrip": "TestPacketRoundTrip" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L68 | neighbors=[test_syn_scanner.py, .test_ip_checksum_valid_in_full_packet(), .test_parse_rejects_short_packet(), .test_syn_flag_is_set(), .test_syn_packet_parses_back_to_fields()]
- "tests_test_syn_scanner_testsyncookie": "TestSynCookie" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L47 | neighbors=[test_syn_scanner.py, .test_cookie_is_32_bit(), .test_cookie_is_deterministic(), .test_cookie_varies_with_key(), .test_cookie_varies_with_port()]
- "tests_test_syn_scanner_testverifyreplycookie": "TestVerifyReplyCookie" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L109 | neighbors=[test_syn_scanner.py, ._make_synack_reply(), .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_tarpit_testportscannertarpitflag": "TestPortScannerTarpitFlag" | kind=code-symbol | source=probe/tests/test_tarpit.py:L42 | neighbors=[test_tarpit.py, ._scanner(), ._summary(), .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tls_fingerprint_testclienthello": "TestClientHello" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L22 | neighbors=[test_tls_fingerprint.py, .test_contains_client_hello_handshake_t…, .test_contains_sni_hostname(), .test_declared_lengths_are_consistent(), .test_is_tls_handshake_record()]
- "tests_test_tls_fingerprint_testparseserverhello": "TestParseServerHello" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L58 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_returns_none_on_alert(), .test_returns_none_on_short(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_posture_modern": "_modern()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L68 | neighbors=[test_tls_posture.py, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_tls11(), .test_grade_f_tls10()]
- "tests_test_transport_testwebsocket": "TestWebSocket" | kind=code-symbol | source=probe/tests/test_transport.py:L530 | neighbors=[test_transport.py, .test_is_ws_connected_false_by_default(), .test_ws_requires_token(), .test_ws_url_http(), .test_ws_url_https()]
- "tests_test_web_methods": "test_web_methods.py" | kind=code-symbol | source=probe/tests/test_web_methods.py:L1 | neighbors=[bce780a feat(probe): enumerate HTTP met…, web_scanner.py, test_dangerous_methods_flagged(), test_no_allow_header(), test_safe_methods_only()]
- "tests_test_wire_identity_testjittereddelay": "TestJitteredDelay" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L57 | neighbors=[test_wire_identity.py, Evasion: blur a fixed scan cadence with…, .test_never_negative_even_at_full_jitte…, .test_stays_within_jitter_band(), .test_zero_or_negative_base_is_zero()]
- "tools_installer_getinstalledrecord": "getInstalledRecord()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L63 | neighbors=[installer.ts, readInstalled(), installAll(), installTool(), tools.ts]
- "tools_installer_ismanaged": "isManaged()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L56 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), managedPath()]
- "tools_installer_readinstalled": "readInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L33 | neighbors=[installer.ts, getInstalledRecord(), installTool(), listStatus(), removeTool()]
- "tools_installer_removetool": "removeTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L243 | neighbors=[tools.ts, installer.ts, managedPath(), readInstalled(), writeInstalled()]
- "ui_output_rule": "rule()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L50 | neighbors=[output.ts, findingDetail(), ln(), scanHeader(), summary()]
- "versions_0002_services_agents": "0002_services_agents.py" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add services and agents tables  Revisio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0003_vuln_scan_fields": "0003_vuln_scan_fields.py" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add enrichment fields index + webhook c…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0004_exploit_tables": "0004_exploit_tables.py" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Exploit results, approvals, and audit l…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0005_detection_validation": "0005_detection_validation.py" | kind=code-symbol | source=manager/backend/alembic/versions/0005_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Detection validation: attack_timeline, …, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0006_llm_outputs": "0006_llm_outputs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0006_llm_outputs.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), AI engine: llm_outputs table + reviewst…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0007_scale_indexes": "0007_scale_indexes.py" | kind=code-symbol | source=manager/backend/alembic/versions/0007_scale_indexes.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3: composite indexes for the hot aggre…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0008_scan_results": "0008_scan_results.py" | kind=code-symbol | source=manager/backend/alembic/versions/0008_scan_results.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), P3-#10: append-only scan_results table …, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0009_outbox_events": "0009_outbox_events.py" | kind=code-symbol | source=manager/backend/alembic/versions/0009_outbox_events.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Transactional outbox for durable backgr…, 2885afa Add comprehensive probe testing…]
- "versions_0010_detection_runs": "0010_detection_runs.py" | kind=code-symbol | source=manager/backend/alembic/versions/0010_detection_runs.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Temporal detection: detection_runs tabl…, 2885afa Add comprehensive probe testing…]
- "versions_0011_job_lease": "0011_job_lease.py" | kind=code-symbol | source=manager/backend/alembic/versions/0011_job_lease.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Job leasing: scan_jobs.lease_expires_at…, 2885afa Add comprehensive probe testing…]
- "versions_0012_agent_recommendations": "0012_agent_recommendations.py" | kind=code-symbol | source=manager/backend/alembic/versions/0012_agent_recommendations.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Agentic AI advisor: agent_recommendatio…, 2885afa Add comprehensive probe testing…]
- "versions_0013_agent_public_key": "0013_agent_public_key.py" | kind=code-symbol | source=manager/backend/alembic/versions/0013_agent_public_key.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, downgrade(), upgrade(), Add agents.public_key (Phase-4 X25519 i…, 2885afa Add comprehensive probe testing…]
- "versions_0024_device_role_inventory": "0024_device_role_inventory.py" | kind=code-symbol | source=manager/backend/alembic/versions/0024_device_role_inventory.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, downgrade(), upgrade(), Device-role inventory: persist the prob…, # NOTE: Postgres cannot DROP a single e…]
- "vuln_enrichment_vulnenrichmentservice_enrich": ".enrich()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L105 | neighbors=[Add NVD CVSS, EPSS, KEV flag, MITRE tec…, VulnEnrichmentService, .get(), .compute_composite_risk(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_fetch_mitre_techniques": ".fetch_mitre_techniques()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L270 | neighbors=[Returns MITRE ATT&CK technique IDs link…, VulnEnrichmentService, ._fetch_all(), .get(), .fetch_nvd()]
- "vuln_enrichment_vulnenrichmentservice_fetch_nvd": ".fetch_nvd()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L163 | neighbors=[Returns {cvss_v3, cvss_vector, descript…, VulnEnrichmentService, ._fetch_all(), .fetch_mitre_techniques(), .get()]
- "vuln_nessus_nessusscanner_create_scan": ".create_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L94 | neighbors=[NessusScanner, ._get_client(), ._get_template_uuid(), Returns nessus scan_id as string., Returns nessus scan_id as string.]
- "vuln_nessus_nessusscanner_get_results": ".get_results()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L166 | neighbors=[NessusScanner, ._get_client(), ._get_plugin_detail(), Returns list of raw finding dicts from …, Returns list of raw finding dicts from …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
