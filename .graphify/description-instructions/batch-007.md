# Node Description Batch 8 of 332

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

- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L361 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _default_host_concurrency(), _finalize_trace(), _gather_per_host(), _port_candidates()] | lang=en
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L555 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _derive_post_stage(), _error_result(), _facts_from_cache()] | lang=en
- "app_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L1 | neighbors=[metadata, RootLayout(), AssistantProvider.tsx, AssistantProvider(), QueryProvider.tsx, QueryProvider()] | lang=en
- "auth_startup": "startup.py" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L1 | neighbors=[config.py, database.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()] | lang=en
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/probe-usecase-alignment": "feat/probe-usecase-alignment" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…] | lang=en
- "commands_interactive_confirm": "confirm()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L79 | neighbors=[interactive.ts, ask(), mainMenu(), pickHostSubset(), pickModulesByCategory(), pickTargets()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@58c2d10f572ed4b7fce3da53bb9f95b696c4b94f": "58c2d10 feat(active-validation): ValidationRequest model + migration" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c140451c247068bc76251c851f7936cbeeb8a0ac": "c140451 fix(portal): clean 409 on duplicate-email provision + 7-day session ref…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f00ce5fb2e9537f4630e4bf1ff0326b3f6422ffe": "f00ce5f fix(ui): session-timer persistence, hydration-safe count-up, security h…" | kind=Commit | source=git | neighbors=[88c9278 feat(ai): pin manager LLM pipel…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@fbe7450ad544cc4fced845b4b28720d54fe802b9": "fbe7450 Add comprehensive documentation for Playwright CLI features- Introduced…" | kind=Commit | source=git | neighbors=[llm_report.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, b393dbe feat: Enhance Sidebar UI and in…] | lang=en
- "discovery_worker_discoveryworker": "DiscoveryWorker" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L55 | neighbors=[worker.py, ._banner_grab_all(), ._grab_one(), .__init__(), .run(), ._run_nmap()] | lang=en
- "main_scripts_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner] | lang=en
- "main_scripts_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, build_client_hello(), cipher_code(), _ext()] | lang=en
- "prompts_report": "report.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ai-engine.ts, buildReportUserMessage(), buildScorecard(), Confidence, DOMAINS] | lang=en
- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, FindingImport, _finish_cancelled_nuclei_job()] | lang=en
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/scanner/db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, e8262a3 feat(probe): explicit unauthent…, DBScanner, interpret_redis_info(), main()] | lang=en
- "scanner_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner] | lang=en
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …] | lang=en
- "scanner_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, build_client_hello(), cipher_code(), _ext()] | lang=en
- "tests_test_branch_registry": "test_branch_registry.py" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, _asset_with(), _fake(), test_datagram_branches_need_no_tcp_stag…] | lang=en
- "tests_test_cli": "test_cli.py" | kind=code-symbol | source=probe/tests/test_cli.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, FakeClient, test_cmd_daemon_run_overrides_stale_env…, test_cmd_doctor_fails_when_no_agent_unl…, test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…] | lang=en
- "tests_test_detection_core_testasset": "TestAsset" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L134 | neighbors=[test_detection_core.py, .test_add_alias(), .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports()] | lang=en
- "tests_test_detection_core_testcvss": "TestCvss" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L322 | neighbors=[test_detection_core.py, .test_known_vectors(), .test_parse_vector(), .test_returns_none_for_malformed(), .test_returns_none_for_v2_vector(), .test_roundup_exact_boundary()] | lang=en
- "tests_test_detection_core_testenrichfinding": "TestEnrichFinding" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L855 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()] | lang=en
- "tests_test_detection_core_testingestvalidation": "TestIngestValidation" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L190 | neighbors=[test_detection_core.py, .test_empty_target(), .test_missing_required_field(), .test_non_dict_record(), .test_port_not_int(), .test_valid_record()] | lang=en
- "tests_test_detection_core_testnormalizedb": "TestNormalizeDb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1001 | neighbors=[test_detection_core.py, .test_mysql_mariadb_engine_with_mariadb…, .test_mysql_mariadb_engine_without_mari…, .test_no_version_confidence_low(), .test_postgresql(), .test_unknown_engine()] | lang=en
- "tests_test_detection_core_testsuppressnegated": "TestSuppressNegated" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L558 | neighbors=[test_detection_core.py, .test_keeps_authoritative_finding(), .test_keeps_inferred_when_auth_version_…, .test_keeps_inferred_when_no_authoritat…, .test_suppresses_inferred_when_authorit…, .test_suppression_produces_an_evidence_…] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator": "TestSigmaRuleGenerator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L173 | neighbors=[test_detection_validation.py, .setup_method(), .test_evidence_customises_rule(), .test_known_technique_template(), .test_output_is_valid_yaml_and_stable_i…, .test_subtechnique_falls_back_to_parent…] | lang=en
- "tests_test_exploit_engine_testnucleiexploitrunner": "TestNucleiExploitRunner" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L349 | neighbors=[test_exploit_engine.py, .setup_method(), .test_evidence_truncated_to_max_bytes(), .test_extract_evidence_includes_curl(), .test_nonexistent_template_not_safe(), .test_parse_poc_output_hit()] | lang=en
- "tests_test_exploit_engine_testvalidatepayload": "TestValidatePayload" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L62 | neighbors=[test_exploit_engine.py, .test_allowed_payload_passes(), .test_bind_shell_blocked(), .test_encrypt_payload_blocked(), .test_generic_none_always_allowed(), .test_meterpreter_blocked()] | lang=en
- "tests_test_host_discovery_udp": "test_host_discovery_udp.py" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, host_discovery.py, scanner_base.py, _closed_udp_port(), _nbstat_reply()] | lang=en
- "tests_test_new_scanners_testudpprobeconstruction": "TestUDPProbeConstruction" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L121 | neighbors=[test_new_scanners.py, .test_ike_probe_header_fields(), .test_ike_probe_init_spi_not_zero(), .test_ike_probe_length_field_matches_ac…, .test_ike_probe_resp_spi_zero(), .test_interpret_ike_short_data()] | lang=en
- "tests_test_portal_read": "test_portal_read.py" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, _added(), _client(), _db_first(), _db_for_create()] | lang=en
- "tests_test_stage2_reconcile": "test_stage2_reconcile.py" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _CM, _hb(), _job(), _rows(), _run()] | lang=en
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 63d9c9a fix(probe): recover from 409 wh…, 81c81cb feat: implement outbox reclaim …, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-007.json

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
