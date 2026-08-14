# Node Description Batch 5 of 186

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

- "lib_clients_store": "clients-store.ts" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, ClientJiraConfig, ClientNotifyConfig, ClientSettings, ClientsFile]
- "lib_openvas_client": "openvas-client.ts" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, findings-store.ts, FindingSeverity, boundedEnvMs()]
- "models_enums_assetcriticality": "AssetCriticality" | kind=code-symbol | source=manager/backend/app/models/enums.py:L33 | neighbors=[enums.py, str, Asset, Attack path analysis API (AttackPathSer…, AssetIn, AssetOut]
- "services_llm_managerllmservice": "ManagerLlmService" | kind=code-symbol | source=manager/backend/app/services/llm.py:L74 | neighbors=[llm.py, ._anthropic(), ._auto_cloud_provider(), ._build_system(), ._client(), ._default_runtime()]
- "tests_test_agents": "test_agents.py" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, TestAccessTokenExpiry]
- "tests_test_detection_core_testdeceptionscore": "TestDeceptionScore" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L616 | neighbors=[test_detection_core.py, .test_capped_at_1(), .test_combined_high(), .test_contradictory_os(), .test_high_product_count(), .test_low_product_count()]
- "tests_test_detection_core_testingestfile": "TestIngestFile" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L220 | neighbors=[test_detection_core.py, .test_authoritative_scanner_creates_aut…, .test_empty_file(), .test_hostname_target_not_ip_keyed(), .test_multi_file_accumulation(), .test_quarantines_malformed()]
- "vuln_nuclei_nucleiscanerror": "NucleiScanError" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L89 | neighbors=[nuclei.py, RuntimeError, .__init__(), ._partial_or_raise(), .run_scan(), Fatal Nuclei failure, optionally carryi…]
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=probe/agent/use_cases.py:L1 | neighbors=[task_runner.py, _as_int(), normalize_intensity(), resolve(), use_case_for_code(), use_cases.py — the finite, pre-defined …]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/probe-usecase-alignment": "feat/probe-usecase-alignment" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "commands_interactive_confirm": "confirm()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L79 | neighbors=[interactive.ts, ask(), mainMenu(), pickHostSubset(), pickModulesByCategory(), pickTargets()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65f22a7e7696fead81236a6770771f450c0d15a6": "65f22a7 Add comprehensive tests for authentication and admin seeding- Implement…" | kind=Commit | source=git | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, main.py, AssistantDrawer.tsx, exceptions.py, router.py, startup.py]
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L55 | neighbors=[worker.py, ._banner_grab_all(), ._grab_one(), .__init__(), .run(), ._run_nmap()]
- "lib_assistant": "assistant.ts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L1 | neighbors=[page.tsx, AdvisorFlow.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, 1fe16c8 stable but some dead code, need…]
- "probe_pipeline": "pipeline.py" | kind=code-symbol | source=probe/pipeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _clean(), _Collector, _ip_key(), main(), _render_summary()]
- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, FindingImport, _finish_cancelled_nuclei_job()]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, classify_cipher()]
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
- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 81c81cb feat: implement outbox reclaim …, database.py, _claim_batch(), _dead_letter_stale_stmt(), enqueue()]
- "workflow_modes": "modes.py" | kind=code-symbol | source=probe/workflow/modes.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_workflow_execution.py]
- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, _atomic_write_private_state(), _sync_directory(), Transport, TransportError, transport.py — all manager communicatio…]
- "auth_startup": "startup.py" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L1 | neighbors=[config.py, database.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2fcec73 feat(verification): stamp verdi…, 8cf23c2 feat(resolution): wire coverage…, 937737b feat(resolution): reopen + flag…, d1b4dd3 trim frontend to 7 core pages; …, config.py]
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …, GET, positiveInt()]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, DashboardCharts.tsx, DashboardGrid.tsx, ExposureCards.tsx]
- "main_scripts_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, main()]
- "main_scripts_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner, main()]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _ConnectSweep, _have_masscan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-004.json

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
