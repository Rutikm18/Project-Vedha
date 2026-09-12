# Node Description Batch 11 of 380

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

- "routers_vuln_scans": "vuln_scans.py" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, FindingImport, _finish_cancelled_nuclei_job()] | lang=en
- "scanner_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L1 | neighbors=[37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner] | lang=en
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …] | lang=en
- "scanner_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, build_client_hello(), cipher_code(), _ext()] | lang=en
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 10fce13 feat(probe): observe web auth s…, 37376de hardening(scanner): OPSEC de-si…, 7a637eb feat: network VA accuracy, KEV …, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
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
- "tests_test_scope_model": "test_scope_model.py" | kind=code-symbol | source=probe/tests/test_scope_model.py:L1 | neighbors=[dbe9b78 Phase 1: typed-scope model (sco…, test_active_segment_requires_site_and_v…, test_classify_container_and_virtual(), test_classify_loopback(), test_classify_physical_default(), test_classify_tunnel()] | lang=en
- "tests_test_stage2_reconcile": "test_stage2_reconcile.py" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _CM, _hb(), _job(), _rows(), _run()] | lang=en
- "ai_llm_report": "llm_report.py" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[_collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, LLMUnavailableError, _normalize_ai_plan()] | lang=en
- "ai_llm_report_llmunavailableerror": "LLMUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L48 | neighbors=[llm_report.py, ._complete(), RuntimeError, Raised when the Anthropic SDK or API ke…, Raised when the Anthropic SDK or API ke…, Raised when the Anthropic SDK or API ke…] | lang=en
- "assistant_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/assistant/page.tsx:L1 | neighbors=[page.tsx, AIBrainWorkspace(), PortalAssistantPage(), 198bae4 snapshot: uncommitted system/ui…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…] | lang=en
- "branch:repo:github.com/Rutikm18/Project-Vedha#spike/probe-go": "spike/probe-go" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5c8e696 docs(probe): correct overclaimi…, 80b6dbc Remove environment secrets from…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@25344045b42fb3f74183072c0b432ee8c30db287": "2534404 scanner(service_enum): commit owner's in-progress changes as-is + re-sy…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2b4ff7132c98967429d138e7459f25f879023fc7": "2b4ff71 feat(fleet): one-click Approve Site — optional name, no code/fields (it…" | kind=Commit | source=git | neighbors=[route.ts, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@aedddfae1bea375d5864f92e26f2ceb7f0bf8065": "aedddfa feat(settings): editable SLA policy windows wired to backend (item 4 UI)" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ce7ab6ece1d67087d6bcbcf4062da2676390bc6e": "ce7ab6e Merge origin/main: reconcile findings + reports evidence work" | kind=Commit | source=git | neighbors=[76240ac UI UX Update, page.tsx, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@eff17d69ed457a0f00a6cec466932ff1357fb74f": "eff17d6 feat(probe): one-click approve endpoint — no code, auto name/caps/scope…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3bb8dba0a692bc5cd7881b8be1ce1529f8f659a": "f3bb8db feat(manager): cross-worker WS backplane + agent job-history + fleet qu…" | kind=Commit | source=git | neighbors=[3565ada fix(ingest): NUL-safe result su…, main.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f8ff2296e5ec2c593a6bed4ab40633d8a857d40f": "f8ff229 feat(ui): remove decorative session clock from both dashboards (item 6)" | kind=Commit | source=git | neighbors=[ecbb4ad feat(agent): rules-of-engagemen…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@fc7afc36732bf000de12e42189e63124bd643652": "fc7afc3 chore(graphify): refresh knowledge graph for remediation subsystem" | kind=Commit | source=git | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "exploit_nuclei_exploit_nucleiexploitrunner": "NucleiExploitRunner" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L47 | neighbors=[nuclei_exploit.py, ._extract_evidence(), ._parse_poc_output(), .run_cve_poc(), .safe_template_check(), Run Nuclei CVE PoC templates against a …] | lang=en
- "launch_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, a789cca scanner: real use-case library,…, POST] | lang=en
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/login/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10ceaca feat: implement AI model fallba…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…] | lang=en
- "main_scripts_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext()] | lang=en
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…] | lang=en
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _detect_drift(), _hash()] | lang=en
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ._ldap_with_users(), .setup_method(), .test_finding_critical_when_privileged(), .test_finding_high_when_not_privileged(), .test_get_spn_accounts_filters_krbtgt_a…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-010.json

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
