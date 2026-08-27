# Node Description Batch 7 of 236

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

- "tests_test_detection_core_testingestvalidation": "TestIngestValidation" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L184 | neighbors=[test_detection_core.py, .test_empty_target(), .test_missing_required_field(), .test_non_dict_record(), .test_port_not_int(), .test_valid_record()]
- "tests_test_detection_core_testnormalizedb": "TestNormalizeDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L932 | neighbors=[test_detection_core.py, .test_mysql_mariadb_engine_with_mariadb…, .test_mysql_mariadb_engine_without_mari…, .test_no_version_confidence_low(), .test_postgresql(), .test_unknown_engine()]
- "tests_test_detection_validation_testsigmarulegenerator": "TestSigmaRuleGenerator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L146 | neighbors=[test_detection_validation.py, .setup_method(), .test_evidence_customises_rule(), .test_known_technique_template(), .test_output_is_valid_yaml_and_stable_i…, .test_subtechnique_falls_back_to_parent…]
- "tests_test_exploit_engine_testnucleiexploitrunner": "TestNucleiExploitRunner" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L349 | neighbors=[test_exploit_engine.py, .setup_method(), .test_evidence_truncated_to_max_bytes(), .test_extract_evidence_includes_curl(), .test_nonexistent_template_not_safe(), .test_parse_poc_output_hit()]
- "tests_test_exploit_engine_testvalidatepayload": "TestValidatePayload" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L62 | neighbors=[test_exploit_engine.py, .test_allowed_payload_passes(), .test_bind_shell_blocked(), .test_encrypt_payload_blocked(), .test_generic_none_always_allowed(), .test_meterpreter_blocked()]
- "tests_test_new_scanners_testudpprobeconstruction": "TestUDPProbeConstruction" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L121 | neighbors=[test_new_scanners.py, .test_ike_probe_header_fields(), .test_ike_probe_init_spi_not_zero(), .test_ike_probe_length_field_matches_ac…, .test_ike_probe_resp_spi_zero(), .test_interpret_ike_short_data()]
- "tests_test_portal_read": "test_portal_read.py" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, _added(), _client(), _db_first(), _db_for_create()]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 63d9c9a fix(probe): recover from 409 wh…, 81c81cb feat: implement outbox reclaim …, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1226 | neighbors=[agent.py, main(), _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device()]
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L534 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _derive_post_stage(), _error_result(), _facts_from_cache()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@0b7bcb82f82922f901d24413b10ed114e096a3a7": "0b7bcb8 feat: probe bootstrap key — self-register without admin login" | kind=Commit | source=git | neighbors=[agent.py, transport.py, config.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c6aa54b98c0dc182941305bf241ca956f806193": "5c6aa54 feat(portal-ui): portal shell/pages restyle + settings page" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans, fix/probe-already-enrolled-409]
- "commit:repo:github.com/Rutikm18/Project-Vedha@ae08d19a6e9e90cc033a56b4aaeea1424c557da7": "ae08d19 feat(scanner): adaptive timeout, SYN retransmit, top-100 default (accur…" | kind=Commit | source=git | neighbors=[65e5684 feat(probe): transparent job lo…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c76b4287cfd451cab1e1212934ab3f6f36445eb6": "c76b428 backend and login page error handling update" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …]
- "findings_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …, GET, positiveInt()]
- "lib_fetcher_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L29 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, DashboardCharts.tsx, DashboardGrid.tsx, ExposureCards.tsx]
- "lib_with_backend_withbackend": "withBackend()" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L22 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "main_scripts_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, build_client_hello(), cipher_code(), _ext(), fingerprint_host()]
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L1 | neighbors=[2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, ae08d19 feat(scanner): adaptive timeout…, build_ip_header()]
- "scanner_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, build_client_hello(), cipher_code(), _ext(), fingerprint_host()]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, classify_cipher(), _get_cert_der()]
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _detect_drift(), _hash()]
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ._ldap_with_users(), .setup_method(), .test_finding_critical_when_privileged(), .test_finding_high_when_not_privileged(), .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_async_udp": "test_async_udp.py" | kind=code-symbol | source=probe/tests/test_async_udp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, _SinkProtocol, _start_server()]
- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L32 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…]
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L75 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1053 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), ConsistencyReport]
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L595 | neighbors=[test_detection_core.py, .test_authoritative_tier4(), .test_multi_signal_tier2(), .test_protocol_scanner_tier3(), .test_single_banner_tier1(), ConsistencyReport]
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L560 | neighbors=[test_detection_core.py, .test_no_smb_facts_returns_none(), .test_smbv1_with_missing_hotfixes_retur…, .test_smbv1_with_patched_host_returns_n…, .test_smbv1_without_hotfix_data_returns…, ConsistencyReport]
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L483 | neighbors=[test_detection_core.py, .test_authoritative_upgrades_state(), .test_different_ids_preserved(), .test_evidence_refs_dedup_preserving_or…, .test_merges_same_id(), ConsistencyReport]
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1027 | neighbors=[test_detection_core.py, .test_classification_intermittent(), .test_classification_mostly_stable(), .test_classification_stable(), .test_rate(), ConsistencyReport]
- "tests_test_detection_core_testsuppressnegated": "TestSuppressNegated" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L516 | neighbors=[test_detection_core.py, .test_keeps_authoritative_finding(), .test_keeps_inferred_when_auth_version_…, .test_keeps_inferred_when_no_authoritat…, .test_suppresses_inferred_when_authorit…, ConsistencyReport]
- "tests_test_detection_core_testwilsonci": "TestWilsonCi" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1008 | neighbors=[test_detection_core.py, .test_all_appearances(), .test_perfect_appearance(), .test_zero_appearances(), .test_zero_n(), ConsistencyReport]
- "tests_test_detection_validation_testsiemparsing": "TestSIEMParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L186 | neighbors=[test_detection_validation.py, .test_elastic_parse(), .test_factory(), .test_sentinel_parse(), .test_splunk_parse(), .test_splunk_spl_includes_host_and_time…]
- "tests_test_manager_ai": "test_manager_ai.py" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 75650c1 feat: add Posture & Patch-Compa…, config.py, _cloud(), test_ai_request_rejects_unsafe_model_an…, test_default_auto_detect_prefers_openai…]
- "tests_test_service_identifier_testserviceidentifier": "TestServiceIdentifier" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L6 | neighbors=[test_service_identifier.py, ._id(), .setup_method(), .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined()]
- "tests_test_syn_scanner": "test_syn_scanner.py" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, ae08d19 feat(scanner): adaptive timeout…, scanner_base.py, _synack_with_options(), TestAdaptiveTimeoutToggle]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-006.json

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
