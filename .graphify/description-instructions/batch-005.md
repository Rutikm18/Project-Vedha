# Node Description Batch 6 of 227

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c4386e4cbc0ee346a71c211a96326772b677c561": "c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug" | kind=Commit | source=git | neighbors=[ae08d19 feat(scanner): adaptive timeout…, main.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 2fcec73 feat(verification): stamp verdi…, 8cf23c2 feat(resolution): wire coverage…, 937737b feat(resolution): reopen + flag…, d1b4dd3 trim frontend to 7 core pages; …]
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L55 | neighbors=[worker.py, ._banner_grab_all(), ._grab_one(), .__init__(), .run(), ._run_nmap()]
- "lib_assistant": "assistant.ts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L1 | neighbors=[page.tsx, AdvisorFlow.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, 1fe16c8 stable but some dead code, need…]
- "lib_backend_bearerfrom": "bearerFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L97 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "main_scripts_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner]
- "main_scripts_service_enum": "service_enum.py" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L1 | neighbors=[2534404 scanner(service_enum): commit o…, 78d51c5 opsec(scanner): de-sign service…, daf3de2 feat(scanner): add service enum…, classify_roles(), _dns_read_name(), Enrichment]
- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, FindingImport, _finish_cancelled_nuclei_job()]
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/scanner/db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, e8262a3 feat(probe): explicit unauthent…, DBScanner, interpret_redis_info(), main()]
- "scanner_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner]
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/scanner/port_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 9c973dd feat(scanner): tarpit/honeypot …, ae08d19 feat(scanner): adaptive timeout…]
- "scanner_service_enum": "service_enum.py" | kind=code-symbol | source=probe/scanner/service_enum.py:L1 | neighbors=[2534404 scanner(service_enum): commit o…, 78d51c5 opsec(scanner): de-sign service…, classify_roles(), _dns_read_name(), Enrichment, guess_os()]
- "tests_test_cli": "test_cli.py" | kind=code-symbol | source=probe/tests/test_cli.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, FakeClient, test_cmd_daemon_run_overrides_stale_env…, test_cmd_doctor_fails_when_no_agent_unl…, test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…]
- "tests_test_detection_core_testasset": "TestAsset" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L128 | neighbors=[test_detection_core.py, .test_add_alias(), .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports()]
- "tests_test_detection_core_testcvss": "TestCvss" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L280 | neighbors=[test_detection_core.py, .test_known_vectors(), .test_parse_vector(), .test_returns_none_for_malformed(), .test_returns_none_for_v2_vector(), .test_roundup_exact_boundary()]
- "tests_test_detection_core_testenrichfinding": "TestEnrichFinding" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L786 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testingestvalidation": "TestIngestValidation" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L184 | neighbors=[test_detection_core.py, .test_empty_target(), .test_missing_required_field(), .test_non_dict_record(), .test_port_not_int(), .test_valid_record()]
- "tests_test_detection_core_testnormalizedb": "TestNormalizeDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L932 | neighbors=[test_detection_core.py, .test_mysql_mariadb_engine_with_mariadb…, .test_mysql_mariadb_engine_without_mari…, .test_no_version_confidence_low(), .test_postgresql(), .test_unknown_engine()]
- "tests_test_detection_validation_testsigmarulegenerator": "TestSigmaRuleGenerator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L146 | neighbors=[test_detection_validation.py, .setup_method(), .test_evidence_customises_rule(), .test_known_technique_template(), .test_output_is_valid_yaml_and_stable_i…, .test_subtechnique_falls_back_to_parent…]
- "tests_test_exploit_engine_testnucleiexploitrunner": "TestNucleiExploitRunner" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L349 | neighbors=[test_exploit_engine.py, .setup_method(), .test_evidence_truncated_to_max_bytes(), .test_extract_evidence_includes_curl(), .test_nonexistent_template_not_safe(), .test_parse_poc_output_hit()]
- "tests_test_exploit_engine_testvalidatepayload": "TestValidatePayload" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L62 | neighbors=[test_exploit_engine.py, .test_allowed_payload_passes(), .test_bind_shell_blocked(), .test_encrypt_payload_blocked(), .test_generic_none_always_allowed(), .test_meterpreter_blocked()]
- "tests_test_new_scanners_testudpprobeconstruction": "TestUDPProbeConstruction" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L121 | neighbors=[test_new_scanners.py, .test_ike_probe_header_fields(), .test_ike_probe_init_spi_not_zero(), .test_ike_probe_length_field_matches_ac…, .test_ike_probe_resp_spi_zero(), .test_interpret_ike_short_data()]
- "tests_test_portal_read": "test_portal_read.py" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, _added(), _client(), _db_first(), _db_for_create()]
- "workflow_modes": "modes.py" | kind=code-symbol | source=probe/workflow/modes.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_workflow_execution.py]
- "auth_startup": "startup.py" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L1 | neighbors=[config.py, database.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@10ceacaffacf60f95eeb0e9b2b247b62bfa5dfb8": "10ceaca feat: implement AI model fallback mechanism and enhance model selection…" | kind=Commit | source=git | neighbors=[AssistantDrawer.tsx, ModelSwitcher.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@8ebc0534dda8a1316f41c2fccf928f42acf9ed46": "8ebc053 feat(risk-rank-ui): surface verification + lifecycle state on findings …" | kind=Commit | source=git | neighbors=[6a1c958 docs(plans): record execution s…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bb0ef3d473623bac3404761b5c3d34baa72612dd": "bb0ef3d feat(probe): route DB services on non-standard ports via banner signatu…" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans]
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …, GET, positiveInt()]
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L1 | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, 2b4ff71 feat(fleet): one-click Approve …, 30261eb feat: enhance advisor flow with…, a4b970c feat(fleet): add run command fo…, b5ffcb0 Refactor Vedha probe installer …, c4386e4 feat(customers): operator Custo…]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, DashboardCharts.tsx, DashboardGrid.tsx, ExposureCards.tsx]
- "main_scripts_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, build_client_hello(), cipher_code(), _ext(), fingerprint_host()]
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L1 | neighbors=[2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, ae08d19 feat(scanner): adaptive timeout…, build_ip_header()]
- "scanner_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, build_client_hello(), cipher_code(), _ext(), fingerprint_host()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-005.json

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
